# Runbook – Booting the Jane-led Agentic Workspace

This runbook spins up a Responsibility OS workspace anchored by Jane (steward persona) plus the default Marketing-led service Responsibilities:

- Website Manager
- Content Manager & Writer
- Social Media Manager
- Product Marketing Manager
- Community Manager
- Protocol Manager (engineering-driven)
- Task Worker service (automation layer)

The workspace currently relies solely on this repository + GitHub tooling; additional SaaS integrations can be layered later. All boots are manual until automation mandates are approved.

---

## 0. Pre-Flight Checklist
1. **Repo sync** – `git pull` latest `main`. Confirm `.gitignore` hides `boot_trial_logs/` and `docs/private/`.
2. **Telemetry policy** – Copy `protocol/telemetry/TELEMETRY_POLICY_TEMPLATE.yaml` to `telemetry/policies.yaml`. Jane verifies via steward mandate that Guardrails know the thresholds.
3. **Persona & Mandate review** – Ensure steward (`persona.steward_jane`), Task Worker persona/mandates, and each Marketing Responsibility’s markdown files exist (or scaffold them using the steward template).
4. **Secrets & Accounts** – Only GitHub is required. Confirm access to the repo hosting the public website (GitHub Pages) and the marketing content folders.
5. **Boot log** – Create a local `boot_trial_logs/<timestamp>/` folder to capture observations (ignored by git).

---

## 1. Global Boot (Jane + Task Worker)

### 1.1 Steward Jane
1. Run mandate `mandate.steward.bootstrap_first_cos` if this is a fresh workspace.
2. Update/confirm Jane’s BOOT_SUMMARY (Phase 1/2 of the boot template) with current rules, tool notes, and telemetry confirmation.
3. Verify telemetry policy presence and log the check in `memory/events.md`.

### 1.2 Task Worker
1. Ensure `protocol/examples/task_worker/` assets (persona, responsibility, mandates, BOOT_SUMMARY) are cloned into the workspace.
2. Execute `mandate.task_worker.task_hydration` manually:
   - Replay pending `kernel.tasks.issue` commands (if any).
   - Seed the internal `tasks/` store with placeholder Tasks for each Responsibility (needs_action).
3. Run `mandate.task_worker.task_escalation` to confirm blocked Tasks surface RFAs to Jane.
4. Record heartbeat metric via telemetry writer (status should be `ok`).

---

## 2. Responsibility Boot Steps

For each Responsibility below, follow the Responsibility Boot Template phases.

### Website Manager
- **Mission**: Keep the GitHub Pages site updated with protocol releases, runbooks, and public announcements.
- **Boot Actions**:
  1. Validate static files (`kernel.md`, `guardrails.md`, persona).
  2. Produce BOOT_SUMMARY capturing publishing cadence (e.g., weekly) and tool usage (`git`, `pages build/deploy`).
  3. Create Tasks:
     - “Publish latest progress log excerpt to website.”
     - “Review site navigation quarterly.”
  4. Verification: run `npm run build` or `pages build` locally (if applicable) and log status.

### Content Manager & Writer
- **Mission**: Author protocol updates, newsletters, and documentation posts.
- **Boot Actions**:
  1. BOOT_SUMMARY: content style guide, approval path (Jane).
  2. Tasks: “Draft monthly protocol update”, “Summarize community feedback”.
  3. Link outputs to `docs/` or `runbooks/` paths; no external CMS yet.

### Social Media Manager
- **Mission**: Prepare social-ready summaries of protocol updates.
- **Boot Actions**:
  1. Checklist for safe messaging (align with Guardrails).
  2. Tasks: “Create weekly thread for GitHub updates”, “Respond to community questions (manual)”.
  3. Since no external tooling yet, note placeholders for future Twitter/LinkedIn APIs.

### Product Marketing Manager
- **Mission**: Translate engineering milestones into go-to-market briefs.
- **Boot Actions**:
  1. BOOT_SUMMARY: link to Protocol Manager outputs, define review cycle.
  2. Tasks: “Update launch brief template”, “Coordinate with Jane on roadmap blog”.
  3. Telemetry: monitor Task completion counts weekly.

### Community Manager
- **Mission**: Moderate community channels (future Discord/Forum) and capture sentiment.
- **Boot Actions**:
  1. Record manual process (since no platform yet).
  2. Tasks: “Publish weekly community summary”, “Log support questions”.
  3. Plan future integrations (Discord bot, mailing list) but mark as context gap.

### Protocol Manager (Engineering-Driven)
- **Mission**: Maintain specs, progress log, CI (if added), and code health.
- **Boot Actions**:
  1. Ensure invariants, kernel spec, telemetry spec references in BOOT_SUMMARY.
  2. Tasks: “Review incoming spec proposals”, “Update PROGRESS_LOG after each release”.
  3. Telemetry: monitor `runtime.uptime`, code lint status (manual for now).

---

## 3. Post-Boot Verification
1. **Task queue** – `tasks/` store shows all default Tasks with `needs_action`.
2. **Telemetry** – `telemetry_metrics` (or markdown mirror) records heartbeats for Jane, Task Worker, each Responsibility (manual entries for now).
3. **Website preview** – Run local build to ensure GitHub Pages compiles.
4. **Runbook log** – Append summary to `boot_trial_logs/<timestamp>/boot_sequence.md`.

---

## 4. Operations & Cadence
- All Responsibilities run manual check-ins (daily quick scan, weekly deep review) until automation mandates exist.
- Jane reviews Task throughput weekly; any backlog triggers a RequestForAction.
- Monthly: publish protocol update via Content + Product Marketing + Website flow.
- Community reports flow back into Protocol Manager for potential spec updates.

---

## 5. Escalation / Rollback
1. If a boot step fails (e.g., Tasks not hydrating), pause the run, log the issue, and notify Jane.
2. Use `mandate.steward.system_health_check` to verify kernel/guardrails before retrying.
3. If GitHub Pages deploy fails, revert to previous commit and log incident in `memory/events.md`.

---

## 6. Future Enhancements
- Integrate marketing tools (newsletter, analytics, Stripe donations) once credentials and Guardrails are ready; extend this runbook with those boot steps.
- Automate Task Worker sweeps (cron) and telemetry exports once the infrastructure is stable.
- Publish a public-facing summary (redacting internal notes) so community members understand the governance model.
