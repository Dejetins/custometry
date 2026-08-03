---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: W27-UI-AN-003-HTML-CONTRACT-COMPLETION
proof_boundary: browser-rendered-local-ui-an-003-html-contract-completion-plus-repository-owned-normative-contract-validation
proof_skills: [better-layout, better-ui, better-accessibility, browser-qa-evidence, playwright-cli]
verdict: passed
product_owner_decision: accepted
redaction: No credentials, cookies, browser storage, private product data, provider payloads, or external side effects are retained. Screenshots contain synthetic Northwind Retail UI data only.
executed_checks:
  - align machine and human blueprints on UI-SHELL-004...006 and UI-DENSITY-004
  - add UI-AN-015 Products as the 117th target route and one honest design backlog without relabeling the 116 accepted historical frames
  - record the reusable HTML candidate then product-owner acceptance then bounded Figma synchronization sequence
  - verify compact Result Trust in Chart and Data and full on-demand trust disclosure
  - verify route-backed revenue chart data and product breakdown Focus Explore states and browser Back return
  - verify channel store product breakdown selection and contribution values
  - verify expanded resized collapsed hidden and restored sidebar states Help user menu aria-current and distinct navigation icons
  - verify 1440 by 900 action axes and 1024 by 768 non-scaled compact reflow
  - inspect browser console resource origins failed image assets and document overflow
  - pnpm --filter @custometry/web lint
  - pnpm --filter @custometry/web typecheck
  - pnpm --filter @custometry/web test
  - pnpm --filter @custometry/web build
  - uv run python -m tools.custometry_quality.validate_blueprints
  - uv run python -m tools.custometry_quality.generate_requirement_index --check
  - uv run python -m tools.custometry_quality.validate_route_registry
  - uv run python -m tools.custometry_quality.check_i18n_parity
  - uv run python -m tools.custometry_quality.validate_delivery_tickets
  - uv run python -m tools.custometry_quality.validate_delivery_contract
  - uv run python -m tools.check --scope local
  - git diff --check
observations:
  - At 1440 by 900 the sidebar is x 12 width 224 and the application is x 248 width 1180, preserving the accepted desktop composition.
  - Expand chart and Expand table share x 1112 y-independent width 32 height 32 and therefore one exact vertical axis.
  - At 1024 by 768 the sidebar is 64 px, the application is 924 px, font size remains 14 px, CSS zoom is 1, and document scroll width equals client width at 1024 px.
  - Keyboard ArrowRight on the sidebar separator changes the persisted width from 224 to 232; collapsed and hidden states expose the expected accessible restore controls.
  - Sales exposes aria-current page; Sales Products and Forecasts use chart-line package and trending-up Lucide identities.
  - Result Trust includes Retail sales v24 freshness quality grain context currency timezone lineage and limitations; the inspector contains no standalone Dataset or Result Trust row.
  - Focus chart uses focus=revenue-trend and Focus table uses focus=breakdown; browser Back returns to the embedded route and Chart to Data retains the trust trigger.
  - The product breakdown exposes 39.7 percent contribution and all three channel store product breakdown options remain available.
  - Fresh-session diagnostics reported zero console errors zero warnings only the local 127.0.0.1 origin and no failed image assets.
---

# W27 UI-AN-003 HTML contract completion evidence

## Outcome and scope

The accepted visual direction is now a complete responsive HTML review
candidate at:

`http://127.0.0.1:5173/w/northwind-retail/analytics/sales?view=html-prototype`

The repository-owned shell, route, trust, density, and prototyping contracts
were aligned with the product-owner decisions. No Figma or Figma-specific
manifest/component path was mutated. W24-W26 and the 116-frame historical
design inventory remain truthful; `UI-AN-015` is the single new target backlog.

## Product-owner acceptance record

- ticket status: `accepted` in
  `.codex/delivery/tickets/W27-UI-AN-003-HTML-CONTRACT-COMPLETION.md`;
- evidence frontmatter: `product_owner_decision: accepted`;
- terminal outcome: `pilot_passed`;
- post-pilot decision: `scale`;
- accepted visual source:
  `http://127.0.0.1:5173/w/northwind-retail/analytics/sales?view=html-prototype`.

These values record the product owner's explicit 2026-08-01 acceptance. They do
not alter the previously observed browser proof or its exclusions.

## Product decision matrix

| Decision | Result | Proof |
| --- | --- | --- |
| Compact Result Trust | Pass | One result trigger combines `Retail sales v24`, Trusted, freshness timestamp, and opens a full details drawer in both Chart and Data. |
| Focus / Explore | Pass | Chart and breakdown use addressable `focus` query state, full application viewport, Escape/close/Back return, inherited period/comparison/context, Trust, and review-only export. |
| Sales coverage | Pass | Embedded and Focus table switch among channel, store, and product with Contribution and `%/Abs` comparison. |
| Dataset/trust exception | Pass | Context inspector contains neither standalone Dataset nor standalone Result Trust row. |
| Sidebar utilities | Pass | Search/Notifications remain immediately after workspace identity; Help/User menu are in the stable footer. |
| Sidebar presentation | Pass | Expanded, pointer/keyboard-resized, collapsed, hidden, and restored states are implemented and persisted. |
| Navigation semantics | Pass | Sales has `aria-current="page"`; Sales, Products, and Forecasts have distinct Lucide icons; Products remains a first-class route identity. |
| Responsive behavior | Pass | No CSS zoom/transform scaling; the compact layout reflows to a 64 px rail and own table overflow at 1024 px with no document overflow. |
| HTML-first process | Pass | Normative process now requires HTML browser review and explicit product-owner acceptance before a separate bounded Figma synchronization stage. |

