# AI Activity Workspace

This folder hosts the dedicated, append-only log system for all AI-enabled collaboration surrounding the Responsibility OS Protocol. It lives outside the `protocol/` tree so operational metadata never pollutes the canonical specifications.

## Scope
- Capture every chat or message input that influences protocol decisions.
- Record Kernel-aligned decisions, Guardrails considerations, and resulting events.
- Store remediation or follow-up actions triggered by AI assistance.

## Operating Rules
1. **Append-Only Logs** – All entries live under `logs/` as dated files. Do not edit history; add corrective notes as new entries.
2. **Message Traceability** – Each entry must link to the originating conversation (URL, transcript snippet, or hash) plus the relevant protocol artifact.
3. **Decision Context** – Document which Kernel and Guardrails clauses were referenced or impacted by the action.
4. **Event Hooks** – When logs describe changes to the protocol repo, reference the commit hash or spec file path for future audits.
5. **Privacy** – Strip personal data; keep references abstract just like the core protocol specs.

Adhering to these rules keeps AI operations auditable without violating the no-workspace constraint inside the protocol specification.
