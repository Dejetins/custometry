---
doc_id: ARCH-DEVELOPMENT-ROADMAP-001
title: Custometry development roadmap and integration decisions
doc_version: 10
product_spec_version: 0.10.0-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: [ARCH-PRINCIPLE-001, AC-018, AC-023, AC-025, AC-031, ANALYTICAL-DOC-001, ANALYTICAL-DOC-011, PRODUCT-ANALYTICS-006, V1-AC-011]
status: proposed
source_audit: development-audit-2026-09-04.md
source_commit: 94672bf97a402d9c90e96ac8b783b6a0e30adba0
owner_priority_update: 2026-09-05
proof_boundary:
  label: proposed-architecture-sequencing-and-acceptance-allocation
  exclusions: [ticket-execution-authority, owner-release-acceptance, implementation-completion, deployment-authority]
---

# Custometry development roadmap and integration decisions

## Purpose and authority

This owner-requested roadmap turns the existing blueprint's release stages into a dependency-aware continuation plan. It addresses the [audit findings](development-audit-2026-09-04.md), preserves implemented kernels, and identifies decisions that would otherwise cause structural rework.

**Status: proposed.** The normative blueprint remains authoritative. This document does not accept a new release promise, remove requirements, activate a ticket, create an execution ledger, or replace current ticket frontmatter. It is an architectural sequencing document, not a second status register. Use the accepted hierarchical planning framework to detail selected branches with the owner; do not encode the whole roadmap into prompts.

The owner has no external delivery deadline or contractual obligation and has not selected the first external release scenario. Calendar estimates would therefore be invented. Progress is measured by completed user outcomes and their actual proof. The first internal result below is an engineering recommendation consistent with blueprint section 31; it is not a customer-specific product limitation.

### Planning process adoption — 2026-09-06

