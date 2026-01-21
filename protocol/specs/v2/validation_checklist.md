# Entity Validation Checklist

**Version**: 1.3
**Derived From**: ENTITY_SPEC.md v1.8
**Purpose**: Systematic validation of entities against specification

---

## Quick Reference

| Tier | Required Items | Use Case |
|------|----------------|----------|
| **Tier 1** | 8 items | Minimal viable entity - identity and objectives |
| **Tier 2** | 38 items | Full entity - memory, inbox, skills |
| **Role-Specific** | 4-5 items | Based on Orchestrator/Domain Specialist/Meta-Entity |
| **Optional** | 11 items | Nice-to-have, not required |

**New users**: Start with Tier 1. Upgrade to Tier 2 when you need memory persistence and skills.

---

## How to Use This Checklist

1. **Determine your tier**: Tier 1 (minimal) or Tier 2 (full)
2. **Run required checks** for your tier
3. **Run role-specific checks** if applicable
4. **Record status**: PASS / WARN / FAIL
5. **Prioritize fixes**: CRITICAL → MEDIUM → LOW

### Severity Definitions

| Severity | Impact | Timeline |
|----------|--------|----------|
| **CRITICAL** | Blocks core functionality | Immediate |
| **MEDIUM** | Degrades functionality | Within 2-3 sessions |
| **LOW** | Minor deviation | When convenient |

---

## Tier 1 Required (8 items)

**Minimum viable entity** - These are required for basic entity functionality.

### Core Files

| # | Check | Severity |
|---|-------|----------|
| T1-1 | `CLAUDE.md` exists at workspace root | CRITICAL |
| T1-2 | `context/kernel/role_definition.md` exists | CRITICAL |
| T1-3 | `active_work/current_objectives.md` exists | CRITICAL |

### Identity Verification

| # | Check | Severity |
|---|-------|----------|
| T1-4 | CLAUDE.md contains boot sequence instructions | CRITICAL |
| T1-5 | CLAUDE.md references correct kernel file paths | CRITICAL |
| T1-6 | role_definition.md defines entity identity | CRITICAL |
| T1-7 | role_definition.md defines scope (in-scope/out-of-scope) | MEDIUM |
| T1-8 | current_objectives.md has at least one priority | MEDIUM |

### Tier 1 Summary

```
Required structure:
entity/
├── CLAUDE.md           ← Boot instructions
├── context/
│   └── kernel/
│       └── role_definition.md  ← Identity
└── active_work/
    └── current_objectives.md   ← Current focus
```

**Pass criteria**: All 8 items PASS or WARN (no CRITICAL failures)

---

## Tier 2 Required (38 items)

**Full entity** - Includes all Tier 1 items plus memory, inbox, and skills.

### Tier 1 Items (8 items)

All Tier 1 items (T1-1 through T1-8) are required for Tier 2.

### Additional Kernel Files (4 items)

| # | Check | Severity |
|---|-------|----------|
| T2-1 | `context/kernel/operating_principles.md` exists | MEDIUM |
| T2-2 | `context/kernel/persona_profile.md` exists | MEDIUM |
| T2-3 | Kernel files total < 1000 lines | MEDIUM |
| T2-4 | No duplicate content across kernel files | LOW |

### Memory Structure (9 items)

| # | Check | Severity |
|---|-------|----------|
| T2-5 | `memory/sessions/exports/` directory exists | CRITICAL |
| T2-6 | `memory/evolution/learnings/` directory exists | MEDIUM |
| T2-7 | `memory/evolution/decisions/` directory exists | MEDIUM |
| T2-8 | `memory/inbox/` directory exists | CRITICAL |
| T2-9 | At least one session export exists | WARN if missing |
| T2-10 | `current_objectives.md` updated in last 14 days | MEDIUM |
| T2-11 | No stale inbox items (pending > 14 days) | MEDIUM |
| T2-12 | At least one session export in last 30 days | WARN if missing |
| T2-30 | Memory indexes updated in last 7 days (if sessions exist) | MEDIUM |

### Skills Structure (8 items)

| # | Check | Severity |
|---|-------|----------|
| T2-13 | `.claude/skills/` directory exists | CRITICAL |
| T2-14 | `.claude/skills/_index.md` exists | MEDIUM |
| T2-15 | `session-start/SKILL.md` exists | CRITICAL |
| T2-16 | `session-export/SKILL.md` exists | CRITICAL |
| T2-17 | No `/jane/` paths in skills (unless this IS Jane) | CRITICAL |
| T2-18 | No parent entity paths in skills | CRITICAL |
| T2-19 | Paths reference correct entity workspace | CRITICAL |
| T2-20 | SKILL.md files have required sections | MEDIUM |

### Inbox Protocol (4 items)

| # | Check | Severity |
|---|-------|----------|
| T2-21 | Inbox uses flat structure (no subfolders) | CRITICAL |
| T2-22 | All inbox items have YAML frontmatter | CRITICAL |
| T2-23 | Frontmatter includes: type, status, priority, created | MEDIUM |
| T2-24 | No autonomous status changes (human-in-the-loop) | CRITICAL |

### Session Continuity (5 items)

| # | Check | Severity |
|---|-------|----------|
| T2-25 | Session-start skill loads kernel context | CRITICAL |
| T2-26 | Session-start skill checks inbox | CRITICAL |
| T2-27 | Session-export skill creates structured exports | MEDIUM |
| T2-28 | Exports follow template format | LOW |
| T2-29 | Session-export writes to `memory/sessions/exports/` (not `session_exports/`) | CRITICAL |

