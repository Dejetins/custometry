---
doc_id: ARCH-DEVELOPMENT-AUDIT-20260904
title: Custometry development audit, 2026-09-04
doc_version: 2
product_spec_version: 0.10.0-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: [AC-018, AC-023, AC-025, AC-031, AC-034, ANALYTICAL-DOC-001, PRODUCT-ANALYTICS-006, WEB-PERF-005]
status: active
audited_commit: 94672bf97a402d9c90e96ac8b783b6a0e30adba0
proof_boundary:
  label: source-evidence-and-development-plan-audit
  exclusions: [full-product-runtime, exhaustive-security-audit, performance-measurement, release-acceptance]
---

# Custometry development audit, 2026-09-04

> Current-use note (2026-09-06): observations, counts and checks below remain
> evidence for audited commit `94672bf97a402d9c90e96ac8b783b6a0e30adba0`.
> They are not rerun by the documentation correction. Later accepted requirements
> and current owner constraints govern new work: Forecasting remains on hold,
> the first external release is unselected, and retired UI-program gates do not
> restart. In particular, F08 does not authorize a new forecasting ticket.
> The accepted target concept, ADR-0007 and current Web source contract retain
> their published authority; this historical audit does not amend them.

## Verdict

**Not ready as a complete executable development plan; ready to prepare the next bounded integration tickets.** The product already has a substantial specification, accepted target architecture, useful backend kernels, and five production feature routes. It does not yet have a demonstrated complete vertical alpha or an executable path covering the whole product.

The main planning problem is the gap between accepted component slices and their composition into user journeys. Rebuilding those components would waste work; declaring the product ready from their individual evidence would overstate progress.

The [proposed development roadmap](development-roadmap-v1.md) adds outcomes, dependencies, decisions and proof obligations to blueprint sections 26–28. The [coverage snapshot](development-coverage-2026-09-04.json) accounts for every indexed product ID, route, overlay, system surface and cross-surface capability. Neither artifact changes ticket status, product requirements, or release authority.

The owner states that development is voluntary, has no external deadline or delivery obligation, has a potential employer customer, and has not selected the first release scenario. The recommended first internal result therefore follows the existing technical slice, without a customer-specific fork or an invented commitment.

## Audit boundary and source identity

The user linked current GitHub `main`. Two independent `git ls-remote` probes resolved it to `94672bf97a402d9c90e96ac8b783b6a0e30adba0`. A temporary archive of that exact commit was used for current-state reading and fresh source checks.

The shared local checkout was at `80cd0976c434b6db62d3e415bc638cbe4a9468c2` and initially reported 240 changed/untracked entries. It contains older UI-program work and is not an authoritative representation of current GitHub `main`. No checkout, reset, stash, branch, worktree, publication, deployment or existing product-source edit was performed by this audit.

Source priority for this assessment:

1. Owner request and clarification.
2. The [machine blueprint][blueprint] and its [human mirror][human].
3. The [UI requirements][ui] and executable route/surface registries.
4. The [accepted target pilot][pilot], [current Web source contract][web-contract], and ADR-0007.
5. Accepted architecture, code, migrations, tests and ticket evidence at the pinned commit.

The pilot now owns its demonstrated composition and behavior, as well as visual language. Old local rules limiting it to visual inspiration are superseded on current `main`. The retired G0–G6 program is not a dependency of further development.

This is a project/architecture/plan audit. Identifier coverage is exhaustive for the supplied indexes; semantic and code inspection is concentrated on high-impact boundaries across all main capability groups. It is not an exhaustive review of every code path, full UI critique, penetration test, runtime replay of every historical ticket, or confirmation that no requirements remain undiscovered.

## What already exists

