---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.10.0-draft
ticket_id: W31-WEB-PRODUCTION-SHELL-ROUTING
proof_boundary: production-web-shell-route-resolution-and-system-presentation-in-a-real-browser-with-contract-fixtures
proof_skills: [contract-impact-analysis, better-accessibility, browser-qa-evidence, playwright-cli]
verdict: passed
redaction: No credentials, cookies, browser storage, provider payloads, or production data were captured; all browser data is explicit W31 contract-fixture content.
executed_checks:
  - source scripts/activate-toolchain.sh && pnpm --filter @custometry/ui-foundation lint && pnpm --filter @custometry/ui-foundation test
  - source scripts/activate-toolchain.sh && pnpm --filter @custometry/web lint && pnpm --filter @custometry/web test && pnpm --filter @custometry/web build
  - source scripts/activate-toolchain.sh && pnpm --filter @custometry/localization test
  - uv run python -m tools.custometry_quality.validate_route_registry
  - uv run python -m tools.custometry_quality.check_i18n_parity
  - source scripts/activate-toolchain.sh && pnpm --filter @custometry/web exec playwright test --config ../../tests/e2e/web-shell/playwright.config.ts
  - uv run python -m tools.custometry_quality.validate_delivery_tickets
  - source scripts/activate-toolchain.sh && uv run python -m tools.check --scope local
  - git diff --check
observations:
  - W31 route, shell, localization, unit, build, repository, and browser checks passed.
  - Playwright ran only web-shell.spec.ts through ticket-owned loopback Vite webServer projects web-768 and web-1920; 8/8 tests passed.
  - Console errors, page errors, HTTP error responses, unexpected request failures, whole-page horizontal overflow, and observed clipping/overlap were absent.
  - React cleanup and navigation intentionally aborted only the instrumented health fixture through AbortController; diagnostics classify those cancellations separately from failures.
  - The initial foreign tree contained 5158 entries; only the untracked W31 ticket intersected allowed scope, and the remaining 5157 outside-scope entries stayed separated.
---

# W31 Web Production Shell Routing Evidence

> Compact evidence for one terminal ticket. It is not another execution-state
> source or a replacement for the product specification.

## Outcome and scope

- outcome: `UI-CAP-001` and `UI-SYS-001...005` now have a production React shell, executable-contract route resolution, a typed lazy file-discovery seam for later feature routes, and honest DEV-only presentation fixtures;
- requirement IDs: [WEB-ARCH-003, WEB-ARCH-004, WEB-ARCH-005, WEB-ARCH-006, UI-SHELL-001, UI-SHELL-002, UI-SHELL-003, ROUTE-001, ROUTE-002, ROUTE-003, ROUTE-004, ROUTE-005, ROUTE-006, ROUTE-007, ROUTE-008, ROUTE-009, ROUTE-010, ROUTE-011, ROUTE-012, RBAC-002, SYS-UI-001, SYS-UI-002, SYS-UI-003, SYS-UI-004, SYS-UI-005, A11Y-001, A11Y-003, A11Y-008, I18N-001, I18N-002, I18N-005];
- included: auth, global, workspace, installation, setup, focus, and system presentation profiles; current navigation; localized titles/copy; Back/refresh/history; route-change and POP focus; skip link; visible focus; 200% reflow-equivalent smoke; reduced motion; Foundation, Help, planned-surface, architecture-spike, and HTML-prototype compatibility seams;
- exclusions: backend policy/authorization, authentication truth, API semantics beyond fixtures, persistence, Compose, full WCAG conformance, screen-reader certification, measured performance, production runtime, release, publication, deployment, mobile-specific navigation, and W32-W35.

## Commands and observations

