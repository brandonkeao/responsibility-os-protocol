# System Invariants

The Kernel enforces deterministic loops that steward agents must follow, and the Guardrails interlock with each step to block unsafe transitions. The following invariants hold for any Responsibility OS deployment:

1. **Alignment Loop** – Every Task record references either an active Mandate run or an accepted RequestForAction plus the Guardrails clause that authorizes it; the Kernel refuses execution if any link is missing.
2. **Memory Append-Only** – Interaction logs, steward reflections, and mandate outcomes write to append-only memory. The Kernel exposes only additive operations and the Guardrails verify no mutation occurred.
3. **Mandate Integrity** – Mandates are immutable intent packages. Kernel validates signatures and Guardrails check scope and temporal bounds before admitting the mandate run to the queue.
4. **Persona Consistency** – Persona traits cannot contradict Guardrails. The Kernel halts activation when persona traits request capabilities outside the Guardrails allowlist.
5. **Auditability** – Every action produces a traceable tuple `(kernel_decision_id, guardrail_clause_id, memory_pointer)`. This tuple anchors reviewers to both Kernel and Guardrails artifacts.
6. **Deterministic Requests** – RequestForAction records live in a SQL-backed queue that enforces status transitions, timestamps, and retries without AI intervention; markdown views are regenerated from the System-of-Record.
7. **Task Ownership** – Native Tasks are append-only objects. Only the Task Worker (running under Guardrails oversight) may mutate Task status, and sync bridges (e.g., `google_workspace_mcp`) can mirror state into Google Tasks or Calendar without ever deleting the canonical Task.

Breaking an invariant requires a protocol version bump recorded in `progress/PROGRESS_LOG.md` so stewards can coordinate upgrades.
