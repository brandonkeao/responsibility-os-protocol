---
authored_by: human
author_id: protocol_steward
created_at: 2025-12-06T20:30:00Z
updated_at: 2025-12-06T20:30:00Z
source: protocol_update:context_packs_v1
context_role: spec
---
# Context Pack Specification

Context Packs are curated, versioned bundles of structured context files used to improve reasoning quality for a specific discipline, role, or use case. Packs are inputs to AI Context Bundles and must be synthesized into a Unified Task Brief (UTB) before execution—never concatenated directly into prompts.

## Placement (RFS)
Store packs under `context/packs/<pack_id>/` with:
- `context_pack.yaml` (manifest)
- 3–6 structured markdown files

All files must follow RFS frontmatter/provenance rules and use patch proposals for material changes.

## Manifest Schema (`context_pack.yaml`)
```yaml
id: pm_pricing_experiments_plg_v1
name: "PLG Pricing Experiments – B2B SaaS"
discipline: product_management
scope: system | workspace | responsibility | task
version: 1.0.0
default_roles:
  - "Pricing Lead"
  - "Growth PM"
files:
  - pm_pricing_identity_v1.md
  - pm_pricing_playbook_v1.md
  - pm_experiment_template_v1.md
  - pm_metrics_reference_v1.md

mem0:               # optional, when using external memory
  enabled: true
  memory_types:
    - past_experiments
    - org_principles
    - user_preferences
  query_tags:
    - pricing
    - revenue
    - experiments
  max_memories: 10
  max_tokens_hint: 800
```

## Structured Context Files
Every pack file must include frontmatter:
```yaml
---
id: pm_pricing_playbook_v1
discipline: product_management
type: playbook         # identity | playbook | reference | policy | template
scope: responsibility  # or system | workspace | task
priority: high
version: 1.0.0
tags: [pricing, experiments, plg, saas]
load_strategy: default
max_tokens_hint: 1200
summary_tokens: 220
---
```

Required sections:
- TL;DR
- Objectives
- Core Principles
- Canonical Structure / Steps
- Heuristics & Checklists
- Examples & Anti-Examples
- Interactions With Other Files

## Unified Task Brief (UTB) Rules
- Mandatory synthesis: select relevant pack files, extract needed sections, and synthesize a UTB (500–1,200 tokens).
- UTB content: single task goal; top 5–8 governing principles; only necessary structures/constraints; style normalized to steward persona + Golden Identity Prompt (GIP).
- No raw concatenation of pack files into prompts. If UTB generation fails, block execution and log memory/telemetry.

## Density Warnings
- Estimate UTB + pack-derived content. Recommended operating range: 2,000–3,500 tokens.
- When exceeding the range, emit a warning (not a block), log pack counts and estimated tokens, and require operator acknowledgment for overrides.

## Execution Stack Order
Guardrails > GIP/persona > UTB > memory injections > user task input. Packs feed UTB; UTB enters the prompt, not the raw pack files.

## mem0 Guidance (Optional)
- mem0 is an optional external memory source; it is never the System-of-Record.
- Memory injections must be summarized, bounded by `max_memories`/`max_tokens_hint`, and placed below UTB and above user input.
- Handle PII/retention per workspace policy; on mem0 outage, proceed without mem0 and log the condition.

## Legacy/Compatibility
- Responsibilities without packs or GIP may operate in legacy mode temporarily, but new Responsibilities must supply GIP and adhere to UTB rules. Surface warnings during boot until upgraded.
