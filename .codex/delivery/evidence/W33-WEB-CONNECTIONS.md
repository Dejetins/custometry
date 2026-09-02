---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.10.0-draft
ticket_id: W33-WEB-CONNECTIONS
proof_boundary: production-ui-data-001-and-ui-data-002-with-real-adapter-or-explicit-unavailable-boundary-and-real-browser-observation
proof_skills: [contract-impact-analysis, better-accessibility, browser-qa-evidence, playwright-cli]
verdict: passed
redaction: No production credential, cookie, browser storage value, DSN, provider payload, source row, environment dump, or raw secret is retained; PostgreSQL passwords are generated at runtime for disposable containers, credential references are omitted from sessionStorage and browser captures, and observations contain only stable codes, bounded counts, safe fixture identifiers, commands, and repository paths.
executed_checks:
  - verify detached HEAD ba4a0ef68a04790400278d43d5850b2dd7efc948, parent 38dabec352ff9aae67127062cf70317f1195f85b, origin/main 68ad124ac6c7400c67df8bdd75752fe1bd350e76, ready W33, accepted W14/W31 with passed evidence, clean preflight, and disjoint W32 ownership
  - source scripts/activate-toolchain.sh && uv run ruff format tests/e2e/web-connections/real_source_intake_fixture.py && uv run ruff check tests/e2e/web-connections/real_source_intake_fixture.py
  - source scripts/activate-toolchain.sh && pnpm --filter @custometry/web lint && pnpm --filter @custometry/web test && pnpm --filter @custometry/web build
  - source scripts/activate-toolchain.sh && pnpm --filter @custometry/web exec playwright test --config ../../tests/e2e/web-connections/playwright.config.ts
  - uv run python -m tools.custometry_quality.validate_route_registry
  - uv run python -m tools.custometry_quality.check_i18n_parity
  - uv run python -m tools.custometry_quality.check_ddd_boundaries
  - uv run python -m tools.custometry_quality.check_contract_drift
  - uv run python -m tools.custometry_quality.validate_delivery_tickets
  - uv run python -m tools.custometry_quality.validate_delivery_contract --contract /Users/daniildegtyarev/.codex/skills/delivery-orchestrator/references/delivery-contract-v1.md
  - source scripts/activate-toolchain.sh && uv run python -m tools.check --scope local
  - git diff --check
observations:
  - W33 route, typed adapter, accessibility, unit, build, repository, real PostgreSQL/API, and browser checks passed.
  - Playwright ran only web-connections.spec.ts through ticket-owned loopback Vite and disposable W14 fixture projects web-768 and web-1920; 8/8 tests passed.
  - The real fixture migrated a disposable PostgreSQL 17.5 control database through revision 0009, ran the production W14 FastAPI router/service/Postgres repository/PostgreSQL connector, and used a second disposable PostgreSQL 17.5 source.
  - The real UI flow observed one persisted active connection, one audit event, a read-only connector test, two discovered catalog objects, authorization denial, response redaction, and a credential reference absent from sessionStorage and cleared after save.
  - W14 has no connection-list query and no persisted draft lifecycle; production UI-DATA-001 returns explicit CONNECTION_LIST_UNAVAILABLE without inventing a GET contract, while UI-DATA-002 stores only a non-secret same-tab draft and performs real create/test/discover operations.
  - Searchable list data and loading, empty, ready, refreshing, degraded, stale, forbidden, and failed presentation states use explicitly labeled DEV-only fixtures and are not persistence, provider-connectivity, or W14 API proof.
  - Console errors, page errors, unexpected request failures, HTTP error responses, and whole-page horizontal overflow were absent in the passing success diagnostics; keyboard focus, labels, 200-percent reflow equivalent, and reduced-motion styles passed at both viewports.
  - Visual review found no W33-owned clipping or overlap at 768 or 1920; the inherited collapsed W31 shell visibly clips its own More sections label at 768 and 200-percent zoom, outside W33 allowed write paths, and W33 makes no shell-readiness claim.
  - The first browser attempt found local port 8000 occupied by a parallel runtime; no product assertion ran. Ticket-owned Vite proxy and disposable W14 fixture were moved to 8033, after which the complete browser suite passed twice, including the final invalidated-evidence rerun.
---

# W33 Web Connections Evidence

> Compact terminal evidence for one execution unit. It does not extend W14,
> replace route or surface contracts, or certify W31-owned shell behavior.

## Outcome and scope

- outcome: production `UI-DATA-001` at `/w/:workspaceKey/connections` and
  `UI-DATA-002` at `/w/:workspaceKey/connections/new` now provide a cohesive
  connection-management slice through lazy contract-owned feature routes;
