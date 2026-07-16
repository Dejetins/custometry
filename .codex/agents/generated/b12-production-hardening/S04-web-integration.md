---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b12-s04-web-integration
scope: "Integrate B12 administration, service health, workers/queues, storage, backup/restore, audit, limits, maintenance, and system surfaces."
spec_version: 0.8.2-draft
requirement_ids: [ADMIN-002, ADMIN-004, ADMIN-006, ADMIN-007, ADMIN-010, ADMIN-011, TEST-INV-052]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B12
  execution_mode: goal_driven
  plan_doc: docs/architecture/workstreams/b12-production-hardening-plan.md
  prompt_pack_dir: .codex/agents/generated/b12-production-hardening
  stage_ledger: docs/architecture/workstreams/b12-production-hardening-stage-reports/b12-production-hardening-stage-ledger.md
  stage_id: S04
  predecessor_gate: {stage_id: S03, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S03 is accepted, B01 and B07 admin/operations contracts are stable, B12 is active for S04]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b12-production-hardening, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S05, unlock_on: accepted, authority: stage_ledger}
---

# B12 S04 — Web integration outline

Intended outcome: safe accessible admin lifecycle, health, workers/queues,
outbox/reconciler, storage, backup/restore, limits, audit, maintenance, 403/404,
session-expired, maintenance, and upgrade-required surfaces.

Detail routes, permissions/redaction, reason codes, keyboard, responsive,
browser security, console/network, and visual QA before execution.
