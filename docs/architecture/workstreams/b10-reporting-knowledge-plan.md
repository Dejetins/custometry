---
artifact_kind: workstream_plan
staged_schema_version: 1
workstream_id: B10
plan_maturity: initial
program_plan: docs/architecture/program/custometry-program-plan.md
module_definition: docs/architecture/workstreams/b10-reporting-knowledge-module.md
plan_doc: docs/architecture/workstreams/b10-reporting-knowledge-plan.md
prompt_pack_dir: .codex/agents/generated/b10-reporting-knowledge
stage_ledger: docs/architecture/workstreams/b10-reporting-knowledge-stage-reports/b10-reporting-knowledge-stage-ledger.md
execution_mode: manual_sequential
hard_dependencies: [B01, B03, B04, B05, B06, B07, B08, B09]
soft_dependencies: []
stage_ids: [S00, S01, S02, S03, S04, S05, S06]
release_milestones: [public_mvp, v1_target]
spec_version: 0.8.2-draft
requirement_ids: [AC-026, AC-032, ADMIN-009, CHART-012, CHART-013, CHART-018, DASHBOARD-001, DASHBOARD-002, DASHBOARD-003, DASHBOARD-004, DASHBOARD-005, DASHBOARD-006, DATA-GUIDE-001, DATA-GUIDE-002, DATA-GUIDE-003, DATA-GUIDE-004, DATA-GUIDE-005, DATA-GUIDE-006, DATA-GUIDE-007, DATA-GUIDE-008, GAP-031, GAP-040, GAP-041, GAP-043, GAP-048, REPORT-001, REPORT-002, REPORT-003, REPORT-004, REPORT-005, REPORT-006, REPORT-007, REPORT-008, REPORT-009, REPORT-010, REPORT-MAIL-001, REPORT-MAIL-002, REPORT-MAIL-003, REPORT-MAIL-004, REPORT-MAIL-005, REPORT-MAIL-006, REPORT-MAIL-007, REPORT-MAIL-008, REPORT-MAIL-009, REPORT-MAIL-010, REPORT-MAIL-011, RISK-013, RISK-014, RISK-017, RISK-019, SEC-011, SEC-015, TEST-INV-021, TEST-INV-036, TEST-INV-037, TEST-INV-039, TEST-INV-048, UC-007, UC-011, UC-014, UC-016, V1-AC-004, V1-AC-008, V1-AC-009, V1-AC-010, V1-AC-015]
---

# B10 Reporting and Knowledge — Initial Plan

## Objective and boundary

Deliver versioned dashboards, immutable ReportSnapshot composition, safe Data
Guides, user-initiated branded report email, and consistent Web/email/bounded
export semantics. B10 composes accepted artifacts; it does not recalculate
their domain truth.

B11 owns post-public-MVP operational email/webhook. B13 owns universal XLSX and
is intentionally later.

## Dependencies and activation

Hard dependencies are B01, B03, B04, B05, B06, B07, B08, and B09. There are no
soft dependencies. Activation requires accepted slices, explicit user
authority, and exact trio registration.

## Requirement groups

| Group | IDs | Planned evidence |
|---|---|---|
| Dashboards | `DASHBOARD-001`–`006`, `AC-026`, `TEST-INV-021`, `UC-007` | version/pinned-latest/permission tests and browser |
| ReportSnapshot/rendering | `REPORT-001`–`010`, `CHART-012`, `CHART-013`, `CHART-018`, `TEST-INV-048`, `UC-011`, `UC-014`, `V1-AC-008`–`010` | contract schema, renderer artifacts, cross-render goldens |
| Data Guides | `DATA-GUIDE-001`–`008`, `TEST-INV-039`, `V1-AC-004` | Markdown sanitizer, version drift, admin/browser flow |
| User report email | `REPORT-MAIL-001`–`011`, `TEST-INV-036`, `TEST-INV-037`, `UC-016`, `V1-AC-015` | sender/domain/PII, idempotency, provider reconciliation, email artifact |
| Public-MVP export/admin/gaps/risks | remaining routed IDs, including `SEC-011` and `SEC-015` | bounded CSV/Parquet/JSON, sensitive-export controls, isolated static rendering, and integration evidence |

## Stage outline

| Stage | Planned outcome | Exit boundary |
|---|---|---|
| `S00` | Inventory reportable consumers, renderer/email/export adapters, permissions, docs, and open policies. | Source-anchored discovery |
| `S01` | Freeze dashboard/report/snapshot/block/guide/mail/export schemas, journeys, APIs, errors, and render identity. | Versioned contracts |
| `S02` | Implement snapshot resolution, binding, guide, recipient, delivery, and export policies. | Domain/property evidence |
| `S03` | Implement PostgreSQL/artifact/renderer/mail/export adapters and migrations. | Real adapter/API evidence |
| `S04` | Implement dashboard/report/guide/send/export browser flows. | Browser/accessibility evidence |
| `S05` | Prove cross-render totals, sender/allowlist/PII, provider unknown state, sanitizer, cancellation, and resources. | Target runtime evidence |
| `S06` | Reconcile requirements, docs, rollback, B11/B13 handoffs, and cold review. | Workstream acceptance |

## Contracts, side effects, and rollback

ReportSnapshot identity freezes resolved blocks, sources, filters, metric and
comparison versions, schema, units, lineage, locale/theme/font, compiler, and
renderer. Email persists an encrypted recipient snapshot and adapter locator.
Unknown submission reconciles before retry. Guide HTML/script/remote executable
content is removed. Rollback preserves immutable snapshots and delivery audit.

## Validation and proof

Acceptance requires database/API/browser/renderer/mail-sandbox evidence,
cross-render golden totals, permission negatives, Markdown security, sender
verification, domain allowlist, PII policy, idempotency, retry/unknown-state,
bounded export, cancellation/cleanup, accessibility, and cold review.

## Risks and completion rule

Primary risks are permission expansion, mutable latest binding, inconsistent
render totals, email spoofing, duplicate delivery, unsafe Markdown, hidden
external effects, and premature XLSX coupling. Completion requires all stages,
matrix traceability, real evidence, migration/rollback, explicit B11/B13
contracts, and no unresolved blocker.
