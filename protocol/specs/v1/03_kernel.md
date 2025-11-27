# Kernel Specification

The Kernel is the deterministic core that interprets charges, sequences agents, and writes append-only records. It operates only when paired with the Guardrails module, which must approve every state transition.

## Functions
1. **Charge Intake** – Validates charge schema, links to Guardrails clause, and enqueues with priority metadata.
2. **Task Planner** – Breaks charges into atomic steps. Each step embeds `guardrail_ref` so Guardrails can evaluate safety preconditions.
3. **Agent Router** – Matches steps to agents or stewards. Router consults persona capabilities and Guardrails to confirm permissions.
4. **Memory Writer** – Commits structured events to append-only memory, exposing monotonic IDs for later audit.
5. **Checkpoint Evaluator** – Queries Guardrails to ensure cumulative behavior remains compliant.

## Interfaces
- `kernel.decide(step, guardrail_ref)` returns allowed actions plus rationale.
- `kernel.append(memory_block)` writes immutable records; Guardrails hash the block for integrity.
- `kernel.recover(pointer)` replays history without mutation, honoring Guardrails redaction policies.

The Kernel never executes arbitrary code—everything flows through declarative plans tied to Guardrails clauses.
