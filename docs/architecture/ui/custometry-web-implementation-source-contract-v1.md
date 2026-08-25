---
doc_id: ARCH-UI-WEB-IMPLEMENTATION-SOURCE-001
title: Custometry Web implementation source contract v1
doc_version: 1
product_spec_version: 0.10.0-draft
ui_spec_version: 0.8.0-draft
visibility: internal
ship: false
owner: engineering
requirement_ids: [WEB-ARCH-003, WEB-ARCH-004, WEB-ARCH-005, WEB-ARCH-006, UI-SHELL-001, UI-SHELL-002, UI-SHELL-003, A11Y-001, I18N-001]
status: active
proof_boundary:
  label: repository-web-implementation-routing-and-reference-contract
  exclusions: [product-runtime-readiness, browser-acceptance, release-readiness, ui-program-certification]
---

# Custometry Web implementation source contract v1

## Decision and execution authority

The owner retired `CUSTOMETRY-UI-DESIGN-PROGRAM-V2` from current execution on
2026-08-24. The triad under
`.codex/delivery/ui-design-programs/custometry-v2/` and
`.codex/agents/generated/custometry-ui-design-g0-v2/` is frozen read-only
historical evidence. It must not be selected by `staged-plan-runner`, resumed,
claimed, or used to certify G4, G5, G6, or program completion.

Current Web implementation executes one bounded delivery ticket at a time.
Ticket frontmatter is the status authority. A coordination graph may record
dependencies and disjoint path ownership, but it is not a status register.
No prompt pack, stage ledger, generated-prompt inventory, or duplicated
certification layer is part of this route.

## Frozen frontier snapshot

This compact snapshot records the last safe boundary without copying the
program's thousands of inventory entries:

- ledger: `.codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md`;
- observed SHA-256: `81961ed673f50a43a5cb4225da99b25ce6d4a23ba0aea58a20bcd6a0bc802158`;
- observed header: `ledger_status: active`,
  `current_stage: G4@family.ops.shell-workspace.baseline-r5`, and
  `next_stage_allowed: false`;
- accepted visual baseline: `G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r5`;
- accepted G4 reference families: auth exception r6 plus auth workspace, core,
  data, data quality, analytics, segments, forecast, promotions, dashboards,
  reports, and pipelines r5;
- pending frontier: OPS and later G4 families; all G5/G6 completion work is
  outside the current route;
- OPS and every downstream row were unclaimed at cutover, and no UI-program
  runner process was active.

The canonical accepted G3 board is
`.codex/delivery/ui-design-programs/custometry-v2/artifacts/g3-r5/review-board.html`.
The ledger rows bind every accepted family to its exact G4 board, transition,
and owner receipt; implementations should follow those row references rather
than scan or copy the evidence inventory. The r5 family boards live under
`.codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r5/`, with the
current auth exception under the corresponding `g4-r6` artifact directory.

The bounded reference map is:

- `G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r5` — board
  `.codex/delivery/ui-design-programs/custometry-v2/artifacts/g3-r5/review-board.html`;
  transition `.codex/delivery/ui-design-programs/custometry-v2/evidence/g3-r5/stage-transition.json`;
  SHA-256 `498a08210ea54da8ba9d0d48c9f6562586b068ecab2b87c741038e1d18db7f56`.
- `G4@family.auth.shell-auth.baseline-exception-auth-r6` — board
  `.codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r6/family-auth-shell-auth-baseline-exception-auth/review-board.html`;
  transition `.codex/delivery/ui-design-programs/custometry-v2/evidence/g4-r6/family-auth-shell-auth-baseline-exception-auth/stage-transition.json`;
  SHA-256 `61d1df571bce6c55ffdab70d3fe4e112a728ddb616385b9fd894af3b3a4d6aab`.
