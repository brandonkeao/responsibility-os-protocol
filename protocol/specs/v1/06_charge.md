# Charge Specification

Charges are structured intent packets that flow through the Kernel while being validated by the Guardrails.

## Schema
- `charge_id` – Stable identifier referenced in memory and Kernel routing tables.
- `title` – Short description of the desired outcome.
- `intent` – Multi-paragraph context kept free of implementation detail.
- `success_metrics` – Quantitative or boolean tests; Guardrails evaluate legality/ethics constraints for each metric.
- `constraints` – Direct references to Guardrails clauses and any temporal or resource limits.
- `handoff_plan` – How responsibility can move between personas or agents; Kernel confirms that append-only memory records each handoff.

## Lifecycle
1. **Draft** – Steward drafts the charge, linking at least one Guardrails clause.
2. **Review** – Guardrails static checks run; Kernel rejects drafts without approvals.
3. **Activation** – Kernel assigns the charge to a persona plus agent set, recording the event in append-only memory.
4. **Completion** – Steward writes a completion report, referencing Kernel decision IDs so auditors can reconstruct the path.

Charges cannot be edited after activation. Any change requires a new charge referencing the superseded ID so history stays append-only.
