---
artifact_kind: module_definition
staged_schema_version: 1
doc_id: MODULE-B02-LOCAL-DATA-LAB
title: B02 Local Data Lab module definition
doc_version: 1
product_spec_version: 0.8.2-draft
visibility: internal
ship: false
workstream_id: B02
owner: data-platform
status: initial
requirement_ids: [AC-016]
proof_boundary:
  label: planned-local-data-lab-boundary
  exclusions:
    - completed-runtime-proof
    - benchmark-slo
    - production-data-migration
    - product-domain-ownership
---

# B02 Local Data Lab — module definition

> This definition establishes the reproducible local-data boundary used by
> later workstreams. It does not claim that the current Compose installation,
> migrations, generated rows, benchmark profile, or browser consumer have
> passed B02 acceptance.

## Identity and purpose

The Local Data Lab is enabling infrastructure, not a business bounded context.
It supplies deterministic, disposable, synthetic data and lifecycle tools so
that product contexts can be developed and proven against stable PostgreSQL
boundaries without treating mocks as runtime evidence.

Its responsibilities are:

- operate a dedicated control PostgreSQL database for platform metadata;
- operate a separate demo-source PostgreSQL database that behaves like an
  external retail source;
- compile deterministic `smoke`, `demo`, and `benchmark` dataset profiles from
  committed versioned inputs;
- expose safe bootstrap, reset, migration, and evidence-verification workflows;
- publish fixture manifests, golden counts, golden KPIs, scenario evidence, and
  canonical evidence hashes;
- provide synthetic data contracts for onboarding, ingestion, data-quality,
  analytics, forecasting, promotion, reporting, and operations workstreams;
- keep real customer data, production secrets, and product-domain behavior out
  of the fixture boundary.

The module has one hard dependency, `W00 Repository and Runtime Foundation`.
`B01 Experience Platform` is a soft coordination dependency for local
documentation and future optional-demo onboarding presentation.

## Ubiquitous language

| Term | Meaning | Exclusion |
|---|---|---|
| Data profile | Versioned row-count, seed, scenario, and resource envelope | An environment name |
| Control database | PostgreSQL persistence owned by the platform control plane | A source dataset |
| Demo source | Separate PostgreSQL service that imitates an external retailer | A schema inside the control database |
| Fixture manifest | Canonical declaration of profile identity, grains, keys, counts, KPIs, scenarios, and evidence hash | Runtime logs |
| Golden evidence | Canonically serialized query result matched to a committed manifest hash | A screenshot or sampled assertion |
| Seed | Explicit deterministic generator input | Ambient randomness |
| Reset | Destruction of only the exact installation-owned demo-source volume | Global Docker cleanup |
| Migration lifecycle | Upgrade, compatibility, downgrade-on-disposable-state, and clean-replay proof | An unverified migration command |
| Benchmark profile | Explicitly opted-in large dataset matching the product scale contract | A default developer dataset or an SLO claim |
| Scenario fixture | Deliberate edge case with a direct machine-verifiable witness | Undocumented anomalous rows |

## State and contract model

### `DatasetProfile`

- `schema_version`;
- stable `profile_id`: `smoke`, `demo`, or `benchmark`;
- deterministic `seed`;
- explicit row-count targets;
- explicit opt-in and large-data confirmation flags;
- declared status: implemented, implemented-unverified, or accepted;
- estimated resource class and supported host constraints.

Changing a seed, count target, scenario meaning, or default selection is a
versioned fixture-contract change. A persisted volume cannot silently switch
profile.

### `FixtureManifest`

- fixture schema version and profile identity;
- timezone and default currency;
- entity grain, primary-key, and synthetic PII classification;
- expected counts and KPIs;
- required scenario names;
- canonical evidence serialization rule;
- expected SHA-256 evidence signature.

The manifest is the acceptance authority for deterministic output. SQL seed
scripts are implementation inputs and cannot independently redefine expected
results.

### `LabInstallationIdentity`

- explicit Compose project name;
- installation-owned volume names and Compose labels;
- selected profile and large-data acknowledgement;
- local runtime state location;
- pinned container image identities;
- no host secret values in evidence.

Reset is allowed only after exact project and volume label verification.

### `MigrationScenario`

- clean upgrade from an empty control database;
- upgrade from the immediately supported predecessor;
- application compatibility during the declared window;
- downgrade on disposable test state when supported;
- failed-migration behavior and recovery evidence;
- schema version and migration head after restart.

