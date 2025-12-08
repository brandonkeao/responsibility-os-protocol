---
layer: core
change_risk: high
---

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

## Task Materialization

Every active mandate now emits a list of canonical Tasks before Responsibilities route work. The Kernel populates the schema defined in `docs/agentic_os_tasks_protocol_update.md`:

- `task_id` (`uuid`), `mandate_id`, `title`, `description`
- `preferred_responsibilities` (`[]string`) – hints for routing when multiple Responsibilities share the same mandate scope.
- `status` (`needs_action | in_progress | blocked | completed`) with Guardrails-approved transitions enforced by the Task Worker.
- `priority` (`low | normal | high`, mapped deterministically to integer queues) and optional `due_date`.
- `external_refs` for Google Task IDs or calendar events created via `google_workspace_mcp`; sync bridges may create/update external artifacts but never delete Tasks.
- `source` (gmail, voice, manual, automation) plus timestamps (`created_at`, `updated_at`).

Mandate runs cite the Task IDs they spawned so auditors can trace Mandate → Task → Responsibility decisions. Only the Task Worker can mutate status fields. Kernel+Guardrails treat missing Task references as a protocol violation and will block execution until the Tasks are rehydrated.

**Safety Rules**
- Tasks are never auto-deleted; archival requires a Guardrails-approved migration entry.
- Calendar deletions cannot cascade into Task removal.
- Only the Task Worker may transition Task status, priority, or due dates.

## Relationship to Requests

- Mandates = internal authority (System-of-Context) with deterministic activation via Kernel APIs.
- RequestForAction = external ask (System-of-Record) that may trigger mandate runs but never bypasses Guardrails.

All cross-responsibility work **must** originate as a RequestForAction. Tasks that represent external intent must cite `request_id` in their `source` field, and the Kernel refuses to create cross-responsibility Tasks without an accepted RFA reference. A Responsibility should only accept an RFA if it already has a mandate that covers the requested work or if it drafts a new mandate through the proposal process.

Context ingestion uses specialized RFAs:
- Tooling submits `ingest_new_context` to the workspace steward (Jane) whenever a bundle is created outside the steward’s direct control.
- The steward distributes validated bundles via `new_context_available` to impacted Responsibilities.
Mandates governing ingestion must reference these types explicitly so Guardrails can enforce routing hygiene.

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
