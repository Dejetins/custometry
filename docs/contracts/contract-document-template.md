---
doc_id: TEMPLATE-CONTRACT
title: Contract document template
doc_version: 1
product_spec_version: 0.8.2-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: []
status: active
proof_boundary:
  label: contributor-template
  exclusions: [implemented-consumer, runtime-compatibility]
---

# <Contract name>

## Identity and ownership

- contract ID/version: `<stable-id>/<version>`;
- owner: `<bounded-context>`;
- callers/consumers: `<inventory>`;
- requirement IDs: `<generated-index references>`;
- compatibility policy: `<additive/versioned/cutover>`.

## Purpose and non-goals

<Which boundary is stabilized and what this contract intentionally does not cover.>

## Shape

<OpenAPI/JSON Schema/DTO/event/port/artifact manifest path, fields, types, constraints, examples, and stable errors. Do not insert a divergent copy of a schema that already exists as a code artifact.>

## Semantics

- workspace/actor/authorization;
- source of truth and consistency;
- ordering/pagination/bounds;
- idempotency/dedupe/request identity;
- timeout/retry/cancellation/unknown state;
- PII/redaction/audit;
- version negotiation/deprecation.

## Failure and degradation

| Condition | Stable code/status | Caller action | Retry/reconcile | Observability/redaction |
|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD |

## Compatibility and migration

| Consumer | Current | Target | Classification | Migration window | Rollback |
|---|---|---|---|---|---|
| TBD | TBD | TBD | `none/compatible-change/breaking-change/unknown` | TBD | TBD |

## Examples and fixtures

<Positive, negative, limit, version, cross-workspace and redaction fixtures.>

## Validation and proof boundary

- static/schema checks: `<commands>`;
- consumer/provider contract tests: `<evidence>`;
- real-boundary evidence: `<API/database/adapter/browser>`;
- exclusions: `<what remains unobserved>`.

## Documentation continuity

<Generated clients/mocks/docs/help/runbooks/indexes to update and exact quality tools.>
