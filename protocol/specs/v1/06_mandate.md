# Mandate Specification

Mandates (formerly called charges) are the internal authority packets a Responsibility uses to authorize work. They stay entirely inside a Responsibility, run under its Kernel + Guardrails pairing, and never grant direct control to other Responsibilities.

## Schema
- `mandate_id` – Stable identifier (`<responsibility>.<mandate_name>`).
- `title` – Short description of the authority domain.
- `intent` – Narrative of the desired outcome, referencing kernel scope and guardrail clauses.
- `success_metrics` – Quantitative or boolean tests the steward will check after each run.
- `constraints` – Guardrail references, resource limits, temporal bounds.
- `dependencies` – Optional list of mandate run IDs or RequestForAction IDs that must complete/accept before activation. Dependencies may include logical operators (`all`, `any`, `timeout_policy`).
- `handoff_plan` – How mandate runs can be reassigned between personas or agents; every handoff writes to memory and cites the governing guardrail clause.

Mandate definitions live in `mandates/definitions/` per the Responsibility Filesystem Standard. Each definition includes provenance frontmatter.

## Mandate Runs

When the Kernel activates a mandate it creates a **mandate run** record:

- Stored under `mandates/runs/<mandate_id>/<ISO8601>.md`.
- Contains step plans, references to RequestForAction IDs (if triggered externally), and outcomes.
- Links to append-only memory entries so auditors can replay the execution.
- Records dependency satisfaction (which prerequisites triggered activation) and orchestration metadata (parallel group ID, DAG node ID).

## Lifecycle

1. **Draft** – Steward documents the mandate definition and submits it to Guardrails for review.
2. **Approval** – Guardrails hash and sign the definition. Sensitive changes must go through the patch proposal workflow.
3. **Activation** – Kernel schedules a mandate run, often in response to a RequestForAction or a cadence timer. The run references the SQL queue row if applicable.
4. **Execution** – Agents perform planned steps; Kernel enforces guardrail references at each checkpoint.
5. **Completion** – Steward appends outcomes to `mandates/runs/...`, updates memory, and, if the run satisfied an RFA, marks the request completed in SQL.
6. **Retirement** – Mandate definition is superseded via a new patch proposal; previous versions remain on disk for audit purposes.

Mandates are immutable once activated. Any change requires creating a new run or new definition so history remains append-only.

## Relationship to Requests

- Mandates = internal authority (System-of-Context) with deterministic activation via Kernel APIs.
- RequestForAction = external ask (System-of-Record) that may trigger mandate runs but never bypasses Guardrails.

A Responsibility should only accept an RFA if it already has a mandate that covers the requested work or if it drafts a new mandate through the proposal process.

## Dependencies & Orchestration

Mandates may declare dependencies on other mandate runs or accepted RFAs. Kernels must evaluate these prerequisites before activation:

- **Type**: `mandate_reference`, `request_reference`, or `event_reference` (when event triggers are defined).
- **Mode**: `all` (default) requires every dependency to finish successfully; `any` activates once one dependency completes; `timeout_policy` dictates what happens if dependencies miss deadlines.
- **DAG Metadata**: Kernels may label mandate runs with `orchestration_group` IDs to support parallel or sequential execution graphs. Guardrails validate that no cycle exists and that escalations occur when timeouts fire.

Example dependency block inside a mandate definition:

```yaml
dependencies:
  mode: all
  timeout_policy: escalate_to:product_cos after:PT48H
  items:
    - type: request_reference
      id: req_2025-11-28_churn_to_growth_cohort_analysis
    - type: mandate_reference
      id: mandate.plg_growth.monthly_growth_analysis@2025-11-30T00:00Z
```

Kernels must expose `kernel.dependencies.status(mandate_run_id)` so stewards can inspect orchestration progress and Guardrails can enforce escalation clauses.
