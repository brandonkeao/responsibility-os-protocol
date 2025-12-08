---
layer: ops_infrastructure
change_risk: high
---

# Jane Zero-Seed Onboarding Spec

## Purpose
Make ZERO_SEED_BOOT a first-class, mandatory onboarding path led by Jane whenever a new workspace starts empty and the user types `init`.

## Trigger Conditions
- Workspace has no `registry/` directory (or it is empty).
- No Responsibility containers exist under `registry/<id>/`.
- No seed file is present.
- First command received is `init`.

## Jane’s Required Flow
1. **Greet & Explain** – Announce ZERO_SEED_BOOT, what Jane will create, and how Responsibilities are portable containers.
2. **Workspace Identity** – Collect `workspace_id` (and optional display name); create `registry/` and `queue/`/`telemetry/` minimal roots if missing.
3. **First Responsibility Creation** – Collect responsibility id, mission/scope, safety boundaries. Scaffold `registry/<id>/` with:
   - `context.md`
   - `manifest.json`
   - `logs/`
   - `tasks/inbound/`, `tasks/outbound/`
   - `notes.md`
4. **Registry Entry** – Create/update `registry/responsibility_registry.json` (or SQL row) to index the new container without overwriting existing entries.
5. **Test RFA** – Emit a test RequestForAction (e.g., `onboarding.test_rfa`) from Jane to the new Responsibility; write markdown mirror to `queue/inbox/<rfa_id>.md` and record in the registry/SoR if present.
6. **Filesystem Verification** – Confirm required files exist (persona/guardrails/mandates may be stubs), narrate checks, and log the verification step.
7. **Progressive Feature Tour** – Offer short guided steps: append-only memory hygiene, BOOT_SUMMARY generation, model preferences stub, telemetry heartbeat, optional Task Worker hydration (if available), and how to add more Responsibilities or bundles later.
8. **Logging & Telemetry** – Record ZERO_SEED_BOOT, Responsibility creation, and test RFA in boot logs, memory, and telemetry (see `TELEMETRY_SPEC.md`).

## Non-Destructive Behavior
- If registry or Responsibility containers exist, Jane must not overwrite; she switches to a read-only tour and offers to continue with existing state.
- If a seed file is present, defer to SEED_BOOT.

## Minimal Artifacts After Onboarding
- `registry/<responsibility_id>/context.md`
- `registry/<responsibility_id>/manifest.json`
- `registry/responsibility_registry.json` entry
- `queue/inbox/<test_rfa_id>.md`
- Boot log entry (ZERO_SEED_BOOT)
- Telemetry events for boot mode + Responsibility creation + test RFA

## Tone and Safety
- Guide/teacher voice; keep steps small and explain why each file matters.
- Pause for approval on safety boundaries and model choices.
- Never require Task Worker or external integrations to complete onboarding.
