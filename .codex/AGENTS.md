# Custometry Agent Engineering Contract

## 0. Purpose and precedence

This is the normative repository-local contract for humans and agents working on Custometry. It governs repository changes, architecture work, prompts, staged execution, evidence, and reporting.

Precedence:

1. platform/system/developer instructions;
2. explicit user constraints for the current task;
3. root `AGENTS.md` and this file;
4. normative machine blueprint `custometry-technical-blueprint-ru.md`;
5. human mirror `custometry-technical-blueprint-human-ru.md`;
6. an accepted task-specific `plan_doc`, current `stage_ledger`, and stage prompt;
7. implemented code, tests, schemas, configuration, and current repository conventions;
8. historical plans, reports, generated prompts, and chat memory.

When two applicable sources conflict, stop at the narrowest material conflict, identify both sources, and follow the higher-priority source. Do not silently reinterpret a `MUST`, a stable requirement ID, or an accepted stage gate.

### 0.1. Repository language policy

- English is the default and required authoring language for repository-created engineering artifacts: architecture documents, ADRs, contracts, plans, prompts, stage ledgers, iteration reports, runbooks, templates, code comments, contributor documentation, and generated contributor indexes.
- The existing normative product sources `custometry-technical-blueprint-ru.md`, `custometry-technical-blueprint-human-ru.md`, and `custometry-ui-blueprint-ru.md` remain Russian until an explicitly authorized product-spec migration renames and translates them.
- Localized product documentation under `docs-site/docs/<locale>/**`, UI localization catalogs, and localized fixtures may use their declared locale; this is product localization, not the repository engineering language.
- Agents may use any language for private reasoning, but durable repository artifacts and agent-to-agent handoff artifacts are English unless the user explicitly requests another artifact language for the current task.
- The final user-facing completion report defaults to Russian. Intermediate repository reports, ledgers, evidence files, and prompts remain English.
- Preserve exact identifiers, paths, commands, and locale-specific product copy. Refer to normative Russian requirements by stable ID and explain them in English instead of copying Russian prose into an engineering artifact.

## 1. Product source of truth

- `custometry-technical-blueprint-ru.md` is normative, currently `0.8.2-draft`.
- `custometry-technical-blueprint-human-ru.md` is a synchronized explanatory representation.
- A new normative requirement appears in the machine version first and is mirrored into the human version in the same scoped change.
- Preserve `document_family_id`, `spec_version`, mutual links, and the set of normative requirement IDs.
- Every non-trivial implementation or plan must cite the requirement IDs it implements, verifies, defers, or intentionally leaves unaffected.
- A `SHOULD` deviation requires an ADR or an explicit decision record with rationale, consequences, and re-evaluation trigger.
- Generated prompts, iteration reports, ledgers, and previous agent conclusions never override the blueprint.

Current repository status is a Foundation scaffold only. Empty directories and manifests reserve ownership boundaries; they do not prove runtime, API, database, browser, deployment, security, performance, or release readiness.

## 2. Fixed product boundaries

Preserve these decisions unless the machine blueprint is deliberately revised under explicit authority:

- modular monolith first; do not split microservices by folder or process name alone;
- PostgreSQL is control-plane and run-state truth; Valkey is delivery/cache, never final state truth;
- immutable published definitions and reproducible result manifests;
- one execution engine for Guided and Pipeline modes;
- transactional outbox, at-least-once delivery, attempt identity, leases/fencing, and reconciler;
- multi-workspace isolation by default and `workspace_id` across scoped metadata, artifacts, tasks, cache, notifications, and audit;
- local filesystem artifacts and a single-server topology through `v1_target`;
- English default/fallback, complete Russian support, locale-neutral core;
- local auth in public MVP; OIDC/Keycloak runtime only post-v1 after a separate security decision;
- public result API, external database destination writes, object storage, remote workers, and Kubernetes are post-v1 and require separate decisions;
- TDA, arbitrary browser Python, generic Airflow/dbt/Jupyter/BI replacement, marketing execution, and causal claims are non-goals.

Only `OPEN-007` and `OPEN-008` remain open product-policy decisions in the current blueprint. Do not invent their values in implementation.

Accepted Foundation operating decisions are recorded in `docs/adr/0001-foundation-operating-model.md`:

- the repository remains public; secrets, customer data, private topology and raw provider state never enter any branch;
- `main` is protected and changes use required PR checks, squash and linear history; no `develop` or per-stage branches;
- the first deployment proof target is the local Apple Silicon MacBook Pro M3 Pro;
- Web/API/data core runtime is offline-capable and has no arbitrary outbound network; Edge is a secretless infrastructure ingress adapter with separate `edge_to_web`/`web_to_api` adjacency and may retain ambient transport egress until target-specific hardening; future connector, mail and update egress use separate explicit allowlists;
- normal local budget is 6 GiB RAM and 25 GiB repository/container-owned data; benchmark is opt-in;
- installation is download-first from pinned digests, not a multi-gigabyte bundle of images, caches and registries;
- safe user/install docs ship locally; operator/admin docs require authorization; architecture, ADRs, contracts, prompts and iteration evidence do not ship in the ordinary installation;
- target product docs use MkDocs Material `/docs` and in-app `/help` over one generated, visibility-aware index; the current contributor `docs/README.md` index is not that runtime proof;
- development data uses separate control and demo-source PostgreSQL boundaries with deterministic retail fixtures.

## 3. Context acquisition

Read the smallest authoritative set that makes the task safe.

Default order:

1. `AGENTS.md` and this file;
2. current user request;
3. machine blueprint headings and requirement IDs directly relevant to the task;
4. human mirror for product meaning and user-facing explanation;
5. active plan/ledger/stage prompt when staged work is involved;
6. nearest implementation entrypoints, contracts, schemas, migrations, tests, and configuration;
7. runtime/deployment material only when that boundary is triggered;
8. historical reports or previous prompts only for unresolved context.

Stop when ownership, changed contracts, expected files, acceptance surfaces, proof boundary, and blockers are known. Do not preload the whole repository or every skill. A missing material source is a blocker, not permission to reconstruct it from memory.

For broad architecture changes: audit current state first, surface material decisions, obtain acceptance of the target plan, then create an executable prompt pack. Do not start cross-domain implementation from a draft architecture conversation.

## 4. Architecture and code direction

- `apps/*` are delivery/process composition roots.
- `packages/*` own domain/application contracts and the ports they need.
- Infrastructure adapters implement ports and are wired at composition roots.
- Domain/application code must not import FastAPI, Celery, SQL drivers, or filesystem implementation details.
- Persistence uses explicit repositories and SQLAlchemy Core; ORM/ActiveRecord is outside the current blueprint.
- Do not read another bounded context's private tables directly from application code.
- API DTOs, persistence rows, and domain types remain distinct when their semantics differ.
- Public backend boundaries use `Protocol`/ABC or an equally explicit contract.
- Prefer composition over implementation inheritance.
- Constructors accept dependencies and validate invariants; network or disk I/O in constructors is forbidden.
- Data transforms should be explicit functions with typed inputs/outputs when a domain object is unnecessary.
- Every nondeterministic path has an explicit seed and reproducible configuration.
- Every tabular dataset declares grain, primary key expectation, timezone/currency policy, lineage, and PII class.
- Do not hide domain assumptions in UI defaults, cache keys, SQL fragments, or model preprocessing.

Use the exact module names in blueprint section 25. `packages/audit/`, CI/runbook paths, frontend workspace manifests, and additional test-surface folders are documented compatible extensions in `docs/architecture/repository-layout.md`.

The complete context ownership and integration rules are in `docs/architecture/bounded-context-map.md`. Do not add a cross-context import, private-table read, shared-kernel business rule, or ownership exception without updating that map and passing `check_ddd_boundaries`.

Development is contract-backed UI-first, not mock-first: establish the shared Experience Platform and versioned route/API/schema examples, generate mocks and clients from the same contracts, then replace the mock adapter context by context with a real vertical slice. A static screen, Penpot frame or mock-only browser flow never proves domain/API/persistence readiness. The high-level dependency sequence and S00–S06 acceptance vocabulary are in `docs/architecture/development-operating-model.md`; they do not authorize a detailed plan or prompt pack.

## 5. Change and Git discipline

- Make the smallest complete change that satisfies the requested behavior and named requirements.
- Preserve foreign or unrelated worktree changes. Each task owns only files/hunks it intentionally creates or modifies.
- Default branch is protected `main`. Product implementation uses one short-lived `codex/<workstream>-<iteration>` branch, required PR checks and squash merge; `develop`, long-lived context branches and per-stage branches are forbidden.
- Do not create a branch, worktree, stash, temporary checkout or auxiliary coordination folder unless the user request or an accepted workstream explicitly authorizes implementation under that workflow. Repository policy alone is not side-effect authority for a read-only task.
- Never push directly to protected `main`, bypass required checks, force-push or delete branch protection.
- Never infer commit, push, PR, merge, release, deploy, or production authority from implementation authority.
- Do not use destructive Git commands without explicit narrow authorization.
- Never use broad staging commands for a mixed checkout. Stage explicit owned paths and inspect `git diff --cached --name-status` before a commit.
- If a mixed file cannot be safely separated by hunk, report that exact file as a blocker.
- File manifests must distinguish `created`, `modified`, `deleted`, `outside_expected_paths`, foreign exclusions, and mixed-file limitations.

