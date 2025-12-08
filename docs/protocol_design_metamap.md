# Responsibility OS Protocol – Progressive Design Map

Audience: operators and contributors who want a plain-English walkthrough of the protocol, starting simple and layering in complexity. This is public-facing; it avoids private data and keeps examples neutral.

## TL;DR
- Start with a **single responsibility** that has a persona, guardrails, mandates, memory, tasks, and a BOOT_SUMMARY snapshot.
- Add **deterministic boot + task hydration** so the responsibility can start and sync work without guessing.
- Layer **queue + telemetry + model discipline** to keep routing auditable and detect drift.
- Scale to **multiple responsibilities** coordinated by a steward and a task worker, sharing RFAs and context bundles.

## Metaphors at a Glance
1) **Train Yard** – Tracks (responsibilities), switch operator (steward), cargo manifests (tasks/RFAs), yard rules (guardrails), yard logbook (memory), dispatch report (BOOT_SUMMARY).
2) **Orchestra** – Sections (responsibilities), conductor (steward), score (mandates/tasks), tuning protocol (model preferences), rehearsal notes (memory), stage manager cues (telemetry/alerts).
3) **Kitchen Brigade** – Stations (responsibilities), head chef (steward), prep lists (tasks), health code (guardrails), order tickets (RFAs), pass checks (telemetry), recipe card snapshot (BOOT_SUMMARY).
We evolve each metaphor in the sections below so operators can pick whichever clicks.

## Stage 1 – Single Responsibility, Minimal Shape
- Files: `persona.md`, `guardrails.md`, `mandates/definitions/*.md`, `tasks/index.json`, `memory/events.md`, `ai_context/model_preferences.md` (even a stub), `BOOT_SUMMARY.latest.json`.
- Behavior: treat memory as append-only, avoid manual edits to BOOT_SUMMARY, keep tasks in `needs_action` until hydrated.
- Metaphor lens:
  - Train Yard: one track with a simple cargo list; yard rules posted; logbook open.
  - Orchestra: a solo player with sheet music and tuning note; conductor absent.
  - Kitchen: one station with a prep list and recipe card; health rules on the wall.

## Stage 2 – Deterministic Boot
- Runbook alignment: use `RESPONSIBILITY_STARTUP_CHECKLIST.md` steps (Phase 0–3) and the stub commands in `tools/` to simulate.
- Key actions: static validation, `kernel.boot.regenerate` (stub) to refresh BOOT_SUMMARY, `kernel.boot.model_check` (stub) to compare runtime vs preferred models, task hydration via `task_worker_hydrate` (stub).
- Outputs: updated BOOT_SUMMARY with input hashes, task_sync state set, optional boot trial log entries.
- Metaphor lens:
  - Train Yard: switch operator verifies track, refreshes dispatch sheet, tags cargo with latest manifest numbers.
  - Orchestra: conductor checks instruments, updates the score sheet, confirms tuning matches the pitch pipe.
  - Kitchen: head chef inspects station, refreshes recipe card, confirms burners match the prep instructions.

## Stage 3 – Queue + Telemetry Hooks (Simulation Mode)
- Queue: use `tools/queue_scaffold.py` to create a stub SQLite queue and `queue_to_markdown.py` to mirror RFAs into `queue/inbox/` markdown.
- Telemetry: use `tools/telemetry_emit.py` to drop local JSON events for `heartbeat`, `context_ingested`, `context_dispatched`, `model_mismatch_on_boot`.
- Purpose: prove the wiring and file locations even before real infra exists; keep everything local and auditable.
- Metaphor lens:
  - Train Yard: incoming cargo requests land in the yard office ledger; yard emits a ping every shift change and records reroutes.
  - Orchestra: stage manager hands written cue cards for new pieces; sound check emits green/yellow lights for each section.
  - Kitchen: new tickets hit the printer; expo sends pass/fail ticks for timing and food safety.

## Stage 4 – Multi-Responsibility Coordination
- Steward + Task Worker: copy examples via `scripts/scaffold_workspace.sh --include-task-worker` to get starter personas/guardrails/mandates and BOOT_SUMMARY placeholders.
- Domain set: marketing examples live at `protocol/examples/marketing/*` (website, content, social, product marketing, community, protocol manager). Use these to populate a workspace until real artifacts are authored.
- Flow: steward acknowledges mandates → task worker hydrates tasks → responsibilities pull RFAs from queue mirrors → telemetry emits heartbeats.
- Metaphor lens:
  - Train Yard: multiple tracks with a central switch tower; task worker is the shunter moving cars between tracks; dispatcher ledger tracks each move.
  - Orchestra: full ensemble; conductor cues sections; stage manager routes new pieces to the right stands; tuning checks ensure no section drifts off-pitch.
  - Kitchen: brigade with multiple stations; head chef sequences tickets; runner moves plates; expo logs timing and alerts on misses.

## Guardrails, Models, and BOOT_SUMMARY Ownership
- Guardrails: define non-negotiables; BOOT_SUMMARY should only be updated by a regenerate command (even stubbed) and not manually edited.
- Model discipline: `ai_context/model_preferences.md` states preferred and allowed models; model check emits ok/warning so humans can reconcile drift.
- Memory: always append-only; record boot, task hydration, queue pulls, and telemetry drill runs as events.

## How to Run a Local Simulation (Quick Script Path)
1. Scaffold: `./scripts/scaffold_workspace.sh /tmp/ws --include-task-worker`.
2. Validate: `python3 tools/check_startup.py /tmp/ws --report /tmp/ws/startup.json`.
3. Regenerate BOOT_SUMMARY: `python3 tools/kernel_boot_regenerate.py /tmp/ws --responsibility-id=demo --log-dir=/tmp/ws/boot_trial_logs`.
4. Model check: `python3 tools/kernel_boot_model_check.py /tmp/ws --actual-model=gpt-4.1 --responsibility-id=demo`.
5. Hydrate tasks: `python3 tools/task_worker_hydrate.py /tmp/ws --state=active`.
6. Queue + mirror: `python3 tools/queue_scaffold.py /tmp/ws --add-sample` then `python3 tools/queue_to_markdown.py /tmp/ws`.
7. Telemetry ping: `python3 tools/telemetry_emit.py /tmp/ws --responsibility-id=demo --event-type=heartbeat --status=ok --note="dry run"`.

## Future Hardening (Beyond These Stubs)
- Replace stub scripts with real Kernel/Guardrails integration and signed BOOT_SUMMARY outputs.
- Enforce schema validation for tasks, BOOT_SUMMARY, model preferences, and RFAs.
- Wire telemetry to a durable sink with alerting; add dashboards for heartbeats and model drift.
- Add OAuth-aware task hydration and real sync status for the Task Worker.
- Expand examples into vetted templates per domain with review/approval flows.

Pick a metaphor (train yard, orchestra, or kitchen) when explaining the protocol to stakeholders. Each evolves cleanly as you add boot, queue, telemetry, and multi-responsibility coordination, so newcomers can follow without absorbing the entire spec first.
