---
layer: ops_infrastructure
change_risk: medium
---

# Responsibility Registry Specification

The registry is the canonical source of truth for which Responsibilities exist inside an installation, their lifecycle state, capability manifest, and routing metadata. It lives in the System-of-Record (SQL) but surfaces human-readable mirrors in `registry/responsibility_registry.json` and per-Responsibility portable containers under `registry/<responsibility_id>/` (see RFS v0.1).

## Registry as Index (not primary store)
- `registry/responsibility_registry.json` (and the SQL table) index Responsibilities and point to their portable containers.
- Containers are the System-of-Context for a Responsibility: `context.md`, `manifest.json`, `logs/`, `tasks/inbound`, `tasks/outbound`, `notes.md`.
- No Responsibility may write into another container without explicit authorization; SYS_HEALTH_OPS retains read-only visibility for audits.

## SQL Schema

```sql
CREATE TABLE responsibilities (
  id                TEXT PRIMARY KEY,             -- e.g., 'churn_analysis'
  workspace_id      TEXT NOT NULL,                -- logical grouping
  name              TEXT NULL,                    -- optional human-friendly name
  chief_of_staff_id TEXT NOT NULL,                -- Responsibility supervising this role
  status            TEXT NOT NULL,                -- 'draft' | 'active' | 'suspended' | 'retired'
  capability_path   TEXT NOT NULL,                -- path to manifest file in System-of-Context
  created_at        DATETIME NOT NULL,
  updated_at        DATETIME NOT NULL,
  retired_at        DATETIME NULL,
  metadata_json     TEXT NULL                     -- arbitrary tags, owners, trust tier
);
```

Optional `workspaces` table may document workspace metadata (`id`, `name`, `chief_of_staff_id`, `created_at`).

## Capability Manifest

Every Responsibility publishes a machine-readable manifest inside its portable container:

```
registry/<responsibility>/manifest.json
```

Example schema:

```json
{
  "version": 1,
  "responsibility_id": "churn_analysis",
  "intent_tags": ["churn", "retention", "cohort_analysis"],
  "mandates": ["mandate.churn.monthly_analysis", "mandate.churn.ad_hoc_deep_dive"],
  "tools": [
    {"name": "sqlite", "resource": "data/churn_analysis.db", "guardrail_clause": "data.local_use_only"},
    {"name": "plotly", "resource": "python", "guardrail_clause": "visualization.standards"}
  ],
  "dependencies": ["data_manager"],
  "model_preferences_file": "ai_context/model_preferences.md"
}
```

The manifest enables:
- Intent routing (intent tags + mandate list)
- Guardrails enforcement (tool listings reference clause IDs)
- Dependency graph (which Responsibilities this one relies on)

## Lifecycle

1. **Draft** – Responsibility added to registry with `status = 'draft'`; manifest validated but not yet routable.
2. **Active** – Kernel and Guardrails approve; intents may route to this Responsibility.
3. **Suspended** – Temporarily offline; Kernel refuses new work.
4. **Retired** – Historical only; mandate runs may be replayed but no new work scheduled.

Status transitions are executed via Kernel commands (`registry.activate(id)`, etc.) so append-only memory captures every change.

## Mirrors in System-of-Context

`responsibility.md` must include frontmatter referencing the registry row:

```yaml
---
responsibility_id: churn_analysis
registry_row: responsibilities/churn_analysis
workspace_id: rebrandly_bi
status: active
chief_of_staff_id: product_cos
capability_manifest: registry/churn_analysis/manifest.json
---
```

Human-readable sections document mission, scope, escalation points, and steward contacts. Automation verifies the manifest hash matches the path recorded in SQL.

## Registry APIs

Kernels must expose read APIs to query the registry:
- `registry.list(workspace_id)` – returns Responsibilities and status metadata.
- `registry.get(id)` – fetches single entry plus manifest hash.
- `registry.search(intent_tags, capabilities)` – used by the intent router to discover candidates.

Write operations (`add`, `update`, `suspend`, `retire`) are mediated via patch proposals or steward commands so Guardrails can enforce governance.