## 6. Contract impact

For non-trivial work, classify every applicable dimension as `none`, `compatible-change`, `breaking-change`, or `unknown`:

- public API and stable error/status behavior;
- ports and boundary interfaces;
- DTO/event/artifact schemas;
- PostgreSQL and artifact persistence schemas;
- configuration/defaults/feature policies;
- request hash, cache key, dedupe, identity, and idempotency semantics;
- service-call auth, timeout, retry, fallback, and degradation semantics;
- external side-effect unknown-state reconciliation;
- logs, metrics, traces, audit, ledgers, reports, and redaction;
- alert/runbook triggers;
- browser-visible defaults and behavior;
- benchmark, rollout, migration, and rollback gates.

A `breaking-change` requires migration/deprecation, compatibility window or coordinated cutover, rollback/recovery, tests, docs, and rollout evidence. `unknown` names the missing evidence and decision owner. Do not call a semantics change `none` because field names stayed the same.

## 7. Skill resolution and routing

Skills are conditional procedures, not a preload checklist. Select the narrowest primary workflow and add companions only when their boundary is triggered. Use exact skill frontmatter names. Resolve aliases/deprecations/conflicts through the global canonical skill catalog and follow its `effective_path`; repository policy and explicit user constraints still win.

### 7.1 Core engineering and delivery

| Trigger | Skill | Boundary |
|---|---|---|
| New target architecture, boundaries, ports/adapters, service integration, ADR, phased migration | `architecture-design` | Designs target state; does not execute a prompt pack. |
| Read-only architecture/plan/docs-code drift review | `architecture-review` | Terminal reviewer; no edits. |
| Compatibility or rollout semantics across contracts | `contract-impact-analysis` | Read-only classification and migration consequences. |
| Concrete bug, regression, failing test, stack trace, flaky defect | `root-cause-debugging` | Reproduce/localize hypothesis before fix; diagnosis-only requests remain read-only. |
| Branch/diff/PR production-risk review | `production-risk-review` | Review only; no implementation. |
| Python lint/type/test/CI-equivalent gates | `backend-quality-gates` | Focused gates first; classify failures. |
| Backend speed, memory, latency, throughput, allocation, CPU/JIT claim | `backend-performance-evidence` | Requires comparable baseline and profiling evidence. |
| NumPy-heavy CPU kernel with justified JIT | `numba` | Use only after measurement; not for orchestration/I/O/GPU. |
| Browser-visible QA, screenshots, console/network, responsive/a11y smoke | `browser-qa-evidence` | Real browser evidence; does not imply overall ship readiness. |
| Terminal-driven browser automation | `playwright` | Use the pinned wrapper; do not create tests unless requested. |
| In-app browser session or signed-in UI state is specifically useful | `browser:control-in-app-browser` | Interactive browser control; prefer APIs/connectors for semantic operations. |
| Release/PR handoff readiness without publishing | `pre-ship-gate` | Review-only readiness verdict. |
| Create/rewrite/audit prompt, prompt pack, template, agent instructions, skill routing | `prompt-manager` | Produces artifacts; never executes them. |
| Execute or inspect an existing linked plan/pack/ledger | `staged-plan-runner` | Runs only the ledger-allowed stage/mode. |
| UI/UX architecture, hierarchy, typography, accessibility, responsive interaction | `ui-ux-pro-max` | Advisory; blueprint and product design system remain authoritative. |

### 7.2 Data, research, and artifact production

