# Intent Router Specification

The intent router converts human or system requests into concrete Responsibility + mandate selections. It relies on the Responsibility registry, capability manifests, and Guardrails to ensure only authorized work is scheduled.

## Inputs
- **Utterance** – natural language text from a human, RequestForAction, or event trigger.
- **Context** – optional metadata (workspace, priority, originating mandate/request).
- **Constraints** – optional filters (e.g., only Responsibilities in `parenting_workspace`).

## Canonical Flow
1. **Normalize intent** – LLM or rules extract key phrases, objective, nouns, and verbs.
2. **Query registry** – call `registry.search(intent_tags, capabilities)` to get candidate Responsibilities.
3. **Score candidates** – compute match score using manifest tags, active mandates, availability, and Guardrails constraints.
4. **Propose plan** – return ranked list with suggested mandate(s) and rationale.
5. **Steward approval** – steward or Kernel auto-rules accept the best proposal, triggering a mandate run or creating an RFA.

## JSON Exchange Format

Requests to the router:
```json
{
  "utterance": "Investigate why annual-plan customers churned last quarter",
  "workspace_id": "rebrandly_bi",
  "context": {
    "origin": "user",
    "priority": 120
  }
}
```

Router response:
```json
{
  "candidates": [
    {
      "responsibility_id": "churn_analysis",
      "mandate_id": "mandate.churn.monthly_analysis",
      "score": 0.93,
      "explanation": "Matches tags ['churn','retention']; mandate supports quarterly cohorts",
      "required_guardrails": ["data.local_use_only"],
      "dependencies": ["data_manager"]
    },
    {
      "responsibility_id": "data_manager",
      "mandate_id": "mandate.data.cohort_correlation",
      "score": 0.71,
      "explanation": "Handles cross-agent correlation but depends on fresh churn analysis"
    }
  ],
  "model_used": "gpt-4o-mini",
  "generated_at": "2025-11-28T10:05:00Z"
}
```

## Kernel APIs
- `intent_router.route(request)` – returns candidates as shown above.
- `intent_router.record_selection(responsibility_id, mandate_id, request_id)` – logs the final choice, enabling telemetry and future learning.

## Guardrails Integration
- Guardrails clauses may require human approval for certain intent categories (e.g., `strategy.*`). The router must include any clauses triggered by the intent so that Kernel approval is aware of the risk profile.

## Telemetry
Installations should log:
- Number of intents routed per workspace.
- Hit rate (top candidate accepted vs. overridden).
- Average latency.
- Model usage (for cost tracking).

These metrics feed stewardship decision-making and ensure the router remains accurate over time.
