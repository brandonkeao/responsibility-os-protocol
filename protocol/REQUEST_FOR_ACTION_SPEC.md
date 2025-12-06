# RequestForAction Specification

RequestForAction (RFA) entries are queued, deterministic messages that allow one Responsibility to ask another to consider work under its own Kernel and Guardrails. RFAs live simultaneously in two layers:

- **System-of-Record (SoR):** a local SQL database that enforces IDs, status transitions, timestamps, and retries. AI never mutates this layer directly; only deterministic services or humans acting through tooling may run SQL commands.
- **System-of-Context (SoC):** regenerated markdown views (e.g., `queue/inbox/<request_id>.md`) that make RFAs legible to stewards and LLMs. These files cite the SoR row and may include narrative summaries, links, and checklists.

## Canonical Schema

```sql
CREATE TABLE requests (
  id                       TEXT PRIMARY KEY,
  type                     TEXT NOT NULL DEFAULT 'request_for_action',
  origin_responsibility_id TEXT NOT NULL,
  target_responsibility_id TEXT NOT NULL,
  origin_mandate_id        TEXT NULL,
  subject                  TEXT NOT NULL,
  summary                  TEXT NOT NULL,
  body_md_path             TEXT NULL,
  payload_json             TEXT NULL,
  workspace_id             TEXT NOT NULL,
  status                   TEXT NOT NULL,
  priority                 INTEGER NOT NULL DEFAULT 100,
  sla_response_seconds     INTEGER NULL,        -- target time to accept/decline
  sla_completion_seconds   INTEGER NULL,        -- target time to finish accepted work
  acknowledged_at          DATETIME NULL,
  created_at               DATETIME NOT NULL,
  available_at             DATETIME NOT NULL,
  due_at                   DATETIME NULL,
  processed_at             DATETIME NULL,
  closed_at                DATETIME NULL,
  idempotency_key          TEXT NULL,
  attempts                 INTEGER NOT NULL DEFAULT 0,
  last_error               TEXT NULL,
  authored_by              TEXT NOT NULL,
  author_agent_id          TEXT NULL,
  source_context           TEXT NULL
);
```

Every modification is mirrored into `request_events` for auditability:

```sql
CREATE TABLE request_events (
  id               INTEGER PRIMARY KEY AUTOINCREMENT,
  request_id       TEXT NOT NULL,
  event_type       TEXT NOT NULL,
  old_status       TEXT NULL,
  new_status       TEXT NULL,
  note             TEXT NULL,
  created_at       DATETIME NOT NULL,
  created_by       TEXT NOT NULL,
  created_agent_id TEXT NULL
);
```

## State Machine

Statuses form a strict state machine so deterministic services can reason about RFAs:

```
created -> pending -> accepted -> completed
                 \-> deferred -> pending
                 \-> rejected
                 \-> cancelled
                 \-> expired
```

- **created** – row exists but not yet visible (`available_at` in the future).
- **pending** – eligible for selection by the target responsibility.
- **accepted** – target has acknowledged and likely scheduled a mandate run.
- **deferred** – temporarily parked; `available_at` must be advanced deterministically.
- **rejected** – declined with a reason linked in `request_events`.
- **cancelled** – origin retracted the request.
- **expired** – `due_at` passed without acceptance.
- **completed** – target recorded outcomes (often referencing mandate runs or reports).

Guardrails enforce that transitions follow the arrows above and that the actor performing the change is authorized.

## SLA Monitoring

- `sla_response_seconds` tracks the expected time to move a request out of `pending`. Kernels should populate `acknowledged_at` when the target first touches the request and emit an alert if the SLA is breached.
- `sla_completion_seconds` specifies how long the target has after acceptance. When exceeded, Guardrails may escalate or auto-reassign responsibility.
- Steward dashboards should expose queue depth, average response/completion time, and breach counts to keep the ecosystem healthy.

## Selection & Locking

Deterministic services claim work with the following canonical query:

```sql
SELECT *
FROM requests
WHERE target_responsibility_id = :target
  AND workspace_id = :workspace_id
  AND status = 'pending'
  AND available_at <= :now
ORDER BY priority ASC, created_at ASC
LIMIT :batch_size;
```