- `G4@family.auth.shell-workspace.baseline-r5` — board
  `.codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r5/family-auth-shell-workspace-baseline/review-board.html`;
  transition `.codex/delivery/ui-design-programs/custometry-v2/evidence/family.auth.shell-workspace.baseline-r5/stage-transition.json`;
  SHA-256 `66f386b6bd7fb1c96b4a8f524e7ec85e80f44e40ccd8dc29072c2ec2f8744efc`.
- `G4@family.core.shell-workspace.baseline-r5` — board
  `.codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r5/family-core-shell-workspace-baseline/review-board.html`;
  transition `.codex/delivery/ui-design-programs/custometry-v2/evidence/family.core.shell-workspace.baseline-r5/stage-transition.json`;
  SHA-256 `e9e6b5ff17b9c1964c7a6e40f8c407eecdbddb1e4fce988fa7264d95fd47e441`.
- `G4@family.data.shell-workspace.baseline-r5` — board
  `.codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r5/family-data-shell-workspace-baseline/review-board.html`;
  transition `.codex/delivery/ui-design-programs/custometry-v2/evidence/family.data.shell-workspace.baseline-r5/stage-transition.json`;
  SHA-256 `72bd46acad7e1372c0bee83230b257c549e9b57bc8114dc7f58d5b73bb80f547`.
- `G4@family.dq.shell-workspace.baseline-r5` — board
  `.codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r5/family-dq-shell-workspace-baseline/review-board.html`;
  transition `.codex/delivery/ui-design-programs/custometry-v2/evidence/family.dq.shell-workspace.baseline-r5/stage-transition.json`;
  SHA-256 `e5532040537ea54b928de34c612a7e946761af0aa38ad6abb0b79454127d7c93`.
- `G4@family.an.shell-workspace.baseline-r5` — board
  `.codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r5/family-an-shell-workspace-baseline/review-board.html`;
  transition `.codex/delivery/ui-design-programs/custometry-v2/evidence/family.an.shell-workspace.baseline-r5/stage-transition.json`;
  SHA-256 `9a62bc70bd5231ead5bfd742071b72623deee658a524833e82bc778142777dd4`.
- `G4@family.seg.shell-workspace.baseline-r5` — board
  `.codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r5/family-seg-shell-workspace-baseline/review-board.html`;
  transition `.codex/delivery/ui-design-programs/custometry-v2/evidence/family.seg.shell-workspace.baseline-r5/stage-transition.json`;
  SHA-256 `fb1d211f8ce4ca41052103798ba8c920650f2af2c97c11749e1150e9cff1524e`.
- `G4@family.fcst.shell-workspace.baseline-r5` — board
  `.codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r5/family-fcst-shell-workspace-baseline/review-board.html`;
  transition `.codex/delivery/ui-design-programs/custometry-v2/evidence/family.fcst.shell-workspace.baseline-r5/stage-transition.json`;
  SHA-256 `f1e676f9fc9fb61661557ccf4be7cf7515b5e5bd19f43cd1ef7c7168773bc8c4`.
- `G4@family.promo.shell-workspace.baseline-r5` — board
  `.codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r5/family-promo-shell-workspace-baseline/review-board.html`;
  transition `.codex/delivery/ui-design-programs/custometry-v2/evidence/family.promo.shell-workspace.baseline-r5/stage-transition.json`;
  SHA-256 `772087dbd48ea2e1f12c0869bfaea5d3bb0e8239edef34d0f108c71df13f360e`.
- `G4@family.dash.shell-workspace.baseline-r5` — board
  `.codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r5/family-dash-shell-workspace-baseline/review-board.html`;
  transition `.codex/delivery/ui-design-programs/custometry-v2/evidence/family.dash.shell-workspace.baseline-r5/stage-transition.json`;
  SHA-256 `dd00dd290403bc26a3a46ca630873d4f6b8d26cb9e9d5d878b95a40331bd4182`.
