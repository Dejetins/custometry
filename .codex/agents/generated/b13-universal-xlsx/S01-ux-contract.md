---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b13-s01-ux-contract
scope: "Freeze B13 workbook, entity, manifest, sheet, split, chart, fallback, security, API, UI, error, and artifact contracts."
spec_version: 0.8.2-draft
requirement_ids: [XLSX-001, XLSX-002, XLSX-003, XLSX-004, XLSX-005, XLSX-006, XLSX-007, XLSX-008, XLSX-009]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B13
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/b13-universal-xlsx-plan.md
  prompt_pack_dir: .codex/agents/generated/b13-universal-xlsx
  stage_ledger: docs/architecture/workstreams/b13-universal-xlsx-stage-reports/b13-universal-xlsx-stage-ledger.md
  stage_id: S01
  predecessor_gate: {stage_id: S00, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S00 is accepted, B10 snapshot and B12 hardening contracts are stable, B13 is active for S01]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b13-universal-xlsx, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S02, unlock_on: accepted, authority: stage_ledger}
---

# B13 S01 — UX and contract outline

Intended outcome: versioned workbook assembly, block mapping, data/presentation
sheet, names/ranges, split, native/raster chart, manifest/hash, security,
progress/cancellation, API/error, and browser contracts.

Detail examples, compatibility, limits, fallback matrix, migration, and gates
after S00. Expected result: S01 evidence and only S02 authorized.
