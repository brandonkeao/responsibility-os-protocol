# Responsibility Portability Standard

## Purpose
Define how Responsibilities are packaged, exported, and imported as portable filesystem containers so they can move across workspaces without losing auditability or violating guardrails.

## Container Definition
Every instantiated Responsibility must reside in a dedicated directory under the workspace registry:

```
registry/<responsibility_id>/
  context.md
  manifest.json
  logs/
  tasks/
    inbound/
    outbound/
  notes.md
```

- This container is the System-of-Context for the Responsibility and the unit of portability.
- `registry/responsibility_registry.json` (and the SQL registry) index these containers but do not store primary state.
- Isolation: no Responsibility may write into another container without explicit authorization. SYS_HEALTH_OPS retains read-only access for audits.

## Export
1. Verify the container passes the startup checklist (Phase 0).
2. Freeze the container: capture file hashes, BOOT_SUMMARY hash, and a manifest timestamp.
3. Package the directory (tar/zip) with a `PORTABILITY_METADATA.json` containing:
   - `responsibility_id`
   - `workspace_id` (source)
   - `boot_summary_hash`
   - `manifest_hash`
   - `created_at`
4. Log the export in telemetry (`telemetry/incidents/migration_<timestamp>.md`) and memory.

## Import
1. Place the container under `registry/<responsibility_id>/` in the target workspace.
2. Add/merge the entry in `registry/responsibility_registry.json` (or insert into the SQL registry) pointing to the container path and status.
3. Run the startup checklist from Phase 0 to regenerate BOOT_SUMMARY and validate model preferences, guardrails, and tasks inbox/outbox.
4. Emit telemetry + memory entries for the import and any repairs.

## Migration Rules for Existing Workspaces
For each row in `registry/responsibility_registry.json` or the SQL registry:
1. If the container is missing, create it and backfill `context.md`, `manifest.json`, `logs/`, `tasks/inbound`, `tasks/outbound`, and `notes.md`.
2. Move any existing context bundles into `context.md` and record hashes in memory.
3. Log migration under `telemetry/incidents/migration_<timestamp>.md` with references to updated files.

## Task Worker Interaction
- Global tasks remain in `tasks/queue`.
- Per-Responsibility tasks MUST use `registry/<responsibility_id>/tasks/inbound` (inputs) and `tasks/outbound` (outputs).

## Deterministic Boot Contract (Recap)
- Boot is successful only when: registry/index exists, containers exist for all seeded Responsibilities, and required files are present inside each container.
- Boot failure if any container or required file is missing.
