
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
└── protocol/
    ├── specs/
    │   └── v1/
    │       ├── 00_overview.md
    │       ├── 01_invariants.md
    │       ├── 02_responsibility.md
    │       ├── 03_kernel.md
    │       ├── 04_guardrails.md
    │       ├── 05_persona.md
    │       ├── 06_charge.md
    │       ├── 07_agent.md
    │       ├── 08_memory.md
    │       └── 09_ui_translation.md
    ├── examples/
    │   └── steward/
    ├── progress/
    │   └── PROGRESS_LOG.md
    └── README.md
```

---

## Steward Objects to Generate

Under `protocol/examples/steward/` Codex must create:

- `steward_responsibility.md` → `responsibility.steward`
- `steward_kernel.md` → `kernel.steward`
- `steward_guardrails.md` → `guardrails.steward`
- `steward_persona.md` → `persona.steward_brandon_host`
- `charge_welcome_user.md` → `charge.steward.welcome_user`
- `charge_system_health.md` → `charge.steward.system_health_check`
- `charge_bootstrap_first_cos.md` → `charge.steward.bootstrap_first_cos`

These define the canonical System Steward.

---

## Rules Codex Must Follow (Protocol Repo)

1. Never skip Kernel or Guardrails references in specs.
2. Steward example must not reference any personal or domain-specific data.
3. Memory is always specified as **append-only** in specs.
4. No `workspaces/` folder is allowed in this repo.
5. No app code or UI code is allowed in this repo.

---

## Completion Signal

When done, Codex must output:

1. A tree view of `responsibility-os-protocol/`
2. A short validation note confirming:
   - All spec files exist under `protocol/specs/v1/`
   - Steward example files exist
   - No `workspaces/` directory was created

End of Protocol Bootstrap.
