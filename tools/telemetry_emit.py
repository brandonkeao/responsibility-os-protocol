#!/usr/bin/env python3
"""Emit stub telemetry events to local JSON files.

Supported event types: heartbeat, context_ingested, context_dispatched, model_mismatch_on_boot.
This is a simulation helper and not production-grade.
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

SUPPORTED = {"heartbeat", "context_ingested", "context_dispatched", "model_mismatch_on_boot"}


def emit_event(workspace: Path, responsibility_id: str, event_type: str, status: str, payload: dict):
    telemetry_dir = workspace / "telemetry"
    telemetry_dir.mkdir(parents=True, exist_ok=True)
    fname = f"{event_type}_{responsibility_id}_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    out_path = telemetry_dir / fname
    event = {
        "responsibility_id": responsibility_id,
        "event_type": event_type,
        "status": status,
        "payload": payload,
        "emitted_at": datetime.now(timezone.utc).isoformat(),
    }
    out_path.write_text(json.dumps(event, indent=2))
    print(f"wrote telemetry event to {out_path}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace", type=Path, help="Workspace root")
    ap.add_argument("--responsibility-id", required=True)
    ap.add_argument("--event-type", required=True, choices=sorted(SUPPORTED))
    ap.add_argument("--status", default="ok")
    ap.add_argument("--note", help="Optional note to include")
    args = ap.parse_args()

    payload = {}
    if args.note:
        payload["note"] = args.note
    emit_event(args.workspace, args.responsibility_id, args.event_type, args.status, payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
