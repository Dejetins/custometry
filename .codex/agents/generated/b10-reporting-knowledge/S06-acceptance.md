---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b10-s06-acceptance
scope: "Reconcile B10 requirements, evidence, cross-render contracts, email effects, guides, exports, migrations, rollback, B11/B13 handoffs, and cold review."
spec_version: 0.8.2-draft
requirement_ids: [AC-026, AC-032, V1-AC-004, V1-AC-008, V1-AC-009, V1-AC-010, V1-AC-015]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B10
  execution_mode: goal_driven
  plan_doc: docs/architecture/workstreams/b10-reporting-knowledge-plan.md
  prompt_pack_dir: .codex/agents/generated/b10-reporting-knowledge
  stage_ledger: docs/architecture/workstreams/b10-reporting-knowledge-stage-reports/b10-reporting-knowledge-stage-ledger.md
  stage_id: S06
  predecessor_gate: {stage_id: S05, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S05 is accepted, all evidence is current, B11 and B13 consumer boundaries are explicit, an independent reviewer is available, B10 is active for S06]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b10-reporting-knowledge, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: null, unlock_on: accepted, authority: stage_ledger}
---

# B10 S06 — Acceptance outline

Intended outcome: complete traceability, current real evidence, contract/
migration/rollback/docs review, external-effect audit, explicit B11 operational
channel and B13 XLSX handoffs, and independent verdict.

Detail after S05. Expected result: completed ledger only with no required
blocker and no claim that B11 or B13 is complete.
