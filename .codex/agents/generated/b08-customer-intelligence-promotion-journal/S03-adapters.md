---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b08-s03-adapters
scope: "Implement B08 PostgreSQL, artifact, execution, API, search, and timeline projection adapters."
spec_version: 0.8.2-draft
requirement_ids: [PROMO-004, PROMO-005, TEST-INV-035]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B08
  execution_mode: goal_driven
  plan_doc: docs/architecture/workstreams/b08-customer-intelligence-promotion-journal-plan.md
  prompt_pack_dir: .codex/agents/generated/b08-customer-intelligence-promotion-journal
  stage_ledger: docs/architecture/workstreams/b08-customer-intelligence-promotion-journal-stage-reports/b08-customer-intelligence-promotion-journal-stage-ledger.md
  stage_id: S03
  predecessor_gate: {stage_id: S02, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S02 is accepted, migrations and shared adapters have owners, B08 is active for S03]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b08-customer-intelligence-promotion-journal, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S04, unlock_on: accepted, authority: stage_ledger}
---

# B08 S03 — Adapters outline

Intended outcome: real database/API/artifact adapters for immutable customer,
segment, cohort, lifecycle, and promotion metadata plus range timeline
projection and bounded search.

Detail migrations, retry/idempotency, audit, permissions, rollback, real
integration tests, and cleanup before execution. Expected result: S03 evidence
and authorization for S04 only.
