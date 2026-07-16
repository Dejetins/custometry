---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b13-s04-web-integration
scope: "Integrate B13 XLSX scope, estimate, warning, progress, cancellation, completion, download, expiry, and audit journeys into Web."
spec_version: 0.8.2-draft
requirement_ids: [UC-015, XLSX-001]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B13
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/b13-universal-xlsx-plan.md
  prompt_pack_dir: .codex/agents/generated/b13-universal-xlsx
  stage_ledger: docs/architecture/workstreams/b13-universal-xlsx-stage-reports/b13-universal-xlsx-stage-ledger.md
  stage_id: S04
  predecessor_gate: {stage_id: S03, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S03 is accepted, B01 and B10 export UI contracts are stable, B13 is active for S04]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b13-universal-xlsx, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S05, unlock_on: accepted, authority: stage_ledger}
---

# B13 S04 — Web integration outline

Intended outcome: accessible export configuration, permission feedback,
estimated size/fallback/split warnings, progress/ETA, cancellation, completion,
download/expiry, errors, and audit identity.

Detail routes, states, fixtures, keyboard, responsive, localization,
console/network, and visual QA before execution. Expected result: browser
evidence and only S05 authorized.
