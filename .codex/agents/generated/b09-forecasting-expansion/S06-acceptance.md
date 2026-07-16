---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b09-s06-acceptance
scope: "Reconcile B09 requirements, evidence, model/spec contracts, migrations, rollback, monitoring, docs, and cold review."
spec_version: 0.8.2-draft
requirement_ids: [AC-038, TEST-INV-030]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B09
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/b09-forecasting-expansion-plan.md
  prompt_pack_dir: .codex/agents/generated/b09-forecasting-expansion
  stage_ledger: docs/architecture/workstreams/b09-forecasting-expansion-stage-reports/b09-forecasting-expansion-stage-ledger.md
  stage_id: S06
  predecessor_gate: {stage_id: S05, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S05 is accepted, evidence matches final code and data identities, an independent reviewer is available, B09 is active for S06]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b09-forecasting-expansion, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: null, unlock_on: accepted, authority: stage_ledger}
---

# B09 S06 — Acceptance outline

Intended outcome: complete forecast requirement traceability, current real
evidence, contract/migration/rollback and monitoring review, documentation,
independent verdict, and honest milestone status.

Detail after S05. Expected result: acceptance report and completed ledger only
when no required blocker remains.
