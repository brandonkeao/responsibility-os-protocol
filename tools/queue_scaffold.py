#!/usr/bin/env python3
"""Create a lightweight SQLite queue for RFAs.

This is a stub for simulations only. It creates tables and an optional sample row.
"""
import argparse
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS rfas (
  id TEXT PRIMARY KEY,
  workspace_id TEXT NOT NULL,
  status TEXT NOT NULL,
  payload TEXT NOT NULL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace", type=Path, help="Workspace root")
    ap.add_argument("--db", type=Path, help="SQLite path (default: workspace/queue.sqlite)")
    ap.add_argument("--add-sample", action="store_true", help="Insert a sample open RFA")
    args = ap.parse_args()

    ws = args.workspace
    db_path = args.db or ws / "queue.sqlite"
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.executescript(SCHEMA)

    if args.add_sample:
        now = datetime.now(timezone.utc).isoformat()
        rfa_id = f"rfa_sample_{now.replace(':', '-')[:19]}"
        payload = {
            "type": "ingest_new_context",
            "notes": "sample RFA created by queue_scaffold",
        }
        cur.execute(
            "INSERT OR IGNORE INTO rfas (id, workspace_id, status, payload, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
            (rfa_id, ws.name, "open", str(payload), now, now),
        )
    conn.commit()
    conn.close()
    print(f"queue ready at {db_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
