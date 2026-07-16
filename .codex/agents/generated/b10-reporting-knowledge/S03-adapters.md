---
artifact_kind: stage_prompt
staged_schema_version: 1
prompt_name: b10-s03-adapters
scope: "Implement B10 PostgreSQL, artifact, renderer, Markdown, mail, export, outbox, and provider-reconciliation adapters."
spec_version: 0.8.2-draft
requirement_ids: [REPORT-MAIL-001, REPORT-MAIL-002, REPORT-MAIL-003, REPORT-MAIL-004, REPORT-MAIL-005, REPORT-MAIL-006, REPORT-MAIL-007, REPORT-MAIL-008, REPORT-MAIL-009, REPORT-MAIL-010, REPORT-MAIL-011, TEST-INV-036, TEST-INV-037]
prompt_pack_execution:
  staged_schema_version: 1
  readiness: outline
  enabled: false
  workstream_id: B10
  execution_mode: manual_sequential
  plan_doc: docs/architecture/workstreams/b10-reporting-knowledge-plan.md
  prompt_pack_dir: .codex/agents/generated/b10-reporting-knowledge
  stage_ledger: docs/architecture/workstreams/b10-reporting-knowledge-stage-reports/b10-reporting-knowledge-stage-ledger.md
  stage_id: S03
  predecessor_gate: {stage_id: S02, allowed_statuses: [accepted, superseded]}
  state_preconditions: [S02 is accepted, renderer and mail sandbox contracts are available, B10 is active for S03]
  required_source_hashes: {}
  branch_policy: {default_branch: main, separate_branch_requested: true, allowed_branch: codex/b10-reporting-knowledge, per_stage_branches: forbidden}
  next_stage_rule: {candidate_stage: S04, unlock_on: accepted, authority: stage_ledger}
---

# B10 S03 — Adapters outline

Intended outcome: real snapshot persistence/artifacts, SSR SVG to PNG, safe
Markdown, verified sender/domain/PII, mail sandbox, bounded CSV/Parquet/JSON,
idempotency, unknown-provider reconciliation, migrations, and API evidence.

Detail exact destinations, secrets, retries, timeouts, cleanup, and real tests
before execution. Expected result: S03 evidence and only S04 authorized.
