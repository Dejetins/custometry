---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b08-s05-real-boundary-proof
scope: "Prove B08 end-to-end customer/segment/promotion behavior, immutable audiences, overlap, permissions, timelines, scale, and recovery."
spec_version: 0.8.2-draft
requirement_ids: [TEST-INV-045, V1-AC-003, V1-AC-014]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B08
  execution_mode: goal_driven
  plan_doc: docs/architecture/workstreams/b08-customer-intelligence-promotion-journal-plan.md
  prompt_pack_dir: .codex/agents/generated/b08-customer-intelligence-promotion-journal
  stage_ledger: docs/architecture/workstreams/b08-customer-intelligence-promotion-journal-stage-reports/b08-customer-intelligence-promotion-journal-stage-ledger.md
  stage_id: S05
  predecessor_gate: {stage_id: S04, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S04 is accepted, target data/runtime/browser environments are available, B08 is active for S05]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b08-customer-intelligence-promotion-journal, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S06, unlock_on: accepted, authority: stage_ledger}
---

# B08 S05 — Real-boundary proof outline

Intended outcome: reproducible database, artifact, API, browser, permission,
overlap, pinned-audience, range-timeline, concurrency, failure, and recovery
evidence on the accepted target profile.

Detail exact fixtures, commands, resource bounds, cleanup, hashes, and stop
gates before execution. Expected result: redacted S05 receipts and only S06
unlocked.