| Area | Observed implementation and evidence | Practical limit |
|---|---|---|
| Requirements | Product `0.10.0-draft`, UI `0.8.0-draft`, machine/human parity, 29 use cases, 48 public-MVP and 54 v1 acceptance IDs, domain invariants and roadmap | IDs include risks, goals, decisions, historical resolutions and references; counting them is not a completeness or progress measure |
| Architecture | Modular monolith, context ownership, immutable artifacts, PostgreSQL truth, outbox/fencing, locale-neutral core, ADR-0007 frontend platform | Many target contexts and public contracts remain unimplemented |
| Identity and organization | W12/W13: local auth, sessions/tokens, workspace/role policy, organization hierarchy, ownership and effective-access kernels; migrations 0002/0003; recorded real PostgreSQL evidence | Auth-to-browser and policy-to-all-data-consumers composition is incomplete |
| Sources | W14: PostgreSQL discovery/preview/extraction session, governed CSV/XLSX validation, import-template publication, migration 0004 | Not all SQL connectors, generalized mapping, searchable connection list or complete file-to-dataset ingestion |
| Data foundation | W15: immutable Parquet, DQ report/waivers, semantic publication, watermark/outbox transaction, retry/fencing/crash evidence; migration 0005 | A fixed retail-source slice, not the full ingestion product or integrated production worker runtime |
| Analytics | W16: governed sales/customer/RFM calculation in `analytics_core`, immutable result metadata/artifacts, API, golden checks; migration 0006 | `analytics_sales` and `analytics_customer` are placeholders; their current functionality is in `analytics_core`. No forecast, full metric registry, general chart/data projection or reporting kernel |
| People | W17: privacy-safe contributor projection and API, migration 0007 | Not the complete organization/people UI or collaboration/adoption product |
| Execution and inbox | W36/W38/W37: operator API, durable transitions, retry/cancel, Valkey adapter, terminal event/public port, permission-filtered inbox; migrations 0008/0009; recorded disposable integration evidence | Actual data computation and independently tested workers/events are not yet composed into a shipped topology |
| Web | W31 shell; W32 sales; W33 connection list/editor boundary; W34 operator runs; W35 inbox | Five route IDs marked implemented; explicit unavailable states and test-only boundaries are part of those acceptances. Auth routes remain planned |
| UI concept | Preserved RU/EN interactive pilot with byte-pinned HTML/ECharts/license and decision notes | Not a production backend, permission model, persistent document service, or complete all-screen implementation |
| Engineering | Locked toolchain, validators, tests, migrations, Foundation Compose, CI and immutable candidate publication | Foundation CI and candidate images are not public-MVP/v1 or end-user-release proof |

All backend code locations were checked directly; a directory's existence was not treated as implementation. The main unimplemented/reserved areas include forecasting, report delivery, promotion journal, audit product surface, plugin SDK, full document composition, methodology/research, collaboration/adoption, digital measurement and product/inventory analytics. Existing modules may contain limited supporting behavior; this is not a claim that every adjacent primitive is absent.

### Execution and surface inventory

At the pinned revision:

- 38 ticket files: 33 `accepted`, 5 `superseded`, zero `ready`, `active`, `draft` or `blocked`.
- Runtime/data graph covers W11–W17; Web graph covers W31–W35. W36–W38 also exist and are accepted. Graph `initial_status` is historical topology metadata, not current status.
- 117 route-level product pages: 111 `planned`, 5 `implemented`, 1 `foundation`; 5 additional Foundation utility routes.
- 25 overlays, 5 system surfaces, 22 cross-surface capabilities.
- Implemented feature IDs: `UI-DATA-001`, `UI-DATA-002`, `UI-AN-003`, `UI-OPS-001`, `UI-NOTIFY-001`. `UI-HELP-001` is Foundation.
- 1,141 indexed IDs; 346 occur in some ticket's requirement list; 177 occur in the selected 15 runtime/backend/Web implementation tickets. 795 occur in no ticket list.
- None of `AC-001`–`AC-048` occurs directly in ticket requirement lists. This is a traceability gap, not proof that every criterion has zero supporting tests.
- 11 open PRs were observed, all Dependabot updates. No open feature PR supplied a missing next development frontier at audit time.

The 177 references are not 177 completed requirements. For example, W32 references discount/PVM obligations while explicitly presenting unavailable capabilities rather than implementing those calculations. Conversely, an unreferenced ID may have partial code or indirect evidence.

## Assessment matrix

