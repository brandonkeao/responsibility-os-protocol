---
layer: ops_infrastructure
change_risk: high
---

# Boot Modes and INIT Command Handling

This document defines the official boot modes for Responsibility OS and how the system reacts to the `init` command.

## Boot Modes
- **ZERO_SEED_BOOT (new default for empty workspaces)**: Triggered when no registry exists, no Responsibility containers are present under `registry/<id>/`, no seed file is present, and the first command is `init`. The system must load Jane’s onboarding flow per `JANE_ZERO_SEED_ONBOARDING_SPEC.md`.
- **SEED_BOOT (existing)**: Triggered when a seed file is present, or registry/responsibility containers already exist. Behavior remains unchanged; seeded Responsibilities and registries are honored.

## Detection Rules
1. On session start, check workspace for:
   - Presence of `registry/` and whether it contains any responsibility subdirectories.
   - Presence of seed files (`seed.json`, `seed.yaml`, or similar).
2. If none are found and the first user command is `init`, set boot mode = ZERO_SEED_BOOT.
3. Otherwise, set boot mode = SEED_BOOT.

## INIT Command Behavior
- If boot mode = ZERO_SEED_BOOT:
  - Hand control to Jane to run the onboarding flow (workspace identity → first Responsibility → registry entry → test RFA → filesystem verification → feature tour).
  - Create required artifacts: `registry/<responsibility_id>/context.md`, `manifest.json`, `logs/`, `tasks/inbound`, `tasks/outbound`, `notes.md`; `registry/responsibility_registry.json` entry; `queue/inbox/<test_rfa_id>.md`; boot log entry; telemetry events.
- If boot mode = SEED_BOOT:
  - Never overwrite existing data. Jane offers a read-only tour and continues with the existing state.
- `init` is the recommended entrypoint for users; other commands remain supported.

## Safety & Guardrails
- Guardrails prevent `init` from deleting or overwriting existing registries or Responsibility containers.
- Cross-responsibility writes remain prohibited during onboarding.
- Task Worker and external integrations are optional; onboarding must succeed without them.

## References
- `JANE_ZERO_SEED_ONBOARDING_SPEC.md` for onboarding flow details.
- `INIT_COMMAND_INTEGRATION_SPEC.md` for command routing and outputs.
