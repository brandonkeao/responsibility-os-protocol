# Responsibility OS Protocol

This repository bootstraps the Responsibility OS Protocol v1. It defines the core specifications, a steward reference implementation, and a lightweight progress log so additional contributors can extend the protocol without shipping product code.

## Layout
- `specs/v1` – canonical protocol specification ordered from overview through UI translation.
- `examples/steward` – system steward artifacts that exercise the spec and prove it is actionable.
- `progress/PROGRESS_LOG.md` – append-only notes about protocol evolution.
- `RESPONSIBILITY_REGISTRY_SPEC.md`, `INTENT_ROUTER_SPEC.md`, `EVENT_TRIGGER_SPEC.md`, `DATA_LINEAGE_SPEC.md`, `REQUEST_FOR_ACTION_SPEC.md`, `RESPONSIBILITY_FILESYSTEM_STANDARD_V0_1.md`, `AI_CONTEXT_BUNDLES.md` – cross-cutting references formalizing the registry, routing, events, lineage, queue, filesystem layout, and AI context worker patterns.

## Working Principles
1. Kernel and Guardrails are always referenced explicitly when describing any subsystem.
2. Memory is append-only and auditable across specs and steward artifacts.
3. No personal, product, or workspace data lives in this repo.
4. Steward artifacts stay domain-neutral so they can be remixed by any Responsible OS instance.

Contributors should read `specs/v1/00_overview.md` first, then follow the numbered files to understand how to extend the protocol.
