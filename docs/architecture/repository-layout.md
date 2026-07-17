---
doc_id: ARCH-REPOSITORY-LAYOUT-001
title: Custometry repository and agent infrastructure layout
doc_version: 6
product_spec_version: 0.8.2-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: []
status: active
proof_boundary:
  label: repository-tree-and-coordination-contract
  exclusions: [product-runtime-readiness, release-readiness]
---

# Custometry Repository and Agent Infrastructure Layout

## Status

- decision status: `active Foundation scaffold and minimal local runtime`;
- normative specification: `custometry-technical-blueprint-ru.md`, `0.8.2-draft`;
- human-readable mirror: `custometry-technical-blueprint-human-ru.md`;
- proof boundary: structure, governance, quality-tool ownership, and the minimal Web/API/PostgreSQL Foundation runtime; no claim of ready product contexts, vertical alpha, or release.

## Goal

Establish the minimal monorepo for Phase 0 (Foundation), retaining the complete target-module map from blueprint section 25 and a runnable local health/documentation skeleton without creating the false impression that `vertical_alpha`, `public_mvp`, or `v1_target` is already implemented.

## Established decisions

1. Both blueprints remain at the repository root. Their mutual relative links do not change.
2. The literal names `apps/`, `packages/`, `plugins/`, `deploy/`, `docs/`, and `tests/` follow section 25 of the machine blueprint.
3. The literal tree is synchronized with the current section 25 in `0.8.2-draft`: `apps/worker_report/`, `packages/promotion_journal/`, `packages/chart_compiler_ts/`, `packages/report_delivery/`, and `packages/data_documentation/` are present.
4. `packages/audit/` is added as a compatible clarification: `audit` has a separate owner and owns `audit_events` in sections 17.2–17.3, although the package is omitted from the literal tree in section 25.
5. `.github/workflows/`, `tools/custometry_quality/`, `docs/runbooks/`, `docs-site/docs/`, and additional test surfaces are added as compatible clarifications required by CI, validation, operations, fail-closed public documentation, and test-pyramid requirements.
6. Frontend workspace manifests are added because the toolchain requires `pnpm` and a pinned `pnpm-lock.yaml`; `packages/chart_compiler_ts/` is included in `pnpm-workspace.yaml` and remains the shared Web/static compiler boundary.
7. Empty modules are reserved ownership boundaries only. A `.gitkeep` file does not imply an implementation or public contract.
8. Until `v1_target`, only a single-server topology with a local artifact filesystem is permitted. Remote workers, object storage, and Kubernetes are not introduced implicitly.
9. `.gitignore` and `.editorconfig` are added as portable hygiene and secret-state boundaries explicitly authorized by the repository-creation task.
10. `.codex/delivery/` contains only currently justified specifications,
    vertical tickets, and compact terminal evidence. It is not a standing
    program-plan registry.

## Alternatives considered

| Alternative | Benefits | Drawbacks | Decision |
|---|---|---|---|
| Literal section 25 tree only | Minimal assumptions | Omits explicitly required audit ownership, pnpm lock, CI, runbooks, and test surfaces | Rejected |
| Section 25 plus documented implied paths | Preserves normative names and makes mandatory acceptance surfaces visible | Requires additions to be distinguished explicitly from the literal tree | Selected |

The second alternative is selected: every addition has a source rationale but is not presented as an implemented runtime contract.

## Dependency direction

- `apps/*` contains composition roots, transport, and process entrypoints;
- `packages/*` contains domain/application boundaries and their owned ports;
- adapters implement ports and are wired in a composition root;
- domain/application code does not import FastAPI, Celery, a concrete database driver, or filesystem implementation details;
- cross-domain reads of private tables are prohibited; interaction uses an explicit contract or repository;
- `plugins/*` is trusted server-side code with a versioned compatibility contract.

## Product structure

```text
apps/
  api/ scheduler/ orchestrator/ outbox_dispatcher/ reconciler/
  worker_data/ worker_ml/ worker_report/ web/
packages/
  contracts/ identity_access/ connection_catalog/ semantic_model/
  promotion_journal/ ingestion/ execution/ artifacts/ data_quality/
  analytics_core/ analytics_customer/ analytics_sales/
  forecasting/ presentation/ chart_compiler_ts/ report_delivery/
  data_documentation/ notifications/ localization/ plugin_sdk/
  audit/                         # clarification from the ownership map
plugins/
  connector_postgresql/ connector_mssql/ connector_files/ example_node/
migrations/
  versions/                     # versioned database revisions
deploy/
  compose/ examples/
tools/
  custometry_quality/            # importable validators, generators, and gates
docs/
  architecture/                # accepted system and engineering decisions
  adr/ contracts/ user-guide/ runbooks/ iterations/
docs-site/docs/                   # current public-only MkDocs source
tests/
  unit/ contract/ integration/ golden/ e2e/ performance/
  security/ recovery/ localization/ accessibility/
```

