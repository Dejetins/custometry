---
artifact_kind: workstream_plan
staged_schema_version: 1
workstream_id: B08
plan_maturity: initial
program_plan: docs/architecture/program/custometry-program-plan.md
module_definition: docs/architecture/workstreams/b08-customer-intelligence-promotion-journal-module.md
plan_doc: docs/architecture/workstreams/b08-customer-intelligence-promotion-journal-plan.md
prompt_pack_dir: .codex/agents/generated/b08-customer-intelligence-promotion-journal
stage_ledger: docs/architecture/workstreams/b08-customer-intelligence-promotion-journal-stage-reports/b08-customer-intelligence-promotion-journal-stage-ledger.md
execution_mode: manual_sequential
hard_dependencies: [B01, B03, B04, B05, B06]
soft_dependencies: [B07]
stage_ids: [S00, S01, S02, S03, S04, S05, S06]
release_milestones: [public_mvp, v1_target]
spec_version: 0.8.2-draft
requirement_ids: [CHART-007, CHART-008, GAP-038, GAP-049, PROMO-001, PROMO-002, PROMO-003, PROMO-004, PROMO-005, PROMO-006, PROMO-007, PROMO-008, PROMO-009, RISK-012, TEST-INV-002, TEST-INV-035, TEST-INV-045, UC-013, V1-AC-003, V1-AC-014]
---

# B08 Customer Intelligence and Promotion Journal — Initial Plan

## Objective and boundary

Deliver customer overview, lifecycle, cohorts, RFM/segments, immutable segment
snapshots, and an auditable promotion journal with planned/actual ranges,
multi-channel/client scope, pinned audiences, and non-causal timeline overlays.

B08 consumes B05 canonical data and B06 presentation contracts. It does not
own ingestion, canonical identity, core metrics, forecasting, report delivery,
operational channels, or causal uplift.

## Dependencies and activation

Hard dependencies B01, B03, B04, B05, and B06 must be accepted for the target
slice. B07 is soft and may be represented by a versioned contract until
reconciliation. The dormant ledger cannot activate without explicit user
authority and exact `.codex/PLANS.md` registration.

## Requirement groups

| Group | IDs | Planned evidence |
|---|---|---|
| Promotion domain/versioning | `PROMO-001`–`PROMO-009`, `V1-AC-003` | domain/property tests, PostgreSQL migrations, API/browser timeline |
| Customer intelligence journeys | `UC-013`, `V1-AC-014`, `TEST-INV-002` | real marts/artifacts, API, browser, accessibility |
| Timeline/chart behavior | `CHART-007`, `CHART-008`, `TEST-INV-045` | range timeline contract, renderer/browser golden evidence |
| Gaps/risks/invariants | `GAP-038`, `GAP-049`, `RISK-012`, `TEST-INV-035` | immutable audience, overlap, permissions, non-causal labeling |

## Stage outline

| Stage | Planned outcome | Exit boundary |
|---|---|---|
| `S00` | Reconcile data owners, customer/segment/promotion contracts, current UI, and matrix rows. | Source-anchored discovery; no implementation |
| `S01` | Freeze user journeys, APIs, schemas, version lifecycle, timeline/ChartSpec, permissions, and errors. | Versioned contract and browser scenarios |
| `S02` | Implement framework-independent customer, segment, cohort, lifecycle, and promotion policies. | Domain/property evidence |
| `S03` | Implement PostgreSQL/artifact/execution/API adapters and migrations. | Real database/API evidence |
| `S04` | Integrate customer/segment/promotion screens and Focus/Explore. | Real browser/accessibility evidence |
| `S05` | Prove end-to-end snapshot, promotion overlap/audience, permissions, scale, and recovery behavior. | Target runtime evidence |
| `S06` | Reconcile requirements, docs, rollback, cold review, and milestone readiness. | Workstream acceptance |

## Contracts, migration, and rollback

Published segment definitions/snapshots and promotion versions are immutable.
Breaking dimensions include canonical customer key, membership grain,
audience identity, planned/actual range semantics, channel/client scope, and
timeline overlay meaning. Migrations require compatibility, backfill,
rollback/recovery, and artifact-lineage plans. Invalid or partially committed
versions remain invisible.

## Validation and proof

Acceptance requires focused Python/TypeScript/database checks plus real
artifact, API, and browser evidence. Required negative cases include source
identity collision, overlapping promotions, pinned audience stability,
workspace/PII permissions, stale optimistic revisions, duplicate commands,
non-causal labels, and inaccessible drag-only interactions.

## Risks and completion rule

Primary risks are duplicated metric truth, mutable audiences, promotion
overlap loss, hidden client/channel shortcuts, and causal overclaiming. B08 is
complete only when all stages are terminal, routed requirements have durable
evidence, migrations/rollback are proven, cold review has no blocker, and the
ledger is completed. This initial plan becomes detailed during accepted S00/S01.
