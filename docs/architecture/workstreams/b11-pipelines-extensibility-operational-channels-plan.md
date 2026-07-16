---
artifact_kind: workstream_plan
staged_schema_version: 1
workstream_id: B11
plan_maturity: initial
program_plan: docs/architecture/program/custometry-program-plan.md
module_definition: docs/architecture/workstreams/b11-pipelines-extensibility-operational-channels-module.md
plan_doc: docs/architecture/workstreams/b11-pipelines-extensibility-operational-channels-plan.md
prompt_pack_dir: .codex/agents/generated/b11-pipelines-extensibility-operational-channels
stage_ledger: docs/architecture/workstreams/b11-pipelines-extensibility-operational-channels-stage-reports/b11-pipelines-extensibility-operational-channels-stage-ledger.md
execution_mode: manual_sequential
hard_dependencies: [B04, B07, B10]
soft_dependencies: [B05, B08, B09]
stage_ids: [S00, S01, S02, S03, S04, S05, S06]
release_milestones: [v1_target]
spec_version: 0.8.2-draft
requirement_ids: [GAP-020, NOTIFY-006, NOTIFY-008, NOTIFY-009, NOTIFY-010, NOTIFY-011, NOTIFY-012, NOTIFY-013, NOTIFY-014, NOTIFY-015, RISK-004, RISK-007, SEC-006, TEST-INV-029, UC-006]
---

# B11 Pipelines, Extensibility and Operational Channels — Initial Plan

## Objective and release boundary

Deliver common-engine pipeline authoring, trusted plugin lifecycle, and
v1-target operational email/webhook delivery. Public MVP remains in-app only;
B11 must not become a public-MVP dependency. B10 user report email is a separate
bounded command and transport policy.

## Dependencies and activation

Hard dependencies are B04, B07, and B10. B05, B08, and B09 are soft node/
contract providers. Activation requires accepted hard slices, explicit user
authority, and exact trio registration.

## Requirement groups

| Group | IDs | Planned evidence |
|---|---|---|
| Operational channels | `NOTIFY-006`, `NOTIFY-008`–`015`, `SEC-006`, `TEST-INV-029` | endpoint versioning, in-app-only MVP gate, mail/webhook sandbox, SSRF/signature/retry/reconciliation |
| Pipeline journey | `UC-006`, `GAP-020` | guided/canvas normalized equivalence and common-engine execution |
| Plugin/channel risks | `RISK-004`, `RISK-007` | compatibility, permissions, resources, secrets, supply chain, rollback |

## Stage outline

| Stage | Planned outcome | Exit boundary |
|---|---|---|
| `S00` | Inventory B04 engine, B07 events/inbox, B10 boundaries, plugins, endpoints, and release gates. | Source-anchored discovery |
| `S01` | Freeze pipeline/node/plugin/channel schemas, lifecycle, APIs, errors, permissions, and UI journeys. | Versioned contracts |
| `S02` | Implement normalized graph, plugin compatibility/lifecycle, routing, dedupe, retry, and reconciliation policies. | Domain/property evidence |
| `S03` | Implement engine/plugin registry/email/webhook/secret/PostgreSQL adapters and migrations. | Real adapter/API evidence |
| `S04` | Implement canvas, plugin admin, channel settings, attempts, and accessible alternatives. | Browser/accessibility evidence |
| `S05` | Prove equivalence, plugin lifecycle, mail/webhook sandbox, SSRF/signature, failure/recovery, and resources. | Target runtime/security evidence |
| `S06` | Reconcile v1 requirements, B12 hardening handoff, docs, rollback, and cold review. | Workstream acceptance |

## Contracts and side effects

Pipeline specs, node contracts, plugin manifests, endpoint versions, routing
policies, delivery identities, signatures, retries, and unknown-state
reconciliation are versioned. Plugins and outbound channels are external/
privileged side effects with explicit destination, authority, secrets,
timeouts, idempotency, audit, cleanup, and rollback.

## Validation and completion

Acceptance requires common-engine parity, negative graph validation, plugin
install/upgrade/disable/remove, supply-chain/permission/resource controls,
email/webhook sandbox proof, SSRF and signature tests, bounded retry and
unknown-state reconciliation, browser/accessibility evidence, and B12
re-hardening. Completion requires terminal stages, traceability, and no
unresolved cold-review blocker.
