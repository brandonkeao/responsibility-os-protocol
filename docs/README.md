# Responsibility OS Docs

This directory hosts research summaries, architectural notes, and operator guides that extend the core `protocol/` specs. Every document should stay implementation-neutral while explaining how protocol objects evolve to meet new use cases.

## Contents
- `protocol_object_evolution.md` – outlines how Kernel, Guardrails, charges, personas, agents, and memory grow from foundational patterns into complex deployments.
- `agentic_os_tasks_protocol_update.md` – details the Mandate → Task → Responsibility rollout plus the Google Workspace MCP sync and safety rules.
- `agentic_os_protocol_tdd.md` – comprehensive protocol technical design (public) covering Kernel/Guardrails, mandates, Tasks, and Task Worker integration.
- Runbook operations live at the repo root. Start with `runbooks/README.md` to learn the standard boot request + logging loop, then apply the specific runbook (`runbooks/dad_mode_boot_runbook.md`, etc.) when bringing an environment online.
- More briefs can be added as the community publishes research or field reports.

Documents in this folder are version-controlled and scoped for public sharing.
