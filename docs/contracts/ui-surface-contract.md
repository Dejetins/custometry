---
doc_id: CONTRACT-UI-SURFACE-001
title: UI surface coverage contract
doc_version: 2
product_spec_version: 0.9.1-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: [UC-001, UC-002, UC-003, UC-004, UC-005, UC-006, UC-007, UC-008, UC-009, UC-010, UC-011, UC-012, UC-013, UC-014, UC-015, UC-016, UC-017, UC-018, UC-019, UC-020, UC-021, UC-022, UC-023, UC-024, UC-025, UC-026, ROUTE-001, RBAC-002, OUTLIER-001, SEGMENT-001]
status: accepted
proof_boundary:
  label: static-ui-surface-coverage
  exclusions: [penpot-visual-conformance, browser-behavior, api-authorization, runtime-implementation]
---

# UI Surface Coverage Contract

## Purpose

Route parity is not requirement coverage. Custometry therefore keeps a
machine-readable UI surface manifest at
`packages/contracts/routes/ui-surface-contracts.json`. It binds every
UI-visible product use case to one or more canonical routes, overlays, system
surfaces, or cross-surface capability contracts. Its JSON Schema is stored next
to it.

The current target contains 110 route-level pages, 25 overlays, 5 system
surfaces, and 19 cross-surface capabilities. W03 accepted Penpot revision 124
as a historical baseline with 91 route frames, 23 overlay frames, and all 5
system surfaces. The remaining 19 routes plus `UI-OVR-024` and `UI-OVR-025` are
design backlog. These are observed and target counts, not a permanent route
ceiling.

## Authority and agent load order

An agent performing UI architecture, Penpot, or Web work loads sources in this
order:

1. `AGENTS.md` and `.codex/AGENTS.md` for authority and delivery rules.
2. `custometry-technical-blueprint-ru.md` for normative product behavior.
3. `custometry-technical-blueprint-human-ru.md` as the synchronized
   explanatory mirror.
4. `custometry-ui-blueprint-ru.md` for human-readable UI composition and
   interaction.
5. `packages/contracts/routes/ui-routes.json` for stable route identity.
6. `packages/contracts/routes/ui-route-contracts.json` for executable route
   guards, permissions, states, history, and design status.
7. `packages/contracts/routes/ui-surface-contracts.json` for complete
   requirement-to-surface coverage and route-decision rationale.
8. The applicable ready delivery ticket for exact write scope and evidence.

Penpot is design evidence. It may reveal a delta, but it does not override the
product blueprint or executable contracts.

## Surface decision policy

A capability receives a standalone route when at least one condition applies:

- it owns a durable entity or version lifecycle;
- notification, audit, bookmark, or support flows require a deterministic deep
  link;
- it needs independent Back, refresh, recovery, or unsaved-change behavior;
- it has an independent permission boundary and complex recoverable state.

A transient confirmation or contextual inspector remains an overlay when it
has no independent lifecycle and always returns to an owning route. Reused
governed behavior such as `vs LY`, filters, Chart-to-Data, Result Trust,
formatting, comments, PII-safe rendering, population treatment, segmentation
previews, and progress becomes a cross-surface capability contract.

The current route count must never be used to force a new durable resource into
an overloaded existing frame.

## Completeness invariant

Static acceptance requires all of the following:

- product use cases `UC-001...UC-026` are present exactly once in the coverage
  binding set and each has at least one valid surface;
- every referenced route exists in both route manifests and the UI blueprint;
- overlay, system-surface, and cross-surface capability IDs, names, and complete
  requirement-reference sets match the UI blueprint exactly;
- every surface requirement ID exists in the product blueprint;
- all 110 routes have English/Russian title parity and executable route policy;
- the Penpot file ID is canonical, while revision drift is recorded rather than
  silently treated as a different file.

JSON Schema proves portable shape. The repository semantic validator proves
cross-file identity, product requirement, permission, localization, and Penpot
count relationships. Neither proves rendered design, browser behavior,
authorization enforcement, accessibility, or runtime readiness.

## Canonical Penpot baseline

- file ID: `7cd71457-8d32-8044-8008-549f83bb4645`;
- current working name: `custometry`;
- W03 accepted historical revision: `124`;
- observed pages: `47`;
- structurally and visually verified route frames: `91`;
- verified overlay frames at W03: `23` of the then-target `24`;
- verified system surfaces at W03: `5` of `5`;
- target route frames for UI specification `0.6.1-draft`: `110`;
- target overlays for UI specification `0.6.1-draft`: `25`;
- target cross-surface capabilities: `19`.

The file ID is the stable identity. A revision change is expected during design
work and must be recorded by the audit. A file-ID mismatch is a hard stop.
W03 evidence and ticket state remain immutable: subsequent work records a new
start/end revision and contract fingerprint instead of rewriting revision 124.

## Population treatment and segmentation surface decision

`UC-025` and `UC-026` reuse the existing analytics, segmentation, and research
routes because the durable lifecycle already belongs to analysis and segment
definitions/versions. `UI-OVR-025` provides contextual treatment diagnostics
and sensitivity inspection. `UI-CAP-018` owns the reusable population-treatment
policy and `UI-CAP-019` owns the bucket, stratified, and exact-K KMeans builder
contract. This keeps URLs stable while making methods, fitted parameters,
exclusion effects, group counts, model/seed identity, and Result Trust visible.

## Change and proof rules

Adding or removing a route updates the UI blueprint, identity registry,
executable manifest, localization catalogs, surface bindings, schemas when
their shape changes, validators, and Penpot backlog/baseline evidence in one
change. Adding an overlay, system surface, or cross-surface capability updates
the UI blueprint and surface manifest together.

An audit may recommend a new route only by applying the decision policy and
showing why an existing route, tab, query state, drawer, modal, or reusable
component is insufficient. It may not change normative product behavior or
edit Penpot unless a later ticket explicitly authorizes those writes.