| Plan concern | Assessment | Severity / consequence |
|---|---|---|
| Product vision, target boundaries, non-goals | OK | Preserve accepted decisions |
| Functional breadth and UI inventory | Partial | Broad but not a validated implementation decomposition |
| Current-state and proof visibility | Risk | High: old checkout and component acceptance obscure product gaps |
| Dependency order and ready frontier | Gap | High: no remaining executable ticket |
| Auth, tenancy, data-policy composition | Risk | High: user journey and data isolation need integration proof |
| Common execution and durable result lifecycle | Risk | High: two kernel paths plus missing runtime composition |
| Mapping/extraction completeness | Risk | High: fixed source shape and bounded extraction can misrepresent complete data |
| Shared document, filter and chart contracts | Gap | High: late implementation would force repeated frontend and persistence changes |
| Forecast and complete alpha scope | Gap | High: alpha cannot close without its required forecast |
| NFRs, budgets, representative workload | Partial | High before release; measurement and policy ownership must be planned |
| Migration, rollout and rollback | Partial | Existing slice migrations are evidenced; cross-slice cutover is unplanned |
| Complete acceptance traceability | Gap | High: ticket acceptance does not close release acceptance |
| UI concept authority | OK on current main | Current production conformance is subsequent work |
| Release/first-customer scenario | Unknown | Owner decision; no deadline or first-release promise inferred |

## Findings and minimum corrections

### F01 — Current local base is stale relative to project authority

**Fact:** Current main contains W15–W17, W31–W38 and the target-pilot retirement decision; the shared local HEAD predates them and contains extensive foreign work.

**Inference:** Continuing from the current local tree could repeat completed work, revive retired UI governance or apply incompatible source assumptions.

**Boundary:** Repository source and execution authority. **Severity:** High before implementation.

**Minimum correction / proof:** Select the pinned or later verified main revision for the next ticket and preserve foreign changes through the repository's normal isolation procedure. Revalidate the ticket and source contract there. This audit does not perform Git recovery or merge local UI work.

### F02 — Existing plans stop at accepted slices

**Fact:** Blueprint section 26 has eight broad phases, while both current ticket graphs terminate in accepted nodes; all current tickets are accepted or superseded.

**Inference:** There is a strategic roadmap, but not a complete executable plan for the remaining product. A new task cannot safely infer its scope from a completed graph.

**Boundary:** Delivery topology. **Severity:** High.

**Minimum correction / proof:** Use the accompanying outcome roadmap; prepare only the immediate integration tickets with dependencies, owned paths, requirement IDs and real-boundary acceptance. Future outcomes stay planning entries until their contracts and prerequisites are known. No parallel status ledger is needed.

### F03 — Browser session and workspace context are not composed

**Fact:** Identity reads the `custometry_access` cookie and protects cookie mutations with CSRF. The sales client uses `credentials: "same-origin"` without an Authorization header; the analytics router accepts only bearer authorization. The shell defaults to `northwind-retail`. W35 explicitly excludes production session-to-bearer delivery and workspace UUID-to-key resolution.

**Fresh probe:** A synthetic cookie-only request to the production analytics router returns `401 AUTHENTICATION_FAILED` before its Identity port is called. No real token or database was used.

**Inference:** A valid browser-session transport is insufficient for this protected analytics path. Individual browser fixtures do not prove a normal user login-to-feature journey.

**Source:** [Identity auth dependency][identity-router], [sales client][sales-client], [analytics router][analytics-router], [W35 evidence][w35].

**Boundary:** Auth, cookie/CSRF, workspace identity, frontend adapters. **Severity:** High.

**Minimum correction / proof:** Identity-owned reusable browser auth dependency, cookie/CSRF handling across protected providers while retaining API-token support, authorized workspace-key resolution, login/refresh/revoke/switch integration. Prove two workspaces and no fixture-injected bearer in the complete browser path.

### F04 — Organization policy exists but analytics does not consume it

**Fact:** `AnalyticsService.run` checks `analysis.run`; its policy hash contains workspace, principal and permission strings. Semantic lookup is workspace/version-scoped. The inspected run path does not call the W13 effective-access service or apply its row/column/department policies. Result reads filter by owner and workspace.

**Inference:** Functional permission and owner filtering cannot establish the full department/object/data ceilings required by AC-018 and RBAC. Policy changes with unchanged role strings are not represented in this result identity.

