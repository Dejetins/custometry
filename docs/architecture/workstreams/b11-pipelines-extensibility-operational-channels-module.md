---
artifact_kind: module_definition
staged_schema_version: 1
doc_id: MODULE-B11-PIPELINES-EXTENSIBILITY-OPERATIONAL-CHANNELS
title: B11 Pipelines, Extensibility and Operational Channels module definition
doc_version: 1
product_spec_version: 0.8.2-draft
visibility: internal
ship: false
workstream_id: B11
owner: platform-extensibility
status: initial
requirement_ids: [GAP-020, NOTIFY-006, NOTIFY-008, NOTIFY-009, NOTIFY-010, NOTIFY-011, NOTIFY-012, NOTIFY-013, NOTIFY-014, NOTIFY-015, RISK-004, RISK-007, SEC-006, TEST-INV-029, UC-006]
proof_boundary:
  label: planned-b11-module-boundary
  exclusions: [public-mvp-email-webhook, user-report-email, arbitrary-plugin-trust, implemented-production-channels, release-readiness]
---

# B11 Pipelines, Extensibility and Operational Channels — module definition

## Purpose and release boundary

B11 adds the common-engine pipeline canvas, trusted plugin contracts,
administrator lifecycle, and v1 operational delivery adapters for email and
webhook. It begins after the public-MVP product slice: public MVP keeps
operational delivery in-app only. B11 must not retroactively make email or
webhook a public-MVP dependency.

User-initiated report email belongs to B10 and remains distinct from
operational notification delivery.

## Ubiquitous language

| Term | Meaning |
|---|---|
| Pipeline definition version | Immutable normalized graph executed by the common engine |
| Guided equivalence | Guided form and canvas compile to the same normalized specification |
| Node contract | Versioned input/output/config/capability contract |
| Plugin manifest | Signed/approved compatibility, permissions, resources, and entrypoint metadata |
| Trusted server plugin | Administrator-installed code inside the declared trust boundary |
| Operational event | Auditable system event eligible for channel routing |
| Channel policy | Workspace/admin rules for in-app, email, and webhook delivery |
| Delivery attempt | Persisted idempotent adapter invocation and result |
| Webhook endpoint version | Immutable URL/security/retry/signature policy version |

## Domain model and invariants

- Guided and canvas definitions produce one normalized execution
  specification and identical result identity.
- Pipeline nodes reference versioned contracts; unknown or incompatible nodes
  fail before execution.
- Plugin installation, enablement, upgrade, disablement, and removal are
  administrator-audited lifecycle transitions.
- Plugins receive explicit capabilities, resources, secrets references, and
  network policy; no ambient trust is assumed.
- Public MVP activates only in-app operational delivery.
- Operational email/webhook endpoints and adapters remain disabled until the
  v1 target slice and explicit B11/B12 gates.
- Delivery pins endpoint version, deduplicates by persisted identity, bounds
  retries/timeouts, verifies webhook signatures, and enforces SSRF policy.
- Unknown delivery state is reconciled; retries are not blind.
- Channel delivery cannot expand event or PII permissions.
- B10 user report email and B11 operational email have separate commands,
  sender policy, templates, audit semantics, and queues.

## Commands, queries, and events

Commands create/publish pipeline definitions, validate graphs, manage plugins,
manage channel endpoints/policies, and deliver/reconcile operational events.
Queries return definitions, validation, plugin compatibility/lifecycle,
channel health, delivery attempts, and safe endpoint metadata.

Events include pipeline published, plugin lifecycle changed, endpoint changed,
operational delivery queued/submitted/succeeded/failed/unknown, and channel
disabled. All are versioned, workspace-scoped, audited, and redacted.

## Ports and dependencies

- B04 supplies execution, node lifecycle, artifacts, outbox, fencing,
  cancellation, and progress.
- B07 supplies operational events/in-app inbox and operator workflows.
- B10 supplies report/snapshot references that may trigger operational
  notices, but B11 does not send user report email.
- B05/B08/B09 are soft contract consumers/providers for nodes.
- B03 supplies administrator/workspace permissions, secrets references, API
  tokens, and audit.
- B12 supplies production network, security, recovery, and channel hardening
  before final v1 acceptance.

Pipeline/plugin/channel domains do not import concrete scheduler, HTTP, SMTP,
webhook, secret-store, or UI frameworks.

## Persistence, security, and operations

PostgreSQL stores pipeline definitions/versions, normalized specs, node
bindings, plugin manifests/installations, endpoint versions, channel policies,
delivery identities/attempts, reconciliation state, and audit references.

Endpoint secrets use secret references and never appear in manifests/logs.
Webhook validation covers DNS/IP changes, redirects, private/link-local
targets, signatures, replay, payload bounds, and timeouts. Plugin supply-chain,
compatibility, resource, and uninstall/rollback evidence is mandatory.

## UI and acceptance

Owned surfaces include pipeline canvas/validation, plugin management,
operational channel settings, endpoint test/status, delivery attempts, and
reconciliation. Canvas actions have keyboard alternatives. UI uses B01
components and B07 operational patterns.

B11 hard-depends on B04, B07, and B10; B05/B08/B09 are soft. Completion
requires normalized-equivalence tests, real common-engine execution, plugin
lifecycle/sandbox proof, email/webhook sandbox evidence, SSRF/signature/retry/
unknown-state tests, browser/accessibility proof, B12 hardening handoff, cold
review, and all routed requirements reconciled.
