# Fixture – Mandate → RequestForAction → Task → Completion

This executable narrative demonstrates the golden flow for cross-responsibility work. It can be replayed by operators or automated tests to verify protocol compliance before connecting to real data.

---

## 1. Mandate Issued (Finance Responsibility)
```md
mandates/definitions/budget_allowance.md
---
mandate_id: finance_cos.monthly_allowance
title: Monthly Allowance Planning
intent: Prepare allowance transfer recommendations for parenting_cos with Guardrail G-ALW-02.
success_metrics:
  - allowance_plan_submitted: true
constraints:
  - guardrail_ref: G-ALW-02
dependencies:
  mode: all
  items: []
---
```
Kernel logs mandate activation: `memory/events.md` entry `mandate_run_started` with `mandate_run_id=finance_cos.monthly_allowance@2025-11-28T09:00Z`.

## 2. RFA Generated
Finance responsibility emits an RFA targeting Parenting:
```md
queue/outbox/req_2025-11-28T09-15Z_finance_to_parenting_allowance.md
---
request_id: req_2025-11-28T09-15Z_finance_to_parenting_allowance
origin_responsibility_id: finance_cos
target_responsibility_id: parenting_cos
status: pending
priority: 100
source_context: mandate_run:finance_cos.monthly_allowance@2025-11-28T09:00Z
workspace_id: dad_mode
sla_response_seconds: 14400
sla_completion_seconds: 86400
---
Summary: Please review the November allowance plan and approve transfers before EOM.
```
SQL SoR entry mirrors these fields; Guardrails sign the transition `created → pending`.

## 3. Kernel Routes RFA
Parenting Kernel calls `kernel.requests.claim('dad_mode', 'parenting_cos', batch_size=5)` → receives the RFA reference. The `workspace_id` parameter ('dad_mode') enforces workspace isolation. Guardrails verify mandate coverage (Parenting has `parenting_cos.allowance_execution`).

## 4. Task Projection
Parenting mandate run triggers Task creation:
```json
tasks/task_3f4d.json
{
  "task_id": "task_3f4d",
  "title": "Approve November allowance transfers",
  "description": "Review finance_cos plan, confirm guardrail compliance, and schedule transfers.",
  "mandate_id": "parenting_cos.allowance_execution",
  "preferred_responsibilities": ["parenting_cos"],
  "status": "needs_action",
  "priority": "high",
  "due_date": "2025-11-30T23:59:59Z",
  "external_refs": {
    "google_task_id": "GTA-98123",
    "calendar_event_id": null
  },
  "source": "request_for_action:req_2025-11-28T09-15Z_finance_to_parenting_allowance",
  "created_at": "2025-11-28T10:00:00Z",
  "updated_at": "2025-11-28T10:00:00Z",
  "task_sync": {
    "state": "active",
    "last_heartbeat": "2025-11-28T10:00:05Z"
  }
}
```
Task Worker records the creation (`kernel.tasks.issue(create)`), syncs to Google Tasks, and appends memory entry `task_created`.

## 5. Execution & Completion
1. Steward reviews plan, triggers `kernel.tasks.issue(update_status: in_progress)`.
2. Transfers executed; steward attaches confirmation doc.
3. Kernel marks Task `completed`, Guardrails confirm no violations.
4. RFA state machine: `pending → accepted → completed`, with SQL + markdown views updated.

## 6. Telemetry & Memory
- Telemetry counters increment:
  - `tasks_created{responsibility="parenting_cos"} += 1`
  - `tasks_completed` increments when Task closes.
  - `queue_latency_seconds` recorded (`accepted_at - available_at`).
- Memory entries (ordered):
  1. `mandate_run_started`
  2. `request_created`
  3. `request_claimed`
  4. `task_created`
  5. `task_status_updated` (in_progress)
  6. `task_status_updated` (completed)
  7. `request_completed`

## 7. Verification Steps
Run this fixture by executing:
1. `kernel.run_fixture(protocol/examples/fixtures/mandate_to_task_end_to_end.md)` (implementation-specific command).
2. Validate outputs:
   - `tasks/index.json` contains `task_3f4d`.
   - RFA SoR row transitions to `completed`.
   - Telemetry aggregator reports the metrics above.
   - Memory log includes all seven events with matching IDs.

Use this document as the “golden flow” reference when onboarding new Responsibilities or debugging Mandate/Task interactions.
