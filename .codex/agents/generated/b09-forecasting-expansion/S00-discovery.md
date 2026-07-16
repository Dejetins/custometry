---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b09-s00-discovery
scope: "Discover B09 baseline forecast, feature, model, registry, monitoring, UI, operations, ownership, and evidence gaps."
spec_version: 0.8.2-draft
requirement_ids: [GAP-013, GAP-014, GAP-015, GAP-016, RISK-005, SEC-005]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B09
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/b09-forecasting-expansion-plan.md
  prompt_pack_dir: .codex/agents/generated/b09-forecasting-expansion
  stage_ledger: docs/architecture/workstreams/b09-forecasting-expansion-stage-reports/b09-forecasting-expansion-stage-ledger.md
  stage_id: S00
  predecessor_gate: {stage_id: null, allowed_statuses: []}
  state_preconditions: [B04 B05 B06 and B08 dependency slices are accepted, B09 is explicitly activated, this outline is detailed against current sources]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b09-forecasting-expansion, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S01, unlock_on: accepted, authority: stage_ledger}
---

# B09 S00 — Discovery outline

Intended outcome: a source-anchored inventory of B06 baselines, features,
forecast specs, libraries, model artifacts, backtests, monitoring, UI, compute,
operations, and unresolved decisions.

Before activation, add exact source hashes, owners, matrix rows, checks, stop
gates, and the B07 soft-dependency strategy. Expected result: S00 report and
only S01 authorized.
