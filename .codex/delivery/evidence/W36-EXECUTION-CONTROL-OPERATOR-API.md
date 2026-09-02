---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.10.0-draft
ticket_id: W36-EXECUTION-CONTROL-OPERATOR-API
proof_boundary: policy-filtered-operator-run-api-postgresql-state-outbox-and-disposable-worker-cancel-retry-reconciliation
proof_skills: [contract-impact-analysis, backend-quality-gates]
verdict: passed
redaction: Disposable PostgreSQL and Valkey credentials, container identities, ports, connection strings, process identifiers, raw task payloads, and temporary secret paths were not retained. Evidence records only pinned local images, safe counts, stable codes, commands, and repository paths.
executed_checks:
  - git fetch origin --prune and verify exact HEAD c7b5405809c1be9fbef637da865693f31e269a90, origin/main 68ad124ac6c7400c67df8bdd75752fe1bd350e76, clean checkout, W36 ready with no blockers, and accepted/passed W15 ancestry
  - uv lock and uv sync --locked --all-packages --all-groups
  - uv run --locked ruff check packages/contracts/execution packages/execution apps/api/src/custometry_api/runs apps/api/src/custometry_api/main.py apps/api/src/custometry_api/config.py migrations/versions/0008_execution_control.py tests/unit/execution_control tests/contract/execution_control tests/integration/execution_control
  - uv run --locked --package custometry-api pytest -q tests/unit/execution_control tests/contract/execution_control tests/integration/execution_control -rs
  - uv run --locked --package custometry-api pytest -q tests/unit/execution_control tests/contract tests/integration/execution_control tests/unit/data_pipeline tests/integration/data_pipeline -rs
  - uv run --locked python -m tools.custometry_quality.validate_migration_lifecycle --mode static
  - uv run python -m tools.custometry_quality.check_ddd_boundaries
  - uv run python -m tools.custometry_quality.check_contract_drift
  - source scripts/activate-toolchain.sh and uv run --locked python -m tools.check --scope local
  - git diff --check
observations:
  - W36 focused unit, generated-contract, real PostgreSQL, authenticated API, Valkey, outbox, worker, concurrency, cancellation, retry, fencing, reconciliation, and migration lifecycle suite passed 19 tests without skips.
  - Real disposable PostgreSQL 17.5 applied revisions 0001 through 0008 on an empty database, repeated head upgrade, downgraded to 0007, removed the W36 schema, and re-upgraded to 0008_execution_control.
  - Real disposable Valkey 8.0.1 carried execute, cancel, and retry delivery from the transactional outbox; workspace, policy, run, attempt, command, and delivery identity remained explicit and PostgreSQL remained the terminal-state truth.
  - The disposable Valkey fixture waits for the server readiness log before its first RESP handshake; the focused handoff rerun passed all 19 tests without a startup race.
  - Authorization failure occurred before store fetch/count; authenticated missing-token, invalid-token, missing-permission, owner-only, operator-wide, hidden-detail, and visible-count cases returned distinct stable outcomes.
  - Cancel remained CANCELLING until every active attempt was fenced and cleanup completed; stale worker completion failed with STALE_FENCING_TOKEN, terminal state stayed immutable, and same-payload replay returned current durable state while a changed-payload replay returned IDEMPOTENCY_CONFLICT.
  - Failed-node retry created a new run and attempt identity with run and attempt retry_of_id ancestry, retained terminal history, required an audit reason, and was delivered and claimed through the disposable Valkey worker boundary.
  - Reconciliation observed lost delivery, a stuck publishing commit, an expired lease, retry ancestry, stale-token rejection, and unfinished aggregate derivation; each repair wrote a durable finding.
  - A live PostgreSQL pg_sleep statement was cancelled through the psycopg driver before the isolated child process was hard-stopped, and the uncommitted-cleanup callback ran.
  - Resource-limit failure exposed only RESOURCE_LIMIT_EXCEEDED, observed/configured integer limits, and a safe remediation; arbitrary logs, inputs, artifacts, source values, secrets, and PII are absent from the API projection.
  - Generated execution-control OpenAPI and the generated TypeScript consumer manifest byte-matched their deterministic source; the repository-wide Foundation contract drift gate also remained green.
  - The broader contract plus W15 source regression passed 49 tests; five legacy W15 real-runtime tests were classified environmental skips because their external password-file variables were not configured. They were not used as W36 proof, whose self-contained real runtime suite passed without skips.
  - >-
    Contract impact is compatible-change: an additive independently versioned HTTP provider,
    additive public execution ports and DTOs, additive PostgreSQL revision 0008 with observed
    downgrade/re-upgrade, additive Valkey configuration defaults and redis dependency, and
    additive scoped idempotency/audit identities. No existing route, DTO, W15 execution claim,
    cache key, configuration default, or browser behavior was removed or redefined.
