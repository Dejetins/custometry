---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: W21-CONTRACT-COMPILED-UI-PILOT
proof_boundary: product-owner-selected-machine-conformant-reproducible-two-render-figma-ui-an-003-design-process-pilot
proof_skills: [figma:figma-use, product-design:ideate, product-design:audit, better-interface]
verdict: passed
redaction: No credentials, cookies, browser storage, private product data, or provider payloads are retained. Figma screenshots contain only synthetic Northwind Retail UI data. Short-lived Figma asset URLs and browser session state were not persisted.
executed_checks:
  - confirm the exact empty baseline of Figma library hX3nQOtcSdCc97uv26m9eG page 0:1 and product MXfxuhSFpIczbUtFmOSyPp page 0:1 before mutation
  - generate exactly three isolated 1440 by 900 graphite success-state explorations and record the user-selected identity ui-an-003-graphite-direction-c-compact-v4
  - validate the 42-token 15-component 26-icon restricted UI-AN-003 contract and nine canonical plus negative-fixture tests
  - compile and check the deterministic render plan with manifest digest a5a324263d0cfa88e9af3e1d87a6ff5cdb1d49d0e893ff598e3183db7c31ecbd and renderer 1.0.0
  - publish the minimum Custometry UI Library slice and read back 44 of 44 roots at publish status CURRENT
  - prove remote variable import remote component import instance creation key preservation and proof-instance cleanup at the exact cross-file boundary
  - render candidate nodes 35:311 and 40:536 from the same manifest and compare normalized receipts and PNG bytes
  - run abyss graphite frost and paper semantic-mode verification renders without separate aesthetic acceptance
  - run a Russian copy-fit verification at actual sidebar toolbar table and inspector widths
  - move notifications into the global header, place the Codex-like context-actions trigger on the inspector axis below it, align chart fullscreen exactly above table export, replace the filter glyph with a funnel, group compact Copy link and Send by email actions in the inspector, and synchronize all six complete screens
  - uv run python -m tools.custometry_quality.ui_design.validate
  - uv run python -m tools.custometry_quality.ui_design.compile_render_plan --check --output .codex/delivery/evidence/assets/W21-CONTRACT-COMPILED-UI-PILOT/ui-an-003.render-plan.v1.json
  - uv run pytest tests/ui_design -q
  - uv run ruff check tools/custometry_quality/ui_design tests/ui_design
  - uv run pyright tools/custometry_quality/ui_design tests/ui_design
  - uv run python -m tools.custometry_quality.validate_blueprints
  - uv run python -m tools.custometry_quality.validate_delivery_tickets
  - uv run python -m tools.custometry_quality.validate_repository_layout
  - uv run python -m tools.check --scope local
  - git diff --check
observations:
  - The selected exploration was explicitly accepted by the product owner before token component manifest or Figma construction began.
  - The final library has 42 variables in two collections five text styles 16 registered component roots and 28 icon components; every one of the 44 publishable roots is CURRENT.
  - The accepted product node 40:536 contains nine registered region instances 79 total instances 37 icon instances zero detached regions zero raw small rectangle icons zero unbound text styles and zero unbound semantic paints.
  - Candidate A and B share normalized semantic digest 08314ced6c1fdb3102801399dbdbc742a67294263dd7b5fb9dd107c5cd11b8b5 and identical PNG SHA-256 c721dd7c24bfcde40c9bff71a8be42d51acb535eeb2eff9860a09d5f16b7e0a1.
  - The post-acceptance user repair is published and synchronized to Candidate A Accepted and all four theme screens — notifications and context actions share screen x 1344 on separate vertical levels, chart fullscreen and table export share screen x 1112, and both share commands are reusable compact 216 by 32 px instances.
  - The Russian verification contains 35 bounded containers and 73 token-and-style-bound text nodes with zero detected overflow; it is verification-only and is not represented as another accepted screen.
  - Machine conformance is passed product decision is accepted and implementation readiness remains not_assessed because this ticket proves design-process output rather than browser or production behavior.
---

# W21-CONTRACT-COMPILED-UI-PILOT Evidence

