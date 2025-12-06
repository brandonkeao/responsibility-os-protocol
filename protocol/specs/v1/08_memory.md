# Memory Specification (Append-Only)

Memory is a tamper-evident, append-only ledger that stores every Kernel decision, Guardrails evaluation, and steward reflection.

## Principles
1. **Append-Only Writes** – Kernel exposes only `memory.append(record)`; there is no update or delete verb. Guardrails monitor the log to detect forbidden mutations.
2. **Structured Entries** – Each record contains `timestamp`, `actor`, `mandate_run_id` or `request_id`, `task_id` (when applicable), `kernel_decision_id`, `guardrail_clause_id`, and a payload. Payloads can reference artifacts but cannot include personal data.
3. **Integrity** – Guardrails hash every entry and store rolling digests so append-only history can be audited externally.
4. **Access** – Read operations stream ordered views. Kernel enforces pagination while Guardrails redact sensitive clauses when required.

## Usage Patterns
- **Planning** – Kernel checkpoints plan states, enabling replay without deviating from Guardrails.
- **Reflection** – Stewards append post-task learnings; Guardrails verify remediation steps exist for incidents.
- **Handoffs** – Agent and persona transfers add linked entries so auditors can follow the responsibility chain.
- **Request Audits** – Accept/defer/reject decisions for RequestForAction records append summaries referencing the deterministic SQL row so markdown mirrors can be regenerated at any time.
- **User Input Intake** – Each Responsibility records user/operator inputs as timestamped bullets in `memory/events.md` with source and pointers to mandates, Tasks, or RFAs. Intake helpers should normalize the shape (e.g., `- 2025-12-06T17:25:00Z user_input (source: human:brandon, task: task-123) – Requested weekly risk digest`).

Memory drives trust in Responsibility OS. Because it is append-only, contributors can audit the lineage of any action by cross-referencing Kernel IDs with Guardrails clauses.
