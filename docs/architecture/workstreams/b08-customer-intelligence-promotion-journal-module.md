---
artifact_kind: module_definition
staged_schema_version: 1
doc_id: MODULE-B08-CUSTOMER-INTELLIGENCE-PROMOTION-JOURNAL
title: B08 Customer Intelligence and Promotion Journal module definition
doc_version: 1
product_spec_version: 0.8.2-draft
visibility: internal
ship: false
workstream_id: B08
owner: customer-intelligence
status: initial
requirement_ids: [CHART-007, CHART-008, GAP-038, GAP-049, PROMO-001, PROMO-002, PROMO-003, PROMO-004, PROMO-005, PROMO-006, PROMO-007, PROMO-008, PROMO-009, RISK-012, TEST-INV-002, TEST-INV-035, TEST-INV-045, UC-013, V1-AC-003, V1-AC-014]
proof_boundary:
  label: planned-b08-module-boundary
  exclusions: [implemented-customer-marts, implemented-segmentation, implemented-promotion-journal, causal-uplift-claims, release-readiness]
---

# B08 Customer Intelligence and Promotion Journal — module definition

> This file defines ownership and contracts. It is not evidence that customer
> intelligence, promotion versions, audience snapshots, charts, or timelines
> are implemented.

## Purpose and boundaries

B08 turns B05-governed customer and transaction semantics plus B06 reportable
analytics into customer intelligence and an auditable promotion journal. It
owns customer overview, lifecycle, cohorts, RFM/segment snapshots, and
immutable promotion versions with planned/actual time ranges, channel scope,
client scope, and pinned audiences.

It does not own:

- canonical source ingestion, identity mapping, metrics, or DQ rules from B05;
- run/artifact execution from B04;
- baseline or expanded forecasting from B06/B09;
- ReportSnapshot delivery and user email from B10;
- operational notification channels from B07/B11;
- causal attribution or uplift claims unless a future approved context adds a
  defensible causal design.

## Ubiquitous language

| Term | Meaning |
|---|---|
| Customer intelligence view | Versioned analysis over canonical customer and sales artifacts |
| Segment definition | Reusable versioned predicate and feature contract |
| Segment snapshot | Immutable membership result at an explicit as-of date |
| Lifecycle state | Registered customer-state classification with versioned rules |
| Cohort | Explicit population and anchor-period definition |
| Promotion | Stable business identity across versions |
| Promotion version | Immutable campaign definition valid for one revision |
| Planned range | Intended start/end interval |
| Actual range | Observed start/end interval recorded separately |
| Channel scope | One or more explicit sales channels |
| Client scope | One or more governed client/customer-account scopes |
| Audience reference | Pinned segment snapshot or immutable customer-list version |
| Promotion overlay | Non-causal visual annotation on analytics |

## Domain model and invariants

- `CustomerAnalysisSpec` references canonical feature/metric versions, filters,
  as-of date, comparison policy, and output grain.
- `SegmentDefinitionVersion` is immutable after publication.
- `SegmentSnapshot` stores definition version, source artifacts, as-of date,
  canonical customer key, membership grain, and lineage.
- `CohortDefinitionVersion` freezes population, anchor event, calendar,
  timezone, filters, and metric versions.
- `PromotionVersion` freezes name, status, planned/actual ranges, channel/client
  scopes, audience reference, budget/metadata policy, and revision lineage.
- A promotion may have multiple channels and clients; no single-channel or
  single-client shortcut is canonical.
- Audience membership is pinned to an immutable segment snapshot or
  customer-list version and cannot drift with a live segment.
- Overlapping promotions remain distinct and visible.
- Planned and actual ranges never overwrite one another.
- Timeline projection uses `range_timeline` and preserves visible-window,
  overlap, audience, and permission semantics.
- Promotion overlays never label correlation as causal effect.
- Customer and segment artifacts use `canonical_customer_id`, explicit primary
  keys, workspace scope, and as-of lineage.

## Commands, queries, and events

| Contract | Result |
|---|---|
| Create/publish segment definition | Immutable definition version |
| Materialize segment snapshot | Immutable membership artifact |
| Build customer/cohort/lifecycle view | Reportable artifact with lineage |
| Create/revise promotion | New immutable promotion version |
| Record actual range | New audited version; planned range retained |
| Bind audience | Pinned segment snapshot or customer-list version |
| Query promotion timeline | Permission-filtered range projection |
| Overlay promotions on report | Non-causal ChartSpec/range timeline binding |

All mutating commands require workspace/actor context, optimistic concurrency,
idempotency, audit, and stable locale-neutral error codes.

## Ports and dependencies

Inbound ports expose customer intelligence queries, segment lifecycle,
promotion lifecycle, audience binding, and timeline projection. Outbound ports
consume:

- B05 canonical customer/sales marts, MetricRegistry, filters, and DQ status;
- B04 execution, immutable artifacts, progress, and cancellation;
- B06 ChartSpec, comparison, Result Trust, and reportable-block contracts;
- B03 workspace, permissions, actor context, and audit;
- B01 route, localization, accessibility, and Focus/Explore presentation;
- B07 operational state as a soft integration only.

B08 publishes versioned customer/segment/promotion contracts for B09/B10/B13.
It never reads private tables owned by another context directly.

## Persistence and artifacts

Owned metadata includes segment definitions/versions, segment snapshot
metadata, cohort/lifecycle definitions, promotion identities/versions,
channel/client scopes, pinned audience references, and audit links. Large
memberships and analytical outputs are immutable artifacts, not unbounded
PostgreSQL blobs.

All collections are bounded/paginated. Published versions are immutable.
Deletion is policy-governed archival; referenced versions cannot disappear
silently.

## UI and evidence

Owned surfaces include customer overview, RFM/segments, cohorts, lifecycle,
promotion list/detail/editor, and promotion timeline. They use the shared Frost
system, compact analytics headers, `vs LY`, searchable typed filters,
Result Trust, chart/table switching, and route-backed Focus/Explore.

Acceptance requires real API/database/browser evidence, keyboard/accessibility
checks, overlap and permission fixtures, immutable-audience proof, and
non-causal labeling. Penpot is a design source, never implementation evidence.

## Contract impact

Initial contracts are `compatible-change`. After first published consumers:

- changing canonical customer key, membership grain, audience identity,
  version immutability, range semantics, channel/client scope, or overlay
  meaning is breaking;
- adding optional metadata is compatible only when permissions, lineage, and
  existing hashes remain stable;
- a causal result is a separate future contract, not an additive label.

## Activation and acceptance

B08 hard-depends on B01, B03, B04, B05, and B06; B07 is soft. Activation waits
for those hard dependencies and an explicit ledger gate. Completion requires
all S00–S06 evidence, matrix traceability, migrations/rollback, independent
cold review, and no unresolved public-MVP or v1 blocker.
