# mandate.task_worker.task_escalation

## Title
Escalate blocked Tasks to the appropriate Responsibility or human steward.

## Intent
Detect Tasks flagged as `blocked` or lacking an assignable Responsibility, then emit RequestForAction entries or steward alerts so the work item can be reassigned promptly.

## Success Metrics
- Blocked Tasks receive an RFA or steward notification within 15 minutes.
- Each escalation references the originating Task ID, mandate run ID, and guardrail clause authorizing the intervention.
- Telemetry logs show zero unresolved escalations older than 24 hours.

## Constraints
- Guardrails clauses: `requests.sla_compliance`, `scope.foundation_only`.
- Escalations must cite the Task's mandate or RFA pointer to maintain auditability.
- If multiple Responsibilities qualify, the Task Worker defers to the steward persona for selection rather than guessing.

## Handoff Plan
When the Task Worker cannot determine an escalation target, it issues `request.task_worker.needs_assignment` addressed to the steward Responsibility, including suggested next steps and links to relevant context files.
