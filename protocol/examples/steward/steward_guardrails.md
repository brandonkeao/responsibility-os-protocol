# guardrails.steward

## Principles
- Every Kernel request must include `guardrail_ref` and context payload.
- Evaluations produce a signed approval or denial that is appended to memory.
- Denials always include a remediation checklist for the steward.

## Clause Families
1. **Safety** – Prevents harmful or irreversible actions; Kernel cannot override these clauses.
2. **Privacy** – Blocks ingestion of personal data; mandates that append-only memory stores only anonymized artifacts.
3. **Scope** – Ensures mandates and RequestForAction items stay inside agreed problem space; Kernel halts when scope drift is detected.

Guardrails stewarding focuses on high signal-to-noise policies, using plain-language rationales so humans can understand why the Kernel was blocked.
