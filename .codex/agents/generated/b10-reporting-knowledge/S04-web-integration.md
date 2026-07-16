---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b10-s04-web-integration
scope: "Integrate B10 dashboard, report, Data Guide, send-report, delivery, and export journeys into Web."
spec_version: 0.8.2-draft
requirement_ids: [ADMIN-009, CHART-012, CHART-013, CHART-018, UC-007, UC-011, UC-014, UC-016]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B10
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/b10-reporting-knowledge-plan.md
  prompt_pack_dir: .codex/agents/generated/b10-reporting-knowledge
  stage_ledger: docs/architecture/workstreams/b10-reporting-knowledge-stage-reports/b10-reporting-knowledge-stage-ledger.md
  stage_id: S04
  predecessor_gate: {stage_id: S03, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S03 is accepted, B01 shared UI and B06 reportable contracts are stable, B10 is active for S04]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b10-reporting-knowledge, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S05, unlock_on: accepted, authority: stage_ledger}
---

# B10 S04 — Web integration outline

Intended outcome: accessible dashboard/report builders, snapshot preview,
Data Guide edit/review, user-sent email, recipients/allowlist feedback,
delivery history, export progress, Focus/Explore, and Result Trust.

Detail actual routes/components, keyboard, localization, responsive, reduced
motion, browser fixtures, console/network, and visual QA before execution.
Expected result: browser evidence and only S05 authorized.
