# Dad Mode Boot Runbook

Operational checklist for spinning up a fresh Dad Mode instance on the Responsibility OS protocol. Follow each step sequentially and capture evidence (memory pointers, telemetry screenshots, or logs) before proceeding.

---

## Phase 0 – Preflight
1. **Clone + Sync Repo** – Pull latest `responsibility-os-protocol`.
2. **Verify Required Files** – Run `tools/check_startup.py parenting_cos` (or manual inspection) to ensure files listed in `protocol/RESPONSIBILITY_STARTUP_CHECKLIST.md` exist.
3. **Credential Audit** – Confirm Google Workspace + Trello OAuth tokens stored in secrets manager and valid.
4. **Expected Output** – Preflight report with ✅ on files + creds.
5. **Failure Modes**
   - Missing file → regenerate from template.
   - Expired OAuth → reauthorize before proceeding.

## Phase 1 – Kernel & Guardrails Boot
1. Start Kernel + Guardrails containers (`make boot-parenting`).
2. Tail logs until `boot_orientation` memory entry appears.
3. Validate Guardrails signature cache.
4. **Expected Output** – Memory entry `boot_orientation_completed`.
5. **Recovery** – If Guardrails reject, review persona vs. guardrail mismatches and redeploy.

## Phase 2 – BOOT_SUMMARY Generation
1. Run `kernel.boot.regenerate parenting_cos`.
2. Upload resulting `BOOT_SUMMARY.latest.json` to the Responsibility filesystem.
3. Confirm memory entry `boot_summary_regenerated` with diff hash.
4. **Failure Modes**
   - Manual edit detected → delete file and rerun regenerate command.
   - Hash mismatch → ensure base files committed and rerun.

## Phase 3 – Task Hydration & Sync
1. Execute `task_worker hydrate parenting_cos`.
2. Check `tasks/index.json` for open Tasks plus `task_sync.state`.
3. Confirm Google Tasks + Calendar bindings exist for sampled Tasks.
4. **Expected Output** – Memory entry `task_hydration_check` with counts; telemetry heartbeat recorded.
5. **Failure Modes**
   - `state=blocked` → fix OAuth scopes, rerun hydration.
   - `state=degraded` → inspect sync job logs; escalate if API outage > 30 min.

## Phase 4 – Request Queue Verification
1. Run SQL query to list pending RFAs for Parenting.
2. Ensure markdown mirrors regenerated.
3. Claim one test RFA (fixture) and complete via Task Worker to validate flow.
4. **Expected Output** – RFA transitions to `completed`, Task lifecycle events recorded.
5. **Failure Modes**
   - Queue latency > `max_queue_latency_seconds` → scale workers or inspect claim logic.

## Phase 5 – Telemetry & Alerts
1. Deploy `telemetry/policies.default.yaml` (or Responsibility override).
2. Ensure metrics streaming to dashboard (tasks_created, sync_errors, heartbeat).
3. Trigger synthetic alert (e.g., pause Task Worker) and confirm alerting path.
4. **Expected Output** – Dashboard screenshot + alert receipt.
5. **Failure Modes**
   - Alerts not firing → check webhook credentials, update policy file.

## Phase 6 – Sign-off
1. Record summary in `boot_trial_logs/<date>/dad_mode_signoff.md`:
   - Checklist steps
   - Memory pointers
   - Outstanding issues
2. Notify stakeholders via preferred channel.

---

### Known Recovery Steps
- **Kernel refuses start** – re-run `docker compose up` with clean volumes; ensure env vars present.
- **Task Worker blocked** – run `task_worker oauth refresh parenting_cos`.
- **Telemetry gaps** – restart telemetry sidecar; verify `heartbeat_interval_seconds`.
- **Guardrail override stuck** – escalate to steward, append memory event describing manual decision.

Use this runbook every time Dad Mode is rebooted or a new environment comes online.
