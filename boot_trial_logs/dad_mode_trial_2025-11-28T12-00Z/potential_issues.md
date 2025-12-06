# Potential Issues & Simplification Targets – `dad_mode_trial_2025-11-28T12-00Z`

---
run_id: dad_mode_trial_2025-11-28T12-00Z
authored_by: ai
context_role: boot_trial_risk_log
created_at: 2025-11-28T12:05:00Z
---

## 1. Protocol Surface Area (Bloat Risk)
- **Observation**: Boot lifecycle now references Mandates, RFAs, Tasks, AI context bundles, Boot Summaries, telemetry metrics, and Google Workspace sync artifacts. Each adds value but stacks layers that new stewards must learn before touching real data.
- **Simplification Idea**: Collapse Boot + Task hydration instructions into a single “Responsibility Startup Checklist” doc that links out to specs instead of duplicating requirements in every spec. We can keep the canonical schemas but move sequencing guidance into one place.
- **Open Question**: Do we really need both BOOT\_SUMMARY and AI context bundles for Dad Mode, or can the context worker derive BOOT\_SUMMARY from the bundle during boot to avoid two sources of “current rules”?

## 2. Task vs Request Redundancy
- **Observation**: Tasks now sit between Mandates and Responsibilities, while RFAs already capture cross-responsibility asks. Without guardrails, Responsibilities may end up mirroring the same work item in both places (RFA + Task). Kernel needs a deterministic rule to prevent duplicates.
- **Simplification Idea**: Require each Task to cite either `request_id` or `mandate_run_id` (already recommended) and expose a single `kernel.work_item_ref` abstraction so downstream tooling (dashboards, telemetry) doesn’t have to branch on Task vs RFA.
- **Action Needed**: Decide whether cross-responsibility work ALWAYS starts via RFA with optional Task projection, or whether Tasks may exist independently. Document that choice in the Task spec before real Dad Mode data arrives.

## 3. Telemetry Threshold Ambiguity
- **Observation**: Telemetry spec defines metric schemas but not threshold defaults. During boot we had to mark the Google Workspace cost metric as `warning` with no numeric rule.
- **Simplification Idea**: Provide a starter `telemetry/policies.yaml` template with suggested thresholds (heartbeat interval, cost per day, queue latency). Responsibilities can override it, but at least the boot process won’t stall while humans invent numbers.

## 4. Boot Summary Ownership
- **Observation**: BOOT\_SUMMARY is described as overriding raw files, yet it is unclear who updates it when context changes (persona vs steward vs automation). Automatic generation during boot may drift if humans edit manual rules later.
- **Simplification Idea**: Treat BOOT\_SUMMARY as an artifact owned by the steward persona and regenerated via a Kernel command, similar to context bundles. That keeps one path for updates and automatically logs deltas to memory.

## 5. Google Workspace Dependencies
- **Observation**: Dad Mode boot assumes `google_workspace_mcp` is available for Tasks + Calendar. If a user doesn’t grant Google access yet, the Task Worker currently logs warnings but no fallback exists.
- **Simplification Idea**: Gate Task boot on capability availability: if Google tokens are missing, create a `task_sync.blocked` state instead of simulating partial sync. Alternatively, allow a “local-only” Task renderer until integrations are approved.

## 6. Multi-Hop Fixture Gap
- **Observation**: The protocol still lacks an end-to-end Mandate → RFA → Task example. Without it we can’t prove the new Task layer behaves with existing specs.
- **Action**: Keep this on the to-do list for the next Dad Mode iteration; no code change now, but note that real data testing should wait until we have at least one vetted fixture.

## 7. Simplify Docs for Operators
- **Observation**: Operators now have to read `PROTOCOL_BOOTSTRAP_V1`, the boot template, the Task spec, telemetry spec, and AI context bundle spec just to run boot.
- **Simplification Idea**: Produce a concise “Dad Mode Boot Runbook” that references each canonical spec but narrates the actual steps (checklist, commands, expected outputs). This prevents drift while still respecting canonical docs.

These issues should be resolved before we point the protocol at live Dad Mode data to prevent confusion, duplicate work items, or mismatched telemetry alarms.
