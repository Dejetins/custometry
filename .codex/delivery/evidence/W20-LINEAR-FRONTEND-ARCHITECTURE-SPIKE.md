---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: W20-LINEAR-FRONTEND-ARCHITECTURE-SPIKE
proof_boundary: browser-proven-custometry-frontend-architecture-and-local-performance-spike
proof_skills: [browser-qa-evidence, backend-performance-evidence, playwright]
verdict: passed
redaction: All browser and performance inputs are deterministic project-owned local fixtures; no credentials, cookies, storage state, private data, provider payloads, screenshots, or traces are committed. Passing traces remain ephemeral under ignored test-results paths.
executed_checks:
  - verify local main and isolated W20 worktree base at 13c46d21a44bbef8ebb82ca55dae5419179382ff
  - verify W20 ready, W19 accepted, W19 evidence passed, W19 commit ancestry, disjoint active ownership, and isolation from W12 and foreign main-worktree changes
  - git fetch origin and verify 1c70d5240bca22d83eb8433e2de161d5c1a90739 is the current origin/main
  - git rebase --onto origin/main 643c35b719f6268ca4cb55bd19d6dda82b899f9d codex/w20-linear-frontend-architecture-spike
  - source scripts/activate-toolchain.sh && pnpm --filter @custometry/web lint
  - source scripts/activate-toolchain.sh && pnpm --filter @custometry/web typecheck
  - source scripts/activate-toolchain.sh && pnpm --filter @custometry/web test
  - source scripts/activate-toolchain.sh && pnpm --filter @custometry/web build
  - source scripts/activate-toolchain.sh && pnpm --filter @custometry/ui-foundation lint
  - source scripts/activate-toolchain.sh && pnpm --filter @custometry/ui-foundation test
  - source scripts/activate-toolchain.sh && pnpm exec playwright test --config apps/web/playwright.spike.config.cjs
  - source scripts/activate-toolchain.sh && pnpm exec playwright test --config tests/performance/playwright.config.ts
  - source scripts/activate-toolchain.sh && pnpm exec playwright test --config tests/performance/playwright.config.ts --repeat-each=2 --workers=1
  - docker build --file apps/web/Dockerfile --target web-build --tag custometry-w20-web-build-check:local .
  - source scripts/activate-toolchain.sh && uv run --locked python -m tools.custometry_quality.validate_delivery_tickets
  - source scripts/activate-toolchain.sh && uv run --locked python -m tools.check --scope local
  - git diff --check
observations:
  - The legacy UI-AN-003 surface remains the default and the spike mounts only at the route-bounded view=linear-spike state; rollback, refresh, Back, and Forward were observed in Chromium.
  - MobX owns only theme and bounded sidebar geometry; TanStack Query owns typed REST and SSE snapshots, refresh, cache, and request cancellation.
  - Exactly abyss, graphite, frost, and paper are available through typed semantic CSS variables; all four switched without reload or server-snapshot identity changes.
  - Post-rebase browser proof passed 6 of 6 tests at 1440x900 and 1280x800 with zero console errors, page errors, or unexpected failed requests.
  - Three sequential post-rebase 30-sample performance runs passed the declared client-overhead budgets on Apple M3 Pro hardware; no long task above 50 ms was observed.
  - The Web image build stage includes the ui-foundation manifest and source explicitly; its isolated Docker build passed after PR CI exposed the selective-copy omission.
  - The production Web bundle measured 460774 raw bytes and 143428 gzip bytes across generated JavaScript and CSS.
---

# W20-LINEAR-FRONTEND-ARCHITECTURE-SPIKE Evidence

> Compact evidence for one terminal ticket. It is not another execution-state
> source or a replacement for the product specification.

## Outcome and scope

- outcome: a minimal browser slice falsifiably proves the accepted React,
  MobX, TanStack Query, styled-components, semantic-token, typed REST/SSE,
  reversible route-boundary, and repeatable client-performance architecture;
- requirement IDs: [WEB-ARCH-001, WEB-ARCH-002, WEB-ARCH-003, WEB-ARCH-004,
  WEB-ARCH-006, WEB-PERF-001, WEB-PERF-002, WEB-PERF-003, WEB-PERF-004,
  WEB-PERF-005, WEB-PERF-006, THEME-001, THEME-005];
- included: `apps/web/**`, `packages/ui-foundation/**`, exact dependency and
  lock updates, ticket-owned unit/browser/performance tests, and this evidence;
- exclusions: no backend, API contract, persistence, blueprint, docs, Penpot,
  deploy orchestration, migration, release, or production data change;
  deterministic mock latency is not real API latency or release performance
  evidence.

## Preflight and isolation

