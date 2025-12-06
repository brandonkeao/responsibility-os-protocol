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

## BOOT_SUMMARY Enforcement
- **Ownership** – BOOT\_SUMMARY artifacts are steward-owned but Guardrails enforce that only `kernel.boot.regenerate` may create or update them. Any manual modification attempt (file hash mismatch without a corresponding regeneration entry) triggers `boot_summary_violation` and halts mandate activation.
- **Drift Control** – Each regeneration logs `(previous_hash, new_hash, responsibility_id)` to memory. Guardrails compare the latest hash against the on-disk file during every Phase 0 check; mismatches block boot.
- **Auditability** – Guardrails retain a ledger of regeneration events so auditors can prove which policies and tools were in effect at any point in time.
