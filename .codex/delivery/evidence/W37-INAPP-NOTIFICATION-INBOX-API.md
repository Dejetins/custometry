---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.10.0-draft
ticket_id: W37-INAPP-NOTIFICATION-INBOX-API
proof_boundary: permission-filtered-inapp-inbox-api-postgresql-outbox-projection-revocation-and-audit
proof_skills: [contract-impact-analysis, backend-quality-gates]
verdict: passed
redaction: Disposable PostgreSQL credentials, container identity and port, connection strings, process identifiers, raw event/provider payloads, arbitrary worker reason text, and temporary secret paths were not retained. Observations contain only stable codes, safe counts, public contract fields, commands, commits, and repository paths.
executed_checks:
  - git fetch origin --prune and verify exact HEAD 1255247c65639fe1a44644617365f56b464ba1cb, parent 7b30c53a1d0b44afd79a29a2796ed8dd37445319, origin/main 68ad124ac6c7400c67df8bdd75752fe1bd350e76, accepted/passed W36 and W38 ancestry, clean W38 paths, and W37-only dirty paths
  - source scripts/activate-toolchain.sh and uv run --locked ruff check packages/contracts/notifications packages/notifications apps/api/src/custometry_api/notifications apps/api/src/custometry_api/main.py migrations/versions/0009_notifications.py tests/unit/notifications tests/contract/notifications tests/integration/notifications
  - source scripts/activate-toolchain.sh and uv run --locked pyright packages/contracts/notifications packages/notifications apps/api/src/custometry_api/notifications tests/unit/notifications tests/contract/notifications tests/integration/notifications
  - source scripts/activate-toolchain.sh and uv run --locked --package custometry-api pytest -q tests/unit/notifications tests/contract/notifications tests/integration/notifications -rs
  - source scripts/activate-toolchain.sh and uv run --locked --package custometry-api pytest -q tests/contract tests/unit/notifications tests/integration/notifications -rs
  - uv run --locked python -m tools.custometry_quality.validate_repository_layout
  - uv run --locked python -m tools.custometry_quality.validate_migration_lifecycle --mode static
  - uv run --locked python -m tools.custometry_quality.check_ddd_boundaries
  - uv run --locked python -m tools.custometry_quality.check_contract_drift
  - uv run --locked python -m tools.custometry_quality.validate_delivery_contract
  - uv run --locked python -m tools.custometry_quality.validate_delivery_tickets
  - source scripts/activate-toolchain.sh and uv run --locked python -m tools.check --scope local
  - git diff --check
observations:
  - >-
    Repair history: the first W37 execution stopped truthfully because accepted W36 exposed only
    execute/cancel command delivery and no public terminal event producer.
    W38-EXECUTION-TERMINAL-NOTIFICATION-EVENT resolved that exact blocker in accepted commit
    1255247c65639fe1a44644617365f56b464ba1cb with passed evidence at
    execution-terminal-notification-event-postgresql-outbox-public-port-and-command-separation.
  - W37 was minimally re-readied by removing only the obsolete blocker_record; requirement IDs, scope, non-goals, acceptance commands, proof boundary, and evidence target were not expanded.
  - Focused Notifications Ruff and strict Pyright passed; Pyright reported zero errors, warnings, or information diagnostics. Focused unit, generated-contract, real PostgreSQL, authenticated API, projection, state, revocation, locale, deep-link, idempotency, and audit tests passed 12 tests without skips.
  - The broader repository contract plus W37 unit and real-boundary regression passed 36 tests without skips.
  - Real disposable PostgreSQL 17.5 applied revisions 0001 through 0009 on an empty database, repeated head upgrade, downgraded to 0008_execution_control while preserving W36 state and removing Notifications tables, then re-upgraded to 0009_notifications.
  - Real W38 lifecycle publication produced stuck, failed, and recovered ExecutionTerminalEvent records transactionally in the accepted W36 execution_outbox. W37 claimed exactly those events through ExecutionTerminalEventOutboxPort and mapped only the public DTO through its Notifications-owned anti-corruption adapter; W37 production code imports no Execution domain, infrastructure, repository, or table.
  - Execute/retry command rows coexisted in the W36 outbox, while the public terminal-event claim returned only execution.run.stuck, execution.run.failed, and execution.run.recovered events. The recovered event was projected before its older failure, released, reclaimed with the same event identity, and replayed; projection converged to one resolved two-event group without duplicate lineage.
  - Event-to-projection mapping preserves workspace/resource/run/attempt/retry lineage, stable source type/version, severity, locale-neutral message/reason/status codes, bounded group identity, safe UI-OPS-002 route parameters, and trace identity. It rejects inconsistent W38 event invariants before recipient resolution.
  - Authenticated positive and negative API cases observed deny-before-store for notification.read, hidden-row and unread-count suppression before pagination/aggregation, workspace/recipient isolation, safe unavailable deep links, immediate query-time access revoke, and no future projection when recipient eligibility was revoked.
  - English and Russian requests returned the same event/projection identity and locale-neutral code/parameters. Rendered copy, locale, email, secrets, raw PII, source values, arbitrary URLs, and provider payloads are excluded from event and API contracts.
  - Read, dismissed, acknowledged, and resolved remain separate durable meanings. Read/dismiss/acknowledge commands use revision CAS and scoped idempotency; same-payload replay returns current state, mismatched replay fails with IDEMPOTENCY_CONFLICT, and repeated recovered-event delivery preserves resolved state.
  - Critical acknowledgement and dismissal wrote only redacted audit intents containing action, workspace, actor, notification, reason code, request ID, and time; no message body, email, provider payload, secret, or resource content was retained.
  - Generated notifications.openapi.json, notification-event.schema.json, and notifications.ts byte-matched their deterministic generator. Repository layout, nine-revision migration graph, 22-context DDD boundaries, registered contract drift, delivery contract/tickets, grouped local, and whitespace checks passed.
  - >-
    Contract impact is compatible-change: the independently versioned Notifications HTTP API,
    public event/recipient/access/audit DTOs and ports, generated OpenAPI/JSON Schema/TypeScript
    consumer, additive 0009_notifications schema, projection/dedupe/group/idempotency identities,
    fail-closed authorization, and redacted audit semantics are additive. Existing W36/W38 APIs,
    producer event/command behavior, config defaults, request hashes, cache keys, route contracts,
    alert/runbook semantics, and browser-visible behavior are unchanged.
