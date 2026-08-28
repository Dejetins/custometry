---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.10.0-draft
ticket_id: W38-EXECUTION-TERMINAL-NOTIFICATION-EVENT
status: accepted
workstream_id: W38
summary: Publish and prove additive versioned redacted Execution terminal notification events through a public duplicate-safe outbox port without changing W36 command delivery or persistence schema.
requirement_ids: [EXEC-STATE-001, EXEC-STATE-002, EXEC-STATE-003, EXEC-STATE-006, EXEC-STATE-007, NOTIFY-002, NOTIFY-003, NOTIFY-004, NOTIFY-005, RBAC-002]
blockers: []
context_sources: [AGENTS.md, .codex/AGENTS.md, .codex/delivery/tickets/W36-EXECUTION-CONTROL-OPERATOR-API.md, .codex/delivery/evidence/W36-EXECUTION-CONTROL-OPERATOR-API.md, .codex/delivery/tickets/W37-INAPP-NOTIFICATION-INBOX-API.md, .codex/delivery/evidence/W37-INAPP-NOTIFICATION-INBOX-API.md, .codex/delivery/specs/in-app-notification-inbox.md, docs/architecture/bounded-context-map.md, docs/architecture/tooling-gates.md]
change_scope:
  allowed_write_paths: [.codex/delivery/tickets/W38-EXECUTION-TERMINAL-NOTIFICATION-EVENT.md, .codex/delivery/evidence/W38-EXECUTION-TERMINAL-NOTIFICATION-EVENT.md, packages/execution/**, packages/contracts/execution/**, packages/contracts/schemas/execution-terminal-event.schema.json, packages/contracts/src/execution-terminal-events.ts, tests/unit/execution_control/**, tests/contract/execution_control/**, tests/integration/execution_control/**]
  forbidden_write_paths: [.codex/delivery/tickets/W37-INAPP-NOTIFICATION-INBOX-API.md, .codex/delivery/evidence/W37-INAPP-NOTIFICATION-INBOX-API.md, packages/notifications/**, apps/api/src/custometry_api/notifications/**, apps/api/src/custometry_api/main.py, packages/contracts/notifications/**, packages/contracts/openapi/notifications.openapi.json, packages/contracts/schemas/notification-event.schema.json, packages/contracts/src/notifications.ts, migrations/**, apps/web/**, deploy/**]
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy: {allowed_within_scope: true, retest_invalidated_evidence: true}
validation:
  depth: runtime
  proof_skills: [contract-impact-analysis, backend-quality-gates]
  commands: [focused execution terminal event contract producer dedupe redaction lineage and command separation tests, deterministic execution terminal event JSON Schema and generated consumer drift tests, real disposable PostgreSQL failed stuck and recovered lifecycle outbox observation through the public event port, negative non-relevant transition tenant isolation duplicate and command dispatcher regression tests, existing W36 execution-control regression, uv run --locked python -m tools.custometry_quality.validate_migration_lifecycle --mode static, uv run --locked python -m tools.custometry_quality.check_ddd_boundaries, uv run --locked python -m tools.custometry_quality.check_contract_drift, source scripts/activate-toolchain.sh && uv run --locked python -m tools.check --scope local, git diff --check]
  proof_boundary: execution-terminal-notification-event-postgresql-outbox-public-port-and-command-separation
  evidence_target: .codex/delivery/evidence/W38-EXECUTION-TERMINAL-NOTIFICATION-EVENT.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: [.codex/delivery/evidence/W38-EXECUTION-TERMINAL-NOTIFICATION-EVENT.md]
---

# Outcome

Execution Control transactionally publishes additive, versioned and redacted
failed, stuck and recovered lifecycle events through a public outbox port that
Notifications can consume without private-table access, while the accepted W36
worker command path remains isolated and unchanged in meaning.

# Non-goals

- Do not implement the Notifications projection/API, Web inbox, email/webhook,
  a new migration, publication, deployment, or production delivery.
- Do not change W37 artifacts or claim that W37 is ready or accepted.

# Work and repair boundary

Extend only the accepted Execution Control package, its public contracts and
focused tests. Reuse the existing W36 JSONB outbox schema with distinct event
identities and query paths. Event consumers must not import Execution private
tables, and the worker dispatcher must never receive domain-event rows.

# Acceptance evidence

Evidence observes real PostgreSQL atomic event persistence for failed, stuck
and recovered outcomes, absence for irrelevant transitions, duplicate-safe
identity, tenant/lineage/redaction invariants, public claim/ack/release behavior,
command/event separation, generated schema/consumer drift, and the unchanged
W36 API, command outbox, idempotency, fencing, cancellation and reconciliation
regression. It excludes W37 completion, browser, Compose, recovery, performance,
release, deployment and production readiness.
