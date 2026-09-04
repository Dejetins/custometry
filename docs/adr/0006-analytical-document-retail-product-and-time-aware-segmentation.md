---
doc_id: ADR-0006
title: Common analytical documents, time-aware segments, and retail product analytics
doc_version: 2
product_spec_version: 0.10.0-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: [GOAL-017, GOAL-018, ANALYTICAL-DOC-001, BLOCK-BUILDER-001, COLLAB-015, SEGMENT-019, DIGITAL-013, PRODUCT-ANALYTICS-001, MATERIALIZE-016]
status: accepted
proof_boundary:
  label: target-requirements-architecture-and-migration-design
  exclusions: [api-implementation, persistence-migration, browser-acceptance, measured-performance, production-readiness]
---

# ADR-0006: Common analytical documents, time-aware segments, and retail product analytics

- status: `accepted`;
- date: `2026-08-05`;
- decision owner: `product owner`;
- supersedes/superseded by: none.

## Context

The product owner accepted a wider platform foundation than the previous UI
program described. Custometry must support large workbook-style reports,
dashboard monitoring, narrative research, page- and data-anchored
collaboration, reusable segment snapshots, digital-to-offline journeys, and
retail product/category/inventory analytics without repeating equivalent
compute.

The previous blueprint represented dashboard widgets, research blocks, and
report blocks independently. It also mixed reusable segmentation rules with
evaluation time, used a weak membership identity, treated product category as
flat attributes, and did not define a page-level snapshot or lazy-loading
boundary for large documents.

## Decision

### One composition contract, separate domain lifecycles

`Presentation & Reports` owns `AnalyticalDocumentVersion` and the public,
versioned `AnalyticalDocumentCompositionV1` contract. This is not a generic
shared kernel, a new bounded context, or a deployable service.

The contract supplies stable `chapter -> page -> section -> block` identity,
ordering, filter scopes, navigation, publication, and root/page snapshots.
`dashboard`, `workbook_report`, and `narrative_research` are presentation
profiles of that contract. A `story` profile is not authorized.

Methodology & Research continues to own questions, methodology, research
lifecycle, reviewed findings, and decisions. Analytics, Forecasting, Data
Quality, Digital Measurement, and Promotions continue to own their
calculations. They expose only versioned public projections or immutable
artifacts to Presentation. Composition cannot contain raw SQL, executable
HTML, library options, source rows, or business calculations.

### One snapshot path

Publication resolves the document hierarchy, effective filters, segment
bindings, required block artifacts, presentation identity, and access policy
into one atomic root snapshot with page manifests. Web, email, XLSX, and full
export consume that same root. Large block/page results remain immutable
artifacts, normally Parquet where tabular bulk results are appropriate;
PostgreSQL remains control-plane truth.

The browser receives a permission-filtered page index and mounts only the
active page. Bounded adjacent-page prefetch is allowed but cannot count as a
view or expose denied metadata. Page navigation cannot start an equivalent
compute operation when a compatible fresh artifact or shared single-flight
operation exists.

### Distinct authoring and collaboration objects

The universal block builder produces one schema-versioned normalized block
definition from guided or advanced modes. The required sequence is subject or
data product, metrics and grain, then dimensions and period. Segment,
filters, comparison, and presentation are conditional or optional stages,
followed by permission, trust, cost, freshness, and reuse preflight.

Published analyst notes, exact data annotations, discussion comments, and
reviewed findings are different objects. Refresh never moves an annotation or
comment to new data silently. A manual re-anchor creates audited provenance.
Discussion promotion to a note or finding is an explicit reviewed authoring
action.

### Time-aware segmentation

A reusable `SegmentDefinitionVersion` contains method and observation-window
policy, not an exact evaluation time. `SegmentRun` resolves one `as_of`, input
artifact set, and policy set into an immutable `SegmentSnapshot`. Membership
identity becomes `[segment_snapshot_id, canonical_customer_id]`.

Consumers choose `pinned_snapshot` or
`latest_successful_by_definition_version`. Published workbook reports and
research pin exact snapshots. Live dashboards may select the latter policy,
but every published document snapshot records the exact resolved segment
snapshot. Segment access does not grant member-row access.

### Product, category, assortment, inventory, and pricing

No new bounded context is introduced:

- Semantic Model owns effective-dated product hierarchy, category assignment,
  reusable store clusters, and assortment scope semantics;
- Ingestion owns inventory, availability, price, and planned-assortment source
  facts;
- Analytics owns `analytics_product` specifications and results;
- Promotion Journal supplies descriptive planned/actual overlays;
- Forecasting exposes versioned product/inventory projections.

The V1 target includes category/SKU performance, assortment, sell-through,
days of inventory, turnover, stockout/availability, basic ABC/XYZ/Pareto,
price/markdown/margin, lifecycle, affinity, descriptive substitution, and
promotion overlays. Missing inventory is not zero, zero sales does not prove a
stockout, and substitution is not a causal claim.

### Digital identity and economics

Raw event customer identifiers remain optional source claims. Published
journeys pin an identity-resolution artifact plus taxonomy, session, journey,
conversion, campaign-normalization, cost-reconciliation, FX, and attribution
versions. First-user acquisition, session acquisition, provider attribution,
platform attribution, observed actuals, and scenarios remain separate
measures and views.

## Compatibility and migration

| Surface | Classification | Required transition |
|---|---|---|
| Existing dashboard/research/report composition shapes | breaking target schema change | add schema-v2 common DTO and legacy read adapters; backfill stable hierarchy IDs; no dual-write |
| Report snapshot | compatible first step | add root/page manifests before retiring legacy resolved-block shape |
| Filter scopes and collaboration anchors | additive DTO change | optional fields first; new normalized request/cache namespace |
| Segment membership identity | breaking persistence/key change | backfill stable snapshot IDs, preserve immutable history, maintain legacy-reference map |
| Digital identity resolution | compatible artifact addition | do not reinterpret or rewrite raw event claims; publish schema-v2 result DTO |
| Product/category/inventory facts | additive | add source/canonical contracts and capability blockers |
| Browser document navigation | breaking target behavior | accept through a bounded implementation ticket with target-concept review and browser evidence |

New drafts write only schema v2 after migration. Published legacy versions
remain readable. Dual-writing two composition formats is prohibited. Rollback
stops new v2 publication but does not delete v2 snapshots or lossy-downconvert
them.

## Verification obligations

- DTO/API/port compatibility and generated-client tests for v1/v2;
- database migration, backfill, restore, and legacy-render parity;
- stable-ID/order/filter-DAG property tests;
- Web/email/XLSX golden parity for one multi-page root snapshot;
- old comment/annotation anchors after refresh and revoke;
- one segment definition evaluated into multiple snapshots and migration
  comparisons;
- product fixtures for hierarchy change, missing inventory, availability,
  sell-through, and ABC/XYZ reconciliation;
- digital fixtures for duplicates, late data, identity conflict, consent deny,
  missing spend, FX, purchase/refund/restatement, and residuals;
- cold/warm/hot/same-key/invalidation/off-peak compute benchmarks;
- browser envelope of 100 pages by 30 blocks, RU/EN/pseudo-locale, keyboard,
  tab overflow, Back/Forward, memory/request/DOM counts, and 200% zoom;
- atomic root/page snapshot recovery after worker loss.

No latency SLO or production hard limit is accepted until measured baseline
evidence exists.
