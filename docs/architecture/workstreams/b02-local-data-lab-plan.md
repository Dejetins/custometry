---
artifact_kind: workstream_plan
staged_schema_version: 1
workstream_id: B02
plan_maturity: initial
program_plan: docs/architecture/program/custometry-program-plan.md
module_definition: docs/architecture/workstreams/b02-local-data-lab-module.md
plan_doc: docs/architecture/workstreams/b02-local-data-lab-plan.md
prompt_pack_dir: .codex/agents/generated/b02-local-data-lab
stage_ledger: docs/architecture/workstreams/b02-local-data-lab-stage-reports/b02-local-data-lab-stage-ledger.md
execution_mode: goal_driven
hard_dependencies: [W00]
soft_dependencies: [B01]
stage_ids: [S00, S01, S02, S03, S04, S05, S06]
release_milestones: [product_foundation, vertical_alpha, public_mvp, v1_target]
spec_version: 0.8.2-draft
requirement_ids:
  - JOURNEY-001
  - GAP-019
  - TEST-INV-009
  - TEST-INV-010
  - TEST-INV-011
  - TEST-INV-012
  - TEST-INV-013
  - TEST-INV-016
  - TEST-INV-026
  - TEST-INV-028
  - TEST-INV-031
  - TEST-INV-033
  - TEST-INV-040
  - AC-014
  - AC-016
  - AC-021
  - AC-022
---

# B02 Local Data Lab — Plan

## Identity and authority

- program/workstream: `custometry-v1 / B02`;
- accepted authority: the normative product blueprint, the canonical program
  plan, the B02 module definition, and the W00 accepted runtime baseline;
- owner roles: Data Platform for fixture contracts and PostgreSQL adapters,
  Platform Engineering for Compose lifecycle, Documentation for local guides,
  and Quality Engineering for independent evidence;
- current proof boundary: repository declarations exist, but no B02 stage has
  been accepted and no fresh B02 runtime proof is attached;
- activation rule: this ledger remains dormant until W00 is accepted, the user
  authorizes B02, and the exact trio is registered as active in
  `.codex/PLANS.md`;
- branch rule: one short-lived `codex/b02-local-data-lab` branch for the whole
  workstream unless the user explicitly authorizes another workflow;
- execution rule: one canonical stage at a time, with validation and ledger
  update before handoff.

## Objective and non-goals

Deliver a reproducible local data laboratory with separate control and source
PostgreSQL services, deterministic profile generation, safe reset and migration
lifecycle, versioned golden manifests, direct scenario witnesses, and fresh
real-boundary evidence. The result must let later workstreams build against
stable synthetic data without confusing mocks or source declarations with
accepted runtime behavior.

Non-goals:

- implementing customer, analytics, forecasting, promotion, report, or
  operations business logic;
- loading real customer or company data;
- defining a production backup/restore system owned by B12;
- claiming benchmark SLOs before measured target-host baselines;
- exposing a public fixture-management API;
- changing the canonical Penpot file;
- completing first-admin, workspace, or authorization behavior owned by later
  workstreams.

## Current-state fact ledger

| Type | Fact, assumption, proposal, or unknown | Source/evidence | Consequence |
|---|---|---|---|
| Fact | Compose declares separate `control-db` and `demo-source-db` services, volumes, credentials, and internal networks. | `compose.yaml` | S03 verifies rather than redesigns this boundary without evidence. |
| Fact | `smoke`, `demo`, and `benchmark` manifests use seed `20260716`; benchmark is opt-in and marked unverified. | `deploy/demo-source/profiles/*.json` | Profile identity and opt-in behavior are explicit contracts. |
| Fact | The demo golden manifest commits counts, KPIs, scenario names, and evidence SHA-256. | `tests/golden/retail-demo-manifest.json` | Drift must fail closed in tests and runtime proof. |
| Fact | Reset targets only the persisted installation-owned demo volume and checks Compose labels. | `deploy/compose/bootstrap.sh` | S03/S05 must test refusal and successful reset paths. |
| Fact | Foundation currently has one Alembic migration containing only platform metadata. | `migrations/versions/0001_foundation_metadata.py` | B02 builds a lifecycle harness but does not absorb future context schema ownership. |
| Assumption | W00 will freeze reproducible Node, pnpm, uv, Docker, and M3 Pro Foundation evidence before B02 activation. | program dependency | Missing W00 acceptance keeps the ledger dormant. |
| Proposal | `smoke` is the fast default lifecycle profile, while `demo` remains an explicit product-data option. | B02 design | S01 must confirm CLI and onboarding-consumer wording before implementation. |
| Unknown | Benchmark generation time, disk, RSS, and developer-machine feasibility are not yet measured. | no accepted evidence | Benchmark remains opt-in and blocks any unsupported milestone claim. |
| Unknown | Later consumers may require more golden scenarios than the current schema exposes. | blueprint golden dataset list | Add versioned scenarios without silently changing accepted meanings. |

