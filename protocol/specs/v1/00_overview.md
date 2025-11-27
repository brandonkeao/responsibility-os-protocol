# Responsibility OS Protocol – Overview

The Responsibility OS Protocol v1 defines how autonomous or co-pilot style systems coordinate work while staying aligned with human intent. It is organized around three anchors: the Kernel (decision engine), the Guardrails (safety and compliance envelope), and the Steward (accountable operator persona). Every component downstream references the Kernel and Guardrails so that autonomy never detaches from system constraints.

## Goals
- Provide a reproducible specification for responsible computational systems.
- Keep memory append-only so historical intent and actions are reviewable.
- Ensure new personas or charges can be registered without modifying the Kernel or Guardrails source of truth.

## Structure
1. `01_invariants` to `09_ui_translation` form a linear specification. Each file references how the Kernel and Guardrails apply to that layer.
2. Steward examples show how to instantiate the protocol without embedding product logic.
3. Progress log captures protocol adjustments for future stewards.

Consumers should read these specs sequentially and use the steward artifacts as living tests for the Kernel and Guardrails alignment.
