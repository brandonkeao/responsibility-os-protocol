#!/usr/bin/env python3
"""Stub task hydration command.

Updates tasks/index.json with a task_sync state and timestamp. Not production-grade.
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_INDEX = {
    "tasks": [],
    "task_sync": {
        "state": "needs_action",
        "last_synced_at": None
    }
}


def load_index(path: Path):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(DEFAULT_INDEX, indent=2))
    try:
        return json.loads(path.read_text())
    except Exception:
        return DEFAULT_INDEX.copy()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace", type=Path, help="Workspace root")
    ap.add_argument("--state", default="active", help="task_sync.state value")
    args = ap.parse_args()

    ws = args.workspace
    index_path = ws / "tasks/index.json"
    data = load_index(index_path)
    data.setdefault("task_sync", {})
    data["task_sync"]["state"] = args.state
    data["task_sync"]["last_synced_at"] = datetime.now(timezone.utc).isoformat()
    index_path.write_text(json.dumps(data, indent=2))
    print(f"hydration stub updated {index_path} with state={args.state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
