---
layer: ops_infrastructure
change_risk: medium
---

# Responsibility Startup Checklist

This checklist collapses the Responsibility boot + Task hydration requirements into a single operational artifact. Responsibilities must satisfy every item before accepting real work. Reference specs are linked for deeper context, but operators should be able to run this checklist alone.

---

## Required Files
1. `persona.md` – persona traits + provenance (`protocol/specs/v1/05_persona.md`).
2. `guardrails.md` – clauses + enforcement metadata (`protocol/specs/v1/04_guardrails.md`).
3. `mandates/definitions/*.md` – authority packets (`protocol/specs/v1/06_mandate.md`).
4. `tasks/index.json` – canonical Task index (may be regenerated from per-task JSON files) (`protocol/specs/v1/10_tasks.md`).
5. `memory/events.md` – append-only log initialized for the Responsibility (`protocol/specs/v1/08_memory.md`).
6. `queue/inbox/*.md` (if accepting RFAs) – regenerated views referencing the SQL queue (`protocol/REQUEST_FOR_ACTION_SPEC.md`).
7. `BOOT_SUMMARY.latest.json` – generated via `kernel.boot.regenerate` (see below).
8. `ai_context/model_preferences.md` or equivalent YAML snippet describing `model.default_model` and `allowed_models`.
9. **Portable container** under `registry/<responsibility_id>/` with `context.md`, `manifest.json`, `logs/`, `tasks/inbound/`, `tasks/outbound/`, `notes.md` (workspace index points here).

## Required Phases
| Phase | Description | Pass Criteria |
| --- | --- | --- |
| Phase 0 – Static Validation | Kernel verifies required files and the portable container (`registry/<responsibility_id>/` with context, manifest, logs, tasks inbound/outbound) exist; hash signatures match Guardrails records. | All files present + signed; missing files block boot. |
| Phase 1 – Orientation Boot | Steward persona reviews mandates, tools, and guardrails; Kernel records acknowledgment. | `memory/events.md` contains `boot_orientation` entry referencing persona + guardrail clauses. |
| Phase 2 – BOOT_SUMMARY Persistence | Run `kernel.boot.regenerate` to produce BOOT_SUMMARY from canonical files (schema in `protocol/RESPONSIBILITY_BOOT_TEMPLATE.md`). | `BOOT_SUMMARY.latest.json` updated with new timestamp; memory records delta hash. |
| Phase 3 – Task Rehydration | Task Worker replays open Tasks from `tasks/` and validates external bindings (Google Tasks/Calendar) and local inbox/outbox (`registry/<id>/tasks/inbound|outbound`). | `tasks/index.json` status matches external sync; telemetry heartbeat reported. |

## Required Outputs
1. **BOOT_SUMMARY.latest.json** – authoritative runtime snapshot (no manual edits).
2. **Task Hydration Report** – appended to memory as `task_hydration_check` with counts (`open`, `blocked`, `degraded`).
3. **Telemetry Heartbeat** – `telemetry/heartbeats/<responsibility>.json` entry or emitted metric meeting `heartbeat_interval_seconds`.
4. **Model Verification Entry** – memory event `boot_model_check` plus telemetry `model_mismatch_on_boot` (even when matching, emit status=`ok`).
5. **Queue Sync Receipt** (if RFAs active) – memory entry referencing SQL queue pointer.

## Failure Conditions
- Missing required file → Kernel blocks boot and logs `boot_failure.missing_file`.
- Guardrail signature mismatch → Guardrails halt with `boot_failure.guardrail_signature`.
- BOOT_SUMMARY stale (>24h) or not generated via `kernel.boot.regenerate` → Kernel refuses Task execution.
- Task Worker reports `task_sync.state=blocked` (no OAuth or revoked scopes) → Responsibility cannot start until resolved.
- Telemetry heartbeat absent for 2 intervals (`heartbeat_interval_seconds * 2`) → automated alert.
- Model mismatch without operator decision → Kernel halts boot until resolved.

## Regeneration Rules
- `BOOT_SUMMARY` belongs to the steward persona. Only `kernel.boot.regenerate` may update it; manual edits are prohibited.
- When any required file changes, rerun the checklist from Phase 0.
- Kernel and Guardrails must append a memory entry for each checklist completion (`boot_checklist.completed`).

Operators should print this checklist (or view in runbook tooling) and mark each item before declaring the Responsibility “live.”
