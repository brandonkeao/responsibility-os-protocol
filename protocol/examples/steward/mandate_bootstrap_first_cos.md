# mandate.steward.bootstrap_first_cos

## Title
Bootstrap a seedless Circle of Stewardship (CoS) instance.

## Intent
Stand up a minimal Responsibility OS deployment with Kernel, Guardrails, and Steward persona configured for collaborative work **without any pre-seeded Responsibilities or Tasks**. Jane onboards the user, creates the first Responsibility, and proves the RequestForAction (RFA) handshake before any other automation is attempted.

## Success Metrics
- User completes Jane-led onboarding and approves the first Responsibility definition (id, mission, success signals, guardrail boundaries, initial context sources).
- Portable container for the new Responsibility exists under `registry/<id>/` with required stubs (manifest, context, notes, logs, tasks inbox/outbox, memory, ai_context).
- Test RFA sent from Jane to the new Responsibility is acknowledged and logged in SQL + markdown mirrors with telemetry heartbeat.
- Follow-on protocol checks run in priority order (memory hygiene → identity prompt/UTB stubs → BOOT_SUMMARY → telemetry heartbeat) with memory pointers.

## Constraints
- No seed data or pre-populated Responsibilities; everything is created in-session.
- Use open-source safe defaults only; avoid external integrations until Guardrails sign-off is stored in memory.
- Guardrails clauses: `safety.bootstrap`, `scope.foundation_only`, `portability.enforced`.

## Operating Steps (Seedless First Boot)
1) Confirm registry exists and is empty; record `boot_orientation` noting seedless onboarding intent.
2) Collect user inputs for the first Responsibility (id/name, mission/success signals, approvals/safety, context sources). Emphasize the portable container requirement and isolation rules.
3) Scaffold the container under `registry/<id>/` with manifest stub, `context.md`, `notes.md`, `logs/`, `tasks/inbound|outbound/`, `memory/events.md`, `ai_context/model_preferences.md`; log the action in memory.
4) Send a test RFA from Jane to the new Responsibility (`ingest_new_context` or `bootstrap_flow_check`). Guide the user through verifying: SQL row, markdown mirror, centralized event log entry, Responsibility acknowledgment, memory updates, and telemetry heartbeat.
5) Run remaining protocol checks in priority order: memory hygiene/append-only reminders, Golden Identity Prompt or Unified Task Brief stub + context budget check, BOOT_SUMMARY generation, telemetry policy confirmation/heartbeat, then optional Task Worker hydration if integrations are present. Emphasize that Tasks remain inside the Responsibility; RFAs mediate collaboration.

## Handoff Plan
If setup stalls, log current state to memory and assign the mandate run to another steward persona with infrastructure capabilities.
