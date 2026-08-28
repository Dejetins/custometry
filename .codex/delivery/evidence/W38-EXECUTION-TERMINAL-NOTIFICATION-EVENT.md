---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.10.0-draft
ticket_id: W38-EXECUTION-TERMINAL-NOTIFICATION-EVENT
proof_boundary: execution-terminal-notification-event-postgresql-outbox-public-port-and-command-separation
proof_skills: [contract-impact-analysis, backend-quality-gates]
verdict: passed
redaction: Disposable PostgreSQL and Valkey credentials, container identities, ports, connection strings, process identifiers, raw provider payloads, arbitrary failure text, and temporary secret paths were not retained. Evidence records only stable codes, safe counts, commands, repository paths, and public contract fields.
executed_checks:
  - verify exact HEAD 7b30c53a1d0b44afd79a29a2796ed8dd37445319, origin/main 68ad124ac6c7400c67df8bdd75752fe1bd350e76, accepted/passed W36 ancestry, W37 blocker evidence, and unchanged W37 candidate hashes
  - source scripts/activate-toolchain.sh and uv run --locked python -m tools.custometry_quality.validate_delivery_tickets
  - uv run --locked ruff check packages/contracts/execution packages/execution/infrastructure/control_postgres.py tests/contract/execution_control tests/integration/execution_control/test_real_terminal_events.py
  - uv run --locked pyright packages/contracts/execution tests/contract/execution_control/test_execution_control_api_contract.py tests/integration/execution_control/test_real_terminal_events.py
  - uv run --locked pytest -q tests/contract/execution_control/test_execution_control_api_contract.py
  - uv run --locked pytest -q tests/integration/execution_control/test_real_terminal_events.py
  - uv run --locked pytest -q tests/unit/execution_control tests/contract/execution_control tests/integration/execution_control --ignore=tests/integration/execution_control/test_real_operator_api.py
  - uv run --locked pytest -q tests/integration/execution_control/test_real_operator_api.py -k 'not test_z_real_postgresql_migration_repeat_downgrade_and_reupgrade'
  - uv run --locked python -m tools.custometry_quality.validate_migration_lifecycle --mode static
  - uv run --locked python -m tools.custometry_quality.check_ddd_boundaries
  - uv run --locked python -m tools.custometry_quality.check_contract_drift
  - source scripts/activate-toolchain.sh and uv run --locked python -m tools.check --scope local
  - git diff --check
observations:
  - W38 generated-contract tests passed 4 tests; the focused real PostgreSQL failure, stuck, recovery, reconciliation, replay, redaction, lineage, public-port, and command-separation suite passed 4 tests without skips.
  - The broader Execution Control regression passed 15 focused tests plus 8 real W36 operator API, state, outbox, Valkey, cancellation, retry, fencing, concurrency, resource-boundary, and reconciliation tests without skips.
  - Real disposable PostgreSQL observed direct failure, expired-lease stuck retry, manual-retry recovery, and reconciler-derived terminal failure events in the durable W36 execution_outbox through the public ExecutionTerminalEventOutboxPort. State mutation or reconciliation repair and event insert share one transaction.
  - Event IDs are UUIDv5 identities over version, workspace, run, attempt, and event type. Repeated terminal publication retained one row and public release/reclaim returned the same event identity.
  - The worker command claim path selects only execute and cancel rows. The public event claim path selects only allowlisted event.execution.*.v1 rows, and command acknowledgement rejects an event row.
  - Failure, stuck, and recovered envelopes retain workspace/resource/run/attempt/retry lineage, stable status and reason codes, locale-neutral message code/parameters, a bounded UI-OPS-002 route descriptor, group identity, and safe trace identity.
  - Arbitrary worker reason text, rendered copy, raw PII, secrets, source values, provider payloads, safe title/remediation, report email, and arbitrary URLs are absent from the event DTO and generated JSON Schema.
  - Ordinary success and cancellation emitted no notification event. Failed and recovered manual-retry events converged on one group identity while preserving distinct immutable event IDs and immediate retry lineage.
  - No migration was added. Static validation passed the current nine-revision dirty-checkout graph, and W38 reuses the accepted W36 JSONB execution_outbox lifecycle.
  - The accepted W36 migration-head assertion was not rerun because the preserved foreign W37 candidate adds uncommitted 0009_notifications.py and would truthfully change the dirty-checkout head. The W36 production regression and W38 real PostgreSQL lifecycle were run separately instead.
  - Focused Pyright passed with zero errors. Mypy is not installed in the locked toolchain; it was not used as proof. Ruff, DDD, contract drift, grouped local, delivery validation, migration static validation, and diff checks passed.
  - >-
    Contract impact is compatible-change: the public Execution DTO/event/port, JSON Schema,
    generated TypeScript consumer, deterministic event identity, and at-least-once delivery
    semantics are additive. Existing W36 HTTP API, command outbox, idempotency, fencing,
    cancellation, reconciliation, persisted schema, configuration, request hashes, alert and
    runbook behavior, route contracts, and browser-visible behavior are unchanged.
