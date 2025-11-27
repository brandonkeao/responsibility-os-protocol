# Responsibility Model

Responsibility OS defines responsibility as the contract between human intent, the Kernel execution path, and the Guardrails that bound behavior.

## Responsibility Chain
1. **Intent Capture** – Humans declare intent via charges; Kernel normalizes structure while Guardrails tag compliance requirements.
2. **Interpretation** – Steward interprets intent through persona filters; Kernel enforces deterministic parsing and Guardrails compare results against prohibited actions.
3. **Execution** – Agents act on behalf of the steward. Kernel issues step-level approvals and Guardrails verify context remains inside allowed scope.
4. **Reflection** – After execution, the steward records reflections and outcomes into append-only memory; Guardrails assert that remediation steps are logged when deviations occur.

## Transfer of Responsibility
Responsibility can be delegated only when:
- The receiving agent acknowledges the charge reference and corresponding Guardrails clause.
- Kernel records the delegation pointer in memory.
- Append-only memory contains both the transfer request and acceptance entries.

If the Guardrails detect missing acknowledgements, the Kernel reclaims responsibility and blocks further execution.
