---
doc_id: CONTRACT-UI-SURFACE-001
title: UI surface coverage contract
doc_version: 6
product_spec_version: 0.10.0-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: [UC-001, UC-002, UC-003, UC-004, UC-005, UC-006, UC-007, UC-008, UC-009, UC-010, UC-011, UC-012, UC-013, UC-014, UC-015, UC-016, UC-017, UC-018, UC-019, UC-020, UC-021, UC-022, UC-023, UC-024, UC-025, UC-026, UC-027, UC-028, UC-029, ROUTE-001, RBAC-002, RBAC-019, RBAC-020, RBAC-027, OUTLIER-001, SEGMENT-001, DISCOUNT-001, PVM-001, METHOD-009, METRIC-017]
status: accepted
proof_boundary:
  label: static-ui-surface-coverage
  exclusions: [ui-program-visual-conformance, browser-behavior, api-authorization, runtime-implementation]
---

# UI Surface Coverage Contract

## Purpose

Route parity is not requirement coverage. Custometry therefore keeps a
machine-readable UI surface manifest at
`packages/contracts/routes/ui-surface-contracts.json`. It binds every
UI-visible product use case to one or more canonical routes, overlays, system
surfaces, or cross-surface capability contracts. Its JSON Schema is stored next
to it.

The current-state inventory contains 117 route-level pages, 25 overlays, 5 system
surfaces, and 22 cross-surface capabilities. W08 accepted historical Penpot revision 181
with the first 110 route frames, all overlays/system surfaces, C24, and flow 09.
The controlled W10 baseline recovery established revision 197; W10 then
accepted all six Organization/People routes, C25, and flow 10 at terminal
revision 213 with inventory `116/25/5`. These are observed identity/domain
counts; the current route registry has since expanded to 117 rows. Neither
count is a permanent route ceiling, future G1 atlas, or proof of the new Web
target.

## Authority and agent load order

An agent performing UI architecture, `ui-design-program`, or Web work loads sources in this
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

Historical Penpot is evidence only. It may reveal a current-inventory delta,
but it does not override the product blueprint, executable contracts, accepted
UI-program visual authority, or current gate evidence.

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

- product use cases `UC-001...UC-029` are present exactly once in the coverage
  binding set and each has at least one valid surface;
- every referenced route exists in both route manifests and the UI blueprint;
- overlay, system-surface, and cross-surface capability IDs, names, and complete
  requirement-reference sets match the UI blueprint exactly;
- every surface requirement ID exists in the product blueprint;
- all 117 routes have English/Russian title parity and executable route policy;
- legacy Penpot identity metadata remains internally consistent while it is
  retained for historical traceability.

JSON Schema proves portable shape. The repository semantic validator proves
cross-file identity, product requirement, permission, localization, and legacy
historical count relationships. Neither proves rendered design, browser behavior,
authorization enforcement, accessibility, or runtime readiness.

## Historical Penpot baseline

- file ID: `7cd71457-8d32-8044-8008-549f83bb4645`;
- current working name: `custometry`;
- W03 accepted historical audit revision: `124`;
- W05 accepted complete architecture delta revision: `156`;
- W06 accepted analytics-density repair revision: `164`;
- W08 accepted discount/methodology Penpot delta revision: `181`;
- W10 controlled start baseline revision: `197`;
- W10 accepted terminal revision: `213`;
- structurally stable and visually reviewed route frames: `116`;
- structurally stable and visually reviewed overlays: `25`;
- structurally stable and visually reviewed system surfaces: `5`;
- current known route rows for UI requirements `0.8.0-draft`: `117`;
- current known overlays for UI requirements `0.8.0-draft`: `25`;
- target cross-surface capabilities: `22`.

The file ID and revisions describe historical identity only. W03/W05/W06/W08
evidence and ticket state remain immutable. Future program work does not write
this file or use it as a current start guard.

## Population treatment and segmentation surface decision

`UC-025` and `UC-026` reuse the existing analytics, segmentation, and research
routes because the durable lifecycle already belongs to analysis and segment
definitions/versions. `UI-OVR-025` provides contextual treatment diagnostics
and sensitivity inspection. `UI-CAP-018` owns the reusable population-treatment
policy and `UI-CAP-019` owns the bucket, stratified, and exact-K KMeans builder
contract. This keeps URLs stable while making methods, fitted parameters,
exclusion effects, group counts, model/seed identity, and Result Trust visible.

## Discount and methodology-trust surface decision

`UC-027` reuses `UI-DATA-008/010/013/014/021/022` and
`UI-AN-002/010/011/012/014`. Durable dataset, metric, method, analysis, result,
and research lifecycles already own the relevant URLs. `UI-CAP-020` owns the
reusable component-discount, effective-policy/cap, PVM, certification/proxy,
and method-availability presentation contract. No new route or overlay is
created solely for controls. The `0.6.2` Penpot delta adds C24 and updates the
declared existing frames from accepted revision 164; W08 accepted it at 181.
`W08-PENPOT-ANALYTICS-BASELINE-RECOVERY` restored `UI-AN-002` and the
non-overlapping `UI-AN-011` authoring structure; the later controlled recovery
established revision 197 as W10's safe start without changing route or product
identity.

## Organization and contributor-insight surface decision

`UC-028` receives `UI-ORG-001/002` and `UI-ADMIN-019/020` because organization
structure, department policy, grants, ownership, version conflicts, and dirty
editing require durable deep links and independent authorization/history.
`UC-029` receives `UI-PEOPLE-001/002` because the contributor directory/profile
are bookmarkable privacy-scoped views. No new overlay is required.
`UI-CAP-021` owns effective-access/ownership behavior reused across routes, and
`UI-CAP-022` owns privacy-safe contributor cards/activity projection. W10
accepted the six frames, C25, and flow 10 at terminal revision 213.

## `ui-design-program` successor boundary

The accepted W10 file remains historical route, domain, and composition
evidence. UI requirements `0.8.0-draft` do not select a new visual or frontend
target. Stable current route IDs, overlays, systems, and capability bindings are
inputs to pre-G0 intake, but the future G1 atlas may expand them from product
requirements and owner intent. No W10 frame or legacy `penpot_status` is
relabeled as current design, browser, or program acceptance.

## Change and proof rules

Adding or removing a current route updates the UI blueprint, identity registry,
executable manifest, localization catalogs, surface bindings, schemas when
their shape changes, validators, and current program inventory when one exists.
Legacy historical metadata changes only when its factual provenance changes.
Adding an overlay, system surface, or cross-surface capability updates
the UI blueprint and surface manifest together.

An audit may recommend a new route only by applying the decision policy and
showing why an existing route, tab, query state, drawer, modal, or reusable
component is insufficient. It may not change normative product behavior or
mutate a design source without current program authority.
