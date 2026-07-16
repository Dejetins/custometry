---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: w14-s04-browser-acceptance
scope: "Verify complete W14 browser, localization, accessibility, email, export, administration, system-surface, and navigation journeys."
spec_version: 0.8.2-draft
requirement_ids: [AC-033, AC-034, AC-035, AC-036, AC-037, AC-038, AC-039, AC-040]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: W14
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/w14-final-acceptance-plan.md
  prompt_pack_dir: .codex/agents/generated/w14-final-acceptance
  stage_ledger: docs/architecture/workstreams/w14-final-acceptance-stage-reports/w14-final-acceptance-stage-ledger.md
  stage_id: S04
  predecessor_gate: {stage_id: S03, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S03 is accepted, release browser environments and supported locales are available, W14 is active for S04]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/w14-final-acceptance, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S05, unlock_on: accepted, authority: stage_ledger}
---

# W14 S04 — Browser acceptance outline

Intended outcome: end-to-end English/Russian, keyboard, screen-reader,
responsive, reduced-motion, routing/history, Focus/Explore, docs/help, system
surfaces, analytics, forecasts, operations, reports, email, and XLSX evidence
with clean console/network and permission negatives.

Detail exact journeys, devices, accessibility method, traces/screenshots, and
owner rerun rules before execution.
