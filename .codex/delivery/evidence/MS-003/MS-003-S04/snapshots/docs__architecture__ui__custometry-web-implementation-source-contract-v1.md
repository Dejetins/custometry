---
doc_id: ARCH-UI-WEB-IMPLEMENTATION-SOURCE-001
title: Custometry Web implementation source contract
doc_version: 5
product_spec_version: 0.11.0-draft
ui_spec_version: 0.9.0-draft
visibility: internal
ship: false
owner: engineering
requirement_ids: [WEB-ARCH-003, WEB-ARCH-004, WEB-ARCH-005, WEB-ARCH-006, UI-SHELL-001, UI-SHELL-002, UI-SHELL-003, A11Y-001, I18N-001]
status: active
proof_boundary:
  label: repository-web-implementation-routing-and-reference-contract
  exclusions: [product-runtime-readiness, browser-acceptance, release-readiness]
---

# Custometry Web implementation source contract

## Decision and execution authority

On 2026-09-04 the owner selected the final interactive pilot as the target UI
concept and authorized removal of the G0-G6 program and generated materials.
The [retirement record](ui-program-retirement.md) identifies the exact historical
commit and recovery boundary. Deleted boards, prompts, ledgers, suspension
markers, and stage receipts are no longer active dependencies.

The owner adopted [hierarchical planning](../planning/framework-v1/README.md)
on 2026-09-06 for all development directions, including Web. New milestone work
uses the accepted plan, prompt pack and one canonical iteration journal; separate
bounded tickets retain their declared status authority. A graph is topology only.
The retired G0-G6 program, certification layers and historical ledgers remain
inactive; adopting the new framework does not restore them. Existing product,
visual-source and browser-proof requirements below remain unchanged.

## Source precedence for implementation

Read only the smallest applicable set:

1. `custometry-technical-blueprint-ru.md` and its synchronized human mirror
   for normative business semantics, contracts, and requirement IDs;
2. `custometry-ui-blueprint-ru.md` and executable route/surface contracts for
   surface identity, roles, states, permissions, and responsive intent;
3. the [target pilot](target-pilot/README.md), its byte-pinned entrypoint and
   decision notes for the demonstrated composition, navigation, analytical
   controls, interactions, density, and visual language;
4. accepted architecture, especially ADR-0007, for production technology and
   dependency boundaries;
5. production code, focused tests, and observed browser evidence for the
   current implementation and its gaps.

The pilot is a target concept, not merely a visual-language anchor. Its
demonstrated structures and interactions should be implemented faithfully.
It is also a fixture-backed prototype: it neither changes backend contracts
nor proves production API, persistence, permissions, accessibility, or responsive
readiness. Screens not shown in the pilot retain their product requirements;
derive coherent patterns from the pilot without forcing every screen into the
same composition. Resolve a material conflict or a non-derivable product/design
decision with the owner before implementation.

The existing frontend remains working implementation evidence. Removing
the design program does not roll it back or certify its conformity. Alignment
to the target concept is subsequent, bounded implementation work.

## Execution unit and proof contract

Every Web implementation unit (ticket or milestone stage) names exact screen or surface IDs, requirement
IDs, user-visible outcomes, dependencies, and safely separable path ownership.
It produces working production UI, focused automated tests, and real-browser
evidence for the changed boundary. Design-only boards, broad pre-implementation
state matrices, or copied program receipts do not satisfy a ticket.

Browser proof covers critical changed states, relevant en/ru behavior,
keyboard/focus and accessibility smoke, console/network failures, and responsive
Web endpoints. Use 768 CSS px and 1920 CSS px as required endpoint anchors
when applicable, adding intermediate widths only when layout risk or a declared
breakpoint warrants them. This is boundary-matched smoke, not a claim of full
WCAG conformance or exhaustive every-state-by-every-anchor coverage.
Mobile-specific design remains unauthorized.

Each browser-depth execution unit (ticket or milestone stage) owns a Playwright
configuration below its declared `tests/e2e/<unit-slice>/` path. It uses Playwright's `webServer` lifecycle to
start host Vite on an explicit loopback port, wait for readiness, fail on startup
error, and clean up. It discovers only unit-owned specs and declares desktop
Web projects for `768x1024` and `1920x1080`; it does not depend on a pre-existing
`CUSTOMETRY_BASE_URL`, reuse the historical foundation-only config, or enable
a sub-768 mobile project.

