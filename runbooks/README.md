# Runbook Bootstrap Guide

Use this guide any time you want to stand up a fresh local workspace and apply one of the Responsibility OS runbooks (Dad Mode, marketing, ops, etc.). The goal is to make the startup process deterministic and repeatable.

---

## 1. Create a Workspace Folder
1. Pick a location on disk, e.g. `~/repos/workspace-os-<team>`, and keep the protocol repo as a clean sibling to your live instance: `workspace-os-<team>/responsibility-os-protocol` plus `workspace-os-<team>/<instance_id>` (e.g., `protocol_marketing_os`).
2. Initialize the canonical folder structure inside the instance, as described in `protocol/RESPONSIBILITY_FILESYSTEM_STANDARD_V0_1.md`:
   - `persona.md`, `guardrails.md`, `mandates/definitions/`, `tasks/index.json`, `memory/events.md`, `queue/`, `ai_context/`, `telemetry/`, `BOOT_SUMMARY.latest.json` placeholder, etc.
   - Seed `tasks/index.json` with `needs_action` placeholders aligned to mandate scope so Task hydration has deterministic targets.
   - Copy templates from `protocol/examples/` (steward persona, guardrails, mandates) and `protocol/telemetry/TELEMETRY_POLICY_TEMPLATE.yaml` → `telemetry/policies.yaml` (or `policies.<responsibility>.yaml`) and ensure `telemetry/heartbeats/` exists for boot heartbeats.
3. Add a `boot_trial_logs/` folder with no files yet—runbooks will drop logs there after execution and it should stay gitignored inside the instance.

## 2. Make a Runbook Boot Request
When you are ready to boot, create a lightweight request file so the action is auditable:

```
boot_requests/<timestamp>_<workspace>_<runbook>.md
```

Example frontmatter:
```md
---
workspace: protocol_marketing
runbook: runbooks/dad_mode_boot_runbook.md
requester: human:brandon
created_at: 2025-12-06T17:25:00Z
---
Intent: Boot Protocol Marketing workspace using the Dad Mode runbook to validate telemetry + ingestion flows.
```

If you collaborate with other operators, share this request (issue, chat, etc.) so everyone knows which runbook is in use.

## 3. Execute the Runbook & Checklist
1. Follow the selected runbook line-by-line. Each runbook references the canonical startup checklist in `protocol/RESPONSIBILITY_STARTUP_CHECKLIST.md`.
2. Record outputs as you go (telemetry hashes, kernel logs, OAuth checks, etc.).
3. When the run finishes, save two artifacts under `boot_trial_logs/<workspace>_<timestamp>/`:
   - `boot_sequence.md` – ordered notes from the boot (phases, commands, evidence links).
   - `workspace_signoff.md` (or `<workspace>_signoff.md`) – detailed phase-by-phase log.
   - `potential_issues.md` – gaps, follow-ups, and improvement ideas for Jane’s protocol-improvement loop.

## 4. Generate an Onboarding Guide
After the initial boot succeeds, add a human-readable onboarding note so others can reuse the setup:

```
onboarding/<workspace>_runbook_guide.md
```

Include:
- Runbook used + commit hash of the protocol repo.
- Where logs live (`boot_trial_logs/...`).
- How to re-run the checklist.
- Any custom telemetry overrides or OAuth requirements.

This guide becomes the “front door” for anyone inheriting the workspace.

---

### Log User Inputs per Responsibility
- Append user/operator inputs as timestamped bullets in each Responsibility’s `memory/events.md` (append-only). Include source and references so stewardship is auditable:
  - `- 2025-12-06T17:25:00Z user_input (source: human:brandon, mandate: stewardship.ops_intake, task: task-123) – Requested weekly digest on risk items; capture in RFA if blocked.`
- If you build automation, provide a simple `log_user_input` helper or template to keep these entries consistent across Responsibilities.

Following these steps keeps every runbook-driven workspace consistent: you know how it was created, which runbook governed the boot, and where to look for signoff logs, issues, and onboarding instructions. Feel free to adapt the templates above, but always capture the three phases (folder scaffold, runbook request, boot outputs) so future operators can audit the process.
