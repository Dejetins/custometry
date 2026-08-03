---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: W26-UI-AN-003-HTML-GLOBAL-ACTIONS-REFINEMENT
proof_boundary: browser-rendered-local-ui-an-003-global-action-refinement-matched-to-product-owner-browser-annotations
proof_skills: [better-layout, better-ui, browser-qa-evidence, playwright-cli]
verdict: passed
redaction: No credentials, cookies, browser storage, private product data, provider payloads, or external side effects are retained. Screenshots contain synthetic Northwind Retail UI data only.
executed_checks:
  - keep one context-panel toggle permanently in the global header in both open and closed states
  - remove the duplicated context-panel toggle from the inspector itself
  - make sidebar Search and Notifications visually transparent at rest and visibly surfaced only on hover
  - shift Notifications 4 px left without changing its 32 by 32 px geometry or the sidebar header padding
  - verify notification disclosure remains transparent when open and not hovered
  - measure global header axes sidebar action geometry chart and table action axes and inspector row geometry
  - verify keyboard focus console network and 1024 by 768 responsive behavior
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
  - The global context toggle remains at x 1327 y 24 width 32 height 32 in both states; More page actions remains at x 1367 y 24 with an 8 px gap.
  - The open state exposes Hide context panel with aria-expanded true and the closed state exposes Show context panel with aria-expanded false.
  - The inspector contains zero context-panel toggle buttons after opening or restoration.
  - Search is at x 161.46875 and Notifications at x 197.46875; both share y 31 width 32 height 32 and now have a 4 px gap.
  - Search and Notifications both use transparent default background and border; hover uses rgb 34 56 74 and rgb 85 116 140 without geometry changes.
  - Notifications remains transparent after its disclosure opens and the pointer leaves; aria-expanded changes correctly between true and false.
  - Expand chart and Download table retain center x 1128 with zero axis delta.
  - Inspector share and view rows retain x 1188 width 216 height 32 with 4 px intra-group gaps.
  - Tab order reaches Search then Notifications and both expose the existing 2 px visible focus outline.
  - The 1024 by 768 smoke has no document overflow and the clean Playwright session reported zero console errors zero warnings and static requests only.
---

# W26 UI-AN-003 HTML global actions refinement evidence

## Outcome and scope

Both product-owner browser annotations were applied to the isolated HTML
prototype at:

`http://127.0.0.1:5173/w/northwind-retail/analytics/sales?view=html-prototype`

Only the prototype component, its local CSS, focused test, ticket, and evidence
were changed. Figma, the application route gate, normative product sources,
shared UI contracts, API, persistence, and production surfaces were not
changed.

## Annotation acceptance matrix

| Annotation | Result | Browser observation |
| --- | --- | --- |
| Fixed global context toggle | Pass | The same `32×32 px` global-header control remains at `x=1327, y=24` in both open and closed states. Its label and `aria-expanded` state update without any position change. |
| No inspector duplicate | Pass | The inspector contains zero buttons whose accessible name matches `context panel`; restoring the panel does not recreate a duplicate. |
| Borderless sidebar actions | Pass | Search and Notifications have transparent background and border at rest and when the notification disclosure is open but not hovered. |
| Hover-only surface | Pass | Both sidebar actions change to `rgb(34, 56, 74)` background and `rgb(85, 116, 140)` border only while hovered, with unchanged geometry. |
| Notification optical adjustment | Pass | Notifications moved from the W25 `x=201.46875` position to `x=197.46875`, a measured `4 px` left shift; its size remains `32×32 px`. |
| Stable alignment and spacing | Pass | Context toggle and More page actions share `y=24`; the chart/table trailing actions still share center `x=1128`; inspector rows remain `216×32 px` with `4 px` gaps. |

## Layout and UI verification

- The global context toggle has one stable ownership location and remains
  discoverable when the inspector is hidden.
- Search and Notifications share `y=31`, size `32×32 px`, and a compact `4 px`
  gap after the requested optical shift.
