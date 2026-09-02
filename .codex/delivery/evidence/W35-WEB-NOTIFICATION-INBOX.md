---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.10.0-draft
ticket_id: W35-WEB-NOTIFICATION-INBOX
proof_boundary: production-ui-notify-001-with-real-adapter-or-explicit-unavailable-boundary-and-real-browser-observation
proof_skills: [contract-impact-analysis, better-accessibility, browser-qa-evidence, playwright-cli]
verdict: passed
redaction: Disposable PostgreSQL credentials, container identity and port, connection strings, bearer fixtures, process identifiers, browser storage, and raw provider payloads were not retained. Screenshots contain only deterministic fictional operational data and public route/status text.
executed_checks:
  - git fetch origin --prune and verify exact clean HEAD 3562700d1bbfaca54791ffcfd0c8102355a2087c, parent b2124fc2b3f73b2f1f1c265453fa072b625e35e4, origin/main 68ad124ac6c7400c67df8bdd75752fe1bd350e76, W31 and W37 accepted/passed ancestry, W35 ready with no blockers, complete context source existence, and no foreign overlap
  - uv run python -m tools.custometry_quality.validate_delivery_tickets
  - uv run python -m tools.custometry_quality.validate_route_registry
  - uv run python -m tools.custometry_quality.check_i18n_parity
  - source scripts/activate-toolchain.sh and pnpm --filter @custometry/web lint and pnpm --filter @custometry/web test and pnpm --filter @custometry/web build
  - uv run --locked ruff check tests/e2e/web-notifications/real_api_fixture.py
  - source scripts/activate-toolchain.sh and pnpm --filter @custometry/web exec playwright test --config ../../tests/e2e/web-notifications/playwright.config.ts
  - source scripts/activate-toolchain.sh and uv run --locked python -m tools.check --scope local
  - git diff --check
observations:
  - >-
    Delivery routing selected exactly one ready ticket, W35, on common-base handoff
    3562700d1bbfaca54791ffcfd0c8102355a2087c. Accepted W31 shell and W37 API commits
    b2124fc2b3f73b2f1f1c265453fa072b625e35e4 and its W38 ancestor
    1255247c65639fe1a44644617365f56b464ba1cb were present with passed evidence.
    No W31 shell, shared UI foundation, backend, API, migration, route/surface contract,
    blueprint, generated UI-program, deploy, or foreign file changed.
  - >-
    UI-NOTIFY-001 is a lazy production feature route at /notifications inside the accepted
    W31 shell. It consumes W37 generated operation paths and typed DTO semantics, sends
    contract/request/idempotency identities, preserves stable error codes and revisions,
    and implements severity, category, read, acknowledged, and resolved filters, duplicate
    group counts, localized details, separate read/dismiss/acknowledged/resolved meanings,
    and permission-aware actions.
  - >-
    Deep links accept only exact UI-OPS-001/UI-OPS-002/UI-OPS-003 route/parameter shapes,
    reject arbitrary URLs, traversal identities and extra parameters, and navigate through
    React Router so the target route reauthorizes. Browser proof covers the accepted W31
    northwind-retail workspace-key default. The accepted W37 identity capability exposes a
    workspace UUID, not a route workspace key, so multi-workspace UUID-to-key resolution is
    outside W35 and remains unproven without a shared contract change.
  - >-
    The real browser boundary launched pinned disposable PostgreSQL 17.5, applied Alembic
    0001 through 0009, and mounted the unchanged production W37 FastAPI router,
    NotificationInboxService, and PostgresNotificationStore. Deterministic Identity,
    recipient, resource-access, reset/revoke controls, and bearer actors were test fixtures;
    production session issuance and shell-to-Authorization delivery were not available in the
    accepted W31/W37 boundary and are explicitly not claimed.
  - >-
    Against that real database/API boundary, Chromium observed three grouped inbox rows,
    all five filters, stale disclosure, critical acknowledgement, durable acknowledgement
    after reload, safe run navigation, missing acknowledgement permission, initial 403,
    resource-access revocation, and fail-closed empty results. Loading, empty, and 503 failed
    presentation states used browser interception only; they do not prove backend failure
    semantics. Stale/degraded, forbidden, filtering, persistence, revocation, and navigation
    used the real W37 adapter.
  - >-
    Playwright CLI passed eight tests with no retry at 768x1024 and 1920x1080 in English and
    Russian. The keyboard flow activated the accepted skip link, traversed to notification
    details, opened and escaped the native modal dialog, and restored focus to its trigger.
    Labels, dialog naming, live status, semantic alerts, visible focus, 44px close target,
    200-percent reflow equivalents at 384x512 and 960x540, reduced motion, and whole-page
    overflow were observed. Normal cases had zero console, page, request, or HTTP errors;
    the negative authorization case contained only the expected 403 browser diagnostics.
  - >-
    Fresh full-page screenshots show no inbox control/card clipping or horizontal overflow.
    At the narrow W31 shell layout, the inherited sidebar More sections label is visually
    clipped while the notification surface remains contained; that shell observation is
    outside W35 write authority and was not repaired or counted as new shell proof.
  - >-
    Focused TypeScript lint passed; Vitest passed 53 tests in 9 files; the production build
    passed with a 22.42 kB UI-NOTIFY-001 lazy chunk. Vite retained the pre-existing non-fatal
    warning for the 591.81 kB main bundle. Delivery, route and RU/EN parity validators, the
    locked Python fixture lint, grouped local gate, and whitespace check passed.
  - >-
    Contract impact is compatible-change at the browser consumer boundary: the planned
    UI-NOTIFY-001 route now loads an additive feature through the existing loader seam and
    existing W37 API. Public APIs, DTOs, ports, persisted schema, config/defaults, request
    hashes, cache keys, identity semantics, migrations, route/surface contracts, shell
    behavior, backend side effects, release and deployment are unchanged.
