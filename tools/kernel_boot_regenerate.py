#!/usr/bin/env python3
"""Stub implementation of kernel.boot.regenerate.

Reads canonical files, emits a BOOT_SUMMARY.latest.json, and records hashes.
Not production-grade; meant for dry-run validation only.
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

INPUTS = [
    "persona.md",
    "guardrails.md",
    "mandates/definitions",
    "tasks/index.json",
    "ai_context/model_preferences.md",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_inputs(root: Path):
    collected = []
    for rel in INPUTS:
        p = root / rel
        entry = {"path": rel, "exists": p.exists(), "type": "dir" if p.is_dir() else "file"}
        if p.exists() and p.is_file():
            entry["sha256"] = sha256_file(p)
        if p.exists() and p.is_dir():
            entry["count"] = len(list(p.iterdir()))
        collected.append(entry)
    return collected


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace", type=Path, help="Workspace root")
    ap.add_argument("--responsibility-id", help="Override responsibility id")
    ap.add_argument("--log-dir", type=Path, help="Optional boot_trial_logs dir")
    args = ap.parse_args()

    ws = args.workspace
    if not ws.exists():
        print(f"workspace not found: {ws}", file=sys.stderr)
        return 2

    rid = args.responsibility_id or ws.name
    generated_at = datetime.now(timezone.utc).isoformat()
    inputs = collect_inputs(ws)
    summary = {
        "responsibility_id": rid,
        "generated_at": generated_at,
        "source": "kernel.boot.regenerate_stub",
        "inputs": inputs,
    }

    out_path = ws / "BOOT_SUMMARY.latest.json"
    out_path.write_text(json.dumps(summary, indent=2))
    print(f"wrote BOOT_SUMMARY to {out_path}")

    if args.log_dir:
        args.log_dir.mkdir(parents=True, exist_ok=True)
        log_path = args.log_dir / f"boot_summary_{rid}.json"
        log_path.write_text(json.dumps(summary, indent=2))
        print(f"logged summary to {log_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
