---
artifact_kind: workstream_plan
staged_schema_version: 1
workstream_id: B13
plan_maturity: initial
program_plan: docs/architecture/program/custometry-program-plan.md
module_definition: docs/architecture/workstreams/b13-universal-xlsx-module.md
plan_doc: docs/architecture/workstreams/b13-universal-xlsx-plan.md
prompt_pack_dir: .codex/agents/generated/b13-universal-xlsx
stage_ledger: docs/architecture/workstreams/b13-universal-xlsx-stage-reports/b13-universal-xlsx-stage-ledger.md
execution_mode: goal_driven
hard_dependencies: [B10, B11, B12]
soft_dependencies: [B06, B08, B09]
stage_ids: [S00, S01, S02, S03, S04, S05, S06]
release_milestones: [v1_feature_freeze, v1_target]
spec_version: 0.8.2-draft
requirement_ids: [GAP-042, RISK-015, TEST-INV-032, TEST-INV-038, TEST-INV-044, TEST-INV-047, UC-015, V1-AC-011, V1-AC-012, XLSX-001, XLSX-002, XLSX-003, XLSX-004, XLSX-005, XLSX-006, XLSX-007, XLSX-008, XLSX-009]
---

# B13 Universal XLSX — Initial Plan

## Objective and sequencing

Build the final universal entity-aware workbook assembler from stable
ReportSnapshot contracts. Preserve data, charts, filters, `vs LY`, Result
Trust, lineage, and permissions; use native Excel charts when semantics are
proven and deterministic PNG otherwise.

B13 is deliberately last. Hard dependencies are B10, B11, and B12. B06, B08,
and B09 are soft block-schema providers. B13 closes `v1_feature_freeze` at S06.

## Requirement groups

| Group | IDs | Planned evidence |
|---|---|---|
| Workbook assembly | `XLSX-001`–`009`, `UC-015` | entity contracts, OOXML generation, browser flow |
| Cross-render parity | `TEST-INV-032`, `TEST-INV-044`, `TEST-INV-047`, `V1-AC-012` | shared snapshot totals/semantics and native/raster parity |
| Boundary/security | `TEST-INV-038`, `GAP-042`, `RISK-015`, `V1-AC-011` | split/no-loss, injection, collisions, limits, openability, resources |

## Stage outline

| Stage | Planned outcome | Exit boundary |
|---|---|---|
| `S00` | Inventory final snapshot/block schemas, chart renderer, Excel limits, security, and supported applications. | Source-anchored discovery |
| `S01` | Freeze workbook/entity/manifest/split/chart/fallback/error/UI contracts. | Versioned XLSX contract |
| `S02` | Implement pure workbook planning, naming, splitting, sanitization, and mapping policies. | Domain/property evidence |
| `S03` | Implement workbook library, artifact, renderer, temp-storage, validation, and cancellation adapters. | Real workbook/API evidence |
| `S04` | Implement export configuration/progress/warning/download browser flow. | Browser/accessibility evidence |
| `S05` | Prove cross-render totals, limits, injection, collisions, native/raster charts, memory/temp, cancellation, and openability. | Target runtime/application evidence |
| `S06` | Reconcile requirements, docs, rollback, cold review, and feature-freeze readiness. | B13 and feature-freeze acceptance |

## Contracts and rollback

Input is immutable ReportSnapshot. Breaking dimensions include block mapping,
sheet/range identity, split ordering, formula/sanitization policy, chart
fallback semantics, manifest/hash identity, and permission/redaction behavior.
Failed/cancelled workbooks remain unpublished and temp output is removed.
Rollback preserves previously committed immutable workbook artifacts.

## Validation and completion

Acceptance requires boundary-size split tests, no row loss/duplication,
sheet-name collisions, formula injection, unsupported block handling,
cross-render golden totals, native/raster chart parity, OOXML-aware validation,
real application openability, bounded memory/temp/disk, cancellation/cleanup,
browser/accessibility evidence, cold review, and matrix traceability.
