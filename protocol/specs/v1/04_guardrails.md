# Guardrails Specification

Guardrails define the operative safety, compliance, and ethics boundaries that every Kernel module references before acting. They act as an always-on co-processor that can veto Kernel decisions.

## Components
1. **Policy Library** – Canonical set of clauses mapped to risks. Each clause includes escalation instructions and Kernel callback signatures.
2. **Evaluator** – Runs policies against proposed Kernel actions. Evaluator must confirm append-only memory entries exist for prerequisite context.
3. **Interlocks** – Mechanisms that pause or halt Kernel loops when clauses fail. Interlocks always log the decision to memory before signaling the Kernel, including blocking a RequestForAction transition when the target Responsibility lacks an appropriate mandate.
4. **Transparency Layer** – Exposes human-readable rationales referencing policy IDs so stewards can explain enforcement outcomes.

## Enforcement Flow
- Kernel submits `guardrail_ref` plus context.
- Guardrails evaluate policies, referencing prior memory entries to preserve append-only audit trails.
- Guardrails verify that any RequestForAction status change aligns with the deterministic state machine defined in the protocol and cross-checks the SQL queue row.
- If approved, Guardrails sign the decision and return it to the Kernel. If rejected, a remediation instruction is emitted and logged.

Guardrails must be versioned with semantic identifiers. Kernel loads only compatible versions, preventing silent drift between safety code and operational logic.
