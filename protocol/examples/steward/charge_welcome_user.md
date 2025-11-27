# charge.steward.welcome_user

## Title
Welcome a new collaborator into Responsibility OS without exposing sensitive data.

## Intent
Provide a concise orientation packet, highlight Kernel + Guardrails structure, and point to append-only memory for prior decisions so the collaborator sees the audit trail.

## Success Metrics
- New collaborator acknowledges the Guardrails summary.
- A welcome note is appended to memory referencing this charge ID.

## Constraints
- No product-specific examples.
- Use only public protocol artifacts.
- Guardrails clauses: `safety.intro`, `transparency.audit`.

## Handoff Plan
If the steward is unavailable, the Kernel routes this charge to any persona with the "orientation" capability and records the transfer.
