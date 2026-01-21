# Dad Mode Boot Runbook

Operational checklist for spinning up a fresh Dad Mode instance on the Responsibility OS protocol. Follow each step sequentially and capture evidence (memory pointers, telemetry screenshots, or logs) before proceeding.

---

## Phase 0 – Preflight (Seedless First Boot)
1. **Clone + Sync Repo** – Pull latest `responsibility-os-protocol`.
2. **Empty Workspace Confirm** – Ensure registry exists and is empty (no pre-seeded Responsibilities). This run relies on Jane to create the first Responsibility during onboarding.
3. **Verify Required Files (base)** – Run `tools/check_startup.py parenting_cos` (or manual inspection) for the steward/Jane container only; the user-created Responsibility will be scaffolded live. Align with `protocol/RESPONSIBILITY_STARTUP_CHECKLIST.md`.
4. **Credential Audit** – Confirm Google Workspace + Trello OAuth tokens stored in secrets manager and valid (optional for first boot; can defer integrations).
5. **Expected Output** – Preflight report with ✅ on base files + creds (or explicit note that integrations are deferred).
6. **Failure Modes**
   - Missing base file → regenerate from template.
   - Expired OAuth → reauthorize before proceeding if integrations are in scope.

## Phase 1 – Kernel & Guardrails Boot
1. Start Kernel + Guardrails containers (`make boot-parenting`).
2. Tail logs until `boot_orientation` memory entry appears.
3. Validate Guardrails signature cache.
4. **Expected Output** – Memory entry `boot_orientation_completed`.
5. **Recovery** – If Guardrails reject, review persona vs. guardrail mismatches and redeploy.

## Phase 2 – Jane-Led Seedless Onboarding
1. Let Jane greet the user and collect first Responsibility inputs: id/name, mission + success signals, approval/safety boundaries, initial context sources.
2. Scaffold the new Responsibility container under `registry/<id>/` with manifest stub, `context.md`, `notes.md`, `logs/`, `tasks/inbound|outbound/`, `memory/events.md`, `ai_context/model_preferences.md`.
3. Append memory entry `responsibility_created` referencing the portable container path; ensure Guardrails sign-off for portability/isolation.
4. Issue a test RFA from Jane to the new Responsibility (`ingest_new_context` or `bootstrap_flow_check`). Validate SQL queue row, markdown mirror, centralized event log entry, Responsibility acknowledgment, and telemetry heartbeat.
5. **Expected Output** – User-approved Responsibility definition, container scaffolded, test RFA acknowledged with memory pointers/event log entries on both sides.
6. **Failure Modes**
   - Registry missing → create empty registry and retry.
   - RFA mirror not present → regenerate queue mirrors; verify SQL connectivity.
   - Telemetry heartbeat missing → deploy policy file and rerun heartbeat.

## Phase 3 – BOOT_SUMMARY Generation
1. Run `kernel.boot.regenerate <responsibility_id>` for the newly created Responsibility.
2. Upload resulting `BOOT_SUMMARY.latest.json` to the Responsibility filesystem.
3. Confirm memory entry `boot_summary_regenerated` with diff hash.
4. Run `kernel.boot.model_check <responsibility_id>` (or equivalent) to compare `actual_model` vs `model.default_model`:
   - Record decision (`proceed`, `abort`, `update_default_model`).
   - Ensure telemetry event `model_mismatch_on_boot` logged (status `ok`, `warning`, or `critical`).
5. **Failure Modes**
   - Manual edit detected → delete file and rerun regenerate command.
   - Hash mismatch → ensure base files committed and rerun.
   - Model mismatch unresolved → halt boot and loop in operator + Guardrails.

## Phase 4 – Task Hydration & Sync
1. Execute `task_worker hydrate parenting_cos`.
2. Check `tasks/index.json` for open Tasks plus `task_sync.state`.
3. Confirm Google Tasks + Calendar bindings exist for sampled Tasks.
4. **Expected Output** – Memory entry `task_hydration_check` with counts; telemetry heartbeat recorded.
5. **Failure Modes**
   - `state=blocked` → fix OAuth scopes, rerun hydration.
   - `state=degraded` → inspect sync job logs; escalate if API outage > 30 min.

## Phase 5 – Request Queue Verification
1. Run SQL query to list pending RFAs for Parenting.
2. Ensure markdown mirrors regenerated.
3. Claim one test RFA (fixture) and complete via Task Worker to validate flow.
4. **Expected Output** – RFA transitions to `completed`, Task lifecycle events recorded.
5. **Failure Modes**
   - Queue latency > `max_queue_latency_seconds` → scale workers or inspect claim logic.

## Phase 6 – Telemetry & Alerts
1. Deploy `telemetry/policies.default.yaml` (or Responsibility override).
2. Ensure metrics streaming to dashboard (tasks_created, sync_errors, heartbeat).
3. Trigger synthetic alert (e.g., pause Task Worker) and confirm alerting path.
4. **Expected Output** – Dashboard screenshot + alert receipt.
5. **Failure Modes**
  - Alerts not firing → check webhook credentials, update policy file.

## Phase 7 – Sign-off
1. Record summary in `boot_trial_logs/<date>/dad_mode_signoff.md`:
   - Checklist steps
   - Memory pointers
   - Outstanding issues
2. Create `boot_trial_logs/<date>/potential_issues.md` capturing any warnings, blocked checks, or follow-up actions discovered during the run.
3. Notify stakeholders via preferred channel.

---

### Known Recovery Steps
- **Kernel refuses start** – re-run `docker compose up` with clean volumes; ensure env vars present.
- **Task Worker blocked** – run `task_worker oauth refresh parenting_cos`.
- **Telemetry gaps** – restart telemetry sidecar; verify `heartbeat_interval_seconds`.
- **Guardrail override stuck** – escalate to steward, append memory event describing manual decision.

Use this runbook every time Dad Mode is rebooted or a new environment comes online.
