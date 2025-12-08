#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <workspace_dir> [--include-task-worker]" >&2
  exit 1
fi

WORKSPACE_DIR="$1"
INCLUDE_TASK_WORKER=false
if [[ $# -ge 2 && "$2" == "--include-task-worker" ]]; then
  INCLUDE_TASK_WORKER=true
fi

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TEMPLATE_DIR="$ROOT_DIR/protocol/examples"

mkdir -p "$WORKSPACE_DIR"
cd "$WORKSPACE_DIR"

mkdir -p ai_context mandates/definitions tasks queue/inbox memory telemetry/heartbeats boot_trial_logs onboarding

: > memory/events.md
cat > tasks/index.json <<'JSON'
{
  "tasks": [],
  "task_sync": {
    "state": "needs_action",
    "last_synced_at": null
  }
}
JSON

cat > ai_context/model_preferences.md <<'MD'
# Model Preferences

preferred_model: gpt-4.1
allowed_models:
  - gpt-4.1
  - gpt-4o-mini
last_detected_model: unknown
fallback_policy: prefer_default
remediation: "If runtime model drifts, rerun kernel.boot.model_check and switch back to preferred model before continuing."
MD

cat > BOOT_SUMMARY.latest.json <<'JSON'
{
  "responsibility_id": "TBD",
  "generated_at": null,
  "hash": null,
  "source": "scaffold_placeholder",
  "notes": "Replace via kernel.boot.regenerate when available."
}
JSON

cat > queue/README.md <<'MD'
# Queue Mirrors

This folder holds markdown mirrors of RequestForAction rows (queue/inbox/*.md). Regenerate from the SQL queue before each boot.
MD

cat > telemetry/heartbeats/README.md <<'MD'
# Telemetry Heartbeats

Drop heartbeat JSON snapshots here during boot. Each file should include responsibility_id, status, timestamp, and source hash.
MD

copy_if_exists() {
  local src="$1" dest="$2"
  if [[ -f "$src" ]]; then
    cp "$src" "$dest"
  fi
}

mkdir -p steward_jane
copy_if_exists "$TEMPLATE_DIR/steward/steward_persona.md" steward_jane/persona.md
copy_if_exists "$TEMPLATE_DIR/steward/steward_guardrails.md" steward_jane/guardrails.md
copy_if_exists "$TEMPLATE_DIR/steward/steward_responsibility.md" steward_jane/responsibility.md
copy_if_exists "$TEMPLATE_DIR/steward/steward_kernel.md" steward_jane/kernel.md
copy_if_exists "$TEMPLATE_DIR/steward/mandate_bootstrap_first_cos.md" steward_jane/mandate_bootstrap_first_cos.md
copy_if_exists "$TEMPLATE_DIR/steward/mandate_system_health_check.md" steward_jane/mandate_system_health_check.md
copy_if_exists "$TEMPLATE_DIR/steward/mandate_welcome_user.md" steward_jane/mandate_welcome_user.md
copy_if_exists "$TEMPLATE_DIR/steward/request_allowance_plan.md" steward_jane/request_allowance_plan.md

if [[ "$INCLUDE_TASK_WORKER" == true ]]; then
  mkdir -p task_worker
  copy_if_exists "$TEMPLATE_DIR/task_worker/task_worker_persona.md" task_worker/persona.md
  copy_if_exists "$TEMPLATE_DIR/task_worker/task_worker_responsibility.md" task_worker/responsibility.md
  copy_if_exists "$TEMPLATE_DIR/task_worker/mandate_task_hydration.md" task_worker/mandate_task_hydration.md
  copy_if_exists "$TEMPLATE_DIR/task_worker/mandate_task_escalation.md" task_worker/mandate_task_escalation.md
  copy_if_exists "$TEMPLATE_DIR/task_worker/BOOT_SUMMARY.md" task_worker/BOOT_SUMMARY.md
fi

echo "Workspace scaffolded at $WORKSPACE_DIR"