| Trigger | Skill | Boundary |
|---|---|---|
| Business-facing dataset analysis, KPI/inference/forecast methodology | `data-analytics-methodology` | Use for analytical conclusions, not mechanical conversion. |
| TDA/Mapper/persistent homology request | `topological-data-analysis` | Product implementation is blocked by `NON-GOAL-004` unless blueprint scope changes; research-only use must be explicit. |
| Current public discourse/trends in a recent window | `last30days` | Cited current research; not a substitute for blueprint authority. |
| Interactive plots, labs, maps, simulations, comparisons | `visualize:visualize` | In-conversation visualization, not production UI code. |
| New/edit raster image asset | `imagegen` | Bitmap generation/editing; not diagrams or repo-native SVG. |
| Word/Google Docs-targeted document artifact | `documents:documents` | Render and visually verify the document. |
| PDF reading/creation/layout verification | `pdf:pdf` | Render and inspect pages. |
| PowerPoint/Google Slides deck | `presentations:Presentations` | Create/edit and verify slide artifacts. |
| Standalone XLSX/CSV/TSV creation or analysis | `spreadsheets:Spreadsheets` | File artifact workflow, not live Excel control. |
| User explicitly targets an active Excel session | `spreadsheets:excel-live-control` | Live workbook only. |
| Reusable personal template skill from Office artifacts | `template-creator:template-creator` | Template-skill authoring, not one-off artifact work. |

### 7.3 Product design and Figma

| Trigger | Skill | Boundary |
|---|---|---|
| Explicit Product Design request or routing among design workflows | `product-design:index` | Selects the narrow design workflow. |
| UX/product-flow audit | `product-design:audit` | Evidence starts with screenshots; read-only critique. |
| Visual alternatives/remixes from a brief | `product-design:ideate` | Image-based exploration. |
| Implement selected screenshot/mockup faithfully | `product-design:image-to-code` | Responsive frontend implementation from a chosen image. |
| Clone a live URL into a local frontend-only app | `product-design:url-to-code` | Live-page reproduction with scope/security limits. |
| Any Figma file-context read/write through `use_figma` | `figma:figma-use` | Mandatory prerequisite before every `use_figma` call. |
| Create a new blank Figma/FigJam/Slides file | `figma:figma-create-new-file` | Mandatory prerequisite before `create_new_file`. |
| Generate a flowchart/architecture/sequence/ERD/state/gantt/timeline in FigJam | `figma:figma-generate-diagram` | Mandatory prerequisite before diagram generation. |
| Build/update a page, modal, panel, or composed view in Figma | `figma:figma-generate-design` | Use alongside `figma:figma-use`. |
| Build/update Figma tokens, variables, component library, or component | `figma:figma-generate-library` | Use alongside `figma:figma-use`. |
| Figma Code Connect mapping | `figma:figma-code-connect` | Creates/maintains `.figma.ts`/`.figma.js`. |
| Implement Figma motion in application code | `figma:figma-implement-motion` | Design-to-code motion boundary. |
| SwiftUI/iOS/iPad Figma translation | `figma:figma-swiftui` | Use direction-specific workflow; pair with `figma-use` for code-to-design. |
| Add/edit/inspect animation in Figma context | `figma:figma-use-motion` | Use alongside `figma:figma-use`. |
| FigJam-specific file work | `figma:figma-use-figjam` | Use alongside `figma:figma-use`. |
| Figma Slides-specific file work | `figma:figma-use-slides` | Use alongside `figma:figma-use`. |

### 7.4 GitHub, platform, and meta-tooling

| Trigger | Skill | Boundary |
|---|---|---|
| General GitHub repo/issue/PR orientation | `github:github` | Read/triage first. |
| Actionable unresolved PR review comments | `github:gh-address-comments` | Inspect threads, then implement only selected fixes. |
| Failing GitHub Actions checks on a PR | `github:gh-fix-ci` | Inspect check/log evidence before an approved fix. |
| Explicit request to commit, push, and open a draft PR | `github:yeet` | Confirm scope, stage owned paths, publish intentionally. |
| OpenAI API/Codex/current model/product guidance | `openai-docs` | Official OpenAI sources only. |
| Create/update a local Codex plugin | `plugin-creator` | Do not patch managed plugin cache. |
| Create/update a Codex skill or routing contract | `skill-creator` | Skill authoring only, with validation. |
| List/install a curated or explicit GitHub skill | `skill-installer` | Do not overwrite system skills or execute downloaded code. |
| Roehub Git→CI→Mac Studio delivery | `publish-ci-deploy` | Roehub-specific; do not use for Custometry. Use an explicit Custometry delivery workflow when one exists. |
| Roehub live backtests redesign prototype | `roehub-live-redesign-prototype:backtests-live-prototype` | Out of scope for Custometry. |

The complete table exists so every currently available skill has an explicit route. It is forbidden to load them all for one task.

## 8. Agent role routing

### 8.1. Separation of responsibilities

- The machine blueprint defines **what the product must do**. Its `MUST`, `SHOULD`, `MAY`, stable IDs, and section semantics are never restated or strengthened in a role file.
- A skill defines **how to execute a triggered workflow**. Its procedure, modes, evidence contract, companions, and conflicts remain in the skill.
- This file defines **repository-wide policy and the complete conditional skill router**.
- `.codex/agents/*.toml` defines **when to select one role, what it owns, which task-local skill routes apply, and where it stops or hands off**.

