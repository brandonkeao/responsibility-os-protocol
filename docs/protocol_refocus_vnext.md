# Responsibility OS – Protocol Refocus vNext

Status: Proposed | Owner: Brandon | Scope: Core Protocol Governance, Context & Memory, Agentic Coordination | Change Risk: High

## Executive Intent
Re-center Responsibility OS on multi-agent organizational cognition: Responsibilities as cognitive agents, context as a first-class resource, memory as institutional knowledge, and coordination as organizational behavior. DevOps/telemetry remain supporting infrastructure, not cognitive drivers.

## Canonical Three-Layer Architecture (Enforced)
- **Layer 1 – Core Agentic Spec (stable):** responsibilities, personas vs responsibilities vs stewards vs kernel semantics, authority/escalation, Golden Identity Prompt, memory lifecycle, coordination primitives, guardrails/invariants. Never owns execution, telemetry, routing, or tooling.
- **Layer 2 – Context & Memory Infrastructure:** golden identity enforcement, context packs, unified task brief synthesis, context window budgeting, context density warnings, mem0 integration model, retrieval/compression strategies.
- **Layer 3 – Operational & DevOps Infrastructure:** telemetry/logging (observability only), task routing, data lineage, filesystem standards, external integrations, execution orchestration. Constraint: no Layer-3 system may alter cognition or authority.

## Governance Rules
1) **Every spec declares its layer + change_risk** (see frontmatter). 
2) **No infrastructure may mutate cognition** (Layer 3 is observability/routing only).
3) **Core changes require invariant proof** before adoption.
4) **Optimize for organizational cognition**: context/memory first-class, agent semantics stable.

## Immediate Work Program
- **Phase 1 – Core Model Lock:** authoritative specs for responsibilities, steward, persona, kernel, task worker, authority/escalation, memory state transitions, coordination without infra.
- **Phase 2 – Context & Memory Formalization:** Golden Identity Prompt, context packs, unified task brief, context density warnings, mem0 integration.
- **Phase 3 – Telemetry Reframing:** observability-only; must not change cognition.

## Repo Audit & Refactor Plan
1) Inventory every spec and assign a layer.
2) Detect drift (core vs context vs ops); re-home or split mixed files.
3) Re-anchor README and onboarding around the three-layer model and 30-minute clarity goal.

## Acceptance Criteria
- All specs declare a layer.
- Core semantics locked; context & memory formalized.
- Telemetry is observability-only.
- README/onboarding reflect the layered model; newcomers grok Responsibilities/Memory/Coordination in <30 minutes.
