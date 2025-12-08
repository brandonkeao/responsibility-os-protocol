---
layer: ops_infrastructure
change_risk: medium
---

# Task Specification

Tasks are now first-class, append-only records that sit between Mandates and Responsibilities. They capture the exact unit of work the Kernel expects a Responsibility to execute. Cross-responsibility asks flow through RFAs; once accepted, the target Responsibility creates and executes its own Tasks inside its portable container.

## Purpose & Placement
- **Chain enforcement** – Tasks formalize the Mandate → Task → Responsibility → Action flow so every action cites both authority (mandate) and execution ownership (responsibility).
- **Responsibility ownership first** – Each Responsibility creates and executes its own Tasks inside its container after accepting an RFA; no Responsibility may place Tasks into another’s container.
- **Context portability** – Tasks live in the Responsibility filesystem (`registry/<responsibility_id>/tasks/inbound|outbound`) so they travel with the container; optional mirrors to external suites must never override the filesystem source of truth.
- **Tool interoperability** – Only the Task Worker may mutate Task state; LLMs and automations go through Kernel-issued commands.
- **Placement** – Global task queues are optional; per-Responsibility tasks reside in the portable container at `registry/<responsibility_id>/tasks/inbound` (inputs) and `tasks/outbound` (outputs/responses). Task Worker must avoid cross-writing between Responsibilities.
- **Zero-seed onboarding** – During ZERO_SEED_BOOT, no Task Worker is required. Jane may draft a minimal onboarding Task or rely on the test RFA alone; any status changes are narrated and recorded in memory until a Task Worker is available.

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
2. **Optional Mirrors** – External mirrors (e.g., Google Tasks/Calendar) are convenience copies only; they must never delete or override Tasks stored in the filesystem. If used, IDs live under `external_refs.*`.
3. **Event Logging** – All Task issuance, acceptance, and completion events are written to the centralized system event log in addition to Responsibility memory to support workspace-wide coordination.

If `task_sync.state` transitions to `blocked` all dependent Responsibilities must halt Task execution (`kernel.tasks.issue` rejects commands) until remediation. `degraded` state may allow retries with warnings; exceeding `max_failed_tasks_per_day` escalates to Guardrails.

## Safety & Ownership
- Tasks are append-only. Deletion requires a Guardrails-approved migration with memory pointers.
- Only the Task Worker service may mutate status, priority, or due dates. Human operators must still invoke the Task Worker (or Kernel command) instead of editing files directly.
- Calendar or Gmail cleanup cannot cascade into Task removal.
- Every Task references a Mandate run ID and, when applicable, a RequestForAction ID; missing references cause the Kernel to halt execution.
- Tasks are strictly internal to a Responsibility/workspace; collaboration between Responsibilities always begins as an RFA even if Tasks eventually mirror the work.
- Responsibilities may open Tasks for themselves proactively (self-serve) or in response to accepted RFAs; both paths must record issuance and updates in memory and the system event log.

## Migration Strategy
1. **Phase 1 – Filesystem Source of Truth**: Stand up the Task Worker and keep the filesystem as the only authoritative store.
2. **Phase 2 – Optional Mirrors**: If needed, add external mirrors without ceding authority; verify that deletions/edits never flow inward.
3. **Phase 3 – Cross-System Routing**: When integrating external partners, enforce RFA-first coordination and maintain Mandate + Guardrails references.

Each migration phase must be recorded in `protocol/progress/PROGRESS_LOG.md` for downstream stewards.

## Implementation Checklist
- Add Task hydration to every Responsibility boot (Phase 3 in the boot template).
- Extend Kernel APIs with `kernel.tasks.issue(command)` and log Guardrails approvals.
- Update dashboards to show Task throughput (created, completed, blocked) per Responsibility alongside mandate runs and RequestForAction volume.
- Ensure LLM tooling reads Tasks from the filesystem and never attempts to mutate Google Tasks directly.