---

# W37 In-App Notification Inbox API Evidence

## Outcome and scope

- outcome: authenticated users can query only currently authorized,
  locale-neutral in-app notifications, obtain a visibility-filtered unread
  count and safe deep link, and idempotently read, dismiss, or acknowledge an
  item whose projection and audit lifecycle are durable in PostgreSQL;
- dependency closure: accepted W38 commit
  `1255247c65639fe1a44644617365f56b464ba1cb` supplies the public versioned
  terminal-event producer/port absent during the first blocked W37 attempt;
- requirement IDs: [NOTIFY-001, NOTIFY-002, NOTIFY-003, NOTIFY-004,
  NOTIFY-005, NOTIFY-007, NOTIFY-008, RBAC-002];
- included: Notifications domain/application/infrastructure, independently
  mounted API, generated OpenAPI/event/TypeScript contracts, revision
  `0009_notifications`, real W38 producer-to-W37 projection, authorization,
  state/idempotency, safe-link, locale-neutral and redacted-audit proof;
- exclusions: no Web inbox, preferences editor, email/webhook, Compose,
  recovery drill, performance benchmark, release, deployment, or production
  readiness claim.

## Commands and observations

| Command or action | Result | Redacted observation / durable reference |
|---|---|---|
| Focused Ruff and strict Pyright | pass | All W37 production/API/contracts/migration/tests passed lint; Pyright reported 0 diagnostics. |
| `uv run --locked --package custometry-api pytest -q tests/unit/notifications tests/contract/notifications tests/integration/notifications -rs` | pass | 12 passed, no skip; includes real PostgreSQL 0009 lifecycle and W38 event intake. |
| `uv run --locked --package custometry-api pytest -q tests/contract tests/unit/notifications tests/integration/notifications -rs` | pass | 36 passed, no skip. |
| Generated contract assertions | pass | `notifications.openapi.json`, `notification-event.schema.json`, and `notifications.ts` byte-match deterministic sources. |
| Real migration lifecycle | pass | Empty/repeat head, downgrade to `0008_execution_control`, W36 preservation, Notifications removal, and re-upgrade to `0009_notifications` passed. |
| Real W38 producer to W37 projection | pass | Public-port failure/stuck/recovered intake, command separation, repeat/reclaim, out-of-order convergence and resolved replay passed without private Execution-table reads. |
| Authorization, state and audit integration | pass | Visibility/count suppression, workspace/recipient isolation, revoke, locale, safe link, read/dismiss/acknowledge/resolved idempotency and redacted audit passed. |
| Repository layout, migration static, DDD and contract drift | pass | Layout is valid; nine revisions and 22 contexts passed; registered and focused generated contracts are synchronized. |
| Delivery contract/ticket validators | pass | W37 terminal evidence and accepted dependency frontier validate. |
| `source scripts/activate-toolchain.sh && uv run --locked python -m tools.check --scope local` | pass | Canonical bounded-handoff profile passed on the completed W37 tree. |
| `git diff --check` | pass | No whitespace errors. |

## Contract impact

Overall classification is `compatible-change`. Public API, DTO/event/port,
generated consumer, persisted schema, projection identity, dedupe/group and
idempotency semantics, authorization failure behavior, and redacted audit
intent are additive. Configuration/defaults, request hashes/cache keys,
existing W36/W38 behavior, alert/runbook semantics, route contracts, and
browser-visible behavior are `none`. No breaking or unknown dimension remains
inside the declared W37 boundary.

## Verdict

`passed` at
`permission-filtered-inapp-inbox-api-postgresql-outbox-projection-revocation-and-audit`.
The previously blocked producer seam is now observed end to end from accepted
W38 transactional publication through its public event port into the W37
PostgreSQL projection and authenticated API. Browser, email/webhook, Compose,
recovery, performance, release, deployment, and production boundaries remain
unproven and out of scope.
