---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b08-s02-domain-application
scope: "Implement B08 framework-independent customer intelligence, segmentation, cohort, lifecycle, promotion, and audience policies."
spec_version: 0.8.2-draft
requirement_ids: [TEST-INV-002, TEST-INV-035]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B08
  execution_mode: goal_driven
  plan_doc: docs/architecture/workstreams/b08-customer-intelligence-promotion-journal-plan.md
  prompt_pack_dir: .codex/agents/generated/b08-customer-intelligence-promotion-journal
  stage_ledger: docs/architecture/workstreams/b08-customer-intelligence-promotion-journal-stage-reports/b08-customer-intelligence-promotion-journal-stage-ledger.md
  stage_id: S02
  predecessor_gate: {stage_id: S01, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S01 contracts are accepted, domain ownership is resolved, B08 is active for S02]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b08-customer-intelligence-promotion-journal, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S03, unlock_on: accepted, authority: stage_ledger}
---

# B08 S02 — Domain and application outline

Intended outcome: pure version lifecycle, segment snapshot, cohort/lifecycle,
promotion overlap, audience pinning, permission, idempotency, and non-causal
overlay policies with property tests.

Activation detailing must name exact packages, invariants, negative cases, and
focused gates. Expected result: framework-free evidence, contract
classification, S02 report, and only S03 unlocked.
