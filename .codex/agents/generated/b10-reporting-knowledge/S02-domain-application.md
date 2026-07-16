---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b10-s02-domain-application
scope: "Implement B10 snapshot resolution, binding, dashboard permission, Data Guide, and immutable knowledge policies."
spec_version: 0.8.2-draft
requirement_ids: [DATA-GUIDE-001, DATA-GUIDE-002, DATA-GUIDE-003, DATA-GUIDE-004, DATA-GUIDE-005, DATA-GUIDE-006, DATA-GUIDE-007, DATA-GUIDE-008, AC-026, TEST-INV-021]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B10
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/b10-reporting-knowledge-plan.md
  prompt_pack_dir: .codex/agents/generated/b10-reporting-knowledge
  stage_ledger: docs/architecture/workstreams/b10-reporting-knowledge-stage-reports/b10-reporting-knowledge-stage-ledger.md
  stage_id: S02
  predecessor_gate: {stage_id: S01, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S01 is accepted, snapshot guide and permission contracts are frozen, B10 is active for S02]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b10-reporting-knowledge, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S03, unlock_on: accepted, authority: stage_ledger}
---

# B10 S02 — Domain and application outline

Intended outcome: pure snapshot resolution, pinned/latest binding, permission
inheritance, guide version/review, sanitizer policy, recipient snapshot, and
delivery/export command policies.

Detail packages, invariants, security negatives, idempotency, and gates before
execution. Expected result: S02 report and only S03 authorized.
