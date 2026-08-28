---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.10.0-draft
ticket_id: W34-WEB-OPERATOR-RUNS
proof_boundary: production-ui-ops-001-with-real-adapter-or-explicit-unavailable-boundary-and-real-browser-observation
proof_skills: [contract-impact-analysis, better-accessibility, browser-qa-evidence, playwright-cli]
verdict: passed
redaction: Disposable PostgreSQL and Valkey credentials, container identities, ports, connection strings, actor tokens, raw payloads, cookies, and browser storage were not retained. Evidence records only safe counts, stable codes, commands, local fixture identities, and repository paths.
executed_checks:
  - git fetch origin main and exact clean preflight at 6abf3338766a4b9b358abadc8aec0f7bbc217209 with parent 8966c164effefa3d0d3207253260edc905138aba, origin/main 68ad124ac6c7400c67df8bdd75752fe1bd350e76, W34 ready, and accepted/passed W31/W36 ancestry
  - source scripts/activate-toolchain.sh and uv run --locked ruff check tests/e2e/web-operator-runs/real_execution_fixture.py
  - source scripts/activate-toolchain.sh and pnpm --filter @custometry/web lint and pnpm --filter @custometry/web test and pnpm --filter @custometry/web build
  - source scripts/activate-toolchain.sh and pnpm --filter @custometry/web exec playwright test --config ../../tests/e2e/web-operator-runs/playwright.config.ts
  - playwright-cli named-session snapshot, filter, viewport, console, and network smoke against the same disposable W36 boundary
  - uv run python -m tools.custometry_quality.validate_route_registry
  - uv run python -m tools.custometry_quality.check_i18n_parity
  - uv run python -m tools.custometry_quality.check_ddd_boundaries
  - uv run python -m tools.custometry_quality.check_contract_drift
  - source scripts/activate-toolchain.sh and uv run python -m tools.check --scope local
  - git diff --check
observations:
  - Web TypeScript, Vitest, and Vite production build passed; the complete Web suite passed 60 tests and the W34 lazy feature chunk built independently.
  - Playwright ran only web-operator-runs.spec.ts through the ticket-owned loopback Vite and disposable API webServer lifecycle; 8/8 tests passed across web-768 at 768x1024 and web-1920 at 1920x1080.
  - The real browser boundary migrated disposable PostgreSQL 17.5 through revision 0009, mounted the unchanged production W36 FastAPI adapter and PostgresExecutionControlStore, and used unchanged ValkeyTaskQueue, ExecutionOutboxDispatcher, and DisposableExecutionWorker adapters against Valkey 8.0.1.
  - Real API observations covered queued, running, succeeded, failed, and cancelling list states; exact state, execution-kind, and safe-trace filters; queue counts, lanes, observation time, and automatic five-second refresh; safe trace identity; and bounded RESOURCE_LIMIT_EXCEEDED details with observed/configured limits and safe remediation.
  - Real persisted cancel moved RUNNING to CANCELLING, remained cancelling until the Valkey-delivered worker cleanup, then refreshed as CANCELLED. Real manual retry created a distinct run and attempt with retry_of_id ancestry and was delivered and claimed through the disposable worker.
  - Reconciliation expired a real PostgreSQL lease, fenced the stale attempt, created a retry attempt, and exposed two-attempt ancestry plus fencing tokens through the production detail projection.
  - Real policy actors proved operator actions, owner-only read with action suppression, and deny-before-presentation 403 behavior. No raw logs, inputs, artifacts, secrets, source values, or PII were rendered.
  - Fixture-only presentation checks were isolated in a separately named test and covered loading, empty, stale, degraded, and dependency-failed states through browser interception. Fixture identity tokens and reset/drain controls were outside the product API namespace and were not used to claim production authentication semantics.
  - RU and EN shipped presentation, keyboard-only traversal, native dialog Escape close and focus restoration, stable accessible names, status text beyond color, polite live updates, reduced motion, and 200-percent reflow-equivalent widths passed. No whole-page horizontal overflow was observed.
  - Playwright CLI independently observed 6 real runs, one result after FAILED filtering, zero horizontal overflow at both 768x1024 and 1920x1080, zero console errors, and successful identity/list/summary network responses. The shell's intentionally aborted readiness probe was followed by a successful readiness response and was not classified as a product request failure.
  - Visual inspection of both endpoint captures found no clipping, overlap, or unresolved empty grid slot after the compact queue-summary repair.
---

# W34 Web Operator Runs Evidence

## Outcome and scope

- outcome: `UI-OPS-001` is a production feature route at
  `/w/:workspaceKey/runs` in the accepted W31 shell, backed by a typed W36
  consumer adapter and operator-grade lifecycle, queue, filter, action,
  ancestry, failure, trace, localization, and accessibility presentation;
- requirement IDs: [UC-010, OPS-001, EXEC-STATE-001, EXEC-STATE-002,
  EXEC-STATE-006, EXEC-STATE-007, EXEC-CANCEL-005, ADMIN-003, ADMIN-005,
  A11Y-001, I18N-001];
- included: queued/running/succeeded/failed/cancelling presentation, queue
  summary, exact filters, five-second auto-refresh, permission-aware cancel and
  failed-node/full-rerun actions with mandatory audit reason, run/attempt retry
  ancestry, safe trace identity, bounded failure copy, loading/empty/stale/
  degraded/forbidden/failed states, RU/EN, keyboard/focus/reflow/reduced-motion
  behavior, and real disposable W36 integration;
- exclusions: no W31 shell/foundation mutation, W36 API/contract/backend/
  migration mutation, route-contract or blueprint mutation, pending OPS G4
  acceptance, another operations route, Compose lifecycle, recovery drill,
  measured performance, full WCAG or screen-reader certification, release,
  publication, deployment, or production-runtime readiness.