The owner adopted the [hierarchical planning framework](framework-v1/README.md).
This roadmap remains a proposed sequence and requirement allocation, not a selected
implementation plan. Its historical ticket-first wording is qualified by the new
route: owner-agreed direction/workstream/milestone decomposition, then one pack and
canonical journal for each authorized milestone. Existing tickets retain evidence
and independent status; do not duplicate their state or revive retired UI programs.
Agents must maintain affected document links, versions, decisions, indexes and
evidence without owner reminders. Product priorities and Forecasting hold remain
unchanged. The owner has now accepted [MAP-001 and its six L1 directions](project-map.md)
at version 1.0.0, followed by the accepted sequential priorities and WS-001 registration at MAP-001 `1.2.0`.
The accepted [WS-001: installable platform and first administrator bootstrap](directions/DIR-006/workstreams/WS-001.md) `1.0.0` belongs to DIR-006, with DIR-001/005 contributions. It fixes M5 Max/36 GB and Linux VM tests, explicit LAN/HTTPS, a guided installer, initial-account roles and no experimental-data migration. The next document is the separate C02 L3 plan for reproducible prebuilt delivery; its MS ID/path/version is produced during that authoring unit. Inventory remains part of L2 preparation; five sequential milestone outcomes are accepted.
The sequence starts with prebuilt delivery, installation and protected bootstrap,
then staff/access, sources, usable data, analysis, authoring, publication/access,
reader use and the next update/recovery cycle. The older report-first recommendation
and N0/N1/M0/M1 rows below are supporting analysis only; where their ordering differs,
[MAP-001](project-map.md#accepted-delivery-sequence) governs the selected planning frontier.

### Owner priority update — 2026-09-05

Forecasting is **on hold** at the owner's explicit request: readiness to implement it is not established. Do not start forecast-specific research, model implementation, backtests, registry expansion or forecast UI tickets until the owner resumes this direction. D09, M3, N7 and the forecast portions of M5/M7 are deferred. Shared semantic, policy, execution and document contracts continue for their current analytical consumers; do not build speculative forecasting infrastructure under those tickets.

The active product focus is **report authoring and reusable segments**, with a preference for drag-and-drop where it helps. The interaction proposal below is a recommendation, not an accepted production design. Non-forecast development no longer depends on M3: M4 can follow M2, and report/rule-segment slices are brought into the internal preview frontier. The frozen audit and coverage snapshot retain their original source-date meaning.

This is an execution-priority change, not deletion of forecast requirements. The existing vertical-alpha/public-MVP/v1 labels still include their specified forecasting obligations. They cannot be declared complete during the hold unless the owner separately revises release criteria in the normative blueprint and its mirror. An internal report-and-segment preview does not require that release-policy decision.

**Later owner correction on the same date:** the three-condition segment example and card-oriented report sketch were too narrow. The owner requested investigation of Mindbox, an existing compact HTML report and adjacent products, without more prototypes. The [capability discovery report](product-capability-discovery-2026-09-05.md) records a newer requirement snapshot at remote main `d5ecbd33c1fd582058ec3514e2084820c8a3f1c2`, existing obligations and candidate gaps. It supersedes the narrow interaction framing below where applicable. No first external release scenario or reduced final product scope has been accepted.

The adopted authoring contract now fixes product semantics for relational/temporal segments, population identity/time, matrices, parameters/comparisons and compact modes. Before N5/N5S become ready, N0 must bind those semantics to actual versioned provider/consumer schemas, migrations and bounded proof. Supported subsets may still ship incrementally; the underlying contracts must not equate the complete segmentation product with predicates on a flat customer-feature row. Existing `FILTER-011/012`, compact/table-first UI requirements and dense-table controls are retained rather than rediscovered as new requirements.

### Owner adoption — 2026-09-05

The owner approved incorporating the core researched ideas into all relevant
project documentation. They are now normative in the machine blueprint and
human mirror, with UI flows, architecture ownership and exact adoption links in
the [authoring contract](../../contracts/analytical-authoring-contract.md).
This closes the feature-adoption portion of N0; it does not declare API schemas,
migrations, provider integrations or N5/N5S ready. Their implementing tickets
must select supported subsets and prove the version transitions.

The delta allocates 35 feature requirements, 11 test invariants and eight v1
acceptance criteria to the target. V1-AC-055 through V1-AC-062 cover related
rules/sequences, curated/composed populations, membership time, compact matrix
authoring, parameters, comparison, evidence selection and semantic diff. Manual
targets, additional membership entities and new PDF/standalone HTML formats
remain separate optional expansions. Existing report channels are retained.

### Owner source-data requirements — 2026-09-05

The [source data adaptation contract](../../contracts/source-data-adaptation-contract.md)
adopts the owner's first-source constraints in the normative machine/human/UI
blueprints. This is accepted requirement scope, not source/provider proof or
ticket execution authority. N0 now binds readiness/coverage, full-snapshot diff,
absence policy, uncertain rekey, DQ remediation and typed derived dimensions to
actual versioned schemas. N3 proves them on the daily-rebuild fixture corpus;
N4 proves trigger/replay/checkpoint/recovery behavior through canonical execution.

The first source has no reliable row updated_at: a recent-sales lookback alone
cannot pass its acceptance. Pull via configurable control-table readiness,
schedule/manual initiation and source push/notification remain target modes;
concrete readiness guarantees, tolerance thresholds and workload limits are
source/workspace inputs, not invented defaults. SP/is_lk child channels and
string booleans are shared mappings, not report-specific formulas. Requirements
V1-AC-063 through V1-AC-067 define the acceptance boundary. Forecasting remains
on hold and existing release labels are not redefined.

## Recommended first outcome

First, an installation administrator obtains a versioned prebuilt delivery, installs
it on the supported target, completes protected bootstrap and retains the state
after restart. Workspace administration then prepares separate staff accounts and
access. These prerequisites are now explicit in MAP-001 and the selected WS-001
draft; the remaining scenario below is not the first development block by itself.

A real user can bootstrap/sign in, select an authorized workspace, import governed Customer/Receipt files, understand mapping and quality issues, run sales/customer/RFM analytics, create a reusable rule-based customer segment, and compose/save/reopen a small analytical report using that segment and existing analytical results. The user can inspect trust and provenance in the accepted UI concept and observe/cancel/retry the same work in Operations. A failure produces an actionable inbox entry and preserves consistent artifacts and history.

Call this an **internal integrated preview** until the required forecast slice also works. The blueprint's **vertical alpha additionally requires monthly revenue Seasonal Naive and CatBoost with rolling backtest**, the common guided/pipeline engine, its artifact/outbox/fencing behavior, and minimal canonical chart rendering. No earlier preview is silently renamed alpha or public MVP.

The potential employer customer can later provide an authorized, sanitized data contract to test interoperability. No customer data, credentials, legal permission, target infrastructure or delivery commitment is assumed here.

## Architectural decisions to preserve

- Modular monolith and one-server local-first delivery through v1; business contexts own state and contracts, while apps compose them.
- PostgreSQL owns control state; immutable artifacts own bulk data; Valkey only delivers/caches.
- Existing W12–W17 and W36–W38 kernels are reused and integrated. An empty planned package is not a reason to move working code without a concrete ownership problem.
- Guided forms and pipeline definitions submit the same normalized execution specification.
- Identity owns actor/workspace/policy decisions. Every protected producer and consumer enforces effective scope.
- Analytics/Forecasting/DQ/Research own meaning; Presentation owns composition/snapshots; charts and renderers never recompute business metrics.
- The accepted target pilot retains authority for its demonstrated composition, navigation, analytical interactions and visual language. Richer or unshown authoring flows follow normative product requirements and the current Web implementation source contract; this roadmap does not amend accepted pilot or proof policy.
- Universal XLSX remains the final new functional v1 increment. Email and operational channels retain distinct delivery semantics. OIDC, remote storage/distributed workers and Yandex Metrica runtime remain future scope.
- No return to the retired G0–G6 process, new design-board program, or family certification ledger.

## Decisions needed before dependent implementation

| Decision | Classification / owner | Recommended disposition | Due / proof |
|---|---|---|---|
| D01: Current base and continuation frontier | Agent-decidable; engineering | Rebase the task envelope on verified current main; preserve the dirty historical checkout; derive ticket status from frontmatter | Before first implementation claim; current source and dependency validation |
| D02: First external release label and scenario | Owner-required; product owner | Prioritize an internal report-and-segment preview while Forecasting is held; select an external scenario and reconcile its release criteria only when external delivery is considered | Before any external release commitment; not a blocker to internal engineering |
| D03: Product-stage inconsistencies | Mostly source reconciliation; material scope changes owner-required | Basic ABC/XYZ/Pareto is v1; enumerate what “extensions” defers. Keep Promotion Journal completion in v1 unless the owner changes scope; allow earlier schema support. Explicitly allocate new product/inventory/document requirements | Before dependent tickets; synchronized machine/human/UI allocation |
| D04: Browser auth and workspace context | Agent-decidable architecture; Identity and Web | Share existing cookie/session and CSRF semantics across browser providers; retain scoped API-token clients; resolve workspace keys against authorized server data | Before feature-wide wiring; actual login → feature → revoke/switch tests |
| D05: Effective data policy and result identity | Agent-decidable architecture; Identity, Semantic, Analytics | Public effective-policy decision before fetch; versioned policy/scope in result/reuse identity; recheck before publication/read/export | Before real restricted datasets or reuse; grant/revoke/row/column negative tests |
| D06: Execution convergence | Agent-decidable architecture; Execution and Data | Canonical Execution run/attempt lifecycle with explicit ingestion batch bindings and owner ports; additive compatibility for W15 history | Before new asynchronous analytical modules; restart/cancel/fencing proof |
| D07: Document and analytical-block identity | Agent-decidable within accepted product semantics; Presentation, Analytics, Web | Common versioned block/result/filter contract, atomic root/page snapshot, stable IDs, separate personal views; minimal first page, then extensions | Before separate dashboard/report/research editors |
| D08: OPEN-007 customer-ID completeness | Methodology proposal plus explicit workspace policy; product/data owner for approved default | Measure representative missingness; define capability states and versioned threshold, denominator and reason codes; never choose a hidden percentage | Before customer analytics is accepted for real inputs |
| D09: OPEN-008 forecast history | On hold; owner resumes Forecasting first | After resumption, derive target/frequency/seasonality/horizon rules, gap policy and leakage-safe tests; insufficient history has an explicit blocker/baseline alternative | Deferred with M3/N7; not a report/segment prerequisite |
| D10: NFR/workload and privacy policy values | Agent prepares evidence; owner decides material operating tradeoffs | Fix reference workloads first, measure latency/resource use, then accept budgets. Set retention/minimum-cell values and recovery loss/time targets with ownership | Before relevant privacy, performance or release boundary; no magic constants inferred from old spikes |
| D11: Static SVG→PNG engine and transport | Bounded technical spike; Presentation/Delivery | Use declared ports, pinned compatible dependency, no-network rendering and a transport with verified idempotency/reconciliation | Before v1 email delivery, with cross-platform failure/fidelity proof |

Do not ask the owner to decide routine port names, hashing, technical artifact ownership or ticket mechanics. Unknown policy choices should become one compact proposal before the affected ticket, not a repeated interruption at every stage.

## Target integration and state flow

~~~mermaid
flowchart TD
  W[Web: authenticated workspace and normalized request] --> A[Identity: effective policy]
  A --> E[Execution: accepted command and durable run]
  E --> O[Transactional outbox]
  O --> Q[Valkey delivery]
  Q --> K[Worker: claim, policy recheck, fencing]
  K --> D[Source and semantic contracts]
  D --> T[Artifact staging and DQ]
  T --> C[Atomic metadata, lineage and publication commit]
  C --> R[Analytics result; Forecasting held]
  R --> P[Presentation: document and root/page snapshot]
  P --> W
  E --> N[Public terminal event]
  N --> I[Notifications inbox]
  I --> W
  X[Reconciler] --> E
  X --> T
~~~

This is a target flow. The audit identifies which arrows do not exist in production composition. No new independently deployed services are implied by these boxes.

| Boundary | Contract and ownership | Failure / retry / identity rule | Required proof |
|---|---|---|---|
| Web → API → Identity | Same-origin browser session, CSRF for cookie mutation, authoritative workspace-key/UUID and effective actor; token auth retained | Unauthorized/forbidden/not-found distinct without existence leaks; refresh once through the shared session owner; no tokens in URL/localStorage | Bootstrap/login/reload/expiry/revoke/switch under two workspaces without injected fixture identity |
| API → Execution | Validated normalized command, request identity, permission/policy version, 202/status reference for long work | Duplicate same payload replays; changed payload conflicts; validation/auth failures are terminal; no unbounded synchronous API computation | Guided/API-equivalent request gives one run/result identity; restart before/after enqueue |
| Execution → delivery → worker | Commands/events via owner ports; run/attempt/lease/fencing, bounded backoff and retry budget | At-least-once delivery; stale worker cannot publish; cancellation remains in progress until child/DB/artifact cleanup completes | Duplicate/lost message, dead worker, reclaim, stale completion, cleanup and immutable terminal history |
| Worker → source | Versioned connector/config/template/mapping and extraction session; adapter resolves secret references | Bounded timeout, cancellation, snapshot consistency and explicit exhaustion; retry session expiry by new attempt; no commit/watermark on incomplete reads | Full file/SQL path; empty, overflow, paging, timeout, drift and late-arriving data |
| Worker → Artifact/DQ/Semantic | Producer-owned content and PII/lineage; artifact commit port; scoped waivers and capability decisions | Staging invisible; failed DQ blocks publication; orphan cleanup is ownership-bound; publication metadata and watermark commit atomically | Crash points, hash mismatch, expired/revoked waiver and cross-workspace reference rejection |
| Result → Presentation | Immutable public result/data/ChartSpec references; explicit metric/filter/policy/version lineage | No renderer-side reduction; refresh creates/rebinds a new result explicitly; published root snapshot stays immutable | Cross-view totals/identity parity; version pinning and denied block/page filtering |
| Terminal event → Notifications | Existing public terminal event port and locale-neutral projection | Separate command/event consumption, dedupe, policy recheck, localized rendering; replay does not reopen resolved issues | Real domain failure → durable inbox; revoke and duplicate terminal events |
| Presentation → email/XLSX | Common ReportSnapshot plus bounded renderer and delivery ports | No partial publication; unknown external submit enters reconciliation, never blind resend; XLSX overflow fails/splits explicitly | Web/static/data parity, kill/restart, transport unknown-state and workbook openability |

Exact timeout, backoff, capacity and retention values belong to a validated ticket-local policy after baseline measurement. The plan specifies their semantics and owner, not unsupported numerical defaults. Logs/evidence contain codes, pseudonymous IDs, hashes and version references; no secrets, cookies, raw PII, file contents or provider payloads.

## Ordered outcomes

Milestones below are proposed roadmap outcomes, not executable ledger rows. Owner-agreed decomposition selects bounded milestone plans; their stages follow the accepted framework. Historical independent tickets remain evidence inputs. A result becomes complete only when its exit evidence exists.

| Outcome | Depends on | User/operational result and scope | Exit evidence / release relationship |
|---|---|---|---|
| M0 — Reconciled scope and integration contracts | Audit | Fix source allocation and current-main task envelope; decide shared auth/policy/run/document interfaces and representative input fixtures; prepare initial tickets | No unexplained requirement conflict at the first frontier; affected provider/consumer/proof owners explicit. Design only, no runtime claim |
| M1 — Authenticated and policy-safe application | M0 D04/D05 | Real bootstrap/login/session, workspace switch, denied/expired/system flows; effective policy applied to existing feature APIs; common generated client/session handling; target navigation and context rules | User reaches all existing feature seams through real auth; two-workspace and same-workspace department/row/column negatives; CSRF, refresh, revoke and deep-link proof |
| M2 — Integrated report-and-segment preview | M1; M0 D06/D07; D08 for customer inputs | CSV/XLSX admission and saved mapping, safe complete extraction, one canonical execution path, DQ/semantic publication, Sales/customer/RFM, reusable rule segment with immutable membership snapshot, common minimal ChartSpec and persisted report with constrained drag-and-drop, trust, run/inbox links | Clean source → rule segment → saved/reopened authorized report without script-only seeding; same guided/pipeline spec identity; forced crash/cancel/retry and no partial publication; actual browser against real APIs/data |
| M3 — Complete vertical alpha — on hold | Owner resumes Forecasting; M2; D08/D09 | Deferred monthly net revenue Seasonal Naive and CatBoost rolling backtest; minimal forecast UI/trust and immutable forecast artifacts through the same engine; all section 26.1/31 obligations | Leakage-free folds and baseline comparison, reproducible artifacts, CPU/resource controls, source/locale-neutrality, alpha journey in development Compose; not an active M4 dependency |
| M4 — Public-MVP data and governance | M2; independent of held M3 | PostgreSQL/MSSQL/MySQL/ClickHouse plus files; incremental/watermark/partition refresh; identity/SCD joins, ReceiptItem/Product/Calendar; mapping/version impact, DQ remediation, Data Guide/filter/metric registries; complete auth and organization admin UI | Real connector matrices; history/return/FX/grain correctness; policy-safe discovery, preview, counts and export; migration/backfill/rollback evidence |
| M5 — Public-MVP analytical product | M4 providers for each sub-slice; forecast portion also needs resumed M3 | Extend M2 rule segments into cohorts/lifecycle; methodology/cases/research; template dashboards, collaboration/adoption/watches; branding/company packs; materialization/single-flight/lanes; schedules/operator/inbox; CSV/Parquet. MVP forecast/baselines/intervals/registry/monitoring remain on hold | Each non-forecast slice can finish independently at its real UI/API/data boundary; complete public-MVP section 26.2 and AC-001–048 remain unfulfilled while required forecasting is held |
| M6 — Public-MVP qualification | All required M5 slices, including resumed forecasting | Full one-server topology, installation/update, coherent backup+key+artifact restore, observability and failure runbooks, privacy/security/accessibility/localization, measured workload and dependency/license evidence | Non-forecast qualification work can proceed on delivered slices; a full public-MVP claim requires every criterion. External release remains separately authorized |
| M7 — V1 analytics and low-code expansion | Actual M5 provider contracts and relevant M6 evidence, not a blanket forecast dependency | Full segment history/outliers/buckets/stratification/KMeans; product/category/assortment/inventory/basic ABC/XYZ/Pareto/pricing; discount/cap/PVM; basket/store/channel; Promotion Journal; digital journeys/attribution/unit economics/assumptions; accessible canvas/templates/SDK. Full forecast target set remains on hold | Every feature uses existing policy/run/result/document contracts; defined input capability blockers and golden method evidence; no causal claim inferred from descriptive data |
| M8 — V1 presentation, delivery and operations | Common M5 document contract; relevant M7 projections | Complete compact/matrix/parameterized composer, explicit click wiring, prior/custom/population comparisons, cell-to-evidence and semantic revision diff; Focus/personal views and unshown UI; notes/annotations/discussions distinctions; themes/branding/help/system lifecycle; bounded static rendering/user report email; email/webhook operational channels | 100 pages × 30 blocks design envelope measured; lazy authorized page loading; exact snapshot/filter/lineage parity; sender/domain/PII policy and unknown-state reconciliation |
| M9 — Pre-XLSX hardening | M7 + M8 | Benchmark entire selected v1 workload, reuse/invalidation/lanes, chart/static render, connector matrices, recovery/update, permissions, all shipped themes, runbooks/docs and supply chain | Blueprint Phase 5 evidence, unresolved cross-channel/method/security defects closed; no new product features added under hardening |
| M10 — Universal XLSX | M9 | One renderer over stable ReportSnapshot: README/Contents/Summary/typed data/charts/Metadata, native charts or same-renderer fallback, safe split/preflight/formula protection | Web/email/XLSX parity, workbook openability, no silent truncation, resource/cancel/recovery evidence. Last new functional v1 slice |
| M11 — Final v1 qualification | M10 | Acceptance-only pass across all v1 obligations and target update/rollback documentation | All V1-AC-001–067 and applicable shared AC/test invariants evidenced; no feature expansion; release/deployment only under explicit authority |

M4/M5/M7/M8 are decomposed below; they are not giant execution tickets. Common contract work may start before their parent milestone closes, but later consumers cannot be accepted before their actual provider prerequisites.

### Capability ownership and completeness allocation

| Delivery track | Existing owner contexts / reuse | Required continuation | Main outcomes |
|---|---|---|---|
| Access and tenancy | Identity/W12/W13 | Shared session, route identity, effective row/column/object/export scope, role/admin/people UI, revocation and privacy-safe activity | M1, M4, M5 |
| Source onboarding | Connection Catalog, Data Documentation, Ingestion/W14/W15 | Saved connections/list/drafts, templates/files → ingestion, mapping/discovery/preview, SQL matrix, consistent incremental/partition/append/upsert and schema drift | M2, M4, M7 |
| Semantic quality | Semantic Model, DQ, Artifacts | Identity/SCD/grain/time/currency, versioned metric/filter/method references, capabilities, waivers/remediation/history, Data Guide and policy-safe artifact lifecycle | M2, M4, M5 |
| Execution and compute reuse | Execution/W15/W36/W38, Notifications/W37 | One production run path, scheduler/typed workers/dispatcher/reconciler, progress/ETA/CPU, single-flight/materialization/partition invalidation and lanes | M2, M3, M5 |
| Core analytics | Analytics/W16 | Complete sales/customer/RFM, trend and dimensional projections, comparisons; cohorts/lifecycle/rule segments and metric semantics | M2, M4, M5 |
| Forecasting — on hold | Forecasting; existing semantic/artifact/execution contracts | No active forecast work. After explicit owner resumption: alpha model pair → MVP targets/intervals/registry/monitoring → full v1; preserve requirements without speculative implementation | Deferred M3 and forecast portions of M5/M7 |
| Documents and Web platform | Presentation, chart_compiler_ts, Web, ui-foundation | Shared normalized block model, small persisted document first, stable root/page snapshots, result trust, ECharts, filter/Focus/Custom View, complete target-pilot conformance and missing-screen outcomes | M1, M2, M5, M8 |
| Research and methodology | Methodology & Research, Analytics public result ports | Registered method lifecycle, cases, evidence/findings/decisions, reusable products and narrative publication through Presentation | M5, M7 |
| Collaboration and adoption | Collaboration & Adoption, Identity, Notifications | Requester/executor, exact anchors/mentions/resolve, likes/follows/views/feed, privacy suppression, adoption, metric watches; authored findings stay Research-owned | M5, M8 |
| Advanced customer segmentation | Analytics, Semantic, Execution | Related-object/aggregate/sequence rules, curated/composed populations, explicit membership time and explanations; existing treatment/buckets/strata/KMeans/history and member grants | M7 |
| Retail product analytics | Semantic, Ingestion, Analytics product boundary, Promotions | Hierarchy/history, assortment/inventory/availability/pricing, base ABC/XYZ/Pareto, product lifecycle, affinity, returns, PVM and source capability blockers | M4 foundations, M7 completion |
| Digital and economics | Digital Journey & Marketing Measurement | Source-independent event/touch/cost/identity contracts, offline reconciliation, funnels, deterministic attribution, governed assumptions/unit economics; Yandex connectors remain future | M7 |
| Low-code and extensions | Execution and trusted Plugin SDK | Guided templates first, equivalent pipeline spec, then accessible canvas, version diff/impact, trusted source extension contracts | M2, M5, M7 |
| Delivery and notifications | Report Delivery vs Notifications | Operational in-app first; later isolated email/webhook policies and verified-sender report delivery; common static report renderer | M5, M8 |
| Operations, security and release | Ops/DevOps, Audit, all context owners | Resource admission, redacted audit, restore/keys/orphans, health/alerts/runbooks, install/update, supported dependencies/licenses, performance/a11y/i18n evidence and user help | Continuous, formal M6/M9/M11 |
| XLSX | Presentation renderer port | Stable final report export, independent from file-import XLSX validation | M10 |

The frozen coverage JSON assigns all 1,141 indexed IDs and all 169 route/overlay/system/capability entries to these planning concerns. Those assignments are broad ownership/qualification allocation, not proof that all IDs in a family are due at the earliest listed milestone. Individual tickets bind exact clauses. The frozen snapshot contains 48 AC and 54 V1-AC entries. The subsequent adoption delta is mapped separately below; frozen audit counts are not a current completeness claim.

### Adopted capability allocation beyond the frozen audit

| Requirements and criteria | Provider dependencies | Delivery outcome / qualification |
|---|---|---|
| FILTER-013 through FILTER-018; V1-AC-055 | Semantic relationships/metrics, DQ completeness, Identity policy, normalized Execution plan; sequences also require event history | N5S begins with correlated customer rules; full aggregates/sequences extend M7; M11 verifies full coverage |
| SEGMENT-029 through SEGMENT-033 and SEGMENT-037; V1-AC-056 | Governed identity/import/artifacts, revision concurrency, dependency resolution and member policy | Collections/composition/explanation extend N5S in M7 with real refresh/revoke proof |
| SEGMENT-034, SEGMENT-035; V1-AC-057 | Versioned effective membership/property history and knowledge-as-of | M7 event-time semantics after history providers; no inferred continuous history |
| PIVOT-001 through PIVOT-006; ANALYTICAL-DOC-014, ANALYTICAL-DOC-015; V1-AC-058 | Metric aggregation compatibility, bounded result projection and common document persistence | N5 compact matrix subset, M8 full authoring; M9/M10 cross-channel and XLSX proof |
| PARAM-001 through PARAM-005; BLOCK-BUILDER-009; V1-AC-059 | Typed registries, template owner lifecycle, target mapping and common result identity | N5 scoped controls, M8 reuse/upgrade/interactions; no copied formula engine |
| COMPARE-011 through COMPARE-013; V1-AC-060 | Calendar/window and population binding, compatible metrics and both-period coverage | M7 producer/M8 consumer slices; independent of Forecasting |
| SEGMENT-036, REPORT-015; V1-AC-061 | Semantic cell keys, complete authorized membership projection and provider conversion capability | M7/M8 drill/selection slices; save/reopen/return and negative access proof |
| REPORT-016, REPORT-017; V1-AC-062 | Immutable version manifests, safe evidence projections and explicit comparable inputs | M8 draft/history diff; existing publications remain unchanged |

TEST-INV-102 through TEST-INV-112 constrain these authoring slices; each implementing
ticket binds exact invariants and actual boundary evidence. Target completion
includes the whole authoring delta, even when an early internal subset omits a feature.

The subsequent accepted source-data delta is allocated separately:

| Requirements and criteria | Provider dependencies | Delivery outcome / qualification |
|---|---|---|
| IDENTITY-006 through IDENTITY-008; DATA-MAP-001 through DATA-MAP-007; INGEST-008 through INGEST-020; DQ-INPUT-001 through DQ-INPUT-008; V1-AC-063 through V1-AC-067 | Published source/key/readiness/coverage/tolerance policy; shared semantic mapping and DQ; canonical Execution and immutable artifact publication | N3 proves snapshot correction, absence/reappearance/reassignment, imperfect-input accounting and typed mappings; N4 proves pull/push/notification replay, checkpoint and recovery. Relevant real-source acceptance requires its applicable proof; M11 verifies the complete v1 delta. |

TEST-INV-113 through TEST-INV-122 constrain these source-data slices. Their
allocation supplements the frozen historical coverage and does not claim that
implementation, provider guarantees or acceptance evidence already exist.

### Public-MVP product decomposition

After M4's provider contracts are available, prepare separate vertical slices for:

1. Extend the M2 rule-segment foundation into cohorts/lifecycle and segment history with exact membership/snapshot/period identity.
2. **On hold:** MVP forecast expansion, intervals, registry and monitoring over the resumed M3 path. This does not block the other slices.
3. Metric/Methodology Registry and AnalysisCase, then Research documents/findings through the shared composer.
4. Dashboard templates and access, then collaboration/feed/adoption and watches with independent privacy policy.
5. Scheduler and materialization reuse, including interactive/maintenance isolation and invalidation; build its admin projection from actual telemetry.
6. Complete organization/people administration, branding/company packs and safe asset validation.
7. Authorized CSV/Parquet exports, retention and backup/restore over the same artifact model.

Each includes its own UI, backend, data-contract and failure proof as applicable. This prevents separate frontend/backend backlogs from declaring incompatible halves complete.

## Immediate ticket-preparation frontier

These are **ticket candidates**, not current ticket files or assigned IDs. Resolve against live ticket names when materializing them. Use the repository ticket template, exact touched paths, command list, evidence target and requirements. No future feature receives `ready` merely because it appears here.

| Candidate | Depends on | Narrow outcome / likely ownership | Acceptance and stopping boundary |
|---|---|---|---|
| N0 — Continuation contract and acceptance allocation | This audit and the capability discovery report | Reconcile blueprint/human/UI release allocations, D04–D07 deltas and NFR ownership; bind the accepted authoring contract to provider/consumer schemas and migration proof before N5/N5S; prepare bounded provider/consumer tickets | Exact supported segment operators, population/time semantics, matrix/parameter contracts and compact outcomes declared; candidate extensions adopted or explicitly deferred. No policy values, product acceptance or implementation completion invented; source-data readiness, identity, mapping and tolerance schemas also bind TEST-INV-113–122/V1-AC-063–067 before their dependent N3/N4 work |
| N1 — Browser identity/workspace bridge | N0 D04 | Identity HTTP adapter and Web session/router/client integration; existing APIs retain token support | Real bootstrap/login→sales/runs/inbox, refresh, cookie mutation CSRF, logout/revoke and two workspace keys; no test bearer injection; unrelated UI redesign excluded |
| N2 — Effective data-policy integration | N0 D05; coordinate shared N1 paths | Identity public policy projection and analytics/source/artifact consumers | Deny before fetch, row/column/PII/export limits, policy-version identity and revoke with unchanged role strings; no cross-context private-table reads |
| N3 — Safe user data admission | N0 source contract, N1/N2 for integrated proof | Connection/list/import/mapping source and semantic contracts; eliminate silent extraction bound; persist file intake identity | Real CSV/XLSX → governed batch; daily full snapshots without row markers, old edits/reassignment/absence, source-readiness generations, duplicate/conflict/degraded coverage and typed SP channel fixtures; empty/overflow/drift/expired-session cases |
| N4 — Domain jobs in canonical execution | N0 D06; N3 batch contract | Execution adapter + data worker + production composition; preserve existing run/artifact history | One real job visible and controllable in Operations and inbox; push/pull/notification replay and incomplete-batch/checkpoint proof; duplicate/restart/cancel/kill/fence evidence; migration/compatibility and no competing authoritative terminal state |
| N5 — Shared compact report composer/ChartSpec skeleton | N0 D07 and selected matrix/parameter semantics; N1/N2 for protected browser proof | Presentation public contract + chart compiler + common Web components; one table-first page with a bounded supported matrix, compact controls/metrics and common blocks; split provider/consumer work into ordinary tickets | Persist/reopen stable blocks and exact results; separate reader/author chrome; drag/reorder plus equivalent commands; correct matrix totals, typed controls, Focus and trust; density/layout preserve business result identity |
| N5S — Reusable relational customer segment and report binding | N0 segment/result language; N2 policy; N3 governed related inputs; N4 run path; D08; N5 for report integration | Analytics-owned expression with an explicit first subset of related-order/line predicates and existence semantics, versioned definition and immutable membership; entity-aware Web editor and protected explanation; Presentation consumes snapshot references | Same-order versus independent-order witness, explicit window/as-of/missing treatment, authorized count/explanation, save/run/reopen/reuse; pinned vs latest-successful, permission/empty/invalid/stale states. Full event sequences and other candidates wait for declared prerequisites; no forecasting prerequisite |
| N6 — Internal integrated preview acceptance | N1–N5 and N5S | One complete real user journey and CI coverage; repair only faults within selected integration scope | Source→DQ→run→sales/customer/RFM→rule segment→saved report→operations/inbox, with failure/revoke/reload; internal preview while Forecasting is held |
| N7 — Alpha forecast slice — on hold | Explicit owner resumption; N6 plus D08/D09 and method/metric contracts | Deferred forecast spec/series/features/backtests/registry minimum, worker and result UI | Monthly revenue Seasonal Naive vs CatBoost rolling backtest, insufficient-history behavior, temporal leakage tests, artifact/policy/cancel proof; no active ticket preparation during hold |

N0 should be a compact reconciliation, not weeks of planning. Only genuinely unresolved contracts become specifications. N1 is the recommended first implementation after that reconciliation. N2 and the data completeness correction block use of restricted real datasets.

### Permitted concurrency and shared ownership

Planning allows independent work after provider contracts are stable; it does not start subagents, tasks or concurrent execution.

- After N0, document/compiler contract work and source-adapter work can progress independently of session UI work, but integrated acceptance waits for N1/N2.
- N3 and N4 share data-pipeline contracts and migration ordering; agree those contracts first or execute serially.
- Source-connector adapters can proceed independently after the connector/session contract and test fixture are fixed; each carries a real database matrix.
- Reports, rule segments, research and collaboration consumers can proceed independently after their actual policy, normalized result, execution and document contracts stabilize. Forecasting is excluded from active work until owner resumption.
- Product analytics belongs to the existing Analytics context; Digital Journey & Marketing Measurement is a separate context. They share declared semantic/metric/result ports rather than private tables.
- Shared OpenAPI/generated clients, migration chain, Web shell/tokens and context contracts have one active integrator per change. Feature-local tickets can run independently only with disjoint ownership.
- When availability is low, execute one ticket at a time. Do not parallelize merely to produce more documents or screens.

## Report and segment authoring — interaction proposal

The owner prefers drag-and-drop but also explicitly requires the ability to author compact, table-first reports. Existing requirements already specify a common document/block engine, guided analytical builder and reusable segments. The earlier conversation sketch only illustrated a small interaction subset and is not visual or functional acceptance. The normative blueprint and accepted analytical-authoring contract govern the adopted capability semantics; the capability discovery report supplies supporting evidence, historical candidate labels and explicitly optional expansion proposals. No new prototypes are requested. A focused working-screen check belongs to the eventual implementation ticket, not another product-wide design program.

### Report composition

Use a block palette/page outline, a central document and a properties panel for the selected block. Drag a metric, chart, table, heading or text block into a visible insertion target; rearrange blocks and sections; use constrained grid spans for dashboards and ordered flow for workbook/research pages. Grid snapping, collision handling and minimum readable sizes replace arbitrary pixel placement. Provide add/move/resize commands operable by clicks and keyboard, plus undo/redo and revision-safe draft persistence. No layout operation starts a new analytical calculation.

Configuring a data block follows `BLOCK-BUILDER-001–008`: subject/data product → registered metric(s) and grain → dimensions and period → segment/population where applicable → optional filters/comparison/presentation. Choosing a block opens these settings; dragging an already configured block preserves them. A saved segment is selected by reference, not reconstructed inside each chart. Show unsupported metric/grain/segment combinations before Add/Run and explain the missing input or permission. Dragging a display label never silently invents a metric, join, aggregation or filter scope.

The initial slice needs one compact table-first page, a bounded matrix capability and real persistence/results. Reader mode hides edit handles, palettes and properties; matrix row/column/measure settings are distinct from arranging page blocks. Density is independent of grid/flow composition. Templates are an optional starting point over the same blocks. Decide hierarchical/total/parameter semantics early, then implement advanced variants and additional pages through their provider contracts. Static/email/XLSX rendering retains its existing sequencing.

### Reusable rule segments

Start with a customer population and an explicit observation-window policy. Show an entity-aware searchable catalog, related orders/lines/events and typed conditions inside visibly nested **all / any / exclude** groups. The contract must distinguish properties of one related object, independent related objects, existence/absence, scoped aggregates and any explicitly supported temporal operators. The earlier “three purchases / revenue / recency” example is a small illustrative subset, not the target definition of segment authoring. First implementation may support fewer operators after the broader representation is resolved.

Add conditions from an allowed feature catalog. Dragging may reorder rows within the same group without changing membership. A separate explicit move-to-group command can change grouping; arbitrary drops must not silently change AND/OR/exclusion semantics. Group operators stay visible and editable. This structured rule tree is the recommended primary editor; a node-and-edge pipeline canvas belongs to advanced workflow authoring and is not required to create a segment.

Preview evaluates the same normalized definition that a saved run uses. It shows authorized population size, matched count/share, as-of/window, freshness, missing-data exclusions and relevant quality/permission blockers. Expensive work uses the canonical asynchronous execution path; mark an estimate or sample explicitly and do not present a stale or sampled count as an exact current count. Previewing membership or exporting members requires its separate row/PII permission.

Save a named, versioned reusable definition; running it creates an immutable membership snapshot. Record missing-value behavior, units/currency, temporal boundaries and exclusion semantics explicitly. A multi-group segmentation additionally needs its declared overlap policy. Start with rule segments and reuse compatible RFM outputs; buckets, historical migration and KMeans remain later capability slices, with their own methodology proof. The Forecasting hold does not itself defer all segmentation, nor authorize new ML work.

### Segment use inside a report

`SEGMENT-019–026` already provides the important distinction: a definition is a reusable rule; a snapshot is its resolved membership at a known time. A published workbook/research report pins an exact snapshot. A live dashboard may explicitly follow the latest successful snapshot for that definition, while each result manifest still records the exact resolved snapshot. Refreshing a draft or live view creates/rebinds a new result; it never silently changes an already published report.

Before applying a segment to a block, validate the customer/transaction/product grain and authorized relationship. Report period and segment observation window are separate controls and must both remain visible when they differ. Reference selection does not grant access to members or widen a block's row/column policy. Show loading, empty, invalid, permission-denied, outdated-preview and failed-run states in the same feature ticket.

### Requirement and proof anchors

- Product blueprint: sections 12.10, 12.14, 12.15 and 14; `SEGMENT-001–028`, `BLOCK-BUILDER-001–008`, `ANALYTICAL-DOC-001–013`, `DASHBOARD-006`, `A11Y-002`.
- Required explanatory mirror: sections 12.2 and the universal block-builder table; dashboard authoring and keyboard alternatives.
- Acceptance: real source → typed segment → immutable snapshot → shared report block → save/reopen; drag and button/keyboard paths yield identical block order/layout; rule grouping, null/time boundaries and permissions use the same backend semantics in preview and saved runs.
- Dragging alternatives also follow [W3C's explanation of WCAG 2.2 SC 2.5.7](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements): an alternative single-pointer interaction is necessary in addition to keyboard operability. A keyboard-only substitute is insufficient for that criterion.

## Compatibility and migration strategy

These are proposed constraints; exact migration artifacts and commands belong to the implementing tickets and current runbooks.

| Change | Classification before implementation | Migration / rollback constraint |
|---|---|---|
| Shared cookie auth alongside tokens | Expected compatible-change; CSRF/CORS tightening may affect current clients | Preserve valid token flows; enumerate current browser mutation behavior; add common dependency without exposing HttpOnly credentials |
| Workspace key resolution | Compatible additive contract; current hard-coded default is not authoritative identity | Resolve only authorized memberships; preserve accepted deep links and safe redirects; reject mismatch before data fetch |
| Effective policy/result identity | Unknown until contract delta is fixed | Version cache/result policy keys; never reuse an artifact computed under incompatible scope; do not retroactively relabel immutable results |
| W15-to-Execution integration | Compatible additive migration preferred | Retain batch/artifact/attempt lineage and old history; new jobs use one terminal authority; no blind dual writes; rollback stops/drains new jobs before reverting consumer routing |
| Generalized mapping/extraction | Compatible versioned specs preferred | Existing fixed retail fixture remains test input; old runs pin old mapping/engine; incomplete new reads never commit; schema upgrades include empty/existing data paths |
| Common document/root snapshot | Additive schema with explicit versioned public union | No live rewrite of published snapshots; drafts use revision/CAS; optional compatibility adapter preserves current route fallback until real API/browser proof |
| Full SQL/incremental behavior | Connector-specific compatible/breaking classification | Watermark/backfill/source-version policy explicit; cutoff and late-arrival replay tested; rollback never pretends an advanced watermark was not committed |
| Mail/static render/XLSX | Additive later capability | Disabled until required evidence; partial render never visible; unknown delivery reconciles with durable handle; no arbitrary resend on rollback |

A migration's unit test or successful DDL is insufficient for data-bearing cutover. Prove fresh database, existing accepted data, interrupted rollout, downgrade/restore policy and immutable lineage at the actual affected boundary. Do not invent a production host or restore credentials.

## Nonfunctional work is part of each outcome

| Concern | First required work | Qualification / evidence |
|---|---|---|
| Security and tenancy | N1/N2 auth, CSRF, effective scope, secret references and PII-safe fixtures | Two-workspace and same-workspace policy tests, source/network/file trust boundaries, export recheck; broader release security review at M6/M9/M11 |
| Correctness and reproducibility | N3/N4 grain, identity, typed inputs, atomic commit and lineage | Golden totals/returns/currency/time/SCD cases, deterministic replay and invalidation; methods/backtests get specialized tests |
| Runtime reliability | N4 restart/duplicate/lease/fencing/cancel; admission and bounded retry | Kill worker/queue outage/DB outage/disk full/corrupt artifact; alert and recovery action tied to each failure |
| Performance and capacity | N0 workload declaration; M2 first measured path | Cold/warm/concurrent p50/p75/p95, CPU/RAM/temp disk and cancellation; 100×30 documents, bounded chart data and reuse/invalidation measurements before M8/M9 acceptance |
| Recovery and lifecycle | Design artifact/DB/key consistency at N4; implement backup/restore before M6 | Coherent backup manifest, restore to isolated target, key decryptability, sample result, downgrade/update path and measured loss/time objective |
| Accessibility and localization | Every changed Web ticket | EN/RU, keyboard/focus, allowed 768/1920 Web endpoints, zoom/reflow and reduced motion; screen-reader/full WCAG claims require their own evidence |
| Observability | Execution and API integration | Versioned event/metric/error names, redaction, queue age, lease/reconciliation, DQ/freshness, resource pressure and render/delivery counters; alert severity/owner/runbook action |
| Maintainability and compatibility | Every contract change | Provider/consumer drift, dependency direction, migrations, backward behavior and generated clients; no manually invented mock DTOs |
| Dependencies and distribution | Ongoing scoped dependency work | Existing Dependabot PRs reviewed under ADR-0007/lockfile policy; pinned builds, license/SBOM/provenance, installer/update docs and supported target proof |
| Privacy/retention | Before collaboration/adoption/export | Versioned event retention, minimum-cell suppression, deletion/anonymization and audit retention separation; approved policy values and revoke propagation |

The initial resource envelope remains the accepted local development policy; do not treat it as a demonstrated production capacity guarantee. No specific latency, restore time or throughput is promised until measured and accepted.

## Ready and done rules

A candidate becomes an execution ticket only when its outcome, exact requirements, current provider contracts, prerequisite evidence, owned paths and proof commands are explicit. Unresolved business policy cannot be replaced with an undocumented default. The architecture roadmap is not executable authority by itself.

A ticket finishes only at its declared boundary. Record separately:

- contract/source correctness;
- actual API, database, artifact or connector behavior;
- browser behavior against that actual provider;
- runtime recovery/capacity or release qualification when required.

At each milestone, trace its acceptance obligations to those ticket references. The coverage snapshot is a planning baseline; it must not become an independent completion register. For a requirement with only prototype evidence, the product obligation remains open even if that prototype ticket is accepted.

A passing release label requires all obligations for that label. A deliberately smaller internal preview may be useful, but changes neither public-MVP requirements nor v1 completion.

## Keeping the plan useful without continuous replanning

Use rolling detail: exact next tickets, next outcome's dependencies, and broad later capability allocation. Revisit the plan only when source semantics change, a provider contract proves inadequate, measured workload breaks an accepted assumption, a shared path blocks independent work, or the owner changes release intent.

Do not seek a guarantee of zero rework. Reduce expensive rework by fixing policy/identity/grain/run/document seams early, testing risky integrations before expanding consumers, preserving versioned contracts, and measuring real workflows. Reversible screen detail and module internals can evolve within those boundaries.

Before every outcome expansion, check for missing contracts and evidence; do not repeat a product-wide audit or rebuild an atlas when the affected boundary is already known. Preserve the single accepted pilot and existing all-screen requirements; implement missing screens in their working feature tickets.

## Documentation and next safe action

Directly affected documents are blueprint sections 26/28/30/31 and relevant contract sections, the human mirror, UI release/source allocation, system/context architecture where a real integration decision changes, generated contract indexes, tickets and focused evidence. Exact files and validators belong to N0 and its successor ticket envelopes.

**Next safe action:** bind the adopted analytical-authoring and source-data-adaptation requirements to actual versioned provider/consumer schemas in N0 on verified current main, retaining settled N1/N2 integration work. Resolve the real source readiness/key/coverage evidence and explicit workspace tolerance policy before N3 acceptance; N3/N4 use the adversarial snapshot corpus and shared execution path. Continue with the compact report composer and relational customer segment, then N6 acceptance. N7 stays on hold. This document does not select an external release scenario or authorize a new implementation ticket.

## Historical revision validation — 2026-09-05

The following paragraph records the early hold/discovery revisions, before the later authoring and source-data requirement adoptions above. The initial hold/interaction update changed this roadmap only; the later discovery correction also added its linked research report and contributor index entry. The normative blueprints, frozen audit/coverage, product code and ticket states are unchanged by these revisions. `validate_blueprints`, `generate_docs_index --check`, `check_docs_links` (using `uv run --locked python -m tools.custometry_quality.<command>` after `source scripts/activate-toolchain.sh`) and `git diff --check` are the documentation validation boundary.

A conversation-only mockup used synthetic customer records to check report block add/reorder/undo, segment AND/OR preview invalidation and fixed membership binding. Browser DOM-event checks observed those state changes; report/segment layouts had no horizontal overflow at 736, 360 and 320 px, with light/dark visual inspection. Native pointer routing into the sandboxed standalone preview was not observed, so these checks do not certify native drag-and-drop, keyboard/screen-reader behavior or any product/API integration. Those remain N5/N5S working-ticket proof.

## Sources

- [Audit and current implementation evidence](development-audit-2026-09-04.md)
- [Product capability discovery and owner correction](product-capability-discovery-2026-09-05.md)
- [Frozen requirement and surface allocation](development-coverage-2026-09-04.json)
- [Normative release stages and phases](https://github.com/Dejetins/custometry/blob/94672bf97a402d9c90e96ac8b783b6a0e30adba0/custometry-technical-blueprint-ru.md#L7493)
- [Normative first internal slice](https://github.com/Dejetins/custometry/blob/94672bf97a402d9c90e96ac8b783b6a0e30adba0/custometry-technical-blueprint-ru.md#L8557)
- [Accepted bounded-context ownership](https://github.com/Dejetins/custometry/blob/94672bf97a402d9c90e96ac8b783b6a0e30adba0/docs/architecture/bounded-context-map.md)
- [Accepted frontend platform](https://github.com/Dejetins/custometry/blob/94672bf97a402d9c90e96ac8b783b6a0e30adba0/docs/adr/0007-responsive-web-frontend-platform.md)
- [Current Web implementation source contract](https://github.com/Dejetins/custometry/blob/94672bf97a402d9c90e96ac8b783b6a0e30adba0/docs/architecture/ui/custometry-web-implementation-source-contract-v1.md)
