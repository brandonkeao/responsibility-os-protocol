# Responsibility Filesystem Standard v0.1 (RFS)

RFS defines how each Responsibility organizes markdown, JSON, and log artifacts so that humans, AI assistants, and deterministic services share the same context. It complements the SQL System-of-Record by treating the filesystem as the **System-of-Context**.

## Guiding Principles
- **Mirrored Layers** – SQL stores truth (requests, status, registry). Markdown/JSON store meaning (mandates, reports, views).
- **Append-Only by Default** – Historical artifacts live forever; new insights appear as new files or sections with timestamps.
- **Explicit Authorship** – Every file includes provenance frontmatter identifying the actor, capability, and source event.
- **AI-Friendly Bundles** – Critical summaries live inside `ai_context/` so LLM calls can stay small and deliberate.

## Canonical Layout

```
<workspace>/<responsibility_id>/
  kernel.md
  guardrails.md
  persona.md

  mandates/
    definitions/
      <mandate>.md
    runs/
      <mandate>/
        <ISO8601>.md

  requests/
    inbox/
      <request_id>.md   # generated view from SQL
    outbox/
      <request_id>.md

  context/
    projects/*.md
    knowledge/*.md

  reports/
    <YYYY-MM-DD>_*.md

  meetings/
    summaries/
      <YYYY-MM-DD>_<title>.md
    transcripts/
      <YYYY-MM-DD>_<title>.md (raw log, referenced by summaries only)

  memory/
    events.md
    insights.md

  ui/
    views/*.json
    diagrams/*.mermaid

  ai_context/
    system_context.md
    current_focus.md
    recent_activity.md
    open_requests.md
    model_preferences.md

  logs/
    events_<YYYY-MM>.ndjson

  proposals/
    <timestamp>_update_<target>.md

  scratch/
    *.md
```

Responsibilities may add folders, but they must not remove or repurpose the namespaces above.

## Frontmatter Contract

All markdown files include:

```yaml
---
authored_by: human | ai | hybrid
author_id: steward | cos_parenting | user:<id>
created_at: 2025-11-28T07:10:00Z
updated_at: 2025-11-28T07:15:00Z
source: mandate_run:parenting_cos.morning_routine@2025-11-28T07:00Z
context_role: kernel | guardrail | persona | mandate_definition | mandate_run |
              request | long_term_memory | short_term_memory | report |
              ui_view | log | scratch
---
```

This metadata lets AI filter relevant files and enables deterministic tooling to verify provenance.

## Patch Proposal System

Sensitive artifacts (`kernel.md`, `guardrails.md`, `persona.md`, and `mandates/definitions/*`) must be changed via reviewable proposals:

```
proposals/
  2025-11-28T10-00Z_update_persona_parenting_cos.md
```

```md
---
type: patch_proposal
target_file: persona.md
authored_by: ai
status: pending       # pending | applied | rejected
---

## Rationale
Explain why the change is needed.

## Proposed Diff
```diff
- Old line
+ New line
```
```

A steward Responsibility applies or rejects proposals, logging the result to `memory/events.md`.

## Queue Views

The `requests/` folder mirrors the SQL queue. Files are generated, not hand-authored, and may be safely regenerated at any time. Each file must cite `request_id` and `db_source` in frontmatter so consumers know how to fetch the authoritative record.

## Reports and Memory

- `reports/` contain structured reflections (weekly reviews, retros, audits).
- `memory/events.md` captures chronological append-only notes.
- `memory/insights.md` contains distilled learnings that survive resets.
- `meetings/summaries/` stores bullet summaries with metadata (`title`, `date`, `attendees`, `responsibilities_interested`) plus pointers to the raw transcript file.
- `meetings/transcripts/` stores the unchunked meeting log (audio-to-text, chat export, etc.). Transcripts are indexed but not broken into arbitrary AI context chunks; instead, summaries reference them and future RAG tooling can re-assess applicability for new Responsibilities.
- When a new Responsibility joins the workspace, stewards can either review the summaries to identify relevant sessions or run a targeted, potentially expensive, RAG pass across transcripts to discover additional matches.

AI assistants should ingest reports first, then memory, before editing mandates or writing new plans.

## UI Definitions

`ui/views/*.json` define how future graphical interfaces should render the Responsibility state. Each view lists source files so revisions are transparent. `ui/diagrams/*.mermaid` stores graph definitions that can be rendered into SVG or ASCII.

## Scratch Space

`scratch/` is intentionally noisy and may be purged. No other folder should contain speculative drafts.

By adhering to RFS v0.1 every Responsibility becomes portable: cloning a folder restores both the semantic context that AI needs and the deterministic hooks that systems use to keep SQL, markdown, and humans in sync.

## Model Preference Declarations

Every Responsibility must declare the preferred AI model(s) inside `ai_context/model_preferences.md`. The file describes:

- Primary model (e.g., `gpt-4o`, `sonnet-3.5`).
- Approved fallbacks.
- Capabilities or mandates that require a specific model family.
- The currently detected model (reported by the AI runtime or orchestration layer).
- Required action if the detected model does not match the preference (auto-switch if tooling allows, otherwise notify the user/steward).

Context workers update this file whenever policies change or when a mismatch is detected, ensuring stewards see drift between intended and actual execution environments.
