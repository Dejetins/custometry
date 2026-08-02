---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: W24-UI-AN-003-HTML-PROTOTYPE
proof_boundary: browser-rendered-local-ui-an-003-graphite-review-prototype-matched-to-accepted-figma-node-40-536
proof_skills: [figma:figma-design-to-code, product-design:image-to-code, product-design:design-qa, browser-qa-evidence, playwright-cli]
verdict: passed
redaction: No credentials, cookies, browser storage, private product data, provider payloads, or short-lived Figma asset URLs are retained. Screenshots contain synthetic Northwind Retail UI data only.
executed_checks:
  - fetch Figma design context for accepted node 40:536 in MXfxuhSFpIczbUtFmOSyPp before implementation
  - render the isolated HTML prototype at 1440 by 900 and compare it with the accepted 1440 by 900 Figma screenshot
  - exercise chart and data switching filter disclosure context inspector hide and restore notifications copy-link feedback and compact share actions without external side effects
  - inspect the browser console and requests and confirm no prototype API request
  - run a 1024 by 768 responsive browser smoke
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
  - The prototype is query-gated at /w/northwind-retail/analytics/sales?view=html-prototype and leaves the existing planned surface and architecture spike available.
  - The 1440 by 900 browser render preserves the accepted sidebar application canvas KPI chart table inspector geometry controls axes colors radii density and content hierarchy.
  - Design QA found no P0 P1 or P2 mismatch; browser and Figma text rasterization can differ at the anti-aliasing level and byte-identical pixels are not claimed.
  - Browser interaction snapshots cover default data filter hidden-context and notification states.
  - The clean browser session reported zero console errors zero warnings and only static asset requests; /api/health/ready was not requested.
  - The 1024 by 768 smoke preserves the complete desktop composition by proportional review scaling with a continuous graphite background.
  - Real persistence export email link sharing authorization and analytics APIs remain deliberately disabled.
---

# W24 UI-AN-003 HTML prototype evidence

## Outcome and scope

The accepted Graphite `UI-AN-003` Sales overview is available as an isolated
HTML/React review prototype at:

`http://127.0.0.1:5173/w/northwind-retail/analytics/sales?view=html-prototype`

The implementation includes the accepted sidebar, page header, compact KPI
strip, chart and table modules, aligned action controls, hideable grouped
context inspector, exact exported Figma glyph assets, and review-only local
interactions. It does not implement W22 production shell or W23 analytics
integration.

## Source and visual comparison

| Boundary | Source | Result |
| --- | --- | --- |
| Figma identity | `MXfxuhSFpIczbUtFmOSyPp`, node `40:536` | Confirmed before source mutation through design context. |
| Figma reference | `assets/W21-CONTRACT-COMPILED-UI-PILOT/figma-candidate-b.png` | `1440x900`, SHA-256 `c721dd7c24bfcde40c9bff71a8be42d51acb535eeb2eff9860a09d5f16b7e0a1`. |
| Browser reference | `assets/W24-UI-AN-003-HTML-PROTOTYPE/browser-1440x900.png` | `1440x900`, SHA-256 `dd9c7a76b151463350dcff59de0aee117cedfd28e3d68d674725bc17f2c9ee93`. |
| Geometry and hierarchy | Side-by-side same-viewport inspection | Pass: sidebar, application canvas, 900/240 content split, KPI strip, chart, table, inspector, action axes, density, radii, colors, labels, and data hierarchy match the accepted source. |
| Severity gate | Product Design QA rubric | P0: 0, P1: 0, P2: 0. Browser/Figma text anti-aliasing is a non-blocking rasterization difference; byte-identical pixels are not claimed. |

## Browser interaction evidence

| State or action | Result | Durable evidence |
| --- | --- | --- |
| Default chart state | Pass | `browser-1440x900.png`. |
| Chart to data and back | Pass | `browser-data-state.png`; semantic Chart/Data controls remain stable. |
| Filter disclosure | Pass | `browser-filter-state.png`; compact Channel and Store choices appear without layout shift. |
| Context inspector hide and restore | Pass | `browser-context-hidden.png`; the header receives one Show context panel action and restores the grouped inspector. |
| Notifications | Pass | `browser-notification-state.png`; the unread bell opens the local notification disclosure. |
| Compact share actions | Pass | Copy link produces an accessible local status; Send by email remains explicitly disabled. |
| Responsive smoke | Pass | `browser-1024-smoke.png`; the complete desktop review composition scales proportionally without clipping or a foreign background. |
| Console and network | Pass | Fresh Playwright session: 0 errors, 0 warnings, React development info only, static requests only, and no `/api/health/ready` request. |

## Commands and observations

| Command | Result | Observation |
| --- | --- | --- |
| `pnpm --filter @custometry/web lint` | pass | TypeScript lint boundary completed without findings. |
| `pnpm --filter @custometry/web typecheck` | pass | No type errors. |
| `pnpm --filter @custometry/web test` | pass | 3 files, 14 tests passed. |
| `pnpm --filter @custometry/web build` | pass | Vite production build completed; 1764 modules transformed. |
| `uv run python -m tools.custometry_quality.validate_delivery_tickets` | pass | 28 tickets validated while W24 was active. |
| `uv run python -m tools.custometry_quality.validate_delivery_contract` | pass | Repository delivery adapter validated. |
| `uv run python -m tools.custometry_quality.validate_repository_layout` | pass | 54 required directories, 18 required files, and 354 tracked files validated. |
| `uv run python -m tools.check --scope local` | pass | Grouped local gate passed. |
| `git diff --check` | pass | No whitespace errors. |

## Contract impact and residual risk

- Runtime route registry, API contracts, permissions, persistence, localization,
  analytics calculations, and production data are unchanged.
- The prototype is opt-in through `?view=html-prototype`; the existing fallback
  and `?view=linear-spike` remain available.
- Save, download, copy, email, filter, trust, and fullscreen behavior is
  intentionally review-only and produces no external or irreversible effect.
- The proof boundary is local browser rendering and interaction, not production
  readiness, backend integration, authorization, deployment, or release.

## Verdict

**Passed** at the declared local browser prototype boundary. The screen is
ready for precise product-owner review and iterative HTML-first UI comments.
