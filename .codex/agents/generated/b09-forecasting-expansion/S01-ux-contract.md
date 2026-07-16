---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b09-s01-ux-contract
scope: "Freeze B09 forecast-spec, model, backtest, prediction, monitoring, promotion, API, UI, and error contracts."
spec_version: 0.8.2-draft
requirement_ids: [AC-038, JOURNEY-005]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B09
  execution_mode: goal_driven
  plan_doc: docs/architecture/workstreams/b09-forecasting-expansion-plan.md
  prompt_pack_dir: .codex/agents/generated/b09-forecasting-expansion
  stage_ledger: docs/architecture/workstreams/b09-forecasting-expansion-stage-reports/b09-forecasting-expansion-stage-ledger.md
  stage_id: S01
  predecessor_gate: {stage_id: S00, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S00 is accepted, upstream forecast and feature contracts are stable, B09 is active for S01]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b09-forecasting-expansion, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S02, unlock_on: accepted, authority: stage_ledger}
---

# B09 S01 — UX and contract outline

Intended outcome: immutable spec/model/prediction/monitoring schemas, baseline
requirements, cutoff/feature availability, intervals, state transitions,
permissions, errors, and browser journeys.

Detail after S00 with exact contracts, examples, compatibility, migration,
checks, and stop gates. Expected result: accepted S01 evidence and only S02
authorized.