---

# W35 Web Notification Inbox Evidence

## Outcome and scope

- outcome: `/notifications` renders the production `UI-NOTIFY-001` inbox in
  the accepted W31 shell with typed W37 data, five filters, grouped events,
  details, safe navigation, localized state/action copy, and permission-aware
  read, dismiss, and acknowledge behavior;
- dependency proof: W31 and W37 are `accepted` with `verdict: passed` in the
  exact combined ancestry; accepted W38 remains an ancestor of W37;
- included: W35 feature/route code, focused unit tests, disposable real-W37
  browser fixture, accessibility/reflow/diagnostic smoke, ticket and evidence;
- excluded: shared shell/auth changes, API/backend/migrations/contracts,
  product blueprints, notification delivery/preferences, publication,
  release, deployment, performance, recovery, or a full-WCAG claim.

## Commands and observations

| Command or observation | Result | Proof boundary |
|---|---|---|
| Preflight fetch, YAML status/dependency/ancestry/source/ownership checks | pass | Exact clean base `3562700d1bbfaca54791ffcfd0c8102355a2087c`; `origin/main` observed at `68ad124ac6c7400c67df8bdd75752fe1bd350e76`. |
| `pnpm --filter @custometry/web lint` | pass | TypeScript `tsc --noEmit`. |
| `pnpm --filter @custometry/web test` | pass | 53 tests, 9 files, no skip. |
| `pnpm --filter @custometry/web build` | pass | Production route chunk built; existing main-bundle size warning only. |
| `uv run --locked ruff check tests/e2e/web-notifications/real_api_fixture.py` | pass | Test-only real-boundary fixture lint. |
| `pnpm --filter @custometry/web exec playwright test --config ../../tests/e2e/web-notifications/playwright.config.ts` | pass | 8/8 Chromium tests, no retry, two required viewports. |
| Delivery, route, and i18n validators | pass | 35 tickets, 117 routes, 200 RU/200 EN keys. |
| `source scripts/activate-toolchain.sh && uv run --locked python -m tools.check --scope local` | pass | Canonical grouped local profile on accepted W35 tree. |
| `git diff --check` | pass | No whitespace errors. |

## Browser observations

Fresh screenshots are retained in the ignored
`tests/e2e/web-notifications/test-results/**` run directory for the current
combined base. Both viewports captured real acknowledgement state, real
revocation, RU keyboard focus restoration, and reduced-motion/reflow state.
The inbox surface stayed within the viewport with readable labels, cards and
actions. No unexpected console/page/network errors were observed; expected
403 diagnostics were asserted only in the explicit denial/revocation case.

## Real versus fixture boundary

PostgreSQL migrations, W37 storage, service, HTTP adapter, query filtering,
grouping, mutation persistence, access revocation and authorization responses
are real repository code. Actor identity, recipient/resource grants, bearer
headers, reset/revoke controls, and deterministic source events are disposable
fixtures. Loading, empty and 503 presentation states are browser-intercepted.
No claim is made that the accepted W31 shell supplies a production bearer
credential or that a multi-workspace UUID can be resolved to its route key;
both would require authority outside W35.

## Contract impact and residual risk

Overall classification is `compatible-change`. W35 is an additive consumer of
the existing W31 feature-loader and W37 contract. No producer contract,
persistence, config, identity, migration, route registry, shared shell, or
backend behavior changed.

Residual risk is limited to the explicit proof boundary: production
session-to-bearer delivery and multi-workspace route-key resolution are not
available from the accepted shared seams; the current browser proof injects a
fixture bearer and covers the accepted `northwind-retail` shell default. The
existing W31 narrow-sidebar label clipping and main-bundle size warning remain
outside W35. These limitations do not weaken the observed W35 feature behavior
or the real W37 persistence/authorization proof described above.

## Verdict

`passed` at
`production-ui-notify-001-with-real-adapter-or-explicit-unavailable-boundary-and-real-browser-observation`.
W35 may move from `ready` to `accepted`; no later ticket, publication, release,
or deployment is implied.
