---
doc_id: ADR-0004
title: Historical UI design program governance and target reset
doc_version: 2
product_spec_version: 0.10.0-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: [DOC-RULE-010, WEB-ARCH-001, WEB-ARCH-005]
status: superseded
proof_boundary:
  label: historical-documentation-authority-record
  exclusions: [browser-runtime, frontend-conformance, release-readiness]
---

# ADR-0004: Historical UI design program governance and target reset

- original decision: 2026-08-05;
- superseded: 2026-09-04, by explicit product-owner decision;
- current source: [Web implementation source contract](../architecture/ui/custometry-web-implementation-source-contract-v1.md);
- history/recovery: [UI program retirement](../architecture/ui/ui-program-retirement.md).

## Historical context

This decision retired the unexecuted Linear/Penpot W19-W23 transition and
introduced a product-wide G0-G6 design workflow. The complete original decision
and generated evidence remain recoverable from the commit named in the
retirement record. They are not current execution or design authority.

## Superseding decision

The owner selected the final interactive pilot as the target UI concept,
including its demonstrated composition and behavior, and authorized deletion of
the G-program and its materials. The [preserved pilot](../architecture/ui/target-pilot/README.md),
product/UI requirements, and ordinary implementation tickets replace that route.
No new intake, atlas certification, family-board sequence, or stage ledger is
required. Complete product coverage remains the intended scope.

Existing backend/domain/API contracts and working frontend code are preserved.
ADR-0007 continues to own frontend technology. Historical implementation
acceptance does not prove conformity to the newly selected target concept.
Responsive Web remains in scope; mobile-specific work requires explicit scope.

## Impact and proof

Documentation/design routing is an intentional `breaking-change`.
Runtime, APIs, persistence, deployment, and existing ticket statuses are
unchanged. Git recovery does not reinstate retired authority; doing so requires
a new owner decision. Checks of documentation and preserved pilot resources
do not certify production functionality, performance, or visual conformance.
