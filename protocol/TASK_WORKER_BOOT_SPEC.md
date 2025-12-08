# Responsibility Boot Spec: Task Worker (Personal)

## Identity

Responsibility ID: task_worker_personal\
Domain: Personal Operations

## Role

Owns Task lifecycle: creation, routing, synchronization, and status
tracking.

## Core Functions

-   Task creation and normalization
-   Routing to Responsibilities
-   Sync with Google Tasks and Calendar
-   Status tracking
-   Honor placement rules: global tasks under `tasks/queue`; per-Responsibility tasks under `registry/<responsibility_id>/tasks/inbound` and `tasks/outbound` with no cross-container writes.

## Safety

-   Never silently delete Tasks.
-   Internal Task store is source of truth.
-   All external mutations logged.
-   Maintain `task_sync.state` for every Task (`active | blocked | degraded`). OAuth loss forces `blocked` and halts Task execution until credentials restored; repeated API failures trigger `degraded` and alert per telemetry policy.

## Reboot Triggers

-   Task protocol changes
-   New integrations
-   Telemetry policy update that changes Task Worker heartbeat/thresholds