Role files are overlays, not mini-blueprints or mini-skills. They cite machine-blueprint sections and exact task-relevant IDs, then follow those sources without paraphrasing normative force. `skills.config` only enables or disables inherited skills; it is not a workflow router and does not guarantee invocation.

### 8.2. Required role contract

Every custom-agent profile must use only fields supported by the current Codex custom-agent schema. Language behavior belongs in `developer_instructions` or this file, not in invented TOML keys.

Each `description` states both `Use for ...` and `Do not use for ...` so selection can happen before the role starts. Each `developer_instructions` defines, in this order:

1. authority and user-facing language;
2. allowed modes and side-effect boundary;
3. owned decisions and explicit non-ownership;
4. minimal authoritative inputs and blueprint anchors;
5. role-local skill triggers, using exact skill names;
6. required output and nearest proof boundary;
7. `complete`, `partial`, and `blocked` conditions;
8. stop, escalation, and role-to-role handoff.

The role-local skill list is a conditional routing overlay, not a closed whitelist and not a preload list. Section 7 remains the complete router. Select one narrow primary workflow for the assignment; add companions only when their own trigger is present. A role must not execute an adjacent workflow merely because the corresponding skill is available.

Every non-trivial role result reports `status`, `mode`, owned scope, exact requirement IDs addressed, output or changes, contract impact, checks/evidence, unverified boundaries, and next handoff. `next_owner` names exactly one role or executor identifier; later downstream owners belong in the handoff context, not in that field. Status semantics are uniform: `complete` means the authorized role-owned deliverable and its declared proof boundary are satisfied; `partial` means useful scoped work exists but a required downstream owner or evidence boundary remains; `blocked` means missing authority, source truth, prerequisite, ownership decision, or safe proof boundary prevents the requested role-owned result. `inspect`, `review`, and `gate` do not authorize fixes. `design`, `implement`, `create`, `update`, `fix`, migration execution, publish, release, and deploy require authority from the user or the active accepted stage.

### 8.3. Role ownership and handoff

| Role | Select for / owns | Route away |
|---|---|---|
| `architect` | Target boundaries, dependency direction, cross-domain contracts, ADRs, phased migration | Terminal review to `architecture-review`; implementation to the owning engineer; accepted prompt authoring to `prompt_manager` only when requested |
| `backend_engineer` | API, domain/application services, control-plane persistence, shared execution semantics, schema-migration content | Data semantics to `data_engineer`; forecasting semantics to `ml_engineer`; browser surface to `frontend_engineer`; runtime rollout to `devops_engineer`; independent evidence to `qa_engineer` |
| `data_engineer` | Connectors, semantic data, ingestion, artifacts, DQ, marts, grain, lineage, source consistency | Generic API/control-plane orchestration to `backend_engineer`; forecast methods/registry semantics to `ml_engineer`; runtime rollout to `devops_engineer`; independent evidence to `qa_engineer` |
| `frontend_engineer` | React/TypeScript surfaces, client integration, i18n and accessibility implementation | Product meaning/copy/acceptance to `product_agent`; API semantics to `backend_engineer`; independent browser/a11y acceptance to `qa_engineer` |
| `ml_engineer` | Forecast series/features, model adapters, temporal evaluation, registry semantics, prediction and monitoring | Canonical source/mart/DQ inputs to `data_engineer`; API/repository adapters to `backend_engineer`; worker/runtime operation to `devops_engineer`; independent forecast evidence to `qa_engineer`; user meaning to `product_agent` |
| `qa_engineer` | Independent test strategy, invariant/contract/integration/browser/security/recovery gates and evidence | Defects to the owning implementation role; product ambiguity to `product_agent`; architecture ambiguity to `architect`; overall ship decision to `pre-ship-gate` |
| `devops_engineer` | Compose/runtime topology, migration delivery, health, observability, backup/restore and authorized release operations | Schema/domain migration content to `backend_engineer`; data/ML behavior to their owners; recovery acceptance to `qa_engineer`; topology redesign to `architect` |
| `product_agent` | Product scope, roles/journeys, capability/readiness semantics, acceptance and user-observable intent | Target architecture to `architect`; UI implementation to `frontend_engineer`; technical implementation to its owner; independent acceptance to `qa_engineer`; accepted prompt authoring to `prompt_manager` |
| `prompt_manager` | Standalone prompts and staged prompt packs from accepted intent | Unresolved architecture to `architect`; unresolved product acceptance to `product_agent`; pack execution to `staged-plan-runner`; implementation to the named executor role |

