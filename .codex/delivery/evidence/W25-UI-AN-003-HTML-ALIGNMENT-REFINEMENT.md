---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: W25-UI-AN-003-HTML-ALIGNMENT-REFINEMENT
proof_boundary: browser-rendered-local-ui-an-003-html-refinement-matched-to-product-owner-browser-annotations
proof_skills: [better-layout, better-ui, browser-qa-evidence, playwright-cli]
verdict: passed
redaction: No credentials, cookies, browser storage, private product data, provider payloads, or external side effects are retained. Screenshots contain synthetic Northwind Retail UI data only.
executed_checks:
  - move notifications beside search in the compact sidebar header and exercise its disclosure
  - move the share group above the compact view controls and remove the dataset control
  - reduce all share and view action rows to one 216 by 32 px geometry with matching 10 px inline padding and 4 px intra-group gaps
  - replace the standalone result trust inspector row with an inline chart summary containing trust status and the last update date and time
  - align More page actions exactly above Hide context panel and preserve the context restore action after hiding
  - confirm fullscreen and table download remain exactly collinear
  - verify shared section-label axes keyboard order hover state console network and 1024 by 768 responsive behavior
  - pnpm --filter @custometry/web lint
  - pnpm --filter @custometry/web typecheck
  - pnpm --filter @custometry/web test
  - pnpm --filter @custometry/web build
  - uv run python -m tools.custometry_quality.validate_delivery_tickets
  - uv run python -m tools.custometry_quality.validate_delivery_contract
  - uv run python -m tools.custometry_quality.validate_repository_layout
  - uv run python -m tools.check --scope local
  - git diff --check
observations:
  - More page actions and Hide context panel share center x 1383 with zero browser-measured axis delta at 1440 by 900.
  - Expand chart and Download table share center x 1128 with zero browser-measured axis delta.
  - Copy link Send by email and all five remaining view controls share x 1188 width 216 height 32 and 10 px inline padding.
  - Intra-group row gaps are consistently 4 px and ON THIS PAGE SHARE and VIEW labels share x 1196.
  - Search and Notifications share y 31 width 32 height 32 with an 8 px gap; Tab order reaches Search then Notifications.
  - Dataset content and the standalone sales-trust button are absent from the browser DOM.
  - The chart summary exposes Trusted and Updated 31 Jul 2026 12:42 with a descriptive accessible name.
  - The clean Playwright session reported zero console errors zero warnings and static requests only; no prototype API request occurred.
---

# W25 UI-AN-003 HTML alignment refinement evidence

## Outcome and scope

All six product-owner browser annotations were applied to the isolated HTML
prototype at:

`http://127.0.0.1:5173/w/northwind-retail/analytics/sales?view=html-prototype`

Only the prototype component, its local CSS, focused test, ticket, and evidence
were changed. Figma, the application route gate, product contracts, shared UI
foundation, API, persistence, and production surfaces were not changed.

## Annotation acceptance matrix

| Annotation | Result | Browser observation |
| --- | --- | --- |
| Compact inspector actions | Pass | SHARE and VIEW action rows are all `216×32 px`, at `x=1188`, with `10 px` inline padding and `4 px` intra-group gaps. |
| SHARE above VIEW | Pass | DOM and visual order is ON THIS PAGE → SHARE → VIEW. |
| Trust and update metadata in chart | Pass | The standalone inspector block is removed; `Trusted · Updated 31 Jul 2026, 12:42` is an inline summary at the chart's trailing bottom corner. |
| Notification beside Search | Pass | Both controls are `32×32 px`, share `y=31`, and have an `8 px` gap in the sidebar header. |
| Global and context action axis | Pass | More page actions and Hide context panel both have center `x=1383`; measured delta is `0 px`. |
| Persistent context restore | Pass | Hiding the inspector exposes Show context panel beside More page actions; restoring recreates the complete inspector. |
| Remove Dataset | Pass | `Retail sales v24` and the Dataset button are absent from visible text and the browser DOM. |

The existing chart/table action axis remains intact: Expand chart and Download
table both have center `x=1128`, measured delta `0 px`.

## Layout and UI verification

- Section labels ON THIS PAGE, SHARE, and VIEW all begin at `x=1196`.
- Copy link, Send by email, Period, Comparison, Stores, Channels, and Audience
  share one width, height, horizontal origin, and inline padding.
- Hover styling preserves geometry and changes only border/background emphasis.
- The notification popover stays within the sidebar surface.
- Keyboard focus reaches Search and then Notifications with visible focus
  styling and stable layout.
- Better Layout review: no actionable alignment, grouping, spacing, or
  responsive findings remain — **Approve**.
- Better UI review: no actionable radius, icon-weight, hover, or optical-axis
  findings remain — **Approve**.

## Browser evidence

| State | Artifact | SHA-256 |
| --- | --- | --- |
| Final 1440×900 | `assets/W25-UI-AN-003-HTML-ALIGNMENT-REFINEMENT/browser-1440x900.png` | `2eb38b83251ed148ac7409801ea80b1eb2ce4d3f796616ca3173c7f5214971aa` |
| Notification disclosure | `assets/W25-UI-AN-003-HTML-ALIGNMENT-REFINEMENT/browser-notification-state.png` | `74affd7914a16560626320b253e6b4288c43be86fe514a8590fe4d2459279c45` |
| Hidden context state | `assets/W25-UI-AN-003-HTML-ALIGNMENT-REFINEMENT/browser-context-hidden.png` | `f6d372bc04428764fc2b22105e78cffdd5311e4f6a035c5836a3ba186b664166` |
| Hover state | `assets/W25-UI-AN-003-HTML-ALIGNMENT-REFINEMENT/browser-hover-state.png` | `79fd3dec18570bf5051f7de3b6c720c46fb928d5536502d83dc79f97414edddb` |
| 1024×768 smoke | `assets/W25-UI-AN-003-HTML-ALIGNMENT-REFINEMENT/browser-1024-smoke.png` | `e10ce9dfe035b6466f1930395e816e88c5aee2aa53689d9b179a733fe594b40a` |

Fresh-session diagnostics: zero console errors, zero warnings, React
development information only, static requests only, and no
`/api/health/ready` request.

## Commands and observations

| Command | Result | Observation |
| --- | --- | --- |
| `pnpm --filter @custometry/web lint` | pass | No findings. |
| `pnpm --filter @custometry/web typecheck` | pass | No type errors. |
| `pnpm --filter @custometry/web test` | pass | 3 files and 15 tests passed. |
| `pnpm --filter @custometry/web build` | pass | Vite build completed; 1764 modules transformed. |
| `uv run python -m tools.custometry_quality.validate_delivery_tickets` | pass | 29 tickets validated while W25 was active. |
| `uv run python -m tools.custometry_quality.validate_delivery_contract` | pass | Repository delivery adapter validated. |
| `uv run python -m tools.custometry_quality.validate_repository_layout` | pass | Repository layout validated. |
| `uv run python -m tools.check --scope local` | pass | Grouped local gate passed. |
| `git diff --check` | pass | No whitespace errors. |

## Contract impact and residual risk

- Contract impact: `none` for runtime routes, API, permissions, persistence,
  data semantics, localization, and Figma identity.
- The new layout intentionally refines only the post-Figma HTML review state
  under the product owner's explicit browser annotations.
- Copy link, email, export, save, filter, fullscreen, and trust actions remain
  review-only and cause no external or irreversible side effect.
- Proof covers the local browser prototype, not production readiness,
  backend integration, deployment, or release.

## Verdict

**Passed** at the declared HTML-only browser boundary. No actionable layout or
UI-polish finding remains in the annotated states.
