#!/usr/bin/env python3
"""Export RFAs from the stub queue to markdown mirrors under queue/inbox/.

Simulation helper only; expects the SQLite DB created by queue_scaffold.
"""
import argparse
import sqlite3
from pathlib import Path


def export_rfas(db_path: Path, workspace: Path, workspace_id: str | None):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    if workspace_id:
        cur.execute("SELECT id, status, payload, created_at, updated_at FROM rfas WHERE workspace_id=?", (workspace_id,))
    else:
        cur.execute("SELECT id, status, payload, created_at, updated_at, workspace_id FROM rfas")
    rows = cur.fetchall()
    conn.close()

    inbox_dir = workspace / "queue" / "inbox"
    inbox_dir.mkdir(parents=True, exist_ok=True)
    for row in rows:
        if workspace_id:
            rfa_id, status, payload, created_at, updated_at = row
            ws_id = workspace_id
        else:
            rfa_id, status, payload, created_at, updated_at, ws_id = row
        md_path = inbox_dir / f"{rfa_id}.md"
        md_path.write_text(
            f"---\n"
            f"workspace_id: {ws_id}\n"
            f"rfa_id: {rfa_id}\n"
            f"status: {status}\n"
            f"created_at: {created_at}\n"
            f"updated_at: {updated_at}\n"
            f"---\n\n"
            f"payload: {payload}\n"
        )
        print(f"wrote {md_path}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace", type=Path, help="Workspace root")
    ap.add_argument("--db", type=Path, help="SQLite path (default workspace/queue.sqlite)")
    ap.add_argument("--workspace-id", help="Filter by workspace_id; default uses workspace folder name")
    args = ap.parse_args()

    ws = args.workspace
    db_path = args.db or ws / "queue.sqlite"
    ws_id = args.workspace_id or ws.name
    if not db_path.exists():
        print(f"queue db not found: {db_path}")
        return 1
    export_rfas(db_path, ws, ws_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
