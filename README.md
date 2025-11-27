# Responsibility OS Protocol Repository

This repository contains the open-source specification set for Responsibility OS protocol v1. It includes the canonical specs, steward examples, and a progress log that lets contributors evolve the protocol without bundling any product workspaces or personal data.

## Repository Layout
- `PROTOCOL_BOOTSTRAP_V1.md` – original bootstrap brief that defines the required structure and rules.
- `protocol/specs/v1/` – ordered specification files (`00_overview.md` → `09_ui_translation.md`). Read them sequentially to understand how Kernel, Guardrails, personas, charges, agents, memory, and UI translation interact.
- `protocol/examples/steward/` – reference steward artifacts (responsibility, kernel, guardrails, persona, and sample charges) proving the specs are actionable.
- `protocol/progress/PROGRESS_LOG.md` – append-only changelog documenting version bumps or adjustments.
- `protocol/README.md` – quick start guide for anyone authoring protocol materials.

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
