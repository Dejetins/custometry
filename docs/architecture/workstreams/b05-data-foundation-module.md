---
artifact_kind: module_definition
staged_schema_version: 1
workstream_id: B05
doc_id: ARCH-B05-MODULE-001
title: Data Foundation module definition
doc_version: 1
product_spec_version: 0.8.2-draft
visibility: internal
ship: false
owner: architecture
requirement_ids:
- AC-001
- AC-002
- AC-003
- AC-004
- AC-005
- AC-006
- AC-021
- AC-022
- AC-024
- AC-035
- AC-039
- CAPABILITY-001
- CAPABILITY-002
- CAPABILITY-003
- CAPABILITY-004
- DATA-RULE-001
- DATA-RULE-002
- DATA-RULE-003
- DATA-RULE-004
- DATA-RULE-005
- DATA-RULE-006
- DATA-RULE-007
- DATA-RULE-008
- DATA-RULE-009
- DATA-RULE-010
- DATA-RULE-011
- DQ-REMEDIATE-001
- DQ-REMEDIATE-002
- DQ-REMEDIATE-003
- DQ-REMEDIATE-004
- DQ-REMEDIATE-005
- DQ-REMEDIATE-006
- DQ-REMEDIATE-007
- DQ-REMEDIATE-008
- FILTER-001
- FILTER-002
- FILTER-003
- FILTER-004
- FILTER-005
- FILTER-006
- FILTER-007
- FILTER-008
- FILTER-009
- FILTER-010
- GAP-001
- GAP-002
- GAP-003
- GAP-004
- GAP-005
- GAP-006
- GAP-007
- GAP-009
- GAP-023
- GAP-024
- GAP-025
- GAP-027
- GAP-029
- GAP-030
- GAP-039
- IDENTITY-001
- IDENTITY-002
- IDENTITY-003
- IDENTITY-004
- IDENTITY-005
- INGEST-001
- INGEST-002
- INGEST-003
- INGEST-004
- INGEST-005
- INGEST-006
- INGEST-007
- JOURNEY-002
- JOURNEY-003
- MART-GRAIN-001
- MART-GRAIN-002
- MART-GRAIN-003
- MART-GRAIN-004
- MART-GRAIN-005
- MART-GRAIN-006
- MART-GRAIN-007
- METRIC-001
- METRIC-002
- METRIC-003
- METRIC-004
- METRIC-005
- METRIC-006
- METRIC-007
- METRIC-008
- OPEN-007
- RISK-002
- RISK-006
- RISK-011
- SEC-003
- SEC-004
- TEST-INV-001
- TEST-INV-010
- TEST-INV-011
- TEST-INV-012
- TEST-INV-013
- TEST-INV-016
- TEST-INV-017
- TEST-INV-026
- TEST-INV-028
- TEST-INV-031
- TEST-INV-034
- UC-001
- UC-002
- UC-003
- UC-009
- UI-DQ-001
- V1-AC-002
status: initial
proof_boundary:
  label: b05-data-foundation-target-contract
  exclusions:
  - implementation-proof
  - runtime-readiness
  - release-readiness
---

# Data Foundation — Module Definition

> This definition precedes implementation. It is not an activation, stage ledger, or runtime-readiness claim.

## Identity

- workstream: `B05`;
- bounded contexts: Connection Catalog owns connection metadata and catalog snapshots; Ingestion owns extracts and watermarks; Semantic Model owns entities, fields, joins, metrics, capabilities, and filter registry; Data Quality owns rules, reports, remediation, and waivers.
- target packages/apps: `packages/connection_catalog`, `packages/semantic_model`, `packages/ingestion`, `packages/data_quality`, `plugins/connector_postgresql`, `plugins/connector_mssql`, `plugins/connector_files`;
- release milestones: `vertical_alpha`, `public_mvp`, `v1_target`;
- primary requirement IDs: 111 exact allocations from the canonical matrix.

## Purpose and non-goals

Turn governed source connections into immutable landing data, semantic entities and metrics, searchable typed filters, quality evidence, and reproducible marts.

Non-goals: Customer segmentation, forecasting algorithms, report delivery, and universal workbook rendering are outside this workstream.

