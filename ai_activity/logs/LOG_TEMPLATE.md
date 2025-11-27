# AI Work Log Template

Copy this template into a dated file named `YYYY-MM-DD.md` inside the `ai_activity/logs/` directory. Append new entries to the bottom of the file.

```
## Entry {sequential_id}
- Timestamp: {UTC ISO8601}
- Participants: {AI agent(s) + human stewards}
- Message Input:
  - Source: {chat/tool/issue link}
  - Summary: {2-3 lines capturing the request}
- Kernel Context:
  - Relevant Charge ID(s): {charge ids, if any}
  - Kernel Decision IDs: {if applicable}
- Guardrails Context:
  - Clause References: {e.g., safety.runtime_integrity}
  - Outcome: {approved/denied/escalated}
- Decision / Event:
  - Action: {what changed in the protocol or repo}
  - Memory Pointer: {append-only reference or log hash}
- Follow-up:
  - Next Steps: {tasks, owners, due dates}
  - Status: {open/closed}
```

## Usage Notes
- When multiple chat snippets inform one decision, nest bullet points under `Message Input` to keep provenance clear.
- If no Kernel decision IDs exist yet, state `pending` so auditors know the action needs backfill.
- Always reference file paths (e.g., `protocol/specs/v1/03_kernel.md`) or commit hashes when logging code work.
