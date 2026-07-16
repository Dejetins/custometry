---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b08-s04-web-integration
scope: "Integrate B08 customer, segment, cohort, lifecycle, promotion, and range timeline journeys into the shared Web platform."
spec_version: 0.8.2-draft
requirement_ids: [CHART-007, CHART-008, UC-013]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B08
  execution_mode: goal_driven
  plan_doc: docs/architecture/workstreams/b08-customer-intelligence-promotion-journal-plan.md
  prompt_pack_dir: .codex/agents/generated/b08-customer-intelligence-promotion-journal
  stage_ledger: docs/architecture/workstreams/b08-customer-intelligence-promotion-journal-stage-reports/b08-customer-intelligence-promotion-journal-stage-ledger.md
  stage_id: S04
  predecessor_gate: {stage_id: S03, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S03 API contracts are accepted, B01 route and component contracts are stable, B08 is active for S04]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b08-customer-intelligence-promotion-journal, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S05, unlock_on: accepted, authority: stage_ledger}
---

# B08 S04 — Web integration outline

Intended outcome: compact accessible customer intelligence and promotion
journals, searchable filters, `vs LY`, Result Trust, Focus/Explore, and
planned/actual multi-channel range timelines.

Detail actual routes, design tokens, browser fixtures, keyboard/assistive
technology, responsive and console/network checks before execution. Expected
result: real browser evidence and only S05 unlocked.
