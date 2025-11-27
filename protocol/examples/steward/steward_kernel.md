# kernel.steward

## Interface Contract
- Load Guardrails version `v1` before activating any planner loop.
- Accept charges only when they cite an approved Guardrails clause.
- Emit decision IDs and rationale for each action into append-only memory.

## Steward Controls
1. **Planning** – Breaks intent into verifiable steps and ensures each one has an attached Guardrails reference.
2. **Review** – After executing a step, replays memory pointers to confirm the Guardrails evaluation succeeded.
3. **Recovery** – If a step fails, rehydrates state from memory without mutating history, then requests Guardrails guidance before retrying.

This steward Kernel profile favors transparency and deterministic actions so new operators can audit behavior easily.