Product contexts own their tables and semantics. B02 owns the reproducible
migration harness and Foundation-only seed metadata, not future context
migrations.

### `GoldenExpectation`

- named query or verifier;
- expected row counts and business-neutral KPIs;
- deterministic scenario witnesses;
- canonical JSON normalization;
- expected content hash;
- tolerance only where the normative metric contract explicitly permits it.

## Invariants

- Control and demo-source data remain in separate PostgreSQL services,
  credentials, databases, volumes, and internal networks.
- Demo-source credentials have a least-privilege reader distinct from the
  database owner.
- Fixture generation uses an explicit seed, UTC timestamps, declared currency,
  stable ordering, and locale-neutral identifiers.
- External identifiers are qualified by source namespace; duplicate source IDs
  across namespaces remain distinct.
- SCD fixtures expose both valid and deliberately invalid overlap/gap cases
  without making invalid rows appear production-safe.
- Returns, cancellations, missing products, anonymous receipts, late updates,
  incomplete periods, leap day, ISO week 53, multi-currency, and promotion
  overlap are directly queryable scenarios.
- Golden evidence fails closed when counts, KPI values, scenario keys,
  scenario witnesses, schema version, or canonical hash drift.
- `smoke` is bounded for fast lifecycle checks; `demo` is the normal opt-in
  product dataset; `benchmark` requires explicit large-data confirmation.
- No benchmark performance or capacity claim is accepted without measured
  target-host evidence.
- Changing a persisted profile requires a verified, installation-scoped reset;
  seed scripts never mutate an existing volume implicitly.
- All emails, loyalty identifiers, names, and other person-like values are
  synthetic and clearly non-production.

## Commands, queries, and events

| Contract | Caller | Result | Failure semantics |
|---|---|---|---|
| `BootstrapLab(profile)` | developer lifecycle tool | healthy control DB and optional demo source | fail before partial profile activation |
| `ResetDemoSource(installation)` | authorized local operator | exact owned demo volume removed | refuse on absent or mismatched ownership labels |
| `ApplyControlMigrations(target)` | migration runner | committed schema head | non-zero exit, no readiness claim |
| `GenerateProfile(profile, seed)` | demo-source initializer | deterministic relational fixture | reject unknown profile or unconfirmed benchmark |
| `CollectGoldenEvidence(profile)` | acceptance harness | canonical JSON evidence | fail on query or serialization error |
| `VerifyGoldenEvidence(manifest, evidence)` | CI/runtime verifier | matching SHA-256 and expectations | fail closed on any drift |
| `DescribeProfile(profile)` | docs/onboarding consumer | safe counts, scenarios, and resource warning | never expose secrets or host paths |

No public product API is owned by B02. If later workstreams expose these
capabilities, B02 supplies versioned ports and fixtures while the consuming
context owns authorization, HTTP semantics, and user-visible policy.

## Ports and adapters

| Port | Primary adapter | Trust boundary | Required behavior |
|---|---|---|---|
| `ProfileCatalog` | committed JSON profile files | repository input | strict schema and known-profile validation |
| `FixtureCompiler` | PostgreSQL initialization scripts | demo-source container | deterministic, idempotent only on an empty volume |
| `ControlMigrationRunner` | Alembic in the migration container | control database | explicit head, transactional behavior where supported |
| `GoldenEvidenceCollector` | read-only SQL queries | demo-source reader | stable ordering and canonical value representation |
| `GoldenEvidenceVerifier` | local Python verifier | committed manifest | strict keys, KPIs, scenarios, and SHA-256 |
| `LabLifecycle` | Compose bootstrap script | local Docker engine | explicit project identity and safe cleanup |
| `ProfileDescriptor` | local docs/onboarding contract | browser or API consumer | safe metadata only, no credentials |

PostgreSQL and Docker Compose are adapters. Dataset semantics, evidence
normalization, reset authorization, and profile rules remain testable without
embedding shell behavior in product-domain code.

## Current baseline to verify, not assume

The repository currently declares:

- pinned PostgreSQL services named `control-db` and `demo-source-db`;
- separate `control` and `demo_source` networks and separate named volumes;
- `smoke`, `demo`, and `benchmark` profile manifests with seed `20260716`;
- demo targets of 1,000 customers, 5,000 receipts, and 15,000 receipt items;
- a benchmark target of 500,000 customers, 10,000,000 receipts, and
  50,000,000 receipt items;