| Check | Result | Observation |
| --- | --- | --- |
| Base | pass | Local `main` and new branch base were exactly `13c46d21a44bbef8ebb82ca55dae5419179382ff`. |
| Predecessor | pass | W19 was `accepted`; `.codex/delivery/evidence/W19-LINEAR-REFERENCE-COMPLETION.md` existed with `verdict: passed`; `d7a33c53925dc090cead912fe80dc02650125eae` was an ancestor of the base. |
| Frontier | pass | W20 was `ready` before mutation and no base ticket had `status: active`; the target branch and worktree path were absent. |
| Ownership | pass | W12 remained in `/Users/daniildegtyarev/Projects/Custometry-roe-12` with backend/API/identity/migration ownership and `apps/web/**` forbidden. Its dirty paths were disjoint. |
| Foreign changes | pass | Main-worktree edits in `.codex/AGENTS.md` and `.codex/agents/ticket_template.md` were not inherited by the clean worktree created at `/Users/daniildegtyarev/Projects/Custometry-w20`. |
| Git handoff base | pass | After `git fetch origin`, `origin/main` was exactly `1c70d5240bca22d83eb8433e2de161d5c1a90739`; the requested `--onto` rebase completed without conflicts and did not replay obsolete W12 coordination commit `643c35b719f6268ca4cb55bd19d6dda82b899f9d`. |

## Architecture observation

| Boundary | Proven implementation seam |
| --- | --- |
| Reversible route | `/w/northwind-retail/analytics/sales` remains the legacy planned surface. `?view=linear-spike` mounts the new slice; the rollback link removes only the presentation query. Refresh, Back, and Forward preserve the canonical route and expected surface. |
| Local state | `SpikeUiStore` uses MobX only for theme and sidebar geometry. Width is clamped to 208-320 px, defaults to 240 px, persists locally, supports pointer drag, ArrowLeft/ArrowRight steps, Home reset, and double-click reset. |
| Server state | TanStack Query owns the snapshot query key, refresh/cache behavior, abort signal, cancellation, and SSE cache replacement. MobX contains no snapshot, authorization, persistence, or terminal-domain field. |
| Typed adapters | REST and SSE payloads pass an explicit runtime type guard before becoming `WorkspaceSnapshot`; transport receipt metadata is presentation-only and separately measured. |
| Themes | `@custometry/ui-foundation` exports exactly `abyss`, `graphite`, `frost`, and `paper`, with `graphite` as UI default and `paper` as static default. styled-components owns composition and only project-owned semantic CSS variables cross the runtime theme boundary. |
| Rollback | The pre-existing `PlannedSurface` remains callable and default. W20 does not remove or relabel it as implemented product behavior. |

Pinned additions were `mobx@6.13.7`, `mobx-react-lite@4.1.0`,
`@tanstack/react-query@5.81.5`, and `styled-components@6.1.19`.
`@playwright/test@1.52.0` was also pinned at the root so ticket-owned external
specs resolve under pnpm's isolated dependency model. Supply-chain lockfile
verification passed during installation. No backend or contract dependency was
added or changed.

## Commands and observations

| Command or action | Result | Redacted observation / durable reference |
| --- | --- | --- |
| `pnpm --filter @custometry/web lint` | pass | TypeScript completed with no diagnostics. |
| `pnpm --filter @custometry/web typecheck` | pass | TypeScript completed with no diagnostics. |
| `pnpm --filter @custometry/web test` | pass | 2 files, 10 tests passed, including legacy shell regression and W20 state/cancel/rollback tests. |
| `pnpm --filter @custometry/ui-foundation lint` | pass | TypeScript completed with no diagnostics. |
| `pnpm --filter @custometry/ui-foundation test` | pass | 1 file, 2 tests passed for exact theme order/defaults and semantic CSS boundary. |
| `pnpm --filter @custometry/web build` | pass | Vite 6.3.5 transformed 1,762 modules. Generated JS was 452.32 kB raw / 141.05 kB gzip and CSS was 8.45 kB raw / 2.38 kB gzip. |
| `pnpm exec playwright test --config apps/web/playwright.spike.config.cjs` | pass | Post-rebase 6/6 Chromium tests passed in 7.1 s at 1440x900 and 1280x800. Route mount/rollback/history/refresh, four-theme switch, pointer and keyboard resize/persistence, REST cancellation, SSE replacement, reserved layout, overflow, console, page-error, and failed-request boundaries were exercised. |
| Passing browser traces | pass, ephemeral | Six `trace.zip` files were produced below ignored `apps/web/test-results/w20-browser/**`. They contain only deterministic local fixture traffic and are not tracked. Screenshots were configured failure-only and no passing screenshot was retained. |
| `pnpm exec playwright test --config tests/performance/playwright.config.ts` | pass | Canonical post-rebase standalone 30-sample run passed in 6.2 s; two additional sequential 30-sample reruns passed in 10.8 s total. The first revalidation attempt exposed a REST/SSE mock race; phase-gating deterministic SSE traffic removed the race without changing measured application code or budgets. |
| `docker build --file apps/web/Dockerfile --target web-build --tag custometry-w20-web-build-check:local .` | pass | PR CI run `29842728443` exposed that the selective Web image context omitted the new workspace package. Adding only the ui-foundation manifest and source `COPY` boundaries made the isolated Web build pass with the same 1,762-module production output. |
| `uv run --locked python -m tools.custometry_quality.validate_delivery_tickets` | pass | Post-rebase `PASS validate_delivery_tickets (observed=true)` with 26 tickets and W20 accepted. |
| `uv run --locked python -m tools.check --scope local` | pass | Post-rebase `PASS check:local (observed=true)` under Node 24.18.0, pnpm 11.13.0, uv 0.9.26, and Python 3.12.2. |
| `git diff --check` | pass | No whitespace errors. |

