---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b11-s04-web-integration
scope: "Integrate B11 pipeline canvas, plugin lifecycle, operational channel, endpoint, attempt, and reconciliation journeys into Web."
spec_version: 0.8.2-draft
requirement_ids: [NOTIFY-006, NOTIFY-008, UC-006]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B11
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/b11-pipelines-extensibility-operational-channels-plan.md
  prompt_pack_dir: .codex/agents/generated/b11-pipelines-extensibility-operational-channels
  stage_ledger: docs/architecture/workstreams/b11-pipelines-extensibility-operational-channels-stage-reports/b11-pipelines-extensibility-operational-channels-stage-ledger.md
  stage_id: S04
  predecessor_gate: {stage_id: S03, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S03 is accepted, B01 and B07 UI contracts are stable, B11 is active for S04]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b11-pipelines-extensibility-operational-channels, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S05, unlock_on: accepted, authority: stage_ledger}
---

# B11 S04 — Web integration outline

Intended outcome: accessible canvas with keyboard alternative, validation,
plugin administration, channel settings, endpoint tests/status, delivery
attempts, and reconciliation, while public-MVP in-app-only history remains
clear.

Detail routes, components, permissions, browser fixtures, responsive,
accessibility, console/network, and visual QA before execution.
