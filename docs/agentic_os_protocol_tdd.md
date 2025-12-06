# Technical Design – Responsibility OS Protocol (Agentic OS)

This document briefs engineers and stewards on the full Responsibility OS (ROS) protocol surface so they can ramp quickly and implement compatible systems, including the Task Worker upgrade. It is intended for public distribution alongside the specs.

---

## 1. Objectives
- Provide a canonical walkthrough of the Mandate → Task → Responsibility → Action chain.
- Describe how Kernel, Guardrails, Responsibilities, and supporting specs interlock.
- Detail Task Worker responsibilities, sync paths (Google Workspace MCP), and telemetry.
- Clarify boundaries between protocol guarantees and app-layer implementations.

## 2. System Layers Overview

| Layer | Artifact(s) | Purpose |
| --- | --- | --- |
| **System-of-Record (SoR)** | SQL queues, Mandate registry, RequestForAction (RFA) tables | Deterministic state transitions, timestamps, retries |
| **System-of-Context (SoC)** | Responsibility filesystem (markdown/JSON), Tasks, BOOT_SUMMARY | Narrative/context for stewards + LLMs |
| **Execution Core** | Kernel + Guardrails pair | Deterministic planning, safety enforcement |
| **Responsibilities** | Personas, mandates, memory | Scoped units of authority |
| **Task Worker** | `task_worker_personal` responsibility | Owns Task lifecycle, sync, routing |

## 3. Component Deep Dive

### 3.1 Kernel (`protocol/specs/v1/03_kernel.md`)
- **Mandate Intake**: verifies signatures, guardrail references, dependencies.
- **Task Planner**: materializes Task objects with guardrail references and preferred responsibilities.
- **Task Worker Interface**: `kernel.tasks.issue(command)` is the only path to mutate Task state.
- **Request Bridge**: deterministic claim of RFAs from SQL queue.
- **Memory Writer**: append-only records for every decision.

### 3.2 Guardrails (`protocol/specs/v1/04_guardrails.md`)
- Hashes and signs mandate definitions.
- Validates persona abilities vs. allowlist.
- Approves Task Worker commands; blocks status transitions that violate invariants.
- Monitors telemetry channels for SLA breaches (tied to `protocol/TELEMETRY_SPEC.md`).

### 3.3 Responsibilities (`protocol/specs/v1/02_responsibility.md`)
- Boot lifecycle (Phase 0-3) defined in `protocol/RESPONSIBILITY_BOOT_TEMPLATE.md` and enforced through `protocol/RESPONSIBILITY_STARTUP_CHECKLIST.md`.
- BOOT_SUMMARY becomes runtime truth; includes rules, tool safety, open Task IDs, context gaps. Only `kernel.boot.regenerate(responsibility_id)` may update it—manual edits are prohibited and Guardrails halt execution when hashes drift.
- Transfer of responsibility requires memory entries (request + acceptance).

### 3.4 Mandates (`protocol/specs/v1/06_mandate.md`)
- Immutable authority packets (`mandate_id`, `intent`, `constraints`, `dependencies`).
- Mandate runs stored under `mandates/runs/<mandate_id>/<ISO8601>.md`.
- Task materialization happens before routing; missing Task references halt execution.
- Safety: Tasks never auto-deleted, external mirrors cannot remove canonical data.

### 3.5 RequestForAction (`protocol/REQUEST_FOR_ACTION_SPEC.md`)
- SQL schema enforces status machine: created → pending → accepted/deferred/rejected/cancelled/expired → completed.
- Markdown mirrors provide SoC visibility but are regenerated from SQL.
- RFAs never transfer authority; they request a Responsibility to run its own mandate(s).
- Every RFA carries `workspace_id`, keeping queues isolated per workspace and tying steward actions to a single environment.
- Two context-centric RFA types extend the system:
  - `ingest_new_context` – issued by CLI/tooling to Jane when proposing new bundles (includes bundle IDs, objectives, optional suggested responsibilities).
  - `new_context_available` – issued by Jane to downstream responsibilities after validation.
  The steward alone transitions context ingestion RFAs and must avoid unnecessary fan-out while honoring opt-outs.

