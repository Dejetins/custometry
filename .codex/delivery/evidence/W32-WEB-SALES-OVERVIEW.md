---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.10.0-draft
ticket_id: W32-WEB-SALES-OVERVIEW
proof_boundary: production-ui-an-003-with-real-adapter-or-explicit-unavailable-boundary-and-real-browser-observation
proof_skills: [contract-impact-analysis, better-accessibility, browser-qa-evidence, playwright-cli]
verdict: passed
redaction: No credentials, cookies, browser storage, provider payloads, or production data were captured; browser integration used disposable PostgreSQL, deterministic governed Parquet data, and explicit fixture tokens.
executed_checks:
  - source scripts/activate-toolchain.sh && pnpm --filter @custometry/web exec vitest run tests/architecture-spike.test.tsx
  - source scripts/activate-toolchain.sh && pnpm --filter @custometry/web exec vitest run tests/analytics-sales/analytics-sales-api.test.ts tests/analytics-sales/sales-overview.test.tsx
  - source scripts/activate-toolchain.sh && pnpm --filter @custometry/web test
  - source scripts/activate-toolchain.sh && pnpm --filter @custometry/web lint && pnpm --filter @custometry/web build
  - source scripts/activate-toolchain.sh && pnpm --filter @custometry/web exec playwright test --config ../../tests/e2e/web-analytics-sales/playwright.config.ts
  - uv run python -m tools.custometry_quality.validate_delivery_contract --contract /Users/daniildegtyarev/.codex/skills/delivery-orchestrator/references/delivery-contract-v1.md
  - uv run python -m tools.custometry_quality.validate_delivery_tickets
  - uv run python -m tools.custometry_quality.validate_route_registry
  - uv run python -m tools.custometry_quality.check_i18n_parity
  - uv run python -m tools.custometry_quality.check_ddd_boundaries
  - uv run python -m tools.custometry_quality.check_contract_drift
  - uv run python -m tools.check --scope local
  - git diff --check
observations:
  - W32 focused adapter and component tests passed 7/7; the user-authorized legacy W20 route rollback correction retained 4/4 focused tests.
  - The complete Web Vitest suite passed 67/67; TypeScript lint and the Vite production build passed.
  - Playwright ran only the W32 spec against projects web-768 at 768x1024 and web-1920 at 1920x1080; 8/8 tests passed.
  - The real browser path performed successful GET and POST calls through the production W16 FastAPI adapter, AnalyticsService, PostgresAnalyticsRepository, disposable migrated PostgreSQL, governed Parquet source artifact, and immutable local result store.
  - Initial real metrics were revenue 425, orders 2, and AOV 212.5; applying store-1 and web typed filters through the real W16 POST boundary returned revenue 145, orders 1, and AOV 145.
  - Read-only analysis.read visibility and a fail-closed 403 boundary were observed; expected browser resource messages were limited to the intentional 403 scenario.
  - RU and EN, Result Trust, period/comparison/filter behavior, loading, empty, ready, refreshing, stale, degraded, forbidden, and failed states, keyboard focus restoration, visible focus, reduced motion, accessibility semantics, and 200-percent reflow-equivalent geometry were observed.
  - No unexpected console errors, page errors, request failures, HTTP error responses, whole-page horizontal overflow, or observed clipping occurred in successful browser scenarios.
  - Loading, empty, stale, degraded, refreshing-failure, and failed presentation states used browser interception and are not claimed as backend/runtime proof.
---

# W32 Web Sales Overview Evidence

> Compact evidence for one terminal ticket. It is not another execution-state
> source or a replacement for the product specification.

## Outcome and scope

- outcome: canonical `/w/:workspaceKey/analytics/sales` now loads production `UI-AN-003` inside the accepted W31 shell, consumes the policy-visible W16 sales result through a typed adapter, and presents governed metrics, comparison/filter controls, trust context, availability limits, and required route states;
- requirement IDs: [UC-004, UC-012, UC-027, DISCOUNT-001, DISCOUNT-004, DISCOUNT-005, DISCOUNT-008, DISCOUNT-009, DISCOUNT-010, DISCOUNT-011, DISCOUNT-012, DISCOUNT-013, DISCOUNT-014, DISCOUNT-015, DISCOUNT-016, DISCOUNT-017, DISCOUNT-018, DISCOUNT-019, PVM-001, PVM-002, PVM-003, PVM-004, PVM-005, PVM-006, METRIC-017, METRIC-019, METHOD-010, METHOD-011, METHOD-012, UI-DENSITY-001, UI-DENSITY-002, UI-DENSITY-003, A11Y-001];
- included: revenue, orders, AOV, aggregate recorded discount and revenue contribution, governed period/comparison/store/channel filters, W16 policy/freshness/quality/lineage Result Trust, RU/EN, read-only/forbidden behavior, responsive Web at 768 and 1920 CSS px, keyboard/focus, reduced motion, 200-percent reflow-equivalent smoke, accessibility semantics, and truthful unavailable boundaries for data W16 does not expose;
- bounded shared correction: `apps/web/tests/architecture-spike.test.tsx` now expects the accepted production `UI-AN-003` terminal state after legacy `?view=linear-spike` rollback instead of the superseded planned surface; navigation and rollback coverage remain intact;
- exclusions: W16 backend/API/contracts/migrations, production authentication, production data, production PostgreSQL/runtime, deployment, release, full WCAG or screen-reader certification, performance readiness, causal attribution, and unavailable margin/time-series/product/store/channel/PVM computations.