## Ubiquitous language

| Term | Meaning | Not the same as |
|---|---|---|
| `ConnectionVersion` | Pinned source configuration metadata without exposed secrets. | A mutable UI form |
| `SemanticVersion` | Immutable entity, field, relationship, metric, capability, and filter contract. | A source database schema |
| `LandingManifest` | Immutable evidence of extracted source data and watermark. | A temporary CSV |
| `QualityDecision` | Versioned pass, warn, block, waive, or remediate result with evidence. | A visual score only |

## Domain model

Connection, CatalogSnapshot, ExtractSpec, Watermark, LandingManifest, SemanticModelVersion, Entity, Field, Relationship, MetricDefinition, FilterField, CapabilitySet, QualityRule, QualityReport, Waiver, and RemediationDecision.

Every write belongs to one context. Cross-context reads use public projections or query ports. Actor, workspace, trace, and contract-version context cross every protected boundary.

## Use cases and contracts

| Command/query/event | Actor/caller | Input/output owner | Errors, idempotency, and version |
|---|---|---|---|
| `TestConnection / SnapshotCatalog` | Authorized administrator | Connection Catalog commands | Secret-safe errors and version pinning |
| `RunIngestion` | Execution Control | ExtractSpec to LandingManifest | Watermark idempotency and immutable manifest |
| `PublishSemanticModel / EvaluateQuality` | Data steward or execution | Versioned schemas and evidence | Blocking decisions are explicit |

Public schemas are versioned before external reliance. Unknown state is explicit; it is never mapped to success or empty data.

## Data ownership

Owner-specific PostgreSQL metadata plus immutable landing/mart artifacts. Grain, key, timezone, currency, identity mapping, lineage, retention, and PII classification are explicit.

Migration, compatibility, retention, lineage, redaction, and rollback are defined before persistence becomes authoritative. No context reads or mutates another context's private tables.

## Ports and adapters

| Port owner | Adapter | Auth/trust | Timeout/retry/unknown state | Degradation |
|---|---|---|---|---|
| Connection Catalog | PostgreSQL/MSSQL/file connector plugins | Secret reference, not secret value | Timeout classes; no blind retry after unknown mutation | Connection degraded |
| Ingestion | Artifact commit port | Pinned workspace/source version | Watermark and immutable manifest | Run failed or blocked |
| Semantic/Data Quality | PostgreSQL repositories and execution port | Role and workspace policy | Versioned publish and idempotent evaluation | Evidence-preserving degraded state |

## UI and documentation

Connections, Data Catalog, Data Model, Metrics, Data Quality, remediation, searchable filter catalog, capability explanations, loading/empty/degraded/forbidden/failed states, and contextual Data Guide links.

The Web contract includes loading, empty, degraded, forbidden, failed, refresh, unsaved-change, and return-to-origin behavior. Shipped `/docs` and `/help` content follows visibility and localization policy. Penpot mutation requires separately confirmed live authority.

## Operations

Connection health, ingestion lag, watermark age, schema drift, quality-rule duration, failed rows, remediation backlog, mart freshness, lineage availability, and secret-safe logs.

All logs, traces, notifications, and evidence redact secrets and raw PII. Capacity assumptions remain single-server and CPU-only through `v1_target` unless an ADR changes the topology.

## Fixtures and acceptance

Deterministic retail source schemas and data with customers, products, receipts, receipt items, stores, calendar, promotions, duplicates, nulls, orphan rows, late data, and drift.

Acceptance follows S00–S06 and requires unit/property, contract, real adapter, browser, runtime, recovery, security, or performance evidence only where the changed boundary triggers it.

## Contract impact

This initial definition is a `compatible-change` to repository planning artifacts and an `unknown` future product contract until S01 freezes schemas. It changes no running API, persistence, browser behavior, or external side effect.

## Open decisions and blockers

OPEN-007 is a hard B05-S01 decision gate for its affected data-contract path; no default may be inferred.

Principal risks: Identity mismatch, invalid grain, unsafe joins, silent schema drift, mutable metrics, PII exposure, non-reproducible watermarks, and quality decisions hidden from consumers.
