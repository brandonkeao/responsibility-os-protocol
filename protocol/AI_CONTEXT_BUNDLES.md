# AI Context Bundles

AI Context Bundles are curated summaries that keep LLM calls efficient while preserving alignment with Kernel + Guardrails decisions. Instead of loading entire Responsibility folders, agents read a small bundle of markdown files maintained by a dedicated Context Worker.

## Bundle Contents per Responsibility

1. **`ai_context/system_context.md`** – distilled description of the kernel, guardrails, persona voice, and long-lived mandates. Includes links to canonical files.
2. **`ai_context/current_focus.md`** – rolling summary of active projects, current objectives, and near-term checkpoints.
3. **`ai_context/recent_activity.md`** – last N significant events (mandate runs, request decisions, reports) with timestamps and memory pointers.
4. **`ai_context/open_requests.md`** – prioritized list of pending RequestForAction items pulled from the SQL queue with backlinks to markdown views.
5. **`ai_context/model_preferences.md`** – preferred model stack, approved fallbacks, current detected model, and remediation instructions if there is drift.
6. **Optional add-ons** – specialized snippets such as `risk_register.md`, `experiments.md`, or `cadence.md` when a Responsibility requires bespoke prompts.

Each file observes the RFS frontmatter contract so provenance is explicit.

## Bundle Metadata
Every bundle (regardless of Responsibility) must expose structured metadata alongside the content files so stewards can automate routing:

```yaml
origin: workspace_ingestion | user_cli | system_derived
primary_responsibilities:
  - parenting_cos
suggested_responsibilities:
  - finance_cos
scope: household_budgeting
bundle_ids:
  - bundle_2025-12-06-allowance-plan
ingestion_status: pending | registered | dispatched | retired
```

- `origin` identifies who initiated the bundle.
- `primary_responsibilities` are the steward’s authoritative routing targets.
- `suggested_responsibilities` capture hints supplied by users/CLI.
- `scope` summarizes the thematic boundary.
- `ingestion_status` tracks Jane’s workflow. She alone transitions the state in order: `pending` → `registered` → `dispatched` → `retired`.

## Context Worker Responsibility

A dedicated Responsibility (e.g., `context_curator`) owns mandates such as:

- `refresh_ai_context(responsibility_id)` – rebuilds the four core files from SQL + recent markdown sources.
- `compact_memory_events(responsibility_id)` – condenses `memory/events.md` into `memory/insights.md` and updates `recent_activity.md` with summaries.
- `update_open_requests(responsibility_id)` – queries the SQL queue, regenerates `open_requests.md`, and optionally emits alerts if SLAs are at risk.
- `check_model_preferences(responsibility_id)` – verifies the runtime model against `model_preferences.md`, attempts to switch via available orchestration controls, and if unsuccessful appends a notification instructing the user which model should be used.

The worker executes on schedules (hourly/daily) and on events (mandate run completed, request status changed). Outputs are append-only (new sections with timestamps) or wholesale refreshes when the file is explicitly marked as such.

## Model Preference Schema

`ai_context/model_preferences.md` must include the structured fields below so orchestration layers and Guardrails can enforce model policy consistently:

```yaml
---
preferred_model: gpt-4o
fallback_models:
  - gpt-4o-mini
  - sonnet-3.5
capability_overrides:
  - mandate: mandate.parenting.allowance_design
    required_model: gpt-4o
last_detected_model: gpt-4o-mini
enforcement_mode: enforce   # enforce | monitor
action_required: notify_parenting_cos
last_checked_at: 2025-11-28T10:05:00Z
guardrail_clause: runtime.model_integrity
---
```

Context workers must update `last_checked_at` during every refresh, set `last_detected_model` based on telemetry, and follow `action_required` when a mismatch occurs (e.g., trigger an auto-switch or notify a steward). When drift is detected they also append a note to `ai_context/recent_activity.md` referencing the same timestamp so auditors can correlate actions.

## Context Ingestion Flows

### Flow 1 – Workspace Drop (Steward-Driven)
1. A user drops a file or data asset into the shared workspace location.
2. Jane (workspace steward) is notified via deterministic watcher.
3. Jane creates lineage entries, assembles an AI Context Bundle with metadata above, and sets `ingestion_status=pending`.
4. After review, Jane registers the bundle, dispatches `new_context_available` RFAs to relevant Responsibilities, and updates `ingestion_status=dispatched`.

### Flow 2 – CLI / Tool-Assisted Ingestion
1. CLI or automation prepares a bundle (including metadata, scope, suggested Responsibilities).
2. CLI **must** issue an `ingest_new_context` RFA to Jane with bundle IDs/objectives.
3. Jane validates the payload, registers the bundle, and issues downstream `new_context_available` RFAs.

Both flows record telemetry events (`context_ingested`, `context_dispatched`) and append memory entries referencing bundle IDs and RFAs so auditors can reconstruct routing decisions.

## Usage Rules

- **Primary Context Pack** – All AI calls that act on a Responsibility should default to loading the four core files plus any files referenced within them. Deep dives can fetch additional reports or mandate runs by following those links. 
- **Model Drift Alerts** – If the detected runtime model differs from the preferred model, the bundle must note the mismatch in `model_preferences.md` and in `recent_activity.md`, indicating whether the system switched automatically or notified the user.
- **No SQL Writes** – Context bundles never mutate the queue or registry. They are semantic reflections of deterministic state.
- **Evaluation Hooks** – Guardrails may require the context worker to log hashes of each bundle refresh inside `memory/events.md` for future audits.
- **Regeneration Triggers** – Whenever a mandate run closes or a RequestForAction changes state, the kernel signals the context worker to refresh `recent_activity.md` and `open_requests.md` before the next AI session.

By standardizing bundles, Responsibility OS keeps LLM usage predictable: AI consumes concise, curated context while deterministic services own truth, leading to faster responses, lower cost, and safer autonomy.

## Context Hygiene Guardrails
- **Volume thresholds** – Track total context volume per Responsibility. Green: <2,500 lines; Yellow: 2,500–3,000 (monitor); Red: >3,000 requires consolidation before adding more. Critical workflows should retain >10% prominence of the total bundle.
- **Prominence protection** – Do not bury operational workflows under verification or meta-docs. Prefer consolidation (e.g., append verification as a final phase in the primary workflow) and add “When to use this workflow” triggers.
- **Pre-change check** – If a change adds >10% to total context volume, require an explicit Guardrails check or steward approval and consider consolidation first.
- **Telemetry hook** – Emit a `context_volume` metric during bundle refresh; Guardrails may block bundle publication if thresholds are exceeded without an override.

## Context Packs and Synthesis
- Context Packs under `context/packs/` are curated inputs to bundles. They must not be concatenated directly into prompts; the context worker or planner selects relevant pack files and synthesizes them into a Unified Task Brief (UTB).
- **Unified Task Brief (UTB)**: 500–1,200 tokens that states the task goal once, distills the top principles, normalizes style to the steward persona/Golden Identity Prompt, and inlines only necessary structures/constraints. UTB is the only pack-derived content admitted to the execution prompt.
- **Golden Identity Prompt**: A human-authored anchor (see Guardrails) that holds mission/optimization/decision style/ethics/voice/failure modes. UTB must respect it; persona + guardrails remain authoritative for safety.
- **Density warnings**: When estimated UTB + pack-derived content exceeds 2,000–3,500 tokens, emit a warning (not a block), log to telemetry, and require operator confirmation for overrides.