## Dependencies and milestones

| Dependency | Type | Required state/evidence | Failure behavior |
|---|---|---|---|
| `W00` | hard | accepted repository/runtime Foundation, reproducible tool activation, healthy Docker engine contract, and M3 Pro proof | keep every B02 stage non-executable in the ledger |
| `B01` | soft | stable local docs shell and optional demo-data presentation contract | core lab proceeds; browser/docs integration uses a bounded fallback and records the missing consumer |

Release contribution:

- `product_foundation`: deterministic local development and acceptance data;
- `vertical_alpha`: stable demo data for the first end-to-end slice;
- `public_mvp`: clean-install golden verification and documented local use;
- `v1_target`: accepted benchmark profile evidence and the extended golden
  family required by all product contexts.

## Requirement allocation

| Requirement IDs | Owning stage | Acceptance evidence |
|---|---|---|
| `JOURNEY-001`, `AC-014` | `S01`, `S04`, `S05` | optional demo-data consumer contract, local guide, and clean Compose proof |
| `TEST-INV-009`, `TEST-INV-033` | `S01`–`S03` | incomplete-period, leap-day, ISO-week-53, and previous-year fixtures |
| `TEST-INV-010`, `TEST-INV-011`, `AC-021` | `S02`, `S03`, `S05` | duplicate namespace and SCD overlap/gap evidence |
| `TEST-INV-012`, `TEST-INV-013`, `AC-022` | `S02`, `S03` | multi-currency and structural metric-shape input fixtures with explicit non-claim boundary |
| `TEST-INV-016`, `TEST-INV-028` | `S02`, `S03` | multi-table extraction failure/session fixtures for downstream adapter tests |
| `TEST-INV-026`, `TEST-INV-031` | `S02`, `S03` | receipt/item grain, canonical customer, and period-key fixtures |
| `TEST-INV-040`, `GAP-019` | `S01`, `S05`, `S06` | explicit benchmark resource policy, measured evidence, and honest milestone blocker |
| `AC-016` | `S02`, `S03`, `S05`, `S06` | stable counts, KPIs, scenarios, canonical hash, and clean-install evidence |

## DDD target and contracts

B02 is an infrastructure module with a framework-independent policy core:

- profile and manifest parsing are pure, versioned contracts;
- fixture generation receives all randomness, time, locale, currency, and size
  inputs explicitly;
- evidence normalization is canonical and deterministic;
- reset authorization depends on `LabInstallationIdentity`, not string
  concatenation alone;
- adapters implement PostgreSQL, Docker Compose, Alembic, and local docs;
- later bounded contexts depend on fixture contracts, not B02 importing their
  domain/application layers.

Contract classification:

| Surface | Initial classification | Compatibility rule |
|---|---|---|
| Profile JSON | `compatible-change` | optional fields only until first acceptance; seed/count/default changes become breaking |
| Fixture relational schema | `compatible-change` | additive nullable columns only; grain/key changes require version and migration |
| Golden manifest/evidence | `compatible-change` | additive scenarios require versioned verifier support; changed meaning/hash policy is breaking |
| Reset CLI | `compatible-change` | new safe flags allowed; ownership or deletion semantics are breaking |
| Compose services/networks | `compatible-change` | names and trust boundaries become stable after accepted consumer use |
| Migration harness | `compatible-change` | context schema ownership cannot move silently |
| Local docs metadata | `compatible-change` | safe descriptive additions; identifiers remain locale-neutral |
| Benchmark profile | `unknown` until S05 | no SLO or support claim without measured evidence |

## Stage plan

