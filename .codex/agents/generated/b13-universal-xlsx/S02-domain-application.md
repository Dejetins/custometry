---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b13-s02-domain-application
scope: "Implement B13 framework-independent workbook planning, naming, splitting, mapping, sanitization, and manifest policies."
spec_version: 0.8.2-draft
requirement_ids: [TEST-INV-038, V1-AC-011]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B13
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/b13-universal-xlsx-plan.md
  prompt_pack_dir: .codex/agents/generated/b13-universal-xlsx
  stage_ledger: docs/architecture/workstreams/b13-universal-xlsx-stage-reports/b13-universal-xlsx-stage-ledger.md
  stage_id: S02
  predecessor_gate: {stage_id: S01, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S01 is accepted, entity and boundary contracts are frozen, B13 is active for S02]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b13-universal-xlsx, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S03, unlock_on: accepted, authority: stage_ledger}
---

# B13 S02 — Domain and application outline

Intended outcome: pure deterministic sheet/range planning, boundary split,
stable naming/collision resolution, formula neutralization, native/raster
selection, permission/redaction, and manifest identity policies.

Detail invariants, property tests, limits, and stop gates before execution.
Expected result: S02 report and only S03 authorized.
