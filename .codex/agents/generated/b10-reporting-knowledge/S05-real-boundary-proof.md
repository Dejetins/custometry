---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b10-s05-real-boundary-proof
scope: "Prove B10 cross-render, dashboard permission, Data Guide security, user-email, provider reconciliation, export, resource, and recovery behavior."
spec_version: 0.8.2-draft
requirement_ids: [AC-032, TEST-INV-039, TEST-INV-048, V1-AC-004, V1-AC-008, V1-AC-009, V1-AC-010, V1-AC-015]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B10
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/b10-reporting-knowledge-plan.md
  prompt_pack_dir: .codex/agents/generated/b10-reporting-knowledge
  stage_ledger: docs/architecture/workstreams/b10-reporting-knowledge-stage-reports/b10-reporting-knowledge-stage-ledger.md
  stage_id: S05
  predecessor_gate: {stage_id: S04, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S04 is accepted, target renderer mail sandbox database and browser boundaries are available, B10 is active for S05]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b10-reporting-knowledge, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S06, unlock_on: accepted, authority: stage_ledger}
---

# B10 S05 — Real-boundary proof outline

Intended outcome: reproducible Web/email/export snapshot totals, guide
sanitization/drift, sender/domain/PII negatives, mail artifact, idempotent
delivery, unknown provider reconciliation, bounded export, cancellation,
resource, recovery, API, and browser evidence.

Detail fixtures, destinations, commands, hashes, measurements, cleanup, and
stop gates before execution. Expected result: S05 receipts and only S06
authorized.
