---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b12-s03-adapters
scope: "Implement B12 deployment, secrets, observability, backup/restore, upgrade, supply-chain, benchmark, and firewall/CNI proof adapters."
spec_version: 0.8.2-draft
requirement_ids: [AC-014, AC-015, AC-034, TEST-INV-025, CHART-019]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B12
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/b12-production-hardening-plan.md
  prompt_pack_dir: .codex/agents/generated/b12-production-hardening
  stage_ledger: docs/architecture/workstreams/b12-production-hardening-stage-reports/b12-production-hardening-stage-ledger.md
  stage_id: S03
  predecessor_gate: {stage_id: S02, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S02 is accepted, target infrastructure and safe test environments are authorized, B12 is active for S03]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b12-production-hardening, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S04, unlock_on: accepted, authority: stage_ledger}
---

# B12 S03 — Adapters outline

Intended outcome: real deploy/config/secrets/metrics/logs/traces/audit,
backup/restore, migration/upgrade, SBOM/license/provenance/vulnerability,
benchmark/soak, and target firewall/CNI evidence adapters.

Detail authority, target identities, external effects, destructive safeguards,
timeouts, rollback, cleanup, and real integration checks before execution.
