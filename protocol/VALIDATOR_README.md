---
authored_by: human
author_id: protocol_steward
created_at: 2025-12-06T20:32:00Z
updated_at: 2025-12-06T20:32:00Z
source: protocol_update:validator_stub
context_role: validator
---
# Protocol Compliance Validator (Stub)

This stub outlines automated/LLM validation to enforce recent context/GIP updates. Implement as a CLI, CI check, or a dedicated “Protocol Steward” responsibility.

## Checks (fail unless noted warn)
- Golden Identity Prompt: present, non-empty, mission/optimization/boundaries/failure modes, single definition.
- Context Packs: `context_pack.yaml` required fields (id, name, discipline, scope, version, files; warn if mem0 missing).
- Structured files: required frontmatter fields and sections (TL;DR, Objectives, Core Principles, Steps, Heuristics, Examples/Anti-Examples, Interactions).
- UTB enforcement: no raw concatenation; UTB present; size 500–1,200; aligned to persona + GIP; log if synthesis fails.
- Density warning: warn if estimated >3,500 tokens or more than 2 primary packs; require operator override logging.
- mem0 injections (if used): summarized, bounded by pack limits, injected below UTB and above user input; fail if ordering/limits violated.
- Execution stack order: Guardrails > GIP/persona > UTB > memory > user task.
- Operator override logging: warn/fail if dense runs have no override confirmation.
- Legacy mode: warn if Responsibility lacks GIP/packs; require upgrade plan.

## Output
- Violations (fail), warnings (risk), passed checks, confidence score.
