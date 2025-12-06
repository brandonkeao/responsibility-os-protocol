# mandate.task_worker.task_hydration

## Title
Hydrate Tasks from Kernel command queue into the Responsibility filesystem and external mirrors.

## Intent
Ensure every pending `kernel.tasks.issue` command is executed deterministically. The Task Worker updates Task files, mirrors eligible fields to Google Tasks/Calendar, and appends audit entries referencing the originating mandate or RequestForAction.

## Success Metrics
- All pending commands processed within the heartbeat window defined in `telemetry/policies.yaml`.
- Each Task file includes `mandate_run_id` or `request_id` references; missing references trigger Guardrails escalation.
- External mirrors (Google Tasks/Calendar) reflect current status within 5 minutes of updates.

## Constraints
- Guardrails clauses: `taskworker.sync_integrity`, `runtime.model_integrity`, `requests.sla_compliance`.
- Task Worker may not delete or overwrite Tasks; only append new records or status transitions.
- External providers are optional; if unavailable, log `task_sync.blocked` and notify the steward via RequestForAction.

## Handoff Plan
If the Task Worker automation is offline for more than two heartbeats, the steward Responsibility clones this mandate, runs a manual hydration, and records findings to `memory/events.md`.
