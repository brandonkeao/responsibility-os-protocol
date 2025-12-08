---
layer: ops_infrastructure
change_risk: high
---

# INIT Command Integration Spec

## Purpose
Define the canonical behavior when a user types `init` in a brand-new workspace so the system deterministically enters ZERO_SEED_BOOT, launches Jane’s onboarding, and creates the minimum viable Responsibility assets without seeds, registries, or external tooling.

## Boot Mode Detection
- **ZERO_SEED_BOOT triggers when all are true**:
  - `registry/` is absent or empty
  - No Responsibility containers exist under `registry/<id>/`
  - No seed file is present (e.g., `seed.json`, `seed.yaml`)
  - The first command received is exactly `init`
- **SEED_BOOT triggers** when any of the above are false or a seed file is present; existing behavior remains unchanged.

## INIT Command Behavior
When ZERO_SEED_BOOT conditions are met and `init` is received, the Kernel routes to Jane for onboarding (see `JANE_ZERO_SEED_ONBOARDING_SPEC.md`):
1. Jane greets the user, explains ZERO_SEED_BOOT, and confirms workspace identity (workspace_id, optional display name).
2. Jane gathers first Responsibility inputs (id, mission/scope, safety boundaries).
3. Jane creates the portable container `registry/<responsibility_id>/` with at least `context.md`, `manifest.json`, `logs/`, `tasks/inbound/`, `tasks/outbound/`, and `notes.md`.
4. Jane writes/updates `registry/responsibility_registry.json` (or inserts into the SQL registry) to index the new Responsibility.
5. Jane emits a test RequestForAction (RFA) to the new Responsibility and writes the markdown mirror under `queue/inbox/`.
6. Jane writes a boot log entry noting ZERO_SEED_BOOT activation and the new Responsibility.

## Safety & Non-Destructive Rules
- If registry or Responsibility containers already exist, `init` must never overwrite data. Jane offers a read-only tour and a “continue with existing state” option.
- `init` is the recommended user-facing entrypoint; other commands remain supported.
- Task Worker and external integrations are optional; onboarding must complete without them.

## Outputs Required After `init` in ZERO_SEED_BOOT
- `registry/<responsibility_id>/context.md`
- `registry/<responsibility_id>/manifest.json`
- `registry/responsibility_registry.json` entry
- `queue/inbox/<test_rfa_id>.md` mirror
- Boot log entry in `boot_trial_logs/` (or equivalent)
- Telemetry event(s) noting ZERO_SEED_BOOT and onboarding-created Responsibility

## Guardrails & Telemetry
- Telemetry must record boot mode (`ZERO_SEED_BOOT`) and onboarding-created Responsibilities (see `TELEMETRY_SPEC.md`).
- Guardrails must prevent cross-Responsibility writes during onboarding and block `init` from deleting or overwriting existing registries.
