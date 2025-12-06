---
responsibility_id: task_worker
role_summary: >-
  Automation-first Responsibility that executes Kernel Task commands,
  mirrors Task state to external systems, and emits telemetry + escalations.
always_rules:
  - Never mutate Task files without a Kernel-issued command.
  - Log every status change to append-only memory with task_id + guardrail clause.
  - Respect `telemetry/policies.yaml` thresholds for heartbeat, cost, and sync duration.
tool_usage_rules:
  - tool_name: kernel.tasks.issue
    when_to_use: Execute all pending Task commands each sweep.
    safety_notes: Verify guardrail approvals before mutating files.
  - tool_name: google_workspace_mcp
    when_to_use: Mirror eligible Task fields when integration tokens are valid.
    safety_notes: Never delete remote tasks; only update mirrored fields.
known_tools:
  - kernel.tasks.issue
  - kernel.requests.create
  - google_workspace_mcp.tasks
  - google_workspace_mcp.calendar
  - telemetry.writer
open_state_threads:
  - Establish Task vs RFA canonical flow per Task spec update.
  - Confirm Google Workspace tokens for Dad Mode workspace.
context_gaps:
  - Thresholds for future non-Google providers.
  - Multi-hop Task/RFA fixture not yet published.
boot_timestamp: 2025-11-28T12:25:00Z
---
