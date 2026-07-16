---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b09-s02-domain-application
scope: "Implement B09 framework-independent specification, cutoff, split, comparison, champion, rollback, and monitoring policies."
spec_version: 0.8.2-draft
requirement_ids: [TEST-INV-004, TEST-INV-009, TEST-INV-030]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B09
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/b09-forecasting-expansion-plan.md
  prompt_pack_dir: .codex/agents/generated/b09-forecasting-expansion
  stage_ledger: docs/architecture/workstreams/b09-forecasting-expansion-stage-reports/b09-forecasting-expansion-stage-ledger.md
  stage_id: S02
  predecessor_gate: {stage_id: S01, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S01 is accepted, leakage and model identity contracts are frozen, B09 is active for S02]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b09-forecasting-expansion, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S03, unlock_on: accepted, authority: stage_ledger}
---

# B09 S02 — Domain and application outline

Intended outcome: pure rolling-cutoff, future-availability, baseline comparison,
spec/model identity, promotion/rollback, prediction, and monitoring policies
with property and leakage-negative tests.

Detail exact packages, tolerances, invariants, and gates before execution.
Expected result: S02 report and only S03 authorized.
