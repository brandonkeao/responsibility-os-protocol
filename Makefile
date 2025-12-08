WORKSPACE ?= ./workspace_stub

.PHONY: boot-parenting boot-regenerate boot-model-check task-hydrate queue-scaffold queue-mirror telemetry-heartbeat

boot-parenting:
	@echo "Stub boot-parenting: set WORKSPACE=/path/to/workspace"
	@python3 tools/kernel_boot_regenerate.py $(WORKSPACE) --responsibility-id=parenting_cos || true

boot-regenerate:
	@python3 tools/kernel_boot_regenerate.py $(WORKSPACE) --responsibility-id=$${RESPONSIBILITY_ID:-$(notdir $(WORKSPACE))} --log-dir=$(WORKSPACE)/boot_trial_logs || true

boot-model-check:
	@python3 tools/kernel_boot_model_check.py $(WORKSPACE) --actual-model=$${ACTUAL_MODEL:-gpt-4.1} --responsibility-id=$${RESPONSIBILITY_ID:-$(notdir $(WORKSPACE))} || true

task-hydrate:
	@python3 tools/task_worker_hydrate.py $(WORKSPACE) --state=$${STATE:-active} || true

queue-scaffold:
	@python3 tools/queue_scaffold.py $(WORKSPACE) --add-sample || true

queue-mirror:
	@python3 tools/queue_to_markdown.py $(WORKSPACE) || true

telemetry-heartbeat:
	@python3 tools/telemetry_emit.py $(WORKSPACE) --responsibility-id=$${RESPONSIBILITY_ID:-$(notdir $(WORKSPACE))} --event-type=heartbeat --status=$${STATUS:-ok} || true
