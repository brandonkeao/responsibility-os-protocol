# Kernel Specification

The Kernel is the deterministic core that interprets Mandates, sequences agents, and writes append-only records. It operates only when paired with the Guardrails module, which must approve every state transition and every RequestForAction handoff accepted into the queue.

## Functions
1. **Mandate Intake** – Validates mandate definitions and run requests, links to Guardrails clauses, and enqueues with priority metadata pulled from the SQL System-of-Record.
2. **Task Planner** – Breaks mandates into atomic steps. Each step embeds `guardrail_ref` so Guardrails can evaluate safety preconditions.
3. **Agent Router** – Matches steps to agents or stewards. Router consults persona capabilities and Guardrails to confirm permissions.
4. **Memory Writer** – Commits structured events to append-only memory, exposing monotonic IDs for later audit.
5. **Request Bridge** – Reads deterministic RequestForAction rows, records accept/defer/reject choices, and mirrors results into the System-of-Context.
6. **Checkpoint Evaluator** – Queries Guardrails to ensure cumulative behavior remains compliant.

## Interfaces
- `kernel.decide(step, guardrail_ref)` returns allowed actions plus rationale.
- `kernel.append(memory_block)` writes immutable records; Guardrails hash the block for integrity.
- `kernel.recover(pointer)` replays history without mutation, honoring Guardrails redaction policies.
- `kernel.requests.claim(responsibility_id, batch_size)` deterministically selects pending RequestForAction rows for the target and returns references that can be mirrored into markdown views. AI may narrate these requests but never bypass this API.

The Kernel never executes arbitrary code—everything flows through declarative plans tied to Guardrails clauses.
