---
artifact_kind: delivery_spec
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.10.0-draft
status: accepted
---

# In-app Notification Inbox Specification

## Problem and user-visible outcome

The accepted architecture gives Notifications ownership of inbox projections,
preferences, acknowledgement/resolution, and operational delivery state, but
the current frontier has no backend unit for the `UI-NOTIFY-001` inbox slice.

An authenticated user can query only their currently authorized in-app
notifications across active workspace memberships, see a bounded unread count,
filter safe locale-neutral events, follow an authorized deep link, mark an item
read or dismissed, and acknowledge a critical item when permitted. Duplicate
source delivery does not create unbounded copies, and access revocation removes
the item from discovery even if a projection is temporarily stale.

## Event, API, and authorization contract

Notifications consumes versioned owner events through an outbox/event adapter.
The event envelope contains an event ID, source owner/type/version, workspace
and resource references, severity/category, occurred-at time, locale-neutral
message code and bounded typed parameters, dedupe/group identity, safe deep-link
route identity/parameters, and trace identity. It excludes rendered copy,
secrets, raw PII, source values, arbitrary provider payloads, and report email.

The backend unit publishes versioned OpenAPI and generated-client contracts for:

- the authenticated user's inbox with bounded pagination and allowlisted
  severity, category, read, dismissed, acknowledged, resolved, workspace, and
  time filters;
- an unread count derived from the same authorization-filtered projection;
- idempotent mark-read, dismiss, and acknowledgement commands with current
  state/revision responses and stable conflict/error semantics;
- a detail projection that returns only safe codes/parameters and an authorized
  deep-link descriptor, never pre-authorized resource content.

Recipient candidates are derived from current membership, role, ownership, and
enabled in-app category policy. Identity & Workspace authorization is rechecked
before projection, count, detail, acknowledgement, or deep-link disclosure.
Hidden resources and counts are removed before filtering, grouping, pagination,
and aggregation. A notification never grants resource access; navigation must
authorize the target again. `notification.read` governs the user's inbox and
`notification.acknowledge` governs acknowledgement. Administrative dismissal
and critical acknowledgement require durable audit intent.

The API returns locale-neutral codes and typed parameters. Web localizes them
using the current user locale with an English/system fallback. Changing locale
does not create a new event, projection identity, or acknowledgement record.

## Persistence, dedupe, and failure invariants

Notifications owns PostgreSQL inbox, recipient projection, state transition,
dedupe/group, preference-reference, and acknowledgement records plus its
migrations. Source domain state and Identity tables remain private to their
owners. Projection consumers record source event identity and tolerate
at-least-once delivery.

- Replaying the same event ID is idempotent. Related events may update a bounded
  group projection without erasing the immutable source-event lineage.
- Read, dismissed, acknowledged, and resolved are separate persisted meanings;
  an acknowledgement cannot be inferred from read state.
- State changes use revision/compare-and-set and idempotency identity. Replays
  return the durable current state; payload mismatch fails closed.
- Delayed projection exposes freshness/degraded status. Empty data is not used
  as a fallback for event intake, Identity, or PostgreSQL failure.
- Membership/resource revoke fails closed at query time and prevents future
  delivery. Reconciliation removes or suppresses now-ineligible projections
  without deleting audit or source-event lineage.
- Critical acknowledgement and administrative dismissal write a redacted audit
  record with actor, resource reference, reason code, request ID, and time.

## Invariants, failure behavior, and non-goals

- The unit implements only the public-MVP in-app inbox backend needed by W35.
  Per-category preference editing may consume the stored preference reference
  later but is not accepted by this slice.
- Email/webhook endpoints, delivery retries, signing, destination verification,
  report email, marketing campaigns, browser UI, publication, deployment, and
  production operations are excluded.
- Acknowledgement does not resolve the source incident or mutate the source
  bounded context. A source-owned resolution event may update the inbox view.
- Deep links use stable route identity and bounded parameters; unsafe or stale
  targets degrade to a safe unavailable state without leaking existence.

## Test and proof seam

Acceptance requires focused projection/state tests, generated-contract and
consumer tests, real PostgreSQL migration and persistence tests, authenticated
API positive/negative visibility tests, repeated and out-of-order outbox-event
delivery, dedupe/group convergence, membership/resource revocation, locale
switch invariance, deep-link authorization, acknowledgement idempotency, and
redacted audit evidence. A real W36 execution failure/recovery event is the
minimum cross-context producer proof. Evidence excludes browser, email/webhook,
Compose, recovery, performance, release, deployment, and production readiness.

## Compatibility and decisions

- Public API, DTO, event, port, and generated-client surfaces:
  `compatible-change` as additive versioned contracts before a stable inbox API
  consumer.
- Persisted schema and projection identity: `compatible-change` requiring owned
  migrations and replay/reconciliation proof.
- Config schema: `none` for this slice; channel enablement and external endpoint
  configuration are excluded.
- Request hash, dedupe, and persistence identity: `compatible-change`, with
  source event ID plus recipient/policy scope and explicit group identity.
- Service-call authorization/error and event-retry semantics:
  `compatible-change`, with deny-before-fetch, duplicate-safe intake, and no
  stale authorization fallback.
- Browser-visible behavior: `none` in the backend unit; W35 owns that boundary.

No new product or bounded-context authority is required. Exact OpenAPI
component names, table names, and safe code catalog layout remain implementation
decisions constrained by the accepted product, architecture, and route sources.
