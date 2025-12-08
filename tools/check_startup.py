#!/usr/bin/env python3
"""Quick, local-only startup checklist validator.

This is a lightweight helper for runbook simulations. It checks for required
files and emits a JSON report. It is not meant to be production-grade.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

REQUIRED = [
    "persona.md",
    "guardrails.md",
    "mandates/definitions",
    "tasks/index.json",
    "memory/events.md",
    "queue/inbox",
    "BOOT_SUMMARY.latest.json",
    "ai_context/model_preferences.md",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def build_report(root: Path) -> dict:
    items = []
    missing = 0
    for rel in REQUIRED:
        p = root / rel
        exists = p.exists()
        entry = {
            "path": rel,
            "exists": exists,
            "type": "dir" if p.is_dir() else "file",
        }
        if exists and p.is_file():
            entry["sha256"] = sha256_file(p)
        if exists and p.is_dir():
            entry["count"] = len(list(p.iterdir()))
        if not exists:
            missing += 1
        items.append(entry)
    status = "ok" if missing == 0 else "missing"
    return {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "workspace": str(root),
        "status": status,
        "missing": missing,
        "items": items,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace", type=Path, help="Path to workspace root")
    ap.add_argument("--report", type=Path, help="Write JSON report to path")
    args = ap.parse_args()

    if not args.workspace.exists():
        print(f"workspace not found: {args.workspace}", file=sys.stderr)
        return 2

    report = build_report(args.workspace)
    print(json.dumps(report, indent=2))
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2))
    return 0 if report["status"] == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
