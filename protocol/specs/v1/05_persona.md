# Persona Specification

Personas describe how stewards or agents express behavior while staying inside Kernel and Guardrails boundaries.

## Fields
1. **Designation** – Unique name referenced by Kernel router; Guardrails confirm designation is approved.
2. **Mission** – Plain-language statement mapping to one or more charges and Guardrails clauses.
3. **Traits** – Ordered list of behavioral anchors (e.g., "evidence-seeking"). Kernel enforces trait priority when resolving conflicts; Guardrails reject traits that contradict policy.
4. **Capabilities** – Declarative allowlist of tools or contexts. Each capability references Guardrails coverage and is audited in memory.
5. **Operating Rhythm** – Cadence for check-ins and reflections. Kernel ensures the rhythm schedules append-only memory updates.

## Lifecycle
- **Registration** – Persona file submitted to Kernel; Guardrails hash and store pointer in append-only memory.
- **Activation** – Kernel links persona to an active charge, ensuring Guardrails approve both the charge scope and persona capabilities.
- **Retirement** – Persona marked inactive via append-only record. Kernel stops routing tasks, Guardrails enforce cooldown period.

Personas never include personal data; they are abstract stewardship roles that can be shared across organizations.
