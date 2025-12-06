# responsibility.task_worker

## Purpose
Provide a reusable Task Worker Responsibility that every workspace can clone to hydrate Tasks, mirror them to external systems, and surface blocked work to stewards.

## Scope
- Execute Kernel-issued Task commands (`kernel.tasks.issue`) under Guardrails oversight.
- Maintain the canonical Task store under `tasks/` plus append-only sync logs.
- Mirror Task metadata to approved external providers (e.g., Google Tasks, Calendar) via the Task Worker mandates.
- Emit RequestForAction entries when Tasks cannot be routed to a Responsibility or require human review.

## Interfaces
- **Kernel**: `kernel.tasks.issue`, `kernel.telemetry.write`.
- **Guardrails**: `taskworker.sync_integrity`, `runtime.model_integrity`.
- **External**: `google_workspace_mcp` (optional), future provider stubs.

## Operating Notes
- Task Worker runs headless but logs every action to `memory/events.md` with `(kernel_decision_id, guardrail_clause_id, task_id)` tuples.
- If external providers are unavailable, Task Worker marks `task_sync.blocked` and emits a RequestForAction targeting the steward Responsibility.
- Telemetry metrics must follow the workspace `telemetry/policies.yaml` thresholds (e.g., heartbeat ≤ 60s, sync duration ≤ 30s).
