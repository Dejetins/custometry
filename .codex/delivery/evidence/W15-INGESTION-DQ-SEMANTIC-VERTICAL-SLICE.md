---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.10.0-draft
ticket_id: W15-INGESTION-DQ-SEMANTIC-VERTICAL-SLICE
proof_boundary: retail-source-to-immutable-artifact-dq-and-semantic-publication
proof_skills: [backend-quality-gates]
verdict: passed
redaction: Runtime database and source passwords remained file-backed and were never printed; no DSN, source row, raw PII, environment dump, snapshot token, absolute temporary artifact path, or provider payload is retained. Evidence records only safe loopback boundaries, bounded counts, hashes, stable error codes, commands, and repository paths.
executed_checks:
  - git fetch origin --prune and verify origin/main 68ad124ac6c7400c67df8bdd75752fe1bd350e76, accepted W14 ticket, passed W14 evidence, and clean W15 allowed paths
  - compare the authorized source W15 ticket read-only and restore only spec_version 0.10.0-draft, status ready, and blockers []
  - uv lock
  - uv sync --locked --all-packages --all-groups
  - uv run ruff check packages/artifacts packages/contracts/data_pipeline packages/data_quality packages/execution packages/ingestion packages/semantic_model apps/worker_data migrations/versions/0005_data_pipeline.py tests/unit/data_pipeline tests/contract/data_pipeline tests/integration/data_pipeline
  - run W15 focused unit, contract, and real PostgreSQL/filesystem integration tests against the owned development runtime
  - uv run --locked --package custometry-api pytest -q tests/contract/source_intake tests/integration/source_intake tests/unit/data_pipeline tests/contract/data_pipeline tests/integration/data_pipeline -rs
  - uv run --locked python -m tools.custometry_quality.validate_migration_lifecycle --mode runtime
  - uv run python -m tools.custometry_quality.check_ddd_boundaries
  - uv run python -m tools.custometry_quality.check_contract_drift
  - uv run python -m tools.custometry_quality.validate_fixture_manifest
  - uv run python -m tools.custometry_quality.validate_delivery_tickets
  - uv run python -m tools.custometry_quality.validate_delivery_contract
  - source scripts/activate-toolchain.sh and uv run --locked python -m tools.check --scope local
  - git diff --check
observations:
  - W14 remains accepted with verdict passed and origin/main is the independently fetched handoff revision; W15-owned paths had no foreign or mixed overlap before execution.
  - Sixteen focused W15 tests passed, including atomic Parquet commit and retry identity, DQ pass/fail/active-waiver/expired-waiver/revoked-waiver/non-waivable boundaries, semantic publication impact, a single shared extraction session, forced crash recovery, stale fencing rejection, and expired-session non-publication.
  - The combined W14 plus W15 regression passed 28 tests against real loopback PostgreSQL control and deterministic retail source boundaries.
  - Real extraction observed 1000 Customer, 5000 Receipt, 15000 ReceiptItem, and 120 Product rows and committed four content-verified Parquet files under generated relative object paths.
  - The deterministic source has five known missing product references; without a waiver the required DQ gate persisted failed evidence and no watermark or semantic version, while an active scoped waiver produced passed_with_waivers and degraded product/basket capabilities with an explicit impact count.
  - A forced crash after four filesystem commits and before the PostgreSQL commit left zero manifest, watermark, semantic, or outbox rows; retry reused identical content hashes and artifact identities, advanced the attempt/fencing token to 2, and committed once.
  - An expired repeatable-read extraction session and a stale fencing token both failed closed before artifact, watermark, semantic, or terminal-success publication.
  - Artifact manifest rows, DQ report, semantic dataset version, watermark, batch state, and semantic_dataset.published outbox intent committed in one PostgreSQL transaction under the current fencing token.
  - Runtime migration lifecycle observed upgrade_empty, upgrade_repeat, downgrade, and reupgrade across five revisions; the development control database reported 0005_data_pipeline as head.
  - Ruff, DDD boundaries, contract drift, fixture manifest, ticket/contract validators, grouped local gate, and whitespace checks passed.
  - "Contract impact is compatible-change: additive internal data-pipeline ports and error envelope, additive pyarrow dependency, generated relative artifact identity, and additive PostgreSQL revision 0005; no public HTTP API, existing DTO, config default, route, cache key, or persisted W14 identity was removed or redefined."
  - A standalone canonical pyright diagnostic remains red only in unchanged tools/custometry_quality/validate_delivery_tickets.py and tools/custometry_quality/validate_route_registry.py; it is unrelated pre-existing evidence outside W15 allowed paths and is not a declared W15 or local-profile gate.
  - Foreign UI, blueprint, UI-program, route-contract, and documentation changes remained outside W15 ownership and were neither edited nor staged by this execution unit.
---

# W15 Ingestion, DQ, and Semantic Vertical Slice Evidence

## Outcome and scope

- outcome: one deterministic retail snapshot now moves through a single
  repeatable-read session into four atomic immutable Parquet artifacts, required
  Data Quality evidence, and a published Customer/Receipt/ReceiptItem/Product
  semantic dataset; watermark and outbox advance only with the successful
  PostgreSQL commit;
- requirement IDs: [UC-002, UC-003, INGEST-001, INGEST-002, INGEST-003,
  INGEST-004, INGEST-005, INGEST-006, INGEST-007];
- included: Artifact Lifecycle, Ingestion, Data Quality, Semantic Model and
  Execution Control owner contexts, worker composition, revision
  `0005_data_pipeline`, local Parquet, failure/retry/fencing/session evidence,
  and W14 connector regression;
- exclusions: no analytics, forecasting, remote/object storage, API/Web/UI,
  browser, production deployment, recovery drill, performance, release, W16,
  or W17 claim.

## Commands and observations

| Command or action | Result | Redacted observation / durable reference |
|---|---|---|
| W15 focused Ruff command | pass | All W15 production, migration, and test paths clean. |
| W15 focused unit/contract/real integration | pass | 16 tests passed; real PostgreSQL and filesystem boundaries observed. |
| `uv run --locked --package custometry-api pytest -q tests/contract/source_intake tests/integration/source_intake tests/unit/data_pipeline tests/contract/data_pipeline tests/integration/data_pipeline -rs` | pass | 28 W14+W15 tests passed. |
| `uv run --locked python -m tools.custometry_quality.validate_migration_lifecycle --mode runtime` | pass | Five-revision graph; all four disposable lifecycle steps observed. |
| `uv run python -m tools.custometry_quality.check_ddd_boundaries` | pass | 22 contexts and explicit composition-root dependency direction. |
| `uv run python -m tools.custometry_quality.check_contract_drift` | pass | Existing registered contract sources remain synchronized. |
| `source scripts/activate-toolchain.sh && uv run --locked python -m tools.check --scope local` | pass | Canonical bounded-handoff profile passed. |
| `git diff --check` | pass | No whitespace errors. |

## Contract impact

`compatible-change`: new internal data-pipeline ports/projections, a stable
error envelope, generated relative Parquet artifact identity, `pyarrow` runtime
dependency, and additive revision `0005_data_pipeline`. The migration has a
tested downgrade and re-upgrade. Existing W14 source identities, source-intake
ports, public HTTP APIs/DTOs, configuration defaults, routes, cache keys, and
consumer behavior remain unchanged.

## Verdict

`passed` at
`retail-source-to-immutable-artifact-dq-and-semantic-publication`. The proven
boundary is disposable real PostgreSQL plus local filesystem storage. Runtime
recovery beyond the declared forced-crash path, performance, release,
production, analytics, forecast, browser, and deployment readiness remain
separate execution units.
