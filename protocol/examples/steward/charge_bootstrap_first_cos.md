# charge.steward.bootstrap_first_cos

## Title
Bootstrap the first Circle of Stewardship (CoS) instance.

## Intent
Stand up a minimal Responsibility OS deployment with Kernel, Guardrails, and Steward persona configured for collaborative work.

## Success Metrics
- Kernel planner responds to test charge within expected latency.
- Guardrails veto test demonstrates proper enforcement.
- Append-only memory captures setup steps with cross-referenced IDs.

## Constraints
- Use open-source safe defaults only.
- No external integrations until Guardrails sign-off is stored in memory.
- Guardrails clauses: `safety.bootstrap`, `scope.foundation_only`.

## Handoff Plan
If setup stalls, log current state to memory and assign the charge to another steward persona with infrastructure capabilities.