- `G4@family.rpt.shell-workspace.baseline-r5` — board
  `.codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r5/family-rpt-shell-workspace-baseline/review-board.html`;
  transition `.codex/delivery/ui-design-programs/custometry-v2/evidence/family.rpt.shell-workspace.baseline-r5/stage-transition.json`;
  SHA-256 `11e92cac124611e7ce98447b431b20f793a9168e30f6ebb2cd4b113003cf46af`.
- `G4@family.pipe.shell-workspace.baseline-r5` — board
  `.codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r5/family-pipe-shell-workspace-baseline/review-board.html`;
  transition `.codex/delivery/ui-design-programs/custometry-v2/evidence/family.pipe.shell-workspace.baseline-r5/stage-transition.json`;
  SHA-256 `6ecd8d988df04d97718abd0bf0f39f507287b672677d8839b13e56f60b01d419`.

The PIPE acceptance recorded at `2026-08-24T12:27:21Z` predates this cutover
and remains truthful historical evidence. This decision neither creates nor
changes any owner acceptance. The historical ledger bytes are intentionally
unchanged because its schema has no truthful suspension state and repository
authority now disables execution above it.

## Source precedence for implementation

An implementation ticket reads only the smallest applicable set in this order:

1. `custometry-technical-blueprint-ru.md` and its synchronized human mirror for
   normative product semantics and requirement IDs;
2. `custometry-ui-blueprint-ru.md` plus executable route/surface contracts for
   exact surface identity, roles, states, permissions, and responsive intent;
3. accepted architecture and frontend platform decisions;
4. the accepted G3 r5 board for shared visual language, density, shell, token,
   and interaction character;
5. an accepted G4 family board only for a screen that belongs to that family;
6. existing production code, focused tests, and observed browser evidence.

Accepted G3/G4 artifacts are reference inputs, not production code, route
status, frontend architecture, or a substitute for real-browser proof. For an
unaccepted family, inherit the accepted G3 baseline and normative product
semantics. Ask the owner only when implementation would introduce a materially
new visual direction, a baseline exception, or non-derivable product meaning.
Ordinary baseline inheritance needs no family approval.

## Ticket and proof contract

Every Web implementation ticket must name exact screen or surface IDs,
requirement IDs, user-visible outcomes, dependencies, and safely separable path
ownership. It must produce working production UI, focused automated tests, and
real-browser evidence for the changed boundary. Design-only boards, broad
pre-implementation state matrices, or copied program receipts do not satisfy a
ticket.

Browser proof covers critical changed states, relevant en/ru behavior,
keyboard/focus and accessibility smoke, console/network failures, and the
responsive Web endpoints. Use 768 CSS px and 1920 CSS px as required endpoint
anchors when applicable, adding intermediate widths only when layout risk or a
declared breakpoint warrants them. This is boundary-matched smoke, not a claim
of full WCAG conformance or exhaustive every-state-by-every-anchor coverage.
Mobile-specific design remains unauthorized.

Each browser-depth ticket owns a Playwright configuration below its declared
`tests/e2e/<ticket-slice>/` path. That configuration must use Playwright's
`webServer` lifecycle to start host Vite on an explicit loopback port, wait for
readiness, fail on startup error, and clean up. It must discover only the
ticket-owned specs and declare desktop Web projects for `768x1024` and
`1920x1080`; it must not depend on a pre-existing `CUSTOMETRY_BASE_URL`, reuse
the historical foundation-only config, or enable a sub-768 mobile project.

Evidence is written once at the implementation boundary. Source checks do not
prove browser, API, persistence, Compose, release, or production behavior.
Publication and deployment require separate explicit authority.

## Current bounded frontier

The current dependency and path-ownership topology is
`.codex/delivery/graphs/custometry-web-implementation-frontier-v1.json`.
`W31-WEB-PRODUCTION-SHELL-ROUTING` is the first immediately executable ticket.
Feature tickets become executable only when their declared dependency is
accepted and their own frontmatter is changed to `ready`. The graph deliberately
does not mirror all atlas screens; later work adds cohesive production slices
as ordinary tickets without reviving or duplicating the frozen design ledger.
