# Telemetry Specification

Telemetry ensures every Responsibility OS deployment exposes health, cost, and drift signals through the same deterministic channels that govern mandates, requests, and events. This spec mirrors other System-of-Record schemas so kernels, guardrails, and stewards can observe the system without bespoke logging.

## Goals

1. Provide a canonical schema for heartbeat, latency, cost, and drift measurements.
2. Keep telemetry append-only and auditable, with Guardrails clauses referencing each record.
3. Enable deterministic alerting and memory reflections when thresholds are breached.

## System-of-Record Schema

```sql
CREATE TABLE telemetry_metrics (
  id                 INTEGER PRIMARY KEY AUTOINCREMENT,
  component_id       TEXT NOT NULL,        -- e.g., 'kernel', 'guardrails', 'context_worker'
  workspace_id       TEXT NULL,
  responsibility_id  TEXT NULL,
  metric_name        TEXT NOT NULL,        -- 'heartbeat', 'queue_latency_ms', 'model_cost_usd'
  metric_value       REAL NOT NULL,
  unit               TEXT NOT NULL,        -- 'ms', 'usd', 'count'
  measurement_window TEXT NOT NULL,        -- ISO 8601 duration such as 'PT1M'
  status             TEXT NOT NULL,        -- 'ok' | 'warning' | 'critical'
  guardrail_clause   TEXT NOT NULL,
  recorded_at        DATETIME NOT NULL,
  context_json       TEXT NULL             -- payload with pointers (request_id, mandate_run_id, etc.)
);

CREATE TABLE telemetry_alerts (
  id                INTEGER PRIMARY KEY AUTOINCREMENT,
  metric_id         INTEGER NOT NULL REFERENCES telemetry_metrics(id),
  alert_type        TEXT NOT NULL,         -- 'sla_breach', 'model_drift', 'cost_threshold'
  severity          TEXT NOT NULL,         -- 'info' | 'warning' | 'critical'
  note              TEXT NULL,
  created_at        DATETIME NOT NULL,
  acknowledged_at   DATETIME NULL,
  acknowledged_by   TEXT NULL              -- steward or automation id
);
```

## Metric Classes

| Class            | Description | Example `metric_name` | Guardrail Reference |
|------------------|-------------|-----------------------|---------------------|
| Heartbeat        | Liveness of Kernel, Guardrails, context workers, and registries. | `heartbeat` with `metric_value = 1`. | `runtime.uptime` |
| Queue Health     | Depth, latency, SLA adherence for RequestForAction queues. | `queue_depth`, `queue_latency_ms`. | `requests.sla_compliance` |
| Cost & Usage     | Token or API spend per responsibility or workspace. | `model_cost_usd`, `token_usage`. | `runtime.cost_budget` |
| Model Drift      | Detected vs preferred model mismatches. | `model_drift_detected`. | `runtime.model_integrity` |
| Error Budget     | Number of Guardrail vetoes, failed events, or retries. | `guardrail_veto_rate`, `event_retry_count`. | `safety.runtime_integrity` |
| Context Ingestion | Steward handling of workspace context bundles. | `context_ingested`, `context_dispatched`. | `context.routing_integrity` |
| Boot Model Enforcement | Per-responsibility model verification at boot. | `model_mismatch_on_boot`. | `runtime.model_integrity` |

## Guardrails Integration

- Guardrails clauses define acceptable ranges. When kernels insert telemetry rows they must cite the clause that authorizes or monitors that metric (e.g., `runtime.cost_budget`).
- Guardrails read `telemetry_metrics` to auto-escalate when `status = 'critical'`, optionally emitting a RequestForAction or mandate run to remediate.
- Telemetry alerts should append a note into `memory/events.md` referencing `telemetry_alerts.id` so auditors can trace remediation steps.

