---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b08-s00-discovery
scope: "Discover and reconcile B08 customer, segment, cohort, lifecycle, promotion, timeline, ownership, and evidence boundaries."
spec_version: 0.8.2-draft
requirement_ids: [GAP-038, GAP-049, RISK-012]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B08
  execution_mode: goal_driven
  plan_doc: docs/architecture/workstreams/b08-customer-intelligence-promotion-journal-plan.md
  prompt_pack_dir: .codex/agents/generated/b08-customer-intelligence-promotion-journal
  stage_ledger: docs/architecture/workstreams/b08-customer-intelligence-promotion-journal-stage-reports/b08-customer-intelligence-promotion-journal-stage-ledger.md
  stage_id: S00
  predecessor_gate: {stage_id: null, allowed_statuses: []}
  state_preconditions: [B01 B03 B04 B05 and B06 dependency slices are accepted, B08 is explicitly activated, the S00 outline is detailed against current sources]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b08-customer-intelligence-promotion-journal, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S01, unlock_on: accepted, authority: stage_ledger}
---

# B08 S00 — Discovery outline

Intended outcome: a source-anchored inventory of current customer intelligence,
segment, cohort, lifecycle, promotion, timeline, UI, data-owner, permission,
and evidence gaps.

Before activation, replace this outline with an executable prompt containing
current file ownership, exact matrix rows, source hashes, checks, stop gates,
and the accepted B07 soft-dependency strategy. Expected result: an English S00
report and a ledger update authorizing only S01.