| Command or action | Result | Redacted observation / durable reference |
|---|---|---|
| `source scripts/activate-toolchain.sh && pnpm --filter @custometry/ui-foundation lint && pnpm --filter @custometry/ui-foundation test` | pass | TypeScript pass; Vitest `2/2`. |
| `source scripts/activate-toolchain.sh && pnpm --filter @custometry/web lint && pnpm --filter @custometry/web test && pnpm --filter @custometry/web build` | pass | TypeScript pass; Vitest `41/41`; Vite production build pass. Rollup reported a non-fatal `590.22 kB` compatibility-bundle warning; no performance claim is made. |
| `source scripts/activate-toolchain.sh && pnpm --filter @custometry/localization test` | pass | RU/EN catalog Vitest `2/2`. |
| `uv run python -m tools.custometry_quality.validate_route_registry` | pass | `117` identity/executable routes, `5` system surfaces, and `22` cross-surface capabilities validated without manifest writes. |
| `uv run python -m tools.custometry_quality.check_i18n_parity` | pass | `200` English and `200` Russian keys. |
| `source scripts/activate-toolchain.sh && pnpm --filter @custometry/web exec playwright test --config ../../tests/e2e/web-shell/playwright.config.ts` | pass | `8/8`; Vite started/stopped on `http://127.0.0.1:41731`; only `web-768` (`768x1024`) and `web-1920` (`1920x1080`) ran. |
| Visual review of Playwright captures | pass | No observed clipping, overlap, or whole-page horizontal overflow. Captures remain below `tests/e2e/web-shell/test-results/` for both projects. |
| `uv run python -m tools.custometry_quality.validate_delivery_tickets` | pass | `35` tickets validated before terminal frontmatter update. |
| `uv run python -m tools.check --scope local` before activation | fail (environmental) | System Node was `24.19.0`; repository requires `24.18.0`. No product failure was inferred. |
| `source scripts/activate-toolchain.sh && uv run python -m tools.check --scope local` | pass | Grouped local profile passed with repository-pinned Node `24.18.0`. |
| `git diff --check` | pass | No whitespace errors. |

### Browser evidence paths

- `tests/e2e/web-shell/test-results/web-shell-route-identity-h-15afd-ion-and-focus-are-preserved-web-768/shell-ru-history.png`;
- `tests/e2e/web-shell/test-results/web-shell-route-identity-h-15afd-ion-and-focus-are-preserved-web-1920/shell-ru-history.png`;
- `tests/e2e/web-shell/test-results/web-shell-keyboard-only-tr-2e353-eserves-logical-route-focus-web-768/keyboard-route-focus.png`;
- `tests/e2e/web-shell/test-results/web-shell-keyboard-only-tr-2e353-eserves-logical-route-focus-web-1920/keyboard-route-focus.png`;
- `tests/e2e/web-shell/test-results/web-shell-system-surfaces--2881d-d-explicitly-fixture-backed-web-768/system-404-ru.png`;
- `tests/e2e/web-shell/test-results/web-shell-system-surfaces--2881d-d-explicitly-fixture-backed-web-1920/system-404-ru.png`;
- `tests/e2e/web-shell/test-results/web-shell-200-percent-refl-3c64b-otion-keep-the-shell-usable-web-768/zoom-200-reduced-motion.png`;
- `tests/e2e/web-shell/test-results/web-shell-200-percent-refl-3c64b-otion-keep-the-shell-usable-web-1920/zoom-200-reduced-motion.png`.

## Contract impact

| Boundary | Classification | Disposition |
|---|---|---|
| Browser-visible shell and route resolution | `compatible-change` | Provisional composition is replaced while canonical IDs/URLs, history, Back, refresh, localized titles, and fallback seams remain available. |
| Internal feature-route registration port | `compatible-change` | Additive typed lazy discovery by stable route ID; later slices add disjoint `*.feature-route.tsx` files without editing a central registry. |
| Public API, DTO, persisted schema, config schema | `none` | No backend, manifest, schema, migration, or deployment path changed. |
| Request hash, cache key, persistence identity | `none` | Route identity remains contract-owned; locale and presentation state do not alter domain identity. |
| Service-call auth/timeout/retry/error semantics | `none` | Existing health presentation probe remains non-authoritative; system fixtures explicitly disclose that backend decisions were not run. |
| External side effects/idempotency/unknown state | `none` | Browser tests use local read-only contract fixtures only. |
| Logs, metrics, traces, audit, redaction, alerts, runbooks | `none` | No operator contract changed; safe guidance is presentation copy only. |
| Rollout gate | `compatible-change` | Foundation, Help, planned surface, and both prototype fallbacks remain; removal requires later real-API and performance evidence. |
| Measured performance | `unknown` | Build emitted a size warning; W31 collected no benchmark and makes no performance-readiness claim. |

## Verdict

`passed`. Browser QA verdict is `ready` only for the declared local production-shell, route-resolution, system-presentation, responsive-Web, and accessibility-smoke boundary. Residual risk remains in real authorization/API integration, screen-reader coverage, measured bundle/runtime performance, and release/runtime proof. The next safe action is owner activation of a dependent ticket only after W31 frontmatter validates as `accepted`.
