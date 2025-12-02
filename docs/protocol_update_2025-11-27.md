# Protocol Update – 2025-11-27

This note summarizes the Responsibility OS protocol refresh driven by the v1.1 context + execution evolution design.

## Mandates & Requests
- Replaced legacy "charge" terminology with **Mandate** throughout specs and steward examples (`protocol/specs/v1/06_mandate.md`, steward mandate examples).
- Introduced **RequestForAction** as a deterministic, SQL-backed queue object (`protocol/REQUEST_FOR_ACTION_SPEC.md`). Added invariants covering System-of-Record (SoR) vs System-of-Context (SoC) responsibilities.
- Kernel spec now references mandate intake, request bridging, and deterministic claim APIs; Guardrails enforce the request state machine.

## Responsibility Filesystem & AI Context Bundles
- Authored **RFS v0.1** (`protocol/RESPONSIBILITY_FILESYSTEM_STANDARD_V0_1.md`) describing canonical folders (mandates, context, meetings, ai_context, proposals, etc.), frontmatter requirements, patch proposals, and queue mirrors.
- Added **AI Context Bundles** spec (`protocol/AI_CONTEXT_BUNDLES.md`) defining system/current_focus/recent_activity/open_requests/model_preferences files, the Context Worker mandates, and model drift alerts.
- Context bundle guidance now includes model preference declarations and detection/remediation rules.

## Steward & Persona Updates
- Steward persona was renamed to **Stewart** and persona spec gained an optional human-readable name field.
- Steward examples now include mandate files plus a sample RequestForAction view (`protocol/examples/steward/request_allowance_plan.md`).

## Progress Log & Docs
- `protocol/progress/PROGRESS_LOG.md` records the v1.1 introduction of mandates, RFAs, RFS, and AI context bundles.
- `docs/protocol_object_evolution.md` was expanded with embedded research from `ai_activity`, including ASCII diagrams and stage-by-stage evolution guidance.

Use this document as a quick reference when reviewing the 2025-11-27 protocol changes or preparing migration steps for downstream repos.
