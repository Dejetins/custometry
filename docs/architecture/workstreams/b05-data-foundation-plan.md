---
artifact_kind: workstream_plan
staged_schema_version: 1
workstream_id: B05
plan_maturity: initial
program_plan: docs/architecture/program/custometry-program-plan.md
module_definition: docs/architecture/workstreams/b05-data-foundation-module.md
plan_doc: docs/architecture/workstreams/b05-data-foundation-plan.md
prompt_pack_dir: .codex/agents/generated/b05-data-foundation
stage_ledger: docs/architecture/workstreams/b05-data-foundation-stage-reports/b05-data-foundation-stage-ledger.md
execution_mode: goal_driven
hard_dependencies:
- B02
- B03
- B04
soft_dependencies:
- B01
stage_ids:
- S00
- S01
- S02
- S03
- S04
- S05
- S06
release_milestones:
- vertical_alpha
- public_mvp
- v1_target
spec_version: 0.8.2-draft
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
---

# Data Foundation — Initial Plan

## Identity and authority

- program/workstream: `custometry-v1 / B05`;
- authority: normative blueprint, accepted architecture, Program Plan, and generated requirement matrix;
- current proof boundary: planning scaffold only;
- activation rule: this plan remains dormant until its ledger becomes `active` and `.codex/PLANS.md` registers the exact trio.

## Objective and non-goals

Turn governed source connections into immutable landing data, semantic entities and metrics, searchable typed filters, quality evidence, and reproducible marts.

Non-goals: Customer segmentation, forecasting algorithms, report delivery, and universal workbook rendering are outside this workstream.

## Current-state fact ledger

| Type | Fact, assumption, proposal, or unknown | Source/evidence | Consequence |
|---|---|---|---|
| Fact | The matrix allocates 111 primary requirements to `B05`. | `docs/architecture/program/requirement-matrix.json` | The plan may not absorb another workstream's primary ownership. |
| Fact | Hard dependencies are `B02`, `B03`, `B04`; soft dependencies are `B01`. | Program routing source | Missing hard evidence keeps the ledger dormant. |
| Fact | No implementation stage is authorized by creating this scaffold. | Ledger `dormant`, prompts `outline/false` | No code, migration, browser, runtime, or external mutation may begin. |
| Unknown | S01 contract details not fixed by accepted sources remain decisions, not defaults. | Module definition open-decision section | Stop the affected contract path until resolved. |

## Dependencies and milestones

Release participation is `vertical_alpha`, `public_mvp`, `v1_target`. Hard dependency evidence is an entry gate; soft dependencies may use versioned generated contracts temporarily but must reconcile before milestone verification.

## Requirement allocation

- exact primary IDs: 111;
- primary families: `AC` (11), `CAPABILITY` (4), `DATA-RULE` (11), `DQ-REMEDIATE` (8), `FILTER` (10), `GAP` (15), `IDENTITY` (5), `INGEST` (7), `JOURNEY` (2), `MART-GRAIN` (7), `METRIC` (8), `OPEN` (1), `RISK` (3), `SEC` (2), `TEST-INV` (11), `UC` (4), `UI-DQ` (1), `V1-AC` (1);
- source: generated exact matrix; no manually maintained numeric ranges;
- stage prompts may repeat an ID when one requirement needs contract, adapter, browser, and acceptance evidence, but may not reference an ID outside this plan.

## DDD target and contracts

Connection Catalog owns connection metadata and catalog snapshots; Ingestion owns extracts and watermarks; Semantic Model owns entities, fields, joins, metrics, capabilities, and filter registry; Data Quality owns rules, reports, remediation, and waivers.

Connection, CatalogSnapshot, ExtractSpec, Watermark, LandingManifest, SemanticModelVersion, Entity, Field, Relationship, MetricDefinition, FilterField, CapabilitySet, QualityRule, QualityReport, Waiver, and RemediationDecision.

The implementation preserves dependency direction: domain → application ports → adapters → composition roots. Public APIs, DTOs, events, persisted schemas, config/defaults, idempotency identity, and browser-visible defaults require compatibility classification and migration when changed.

## Stage plan

| Stage | Outcome | Entry gate | Exit evidence | Rollback/stop gate |
|---|---|---|---|---|
| `S00` | Discovery | Previous stage accepted; hard dependencies remain observed | Confirm source-anchored scope, ownership, vocabulary, dependencies, risks, and stop gates. | Missing authority, contract, or boundary evidence blocks progression |
| `S01` | UX and contract | Previous stage accepted; hard dependencies remain observed | Freeze routes, states, commands, queries, events, schemas, permissions, errors, and compatibility. | Missing authority, contract, or boundary evidence blocks progression |
| `S02` | Domain and application | Previous stage accepted; hard dependencies remain observed | Implement or specify framework-free aggregates, invariants, policies, use cases, and owned ports. | Missing authority, contract, or boundary evidence blocks progression |
| `S03` | Adapters | Previous stage accepted; hard dependencies remain observed | Implement or specify persistence and outbound adapters, migrations, retry classes, and unknown-state reconciliation. | Missing authority, contract, or boundary evidence blocks progression |
| `S04` | Web integration | Previous stage accepted; hard dependencies remain observed | Connect the accepted contract to the Frost Web experience with complete system states and accessibility. | Missing authority, contract, or boundary evidence blocks progression |
| `S05` | Real-boundary proof | Previous stage accepted; hard dependencies remain observed | Observe the nearest database, API, browser, worker, Compose, or artifact boundary required by the slice. | Missing authority, contract, or boundary evidence blocks progression |
| `S06` | Acceptance | Previous stage accepted; hard dependencies remain observed | Reconcile requirement evidence, contracts, docs, rollback, residual risk, and independent review. | Missing authority, contract, or boundary evidence blocks progression |

## Migration, rollback, and recovery

S01 records compatibility and migration obligations before implementation. Stateful S03 work requires empty-install and supported upgrade evidence. Rollback never deletes authoritative state blindly; unknown external or durable effects are reconciled through owned identities.

## Validation and proof boundaries

Focused validation starts with the smallest affected unit/contract and expands to database, API, browser, worker, Compose, recovery, security, performance, or delivery only when that boundary is changed. Green planning validators do not prove implementation or release readiness.

## Documentation continuity

Keep the Program Plan, routing, generated matrix, module definition, plan, ledger, stage prompts, architecture index, affected contracts, and runbooks synchronized. Product obligations first change the normative blueprint and human mirror.

## Risks and open decisions

OPEN-007 is a hard B05-S01 decision gate for its affected data-contract path; no default may be inferred.

Principal risks: Identity mismatch, invalid grain, unsafe joins, silent schema drift, mutable metrics, PII exposure, non-reproducible watermarks, and quality decisions hidden from consumers.

## Change ownership

- planned primary paths: `packages/connection_catalog`, `packages/semantic_model`, `packages/ingestion`, `packages/data_quality`, `plugins/connector_postgresql`, `plugins/connector_mssql`, `plugins/connector_files`;
- planning paths: `docs/architecture/workstreams/b05-data-foundation-*` and `.codex/agents/generated/b05-data-foundation/`;
- foreign exclusions: unrelated dirty files, other workstreams, secrets, generated caches, production systems, and Penpot until separately authorized;
- mixed-file policy: stop when safe hunk separation is impossible;
- branch policy: one authorized short-lived workstream branch; per-stage branches are forbidden.

## Completion rule

The workstream completes only when every non-superseded stage is terminal, the ledger is `completed`, all primary requirements have their matrix-declared evidence, release checkpoints are reconciled, and no blocker remains.
