---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b10-s00-discovery
scope: "Discover B10 dashboard, ReportSnapshot, renderer, Data Guide, user-email, export, permissions, ownership, and evidence gaps."
spec_version: 0.8.2-draft
requirement_ids: [GAP-031, GAP-040, GAP-041, GAP-043, GAP-048, RISK-013, RISK-014, RISK-017, RISK-019, SEC-011, SEC-015]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B10
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/b10-reporting-knowledge-plan.md
  prompt_pack_dir: .codex/agents/generated/b10-reporting-knowledge
  stage_ledger: docs/architecture/workstreams/b10-reporting-knowledge-stage-reports/b10-reporting-knowledge-stage-ledger.md
  stage_id: S00
  predecessor_gate: {stage_id: null, allowed_statuses: []}
  state_preconditions: [B01 B03 B04 B05 B06 B07 B08 and B09 slices are accepted, B10 is explicitly activated, this outline is detailed against current sources]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b10-reporting-knowledge, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S01, unlock_on: accepted, authority: stage_ledger}
---

# B10 S00 — Discovery outline

Intended outcome: source-anchored inventory of reportable consumers, dashboard
and snapshot contracts, renderers, guides, sender/domain/PII policies,
mail/export adapters, Web flows, and B11/B13 boundaries.

Detail owners, matrix rows, hashes, checks, external effects, and stop gates
before activation. Expected result: S00 report and only S01 authorized.
