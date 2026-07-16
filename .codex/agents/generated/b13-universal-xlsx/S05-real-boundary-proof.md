---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b13-s05-real-boundary-proof
scope: "Prove B13 cross-render totals, Excel limits, injection, collisions, native/raster charts, resources, cancellation, cleanup, and openability."
spec_version: 0.8.2-draft
requirement_ids: [TEST-INV-032, TEST-INV-038, TEST-INV-044, TEST-INV-047, V1-AC-012]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B13
  execution_mode: goal_driven
  plan_doc: docs/architecture/workstreams/b13-universal-xlsx-plan.md
  prompt_pack_dir: .codex/agents/generated/b13-universal-xlsx
  stage_ledger: docs/architecture/workstreams/b13-universal-xlsx-stage-reports/b13-universal-xlsx-stage-ledger.md
  stage_id: S05
  predecessor_gate: {stage_id: S04, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S04 is accepted, target workbook application renderer artifact and browser boundaries are available, B13 is active for S05]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b13-universal-xlsx, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S06, unlock_on: accepted, authority: stage_ledger}
---

# B13 S05 — Real-boundary proof outline

Intended outcome: reproducible no-loss/no-duplicate split, formula injection,
sheet collisions, cross-render totals, native/raster parity, large workbook
memory/temp/disk, cancellation/cleanup, OOXML validation, real application
openability, API, and browser evidence.

Detail exact fixtures, limits, applications, commands, hashes, measurements,
cleanup, and stop gates before execution.
