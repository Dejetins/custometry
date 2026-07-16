---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b08-s01-ux-contract
scope: "Freeze B08 journeys, lifecycle, API, artifact, permission, timeline, ChartSpec, error, and migration contracts."
spec_version: 0.8.2-draft
requirement_ids: [PROMO-001, PROMO-002, PROMO-003, PROMO-004, PROMO-005, PROMO-006, PROMO-007, PROMO-008, PROMO-009]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B08
  execution_mode: goal_driven
  plan_doc: docs/architecture/workstreams/b08-customer-intelligence-promotion-journal-plan.md
  prompt_pack_dir: .codex/agents/generated/b08-customer-intelligence-promotion-journal
  stage_ledger: docs/architecture/workstreams/b08-customer-intelligence-promotion-journal-stage-reports/b08-customer-intelligence-promotion-journal-stage-ledger.md
  stage_id: S01
  predecessor_gate: {stage_id: S00, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S00 is terminal and accepted for execution, B05 and B06 contracts are stable, B08 is active for S01]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b08-customer-intelligence-promotion-journal, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S02, unlock_on: accepted, authority: stage_ledger}
---

# B08 S01 — UX and contract outline

Intended outcome: versioned contracts for customer/segment/cohort/lifecycle
views, immutable promotion versions, planned/actual ranges, channel/client
scope, pinned audiences, non-causal overlays, permissions, errors, and browser
journeys.

Detail this prompt only after S00. Expected result: tested schemas/examples,
contract-impact and migration decisions, browser scenarios, an English S01
report, and ledger authorization for S02 only.
