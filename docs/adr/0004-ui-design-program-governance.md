---
doc_id: ADR-0004
title: UI design program governance and target reset
doc_version: 1
product_spec_version: 0.9.5-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: [DOC-RULE-010, WEB-ARCH-001, WEB-ARCH-005]
status: accepted
proof_boundary:
  label: documentation-authority-reset
  exclusions: [accepted-visual-direction, completed-ui-program, browser-runtime, frontend-stack-selection]
---

# ADR-0004: UI design program governance and target reset

- status: `accepted`;
- date: `2026-08-05`;
- decision owner: `product owner`;
- requirement IDs: `DOC-RULE-010`, `WEB-ARCH-001`, `WEB-ARCH-005`;
- supersedes/superseded by: the unexecuted Linear-workspace UI transition route; no successor ADR yet.

## Context

The Linear-workspace visual and frontend standard and the Custometry-specific
transition specification no longer express the intended product direction.
Their W19-W23 delivery graph was not executed, but W19 was still marked ready
and the target stack, themes, reference fidelity, Penpot vNext, and performance
budgets had also leaked into higher-authority product and architecture sources.

The product owner intends to expand the platform and introduce genuinely new
product ideas before accepting a target visual language, screen atlas, frontend
architecture, or rollout plan. Existing route and surface inventories remain
useful current-state evidence, but they cannot be treated as a complete future
product or as accepted visual authority.

## Decision criteria

1. Product meaning must come from the owner brief and normative product
   requirements, not from a third-party visual reference.
2. The next program must cover the complete responsive-Web product rather than
   one shell or golden slice.
3. Current implementation and historical design evidence must not silently
   become the target.
4. Architecture and visual choices must remain reversible until their proper
   evidence and review gates close.

## Options

| Option | Benefits | Costs/risks | Fit |
|---|---|---|---|
| Keep the Linear transition and edit its visuals | Lowest documentation churn | Preserves rejected assumptions and an incomplete product path | Rejected |
| Delete only the two named documents | Removes visible sources | Leaves ready tickets, embedded requirements, and broken dependencies | Rejected |
| Reset target authority and enter `ui-design-program` through pre-G0 intake | Reopens product breadth, creates complete atlas/journey/family/wave coverage, and separates owner acceptance from machine proof | Requires a new detailed brief and accepted visual direction before G0 | Accepted |

## Decision

The Linear-workspace standard, project transition specification, migration
registry, reference manifest, graph, and unexecuted W19-W23 tickets are retired.
They are not active architecture, design, implementation, or execution sources.

`custometry-ui-blueprint-ru.md` becomes the pre-G0 product UI requirements and
current-inventory baseline. It records known roles, outcomes, journeys,
surfaces, states, actions, data meaning, accessibility, localization, and
responsive-Web constraints. It does not select a frontend framework, state
library, component library, theme set, typography, icon set, shell geometry,
motion language, or visual reference.

The next product-wide UI effort must use `ui-design-program`. No G0 program,
prompt pack, or ledger is initialized until the owner brief establishes the
detailed product path and an accepted pilot or bounded pre-G0 visual proposal
establishes one `visual_authority`.

The existing route, route-policy, and surface manifests remain current-state
inventory evidence. Their `116/25/5` historical coverage is not a permanent
ceiling, not the future all-screen atlas, and not visual or browser acceptance.
Historical Penpot evidence remains truthful history only.

## Consequences

- Product expansion and the visual direction are explicitly open for owner
  input before G0.
- The browser frontend stack must be selected by a later architecture decision
  after product scope and platform baseline are known.
- Existing backend/domain/API contracts remain authoritative unless the new
  product requirements deliberately change them through their own compatibility
  decision.
- No frontend implementation ticket is ready after this reset.
- Responsive Web remains in scope; mobile-specific information architecture
  remains unauthorized until the owner explicitly adds it.

## Contract impact and migration

- Documentation and design authority: `breaking-change`; old sources and their
  execution graph are retired.
- Product behavior: `compatible-change` for preserved capabilities; product
  expansion remains unresolved and is not invented by this ADR.
- Runtime, API, persistence, and deployment: `none`; this decision changes no
  implementation or production state.
- Browser and design evidence: previous Penpot evidence is historical only;
  future evidence is produced by the selected `ui-design-program` mode and real
  browser boundary.
- Rollback: restoring the old target requires a new explicit owner decision and
  a current-authority replacement; deleted files cannot become active merely by
  being recovered from Git history.

## Verification and proof boundary

Repository proof consists of blueprint synchronization, link/index validation,
delivery-ticket validation, route/surface contract validation, and the grouped
local documentation/static gate. These checks prove authority consistency only.
They do not prove a new visual direction, complete G0-G6 program, browser
behavior, accessibility conformance, frontend performance, or runtime readiness.

## Re-evaluation triggers

- the owner provides the detailed product expansion brief;
- an accepted pilot or pre-G0 visual proposal exists;
- the target frontend architecture must be selected;
- mobile-specific scope is explicitly authorized;
- the current route/surface inventory is replaced by a complete G1 atlas.
