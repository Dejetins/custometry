---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.10.0-draft
ticket_id: W36-EXECUTION-CONTROL-OPERATOR-API
status: accepted
workstream_id: W36
summary: Publish and prove the policy-filtered operator run query and command API over durable execution-control transitions, cancellation, retry, fencing, and reconciliation.
requirement_ids: [UC-010, EXEC-STATE-001, EXEC-STATE-002, EXEC-STATE-003, EXEC-STATE-004, EXEC-STATE-006, EXEC-STATE-007, EXEC-CANCEL-001, EXEC-CANCEL-003, EXEC-CANCEL-004, EXEC-CANCEL-005, EXEC-CANCEL-006, ADMIN-003, ADMIN-005, RBAC-002]
blockers: []
context_sources: [AGENTS.md, .codex/AGENTS.md, .codex/delivery/specs/operator-runs-api-and-execution-control.md, custometry-technical-blueprint-ru.md, custometry-technical-blueprint-human-ru.md, custometry-ui-blueprint-ru.md, docs/architecture/system-design.md, docs/architecture/bounded-context-map.md, packages/contracts/routes/ui-route-contracts.json, .codex/delivery/tickets/W15-INGESTION-DQ-SEMANTIC-VERTICAL-SLICE.md]
change_scope:
  allowed_write_paths: [.codex/delivery/tickets/W36-EXECUTION-CONTROL-OPERATOR-API.md, .codex/delivery/evidence/W36-EXECUTION-CONTROL-OPERATOR-API.md, packages/execution/**, apps/api/src/custometry_api/runs/**, apps/api/src/custometry_api/main.py, apps/api/src/custometry_api/config.py, apps/api/pyproject.toml, packages/contracts/execution/**, packages/contracts/openapi/**, packages/contracts/schemas/**, packages/contracts/src/**, docs/contracts/contract-drift.json, pyproject.toml, uv.lock, migrations/versions/*_execution_control.py, tests/unit/execution_control/**, tests/contract/execution_control/**, tests/integration/execution_control/**]
  forbidden_write_paths: [custometry-technical-blueprint-ru.md, custometry-technical-blueprint-human-ru.md, custometry-ui-blueprint-ru.md, apps/web/**, packages/contracts/routes/**, packages/notifications/**, apps/api/src/custometry_api/notifications/**, deploy/**]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy: {allowed_within_scope: true, retest_invalidated_evidence: true}
validation:
  depth: runtime
  proof_skills: [contract-impact-analysis, backend-quality-gates]
  commands: [focused execution state transition cancellation retry authorization and idempotency tests, generated OpenAPI and consumer contract drift tests, real PostgreSQL migration and concurrency lifecycle, authenticated API positive and negative visibility tests, disposable Valkey outbox worker fencing cancellation retry and reconciliation exercise, uv run python -m tools.custometry_quality.check_ddd_boundaries, uv run python -m tools.custometry_quality.check_contract_drift, source scripts/activate-toolchain.sh && uv run python -m tools.check --scope local, git diff --check]
  proof_boundary: policy-filtered-operator-run-api-postgresql-state-outbox-and-disposable-worker-cancel-retry-reconciliation
  evidence_target: .codex/delivery/evidence/W36-EXECUTION-CONTROL-OPERATOR-API.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: [.codex/delivery/evidence/W36-EXECUTION-CONTROL-OPERATOR-API.md]
---

# Outcome

Authorized operators and resource owners can list visible runs and queue state,
then cancel or manually retry eligible work through typed contracts whose
durable PostgreSQL transitions, audit reasons, attempt ancestry, idempotency,
fencing, and reconciliation are observed at a disposable worker boundary.

# Non-goals

- Do not implement Web UI, schedules/pipeline editing, notification inbox,
  arbitrary log or artifact content access, publication, or deployment.
- Do not claim Compose, recovery, performance, release, or production-runtime
  readiness from this bounded disposable integration.

# Work and repair boundary

Extend only the accepted W15 execution-control kernel and its public API,
contracts, owned migrations, and focused tests. Preserve owner-context table
privacy and use public authorization/audit ports. Shared composition files may
change only through safely separable hunks after W15 is accepted.

# Acceptance evidence

Evidence covers API/DTO compatibility, deny-before-fetch/count behavior,
transition and terminal-state invariants, cancel/retry idempotency, concurrency,
real PostgreSQL persistence, and disposable outbox/Valkey/worker fencing and
reconciliation. It states the exact unproven Compose, recovery, performance,
release, deployment, and production boundaries.
