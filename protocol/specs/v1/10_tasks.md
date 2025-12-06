# Task Specification

Tasks are now first-class, append-only records that sit between Mandates and Responsibilities. They capture the exact unit of work the Kernel expects a Responsibility to execute and provide the bridge into external productivity suites (e.g., Google Workspace) via `google_workspace_mcp`.

## Purpose & Placement
- **Chain enforcement** – Tasks formalize the Mandate → Task → Responsibility → Action flow so every action cites both authority (mandate) and execution ownership (responsibility).
- **Context portability** – Tasks are stored in the Responsibility filesystem and replicated to trusted providers (Google Tasks, Calendar) without forfeiting protocol guarantees.
- **Tool interoperability** – Only the Task Worker may mutate Task state; LLMs and external automations must go through Kernel-issued commands.

## Canonical Schema

```json
{
  "task_id": "uuid",
  "title": "string",
  "description": "string",
  "mandate_id": "string",
  "preferred_responsibilities": ["string"],
  "status": "needs_action | in_progress | blocked | completed",
  "priority": "low | normal | high",
  "due_date": "iso8601 | null",
  "external_refs": {
    "google_task_id": "string | null",
    "calendar_event_id": "string | null"
  },
  "task_sync": {
    "state": "active | blocked | degraded",
    "last_heartbeat": "iso8601",
    "last_error": "string | null"
  },
  "source": "gmail | voice | manual | automation",
  "created_at": "iso8601",
  "updated_at": "iso8601"
}
```

Additional implementation notes:
- `preferred_responsibilities` guides routing when multiple Responsibilities share a mandate scope. Guardrails validate that every selected Responsibility can legally execute the Task.
- Status transitions follow `needs_action → in_progress → completed` with optional branches to `blocked`; only the Task Worker (operating under Kernel commands) can move between states.
- `priority` maps to deterministic queue weights (`low=300`, `normal=200`, `high=100` is the recommended encoding).
- `task_sync.state` communicates connector health:
  - `active` – credentials valid, last sync succeeded within `heartbeat_interval_seconds`.
  - `blocked` – OAuth missing or revoked; Responsibility must remediate before boot completes.
  - `degraded` – connector reachable but API errors persist; Guardrails may permit execution with warnings.
  Task Worker updates `last_heartbeat` and `last_error` automatically; manual edits are forbidden.

## Sync Model
1. **Internal Task Store** – Markdown or structured JSON files inside the Responsibility filesystem serve as the source of truth.
2. **Google Task Mirror** – `google_workspace_mcp` mirrors title, description, due date, and status to Google Tasks for steward visibility. Google-side IDs are stored under `external_refs.google_task_id`.
3. **Calendar Binding** – Optional `calendar_event_id` links blockers or deadlines to Google Calendar. Calendar deletions never delete Tasks; they simply clear the binding and log a memory event.

Sync bridges are one-way initiators: they may create or update external artifacts but must never delete or overwrite Tasks stored in the filesystem. Kernel logs every sync command, and Guardrails confirm that the Task Worker executed it successfully.

If `task_sync.state` transitions to `blocked` all dependent Responsibilities must halt Task execution (`kernel.tasks.issue` rejects commands) until OAuth credentials are restored. `degraded` state adds telemetry warnings but allows retries; exceeding `max_failed_tasks_per_day` escalates to Guardrails.

## Safety & Ownership
- Tasks are append-only. Deletion requires a Guardrails-approved migration with memory pointers.
- Only the Task Worker service may mutate status, priority, or due dates. Human operators must still invoke the Task Worker (or Kernel command) instead of editing files directly.
- Calendar or Gmail cleanup cannot cascade into Task removal.
- Every Task references a Mandate run ID and, when applicable, a RequestForAction ID; missing references cause the Kernel to halt execution.
- Tasks are strictly internal to a Responsibility/workspace; collaboration between Responsibilities always begins as an RFA even if Tasks eventually mirror the work.

## Migration Strategy
1. **Phase 1 – Gmail + Calendar + Tasks**: Stand up Task Worker + `google_workspace_mcp` connectors and confirm sync loops.
2. **Phase 2 – Internal Task DB**: Promote the filesystem-backed Task store to the source of truth, keeping Google Tasks as a convenience mirror.
3. **Phase 3 – Cross-System Routing**: Route Tasks between Responsibilities and external partners while preserving Mandate + Guardrails references.

Each migration phase must be recorded in `protocol/progress/PROGRESS_LOG.md` for downstream stewards.

## Implementation Checklist
- Add Task hydration to every Responsibility boot (Phase 3 in the boot template).
- Extend Kernel APIs with `kernel.tasks.issue(command)` and log Guardrails approvals.
- Update dashboards to show Task throughput (created, completed, blocked) per Responsibility alongside mandate runs and RequestForAction volume.
- Ensure LLM tooling reads Tasks from the filesystem and never attempts to mutate Google Tasks directly.