- requirement IDs: [UC-001, CONNECTOR-001, CONNECTOR-004, A11Y-001,
  I18N-001];
- included: typed W14 source-intake adapter, explicit unavailable list
  boundary, governed/searchable presentation list, status/owner metadata,
  connector selection, reference-only credential/profile fields, template
  version, validation/error-summary focus, tab-only non-secret draft restore,
  permission-aware controls, stable safe errors, create/test/discover feedback,
  RU/EN, responsive Web, reduced motion, and browser diagnostics;
- exclusions: no W14 backend/API/contract/plugin/migration mutation, no invented
  list or external-provider connectivity, no secret storage, no persisted draft
  lifecycle, no file upload, no full connector matrix, no screen-reader/full
  WCAG certification, no measured performance, and no deployment or release.

## Commands and observations

| Command or action | Result | Redacted observation |
|---|---|---|
| Base, dependency, evidence, ancestry, and ownership preflight | pass | Exact base/parent/origin matched; W14 and W31 were `accepted` with `passed` evidence; W32-owned analytics-sales paths and W33-owned connection paths were disjoint. |
| `source scripts/activate-toolchain.sh && uv run ruff format tests/e2e/web-connections/real_source_intake_fixture.py && uv run ruff check tests/e2e/web-connections/real_source_intake_fixture.py` | pass | Python browser fixture formatted; Ruff clean. |
| `source scripts/activate-toolchain.sh && pnpm --filter @custometry/web lint && pnpm --filter @custometry/web test && pnpm --filter @custometry/web build` | pass | TypeScript pass; Vitest `67/67`; Vite production build pass with both W33 lazy route chunks. Existing main compatibility bundle warning was `592.62 kB`; no performance claim is made. |
| Initial Playwright attempt on port 8000 | fail (environmental) | Port was already occupied by a parallel local runtime; no product assertion executed and no foreign process was stopped. |
| `source scripts/activate-toolchain.sh && pnpm --filter @custometry/web exec playwright test --config ../../tests/e2e/web-connections/playwright.config.ts` | pass | Final rerun `8/8`; only `web-768` (`768x1024`) and `web-1920` (`1920x1080`) ran against Vite `41733` and the disposable W14 fixture `8033`. |
| Real W14 adapter/API/PostgreSQL browser flow | pass | Production create/test/discover, persistence, authorization, one audit event, read-only enforcement, two catalog objects, response redaction, and safe draft reload observed. |
| Presentation-fixture browser flow | pass | Search, status/owner filtering, loading/empty/ready/refreshing/degraded/stale/forbidden/failed, EN/RU, and fail-closed recovery states observed without claiming W14 persistence. |
| Keyboard/accessibility/responsive visual review | pass at W33 boundary | Logical focus and error-summary focus, native labels, no positive tabindex, 200-percent reflow equivalent, reduced motion, and no W33 horizontal overflow/clipping passed. Inherited W31 collapsed-nav label clipping remains outside scope. |
| `uv run python -m tools.custometry_quality.validate_route_registry` | pass | `117` routes, `20` profiles, `22` cross-surface capabilities. |
| `uv run python -m tools.custometry_quality.check_i18n_parity` | pass | `200` English and `200` Russian shared-catalog keys; feature-local RU/EN copy is parity-tested because shared localization paths were forbidden. |
| `uv run python -m tools.custometry_quality.check_ddd_boundaries` | pass | `22` contexts; W33 introduced no cross-context backend dependency. |
| `uv run python -m tools.custometry_quality.check_contract_drift` | pass | Three registered generated-contract sources remained synchronized. |
| `uv run python -m tools.custometry_quality.validate_delivery_tickets` | pass | `38` delivery tickets validated before terminal update; rerun after acceptance is recorded below by the terminal verdict. |
| `uv run python -m tools.custometry_quality.validate_delivery_contract --contract /Users/daniildegtyarev/.codex/skills/delivery-orchestrator/references/delivery-contract-v1.md` | pass | Global contract and Custometry adapter validated. |
| `source scripts/activate-toolchain.sh && uv run python -m tools.check --scope local` | pass | Grouped local repository profile passed with pinned toolchain. |
| `git diff --check` | pass | No whitespace errors in the final scoped change. |

### Browser evidence paths

