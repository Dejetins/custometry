---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b08-s06-acceptance
scope: "Reconcile B08 requirements, evidence, contracts, migrations, rollback, documentation, cold review, and milestone readiness."
spec_version: 0.8.2-draft
requirement_ids: [V1-AC-003, V1-AC-014]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B08
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/b08-customer-intelligence-promotion-journal-plan.md
  prompt_pack_dir: .codex/agents/generated/b08-customer-intelligence-promotion-journal
  stage_ledger: docs/architecture/workstreams/b08-customer-intelligence-promotion-journal-stage-reports/b08-customer-intelligence-promotion-journal-stage-ledger.md
  stage_id: S06
  predecessor_gate: {stage_id: S05, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S05 is accepted, all stage evidence is current, an independent cold reviewer is available, B08 is active for S06]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b08-customer-intelligence-promotion-journal, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: null, unlock_on: accepted, authority: stage_ledger}
---

# B08 S06 — Acceptance outline

Intended outcome: complete matrix traceability, current evidence, contract and
migration review, rollback/docs, independent verdict, and an honest public-MVP
or v1 milestone decision.

Detail this prompt after S05. Expected result: an English acceptance report and
a completed ledger only when no required blocker remains.
