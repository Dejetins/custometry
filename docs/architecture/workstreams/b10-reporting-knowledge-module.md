---
artifact_kind: module_definition
staged_schema_version: 1
doc_id: MODULE-B10-REPORTING-KNOWLEDGE
title: B10 Reporting and Knowledge module definition
doc_version: 1
product_spec_version: 0.8.2-draft
visibility: internal
ship: false
workstream_id: B10
owner: reporting-platform
status: initial
requirement_ids: [AC-026, AC-032, ADMIN-009, CHART-012, CHART-013, CHART-018, DASHBOARD-001, DASHBOARD-002, DASHBOARD-003, DASHBOARD-004, DASHBOARD-005, DASHBOARD-006, DATA-GUIDE-001, DATA-GUIDE-002, DATA-GUIDE-003, DATA-GUIDE-004, DATA-GUIDE-005, DATA-GUIDE-006, DATA-GUIDE-007, DATA-GUIDE-008, GAP-031, GAP-040, GAP-041, GAP-043, GAP-048, REPORT-001, REPORT-002, REPORT-003, REPORT-004, REPORT-005, REPORT-006, REPORT-007, REPORT-008, REPORT-009, REPORT-010, REPORT-MAIL-001, REPORT-MAIL-002, REPORT-MAIL-003, REPORT-MAIL-004, REPORT-MAIL-005, REPORT-MAIL-006, REPORT-MAIL-007, REPORT-MAIL-008, REPORT-MAIL-009, REPORT-MAIL-010, REPORT-MAIL-011, RISK-013, RISK-014, RISK-017, RISK-019, SEC-011, SEC-015, TEST-INV-021, TEST-INV-036, TEST-INV-037, TEST-INV-039, TEST-INV-048, UC-007, UC-011, UC-014, UC-016, V1-AC-004, V1-AC-008, V1-AC-009, V1-AC-010, V1-AC-015]
proof_boundary:
  label: planned-b10-module-boundary
  exclusions: [universal-xlsx, operational-email-webhook, production-mail-readiness, implemented-cross-render-proof, release-readiness]
---

# B10 Reporting and Knowledge — module definition

## Purpose and boundaries

B10 owns dashboards, reusable report composition, immutable
`ReportSnapshot`, safe Data Guides, user-initiated branded report email, and
cross-render presentation contracts for Web, email, and bounded public-MVP
exports. It composes accepted artifacts from B05–B09 without recalculating
their domain truth.

Boundaries:

- B06 owns core ChartSpec/ECharts compilation and reportable analytics blocks;
- B07 owns public-MVP in-app operational notifications;
- B11 owns post-public-MVP operational email/webhook channels and plugin/canvas
  delivery, not user-sent reports;
- B13 owns the final universal entity-aware XLSX assembler and is deliberately
  last;
- B12 owns production security/recovery/performance hardening.

## Ubiquitous language

| Term | Meaning |
|---|---|
| Dashboard version | Immutable widgets, filters, layout, access policy, and bindings |
| Report definition | Versioned reusable composition intent |
| ReportSnapshot | Immutable resolved blocks, filters, bindings, schemas, units, lineage, and render identity |
| Report block | Typed chart, table, KPI, text, guide, or timeline entity |
| Pinned binding | Exact immutable source artifact/version |
| Latest binding | Governed resolver evaluated when snapshot is created |
| Data Guide | Versioned administrator-authored Markdown bound to dataset semantics |
| Sender identity | Authenticated user plus verified/authorized email transport identity |
| Recipient policy | Administrator-managed allowed-domain and permission rules |
| Cross-render contract | Same resolved snapshot semantics across Web, email, and export |

## Domain model and invariants

- Dashboard versions never expand permissions of underlying artifacts.
- `ReportSnapshot` resolves every block, source artifact, filter, metric,
  comparison, schema, unit, lineage, locale/format, theme, font, and renderer
  identity before delivery.
- Web, email, and export render the same resolved snapshot semantics.
- User-sent report email is a deliberate authenticated command; the visible
  sender is the user, not an anonymous alert system.
- Sender email and transport authority are verified independently.
- Recipients must pass administrator domain allowlist, report permission, PII
  permission, and recipient snapshot validation.
- Unknown provider submission is reconciled through a persisted adapter handle;
  it is never blindly retried.
- Data Guide Markdown uses an approved template, sanitizes raw
  HTML/script/remote executable content, and enters review-required state after
  dataset-version drift.
- Chart/table/timeline blocks preserve Result Trust, comparison, filters,
  permissions, and source lineage.
- Public MVP exports CSV/Parquet and bounded internal JSON only; external
  database writes and public result API are absent.
- Universal XLSX behavior is a B13 consumer contract, not implemented here.

## Commands, queries, and events

Commands create/publish dashboards, definitions, snapshots, guides, sender
identities, recipient policies, email deliveries, and bounded exports. Queries
resolve accessible dashboards/reports/guides, snapshot status, delivery status,
and lineage. Events cover snapshot ready, guide review required, delivery
submitted/succeeded/failed/unknown, and export ready.

Long operations use B04 run/artifact/progress contracts. Delivery commands use
idempotency, audited recipient snapshots, bounded retries, timeout classes,
unknown-state reconciliation, and redaction.

## Ports and dependencies

Inbound ports serve dashboard/report/guide/email/export application use cases.
Outbound ports consume:

- B03 identity, workspace, permissions, PII policy, sender/user context, audit;
- B04 execution, artifacts, outbox, progress, and cancellation;
- B05–B09 governed reportable artifacts and schemas;
- B06 ChartSpec/static rendering and Result Trust;
- B07 operational state where shown in dashboards;
- B01 routes, localization, accessibility, Focus/Explore, and local help;
- outbound mail transport through a versioned B10 adapter for user report
  delivery only.

No renderer, transport, or Markdown library is imported by domain/application
code.

## Persistence, artifacts, and security

PostgreSQL stores definitions/versions, snapshot metadata, block bindings,
guide versions/review state, sender verification/authorization metadata,
allowlist policy, delivery state, provider locator, and audit references.
Rendered files and large snapshot payloads are immutable artifacts.

Recipient data is encrypted where required and redacted in logs. Formula-like
content and unsafe Markdown are treated as hostile input. Remote assets,
runtime scripts, and arbitrary URLs are rejected unless an explicit approved
adapter contract allows them.

## UI and documentation

Owned surfaces include dashboard/report builders, snapshot preview/status,
Data Guide editor/review, send-report flow, recipients/domain feedback,
delivery history, and export center. They use shared compact analytics,
searchable typed filters, route-backed Focus, Result Trust, progress/ETA,
accessibility, localization, and reduced motion.

Email uses a bounded branded template, bundled assets/fonts, PNG from SSR SVG,
and safe fallbacks. Browser evidence and email artifact inspection are both
required; a screenshot alone is insufficient.

## Contract impact and acceptance

Snapshot identity, resolved binding semantics, permission inheritance, sender
identity, recipient snapshot, delivery idempotency, guide sanitization, and
cross-render block schemas are breaking dimensions after publication.

B10 hard-depends on B01, B03, B04, B05, B06, B07, B08, and B09. Completion
requires real database/API/browser/renderer/mail-sandbox evidence, provider
unknown-state tests, guide security tests, cross-render golden totals, public
MVP export boundaries, independent cold review, and matrix reconciliation. It
does not complete B11 operational channels or B13 universal XLSX.