The complete domain ownership matrix is in [bounded-context-map.md](./bounded-context-map.md). `apps/*` contains process composition roots; `packages/*` owns domain/application code and ports; `tools/*` provides contributor validation and is not imported by the product domain.

## Agent coordination structure

```text
AGENTS.md                       # standard discovery point
.codex/
  AGENTS.md                    # compact repository routing map
  agents/
    *.toml                     # roles; do not duplicate product or skill procedure
    spec_template.md
    ticket_template.md          # one ready ticket = one execution unit
    iteration_report_template.md
  delivery/
    specs/                     # only when behavior or proof seam is unresolved
    tickets/                   # current delivery frontier and execution state
    evidence/                  # ticket-local durable evidence
docs/iterations/               # standalone bounded reports only
```

A ticket is the sole repository-local execution-state source for its execution
unit. Goal mode is optional runtime orchestration, not a file-backed source of
truth. Raw `.codex/agents/.context/`,
`.codex/tmp/`, `.codex/sessions/`, logs, and secrets are not committed.

### Separation of agent layers

| Layer | Sole responsibility |
|---|---|
| Machine blueprint | Defines what the product must implement, including the exact `MUST` / `SHOULD` / `MAY` modality and stable requirement IDs |
| Skill | Defines the procedure for a specific type of work and its evidence boundary |
| `.codex/AGENTS.md` | Defines repository policy, the complete central skill trigger router, and shared role responsibility/handoff boundaries |
| `.codex/agents/*.toml` | Defines when to select or not select a role, its decision and change scope, role-local skill routes, mandatory inputs, output, evidence, stop conditions, and handoff |

A TOML profile is a role overlay, not a mini-blueprint or mini-skill. It refers to exact machine-blueprint sections and IDs but does not restate normative requirements or change their force. `skills.config` only enables or disables an inherited skill and does not mean the skill must be selected or invoked.

All nine profiles use the common result `complete | partial | blocked` and
exactly one `handoff_to`/next executor. A role profile selects expertise and
handoff boundaries; it does not create delivery authority.

## Contract impact

| Surface | Previous contract | New contract | Consumers/evidence | Classification | Migration/rollback | Verification | Unknowns |
|---|---|---|---|---|---|---|---|
| Public API / errors | absent | Foundation `/health/live`, `/health/ready`, `/version`, OpenAPI only | FastAPI composition root | `compatible-change` | version before external consumer | focused API tests + runtime smoke required | not a product API |
| Ports / interfaces | absent | health/readiness port, loopback Web ingress, reserved domain ports | API/Web/Compose contracts | `compatible-change` | preserve stable health semantics or version | contract/static/runtime checks | dynamic-port runtime proof required |
| DTO / event / artifact schemas | absent | Foundation health OpenAPI + JSON Schema + generated TypeScript client; route-registry JSON Schema | API/Web contract consumers | `compatible-change` | version before external consumer; semantic drift fails closed | provider OpenAPI equality + bound JSON Schema semantics + generated-client byte match | domain events and artifact schemas are still absent |
| Persisted schema / migrations | absent | Foundation `platform_metadata` Alembic revision | control PostgreSQL | `compatible-change` | supported downgrade/re-upgrade before product state | migration static + runtime lifecycle | no domain tables |
| Config / defaults / feature policies | absent | locked uv/pnpm, core/demo/migration Compose, loopback dynamic ingress, internal networks | manifests, policy, and bootstrap | `compatible-change` | `.runtime.env` is ignored and regenerable; volumes are preserved | parser/lock/Compose/tool gates | release-image publication remains separate |
| Request hash / cache / identity / idempotency | absent | absent | implementation files are absent | `none` | N/A | file inventory | none |
| Service auth / timeout / retry / errors | absent | unauthenticated Foundation health only; dependency timeout/readiness code | API health boundary | `compatible-change` | add authentication before product routes | focused API + browser/Compose smoke | product authentication not implemented |
| External effects / unknown-state reconciliation | absent | absent | no runtime/external call | `none` | N/A | scope review | none |
| Logs / metrics / traces / audit / redaction | absent | governance/redaction policy + bounded container logs | `.codex/AGENTS.md`, Compose logging | `compatible-change` | version before operational consumers | static review | metrics, traces, and audit runtime not implemented |
| Agent delivery semantics | static program plans, generated stage packs, and ledgers duplicated execution state | Global Delivery Contract v1 plus repository-local specs, vertical tickets, and compact terminal evidence | `.codex/AGENTS.md`, `.codex/delivery/**` | `breaking-change` for obsolete agent workflow; product behavior `none` | old artifacts and validators are removed; Git history retains provenance | delivery-contract/ticket validators + focused tests + cold review | Goal scheduling remains external |
| Agent role selection / routing | draft profiles contained unsupported language fields and mixed product, workflow, and role policy | nine schema-valid role overlays with one common contract, a central skill router, and explicit handoffs | `.codex/AGENTS.md`, `.codex/agents/*.toml` | `compatible-change` | revert profiles only before the first dependent agent workflow; after that, role-name compatibility is required | `codex doctor` + 18 read-only spawn canaries + cold review | custom-role child persistence in Codex 0.144.2 |
| Alerts / runbooks | absent | versioned runbook contract/template | `docs/runbooks/` | `compatible-change` | add a responsible role and trigger with the runtime feature | link/metadata checks | alert thresholds intentionally absent |
| Browser-visible behavior | absent | Foundation shell, version/status, local public documentation link | React/Web image | `compatible-change` | version routes/copy before stable release | unit + browser runtime required | full Experience Platform not implemented |
| Benchmark / rollout gates | absent | tested quality CLIs, evidence schemas, and grouped profiles | `tools/custometry_quality`, tests | `compatible-change` | version tool contracts and fixtures | tooling tests + grouped profiles | release evidence must be fresh and observed |
| Git / coordination | remote-only initial commit | local `main` tracks `origin/main`; durable/ephemeral policy added | Git status/remote and `.gitignore` | `compatible-change` | remove uncommitted scaffold | Git inspection | commit/push not authorized |