- `tests/e2e/web-connections/test-results/web-connections-real-W14-a-65106-ts-and-discovers-PostgreSQL-web-768/real-w14-save-test-redacted.png`;
- `tests/e2e/web-connections/test-results/web-connections-real-W14-a-65106-ts-and-discovers-PostgreSQL-web-1920/real-w14-save-test-redacted.png`;
- `tests/e2e/web-connections/test-results/web-connections-presentati-69ac4-s-and-EN-to-RU-localization-web-768/ru-presentation-state-matrix.png`;
- `tests/e2e/web-connections/test-results/web-connections-presentati-69ac4-s-and-EN-to-RU-localization-web-1920/ru-presentation-state-matrix.png`;
- `tests/e2e/web-connections/test-results/web-connections-permission-6a796--protected-data-fail-closed-web-768/permission-denied.png`;
- `tests/e2e/web-connections/test-results/web-connections-permission-6a796--protected-data-fail-closed-web-1920/permission-denied.png`;
- `tests/e2e/web-connections/test-results/web-connections-keyboard-s-9be14-educed-motion-remain-usable-web-768/keyboard-reflow-reduced-motion.png`;
- `tests/e2e/web-connections/test-results/web-connections-keyboard-s-9be14-educed-motion-remain-usable-web-1920/keyboard-reflow-reduced-motion.png`.

The capture directory is ticket-local ignored runtime output and is not staged
as product source. Captures contain only deterministic fixture labels and
redacted/bounded results.

## Real versus fixture proof boundary

The strongest local boundary is real for the operations W14 actually owns:
browser request -> production W33 adapter -> production W14 FastAPI router ->
production application service -> production PostgreSQL repository and
PostgreSQL connector -> disposable migrated control/source databases. The
fixture supplies only local identity actors, runtime-generated disposable
database credentials, container lifecycle, and a bounded persistence/audit
probe. It does not replace the production W14 create, authorization,
persistence, redaction, test, or discovery code.

W14 does not expose a list query or persisted draft lifecycle. W33 therefore
does not infer either capability. Production listing fails explicitly and
safely with `CONNECTION_LIST_UNAVAILABLE`; draft persistence is limited to
non-secret fields in the current browser tab, with the credential reference
excluded. Search/filter data, state matrices, future connector choice, and
provider-test presentation are explicit DEV-only fixtures. No external
provider connectivity is claimed.

## Contract impact

| Boundary | Classification | Disposition |
|---|---|---|
| Public API, persisted schema, migrations, provider contracts | `none` | W33 consumes W14 `1.0.0` create/test/discover and identity boundaries without modifying them. |
| Internal browser port and DTOs | `compatible-change` | Additive typed `ConnectionCatalogPort` and W14 adapter inside the W33 feature; no shared consumer default changes. |
| Browser-visible route behavior | `compatible-change` | Canonical `UI-DATA-001` and `UI-DATA-002` routes gain production implementations while stable route IDs/URLs and W31 lazy discovery remain unchanged. |
| Request, auth, timeout, retry, and error semantics | `compatible-change` | Same-origin credentials, W14 contract/request headers, stable non-sensitive error codes, fail-closed permissions, and no blind retry after an ambiguous create. |
| Draft/browser storage behavior | `compatible-change` | Workspace-scoped current-tab draft contains connector, display name, profile reference, and template version only; credential reference is deliberately omitted. |
| Identity, cache keys, request hashes, domain persistence identity | `none` | W33 introduces no backend identity, cache, hash, or persistence rule. |
| Side effects and idempotency | `compatible-change` | Explicit user action creates one W14 connection and then runs read-only test/discovery; W33 does not silently resubmit failed creates. |
| Logs, metrics, audit, redaction, alerts, runbooks | `compatible-change` | Backend audit behavior is unchanged; browser redaction guard and safe copy add defense without operator-contract mutation. |
| Measured performance | `unknown` | No benchmark was run; the existing main bundle size warning remains a residual risk. |

## Residual risks

- W14 cannot prove a production searchable list or persisted draft until a
  later accepted backend/query boundary exists; production W33 reports that
  capability gap explicitly.
- External PostgreSQL/provider networks, production secret resolution, recovery,
  screen readers, measured runtime/bundle performance, release, and deployment
  remain unproved.
- The accepted W31 shell's collapsed `More sections` label clips visibly at the
  narrow/zoomed browser observations. W33-owned content does not overflow, and
  W31 shell/shared paths were intentionally not changed.

## Verdict

`passed`. Browser QA verdict is `ready with inherited-shell caveat` for the
declared W33 production-route, real W14 adapter, explicit unavailable/list and
local-draft boundaries, responsive-Web, localization, and accessibility-smoke
scope. The next safe action is a separate ready ticket that does not rely on an
unproved production list or secret-provider capability.