### 3.6 Tasks (`protocol/specs/v1/10_tasks.md`)
- Canonical schema: `task_id`, `title`, `description`, `mandate_id`, `preferred_responsibilities`, `status`, `priority`, `due_date`, `external_refs`, `task_sync`, `source`, timestamps.
- Sync model: Internal Task store ↔ Google Tasks ↔ Calendar (optional) via `google_workspace_mcp`.
- `task_sync.state` tracks connector health (`active | blocked | degraded`). Blocked states halt Task execution until OAuth restored; degraded states raise telemetry warnings and retry per policy.
- Invariants: Task ownership (#7/#8) ensures only Task Worker can mutate and all cross-responsibility Tasks cite accepted RFAs.
- Migration phases: Gmail/Calendar/Tasks enablement → internal DB source of truth → cross-system routing.

### 3.7 Task Worker Responsibility (`protocol/TASK_WORKER_BOOT_SPEC.md`)
- Identity: `task_worker_personal`, domain = Personal Operations.
- Core functions: creation/normalization, routing, sync, status tracking.
- Safety: no silent deletes, internal store = source of truth, external mutations logged.
- Reboot triggers: protocol changes, new integrations.

### 3.8 Memory (`protocol/specs/v1/08_memory.md`)
- Append-only ledger referencing `mandate_run_id`, `request_id`, and `task_id`.
- Used for planning checkpoints, reflections, handoffs, request audits.
- Guardrails hash entries; telemetry monitors drift.

### 3.9 Filesystem (`protocol/RESPONSIBILITY_FILESYSTEM_STANDARD_V0_1.md`)
- Canonical tree per Responsibility:
  ```
  responsibilities/<responsibility_id>/
    persona.md
    guardrails.md
    mandates/
      definitions/
      runs/
    tasks/
      task_<uuid>.json
      index.json
    memory/events.md
    queue/
    ai_context/
  ```
- Append-only policy: modifications require new files or addendum entries.

### 3.10 Telemetry (`protocol/TELEMETRY_SPEC.md`)
- Metrics: task throughput, sync lag, mandate run duration, SLA breach counts.
- Alerts: Task sync failures, blocked tasks beyond SLA, request queue backlog.
- Default policy file `protocol/telemetry/policies.default.yaml` supplies sane budgets (cost, queue latency, heartbeat intervals, failed task thresholds). Responsibilities copy/override it (`telemetry/policies.<responsibility>.yaml`) and `telemetry/` artifacts live beside each Responsibility per the filesystem spec.

### 3.11 Operational Artifacts
- **Responsibility Startup Checklist** (`protocol/RESPONSIBILITY_STARTUP_CHECKLIST.md`) – operator-facing checklist that merges boot phases, required files, outputs, and failure modes into one document. Kernels log `boot_checklist.completed` after each run and now require `boot_model_check` + telemetry `model_mismatch_on_boot`.
- **Dad Mode Boot Runbook** (`runbooks/dad_mode_boot_runbook.md`) – applies the checklist to the public Dad Mode instance, including telemetry validation, model verification, context-ingestion tests, and the requirement to log both `dad_mode_signoff.md` and `potential_issues.md` under `boot_trial_logs/<timestamp>/`.
- **Golden Flow Fixture** (`protocol/examples/fixtures/mandate_to_task_end_to_end.md`) – executable narrative showing Mandate → RFA → Task → completion with telemetry + memory references. Use it before onboarding real data.

### 3.12 Context Ingestion & Telemetry
- `protocol/AI_CONTEXT_BUNDLES.md` now defines bundle metadata (`origin`, `primary/suggested responsibilities`, `scope`, `ingestion_status`) plus the two ingestion flows (workspace drop vs CLI-assisted).
- Stewards log `context_ingested` when they register a bundle and `context_dispatched` when they emit `new_context_available` RFAs. Payloads include bundle IDs, RFA IDs, notified responsibilities, and workspace IDs.
- Telemetry policies (`protocol/telemetry/policies.default.yaml`) add defaults for context backlog and model mismatch handling; Guardrails monitor these metrics and escalate via RFAs/alerts when thresholds break.

---

## 4. Data & Control Flow

1. **Intent Intake**: Human steward defines or updates mandates; Guardrails approve; Kernel queues runs.
2. **Mandate Activation**: Kernel spawns a mandate run, generates Tasks, logs references.
3. **Task Lifecycle**:
   - Task Worker writes canonical JSON files.
   - Sync service mirrors to Google Tasks; optional calendar bindings for due dates/blockers.
   - Preferred responsibilities + guardrail refs drive routing.
4. **Execution**: Responsibility claim leads to action planning and memory writes per step.
5. **Reflection/Completion**: Task Worker receives status updates; memory records `task_id`; RFA (if any) marked completed via deterministic SQL procedure.

### Sequence Sketch
```text
Mandate Run
  ↓
Kernel.TaskPlanner()
  ↓
kernel.tasks.issue(create)
  ↓
Task Worker → tasks/index.json
  ↓
task_worker.sync.google_tasks()
  ↓
Kernel.Router assigns Responsibility
  ↓
Responsibility executes → status updates issued via Task Worker
  ↓
Memory + Telemetry append events
```

---

## 5. Interfaces and Contracts

| Interface | Direction | Description |
| --- | --- | --- |
| `kernel.tasks.issue(command)` | Kernel → Task Worker | Commands: `create`, `update_status`, `bind_google_task`, `bind_calendar_event`, `annotate`. Guardrails approve before execution. |
| `task_worker.sync.google_tasks(task_id)` | Task Worker → Google Workspace MCP | Creates/updates external tasks, logs IDs in `external_refs`. |
| `task_worker.route(task)` | Task Worker → Kernel Router | Returns candidate responsibilities + rationale. |
| `memory.append(record)` | Kernel → Memory | Includes `task_id` when Task-related. |
| `kernel.requests.claim(workspace_id, responsibility_id, batch_size)` | Kernel → SoR | Deterministic selection of pending RFAs filtered by workspace (enforces Invariant 10). |

All interfaces emit telemetry events (`telemetry.emit(metric, value, tags)`).

---

## 6. Safety & Compliance Mapping

| Invariant | Enforcement |
| --- | --- |
| Alignment Loop | Task schema requires `mandate_id`/`request_id`; Kernel rejects missing link. |
| Memory Append-Only | Memory interface lacks delete/update; Guardrails hash. |
| Mandate Integrity | Guardrails sign definitions, Kernel checks signatures before run. |
| Persona Consistency | Router consults persona capabilities; Guardrails block mismatches. |
| Auditability | Every Task command logs `(kernel_decision_id, guardrail_clause_id, task_id, memory_pointer)`. |
| Deterministic Requests | RFA state machine enforced in SQL + Guardrails. |
| Task Ownership | Only Task Worker receives `kernel.tasks.issue`; Guardrails verify actor. |

Additional safety checks:
- Sync watchers detect missing Google Task bindings and re-issue create commands.
- Calendar deletions mark bindings as `stale` but leave Task intact.
- SLA monitors escalate to steward or Guardrails automation when `blocked` status persists past policy.

---

## 7. Migration & Versioning Notes

1. **Phase 1**: Stand up Task Worker + Google Workspace MCP connectors. Verify creation/status sync.
2. **Phase 2**: Promote filesystem Task store to SoT; external systems become mirrors. Build import script for legacy task trackers.
3. **Phase 3**: Enable cross-responsibility Task routing + external partner handoffs.

Each phase requires:
- Progress log entry (`protocol/progress/PROGRESS_LOG.md`).
- Telemetry dashboards updated with new metrics.
- Steward boot instructions refreshed if tools/policies change.

---

## 8. Boundary Between Protocol and Application

- **Protocol Guarantees**: deterministic planning, safety enforcement, append-only records, Task lifecycle, Google Workspace sync contract, telemetry schema.
- **Application Responsibilities** (see private TDD): user experience, multi-tenant SaaS, billing, secrets management, voice interface, Trello/TODO integration, analytics dashboards, feature gating.
- Protocol artifacts must remain domain-neutral; application layer injects household or enterprise context through Responsibilities configured outside this repository.

---

## 9. Open Work / Future Enhancements
1. **Batch Task Commands** – evaluate need for bulk updates to reduce MCP round trips.
2. **Policy-Aware Sync** – add rules for which Task metadata may be exported to third-party systems.
3. **Task Templates** – optional spec for reusable Task blueprints tied to mandates.
4. **Advanced Telemetry** – correlate Task throughput with model usage budgets.
5. **Cross-Instance Federation** – spec for sharing Tasks or RFAs between separate Agentic OS deployments while preserving guardrail signatures.

Contributors should reference this TDD before proposing spec modifications to ensure new work maintains the established contracts.
