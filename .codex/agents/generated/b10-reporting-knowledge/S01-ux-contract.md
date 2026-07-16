---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b10-s01-ux-contract
scope: "Freeze B10 dashboard, report, snapshot, block, binding, render-identity, API, UI, error, and migration contracts."
spec_version: 0.8.2-draft
requirement_ids: [DASHBOARD-001, DASHBOARD-002, DASHBOARD-003, DASHBOARD-004, DASHBOARD-005, DASHBOARD-006, REPORT-001, REPORT-002, REPORT-003, REPORT-004, REPORT-005, REPORT-006, REPORT-007, REPORT-008, REPORT-009, REPORT-010]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B10
  execution_mode: goal_driven
  plan_doc: docs/architecture/workstreams/b10-reporting-knowledge-plan.md
  prompt_pack_dir: .codex/agents/generated/b10-reporting-knowledge
  stage_ledger: docs/architecture/workstreams/b10-reporting-knowledge-stage-reports/b10-reporting-knowledge-stage-ledger.md
  stage_id: S01
  predecessor_gate: {stage_id: S00, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S00 is accepted, upstream reportable contracts are stable, B10 is active for S01]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b10-reporting-knowledge, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S02, unlock_on: accepted, authority: stage_ledger}
---

# B10 S01 — UX and contract outline

Intended outcome: immutable dashboard/report/snapshot/block schemas, pinned and
latest binding semantics, filters, Result Trust, permissions, cross-render
identity, APIs/errors, and browser journeys.

Detail examples, compatibility, migration, renderer capability, UI states, and
focused gates after S00. Expected result: S01 evidence and only S02 authorized.