Boundary decisions are explicit: backend owns schema-migration content while DevOps owns migration-job and rollout execution; ML owns model-registry semantics while backend owns generic repository/API adapters; product defines accessibility intent, frontend implements it, and QA verifies it independently; data owns canonical inputs and artifacts while ML owns forecast methodology and lifecycle.

Use subagents for concrete independent subtasks. Exactly one cold read-only reviewer is used for architecture, plans, prompts, agent instructions, or routing artifacts when the environment permits. The reviewer does not edit or spawn another review; the author fixes findings and performs local follow-up.

## 9. Staged plans and prompt packs

A runnable staged workstream has exactly three linked durable execution sources:

1. `plan_doc` — what, why, target state, phases, rollback, proof boundaries;
2. `prompt_pack_dir` — one self-contained executor prompt per stage under `.codex/agents/generated/<pack-slug>/`;
3. `stage_ledger` — current stage, status, evidence, blocker, contract impact, file manifest, and handoff under the plan's `*-stage-reports/` directory.

Do not create `GOAL.md`, a second ledger, a chat-derived state file, or another coordination source unless the user explicitly requests it.

Execution modes:

- `manual_sequential`: execute one requested or next allowed stage and stop;
- `goal_driven`: continue only while the ledger explicitly permits the next stage; stop on `blocked`, `completed`, missing evidence/artifact, or required approval.

Stage statuses are `pending`, `in_progress`, `accepted`, `blocked`, `skipped`, or `superseded`. Only `accepted` (or an explicit supersession relation) may unlock its dependent stage.

Every stage prompt declares requirement IDs, predecessor/state/hash gates, one shared branch policy for the pack, owned/foreign paths, non-goals, contract classification, validation depth, proof boundary, stop conditions, ledger-before-report update order, and next-stage rule. It must be executable without chat history or another stage prompt.

## 10. Durable and ephemeral agent artifacts

Tracked durable artifacts:

- `.codex/AGENTS.md`, `.codex/PLANS.md`;
- `.codex/agents/*.toml` role definitions;
- canonical prompt, ledger, and iteration-report templates;
- `.codex/agents/generated/**/*.md` prompt packs;
- accepted plans, ADRs, runbooks, stage ledgers, and bounded stage/iteration reports.

Never commit:

- `.codex/agents/.context/`, `.codex/tmp/`, `.codex/sessions/`;
- raw transcripts, browser state, cookies, tokens, credentials, env dumps, or provider payloads;
- runtime logs or large generated data/model artifacts;
- machine-local `*.local.*` files.

Promote stable knowledge from ephemeral state into the blueprint, an ADR, a plan/ledger, a runbook, or `.codex/PLANS.md`. Do not treat raw logs as durable project truth.

## 11. Validation and proof boundaries

Tests are a gate, not universal acceptance. Select the nearest meaningful evidence:

- pure domain logic: focused unit/property/invariant tests;
- port/adapter: contract tests and a real adapter boundary where available;
- API/use case: real request, auth/RBAC/error/DTO mapping, OpenAPI checks;
- persistence/migration: PostgreSQL integration and upgrade/downgrade evidence;
- ingestion/artifacts: real fixture/source, atomic manifest/hash/watermark evidence;
- forecasting: time-ordered leakage checks, rolling backtest, baseline comparison;
- browser: actual journey, screenshots, console/network, en/ru, responsive and a11y smoke;
- runtime/ops: Compose service health, failure/recovery, backup/restore, migration job;
- performance: comparable baseline, corpus, environment, peak memory/profile, regression threshold;
- delivery: reviewed owned scope, CI, artifact/provenance, deploy and post-deploy smoke when authorized.

Never relabel static reasoning as runtime proof, mocks as real integration, a local browser as production deployment, or tests as benchmark evidence. If a required boundary cannot be observed, report `partial` or `blocked`.

Default Python gates once implementation exists:

```bash
uv run ruff check <focused-target>
uv run pyright
uv run pytest -q <focused-target>
```

Frontend gates, Compose checks, blueprint-sync checks, localization/a11y gates, MSSQL release matrix, SBOM/provenance, recovery, and performance gates are added in the stage that creates their implementation. Do not claim them before they exist.

### 11.1. Mandatory repository quality tools

Canonical grouped commands:

```bash
uv run python -m tools.check --scope pre-commit
uv run python -m tools.check --scope local
uv run python -m tools.check --scope pre-push
uv run python -m tools.check --scope ci
uv run python -m tools.check --scope release
```

