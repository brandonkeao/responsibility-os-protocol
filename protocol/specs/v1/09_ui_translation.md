---
layer: context_infrastructure
change_risk: medium
---

# UI Translation Specification

Responsibility OS may surface interfaces for humans, but UI layers must remain faithful to Kernel decisions and Guardrails outcomes.

## Principles
1. **Source of Truth** – UI components render data straight from append-only memory or Kernel APIs; no derived state may bypass Guardrails validation.
2. **Clarity** – Every displayed action includes the relevant Guardrails clause ID and Kernel decision summary so humans understand enforcement context.
3. **Action Gating** – Buttons, prompts, or automations must call Kernel endpoints that already embed Guardrails checks. UI code never issues privileged actions on its own.
4. **Audit Hooks** – UI events (approvals, comments, overrides) append records to memory so auditors can correlate human input with Kernel behavior.

## Accessibility and Localization
- UI translation layers should separate content strings from policy logic, enabling safe localization while keeping Guardrails references intact.
- When translating summaries, always preserve the Kernel decision ID and Guardrails clause labels exactly, ensuring reviewers can match translations to source specs.

Adhering to this spec prevents interface drift from the Kernel and Guardrails contract, keeping human interactions auditable and compliant.
