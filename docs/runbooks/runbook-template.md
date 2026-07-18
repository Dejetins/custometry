---
doc_id: TEMPLATE-RUNBOOK
title: Runbook template
doc_version: 1
product_spec_version: 0.9.0-draft
visibility: internal
ship: false
owner: operations
requirement_ids: []
status: active
proof_boundary:
  label: contributor-template
  exclusions: [observed-recovery-drill, target-runtime-readiness]
---

# RUNBOOK-NNN: <Failure or recovery action>

## Metadata

- owner/on-call: `<owner>`;
- supported versions: `<range>`;
- severity/user impact: `<classification>`;
- alert/stable error codes: `<IDs>`;
- last reviewed/drilled: `<date/evidence>`;
- visibility: `authenticated | internal`.

## Symptoms and impact

<Observable symptoms, affected capability and safe user message. Do not reveal denied resources, PII, secret or private topology.>

## Preconditions and evidence

<Permissions, backups, bounded redacted commands/log fields and stop condition.>

## Diagnosis

1. <Safe check and expected branches.>
2. <Safe check and expected branches.>

## Mitigation

1. <Bounded reversible action.>
2. <Expected outcome.>

## Rollback and escalation

<When to stop, revert and transfer ownership. No blind retry after unknown external result.>

## Verification/post-conditions

<Data integrity, application/business readiness, user flow, metrics and negative checks.>

## Recovery proof boundary

- observed target/environment: `<target>`;
- evidence location: `<immutable reference>`;
- exclusions/residual risk: `<explicit>`.
