---
artifact_kind: delivery_spec
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.10.0-draft
status: accepted
---

# Operator Runs API and Execution Control Specification

## Problem and user-visible outcome

The accepted architecture assigns run state, node attempts, outbox delivery,
leases/fencing, retry, cancellation, reconciliation, and progress to Execution
Control, but the current delivery frontier has no bounded backend unit that
makes those semantics consumable by `UI-OPS-001`.

An authorized workspace operator or resource owner can query a policy-filtered
run list and queue summary, distinguish queued, running, succeeded, failed, and
cancelling work, and issue an idempotent cancel or explicit manual retry through
an authenticated API. PostgreSQL remains the state truth. Valkey or a worker
delivery backend may transport tasks but cannot determine terminal state.

## API, authorization, and projection contract

The backend unit publishes versioned OpenAPI and generated-client contracts for:

- a workspace-scoped run list with bounded pagination and allowlisted filters
  for state, execution kind, owner, time range, and safe trace identity;
- a queue summary with state/lane counts, oldest queued age, observation time,
  and explicit stale/degraded status rather than invented real-time precision;
- an idempotent cancel command that returns the current durable run state and
  never moves a terminal run to `CANCELLING`;
- an explicit manual retry command that selects failed-node retry or full rerun,
  requires an audit reason, and creates a new run/node execution identity with
  `retry_of_id` rather than mutating terminal history.

Every request resolves actor, workspace, effective policy version, request ID,
and contract version. `run.read` is required before list or detail projection;
`run.cancel`, `run.retry`, and where applicable `run.create` are checked for the
specific action and resource. Owner access never exceeds current workspace,
object, row/column, or PII ceilings. Authorization is evaluated before fetch,
count, filtering, pagination, or mutation so hidden run existence, titles,
inputs, artifacts, failures, or counts are not leaked. Operator projections use
safe codes/parameters and redacted trace references, never source values,
secrets, raw PII, arbitrary logs, or artifact content.

Repeatable mutations require a workspace/actor/route-scoped idempotency key and
payload hash. A mismatched replay fails with a stable conflict error. Compare-
and-set uses current state/revision; invalid transitions return a stable error
code and the safe current state. API timeouts do not invent cancellation or
retry success: a follow-up query resolves the PostgreSQL truth.

## Persistence, transitions, and runtime invariants

Execution Control owns its PostgreSQL schema, repositories, migrations, run and
node-attempt histories, outbox intents, leases/fencing tokens, retry ancestry,
and reconciliation findings. Cross-context consumers use public command/status/
progress ports and never query those private tables.

- Run transitions follow `CREATED -> VALIDATING -> QUEUED -> RUNNING` and the
  accepted terminal/partial rules; cancellation remains `CANCELLING` until
  active attempts stop or are fenced and cleanup policy completes.
- Terminal state is immutable. Automatic pre-terminal retry creates a new
  attempt; manual terminal retry creates a new execution record.
- Each transition persists previous/new state, revision, actor or service,
  occurred-at time, reason code, and request ID in the same owner transaction
  as the durable state and required audit/outbox intent.
- At-least-once delivery is duplicate-safe. Only the current fencing token may
  publish progress, artifacts, or terminal state. Reconciliation repairs lost
  delivery, expired leases, incomplete commits, and unfinished aggregate state.
- Queue summaries and progress are explicit projections with freshness; cache
  or Valkey loss may degrade them but cannot replace durable run state.

## Invariants, failure behavior, and non-goals

- Empty is a successful authorized query with no visible runs; forbidden,
  stale/degraded, dependency unavailable, and failed are distinct outcomes.
- Cancelling an already terminal run is an idempotent no-op returning its
  terminal state. Retry of an ineligible state or node fails without mutation.
- Audit failure policy is decided before the business side effect. Required
  audit intent and the mutation commit atomically or the mutation fails.
- The unit does not implement the Operator Center Web UI, pipelines/schedules,
  arbitrary log download, artifact browsing, runtime-health administration,
  notification inbox, publication, deployment, or production operations.
- It does not claim complete worker/runtime or recovery readiness from API and
  source tests. Real worker-stop/fencing and redelivery observations remain
  mandatory at the ticket boundary.

## Test and proof seam

Acceptance requires focused domain/property tests plus generated-contract and
consumer tests, a real PostgreSQL migration lifecycle, authenticated API
positive/negative visibility tests, duplicate idempotency replay, concurrent
compare-and-set races, and a disposable Valkey/outbox/worker exercise that
observes cancel, fencing, retry ancestry, lost-delivery reconciliation, and
terminal immutability. Evidence must separate API/persistence proof from the
disposable worker boundary and exclude Compose, recovery, performance, release,
deployment, and production readiness.

## Compatibility and decisions

- Public API, DTO, port, and generated-client surfaces: `compatible-change`
  as additive versioned contracts before a stable operator API consumer.
- Persisted schema and execution identity: `compatible-change` requiring owned
  migrations and rollback proof; terminal records are never rewritten.
- Config/defaults, cache keys, and request hashes: `compatible-change` where
  new execution/idempotency identities are added; current identity/access
  contracts remain unchanged.
- Service-call auth/error and side-effect idempotency semantics:
  `compatible-change`, with deny-before-fetch and explicit unknown-state rules.
- Browser-visible behavior: `none` in the backend unit; W34 owns that boundary.

No new product or bounded-context authority is required: the specification is
a delivery projection of the accepted product blueprint, System Design,
bounded-context map, and executable route contract. Exact OpenAPI component
names and physical table names remain implementation decisions inside these
invariants.
