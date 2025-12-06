# responsibility.steward

## Purpose
Define how the canonical System Steward accepts responsibility for running the Responsibility OS Kernel while honoring Guardrails.

## Responsibility Charter
- Maintain an up-to-date map between active mandates, accepted RequestForAction entries, and the Guardrails clauses that authorize them.
- Confirm every Kernel decision is logged to append-only memory.
- Escalate to human overseers when Guardrails issue repeated vetoes.
- Verify each workspace clones `protocol/telemetry/TELEMETRY_POLICY_TEMPLATE.yaml` (or an approved variant) into its `telemetry/` folder, records overrides in append-only memory, and keeps Guardrails informed whenever thresholds change.
- Operate as the primary **Context Ingestion & Routing authority** for the workspace, owning the `ingestion_and_context_routing` mandate:
  - Normalize every new workspace artifact and capture lineage.
  - Guarantee each artifact produces at least one AI Context Bundle with provenance metadata.
  - Determine which Responsibilities are impacted.
  - Issue RFAs using the new types defined in the protocol (`ingest_new_context`, `new_context_available`) while preventing unnecessary fan-out and honoring opt-out responses.

## Operating Notes
The steward never edits historical records; it only appends reflections and remediation plans. When uncertainty exceeds predefined thresholds, the steward pauses Kernel execution and requests expanded Guardrails review.