## Browser QA boundary

- target/build: local Vite W20 working tree rebased onto
  `origin/main` at `1c70d5240bca22d83eb8433e2de161d5c1a90739`; no deployment;
- browser: Playwright Chromium `136.0.7103.25`;
- viewports: 1440x900 and 1280x800 CSS px;
- auth/data: no credentials or authenticated private data; only project-owned
  `northwind-retail` synthetic fixture data with 12-13 result rows;
- observed states: legacy, spike mounting, REST success, SSE success,
  refreshing with prior layout retained, cancellation, four themes, persisted
  resize, refresh, rollback, Back, and Forward;
- console/network: zero console errors, zero page errors, and zero unexpected
  failed requests. Expected `net::ERR_ABORTED` events from route-unmount
  AbortController cleanup, EventSource close, and the explicit cancellation
  proof were classified separately;
- readiness: `ready` at the W20 browser-spike boundary only. Real auth, real API,
  error/forbidden/session-expired states, WCAG contrast, localization,
  reduced-motion, Compose, recovery, and release remain W22/W23 proof.

## Performance method and results

The harness is an explicit ticket hot-path marker, not a speculative
optimization benchmark. It measures current client overhead against the
accepted budgets and makes no before/after performance-win claim.

Environment and workload:

- macOS 15.7.4 arm64, Apple M3 Pro, 11 logical CPUs, 19,327,352,832 bytes RAM;
- Playwright Chromium 136.0.7103.25, 1440x900 viewport,
  `navigator.hardwareConcurrency=11`;
- 12-row deterministic snapshot, 30 warm samples after one cold mount;
- TanStack Query warm cache with explicit REST refetch;
- same-process Playwright route boundary with deterministic phased 15 ms REST
  and 12 ms SSE fixture delay; this delay is mock transport, not API latency;
- client dispatch is interaction handler to query-function dispatch;
  REST/SSE-to-paint uses transport receipt to the second animation frame;
  INP uses Chromium Event Timing interaction entries; long tasks use the
  browser Long Tasks observer.

Canonical standalone run:

| Metric (ms) | n | p50 | p75 | p95 | max | Budget result |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Client dispatch | 30 | 0.1 | 0.1 | 0.2 | 0.2 | pass: p75 <=20, p95 <=50 |
| REST response-to-paint | 30 | 30.0 | 30.5 | 32.6 | 46.3 | pass: p75 <=100, p95 <=200 |
| SSE receipt-to-paint | 30 | 24.5 | 31.2 | 33.6 | 34.3 | pass: p75 <=100, p95 <=200 |
| INP/Event Timing | 72 | 16 | 16 | 16 | 16 | pass: p75 <=100, max <=200 |
| Long task | 0 | 0 | 0 | 0 | 0 | pass: no task >50 ms |

Across all three sequential post-rebase runs, the p75/p95 envelopes were:
client dispatch `0.1-0.2 / 0.2-0.3 ms`; REST-to-paint `27.8-30.5 /
31.3-32.6 ms`; SSE-to-paint `31.2-32.2 / 33.0-34.1 ms`; INP `16 / 16 ms`,
with maximum 16 ms; long tasks above 50 ms remained zero. The produced JS+CSS
bundle was 460,774 raw bytes and 143,428 gzip bytes. These results validate the
seam and measurement method on the declared hardware; W22/W23 must remeasure
real API/network/render work and the lowest supported client profile.

## Contract impact and handoff decision

| Surface | Classification | Result |
| --- | --- | --- |
| Backend/API/persistence/migrations | `none` | No files or contracts changed. |
| Frontend dependencies | `breaking-change before first stable Web release` | Accepted stack dependencies are pinned and isolated behind the spike route. |
| Route identity | `compatible-change with fallback` | `UI-AN-003` and its canonical path are unchanged; the legacy surface remains default. |
| Theme IDs/tokens | `breaking-change before first stable theme consumer` | The spike exposes only the accepted four IDs through semantic variables. |
| Browser behavior | `compatible experimental slice` | Opt-in route view is reversible and browser-proven; it is not the W22 production shell. |
| Performance | `directional local evidence` | Client overhead passes initial budgets under deterministic mocks; real API and release claims remain unverified. |

Decision: **proceed** with W21's separate Penpot vNext foundations because no
architecture change or stop condition was found. W22 may **proceed after W21 is
accepted**, retaining this route boundary, state separation, and harness while
adding real authentication/API states, accessibility/contrast/localization,
reduced motion, real network/API/render decomposition, and production-shell
browser evidence. W20 does not authorize W22 to start before its graph
predecessor is accepted.

## Verdict

`passed` at the declared browser-proven frontend-architecture and local
performance-spike boundary. The evidence is sufficient to accept W20, but it
does not claim a production shell, real API latency, release readiness, or
deployment evidence.