- a demo golden manifest with expected counts, KPIs, scenarios, and evidence
  SHA-256
  `c8fb789e32c681af5306e8d8ffe9a9681d05ba6bb974d3a02c2588185471ffc8`;
- an installation-scoped `--reset-demo-data` flow with Compose-label checks;
- an initial Alembic migration for Foundation platform metadata.

These are source facts only. B02 S05 must produce fresh runtime evidence before
they become accepted behavior.

## Fixture coverage

The minimum accepted profile family covers:

- clean ideal data and bounded smoke data;
- anonymous receipts, returns, cancellations, duplicated or late source
  behavior, and missing product references;
- multiple currencies with no implicit cross-currency total;
- duplicate IDs across source namespaces;
- SCD end dates, overlaps, gaps, and event-time selection cases;
- incomplete periods, leap day, ISO week 53, and previous-year calendar edges;
- header and item grain reconciliation inputs;
- overlapping, multi-channel, segment-snapshot, and customer-list promotions;
- additive, semi-additive, distinct, and ratio metric inputs;
- irregular and intermittent time-series inputs and short-history entities;
- low/high-cardinality, sensitive, localization, Markdown, report, XLSX,
  ChartSpec, timeline, and renderer-boundary fixtures as later consumers define
  their versioned contracts.

Later workstreams may extend fixture columns or scenarios through compatible,
versioned changes. They may not mutate an accepted scenario meaning silently.

## Data ownership, privacy, and security

- The control database contains platform metadata only.
- The demo-source database contains synthetic source-system records only.
- B02 does not ingest or copy real business data.
- Committed fixtures contain no secrets, tokens, production hostnames, or real
  direct identifiers.
- Generated credentials live in installation-local secret storage and are
  excluded from logs and evidence.
- The demo-source reader receives only the grants needed by ingestion tests.
- No database port is published to non-loopback host interfaces by default.
- Network isolation claims are limited to the Compose boundary; production
  ingress/egress enforcement remains a separate hardening concern.

## Documentation and consumer integration

B02 owns local, English-first contributor and operator documentation for:

- selecting `smoke`, `demo`, or `benchmark`;
- understanding dataset size and scenarios;
- performing an installation-scoped reset;
- collecting and verifying golden evidence;
- adding a scenario without breaking determinism;
- interpreting the explicit limits of benchmark and migration evidence.

The local documentation site may display profile metadata. Optional demo
dataset selection during first-run onboarding is a consumer contract for B01
and the later identity/workspace owner; B02 does not own bootstrap
authorization or workspace creation.

## Operations and observability

- lifecycle output identifies the profile, seed, image identity, migration
  head, database readiness, and evidence hash without secrets;
- startup and verification commands use bounded timeouts and non-zero failures;
- the benchmark profile reports resource warnings and never starts implicitly;
- runtime proof records host architecture, detected CPU/memory envelope,
  profile, duration, peak resource use where measured, and exact commands;
- restart/persistence and reset/reseed are tested separately;
- no success claim is inferred from a healthy container alone.

## Contract impact

The initial lab contract is a `compatible-change` while no accepted external
consumer exists. After acceptance:

- adding optional fixture columns or scenarios is compatible only when existing
  grains, keys, counts, and golden meanings remain stable;
- changing seed, primary keys, grains, scenario meaning, default profile,
  evidence serialization, or reset identity is a breaking change;
- changing benchmark counts requires an explicit blueprint and milestone
  decision;
- control-plane schema changes follow the owning context migration policy and
  cannot be hidden inside fixture initialization.

## Acceptance boundary

B02 is accepted only after S00–S06 provide:

- source-anchored contract and ownership review;
- versioned profile, manifest, reset, migration, and consumer contracts;
- deterministic generator and verifier tests;
- real PostgreSQL adapter and migration lifecycle checks;
- local documentation/browser integration proof;
- fresh clean-install, reset, reseed, restart, and golden-hash runtime evidence;
- explicit benchmark generation evidence or a recorded milestone blocker that
  prevents the relevant release claim;
- independent cold review, requirement traceability, rollback instructions, and
  a completed stage ledger.

The module does not accept backup/restore for the whole product, analytical
correctness of downstream contexts, forecasting accuracy, production network
hardening, or release readiness on behalf of other workstreams. Normative data
rules remain owned by B05; B02 supplies deterministic inputs and evidence that
allow B05 to prove them.
