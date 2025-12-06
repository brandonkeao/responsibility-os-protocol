# Responsibility OS Protocol Repository

This repository carries the open-source specification set for Responsibility OS protocol v1 plus a long-lived roadmap for responsible autonomy. It currently ships the core specs and steward examples needed to bring a transparent Kernel + Guardrails system online.

## Current Protocol Snapshot
Responsibility OS v1 codifies Kernel, Guardrails, personas, charges, agents, and append-only memory primitives so teams can stand up an auditable co-pilot. The numbered files in `protocol/specs/v1/` act as a linear playbook: read the overview, lock in invariants, and then extend personas or charges with the steward examples under `protocol/examples/steward/`. `PROTOCOL_BOOTSTRAP_V1.md` documents the original bootstrap contract and `protocol/progress/PROGRESS_LOG.md` tracks every spec adjustment.

## Long-Term Vision
Responsibility OS is meant to evolve into a portable Context OS that travels with stewards, adapts to new model backends, and scales from solo operators to organizations. The design principles derive from safety engineering (Kernel/Guardrails interlocks), knowledge management (append-only memory and traceable personas), and organizational science (clear charge delegation and stewardship). Engineering priorities focus on deterministic planning interfaces, policy-aware tooling that keeps safety clauses inline, and lineage-preserving storage so auditors can cross disciplines—from compliance to product operations—without losing context.

Future scope areas include trust tooling (cryptographic Guardrails attestations and reproducible planning traces), federated persona registries for multi-organization stewardship, structured UI translation layers that keep enforcement metadata intact, and reference deployments that demonstrate how Context OS patterns integrate with existing DevOps and compliance pipelines.

## Repository Layout
- `PROTOCOL_BOOTSTRAP_V1.md` – original bootstrap brief that defines the required structure and rules.
- `protocol/specs/v1/` – ordered specification files (`00_overview.md` → `10_tasks.md`). Read them sequentially to understand how Kernel, Guardrails, personas, mandates, agents, memory, UI translation, and now Task routing interact.
- `protocol/examples/steward/` – reference steward artifacts (responsibility, kernel, guardrails, persona, and sample mandates) proving the specs are actionable.
- `protocol/examples/task_worker/` – reusable Task Worker persona, mandates, and BOOT_SUMMARY so service roles can be instantiated verbatim.
- `protocol/examples/fixtures/mandate_to_task_end_to_end.md` – golden flow showing Mandate → RFA → Task → telemetry/memory updates.
- `protocol/progress/PROGRESS_LOG.md` – append-only changelog documenting version bumps or adjustments.
- `protocol/README.md` – quick start guide for anyone authoring protocol materials.
- Cross-cutting specs live beside the steward examples (`RESPONSIBILITY_FILESYSTEM_STANDARD_V0_1.md`, `RESPONSIBILITY_BOOT_TEMPLATE.md`, `RESPONSIBILITY_STARTUP_CHECKLIST.md`, `TASK_WORKER_BOOT_SPEC.md`, `AI_CONTEXT_BUNDLES.md`, `REQUEST_FOR_ACTION_SPEC.md`, `RESPONSIBILITY_REGISTRY_SPEC.md`, `INTENT_ROUTER_SPEC.md`, `EVENT_TRIGGER_SPEC.md`, `DATA_LINEAGE_SPEC.md`, `TELEMETRY_SPEC.md`, `telemetry/policies.default.yaml`) and define shared infrastructure contracts.
- `docs/agentic_os_tasks_protocol_update.md` documents the Task worker + Google Workspace sync rollout plan.
- `docs/agentic_os_protocol_tdd.md` provides a narrative walkthrough of the entire Responsibility OS protocol for new contributors.
- Runbooks live under `runbooks/`. Start with `runbooks/README.md` for the standard “create workspace → request boot → log signoff + onboarding guide” flow, then follow the specific runbook you need (e.g., `runbooks/dad_mode_boot_runbook.md`).
- `boot_trial_logs/` stores timestamped folders for each simulated or live boot (`dad_mode_signoff.md` + `potential_issues.md`) so the operational state stays auditable.

## Getting Started
1. Clone the repository:
   ```bash
   git clone git@github.com:brandonkeao/responsibility-os-protocol.git
   cd responsibility-os-protocol
   ```
2. Review `protocol/README.md` and then walk through the numbered files in `protocol/specs/v1/`.
3. Use the steward examples as templates when you create new personas or charges; keep them domain neutral and reference both Kernel and Guardrails clauses.

## Usage Guidelines
- Treat everything as append-only. If you need to revise history, add a new entry (spec file, steward artifact, or progress note) rather than editing away prior context.
- Never add product code, UI code, or personal data. This repository is strictly for specs and neutral examples.
- Do not create a `workspaces/` directory; coordination artifacts belong in separate repos.

## Contributing
We follow standard open-source contribution etiquette:
1. **Discuss** – Open an issue describing the change (e.g., spec clarifications, new steward artifacts, protocol enhancements). Reference the relevant spec files and Guardrails clauses.
2. **Branch** – Create a descriptive branch name such as `feature/invariant-updates` or `docs/add-charge-template`.
3. **Implement** – Update specs or examples, ensuring Kernel and Guardrails references remain explicit. Append new entries to `protocol/progress/PROGRESS_LOG.md` when you change invariants or steward behavior.
4. **Test/Review** – Self-review for compliance with the repository rules (append-only memory, no personal data) and ensure markdown lint or spell-check passes if you have those tools available.
5. **Pull Request** – Submit a PR referencing the issue, summarizing the changes, and listing any follow-up actions. Expect maintainers to request additional clarity or Guardrails mapping as part of the review.

## License and Code of Conduct
- Unless otherwise stated in individual files, assume contributions are made under the repository’s default license (add one if/when you choose; MIT or Apache 2.0 are common for spec repos).
- Contributors are expected to follow standard open-source community norms: be respectful, document intent, and keep discussions focused on improving the protocol.

For major proposals (new spec sections, Guardrails rewrites, persona taxonomy changes), please start a discussion thread or RFC in an issue so the steward community can review before you open a pull request.