> Compact evidence for one terminal ticket. It is not another execution-state
> source or a replacement for the product specification.

## Outcome and scope

- outcome: the selected premium Linear-style `UI-AN-003` Sales Overview
  direction was compiled from versioned contracts into a published minimum
  Figma library slice, rendered twice into isolated product candidates,
  audited by read-back, and accepted at the declared design-process boundary;
- requirement IDs: [WEB-ARCH-003, WEB-ARCH-005, WEB-ARCH-006, THEME-001,
  THEME-002, THEME-003, THEME-005, THEME-008, UI-DENSITY-001,
  UI-DENSITY-002, UI-DENSITY-003, FILTER-001, FILTER-002, FILTER-003,
  FILTER-004, FILTER-010, COMPARE-001, COMPARE-002, COMPARE-003,
  CHART-001, CHART-002, CHART-006, A11Y-001, A11Y-003];
- included: the ticket-owned UI design contracts and compiler, their tests and
  negative fixtures, exact authorized Figma library and product files, and the
  ticket evidence assets listed below;
- exclusions: no application code, API, route, permission, persistence,
  analytics, deployment, production data, browser runtime, keyboard behavior,
  screen-reader behavior, reduced-motion implementation, real export, or
  production readiness is claimed.

## Authority, baseline, and selection

| Boundary | Result | Observation |
| --- | --- | --- |
| Library identity | pass | Figma Design `hX3nQOtcSdCc97uv26m9eG`, Page 1 `0:1`. Initial top-level children, local collections, variables, and styles were all zero. |
| Product identity | pass | Figma Design `MXfxuhSFpIczbUtFmOSyPp`, Page 1 `0:1`. Initial top-level children, local collections, variables, and styles were all zero. |
| Frozen screen contract | pass | Route `/w/:workspaceKey/analytics/sales`, role `AN`, success state, 1440x900, graphite, required actions and regions remained unchanged. |
| Exploration set | pass | Exactly three independent images are retained as `exploration-a.png`, `exploration-b.png`, and `exploration-selected.png`. |
| Product selection | accepted | User accepted `ui-an-003-graphite-direction-c-compact-v4` on 2026-07-31 before Figma mutation. The visual decision is versioned in `packages/contracts/ui-design/visual-decisions.ui-an-003.v1.json`. |

Exploration SHA-256 identities:

- A: `bc4fbc3f193d3d084e2d6cd012d171aa05e415ae1fb3e4969f0383a9f2dbb318`;
- B: `45fa1d24f6187215868f22a461ba84a1f6ea8814907b402cf20eef8e486c41da`;
- selected: `397b16bb3460a0dde99cb097a4bb833872ee3d2788f5bf74c795cac55c815e6d`.

## Contract and compiler slice

| Artifact | Version / identity | Observed result |
| --- | --- | --- |
| Token contract | `custometry.ui-design.tokens/v1`, `1.0.0` | 42 tokens; exact themes `abyss`, `graphite`, `frost`, `paper`. |
| Component registry | `custometry.ui-design.components/v1`, `1.0.0` | 16 registered component roots with exact Figma keys. |
| Icon registry | `custometry.ui-design.icons/v1`, `1.0.0` | 28 monochrome component icons with exact Figma keys. |
| Restricted manifest | `custometry.ui-design.screen-manifest/v1`, `1.0.0` | Nine required regions, registered actions only, exact target identities, no raw construction keys. |
| Renderer | `1.0.0` | Deterministic plan digest `a5a324263d0cfa88e9af3e1d87a6ff5cdb1d49d0e893ff598e3183db7c31ecbd`. |
| Negative fixtures | 7 fail-closed classes | Raw node, unknown component, forbidden action, missing region, detached instance, target drift, and unknown version are rejected. |

The compiler allowlist contains only `candidate-root`, `application-grid`, and
`primary-content-stack` as structural wrappers. Every visible product region
in the receipt is required to read back as an `INSTANCE` with a published
component key.

## Figma library and cross-file gate

Final library inventory:

- `Custometry / Theme`: key
  `9d940eb036cbfd021501a403ebf72a5fd3131e6e`, 17 variables, four modes;
