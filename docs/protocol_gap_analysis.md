# Protocol v1.1 Gap Analysis (2025-11-27)

This note evaluates the current Responsibility OS protocol after incorporating the v1.1 context/execution evolution work. It highlights areas to consider for the next revision of the standard. Items marked **[Spec]** belong in protocol law; items marked **[Guide]** can live in docs or playbooks.

## 1. Registry & Versioning (**[Spec]**)
- We define mandates, personas, and Guardrails, but there is no canonical registry schema for responsibilities (IDs, tags, owners, lifecycle). Consider formalizing a `responsibilities` table and associated markdown manifest so installations can sync members deterministically.
- No protocol-level migration process exists when mandate definitions change. We should specify how to version mandates (e.g., semantic version field + supersedes pointer) and how to mark runs against historical versions.

## 2. RequestForAction Service Levels (**[Spec]**)
- The request spec describes status transitions but omits SLA/timeout policies. Introduce normative guidance for `available_at`, `due_at`, escalation timers, and automated reminders logged to memory.
- Define how to handle batching/ordering when a responsibility has multiple queues (e.g., “urgent” vs “standard”) and how Guardrails audit fairness.

## 3. Meeting & Transcript Indexing (**[Guide]**)
- RFS now includes `meetings/summaries` and `meetings/transcripts`, but we should prescribe a metadata schema (frontmatter fields for topic, participants, responsibilities concerned, tags). This will enable deterministic linking to mandates/requests and power future RAG pipelines.
- Add guidance for storing action items that emerge from meetings and linking them to mandate runs or RFAs.

## 4. Observability & Telemetry (**[Spec]**)
- Kernel and context workers emit memory entries but there is no standardized telemetry stream (metrics, health probes). Define a minimal “operational telemetry contract” (heartbeat interval, error topics, log levels) so multiple implementations can coexist.

## 5. Role-Based Access & Secrets (**[Spec]**)
- The filesystem standard avoids personal data but does not describe secret handling when mandates require credentials. We should specify how secrets are referenced (e.g., via vault IDs) and how Guardrails ensure AI never sees plaintext secrets.

## 6. Patch Proposal Governance (**[Guide]**)
- Patch proposals exist but lack an approval workflow. Recommend a steward review checklist (impact assessment, back-out plan) and define timeouts/escalations when proposals remain pending.

## 7. Model Preference Enforcement (**[Spec]**)
- We added `model_preferences.md`, yet there is no canonical machine-readable schema. Define required fields (preferred model, version, fallbacks, last_detected_model, enforcement_mode) so orchestration services can parse and act consistently.

## 8. Context Worker Scaling (**[Guide]**)
- Context refresh cadence is unspecified. Provide guidance for choosing frequencies (per Responsibility criticality), failure handling, and instrumentation (e.g., log bundle size, latency).

## 9. Cross-Responsibility Discovery (**[Guide]**)
- As new responsibilities join, there is no protocol for discovering relevant historical artifacts beyond manual reading. Document a recommended process (AI-assisted survey, RAG against root context, human nomination) and describe how to store the mapping between responsibilities and notable transcripts/reports.

## 10. Compliance & Legal Hooks (**[Spec]**)
- If organizations need legal approvals, the protocol should mention optional compliance attachments (e.g., `compliance/` folder with attestations) and how Guardrails reference them before executing mandates tied to regulated data.

## 11. Canonical Examples & Tests (**[Guide]**)
- Steward examples cover basic mandates and one request. We should add test fixtures for multi-hop workflows (Mandate → RFA → Mandate) and for failure scenarios (rejections, expired requests) to help new adopters validate implementations.

Addressing these items will tighten the standard before we ratify a v1.2 release and will make downstream ecosystem development (e.g., Dad Mode) smoother.
