# Agent Specification

Agents are operational workers (human or synthetic) that execute Kernel-planned steps subject to Guardrails enforcement.

## Registration
- Kernel ingests an agent capability manifest referencing Guardrails clause coverage.
- Append-only memory stores the manifest hash plus approval status.
- Guardrails confirm the agent's allowed tools and data domains before the Kernel routes any work.

## Execution Flow
1. Kernel issues a step with `guardrail_ref`.
2. Agent acknowledges the step, writing the acknowledgement to append-only memory.
3. Agent executes action, cites the Guardrails clause satisfied, and emits observations.
4. Kernel validates output; Guardrails re-check context to ensure no drift from policy.

## Accountability
- Every agent run references the supervising persona plus either the active mandate run ID or the RequestForAction ID being serviced.
- Guardrails may pause or revoke agent access if outputs violate policy; Kernel records the pause decision in memory.
- Agents must emit reflective notes when uncertainty is high, enabling stewards to update Guardrails if needed.

Agents never interact with live data unless a Guardrails clause authorizes it. This keeps the protocol safe for open-source use.
