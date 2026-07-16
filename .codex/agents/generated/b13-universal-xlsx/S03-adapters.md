---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b13-s03-adapters
scope: "Implement B13 workbook-library, OOXML validation, artifact, renderer, temp-storage, cancellation, and API adapters."
spec_version: 0.8.2-draft
requirement_ids: [TEST-INV-032, TEST-INV-044, TEST-INV-047]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B13
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/b13-universal-xlsx-plan.md
  prompt_pack_dir: .codex/agents/generated/b13-universal-xlsx
  stage_ledger: docs/architecture/workstreams/b13-universal-xlsx-stage-reports/b13-universal-xlsx-stage-ledger.md
  stage_id: S03
  predecessor_gate: {stage_id: S02, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S02 is accepted, approved workbook and renderer adapters are selected, B13 is active for S03]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b13-universal-xlsx, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S04, unlock_on: accepted, authority: stage_ledger}
---

# B13 S03 — Adapters outline

Intended outcome: real workbook generation, native/raster charts, immutable
artifact commit, temp cleanup, cancellation, OOXML validation, application
openability harness, progress, API, and resource controls.

Detail libraries, supply chain, file effects, timeouts, cleanup, and
integration tests before execution. Expected result: S03 evidence and only S04
authorized.
