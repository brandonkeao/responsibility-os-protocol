# Data Lineage and Artifact Specification

To make recommendations auditable, every Responsibility must record how inputs transform into outputs. The lineage system complements append-only memory by focusing on data artifacts.

## Tables

```sql
CREATE TABLE data_artifacts (
  id             TEXT PRIMARY KEY,
  responsibility_id TEXT NOT NULL,
  artifact_type  TEXT NOT NULL,      -- 'dataset' | 'visualization' | 'report' | 'model'
  uri            TEXT NOT NULL,      -- path in filesystem or external URL
  created_at     DATETIME NOT NULL,
  source_type    TEXT NOT NULL,      -- 'event' | 'mandate_run' | 'request' | 'manual'
  source_id      TEXT NOT NULL,      -- e.g., mandate run ID
  metadata_json  TEXT NULL
);

CREATE TABLE transformations (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  responsibility_id TEXT NOT NULL,
  input_artifact_id  TEXT NOT NULL,
  output_artifact_id TEXT NOT NULL,
  tool_name       TEXT NOT NULL,
  guardrail_clause TEXT NOT NULL,
  created_at     DATETIME NOT NULL
);
```

## Filesystem Mirrors

Each Responsibility may maintain `artifacts/index.md` summarizing key artifacts with frontmatter linking to the SQL IDs. Visualizations and reports should reference their artifact IDs in frontmatter for easy lookup.

Example frontmatter in a report:
```yaml
---
artifact_id: art_churn_q4_report
inputs:
  - art_churn_dataset_q4
  - art_payment_failure_chart
kernel_decisions:
  - kdec_12345
---
```

## Kernel API
- `lineage.register_artifact(info)` – records new artifact and returns ID.
- `lineage.link(input_ids, output_id, tool_name)` – records transformation edges.
- `lineage.trace(artifact_id)` – returns DAG of upstream/downstream artifacts for stewardship review.

## Guardrails
- Guardrails clauses should reference artifact classes (e.g., `data.export_requires_redaction`) so lineage helps verify compliance.
- When a mandate uses an artifact, Kernel can ensure the artifact’s guardrail clause matches the mandate’s permissions.

## Usage Patterns
- **Report regeneration** – trace artifacts to re-run analyses using original inputs.
- **Audit** – demonstrate which data and tools produced a recommendation.
- **Cleanup** – identify obsolete artifacts when downstream outputs retire.

Lineage metadata belongs to the System-of-Record but the System-of-Context should reference artifact IDs so humans and AI can narrate provenance succinctly.