**Source:** [analytics application][analytics-service] and [repository projection][analytics-repository], compared with the [context map][contexts].

**Boundary:** Protected data fetch, policy-aware result/cache identity and revoke behavior. **Severity:** High; blocker to using department-restricted real data.

**Minimum correction / proof:** Consume an Identity-owned public effective-policy decision before source access and again before protected publication/read/export; include the authoritative policy version/scope in identities. Test same-workspace denied rows/columns, grant/revoke with unchanged roles, cache reuse, hidden counts and worker reauthorization. This audit does not claim an observed production data leak.

### F05 — File validation and fixed extraction do not yet form generalized ingestion

**Fact:** W14 file API exposes template create/publish/validate and returns validation metadata. W15 reads fixed `RETAIL_OBJECTS` under schema `retail`; every object is extracted with `limit=100_000`. The PostgreSQL adapter issues `SELECT ... LIMIT %s` and returns those rows. The inspected runner has no paging/exhaustion check and derives a watermark from the extracted receipts.

**Inference:** Sources larger than the limit can be accepted as incomplete snapshots, and the data path cannot yet ingest a user-mapped CSV/XLSX dataset. Deterministically sorting returned rows does not establish source completeness.

**Source:** [file API][imports-router], [runner][data-runner], [PostgreSQL adapter][pg-connector].

**Boundary:** Source completeness, mapping, artifacts, DQ and watermarks. **Severity:** High; release blocker for arbitrary source datasets.

**Minimum correction / proof:** Persist governed mapping and source/import identity, join validated files into the same normalized ingestion path, implement paged/streamed extraction or explicit fail-closed overflow, and handle empty sources. Test 0/1/100,000/100,001 rows, multi-batch consistency, deleted/late rows, overflow, failure/retry and no watermark advance on incomplete reads.

### F06 — Execution kernels and runtime composition remain separate

**Fact:** W15 uses `PostgresExecutionRepository` and `data_pipeline_outbox`; W36 uses `PostgresExecutionControlStore` and `execution_runs/execution_outbox`. Analytics POST computes synchronously. Compose defines control DB, optional demo source, migration, API, Web and Edge; it does not compose Valkey, scheduler, dispatcher, reconciler and domain workers. Some corresponding app directories contain only `.gitkeep`.

**Inference:** Operator commands/events can work in their disposable harness without controlling the real ingestion/analytics computation. An accepted cancel API is not proof that a running analytical job stops safely.

**Source:** [runner][data-runner], [execution store][execution-store], [Compose][compose], [analytics router][analytics-router].

**Boundary:** AC-023/025/031/034, job state, idempotency, queue delivery, cancellation and cleanup. **Severity:** High.

**Minimum correction / proof:** Bind domain jobs to the canonical Execution lifecycle via owner ports; migrate additively and preserve old attempts/artifacts. Compose the delivery loops and workers. Prove real input → command → worker → artifact → result → terminal event/inbox, including lost worker, duplicate delivery, cancellation, restart and stale fencing.

### F07 — Common document and chart foundations are still missing

**Fact:** The blueprint defines stable chapters/pages/sections/blocks, scope inheritance, personal views, atomic root/page snapshots and common Web/email/XLSX reuse. The pilot demonstrates much of that behavior. `packages/presentation` currently contains People support, while the chart compiler exports `chartCompilerLifecycle = "planned"` and no compile function.

**Inference:** Implementing reports, research, dashboards, Focus and exports separately now would create incompatible persisted blocks, filters and snapshot identities.

**Source:** [composition requirements][composition], [compiler placeholder][compiler], [pilot][pilot].

**Boundary:** Document persistence, filter identity, chart-data contracts, export and UI state. **Severity:** High.

**Minimum correction / proof:** Establish the minimal common document/result/chart contract and one persisted end-to-end page before feature expansion. Reuse domain result projections; do not copy demo calculations or localStorage as backend behavior. Grow the 100×30 envelope through measured tests without building every editor first.

### F08 — A complete vertical alpha still lacks forecasting

