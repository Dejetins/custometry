---
doc_id: TEMPLATE-ADR
title: ADR template
doc_version: 1
product_spec_version: 0.8.2-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: []
status: active
proof_boundary:
  label: contributor-template
  exclusions: [decision-approval, runtime-proof]
---

# ADR-NNNN: <Decision title>

- status: `proposed | accepted | superseded | deprecated`;
- date: `YYYY-MM-DD`;
- decision owner: `<owner>`;
- requirement IDs: `<generated-index references>`;
- supersedes/superseded by: `<ADR or none>`.

## Context

<Current facts, forces, failure cost, constraints and unknowns.>

## Decision criteria

<Explicit criteria and priority.>

## Options

| Option | Benefits | Costs/risks | Fit |
|---|---|---|---|
| TBD | TBD | TBD | TBD |

## Decision

<Selected option and exact boundary.>

## Consequences

<Positive, negative and operational costs.>

## Contract impact and migration

<API/ports/schemas/persistence/config/identity/browser/ops classification, compatibility window and rollback.>

## Verification and proof boundary

<Evidence required to prove the decision works; explicitly separate current evidence from target acceptance.>

## Re-evaluation triggers

<Measurable condition/date/new boundary that requires review.>
