---
doc_id: TEMPLATE-ARCHITECTURE
title: Architecture document template
doc_version: 1
product_spec_version: 0.8.2-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: []
status: active
proof_boundary:
  label: contributor-template
  exclusions: [runtime-readiness, implementation-readiness]
---

# <Architecture document title>

## Metadata

- status: `proposed | accepted | superseded`;
- owner: `<owner>`;
- product specification: `custometry-technical-blueprint-ru.md`, `<version>`;
- requirement IDs: `<generated-index references>`;
- current-state boundary: `<what was observed>`;
- target-state boundary: `<what is proposed>`.

## Business objective and non-goals

<User or operational outcome, scale and failure cost, and explicit exclusions.>

## Current-state fact ledger

| Type | Fact/assumption/unknown | Source/evidence | Consequence |
|---|---|---|---|
| Fact | TBD | TBD | TBD |

## Target boundaries

<Owners, components, dependency direction, trust boundaries, and data ownership.>

## Contracts and flows

<Caller/callee, API/command/event/port, versioning, auth, timeout, retry, idempotency, failure/degradation, observability/redaction.>

## Options and decision

| Option | Benefits | Costs/risks | Decision |
|---|---|---|---|
| TBD | TBD | TBD | TBD |

## Contract impact

| Surface | Old | New | Classification | Migration/rollback | Proof |
|---|---|---|---|---|---|
| API/ports/schemas | TBD | TBD | `none/compatible-change/breaking-change/unknown` | TBD | TBD |
| Persistence/artifacts | TBD | TBD | TBD | TBD | TBD |
| Config/identity/idempotency | TBD | TBD | TBD | TBD | TBD |
| Browser/ops/security | TBD | TBD | TBD | TBD | TBD |

## Delivery and rollback

<Reversible migration phases, entry and exit criteria, owned artifacts, stop
conditions, and rollback when the architecture change genuinely requires
phased coordination.>

## Validation and proof boundaries

<Tests and API/database/browser/runtime/performance/recovery evidence; state exactly what remains unproven.>

## Documentation continuity

<Which blueprint, human mirror, UI, documentation, ADR, runbook, and index artifacts change, and which tools verify them.>

## Residual risks

<Risk, owner, mitigation, review trigger.>

## File manifest

- created: []
- modified: []
- deleted: []
- outside expected paths: []
- foreign exclusions: []