Rollback for unused reserved modules means removing the additions before the
first consumer exists. Foundation runtime state is rolled back only through a
documented migration-, image-, and volume-aware procedure; deleting a
directory is no longer sufficient rollback.

## Scaffold validation

- Git tracks `origin/main`, and the existing remote `LICENSE` is preserved.
- The section 25 tree and explicitly documented implied paths are present.
- `pyproject.toml`, `package.json`, `pnpm-workspace.yaml`, `mkdocs.yml`, and `compose.yaml` pass syntax and static-contract validation.
- The spec, ticket, and evidence templates use `spec_version: 0.8.2-draft` and pass structural validation.
- Nine role TOML files use only the supported fields `name`, `description`, and `developer_instructions`; `codex doctor` reports no malformed-role warnings.
- Foundation health, documentation, API, browser, and Compose boundaries require actual runtime evidence. Compose establishes `edge_to_web` and `web_to_api` without direct Edge-to-API adjacency, but does not prove strict Edge outbound denial; that is a separate target firewall/CNI hardening gate. Product analytics, authentication, execution, deployment, recovery, and performance readiness do not follow from the scaffold.
- Repository-local `.pnpm-store/` and `.playwright-cli/` are manifest-owned disposable tool state: they count against the owned-disk budget, are excluded from Git and the Docker context, and may be deleted only by the exact confirmed cleanup command.

The canonical machine check for the tree is:

```bash
uv run python -m tools.custometry_quality.validate_repository_layout
```

It validates blueprint-owned literal paths and documented extensions. The manual list in this document remains explanatory and is not an alternative parser source.

## Residual risks

- The presence of `.github/workflows/` and quality tools does not prove actual protected-`main` configuration or a successful GitHub-hosted run; that requires remote repository evidence.
- In Codex 0.144.2, a non-empty custom-role TOML loses inherited `ephemeral=true` on role reload: canary children persist only in local `~/.codex` state/session storage. The filesystem remained read-only, network access restricted, and approval policy `never`; the repository and external systems were unchanged. Adding unsupported `ephemeral` to TOML is prohibited.
- Local development activates the exact `.node-version`/`.nvmrc`, Corepack
  `packageManager`, and `.uv-version` pins through
  `scripts/activate-toolchain.sh`; the activation fails instead of silently
  accepting a different globally active tool. Git hooks invoke the same
  activation through `scripts/run-hook-profile.sh`, so GUI-launched Git does
  not inherit an incompatible ambient Node or pnpm selection.
- Foundation Compose is a local development skeleton, not a production topology or a proven release artifact.
- `OPEN-007` and `OPEN-008` remain unresolved product decisions, not scaffold defaults.