**Fact:** `packages/forecasting` is reserved; current API result types are sales/customer/RFM. Blueprint 26.1/31 requires monthly net revenue, Seasonal Naive, CatBoost and rolling backtest. Neither existing graph owns that remaining outcome.

**Inference:** Sales or an operational foundation may be a useful internal preview, but it cannot be labelled the specified vertical alpha.

**Boundary:** Release naming, temporal correctness, feature lineage and model lifecycle. **Severity:** High for alpha acceptance.

**Minimum correction / proof:** Add a forecast slice after the shared execution/metric contracts, resolve OPEN-008, and prove leakage-free temporal folds, deterministic baseline comparison and reproducible artifacts. Keep any earlier internal preview explicitly distinct from vertical alpha.

### F09 — Release allocation needs a reconciliation pass

**Fact:** Product analytics 12.17 and PRODUCT-ANALYTICS-006 require basic ABC/XYZ/Pareto in v1; section 26.5 defers “ABC/XYZ extensions” without describing the extension boundary. Phase 3 mentions Promotion Journal although its routes and v1 release list assign it to v1. Expanded product/inventory/document obligations are more detailed than the broad phase lists. OPEN-007 and OPEN-008 remain open.

**Inference:** Different executors can legitimately derive different first-release and phase scopes from these sources. Absence of more OPEN entries is not proof that all implementation decisions are settled.

**Boundary:** Product scope and acceptance allocation. **Severity:** Medium, High if used to remove a required capability.

**Minimum correction / proof:** Preserve basic ABC/XYZ/Pareto and all accepted product/inventory obligations in v1; enumerate only the deferred extensions. Separate early schema support from completed Promotion Journal delivery. Bind every acceptance criterion to an outcome and record open policy/measurement decisions before affected implementation. Any real reduction of accepted scope needs owner approval.

### F10 — Nonfunctional requirements are broad but not fully operationalized

**Fact:** Security, accessibility, resource limits, performance measurement, backup and recovery are extensively specified. OPS-006 intentionally defers SLO thresholds until measurement. WEB-PERF-005 still refers to an accepted “program baseline” after retirement; the retirement record assigns performance to ticket acceptance. Historical architecture-spike thresholds exist but are not current-product benchmarks. Product recovery/performance evidence files expected by release gates are absent.

**Inference:** It would be wrong both to say “there are no NFRs” and to claim those NFRs are now measurable acceptance gates for the final product.

**Boundary:** Workload envelope, latency/CPU/RAM/disk, recovery, privacy/retention and accessibility. **Severity:** High before release.

**Minimum correction / proof:** Declare representative dataset/document/concurrency profiles, measure the first real journey, accept budgets in ordinary ticket-owned evidence, and define restore loss/time targets, backup/key scope, privacy/retention policy values and alert owners before those boundaries ship. Do not silently inherit old spike thresholds or invent unmeasured performance guarantees.

### F11 — Green CI currently proves Foundation, not integrated product acceptance

**Fact:** Exact-main GitHub Foundation checks passed. The runtime browser configuration selects `foundation.spec.ts`, while feature suites have separate configurations. W32–W35 retain explicit fixture/unavailable boundaries. No current ticket directly maps the 48 AC IDs. Release gate defaults require separate performance/recovery and supply-chain evidence.

**Inference:** Passing CI and 33 accepted tickets do not establish the first real-user workflow or public-MVP acceptance.

**Source:** [CI workflow][ci], [browser configuration][browser-config], [W32][w32] and [W35][w35].

**Boundary:** Integration regression and release claims. **Severity:** High.

**Minimum correction / proof:** Make the real authenticated vertical journey an explicit CI obligation as it becomes runnable; map AC IDs to implementation and release evidence. Retain fixture tests for presentation states with their narrower claims. Source tests and build success remain separate from browser/runtime proof.

### F12 — Operational and extension scope needs named future outcomes

**Fact:** Current target architecture covers all required SQL connectors, schedules, CPU/progress, retention/orphans, restore/key recovery, audit, methodology/research, collaboration/adoption, full forecast, digital measurement, products/inventory, reporting, notification channels and SDK. Existing graphs cover only a small subset. The current Compose/runbooks are Foundation/development oriented.

