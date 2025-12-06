
# Responsibility OS – Protocol Bootstrap for Codex
Version: v1.0
Status: Active

---

## Purpose

Deploy the **Responsibility OS Protocol v1** as a clean, open-source–ready repository
with:

- Core specs
- Steward example
- Progress log

No product workspaces, no app code, no personal data.

---

## Target Repository Structure

Codex must create this structure:

```text
responsibility-os-protocol/
├── PROTOCOL_BOOTSTRAP_V1.md
├── README.md
├── docs/
│   ├── README.md
│   ├── protocol_gap_analysis.md
│   ├── protocol_object_evolution.md
│   ├── protocol_update_2025-11-27.md
│   ├── dad_mode_ecosystem_learnings.md
│   └── synapse_learnings_protocol_vs_app.md
└── protocol/
    ├── README.md
    ├── specs/
    │   └── v1/
    │       ├── 00_overview.md
    │       ├── 01_invariants.md
    │       ├── 02_responsibility.md
    │       ├── 03_kernel.md
    │       ├── 04_guardrails.md
    │       ├── 05_persona.md
    │       ├── 06_mandate.md
    │       ├── 07_agent.md
    │       ├── 08_memory.md
    │       └── 09_ui_translation.md
    ├── AI_CONTEXT_BUNDLES.md
    ├── RESPONSIBILITY_FILESYSTEM_STANDARD_V0_1.md
    ├── REQUEST_FOR_ACTION_SPEC.md
    ├── RESPONSIBILITY_REGISTRY_SPEC.md
    ├── INTENT_ROUTER_SPEC.md
    ├── EVENT_TRIGGER_SPEC.md
    ├── DATA_LINEAGE_SPEC.md
    ├── TELEMETRY_SPEC.md
    ├── examples/
    │   ├── steward/
    │   └── task_worker/
    ├── progress/
    │   └── PROGRESS_LOG.md
```

---

## Steward Objects to Generate

Under `protocol/examples/steward/` Codex must create:

- `steward_responsibility.md` → `responsibility.steward`
- `steward_kernel.md` → `kernel.steward`
- `steward_guardrails.md` → `guardrails.steward`
- `steward_persona.md` → `persona.steward_jane`
- `mandate_welcome_user.md` → `mandate.steward.welcome_user`
- `mandate_system_health_check.md` → `mandate.steward.system_health_check`
- `mandate_bootstrap_first_cos.md` → `mandate.steward.bootstrap_first_cos`
- `request_allowance_plan.md` → sample RequestForAction mirror proving deterministic queue views.

These define the canonical System Steward and demonstrate mandate + RequestForAction alignment.

---

## Rules Codex Must Follow (Protocol Repo)

1. Never skip Kernel or Guardrails references in specs or steward artifacts.
2. Steward examples must not reference any personal or domain-specific data; keep personas abstract and domain-neutral.
3. Memory is always specified as **append-only** across specs, steward artifacts, and examples.
4. Maintain a clean split between the SQL **System-of-Record** (RFAs, registry, events) and the markdown **System-of-Context** mirrors. Files like `requests/inbox/*.md` are regenerated views only.
5. Follow Responsibility Filesystem Standard v0.1 for folder layout, provenance frontmatter, and patch proposal workflow.
6. No `workspaces/` folder is allowed in this repo.
7. No app code or UI implementation code is allowed in this repo (UI translation specs live as markdown only).

---

## Completion Signal

When done, Codex must output:

1. A tree view of `responsibility-os-protocol/`
2. A short validation note confirming:
   - All spec files exist under `protocol/specs/v1/`
   - Steward example files exist
   - No `workspaces/` directory was created

End of Protocol Bootstrap.
