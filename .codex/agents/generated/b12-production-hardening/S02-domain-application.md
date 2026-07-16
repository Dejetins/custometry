---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b12-s02-domain-application
scope: "Implement B12 framework-independent security, retention, limit, compatibility, evidence, capacity, and release-gate policies."
spec_version: 0.8.2-draft
requirement_ids: [SCALE-001, SCALE-002, SCALE-003, SCALE-004, OPS-001, OPS-002, OPS-003, OPS-004]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B12
  execution_mode: goal_driven
  plan_doc: docs/architecture/workstreams/b12-production-hardening-plan.md
  prompt_pack_dir: .codex/agents/generated/b12-production-hardening
  stage_ledger: docs/architecture/workstreams/b12-production-hardening-stage-reports/b12-production-hardening-stage-ledger.md
  stage_id: S02
  predecessor_gate: {stage_id: S01, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S01 is accepted, target and evidence contracts are frozen, B12 is active for S02]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b12-production-hardening, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S03, unlock_on: accepted, authority: stage_ledger}
---

# B12 S02 — Domain and application outline

Intended outcome: pure policy/validator logic for configuration, secrets
references, permissions, retention, resources, topology, evidence expiry,
upgrade compatibility, recovery objectives, severity, and milestone gates.

Detail exact modules, invariants, property tests, and stop gates before
execution. Expected result: S02 report and only S03 authorized.
