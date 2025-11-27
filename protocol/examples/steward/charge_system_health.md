# charge.steward.system_health_check

## Title
Run a Responsibility OS system health check.

## Intent
Validate that Kernel services, Guardrails evaluators, and append-only memory writers are operating normally with the latest policy versions.

## Success Metrics
- Kernel heartbeat recorded within the last hour.
- Guardrails evaluation log contains at least one approved and one denied action for sampling.
- Memory digest matches the Guardrails hash checkpoint.

## Constraints
- Read-only diagnostics; no production changes.
- Guardrails clauses: `safety.runtime_integrity`, `privacy.log_review`.

## Handoff Plan
If automation is unavailable, a human steward follows the same checklist and records findings via the Kernel interface.
