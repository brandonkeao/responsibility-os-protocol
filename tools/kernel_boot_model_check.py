#!/usr/bin/env python3
"""Stub implementation of kernel.boot.model_check.

Compares actual model against preferred/allowed models from ai_context/model_preferences.md.
Outputs a simple status and optional log file. Not production-grade.
"""
import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path


def parse_model_prefs(path: Path):
    prefs = {"preferred_model": None, "allowed_models": []}
    if not path.exists():
        return prefs
    preferred = None
    allowed = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("-"):
                allowed.append(line.lstrip("- "))
            elif ":" in line:
                key, val = line.split(":", 1)
                key = key.strip()
                val = val.strip()
                if key == "preferred_model":
                    preferred = val
                elif key == "allowed_models":
                    allowed = []
    prefs["preferred_model"] = preferred
    prefs["allowed_models"] = allowed
    return prefs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace", type=Path, help="Workspace root")
    ap.add_argument("--actual-model", required=True, help="Runtime model id")
    ap.add_argument("--responsibility-id", help="Override responsibility id")
    ap.add_argument("--log-file", type=Path, help="Optional log file path")
    args = ap.parse_args()

    ws = args.workspace
    prefs_path = ws / "ai_context/model_preferences.md"
    prefs = parse_model_prefs(prefs_path)
    preferred = prefs.get("preferred_model")
    allowed = prefs.get("allowed_models", [])

    status = "ok"
    if preferred and args.actual_model != preferred and args.actual_model not in allowed:
        status = "warning"
    rid = args.responsibility_id or ws.name
    result = {
        "responsibility_id": rid,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "actual_model": args.actual_model,
        "preferred_model": preferred,
        "allowed_models": allowed,
        "status": status,
    }

    print(result)
    if args.log_file:
        args.log_file.parent.mkdir(parents=True, exist_ok=True)
        args.log_file.write_text(str(result))
    return 0 if status == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