- `Custometry / Foundation`: key
  `208186b9d397dad4738ba4803ce5b868294e38da`, 25 variables, one mode;
- five published Inter text styles;
- 16 registered roots and 28 icon roots, all `CURRENT`;
- registry binding audit: 129 text nodes, 400 semantic solid paints, 81
  nested instances, zero missing text-style bindings, zero unbound paints.

The exact cross-file recheck imported remote variable
`color/bg/window` key `18d4d12552033e6b9f00e2481ef8f3120721ed73`
and published button variant key
`c25505192d94125b8e3ff3a7a46d8cdf1f7dd364`, created an `INSTANCE` whose
main-component key matched, and removed it. Product top-level count was seven
before and after cleanup.

## Deterministic product renders and repair history

| Dimension | Candidate A | Candidate B / accepted |
| --- | --- | --- |
| Node | `35:311` | `40:536` |
| Candidate ID | `UI-AN-003--success--graphite--render-a` | `UI-AN-003--success--graphite--render-b` |
| Lifecycle | `candidate` | `accepted` |
| Machine conformance | `passed` | `passed` |
| Product decision | `accepted_direction` | `accepted` |
| Implementation readiness | `not_assessed` | `not_assessed` |
| Repairs | 2 | 0 |
| Regions / detached | 9 / 0 | 9 / 0 |
| Total / icon instances | 79 / 37 | 79 / 37 |
| Text / unbound styles | 117 / 0 | 117 / 0 |
| Solid paints / unbound | 278 / 0 | 278 / 0 |
| PNG SHA-256 | `c721dd7c24bfcde40c9bff71a8be42d51acb535eeb2eff9860a09d5f16b7e0a1` | same |
| Normalized receipt digest | `08314ced6c1fdb3102801399dbdbc742a67294263dd7b5fb9dd107c5cd11b8b5` | same |

Bounded repair attempts on Candidate A:

1. Reordered the shell behind the allowed content wrappers after the first
   read-back exposed incorrect visual stacking.
2. Corrected the chart's June axis-label position and the compact trust
   trigger's dot/value alignment in the registered library roots, republished
   them, and resynchronized the candidate.

All invalidated binding, instance, screenshot, and receipt checks were rerun.
Candidate B was then rendered cleanly from the final published library and
required no repair. The final screenshots are byte-identical, so the bounded
visual diff is zero of 1,296,000 pixels.

After acceptance, successive annotated product-owner reviews authorized a
focused UI repair. `Page/Header` keeps the unread notification action at screen
`x=1344`, `y=24` and global overflow at its far-right edge. The published
`Context/Inspector` now places the Codex-like context-actions trigger directly
below it at screen `x=1344`, `y=106`, so the two controls exchange their former
roles without duplicating notification state. The compact `Chart/Toolbar` is
508 px wide and shifted 40 px right; its filter uses the conventional funnel
glyph and its sole fullscreen action is at screen `x=1112`. `Table/Channel`
places overflow at screen `x=1072` and export at `x=1112`, making fullscreen
and export exactly collinear across blocks. The inspector is grouped into
`ON THIS PAGE`, `VIEW`, and `SHARE`, with published `Context/Action Row`
instances for `Copy link` and `Send by email`; both are `216×32`, matching the
ordinary control height. A published `Control/Text Tab` component set
continues to provide fixed `48×32` default, active, hover, and active-hover
Chart/Data variants using an `ON_HOVER` 120 ms dissolve and no layout shift.
Header, toolbar, table, and inspector instances were resynchronized on
Candidate A, Accepted, and all four theme screens. All six read back with the
same axes, icons, grouping, and compact action sizes. This user-authorized
change is recorded separately from Candidate A's original two-attempt
machine-repair budget.

## Theme and locale verification

| Verification | Node | Result | Screenshot |
| --- | --- | --- | --- |
| abyss `4:0` | `42:859` | 9 regions, 0 detach, semantic control `#142533` | `theme-abyss.png` |
| graphite `4:1` | `42:1194` | 9 regions, 0 detach, semantic control `#1B2C3B` | `theme-graphite.png` |
| frost `4:2` | `42:1529` | 9 regions, 0 detach, semantic control `#DDE8ED` | `theme-frost.png` |
| paper `4:3` | `42:1864` | 9 regions, 0 detach, semantic control `#E4E9EC` | `theme-paper.png` |
| Russian copy fit | `46:2475` | 35 bounded containers, 73 styled texts, 0 overflow, 0 unbound style/paint | `figma-locale-stress-ru.png` |