| Stage | Outcome | Entry gate | Exit evidence | Rollback/stop gate |
|---|---|---|---|---|
| `S00` | Freeze current facts, ownership, consumers, scenario coverage, and proof gaps. | W00 accepted; B02 activated; clean ownership review | source inventory, contract-impact map, exact file manifest, risks, and accepted scope report | unknown data owner, unsafe shared-file ownership, or missing W00 evidence blocks |
| `S01` | Freeze profile, manifest, reset, migration, benchmark-warning, docs, and optional-demo consumer contracts. | `S00 accepted` | schemas/examples, error semantics, compatibility rules, docs flow, and test plan | ambiguous defaults, destructive reset semantics, or cross-context contract conflict blocks |
| `S02` | Implement/test deterministic policy core and fixture semantics. | `S01 accepted` | pure tests for profiles, seed determinism, canonical evidence, namespaces, SCD, calendar, grain, currency, promotion, and failure scenarios | ambient randomness, unstable ordering, PII, or unversioned scenario drift blocks |
| `S03` | Complete PostgreSQL, Compose, Alembic, generator, reader, reset, and verifier adapters. | `S02 accepted` | adapter/integration tests, least-privilege grants, migration/replay checks, failure/refusal tests | unsafe deletion, mixed database ownership, non-repeatable output, or migration uncertainty blocks |
| `S04` | Integrate safe profile metadata and lifecycle guidance into local `/docs` and the optional-demo consumer contract. | `S03 accepted`; B01 contract available or bounded fallback recorded | real local docs browser flow, contract fixture, keyboard/accessibility smoke, no-secret network/console evidence | browser contract drift, hidden benchmark start, or authorization ownership leakage blocks |
| `S05` | Produce fresh real-boundary proof on the supported local host. | `S04 accepted`; Docker/runtime prerequisites healthy | clean smoke/demo install, migrations, golden hash, restart/persistence, reset/reseed, negative isolation, resource evidence, and benchmark decision | missing engine, non-golden output, secret exposure, unsafe cleanup, or unsupported resource use blocks |
| `S06` | Close traceability, documentation, rollback, and independent acceptance review. | `S05 accepted` | all requirement rows linked, cold-review blockers fixed, ledger complete, docs indexes/gates green | any unresolved required evidence, benchmark milestone gap, or documentation drift prevents completion |

## Profile and evidence contract

### `smoke`

- bounded lifecycle profile;
- current targets: 4 stores, 100 customers, 40 products, 6 promotions,
  500 receipts, and 1,000 receipt items;
- no large-data acknowledgement;
- used for migration, startup, reset, and negative-path checks.

### `demo`

- opt-in product exploration profile;
- current targets: 20 stores, 1,000 customers, 120 products, 12 promotions,
  5,000 receipts, and 15,000 receipt items;
- manifest commits UTC, EUR, grains, keys, synthetic PII classes, counts, KPIs,
  scenarios, and canonical evidence hash;
- used for golden and browser-consumer proof.

### `benchmark`

- explicit opt-in plus large-data confirmation;
- blueprint targets: 500,000 customers, 10,000,000 receipts,
  50,000,000 receipt items, 100,000 products, 1,000 stores, and 36 months;
- must support bounded generation, progress/status, cancellation or safe
  termination, cleanup, and measured resource evidence;
- remains `implemented_unverified` until S05 accepts the target-host run;
- no benchmark SLO is inferred from generator existence.

## Migration, rollback, reset, and recovery

- A new migration is exercised on an empty control database and the supported
  predecessor state.
- Failure leaves a diagnosable state and never reports readiness.
- Downgrade is proven on disposable state where the migration declares support;
  data-preserving production rollback belongs to the owning context.
- Demo-source fixture changes use a new manifest/schema version when existing
  volumes cannot be read compatibly.
- Profile changes never rewrite an initialized volume; the lifecycle requires
  an exact installation-scoped reset.
- Reset refuses unsafe project names, unlabelled volumes, mismatched Compose
  ownership, or a request outside the demo-source volume.
- Recovery proof covers restart with persisted data, explicit reset, reseed,
  re-verification, and removal of temporary evidence.
- Rollback never invokes global Docker prune, broad volume deletion, or
  host-wide PostgreSQL cleanup.

