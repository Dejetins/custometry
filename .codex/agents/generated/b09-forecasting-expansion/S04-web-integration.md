---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b09-s04-web-integration
scope: "Integrate B09 specification, training, comparison, prediction, promotion, rollback, and monitoring journeys into Web."
spec_version: 0.8.2-draft
requirement_ids: [JOURNEY-005, UC-005]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B09
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/b09-forecasting-expansion-plan.md
  prompt_pack_dir: .codex/agents/generated/b09-forecasting-expansion
  stage_ledger: docs/architecture/workstreams/b09-forecasting-expansion-stage-reports/b09-forecasting-expansion-stage-ledger.md
  stage_id: S04
  predecessor_gate: {stage_id: S03, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S03 is accepted, B01 and B06 presentation contracts are stable, B09 is active for S04]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b09-forecasting-expansion, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S05, unlock_on: accepted, authority: stage_ledger}
---

# B09 S04 — Web integration outline

Intended outcome: accessible route-backed forecast specs, runs, intervals,
model comparison, champion promotion/rollback, prediction products, monitoring,
Result Trust, progress/ETA, and Focus/Explore.

Detail routes, states, fixtures, keyboard, responsive, reduced-motion, and
console/network checks before execution. Expected result: real browser evidence
and only S05 authorized.
