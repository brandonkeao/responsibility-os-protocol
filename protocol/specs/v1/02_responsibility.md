# Responsibility Model

Responsibility OS defines responsibility as the contract between human intent, the Kernel execution path, and the Guardrails that bound behavior. Starting with the Task update, every mandate now materializes into one or more **Tasks** before a Responsibility claims the work, producing the deterministic chain **Mandate → Task → Responsibility → Action**.

## Responsibility Chain
1. **Intent Capture** – Humans declare intent via Mandate definitions (internal authority) or create RequestForAction records for peer Responsibilities; Kernel normalizes structure while Guardrails tag compliance requirements.
2. **Interpretation** – Steward interprets intent through persona filters; Kernel enforces deterministic parsing and Guardrails compare results against prohibited actions.
3. **Execution** – Agents act on behalf of the steward. Kernel issues step-level approvals and Guardrails verify context remains inside allowed scope.
4. **Reflection** – After execution, the steward records reflections and outcomes into append-only memory; Guardrails assert that remediation steps are logged when deviations occur.

### Responsibility Boot Lifecycle
Responsibilities boot through four deterministic phases documented in `protocol/RESPONSIBILITY_BOOT_TEMPLATE.md` and consolidated operationally in `protocol/RESPONSIBILITY_STARTUP_CHECKLIST.md`:

1. **Phase 0 – Static Files**: Kernel validates persona, guardrails, mandate definitions, and known tools.
2. **Phase 1 – Orientation Boot**: Steward produces a BOOT\_SUMMARY using the canonical schema so downstream agents inherit rules, tool safety notes, and context gaps.
3. **Phase 2 – BOOT\_SUMMARY Persistence**: Summary becomes the primary runtime artifact; raw files serve as append-only provenance. Stewards must invoke `kernel.boot.regenerate(<responsibility_id>)` to update it; manual edits are prohibited.
4. **Phase 3 – Task Execution Rehydration**: Responsibilities replay open Tasks (and their Mandate references) before issuing new actions so memory, Task status, and RequestForAction links remain aligned.

The BOOT\_SUMMARY schema carries `always_rules`, `tool_usage_rules`, `known_tools`, `open_state_threads`, and `context_gaps`. Guardrails treat BOOT\_SUMMARY as authoritative until a reboot occurs (triggered by policy, tool, or scope changes) and log every regeneration delta to memory.

### Model Declaration & Boot Enforcement
Responsibilities must declare their runtime model policy:

```yaml
model:
  default_model: gpt-5.1
  allowed_models:
    - gpt-5.1
    - gpt-4.1-mini
  notes: Primary tested model.
```

- During Phase 0/1 of the startup checklist the Kernel compares `actual_model` (reported by orchestration) to `default_model`.
- If they match → boot continues.
- If `actual_model` is in `allowed_models` → Guardrails emit a soft warning and log telemetry (`model_mismatch_on_boot` with `status=warning`).
- If `actual_model` is outside the list → Guardrails emit a hard warning, require operator decision (`proceed`, `abort`, or `update_default_model`), and log telemetry with `status=critical`.
- Choosing `update_default_model` demands a PROGRESS\_LOG entry plus append-only memory pointer referencing the policy change.

Every decision is recorded in memory (`boot_model_check`) and telemetry (`model_mismatch_on_boot`) so auditors can trace deviations.

## Transfer of Responsibility
Responsibility can be delegated only when:
- The receiving agent acknowledges the Mandate run or accepted RequestForAction reference and corresponding Guardrails clause.
- Kernel records the delegation pointer in memory.
- Append-only memory contains both the transfer request and acceptance entries.

If the Guardrails detect missing acknowledgements, the Kernel reclaims responsibility and blocks further execution.

Responsibility folders must keep semantic context (System-of-Context) synchronized with the SQL-backed registry and request queue (System-of-Record). All delegations are logged in both layers so AI assistants can narrate the why while deterministic services preserve the what.
