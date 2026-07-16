---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b12-s01-ux-contract
scope: "Freeze B12 security, deployment, recovery, supply-chain, performance, operational, system-surface, evidence, and release contracts."
spec_version: 0.8.2-draft
requirement_ids: [SEC-001, SEC-002, SEC-003, SEC-004, SEC-005, SEC-006, SEC-007, SEC-008, SEC-009, SEC-010, SEC-011, SEC-012, SEC-013, SEC-014, SEC-015, SEC-016, SEC-017, SEC-018]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B12
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/b12-production-hardening-plan.md
  prompt_pack_dir: .codex/agents/generated/b12-production-hardening
  stage_ledger: docs/architecture/workstreams/b12-production-hardening-stage-reports/b12-production-hardening-stage-ledger.md
  stage_id: S01
  predecessor_gate: {stage_id: S00, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S00 is accepted, target and release scopes are frozen, B12 is active for S01]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b12-production-hardening, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S02, unlock_on: accepted, authority: stage_ledger}
---

# B12 S01 — UX and contract outline

Intended outcome: versioned security/ops/deploy/upgrade/recovery/performance
profiles, evidence schemas, severity/rerun/expiry rules, admin/system journeys,
firewall/CNI requirement, and public-MVP versus v1 gates.

Detail exact target policies, compatibility, runbooks, receipts, and review
criteria after S00. Expected result: S01 evidence and only S02 authorized.
