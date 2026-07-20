---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.3-draft
ticket_id: W15-INGESTION-DQ-SEMANTIC-VERTICAL-SLICE
status: draft
workstream_id: W15
summary: Deliver one restart-safe retail extraction through immutable artifacts, required data-quality evidence, and a published Customer/Receipt/ReceiptItem/Product semantic dataset.
requirement_ids: [UC-002, UC-003, INGEST-001, INGEST-002, INGEST-003, INGEST-004, INGEST-005, INGEST-006, INGEST-007]
blockers: [W14-SOURCE-CONNECTION-FILE-IMPORT-KERNEL]
context_sources: [AGENTS.md, .codex/AGENTS.md, custometry-technical-blueprint-ru.md, custometry-technical-blueprint-human-ru.md, docs/architecture/system-design.md, docs/architecture/bounded-context-map.md, tests/golden/retail-demo-manifest.json]
change_scope:
  allowed_write_paths: [.codex/delivery/tickets/W15-INGESTION-DQ-SEMANTIC-VERTICAL-SLICE.md, .codex/delivery/evidence/W15-INGESTION-DQ-SEMANTIC-VERTICAL-SLICE.md, packages/artifacts/**, packages/execution/**, packages/ingestion/**, packages/data_quality/**, packages/semantic_model/**, apps/worker_data/**, packages/contracts/data_pipeline/**, pyproject.toml, uv.lock, migrations/versions/*_data_pipeline.py, tests/unit/data_pipeline/**, tests/contract/data_pipeline/**, tests/integration/data_pipeline/**]
  forbidden_write_paths: [custometry-technical-blueprint-ru.md, custometry-technical-blueprint-human-ru.md, custometry-ui-blueprint-ru.md, apps/web/**, packages/contracts/routes/**, packages/analytics_core/**, packages/analytics_customer/**, packages/analytics_sales/**]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy: {allowed_within_scope: true, retest_invalidated_evidence: true}
validation:
  depth: integration
  proof_skills: [backend-quality-gates]
  commands: [focused domain invariant and artifact contract tests, real PostgreSQL plus filesystem artifact integration, clean extraction and retry idempotency, forced crash and watermark non-advance, required DQ pass fail and waiver boundaries, semantic publication and impact evidence, migration lifecycle and DDD gates, uv run python -m tools.check --scope local, git diff --check]
  proof_boundary: retail-source-to-immutable-artifact-dq-and-semantic-publication
  evidence_target: .codex/delivery/evidence/W15-INGESTION-DQ-SEMANTIC-VERTICAL-SLICE.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: []
---

# Outcome

The deterministic retail source produces committed, reproducible artifacts and
a governed semantic dataset only after required DQ evidence succeeds.

# Non-goals

- Do not implement analytics, forecasting, remote workers, object storage, or
  browser UI.

# Work and repair boundary

Preserve PostgreSQL state truth, transactional outbox/fencing semantics, atomic
artifact commit, and owner-context boundaries.

# Acceptance evidence

Requires real database/filesystem observation, failure and restart paths,
watermark integrity, DQ and semantic publication proof, not source tests alone.