**Inference:** These obligations can fall between backend, UI and infrastructure streams unless a single outcome decomposition owns them. Leaving them until a final “hardening” stage would force schema, policy and lifecycle rework.

**Boundary:** Cross-context delivery and operations. **Severity:** High.

**Minimum correction / proof:** Assign each capability family to the roadmap outcomes; design identity/policy/lifecycle seams early, implement optional consumers later, and qualify operations incrementally. Keep universal XLSX as the last new v1 functional slice, as already specified.

## Fresh checks and inherited evidence

| Check | Observation | What it establishes |
|---|---|---|
| Exact-main `uv sync --locked --all-packages --all-groups` | Passed in temporary snapshot | Reproducible Python dependency installation |
| Exact-main `uv run --locked --package custometry-api pytest -q tests/unit tests/contract -rs` | **82 passed** | Existing domain/property/contract suite |
| Exact-main `corepack pnpm install --frozen-lockfile --ignore-scripts` | Passed | Locked frontend dependencies; package lifecycle scripts intentionally not executed |
| Exact-main `corepack pnpm --filter @custometry/web test` | **74 passed**, 15 files | Web component/client tests, including prototype tests |
| Exact-main `corepack pnpm --filter @custometry/web build` | Passed; main chunk 593.01 kB uncompressed | TypeScript/build success; size warning is not a measured performance failure |
| Cookie transport probe | 401 before Identity lookup | Reproduced missing cookie auth composition in analytics router |
| Individual snapshot source validators | 14 static validators passed; layout could not observe Git metadata | Blueprint/index/docs/contracts/routes/tickets/DDD/migration-source consistency |
| Snapshot doctor after exact toolchain activation | Passed | Static environment/toolchain preconditions |
| Grouped snapshot `tools.check --scope local` | Environmental failure: archive has no `.git` | Full grouped result is not claimed green |
| Shared local checkout `tools.check --scope local`, before and after audit writes | Passed | Audit-document handoff on the older dirty checkout; not current-main product proof |
| Frozen coverage validation | Passed: 1,141 unique IDs, 169 unique surfaces, 102 acceptance allocations, complete track references | Inventory/allocation integrity, not implementation completion |
| Pinned source validation | Passed: source hashes, pilot HTML/runtime/license hashes, source-link files and line bounds | References resolve to the exact audited input |
| [Exact-main Foundation CI][ci-run] | All observed checks succeeded | Existing hosted Foundation profile |
| W11–W17/W31–W38 evidence | Read, compared with current source; not wholly rerun | Historical scoped integration/browser observations |

An initial unactivated individual doctor invocation saw Node 24.19.0 rather than the required 24.18.0; rerunning with `source scripts/activate-toolchain.sh` passed. This was environmental, not a product defect.

No new database/container/browser, performance, restore, vulnerability or release drill was run. The HTTP probe used a synthetic placeholder cookie and did not touch a database. The report does not claim those unobserved boundaries.

## Required documentation continuity

The next contract/scope reconciliation should update the directly affected blueprint sections and human mirror together, then UI release/source references, affected architecture and ready tickets. Preserve original accepted ticket evidence and attach new integration evidence to successor work; do not rewrite old acceptances to imply stronger proof.

The accompanying roadmap is **proposed architectural sequencing**, explicitly requested by the owner. Current ticket frontmatter remains the only execution-state authority. Its first safe action is a contract/release-allocation ticket, followed by the session/workspace/policy integration slice. Real data admission depends on closing F04/F05, not simply on adopting the roadmap.

## Deliverables and residual uncertainty

Created by this assignment: this audit, the proposed roadmap, and the frozen coverage JSON. `docs/README.md` was regenerated with exactly two owned index additions; its pre-existing ADR-0004 rename was preserved. No product code, normative product text or ticket statuses are changed. The grouped local handoff gate and whitespace check passed after the documentation additions.

Remaining uncertainty: first external release scenario, actual available engineering capacity, representative permitted customer-data shape/volume, final policy thresholds, target production configuration and runtime behavior of the fully composed product. None prevents planning or bounded internal engineering; each is due before the outcome that relies on it.