The theme sweep proves semantic-token compatibility only; it is not four
separate visual acceptances. Published remote instances do not expose text
component properties in this minimum slice, so the Russian run is a separate
verification-only copy-fit matrix using the actual 240 px sidebar, compact
toolbar, dense table, and 208 px inspector value widths. It does not detach or
masquerade as another accepted product candidate. Exposing localized component
properties remains a future library-extension decision.

## Durable evidence assets

The directory
`.codex/delivery/evidence/assets/W21-CONTRACT-COMPILED-UI-PILOT/`
contains:

- frozen exploration images and selected identity;
- pre-repair and final Candidate A screenshots plus final Candidate B;
- the library-level header-control repair screenshot and structured repair receipt;
- four semantic theme screenshots and the Russian copy-fit screenshot;
- deterministic render plan, both render receipts, normalized reproducibility
  comparison, cross-file proof, library/product audits, theme sweep, and locale
  stress receipts.

No short-lived Figma URLs, browser session state, credentials, cookies, or
private data are retained.

## Commands and observations

| Command or action | Result | Redacted observation / durable reference |
| --- | --- | --- |
| `uv run python -m tools.custometry_quality.ui_design.validate` | pass | 42 tokens, 16 components, 28 icons, nine regions, exact candidate target. |
| render-plan `--check` | pass | Artifact matches deterministic compiler output; digest `a5a32426...ecbd`, renderer `1.0.0`. |
| actual receipt audit | pass | Both receipts pass and normalize to `08314ced...8b5`. |
| `uv run pytest tests/ui_design -q` | pass | 9 tests passed, including all declared fail-closed classes. |
| `uv run ruff check tools/custometry_quality/ui_design tests/ui_design` | pass | No findings. |
| `uv run pyright tools/custometry_quality/ui_design tests/ui_design` | pass | 0 errors, 0 warnings. |
| `uv run python -m tools.custometry_quality.validate_blueprints` | pass | 953 requirement IDs, spec `0.9.4-draft`. |
| `uv run python -m tools.custometry_quality.validate_delivery_tickets` | pass | Final accepted ticket and evidence reference validate. |
| `uv run python -m tools.custometry_quality.validate_repository_layout` | pass | Repository layout validates with ticket-owned additions. |
| `uv run python -m tools.check --scope local` | pass | Grouped local source/document/tooling gate passed; no runtime claim. |
| `git diff --check` | pass | No whitespace errors. |

## Contract impact and decision

| Surface | Classification | Result |
| --- | --- | --- |
| Product semantics, routes, permissions, API, persistence | `none` | No normative or runtime contract changed. |
| UI design contracts | `compatible-change before first consumer` | Versioned pilot-only schema, registry, manifest, compiler, and evidence were added. |
| Figma library | `compatible minimum slice` | Exact published variables, styles, components, and icons exist for UI-AN-003 only. |
| Figma product file | `compatible design artifact` | One accepted candidate, one reproducibility peer, and bounded verification frames exist at the authorized target. |
| Runtime implementation | `not_assessed` | No application source or browser surface changed. |

Decision: **scale** the contract-compiled process to the next explicitly
authorized screen slice, reusing the versioned contracts, fail-closed compiler,
cross-file gate, two-render receipt comparison, and lifecycle metadata. Do not
expand this pilot into a global component index or runtime implementation
without a new ready ticket. The next safe action is to define that screen's
frozen contract and require a fresh product-owner selection before adding its
library slice.

## Verdict

`passed` at the declared product-owner-selected, machine-conformant,
reproducible two-render Figma design-process boundary. The accepted identity is
product node `40:536` in `MXfxuhSFpIczbUtFmOSyPp`; machine conformance is
`passed`, product decision is `accepted`, and implementation readiness remains
`not_assessed`.
