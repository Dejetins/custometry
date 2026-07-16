---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b11-s00-discovery
scope: "Discover B11 common-engine pipeline, plugin, operational-event, email/webhook, security, ownership, and evidence boundaries."
spec_version: 0.8.2-draft
requirement_ids: [GAP-020, RISK-004, RISK-007, SEC-006]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B11
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/b11-pipelines-extensibility-operational-channels-plan.md
  prompt_pack_dir: .codex/agents/generated/b11-pipelines-extensibility-operational-channels
  stage_ledger: docs/architecture/workstreams/b11-pipelines-extensibility-operational-channels-stage-reports/b11-pipelines-extensibility-operational-channels-stage-ledger.md
  stage_id: S00
  predecessor_gate: {stage_id: null, allowed_statuses: []}
  state_preconditions: [B04 B07 and B10 slices are accepted, public MVP in-app-only behavior is frozen, B11 is explicitly activated, this outline is detailed]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b11-pipelines-extensibility-operational-channels, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S01, unlock_on: accepted, authority: stage_ledger}
---

# B11 S00 — Discovery outline

Intended outcome: inventory common-engine/guided definitions, node/plugin
contracts, operational events/in-app inbox, B10 user-email boundary, outbound
channel adapters, secrets/network risks, and v1 evidence gaps.

Detail sources, owners, hashes, B05/B08/B09 soft contracts, checks, and stop
gates before execution. Expected result: S00 report and only S01 authorized.