[blueprint]: https://github.com/Dejetins/custometry/blob/94672bf97a402d9c90e96ac8b783b6a0e30adba0/custometry-technical-blueprint-ru.md
[human]: https://github.com/Dejetins/custometry/blob/94672bf97a402d9c90e96ac8b783b6a0e30adba0/custometry-technical-blueprint-human-ru.md
[ui]: https://github.com/Dejetins/custometry/blob/94672bf97a402d9c90e96ac8b783b6a0e30adba0/custometry-ui-blueprint-ru.md
[pilot]: https://github.com/Dejetins/custometry/blob/94672bf97a402d9c90e96ac8b783b6a0e30adba0/docs/architecture/ui/target-pilot/README.md
[web-contract]: https://github.com/Dejetins/custometry/blob/94672bf97a402d9c90e96ac8b783b6a0e30adba0/docs/architecture/ui/custometry-web-implementation-source-contract-v1.md
[contexts]: https://github.com/Dejetins/custometry/blob/94672bf97a402d9c90e96ac8b783b6a0e30adba0/docs/architecture/bounded-context-map.md
[identity-router]: https://github.com/Dejetins/custometry/blob/94672bf97a402d9c90e96ac8b783b6a0e30adba0/apps/api/src/custometry_api/identity/router.py#L311
[sales-client]: https://github.com/Dejetins/custometry/blob/94672bf97a402d9c90e96ac8b783b6a0e30adba0/apps/web/src/features/analytics-sales/analytics-sales-api.ts
[analytics-router]: https://github.com/Dejetins/custometry/blob/94672bf97a402d9c90e96ac8b783b6a0e30adba0/apps/api/src/custometry_api/analytics/router.py
[analytics-service]: https://github.com/Dejetins/custometry/blob/94672bf97a402d9c90e96ac8b783b6a0e30adba0/packages/analytics_core/application/service.py#L354
[analytics-repository]: https://github.com/Dejetins/custometry/blob/94672bf97a402d9c90e96ac8b783b6a0e30adba0/packages/analytics_core/infrastructure/postgres.py
[imports-router]: https://github.com/Dejetins/custometry/blob/94672bf97a402d9c90e96ac8b783b6a0e30adba0/apps/api/src/custometry_api/imports/router.py
[data-runner]: https://github.com/Dejetins/custometry/blob/94672bf97a402d9c90e96ac8b783b6a0e30adba0/apps/worker_data/vertical_slice.py
[pg-connector]: https://github.com/Dejetins/custometry/blob/94672bf97a402d9c90e96ac8b783b6a0e30adba0/plugins/connector_postgresql/adapter.py#L110
[execution-store]: https://github.com/Dejetins/custometry/blob/94672bf97a402d9c90e96ac8b783b6a0e30adba0/packages/execution/infrastructure/control_postgres.py
[compose]: https://github.com/Dejetins/custometry/blob/94672bf97a402d9c90e96ac8b783b6a0e30adba0/compose.yaml
[composition]: https://github.com/Dejetins/custometry/blob/94672bf97a402d9c90e96ac8b783b6a0e30adba0/custometry-technical-blueprint-ru.md#L4219
[compiler]: https://github.com/Dejetins/custometry/blob/94672bf97a402d9c90e96ac8b783b6a0e30adba0/packages/chart_compiler_ts/src/index.ts
[w32]: https://github.com/Dejetins/custometry/blob/94672bf97a402d9c90e96ac8b783b6a0e30adba0/.codex/delivery/evidence/W32-WEB-SALES-OVERVIEW.md
[w35]: https://github.com/Dejetins/custometry/blob/94672bf97a402d9c90e96ac8b783b6a0e30adba0/.codex/delivery/evidence/W35-WEB-NOTIFICATION-INBOX.md
[ci]: https://github.com/Dejetins/custometry/blob/94672bf97a402d9c90e96ac8b783b6a0e30adba0/.github/workflows/ci.yml
[browser-config]: https://github.com/Dejetins/custometry/blob/94672bf97a402d9c90e96ac8b783b6a0e30adba0/tests/e2e/playwright.config.ts
[ci-run]: https://github.com/Dejetins/custometry/actions/runs/33915506361
