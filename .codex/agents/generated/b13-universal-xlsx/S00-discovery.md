---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b13-s00-discovery
scope: "Discover B13 final ReportSnapshot/block contracts, Excel/OOXML limits, renderers, libraries, security, ownership, and evidence gaps."
spec_version: 0.8.2-draft
requirement_ids: [GAP-042, RISK-015]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B13
  execution_mode: goal_driven
  plan_doc: docs/architecture/workstreams/b13-universal-xlsx-plan.md
  prompt_pack_dir: .codex/agents/generated/b13-universal-xlsx
  stage_ledger: docs/architecture/workstreams/b13-universal-xlsx-stage-reports/b13-universal-xlsx-stage-ledger.md
  stage_id: S00
  predecessor_gate: {stage_id: null, allowed_statuses: []}
  state_preconditions: [B10 B11 and B12 are accepted, B13 is explicitly activated, final block contracts are frozen, this outline is detailed]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b13-universal-xlsx, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S01, unlock_on: accepted, authority: stage_ledger}
---

# B13 S00 — Discovery outline

Intended outcome: inventory final ReportSnapshot/entity schemas, renderer
capabilities, chart parity, Excel limits, workbook libraries, temp/artifact
storage, permissions, injection risks, supported applications, and proof gaps.

Detail sources, owners, hashes, B06/B08/B09 soft schema inputs, checks, and stop
gates before execution. Expected result: S00 report and only S01 authorized.