- `pre-commit`: all twelve deterministic source checks: blueprints, generated requirement/docs indexes, links, layout, staged templates/triads, profiles, DDD, contract drift, routes, i18n, and fixtures.
- `local`: `pre-commit` plus `doctor --mode static`; use for normal handoff.
- `pre-push`: `local` plus migration, Compose and browser static contracts; invoked by the push hook.
- `ci`: exact `pre-push` parity as the canonical PR/merge profile independent of developer hooks.
- `release`: CI plus required target runtime observations; missing runtime, drill, artifact or baseline is a failure, never skip-success.

Shell hooks and GitHub Actions invoke these profiles; they must not reimplement validation logic. Each tool has focused automated success/failure/unsafe-input tests and stable non-zero failure. Generators change only owned files without `--check`; CI always checks drift and never auto-commits.

| Trigger | Required direct tool (prefix `uv run python -m tools.custometry_quality.`) | Hook profiles |
|---|---|---|
| Machine/human/UI blueprint or requirement references | `generate_requirement_index --check`, `validate_blueprints` | pre-commit, local, pre-push, ci, release |
| Contributor docs tree/index | `generate_docs_index --check`, `check_docs_links` | pre-commit, local, pre-push, ci, release |
| Any Markdown/link/anchor | `check_docs_links` | pre-commit, local, pre-push, ci, release |
| App/package/tool/docs/test tree changes | `validate_repository_layout` | pre-commit, local, pre-push, ci, release |
| Plan/prompt/ledger/report template or future staged triad | `validate_staged_workstream` | pre-commit, local, pre-push, ci, release |
| `AGENTS`, role TOML, templates or skill routes | `validate_agent_profiles` | all profiles; semantic role changes also require canary |
| Setup, engine, configuration, ports, network, resources or Compose/release | `doctor` | local/pre-push/ci static; release static + target runtime |
| Generated/temp/container data deletion or disk remediation | `cleanup` dry-run; apply only as `cleanup --apply --ownership-manifest <path> --confirm DELETE-CUSTOMETRY-OWNED-PATHS` | direct trigger only; release synthetic ownership drill |
| Package imports, context boundaries or exception allowlist | `check_ddd_boundaries` | all profiles |
| OpenAPI, JSON Schema, DTO, examples, generated TS client or mocks | `check_contract_drift` | all profiles |
| Route registry, UI map, navigation or Help mapping | `validate_route_registry` | all profiles; browser proof separately when runnable |
| UI/copy/error/help locale catalogs or locale-neutral IDs | `check_i18n_parity` | all profiles |
| Fixture generator/profile/seed/schema/golden outcomes | `validate_fixture_manifest` | all profiles |
| Persistence schema or migrations | `validate_migration_lifecycle` | pre-push/ci/release static; release runtime empty/repeat/down/re-up |
| Compose, images, health, networks, volumes or runtime config | `compose_lifecycle` | pre-push/ci/release static; release disposable runtime |
| Web/API/auth/routes/docs/help/system states | `browser_smoke` | pre-push/ci/release manifest; release runtime browser |
| Dependency, base image or built OCI | `gate_sbom`, `gate_licenses` | direct artifact CI when available; release required final digest |
| Backup, restore, migration or stateful runtime | `gate_recovery` | direct integration when triggered; release fresh observed evidence |
| Hot path, resource default or benchmark corpus | `gate_performance` | direct comparable regression when triggered; release fresh threshold evidence |

Direct command semantics, proof boundaries and change-trigger groups are normative repository process documentation in `docs/architecture/tooling-gates.md`. If this matrix and implemented `--help` diverge, stop and repair the docs/tool contract in the same scoped change.

## 12. Security, privacy, and operations

