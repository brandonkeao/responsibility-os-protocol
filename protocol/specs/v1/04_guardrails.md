---
layer: core
change_risk: high
---

# Guardrails Specification

Guardrails define the operative safety, compliance, and ethics boundaries that every Kernel module references before acting. They act as an always-on co-processor that can veto Kernel decisions.

## Components
1. **Policy Library** – Canonical set of clauses mapped to risks. Each clause includes escalation instructions and Kernel callback signatures.
2. **Evaluator** – Runs policies against proposed Kernel actions. Evaluator must confirm append-only memory entries exist for prerequisite context.
3. **Interlocks** – Mechanisms that pause or halt Kernel loops when clauses fail. Interlocks always log the decision to memory before signaling the Kernel, including blocking a RequestForAction transition when the target Responsibility lacks an appropriate mandate.
4. **Transparency Layer** – Exposes human-readable rationales referencing policy IDs so stewards can explain enforcement outcomes.

## Enforcement Flow
- Kernel submits `guardrail_ref` plus context.
- Guardrails evaluate policies, referencing prior memory entries to preserve append-only audit trails.
- Guardrails verify that any RequestForAction status change aligns with the deterministic state machine defined in the protocol and cross-checks the SQL queue row.
- If approved, Guardrails sign the decision and return it to the Kernel. If rejected, a remediation instruction is emitted and logged.

Guardrails must be versioned with semantic identifiers. Kernel loads only compatible versions, preventing silent drift between safety code and operational logic.

## BOOT_SUMMARY Enforcement
- **Ownership** – BOOT\_SUMMARY artifacts are steward-owned but Guardrails enforce that only `kernel.boot.regenerate` may create or update them. Any manual modification attempt (file hash mismatch without a corresponding regeneration entry) triggers `boot_summary_violation` and halts mandate activation.
- **Drift Control** – Each regeneration logs `(previous_hash, new_hash, responsibility_id)` to memory. Guardrails compare the latest hash against the on-disk file during every Phase 0 check; mismatches block boot.
- **Auditability** – Guardrails retain a ledger of regeneration events so auditors can prove which policies and tools were in effect at any point in time.

## Context Ingestion Oversight
- Guardrails ensure only the designated steward for a workspace can change bundle `ingestion_status`, originate `new_context_available` RFAs, or accept `ingest_new_context` requests.
- Every transition logs telemetry (`context_ingested`, `context_dispatched`) and a memory pointer; Guardrails compare bundle metadata (origin, scope, responsibilities) to the RFAs generated to prevent over-dispatch.
- Opt-out acknowledgments from Responsibilities must be honored; Guardrails block repeated notifications when a Responsibility marked the context as irrelevant unless new scope is provided.

## Context Hygiene Enforcement
- Guardrails ingest a `context_volume` metric emitted during bundle refresh. If total context exceeds thresholds (Green <2,500 lines; Yellow 2,500–3,000 monitor; Red >3,000), Guardrails may require consolidation or explicit steward override before publishing bundles.
- Guardrails verify critical operational workflows retain prominence (>10% of total bundle) and are not displaced by verification/meta docs; if prominence falls, block or warn until consolidation is applied.
- Changes that increase context volume by >10% without consolidation prompts are flagged for steward approval and logged to append-only memory with rationale.

## Golden Identity Prompt and UTB
- A Responsibility must provide a human-authored Golden Identity Prompt (GIP) defining mission, optimization, decision style, ethics, voice, and failure modes. GIP is stored alongside persona (e.g., `persona/golden_identity.md`) with RFS frontmatter and patch-proposal change control.
- Guardrails block boot/mandate execution if GIP is missing or unsigned; remediation is to author/approve GIP and re-run boot checks.
- GIP anchors style/intent; it must not override safety clauses. Precedence: Guardrails > GIP/persona > UTB > memory injections.
- Context Packs feed a Unified Task Brief (UTB); Guardrails require that UTB generation succeeds and respects GIP. If UTB synthesis fails, block execution and log to memory/telemetry.
- Guardrails log context density warnings when UTB + pack-derived content exceeds 2,000–3,500 tokens; warnings do not block by default but require operator acknowledgment for overrides.
- Guardrails should warn when Responsibilities operate in legacy mode (no GIP or packs) and require upgrade before accepting non-legacy workloads.