- The header toggle and More page actions share one horizontal axis with an
  `8 px` gap and do not move when the inspector changes state.
- Hover treatment changes paint only; button boxes and surrounding spacing do
  not change.
- Keyboard focus reaches Search and then Notifications with the existing
  `2 px` visible focus outline, preserving keyboard access despite the
  borderless resting treatment.
- Better Layout review: no actionable ownership, alignment, grouping, spacing,
  or responsive finding remains — **Approve**.
- Better UI review: no actionable default, hover, focus, optical spacing, or
  icon-control finding remains — **Approve**.

## Browser evidence

| State | Artifact | SHA-256 |
| --- | --- | --- |
| Final 1440×900 | `assets/W26-UI-AN-003-HTML-GLOBAL-ACTIONS-REFINEMENT/browser-default-1440x900.png` | `2f81ceb3973493e05f330f44dd91bc300c1f74a9d97da7785c46632103b13fde` |
| Context hidden | `assets/W26-UI-AN-003-HTML-GLOBAL-ACTIONS-REFINEMENT/browser-context-hidden.png` | `72f32c3d3086f5f779bb3813f9e086c8b6cc3c27f3bf30afb12390bed3d900e9` |
| Search hover | `assets/W26-UI-AN-003-HTML-GLOBAL-ACTIONS-REFINEMENT/browser-search-hover.png` | `054e202e92c9b4abcd1d782e93d841a8d7f4ad3b1858b70ad7aeeca2eac81dbe` |
| Notification hover | `assets/W26-UI-AN-003-HTML-GLOBAL-ACTIONS-REFINEMENT/browser-notification-hover.png` | `37a5d7963e070a7ead9a82ccbe8c3896f1f51430348022ddd7880805c98eb951` |
| Keyboard focus | `assets/W26-UI-AN-003-HTML-GLOBAL-ACTIONS-REFINEMENT/browser-keyboard-focus.png` | `f964607205948eb02ad92e865351c0e1676914c21ffad981129dbd82d5d264f0` |
| 1024×768 smoke | `assets/W26-UI-AN-003-HTML-GLOBAL-ACTIONS-REFINEMENT/browser-1024-smoke.png` | `1e442099fd9e783a5f96d5695ecc386a96bbcece831c0884171ff5cdd3ecd99f` |

Fresh-session diagnostics: zero console errors, zero warnings, React
development information only, static requests only, no prototype API request,
and no horizontal or vertical document overflow at `1024×768`.

## Commands and observations

| Command | Result | Observation |
| --- | --- | --- |
| `pnpm --filter @custometry/web lint` | pass | No findings. |
| `pnpm --filter @custometry/web typecheck` | pass | No type errors. |
| `pnpm --filter @custometry/web test` | pass | 3 files and 15 tests passed. |
| `pnpm --filter @custometry/web build` | pass | Vite build completed; 1764 modules transformed. |
| `uv run python -m tools.custometry_quality.validate_delivery_tickets` | pass | Delivery tickets validated with W26 active and again after acceptance. |
| `uv run python -m tools.custometry_quality.validate_delivery_contract` | pass | Repository delivery adapter validated. |
| `uv run python -m tools.custometry_quality.validate_repository_layout` | pass | Repository layout validated. |
| `uv run python -m tools.check --scope local` | pass | Grouped local gate passed. |
| `git diff --check` | pass | No whitespace errors. |

## Contract impact and residual risk

- Contract impact: `none` for runtime routes, API, permissions, persistence,
  data semantics, localization, and Figma identity.
- The change intentionally refines only the post-Figma HTML review state under
  the product owner's explicit browser annotations.
- Search, notifications, copy link, email, export, save, filter, fullscreen,
  and trust actions remain review-only and cause no external or irreversible
  side effect.
- Proof covers the local browser prototype, not production readiness, backend
  integration, deployment, or release.

## Verdict

**Passed** at the declared HTML-only browser boundary. No actionable layout or
UI-polish finding remains in the annotated states.
