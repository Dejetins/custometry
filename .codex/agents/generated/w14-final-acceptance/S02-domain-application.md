---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: w14-s02-contract-reconciliation
scope: "Reconcile W14 requirement rows, public and internal contracts, migrations, documentation, source identities, and evidence freshness."
spec_version: 0.8.2-draft
requirement_ids: [AC-017, AC-018, AC-019, AC-020, AC-021, AC-022, AC-023, AC-024]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: W14
  execution_mode: goal_driven
  plan_doc: docs/architecture/workstreams/w14-final-acceptance-plan.md
  prompt_pack_dir: .codex/agents/generated/w14-final-acceptance
  stage_ledger: docs/architecture/workstreams/w14-final-acceptance-stage-reports/w14-final-acceptance-stage-ledger.md
  stage_id: S02
  predecessor_gate: {stage_id: S01, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S01 is accepted, matrix and evidence schemas are frozen, W14 is active for S02]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/w14-final-acceptance, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S03, unlock_on: accepted, authority: stage_ledger}
---

# W14 S02 — Contract reconciliation outline

Intended outcome: exact AC/V1-AC dispositions, contract compatibility,
migrations/rollback, route/API/schema/event/artifact/config identities,
documentation visibility, evidence freshness, and owner-returned blockers.

W14 may correct acceptance records only. Missing feature or runtime behavior
returns to B01–B13. Expected result: S02 report and only S03 authorized.
