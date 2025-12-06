# Kernel Specification

The Kernel is the deterministic core that interprets Mandates, sequences agents, and writes append-only records. It operates only when paired with the Guardrails module, which must approve every state transition and every RequestForAction handoff accepted into the queue.

## Functions
1. **Mandate Intake** – Validates mandate definitions and run requests, links to Guardrails clauses, and enqueues with priority metadata pulled from the SQL System-of-Record.
2. **Task Planner** – Breaks mandates into canonical Tasks. Each Task carries `guardrail_ref`, preferred responsibilities, priority, due date, and source metadata so Guardrails can evaluate safety preconditions before any execution.
3. **Task Worker Interface** – Issues signed commands to the dedicated Task Worker (the only actor allowed to mutate Task state) and bridges state to external providers such as Google Tasks via `google_workspace_mcp`. Kernel ensures sync mirrors cannot delete canonical Tasks.
4. **Agent Router** – Matches Tasks and plan steps to agents or stewards. Router consults persona capabilities and Guardrails to confirm permissions.
5. **Memory Writer** – Commits structured events to append-only memory, exposing monotonic IDs for later audit.
6. **Request Bridge** – Reads deterministic RequestForAction rows, records accept/defer/reject choices, and mirrors results into the System-of-Context.
7. **Checkpoint Evaluator** – Queries Guardrails to ensure cumulative behavior remains compliant.

## Interfaces
- `kernel.decide(step, guardrail_ref)` returns allowed actions plus rationale.
- `kernel.append(memory_block)` writes immutable records; Guardrails hash the block for integrity.
- `kernel.recover(pointer)` replays history without mutation, honoring Guardrails redaction policies.
- `kernel.requests.claim(responsibility_id, batch_size)` deterministically selects pending RequestForAction rows for the target and returns references that can be mirrored into markdown views. AI may narrate these requests but never bypass this API.
- `kernel.tasks.issue(command)` is the sole interface to the Task Worker. Commands capture Task creation, status transitions, and sync intents (`google_workspace_mcp`, calendar bindings). Guardrails validate each command before execution and log a corresponding memory pointer.
- `kernel.boot.regenerate(responsibility_id)` produces a fresh BOOT\_SUMMARY from canonical files, records a hash delta in memory, and updates Guardrails state so manual edits are never required.

The Kernel never executes arbitrary code—everything flows through declarative plans tied to Guardrails clauses.
