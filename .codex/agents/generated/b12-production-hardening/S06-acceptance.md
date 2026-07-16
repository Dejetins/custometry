---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b12-s06-acceptance
scope: "Require accepted B11, re-prove affected hardening, reconcile B12 v1 evidence, residual risks, rollback, documentation, and cold review."
spec_version: 0.8.2-draft
requirement_ids: [AC-034, TEST-INV-046, TEST-INV-052, V1-AC-019]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B12
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/b12-production-hardening-plan.md
  prompt_pack_dir: .codex/agents/generated/b12-production-hardening
  stage_ledger: docs/architecture/workstreams/b12-production-hardening-stage-reports/b12-production-hardening-stage-ledger.md
  stage_id: S06
  predecessor_gate: {stage_id: S05, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S05 public-MVP proof is accepted, B11 is accepted, all plugin email webhook affected evidence is refreshed, an independent reviewer is available, B12 is active for S06]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b12-production-hardening, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: null, unlock_on: accepted, authority: stage_ledger}
---

# B12 S06 — Final v1 hardening acceptance outline

Intended outcome: B11-gated re-hardening of plugins and operational channels,
complete v1 security/recovery/supply-chain/performance/operations traceability,
current target evidence, rollback/docs, residual-risk decision, and independent
verdict.

Detail after B11 and S05. Expected result: completed B12 ledger only when no
critical/high or required evidence blocker remains.
