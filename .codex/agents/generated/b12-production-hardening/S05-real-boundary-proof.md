---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b12-s05-real-boundary-proof
scope: "Prove the B01-B10 public-MVP release candidate across install, upgrade, recovery, security, supply chain, performance, operations, and target network boundaries."
spec_version: 0.8.2-draft
requirement_ids: [AC-014, AC-015, AC-034, OPS-005, OPS-006, OPS-007, OPS-008, TEST-INV-025, TEST-INV-046, V1-AC-013]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B12
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/b12-production-hardening-plan.md
  prompt_pack_dir: .codex/agents/generated/b12-production-hardening
  stage_ledger: docs/architecture/workstreams/b12-production-hardening-stage-reports/b12-production-hardening-stage-ledger.md
  stage_id: S05
  predecessor_gate: {stage_id: S04, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S04 is accepted, B01 through B10 evidence is current, immutable release candidate and target identities are authorized, B12 is active for S05]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b12-production-hardening, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S06, unlock_on: accepted, authority: stage_ledger}
---

# B12 S05 — Public-MVP real-boundary proof outline

Intended outcome: target install/upgrade, database/artifact backup/restore,
security, workspace/PII isolation, Edge-Web-API and firewall/CNI baseline,
supply-chain, benchmark/soak/capacity, operations, browser, rollback, and
cleanup evidence for B01–B10.

B11 operational email/webhook is excluded from this public-MVP checkpoint.
Detail immutable identities, commands, receipts, severity, rerun/expiry, and
go/no-go rules before execution.
