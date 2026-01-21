# Entity Specification Protocol v2

**Version**: 2.1
**Released**: January 20, 2026

---

## Overview

Version 2 consolidates the numbered v1 specification files into a single comprehensive `ENTITY_SPEC.md`. This represents the matured, production-tested format used across multiple workspaces.

## Files

| File | Purpose |
|------|---------|
| `ENTITY_SPEC.md` | Complete entity specification (2,100+ lines) |
| `validation_checklist.md` | Entity validation framework |

## Key Changes from v1

### Consolidation
- v1's 10 numbered files consolidated into single `ENTITY_SPEC.md`
- Easier to navigate and maintain
- Single source of truth

### New in v2.0
- **Plan Persistence**: Multi-session work tracking with human-in-the-loop approval
- `/persist-plan` skill specification

### New in v2.1
- **Context Maps**: Optional pattern for loadable knowledge modules
- **Skill Classification**: Core/Domain/Custom skill framework

## Migration from v1

v2 is conceptually compatible with v1. Key mappings:

| v1 File | v2 Section |
|---------|------------|
| 01_invariants | Design Philosophy, Token Budget Guidelines |
| 02_responsibility | Entity Roles, Entity Tiers |
| 03_kernel | Three-Layer Architecture, Context |
| 04_guardrails | Operating Principles (in kernel) |
| 05_persona | Persona Profile (in kernel) |
| 06_mandate | CLAUDE.md, Role Definition |
| 07_agent | Entity Roles (Orchestrator, Domain Specialist) |
| 08_memory | Memory Maintenance, Inbox Protocol |
| 09_ui_translation | Boot Sequence |
| 10_tasks | Core Skills, Plan Persistence |

## Usage

For new entities, use `ENTITY_SPEC.md` directly. It contains all required structure, examples, and guidelines for building Jane-like entities.

---

**Maintained by**: Protocol (Meta-Entity)
