---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b11-s01-ux-contract
scope: "Freeze B11 pipeline, node, plugin, endpoint, channel, delivery, API, UI, security, error, and lifecycle contracts."
spec_version: 0.8.2-draft
requirement_ids: [NOTIFY-006, NOTIFY-008, NOTIFY-009, NOTIFY-010, NOTIFY-011, NOTIFY-012, NOTIFY-013, NOTIFY-014, NOTIFY-015]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B11
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/b11-pipelines-extensibility-operational-channels-plan.md
  prompt_pack_dir: .codex/agents/generated/b11-pipelines-extensibility-operational-channels
  stage_ledger: docs/architecture/workstreams/b11-pipelines-extensibility-operational-channels-stage-reports/b11-pipelines-extensibility-operational-channels-stage-ledger.md
  stage_id: S01
  predecessor_gate: {stage_id: S00, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S00 is accepted, B04 B07 and B10 contracts are stable, B11 is active for S01]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b11-pipelines-extensibility-operational-channels, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S02, unlock_on: accepted, authority: stage_ledger}
---

# B11 S01 — UX and contract outline

Intended outcome: normalized pipeline/node/plugin and channel schemas,
administrator lifecycle, endpoint versions, in-app-only MVP gate, email/webhook
v1 policy, signatures, SSRF, retries, reconciliation, permissions, APIs/errors,
and accessible journeys.

Detail examples, compatibility, migration, security, and gates after S00.
Expected result: S01 evidence and only S02 authorized.
