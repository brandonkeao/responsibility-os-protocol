# request.steward.finance_to_parenting_allowance

```yaml
origin_responsibility_id: finance_cos
target_responsibility_id: parenting_cos
origin_mandate_id: finance_cos.monthly_budget_review
request_id: req_2025-11-28T09-15Z_finance_to_parenting_allowance
status: pending
priority: 100
authored_by: ai
author_agent_id: finance_cos
created_at: 2025-11-28T09:15:00Z
available_at: 2025-11-28T09:15:00Z
source_context: mandate_run:finance_cos.monthly_budget_review@2025-11-28T09:00Z
```

## Summary
Finance CoS recommends establishing a structured allowance plan for Child A that respects the latest household budget. Parenting CoS is asked to consider running its `allowance_design` mandate and reporting back.

## Suggested Response Options
- Accept and clone the `allowance_design` mandate template, linking the resulting run ID back to this request.
- Defer until the Parenting cadence meeting on `2025-11-30`. Update the SQL row with a new `available_at`.
- Reject with rationale (e.g., missing data) so Finance CoS can adjust inputs.

## Context References
- Finance budget report: `../finance_cos/reports/2025-11-28_family_budget_review.md`
- Child profile: `parenting_cos/context/knowledge/kids_profiles.md`

> _Note: this markdown is a view generated from the SQL queue. The canonical row lives in `requests` with the same `request_id`._