## Validation and proof boundaries

Focused gates progress from static contracts to the real boundary:

1. profile/manifest schema and deterministic pure tests;
2. SQL lint/parser and migration graph checks;
3. disposable PostgreSQL integration tests;
4. Compose configuration and negative ownership/reset tests;
5. local documentation build and browser flow;
6. clean runtime install with evidence capture;
7. cold independent review and grouped repository gates.

Expected durable evidence:

- `docs/architecture/workstreams/b02-local-data-lab-stage-reports/S00-discovery.md`;
- one report per subsequent stage in the same directory;
- machine-readable runtime receipts under a stage-owned ignored temporary
  directory until redacted summaries are committed;
- committed golden manifests and verifier output identifiers;
- command, host envelope, image digest, migration head, profile, seed,
  duration, and evidence hash in S05.

This plan does not use a green unit suite to claim PostgreSQL, Docker, browser,
benchmark, recovery, or release readiness.

## Documentation continuity

S04/S06 update the smallest applicable English sources and generated indexes:

- local developer setup and demo-data guide;
- fixture extension and golden-evidence guide;
- reset and migration runbook;
- architecture/workstream index and program traceability;
- user-facing `/docs` content for safe demo profile selection;
- Russian product documentation only when normative product meaning changes.

No internal prompt, ledger, ADR, or architecture file is shipped in the public
documentation bundle unless the documentation visibility contract explicitly
allows it.

## Risks and open decisions

| Risk/decision | Owner | Due stage | Mitigation or stop condition |
|---|---|---|---|
| Benchmark may exceed laptop time, disk, or memory. | Data Platform | `S01`, measured `S05` | explicit opt-in, resource estimate, cancellation/cleanup, no support claim without evidence |
| Golden KPIs could accidentally encode business metric semantics owned elsewhere. | Architecture + consumer owner | `S01` | keep B02 KPIs structural; downstream metrics own reconciled definitions |
| SQL generation order or PostgreSQL version could change evidence. | Data Platform | `S02` | stable ordering, pinned image, canonical serialization, explicit schema version |
| Reset could delete foreign state. | Platform Engineering | `S01`–`S03` | project-name validation, exact Compose labels, negative tests, no global cleanup |
| Migration harness could absorb context ownership. | Architecture | `S00`, `S03` | ownership table and scoped migration fixtures only |
| Local docs integration could depend on unfinished B01. | Experience Platform | `S04` | soft dependency; use existing docs shell, record deferred product onboarding UI |
| Current golden scenarios do not cover the full v1 list. | Program owner | `S00`, `S06` | assign each missing fixture to B02 or the defining consumer before milestone closure |
| Compose isolation is not production firewall proof. | Security/Operations | `S05` | state proof boundary and defer production firewall/CNI evidence |

## Change ownership

Primary owned paths:

- `deploy/demo-source/**`;
- `tests/golden/**`;
- B02-specific tests and tools under `tests/**` and
  `tools/custometry_quality/**`;
- B02 workstream plan, module, reports, prompt pack, and local documentation.

Shared paths requiring scoped-hunk review:

- `compose.yaml`;
- `deploy/compose/bootstrap.sh`;
- `migrations/**`;
- documentation indexes, runtime setup guides, and program traceability.

Foreign exclusions:

- product-domain calculations and persistence owned by B03–B13;
- B01 shell/component implementation except an explicitly agreed consumer
  integration hunk;
- production backup/restore implementation;
- CI, branch, release, or deployment policy outside B02 evidence needs;
- Penpot and design-file authority.

Mixed-file policy: stop when safe hunk separation is impossible. Preserve all
foreign changes and never stage unrelated files.

## Completion rule

B02 is complete only when:

- all non-superseded stages are terminal and the ledger is `completed`;
- every plan requirement is mapped to durable evidence;
- separate control/demo PostgreSQL, migration, profile, reset, and golden
  contracts pass fresh real-boundary proof;
- the benchmark profile has accepted target-host evidence for every milestone
  that requires it, or that milestone remains blocked;
- local documentation and consumer contracts are verified;
- cold independent review reports no unresolved blocker;
- the requirement matrix, indexes, and applicable local/CI gates pass;
- no result claims downstream analytical, production, or release readiness
  outside the B02 proof boundary.
