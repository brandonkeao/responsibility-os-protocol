# Event Trigger Specification

External systems (webhooks, polling jobs, sensors) may notify the Kernel about new information. Event triggers convert those notifications into deterministic mandate runs or RequestForAction entries without relying on ad-hoc AI reasoning.

## System-of-Record Schema

```sql
CREATE TABLE events (
  id            TEXT PRIMARY KEY,
  source        TEXT NOT NULL,             -- e.g., 'stripe', 'calendar', 'school_portal'
  type          TEXT NOT NULL,             -- e.g., 'subscription_cancelled'
  payload_json  TEXT NOT NULL,
  received_at   DATETIME NOT NULL,
  processed_at  DATETIME NULL,
  status        TEXT NOT NULL DEFAULT 'pending', -- 'pending' | 'processing' | 'completed' | 'failed'
  retriable     INTEGER NOT NULL DEFAULT 1,
  metadata_json TEXT NULL
);
```

Event processors may log lifecycle entries to `event_history` (similar to `request_events`).

## Trigger Mapping

Mappings live in System-of-Context under each Responsibility, e.g., `triggers/<responsibility_id>.yaml`:

```yaml
- source: stripe
  type: subscription_cancelled
  guardrail_clause: data.billing_scope
  action:
    kind: mandate_run
    mandate_id: mandate.churn.process_new_cancellation
    payload_template: payloads/stripe_cancellation_to_mandate.json
- source: school_calendar
  type: meeting_added
  action:
    kind: request_for_action
    target_responsibility_id: parenting_cos
    template: payloads/calendar_event_to_rfa.md
```

Kernels read mappings and when an event arrives will:
1. Validate Guardrails clause(s) for the source.
2. Execute the action (spawn mandate run or create RFA) with deterministic payload templating.
3. Update the `events` table and append a memory entry referencing both the event ID and resulting mandate/request IDs.

## Kernel API
- `kernel.events.ingest(source, type, payload)` – inserts into SQL and enqueues for processing.
- `kernel.events.process(event_id)` – executes mapping, handles retries, updates status.
- `kernel.events.status(event_id)` – returns lifecycle info for monitoring.

## Guardrails Considerations
- Guardrails may block certain sources or types unless approved (e.g., personal email ingest).
- Rate limits and throttling policies should be encoded in guardrail clauses (e.g., `stripe.events_per_minute <= 60`).

## Observability
Track:
- Pending vs processed count.
- Average latency from `received_at` to mandate/RFA creation.
- Failure rate and retry attempts.

These metrics should surface in stewardship dashboards so event-driven workflows remain healthy.