---

# W38 Execution Terminal Notification Event Evidence

## Outcome and scope

- outcome: Execution Control transactionally persists additive versioned,
  locale-neutral, redacted failure, stuck, and recovery events in the accepted
  W36 outbox and exposes them through a public duplicate-safe port without
  exposing private Execution tables to Notifications;
- requirement IDs: [EXEC-STATE-001, EXEC-STATE-002, EXEC-STATE-003,
  EXEC-STATE-006, EXEC-STATE-007, NOTIFY-002, NOTIFY-003, NOTIFY-004,
  NOTIFY-005, RBAC-002];
- included: public Python event DTO/port, deterministic JSON Schema and
  TypeScript consumer, failure/stuck/recovered producer seams, stable event and
  group identity, W36 outbox reuse, and explicit worker command/event query and
  acknowledgement separation;
- exclusions: no W37 projection/API/migration mutation, Web inbox, email,
  webhook, Compose, recovery drill, performance benchmark, release,
  deployment, or production proof.

## Commands and observations

| Command or action | Result | Redacted observation / durable reference |
|---|---|---|
| Focused Ruff and Pyright | pass | Ruff passed; focused Pyright reported 0 errors, warnings, or information diagnostics. |
| `uv run --locked pytest -q tests/contract/execution_control/test_execution_control_api_contract.py` | pass | 4 passed; generated event schema and TypeScript consumer byte-match their deterministic generator. |
| `uv run --locked pytest -q tests/integration/execution_control/test_real_terminal_events.py` | pass | 4 passed against disposable PostgreSQL; no skips. |
| Focused Execution Control regression | pass | 15 passed outside the W36 API file; the W36 API selection passed 8 with its dirty-head migration assertion deselected. |
| `uv run --locked python -m tools.custometry_quality.validate_migration_lifecycle --mode static` | pass | Current nine-revision dirty-checkout graph is valid; W38 adds no migration. |
| `uv run --locked python -m tools.custometry_quality.check_ddd_boundaries` | pass | 22 bounded contexts; no cross-context private-table consumer was added. |
| `uv run --locked python -m tools.custometry_quality.check_contract_drift` | pass | Registered repository contracts remain synchronized; W38 has focused deterministic drift assertions. |
| `source scripts/activate-toolchain.sh && uv run --locked python -m tools.check --scope local` | pass | Canonical grouped local profile passed on the combined preserved W37 plus W38 tree. |
| `git diff --check` | pass | No whitespace errors. |

## Contract impact

`compatible-change`. The event DTO, public port, JSON Schema, generated
TypeScript consumer, stable event/dedupe identity, and external at-least-once
delivery semantics are additive. Persisted schema, configuration/defaults,
request hashes, existing command identity, W36 authorization/error semantics,
alert/runbook behavior, UI route contracts, and browser-visible behavior are
`none`. No breaking or unknown dimension remains inside the W38 boundary.

## Verdict

`passed` at
`execution-terminal-notification-event-postgresql-outbox-public-port-and-command-separation`.
This proves a real local PostgreSQL producer/outbox/public-port seam for W37 to
consume next. It does not prove W37 projection completion, browser behavior,
email/webhook delivery, Compose, recovery, performance, release, deployment,
or production readiness.
