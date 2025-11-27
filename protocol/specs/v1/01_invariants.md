# System Invariants

The Kernel enforces deterministic loops that steward agents must follow, and the Guardrails interlock with each step to block unsafe transitions. The following invariants hold for any Responsibility OS deployment:

1. **Alignment Loop** – Every task proposal references a current charge plus the Guardrails section that authorizes it; the Kernel refuses execution if either link is missing.
2. **Memory Append-Only** – Interaction logs, steward reflections, and charge outcomes write to append-only memory. The Kernel exposes only additive operations and the Guardrails verify no mutation occurred.
3. **Charge Integrity** – Charges are immutable intent packages. Kernel validates signatures and Guardrails check scope and temporal bounds before admitting the charge to the queue.
4. **Persona Consistency** – Persona traits cannot contradict Guardrails. The Kernel halts activation when persona traits request capabilities outside the Guardrails allowlist.
5. **Auditability** – Every action produces a traceable tuple `(kernel_decision_id, guardrail_clause_id, memory_pointer)`. This tuple anchors reviewers to both Kernel and Guardrails artifacts.

Breaking an invariant requires a protocol version bump recorded in `progress/PROGRESS_LOG.md` so stewards can coordinate upgrades.
