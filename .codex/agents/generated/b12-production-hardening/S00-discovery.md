---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b12-s00-discovery
scope: "Discover B12 target topology, threats, secrets, recovery, supply chain, performance, operations, evidence, and milestone gaps."
spec_version: 0.8.2-draft
requirement_ids: [GAP-017, GAP-018, GAP-019, RISK-008]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B12
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/b12-production-hardening-plan.md
  prompt_pack_dir: .codex/agents/generated/b12-production-hardening
  stage_ledger: docs/architecture/workstreams/b12-production-hardening-stage-reports/b12-production-hardening-stage-ledger.md
  stage_id: S00
  predecessor_gate: {stage_id: null, allowed_statuses: []}
  state_preconditions: [B01 through B10 slices are accepted, B12 is explicitly activated, release targets are identified, this outline is detailed]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b12-production-hardening, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S01, unlock_on: accepted, authority: stage_ledger}
---

# B12 S00 — Discovery outline

Intended outcome: source-anchored inventory of target hosts/topology, threat
model, secrets, auth, data, networks, Edge/Web/API, upgrades, backup/restore,
recovery, supply chain, licenses, performance, capacity, admin/ops, evidence
freshness, and public-MVP/v1 gaps.

Detail owners, targets, matrix rows, hashes, severity, B11 soft-gate behavior,
checks, and stop gates before execution.