**Workspace Isolation Enforcement:** The query MUST include `workspace_id` to enforce Invariant 10 (Workspace Isolation). This prevents cross-workspace RFA leakage when Responsibilities share identical IDs across different workspaces. Kernels must pass the current workspace context when invoking this query.

AI may read the markdown mirror of the results but must never alter status fields. Any acceptance, deferral, or rejection must be executed by a kernel-owned command that writes to SQL and appends a memory event.

## Markdown View Contract

For each SoR row, tooling may materialize `queue/inbox/<request_id>.md` (target view) or `queue/outbox/<request_id>.md` (origin view) using frontmatter:

```md
---
type: request_for_action
request_id: req_2025-11-28T09-15Z_finance_to_parenting_allowance
db_source: local_sql
status: pending
origin_responsibility_id: finance_cos
target_responsibility_id: parenting_cos
origin_mandate_id: finance_cos.monthly_budget_review
priority: 100
authored_by: ai
author_agent_id: finance_cos
created_at: 2025-11-28T09:15:00Z
available_at: 2025-11-28T09:15:00Z
due_at: 2025-11-30T23:59:59Z
source_context: mandate_run:finance_cos.monthly_budget_review@2025-11-28T09:00Z
workspace_id: dad_mode
---
```

The markdown body should summarize the intent, suggested actions, and provide links back to reports, mandate runs, or context files. Since these files are views, they can be regenerated from SQL at any moment, preventing drift between SoR and SoC.

## Lifecycle Responsibilities

- **Origin Responsibility** – creates the RFA, references the originating mandate run, and monitors outbound status.
- **Target Responsibility** – reviews the inbox, mirrors accepted RFAs into mandate runs, and logs outcomes.
- **Kernel Services** – mediate all status transitions, ensuring Guardrails review every change.
- **AI Assistants** – narrate summaries, propose responses, and draft follow-up mandates but never mutate SQL rows directly.

## Relationship to Mandates

An accepted RequestForAction does **not** transfer authority. It simply asks the target Responsibility to consider creating or running its own mandate. The target may:

1. Accept and spawn one or more mandate runs.
2. Defer until preconditions are met.
3. Reject with rationale, appending the decision to both memory and `request_events`.
4. Expire/cancel based on deterministic policies.

This separation keeps governance clear: mandates remain internal authority, RFAs manage cross-responsibility collaboration, and both layers stay auditable.

## Workspace Scope & New RFA Types
- Every RFA row now records `workspace_id`. Kernels and Guardrails must enforce isolation: RFAs may only reference Responsibilities registered to the same workspace, and markdown mirrors must display the workspace identifier.
- Steward responsibilities (Jane@workspace) act as the ingestion and routing authority for workspace context. To support this, two new types augment the `type` field:

### `ingest_new_context`
Used when CLI tools or automations propose a new AI Context Bundle for steward validation.

**Required Fields**
- `type: ingest_new_context`
- `origin_responsibility_id`: producer (CLI, automation)
- `target_responsibility_id`: steward (e.g., `jane@dadmode`)
- `workspace_id`
- `payload_json.bundle_ids`: array of bundle identifiers
- `payload_json.objectives`: list or text describing why the bundle matters

**Optional Fields**
- `payload_json.user_hints.suggested_responsibilities`
- `payload_json.tags`

Upon acceptance, the steward must normalize the artifact, update lineage, and dispatch downstream RFAs.

### `new_context_available`
Used by the steward to notify Responsibilities that vetted context bundles exist.

**Required Fields**
- `type: new_context_available`
- `origin_responsibility_id`: steward
- `target_responsibility_id`: impacted responsibility
- `workspace_id`
- `payload_json.bundle_ids`
- `payload_json.objectives`

Receiving Responsibilities should:
1. Review the bundle(s) and update their memory/context files.
2. Respond with relevance (`ack_context_relevant`, `not_relevant`) or issue follow-up RFAs/Tasks as needed.

Guardrails verify that only steward personas can originate `new_context_available` RFAs and that every `ingest_new_context` request transitions through steward review before downstream dispatch.

> **RFA vs Task Separation:** RFAs always mediate cross-responsibility coordination at the workspace boundary. Once a Responsibility accepts the ask, it materializes its own Tasks internally; Tasks must never be used as substitutes for RFAs when collaboration or ingestion responsibilities span multiple Responsibilities.