## Commands and observations

| Command or action | Result | Redacted observation / durable reference |
|---|---|---|
| `source scripts/activate-toolchain.sh && pnpm --filter @custometry/web exec vitest run tests/architecture-spike.test.tsx` | pass | Legacy W20 navigation/rollback suite `4/4`; canonical rollback now terminates at production W32 behavior and rejects `Planned surface`. |
| `source scripts/activate-toolchain.sh && pnpm --filter @custometry/web exec vitest run tests/analytics-sales/analytics-sales-api.test.ts tests/analytics-sales/sales-overview.test.tsx` | pass | W32 typed adapter and component/state tests `7/7`. |
| `source scripts/activate-toolchain.sh && pnpm --filter @custometry/web test` | pass | Complete Web Vitest suite `67/67`. |
| `source scripts/activate-toolchain.sh && pnpm --filter @custometry/web lint && pnpm --filter @custometry/web build` | pass | TypeScript passed; Vite production build passed. The existing main bundle emitted a non-fatal size warning, so no performance claim is made. |
| `source scripts/activate-toolchain.sh && pnpm --filter @custometry/web exec playwright test --config ../../tests/e2e/web-analytics-sales/playwright.config.ts` | pass | `8/8` across `web-768` and `web-1920`; real W16 GET/POST, policy, RU/EN, trust, state, keyboard, reflow, motion, diagnostics, and geometry checks passed. |
| Visual inspection of Playwright captures | pass | The 768 and 1920 ready/filter views and RU reflow-equivalent capture preserve the accepted Graphite shell direction without observed overlap, clipping, or horizontal overflow. |
| `uv run python -m tools.custometry_quality.validate_delivery_contract --contract /Users/daniildegtyarev/.codex/skills/delivery-orchestrator/references/delivery-contract-v1.md` | pass | Repository adapter, installed delivery contract, skill, and global router observed. |
| `uv run python -m tools.custometry_quality.validate_delivery_tickets` | pass | Delivery ticket graph and evidence schema validated. |
| `uv run python -m tools.custometry_quality.validate_route_registry` | pass | `117` route contracts and `5` system surfaces validated without contract mutation. |
| `uv run python -m tools.custometry_quality.check_i18n_parity` | pass | `200` English and `200` Russian catalog keys remain aligned; W32 copy is feature-local and covered in both languages. |
| `uv run python -m tools.custometry_quality.check_ddd_boundaries` | pass | Python/TypeScript boundary policy passed. |
| `uv run python -m tools.custometry_quality.check_contract_drift` | pass | Generated API client and schema bindings remain byte/semantic aligned; W32 changed no provider contract. |
| `uv run python -m tools.check --scope local` | pass | Grouped local repository profile passed. |
| `git diff --check` | pass | No whitespace errors in the staged W32 boundary. |

## Real boundary versus fixture-only proof

- real integration: production `create_analytics_app`, `AnalyticsService`, `PostgresAnalyticsRepository`, migrated PostgreSQL schema, governed semantic projection view, content-hash-verified Parquet receipt artifact, immutable analytics result artifact, policy-filtered list, and typed run request;
- fixture-only: deterministic receipts, loopback fixture token identity, disposable database lifecycle, and test-owned reset/health endpoints;
- presentation-only: browser interception for loading, empty, stale, degraded, refreshing dependency failure, and initial failed states; those checks prove UI state handling only;
- not proven: production identity provider, secrets, production network/runtime, production database/data, deployment, recovery, or release behavior.

## Contract impact

| Boundary | Classification | Disposition |
|---|---|---|
| Browser-visible `UI-AN-003` route | `compatible-change` | The contract-owned canonical URL and W31 shell identity remain stable while the planned fallback is replaced by the ticketed production surface. |
| Internal browser analytics adapter | `compatible-change` | Additive typed consumer of existing W16 identity and analytics endpoints; no provider DTO or error contract changed. |
| Legacy W20 rollback expectation | `compatible-change` | User-authorized test-only correction preserves navigation/history coverage and updates only the superseded terminal surface expectation. |
| Public API, DTO, persisted schema, migrations, config | `none` | No backend, contract, schema, migration, configuration, or deployment path changed. |
| Request/policy/filter/result identity | `none` | W16 continues to own request, policy, filter, result, artifact, and lineage hashes. |
| Discount and PVM semantics | `none` | UI reports aggregate recorded discount only and explicitly declines component, cap, value-origin, causal, or PVM claims unavailable from W16. |
| Measured performance | `unknown` | No benchmark was run; the build warning is retained as residual risk. |

## Verdict

`passed`. W32 is accepted for the declared local production `UI-AN-003`, real
W16 adapter/API/PostgreSQL integration, responsive browser, and accessibility-
smoke boundary. Residual risk remains in production identity/runtime/data,
screen-reader certification, measured bundle/runtime performance, and the
future backend projections required to replace explicit unavailable margin,
trend, dimensional breakdown, and PVM states. No W33 path, backend contract,
publication, release, or deployment action was performed.
