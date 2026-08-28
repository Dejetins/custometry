---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.10.0-draft
ticket_id: W37-INAPP-NOTIFICATION-INBOX-API
status: accepted
workstream_id: W37
summary: Publish and prove the permission-filtered in-app inbox API with duplicate-safe event projection, locale-neutral content, acknowledgement persistence, safe deep links, and audit.
requirement_ids: [NOTIFY-001, NOTIFY-002, NOTIFY-003, NOTIFY-004, NOTIFY-005, NOTIFY-007, NOTIFY-008, RBAC-002]
blockers: []
context_sources: [AGENTS.md, .codex/AGENTS.md, .codex/delivery/specs/in-app-notification-inbox.md, custometry-technical-blueprint-ru.md, custometry-technical-blueprint-human-ru.md, custometry-ui-blueprint-ru.md, docs/architecture/system-design.md, docs/architecture/bounded-context-map.md, packages/contracts/routes/ui-route-contracts.json, .codex/delivery/tickets/W36-EXECUTION-CONTROL-OPERATOR-API.md]
change_scope:
  allowed_write_paths: [.codex/delivery/tickets/W37-INAPP-NOTIFICATION-INBOX-API.md, .codex/delivery/evidence/W37-INAPP-NOTIFICATION-INBOX-API.md, packages/notifications/**, apps/api/src/custometry_api/notifications/**, apps/api/src/custometry_api/main.py, apps/api/src/custometry_api/config.py, apps/api/pyproject.toml, packages/contracts/notifications/**, packages/contracts/openapi/**, packages/contracts/schemas/**, packages/contracts/src/**, docs/contracts/contract-drift.json, pyproject.toml, uv.lock, migrations/versions/*_notifications.py, tests/unit/notifications/**, tests/contract/notifications/**, tests/integration/notifications/**]
  forbidden_write_paths: [custometry-technical-blueprint-ru.md, custometry-technical-blueprint-human-ru.md, custometry-ui-blueprint-ru.md, apps/web/**, packages/contracts/routes/**, packages/execution/**, apps/api/src/custometry_api/runs/**, deploy/**]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy: {allowed_within_scope: true, retest_invalidated_evidence: true}
validation:
  depth: api
  proof_skills: [contract-impact-analysis, backend-quality-gates]
  commands: [focused notification projection state dedupe authorization deep-link locale and audit tests, generated OpenAPI event and consumer contract drift tests, real PostgreSQL migration and persistence lifecycle, authenticated API positive and negative visibility tests, repeated out-of-order W36 outbox event projection and access-revocation integration, uv run python -m tools.custometry_quality.check_ddd_boundaries, uv run python -m tools.custometry_quality.check_contract_drift, source scripts/activate-toolchain.sh && uv run python -m tools.check --scope local, git diff --check]
  proof_boundary: permission-filtered-inapp-inbox-api-postgresql-outbox-projection-revocation-and-audit
  evidence_target: .codex/delivery/evidence/W37-INAPP-NOTIFICATION-INBOX-API.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: [.codex/delivery/evidence/W37-INAPP-NOTIFICATION-INBOX-API.md]
---

# Outcome

Authenticated users receive only currently authorized locale-neutral in-app
notifications and can read, dismiss, or acknowledge them through typed APIs
whose PostgreSQL state, duplicate/out-of-order event projection, safe deep links,
revocation behavior, and required audit are observed.

# Non-goals

- Do not implement the Web inbox, preference editor, email/webhook channels,
  report email, external delivery endpoints, publication, or deployment.
- Do not claim browser, Compose, recovery, performance, release, or production
  readiness from API and integration proof.

# Work and repair boundary

Own only Notifications domain/application code, API adapters, contracts, owned
migrations, and focused tests. Consume W36 and Identity/Audit through public
events and ports; never read their private tables. Shared composition files may
change only through safely separable hunks after W36 is accepted.

# Acceptance evidence

Evidence covers additive contract compatibility, real PostgreSQL persistence,
authenticated visibility and count suppression, duplicate/out-of-order event
convergence, access revocation, locale invariance, acknowledgement idempotency,
safe deep links, and redacted audit. It explicitly excludes browser,
email/webhook, Compose, recovery, performance, release, deployment, and
production boundaries.