## Browser geometry and interaction evidence

- Desktop root is exactly `1440×900`; sidebar/app boxes are `224×876` and
  `1180×876` with the accepted `12 px` outer/gap rhythm.
- Chart and table trailing Focus actions share `x=1112`, width `32`, and height
  `32`; context rows and share rows remain `32 px` high with `4 px` group gaps.
- At `1024×768`, computed root font remains `14px` and computed `zoom` is `1`.
  The collapsed rail is `64 px`, application width is `924 px`, and
  `documentElement.scrollWidth === clientWidth === 1024`.
- Keyboard resize exposes `role="separator"`, min `208`, max `320`, current
  value, `8 px` arrow steps, and Home/double-click reset. The observed
  ArrowRight step persisted `224 → 232`.
- Help and user-menu disclosures, Notifications, Result Trust, Chart/Data,
  `%/Abs`, breakdown selection, sidebar state changes, and both Focus surfaces
  were exercised in the fresh browser session.
- Fresh session: `0` console errors, `0` warnings, only
  `http://127.0.0.1:5173` resources, and no failed image asset.

## Browser artifacts

| State | Artifact | SHA-256 |
| --- | --- | --- |
| Desktop default `1440×900` | `assets/W27-UI-AN-003-HTML-CONTRACT-COMPLETION/desktop-default-1440x900.png` | `be28cd5236ad1c92cf6c63c9fd8e74162e01a628b9b780ca6edac502d8284e0a` |
| Compact default `1024×768` | `assets/W27-UI-AN-003-HTML-CONTRACT-COMPLETION/compact-default-1024x768.png` | `8ec7485b9e9720a4856b9dc4ba47ceeba787b2911bee4a44c6e9c960b65aeae9` |
| Result Trust drawer | `assets/W27-UI-AN-003-HTML-CONTRACT-COMPLETION/desktop-result-trust-1440x900.png` | `611adae394032ab10ab42f001ebf0de683748509db850994815a09df7483b7c2` |
| Focus chart | `assets/W27-UI-AN-003-HTML-CONTRACT-COMPLETION/focus-chart-1440x900.png` | `3a1c4ab27405d69ca016e4c9d0faf6b5cc78b84408a73f48d00a3daefd53cf17` |
| Focus product breakdown | `assets/W27-UI-AN-003-HTML-CONTRACT-COMPLETION/focus-product-breakdown-1440x900.png` | `a0b236b1c5f23e2efe24a2f1b2d63ff5978e0fcbda14f2904f100cf0eebe991a` |
| Sidebar collapsed | `assets/W27-UI-AN-003-HTML-CONTRACT-COMPLETION/desktop-sidebar-collapsed-1440x900.png` | `e3f43a6938b9c80fc938f23669880970e1c4bae5b861b2ce3225e4f508fc3082` |
| Sidebar hidden | `assets/W27-UI-AN-003-HTML-CONTRACT-COMPLETION/desktop-sidebar-hidden-1440x900.png` | `8befae928f51648a3521582dbffee62514b2f55aafe4ade62ef3b376b1a3eec7` |

## Commands and observations

| Command | Result | Observation |
| --- | --- | --- |
| `pnpm --filter @custometry/web lint` | pass | TypeScript lint boundary completed without findings. |
| `pnpm --filter @custometry/web typecheck` | pass | No type errors. |
| `pnpm --filter @custometry/web test` | pass | `3` files, `22` tests passed; prototype suite contains `12` focused tests. |
| `pnpm --filter @custometry/web build` | pass | Vite build completed; `1764` modules transformed. |
| `uv run python -m tools.custometry_quality.validate_blueprints` | pass | Machine/human parity; `958` requirement IDs. |
| `uv run python -m tools.custometry_quality.generate_requirement_index --check` | pass | Generated index is current with `958` requirements. |
| `uv run python -m tools.custometry_quality.validate_route_registry` | pass | `117` routes/contracts, `116` baseline verified, `1` design backlog. |
| `uv run python -m tools.custometry_quality.check_i18n_parity` | pass | en/ru parity at `169` keys each. |
| `uv run python -m tools.custometry_quality.validate_delivery_tickets` | pass | `31` tickets validated. |
| `uv run python -m tools.custometry_quality.validate_delivery_contract` | pass | Repository adapter validated. |
| `uv run python -m tools.check --scope local` | pass | Grouped local gate passed. |
| `git diff --check` | pass | No whitespace errors. |

## Contract impact and residual risk

- Route/UI registry: compatible additive change before stable runtime — one
  planned `UI-AN-015` route and localization title; no API or permission
  catalog expansion.
- Shell/default presentation: breaking design change before stable runtime —
  sidebar utility ownership and Dataset/Trust composition now follow the
  accepted product-owner visual decision.
- API, persistence, data semantics, request/cache identity, deployment, and
  production authorization: no change.
- ECharts bar rendering, command palette, More page actions, typed filter
  expressions/chips, and real share/email/download/export side effects remain
  explicitly deferred to later implementation tickets.
- This evidence proves the isolated local HTML review boundary. It does not
  prove production runtime, API integration, full accessibility conformance,
  performance budgets, release, or deployment.

## Verdict

**Passed** at the declared repository-contract and local-browser boundary.
The product owner explicitly accepted this exact HTML candidate on 2026-08-01.
W27 is therefore `accepted`, its terminal outcome is `pilot_passed`, and the
post-pilot decision is `scale`. This accepted HTML candidate is the sole visual
source authorized for the next bounded Figma synchronization unit; production
runtime readiness remains outside this evidence boundary.
