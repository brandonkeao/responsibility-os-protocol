# Memory Specification (Append-Only)

Memory is a tamper-evident, append-only ledger that stores every Kernel decision, Guardrails evaluation, and steward reflection.

## Principles
1. **Append-Only Writes** – Kernel exposes only `memory.append(record)`; there is no update or delete verb. Guardrails monitor the log to detect forbidden mutations.
2. **Structured Entries** – Each record contains `timestamp`, `actor`, `charge_id`, `kernel_decision_id`, `guardrail_clause_id`, and a payload. Payloads can reference artifacts but cannot include personal data.
3. **Integrity** – Guardrails hash every entry and store rolling digests so append-only history can be audited externally.
4. **Access** – Read operations stream ordered views. Kernel enforces pagination while Guardrails redact sensitive clauses when required.

## Usage Patterns
- **Planning** – Kernel checkpoints plan states, enabling replay without deviating from Guardrails.
- **Reflection** – Stewards append post-task learnings; Guardrails verify remediation steps exist for incidents.
- **Handoffs** – Agent and persona transfers add linked entries so auditors can follow the responsibility chain.

Memory drives trust in Responsibility OS. Because it is append-only, contributors can audit the lineage of any action by cross-referencing Kernel IDs with Guardrails clauses.