- Never expose secrets, DSNs, tokens, cookies, raw PII, source snapshot tokens, or sensitive provider payloads.
- Apply workspace authorization before pagination/aggregation and re-check sensitive artifact/source access in workers.
- Keep PII classification and redaction explicit in artifacts, logs, traces, reports, and samples.
- User SQL is typed/parsed and read-only; do not concatenate SQL fragments.
- Artifact paths are platform-generated, root-normalized, and protected against traversal/symlink escape.
- External/durable side effects require target, authority, idempotency identity, retry classes, timeout, unknown-state reconciliation, audit, and rollback.
- Do not implement blind retries after an unknown result.
- Runtime changes name metrics, alerts, owners, and versioned runbooks for user-impacting failures.
- Performance claims require baseline evidence; folder names and intuition do not establish a hot path.
- The first runtime target is one selected engine on the M3 Pro. `doctor` fails on ambiguous simultaneous engine contexts; two image/cache stores are not treated as extra capacity.
- Foundation publishes only the Web ingress on loopback. PostgreSQL and Valkey have no host-published ports. An explicit occupied port fails; automatic selection is persisted and verified against the actual engine mapping.
- Web/API/data core networks remain internal and have no arbitrary egress in Foundation. Edge is not a bounded context or product microservice: it remains secretless/read-only/state-free, accepts no user-controlled upstream, attaches only to `ingress_edge` and `edge_to_web`, and MUST share no network with API/control/data services. Compose does not portably provide ingress-only networking, so Edge MAY retain ambient transport egress until a target-specific firewall/CNI-equivalent hardening stage proves otherwise. Future connector, mail and update egress are separate allowlisted adapters/zones with negative probes; attaching core services to a broad Internet-capable network is forbidden.
- Default installation pulls immutable artifacts and verifies digest/platform before migration/start. Build or pull exit `0` without the expected manifest, platform and runtime start is failure.
- Cleanup is dry-run by default, ownership-manifest bounded and post-condition checked. Never delete resources by broad name/label guesses.

## 13. UI, localization, and accessibility

- Guided and Pipeline UI compile to the same normalized specifications and execution engine.
- Keep language, format locale, timezone, dataset timezone, and currency independent.
- English is default/fallback; shipped English and Russian catalogs have full parity.
- Domain identifiers, enum values, manifests, error codes, cache keys, and audit actions are locale-neutral.
- Core journeys target WCAG 2.2 AA and include keyboard alternatives to drag-and-drop.
- Every empty/loading/degraded/forbidden/failed state explains cause and next action.
- Browser-visible claims require real browser evidence when a runnable surface exists.

## 14. Documentation continuity

Update authoritative documentation when behavior, contracts, operations, security, or user journeys change. Create a new document only for a durable decision, architecture, migration, runbook, or handoff that lacks a current home.

Blueprint changes must preserve machine/human synchronization and requirement traceability. Repository-authored engineering documentation is English by default; the Russian product blueprints and declared localized product documentation are explicit exceptions under section 0.1.

Documentation delivery follows `docs/architecture/documentation-platform.md`:

- Markdown in Git is the authoring source; MkDocs Material builds versioned local `/docs` with bundled assets and no CDN;
- Foundation fail-closed public source is only `docs-site/docs/**`; contributor `docs/**` and generated `docs/README.md` are not copied into the product image. `docs/user-guide/**` remains templates/future metadata pipeline until a tested visibility builder replaces this split;
- in-app `/help` uses the same generated permission-aware index and may merge authorized runtime Data Guides;
- `public` user/install docs may ship without workspace membership; `authenticated` operator/admin docs require server-side authorization; `internal` architecture/ADR/contracts/prompts/iteration evidence never enters the ordinary installation artifact;
- missing or invalid visibility metadata fails closed; client-side hiding is not authorization;
- docs behavior changes run `generate_docs_index --check` and `check_docs_links`; route/help changes also run `validate_route_registry`; localized navigation/content keys run `check_i18n_parity`;
- CI never auto-commits generated docs/indexes;
- a Penpot/docs screenshot is design evidence only; browser tests prove navigation/search/visibility/offline behavior.
- Use the practical metadata/proof templates in `docs/adr/adr-template.md`, `docs/contracts/architecture-document-template.md`, `docs/contracts/contract-document-template.md`, `docs/runbooks/runbook-template.md`, and `docs/user-guide/user-install-guide-template.md`; they are contributor artifacts with `visibility: internal` and `ship: false`, not plans or prompt packs.

## 15. Final reporting

Only the final user-facing completion report defaults to Russian. Durable repository reports, ledgers, prompts, evidence, and handoffs remain English unless the user explicitly requests another artifact language. For non-trivial work, the completion report covers:

- outcome and scope;
- requirements addressed;
- created/modified/deleted file manifest and foreign exclusions;
- contract-impact classification;
- checks and real-boundary evidence actually run;
- what was not verified;
- blockers, residual risks, and next executable action.

For architecture, plan, prompt-pack, agent-instruction, or skill-routing artifacts, finish with a readable cold-review receipt:

- review status and mode (`independent subagent` or accurately labeled fallback);
- review scope and verdict (`Release`, `Release after fixes`, or `Block`);
- fixed findings and local follow-up;
- residual risks and what they mean for the next step.