### Tier 2 Summary

```
Required structure (in addition to Tier 1):
entity/
├── context/
│   └── kernel/
│       ├── operating_principles.md
│       └── persona_profile.md
├── memory/
│   ├── sessions/
│   │   └── exports/
│   ├── evolution/
│   │   ├── learnings/
│   │   └── decisions/
│   └── inbox/
└── .claude/
    └── skills/
        ├── _index.md
        ├── session-start/SKILL.md
        └── session-export/SKILL.md
```

**Pass criteria**: All Tier 1 + Tier 2 items PASS or WARN (no CRITICAL failures)

---

## Role-Specific Requirements

*Run only the section matching your entity's role*

### Orchestrator (5 items)

| # | Check | Severity |
|---|-------|----------|
| O-1 | `context/kernel/agent_coordination.md` exists | CRITICAL |
| O-2 | `context/kernel/_summary.md` exists | MEDIUM |
| O-3 | `memory/evolution/agent_births/` exists | MEDIUM |
| O-4 | All spawned entities listed in coordination file | MEDIUM |
| O-5 | Routing rules defined for each entity | MEDIUM |

### Domain Specialist (4 items)

| # | Check | Severity |
|---|-------|----------|
| D-1 | No coordination file (defers to parent) | LOW |
| D-2 | `memory/messages_to_[parent]/` exists | MEDIUM |
| D-3 | Parent escalation path documented in CLAUDE.md | MEDIUM |
| D-4 | Domain-specific context files present | MEDIUM |

### Meta-Entity (5 items)

| # | Check | Severity |
|---|-------|----------|
| M-1 | `context/kernel/specification_philosophy.md` exists | CRITICAL |
| M-2 | `docs/` directory exists at workspace root | CRITICAL |
| M-3 | Canonical specification maintained in `docs/` | CRITICAL |
| M-4 | Version history tracked (CHANGELOG.md) | MEDIUM |
| M-5 | Peer communication path defined (not escalation) | MEDIUM |

---

## Optional (11 items)

*These are recommended but not required for compliance*

### Structure

| # | Check | Notes |
|---|-------|-------|
| OPT-1 | `context/kernel/_summary.md` exists | Useful if kernel >500 lines |
| OPT-2 | `context/conditional/` directory exists | For role-based context |
| OPT-3 | `data/` directory structure exists | For domain data |
| OPT-4 | `memory/evolution/reviews/` exists | For entities doing reviews |
| OPT-5 | `memory/sessions/exports/_template.md` exists | For consistent exports |
| OPT-6 | `memory/inbox/_README.md` exists | Documents inbox usage |
| OPT-7 | `.claude/commands/` directory exists | For command wrappers |
| OPT-8 | `memory/graph/` directory exists | For context graph (v1.7+) |

### Skills

| # | Check | Notes |
|---|-------|-------|
| OPT-9 | `handoff/SKILL.md` exists | For cross-entity communication |
| OPT-10 | `entity-diagnostic/SKILL.md` exists | For self-validation |
| OPT-11 | `expert-review/SKILL.md` exists | For expert perspectives (v1.7+) |

---

## File Naming Conventions

| File Type | Pattern | Example |
|-----------|---------|---------|
| Inbox items | `YYYY-MM-DD_[slug].md` | `2026-01-05_task-request.md` |
| Session exports | `YYYY-MM-DD_[slug].md` | `2026-01-05_planning-session.md` |
| Learnings | `YYYY-MM-DD_[slug].md` | `2026-01-05_api-patterns.md` |
| Decisions | `NNNN-[slug].md` | `0001-use-typescript.md` |

**Rules**:
- No spaces in filenames (use hyphens)
- Lowercase preferred
- Dates in ISO format (YYYY-MM-DD)

---

## Quick Diagnostic Commands

```bash
# Check for wrong paths in skills
grep -r "/jane/" .claude/skills/

# Count kernel file lines
wc -l context/kernel/*.md

# List inbox structure
find memory/inbox -type f -name "*.md"

# Check for stale inbox items
find memory/inbox -name "*.md" -mtime +14

# List all skills
ls -la .claude/skills/*/SKILL.md
```

---

## Common Issues Reference

| Issue | Cause | Fix |
|-------|-------|-----|
| `/jane/` paths in skills | Copied without update | Search/replace entity paths |
| Nested inbox folders | Pre-v1.3 structure | Flatten, add frontmatter |
| Missing persona_profile.md | Birth oversight | Create from template |
| Stale objectives | Inactive period | Update current focus |
| Extra root directories | Organic growth | Move to appropriate layer |
| Entity doesn't know identity | CLAUDE.md wrong paths | Verify kernel paths |

---

## Validation Workflow

```
1. Determine tier
   │
   ├─→ Tier 1 (8 items)
   │   └─→ Done
   │
   └─→ Tier 2 (38 items)
         │
         └─→ Add role-specific (4-5 items)
             │
             ├─→ Orchestrator: +5 items
             ├─→ Domain Specialist: +4 items
             └─→ Meta-Entity: +5 items

2. Run checks, record results

3. Count by severity:
   - CRITICAL failures: Block deployment
   - MEDIUM failures: Plan remediation
   - LOW failures: Note for later

4. Fix CRITICAL items first

5. Generate validation report
```

---

**Maintained by**: Protocol (Meta-Entity)
**Spec Reference**: ENTITY_SPEC.md v1.8