### Event Payload Requirements
- `context_ingested`: emitted when Jane accepts a bundle (via `ingest_new_context` or workspace drop). Payload MUST include `bundle_ids`, `rfa_ids`, `responsibility_ids_notified` (if known), `workspace_id`, and timestamp.
- `context_dispatched`: emitted when Jane sends `new_context_available` RFAs. Same payload requirements as above plus the list of RFAs created.
- `model_mismatch_on_boot`: emitted during Phase 0/1 of the startup checklist whenever `actual_model` differs from `default_model`. Payload MUST include `responsibility_id`, `default_model`, `actual_model`, `operator_decision` (`proceed`, `abort`, `update_default_model`), and the memory pointer documenting the decision.
- `responsibility_migration`: emitted when exporting/importing a Responsibility container. Payload SHOULD include `responsibility_id`, `workspace_id`, `action` (`export|import|backfill`), `manifest_hash`, `context_hash`, `boot_summary_hash`, and pointers to `telemetry/incidents/migration_<timestamp>.md`.

## Kernel & Worker Responsibilities

- **Kernel** records heartbeats at least every minute per active workspace and logs queue depth/latency after each RequestForAction claim cycle.
- **Guardrails** log veto counts and policy drift metrics at the end of each evaluation batch.
- **Context Workers** record bundle refresh duration, model preference verification results, and context file sizes to help tune schedules.
- **Event Processors** log success/failure ratios per source to surface integration issues.

All writers must treat telemetry tables as append-only; no updates or deletes outside of deterministic archival jobs approved by Guardrails.

## Consumption Patterns

1. Steward dashboards query `telemetry_metrics` grouped by `component_id` and `metric_name` to render health widgets.
2. Alerting services watch for `status != 'ok'` and emit `telemetry_alerts` rows plus optional RequestForAction entries targeting the relevant responsibility.
3. AI assistants read markdown mirrors (`reports/telemetry/*.md`) generated from SQL snapshots so they can narrate health state without direct database writes.

## Markdown Mirror Contract

Installations may materialize telemetry summaries under `reports/telemetry/<YYYY-MM-DD>.md` using frontmatter:

```md
---
report_type: telemetry_snapshot
source: telemetry_metrics
generated_at: 2025-11-28T11:00:00Z
workspace_id: dad_mode
guardrail_clause: runtime.telemetry_reporting
---
```

The body should include tables or bullet lists referencing metric IDs, alert IDs, and recommended follow-ups. As with queue views, these files are views and may be regenerated anytime.

## Policy Template

To avoid ad-hoc thresholds, start from `protocol/telemetry/policies.default.yaml`. Copy it into the target workspace (e.g., `telemetry/policies.parenting_cos.yaml`) and adjust values per Responsibility. The defaults cover:

- Heartbeat intervals by component (`runtime.uptime`, `safety.runtime_integrity`).
- Request queue latency and SLA timers (`requests.sla_compliance`).
- Daily cost budgets (`runtime.cost_budget`).
- Task Worker sync retry ceilings (`taskworker.sync_integrity`).
- Model drift enforcement windows (`runtime.model_integrity`).
- Event retry counts and escalation hooks (`events.retry_policy`).
- Task Worker sync degradation handling (`taskworker.sync_integrity`).

Responsibilities may override the defaults by adding an entry under the `overrides` section keyed by `responsibility_id`. Kernels should load the effective policy at boot, record the file hash in memory, and feed the values into telemetry alerting logic so new installations inherit sane thresholds without editing the spec. Any overrides must be recorded in append-only memory with pointers to the policy file version and guardrail clause enforcing it.

## Append-Only Memory Hooks

Whenever a telemetry alert is created or resolved:

- Append to `memory/events.md`: include `telemetry_alert_id`, `metric_id`, `status`, remediation summary, and any spawned mandate run or RequestForAction IDs.
- Reference the guardrail clause that triggered the remediation so auditors can replay enforcement logic.

By mirroring telemetry in the same deterministic patterns as RFAs and events, Responsibility OS keeps observability portable and auditable across deployments.