## Commands and observations

| Command or action | Result | Boundary observation |
|---|---|---|
| `uv run --locked ruff check tests/e2e/web-operator-runs/real_execution_fixture.py` | pass | Ticket-owned disposable fixture is lint-clean. |
| `pnpm --filter @custometry/web lint` | pass | TypeScript contract and component surface compile. |
| `pnpm --filter @custometry/web test` | pass | Vitest `60/60`; focused W34 adapter/UI tests are included. |
| `pnpm --filter @custometry/web build` | pass | Vite emitted independent `UI-OPS-001` JS/CSS chunks; the pre-existing non-fatal main compatibility-bundle warning remained. |
| `pnpm --filter @custometry/web exec playwright test --config ../../tests/e2e/web-operator-runs/playwright.config.ts` | pass | `8/8`; real W36 boundary and isolated presentation fixtures at both required endpoint anchors. |
| `playwright-cli -s=w34 ...` | pass | Named Chromium session: real route, filter `6 → 1`, 768/1920 viewports, zero overflow, zero console errors, expected successful W36 network responses. |
| `validate_route_registry` | pass | 117 executable route contracts and 22 cross-surface capabilities remain valid; contracts were not modified. |
| `check_i18n_parity` | pass | Existing catalog parity remains `200/200`; W34 feature-local RU/EN copy is covered by focused and browser tests. |
| `check_ddd_boundaries` | pass | 22 contexts remain valid; the Web adapter consumes only the public generated W36 contract. |
| `check_contract_drift` | pass | Registered generated contract sources remain synchronized; W36 generated files were not changed. |
| `uv run python -m tools.check --scope local` | pass | Canonical bounded-handoff local profile passed on the implementation tree. |
| `git diff --check` | pass | No whitespace errors. |

### Browser evidence paths

- `tests/e2e/web-operator-runs/test-results/web-operator-runs-real-W36-187a0-nd-exposes-fencing-ancestry-web-768/real-w36-operator-runs.png`;
- `tests/e2e/web-operator-runs/test-results/web-operator-runs-real-W36-187a0-nd-exposes-fencing-ancestry-web-1920/real-w36-operator-runs.png`;
- `tests/e2e/web-operator-runs/test-results/web-operator-runs-real-W36-58c5f-ed-before-list-presentation-web-768/real-w36-forbidden.png`;
- `tests/e2e/web-operator-runs/test-results/web-operator-runs-RU-keybo-cbdb1-eflow-honors-reduced-motion-web-768/ru-keyboard-reflow-reduced-motion.png`;
- `tests/e2e/web-operator-runs/test-results/web-operator-runs-fixture--aea18-egraded-and-failed-distinct-web-768/fixture-only-presentation-states.png`;
- `tests/e2e/web-operator-runs/test-results/playwright-cli-768.png` and
  `tests/e2e/web-operator-runs/test-results/playwright-cli-1920.png`.

The captures and traces are ignored runtime output and are not committed.

## Contract impact

| Boundary | Classification | Disposition |
|---|---|---|
| Browser-visible `UI-OPS-001` behavior | `compatible-change` | A planned canonical route gains its production implementation without changing route ID, URL, role hints, guard, or query identity. |
| Internal Web execution consumer adapter | `compatible-change` | Additive typed consumer of existing generated W36 operation paths, version header, request identity, and idempotency requirements. |
| Public API contract | `none` | No W36 provider path, method, status, authorization, timeout, retry, or error semantic changed. |
| Port contract and DTO schema | `none` | Public ports, generated OpenAPI, TypeScript contract, and schemas are unchanged. |
| Persisted schema | `none` | No migration or backend persistence path changed; the fixture applies existing migrations only to disposable PostgreSQL. |
| Config schema/defaults | `none` | Product configuration is unchanged; loopback fixture ports are test-owned. |
| Request hash, cache key, persistence identity | `none` | The adapter supplies existing scoped idempotency and request identities; domain/run identity semantics are unchanged. |
| External side-effect idempotency and unknown state | `none` | UI exposes W36 durable follow-up truth and does not redefine cancel/retry outcomes. |
| Logs, metrics, traces, audit, reports, redaction | `compatible-change` | Safe trace IDs, stable codes, bounded remediation, and required audit reason become visible/collectable in UI; raw operational content remains excluded. |
| Alerts and runbooks | `none` | No trigger, severity, routing, or runbook contract changed. |
| Performance/rollout gate | `unknown` | No benchmark was run; existing lazy route loading limits the new feature chunk, but no performance claim is made. |

## Real versus fixture proof boundary

`Real`: disposable PostgreSQL migration/state, production W36 API/store,
policy filtering, list/detail/queue responses, cancellation and retry writes,
transition persistence, Valkey delivery, outbox dispatch, worker claim/cleanup,
fencing, reconciliation, and browser observation of their safe projections.

`Fixture-only`: deterministic local actor tokens, seed/reset/drain helpers,
presentation of stale/degraded freshness values not currently emitted by the
real store, delayed loading, empty response, and 503 response interception.
Those checks prove only W34 presentation behavior.

## Verdict

`passed`. Browser QA verdict is `ready` for the declared local production
`UI-OPS-001` and disposable real-W36 integration boundary. Residual risk remains
in production authentication/session composition, target Compose/network
lifecycle, real degraded queue projection emission, screen-reader coverage,
measured performance, recovery, release, and deployment proof. The next safe
action is a separately authorized ready ticket; W34 does not activate or begin
W32, W33, or any other unit.