Evidence is written once at the implementation boundary. Source checks do not
prove browser, API, persistence, Compose, release, or production behavior.
Publication and deployment require explicit authority.

## Existing topology and next work

The existing dependency/path topology is
`.codex/delivery/graphs/custometry-web-implementation-frontier-v1.json`.
Read live ticket frontmatter and accepted dependency evidence before choosing
work; the graph's existence is not a declaration that W31 or any successor is
ready. Historical ticket evidence describes its original implementation basis,
not acceptance against the newly selected target concept.

Plan remaining cohesive product slices through the framework with the owner; execute the selected milestone or independent-ticket route.
This cleanup does not activate a new W39 frontier or implement a UI redesign.

## First-run entry increment — MS-002-S03

The root `/` now composes the installation entry directly, outside the legacy
workspace shell. Its shared `pilot-entry/v1` primitives live in
`packages/ui-foundation/src/installation.tsx`; existing theme IDs and feature
routes retain their previous behavior. The preserved FoundationHome remains a
compatibility source, not an accepted target design.

The entry inherits the pilot's graphite palette, 17px heading, 14px base type,
10px panels, 7px controls, cyan primary action and 2px focus treatment. Its
720px single-column status composition is derived for an installation with no
workspace, rather than copying the pilot's report/navigation composition.
The typed operational adapter consumes S02 status including HTTP 503; Query
owns refetch/cancellation and hides retained successful data after errors.
Public help is linked by localized catalog URL. No account or domain truth is
stored in the browser.

[Stage evidence](../../../.codex/delivery/evidence/MS-002/MS-002-S03/report.md)
separates host-Vite/real-API behavior from normalized source comparison. S04
must package these sources with S02 API in a new identified bundle; S05 retains
the owner's final visual decision. This does not expand product-route coverage.

## Bounded report workspace — MS-003-S04

The current capability inventory below narrows the `implemented` marker in the
[route registry](../../../packages/contracts/routes/ui-routes.json) and
[execution contracts](../../../packages/contracts/routes/ui-route-contracts.json).
Those markers identify a working bounded route, not completion of every target
capability on that screen. Route identities and workspace-aware path/query shapes
are unchanged; the prepared access details supply the workspace UUID.

| Route | Implemented capability | Deferred target capability |
|---|---|---|
| UI-AUTH-001 | Real ordinary-analyst email/password session, workspace identifier, RU/EN, failure/re-entry | Password recovery, remember-device settings, administrative setup |
| UI-RPT-001 | Authorized saved-draft library and supplied sales template | Publication, delivery scheduling, arbitrary templates |
| UI-RPT-002 | Title, source version, dates, Store, same-date previous-year comparison; explicit Apply and CAS Save | Block builder, segments, product/customer analysis |
| UI-RPT-003 | Exact saved draft/page preview, canonical SVG line and full accessible tables, Result Trust, Focus | Published reports, email/XLSX/export, full renderer certification |

[The implementation](../../../apps/web/src/features/reports/ReportWorkspace.tsx)
uses shared `reportThemeVariables` and bilingual `reportCopy`; the preserved
pilot remains the visual authority. Its rail, document hierarchy, metric rail,
chart/table panel, inspector and Focus are applied to the receipt-total subset.
The editor adds the required explicit title/source/date inputs; unsupported pilot
controls are omitted. Canonical S03 system BrandProfile tokens determine chart
colors. The inspector moves below the chart at the narrow desktop endpoint.

TanStack Query owns server results, drafts and versioned projections. Component
state holds only unsaved controls/presentation; a session-scoped memory map retains
unsaved inputs across history navigation. Only locale preference enters
localStorage. Authorization failure clears protected queries and draft memory,
hides protected content, and rejects late responses from the previous generation.
A 409 retains input and offers explicit reload. Apply never silently replaces a
saved snapshot; Save pins the calculated result. Exact reopen validates the page
locator and reads immutable artifacts without calculation.

[Stage evidence](../../../.codex/delivery/evidence/MS-003/MS-003-S04/report.md)
records real host Vite/production API/owned PostgreSQL/artifact browser proof,
RU/EN at 768x1024 and 1920x1080, keyboard/Focus and 200% layout zoom smoke.
This source increment does not certify packaged HTTPS, full accessibility or
complete design-system fidelity; S05 packages it and S06 retains owner review.
User-facing [report help](../../../docs-site/docs/user-guide/reports.md) explains
entry details, Apply/Save and recovery without backend implementation jargon.