---

# W36 Execution Control Operator API Evidence

## Outcome and scope

- outcome: authorized operators can query a safe policy-filtered run list,
  detail/attempt ancestry, and state/lane queue summary, then issue idempotent
  cancel or manual retry commands whose durable state, audit history, outbox,
  fencing, cleanup, and reconciliation behavior were observed at disposable
  PostgreSQL, Valkey, and worker boundaries;
- requirement IDs: [UC-010, EXEC-STATE-001, EXEC-STATE-002, EXEC-STATE-003,
  EXEC-STATE-004, EXEC-STATE-006, EXEC-STATE-007, EXEC-CANCEL-001,
  EXEC-CANCEL-003, EXEC-CANCEL-004, EXEC-CANCEL-005, EXEC-CANCEL-006,
  ADMIN-003, ADMIN-005, RBAC-002];
- included: independently versioned `/execution` provider, generated OpenAPI
  and TypeScript consumer manifest, public execution contracts/ports, revision
  `0008_execution_control`, real PostgreSQL CAS/idempotency/audit/history,
  disposable Valkey delivery, isolated worker cancellation, retry ancestry,
  fencing, concurrency, and reconciliation;
- exclusions: no Web UI, route-contract change, schedule or pipeline editing,
  notification inbox, arbitrary log/artifact access, Compose lifecycle,
  recovery drill, performance benchmark, release, deployment, or production
  readiness claim.

## Commands and observations

| Command or action | Result | Redacted observation / durable reference |
|---|---|---|
| W36 focused Ruff command | pass | All W36 production, migration, contract, and test paths passed. |
| `uv run --locked --package custometry-api pytest -q tests/unit/execution_control tests/contract/execution_control tests/integration/execution_control -rs` | pass | 19 passed with no skip; real PostgreSQL and Valkey containers and an isolated cancellation process were observed. |
| Generated OpenAPI and consumer drift assertions | pass | `packages/contracts/openapi/execution-control.openapi.json` and `packages/contracts/src/execution-control.ts` byte-match the deterministic generator. |
| Real migration lifecycle inside the focused suite | pass | Empty upgrade, repeat, downgrade to `0007_contributor_projection`, and re-upgrade to `0008_execution_control` passed. |
| `uv run --locked python -m tools.custometry_quality.validate_migration_lifecycle --mode static` | pass | Eight-revision graph is valid. |
| `uv run python -m tools.custometry_quality.check_ddd_boundaries` | pass | 22 bounded contexts; application/domain dependency direction remains valid. |
| `uv run python -m tools.custometry_quality.check_contract_drift` | pass | Existing registered Foundation sources and generated consumer remain synchronized. |
| `source scripts/activate-toolchain.sh && uv run --locked python -m tools.check --scope local` | pass | Canonical bounded-handoff profile passed on the implementation tree. |
| `git diff --check` | pass | No whitespace errors. |

## Contract impact

`compatible-change` across public API, public ports, DTOs, persisted schema,
configuration, persistence/idempotency identity, service authorization/error
semantics, external delivery semantics, and operator audit/history reports.
The provider is additive and independently versioned; migration downgrade and
re-upgrade are observed. Alert/runbook and browser-visible behavior are `none`.
No breaking or unknown dimension remains inside the declared boundary.

## Verdict

`passed` at
`policy-filtered-operator-run-api-postgresql-state-outbox-and-disposable-worker-cancel-retry-reconciliation`.
The authenticated API proof injects the accepted Identity service port so W36
can exercise positive and negative current-policy actors without changing the
Identity-owned role catalog; W12 session persistence was not re-proved. Compose,
recovery, performance, release, deployment, production runtime, Web UI, and
notification delivery remain separate execution units.
