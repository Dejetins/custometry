---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.10.0-draft
ticket_id: W14-SOURCE-CONNECTION-FILE-IMPORT-KERNEL
proof_boundary: governed-postgresql-and-template-file-source-intake
proof_skills: [backend-quality-gates, contract-impact-analysis]
verdict: passed
redaction: No database password, bootstrap or access token, cookie, DSN, source row, raw PII, environment dump, or provider payload is retained; temporary credentials were file-backed and observations contain only bounded counts, stable error codes, hashes, safe schema/object names, commands, and repository paths.
executed_checks:
  - verify HEAD 7ca2ddad35b924d4827357094e39ef7ec70189d2 contains accepted W13 merge 3ec4ef1 and passed predecessor evidence
  - record foreign working-tree changes read-only and verify W14-owned paths are safely separable before writes and before acceptance
  - reconcile the W14 source contract from 0.9.3-draft to 0.10.0-draft and narrow the requirement mapping to the PostgreSQL plus governed CSV/XLSX increment
  - source scripts/activate-toolchain.sh
  - uv lock
  - uv sync --all-packages --all-groups
  - uv run ruff format --check packages/contracts/source_intake packages/connection_catalog packages/data_documentation plugins/connector_postgresql plugins/connector_files apps/api/src/custometry_api/connections apps/api/src/custometry_api/imports tests/contract/source_intake tests/integration/source_intake
  - uv run ruff check packages/contracts/source_intake packages/connection_catalog packages/data_documentation plugins/connector_postgresql plugins/connector_files apps/api/src/custometry_api/connections apps/api/src/custometry_api/imports tests/contract/source_intake tests/integration/source_intake tests/unit/identity_access/test_policy.py
  - uv run pyright packages/contracts/source_intake packages/connection_catalog packages/data_documentation plugins/connector_postgresql plugins/connector_files apps/api/src/custometry_api/connections apps/api/src/custometry_api/imports tests/contract/source_intake tests/integration/source_intake tests/unit/identity_access/test_policy.py
  - uv run pytest -q tests/unit/identity_access/test_policy.py tests/contract/source_intake
  - run tests/integration/source_intake against disposable pinned PostgreSQL 17.5 control and deterministic demo-source containers after alembic upgrade head
  - uv run python -m tools.custometry_quality.validate_fixture_manifest
  - uv run python -m tools.custometry_quality.validate_migration_lifecycle --mode static
  - CUSTOMETRY_MIGRATION_RUN_ID=w14-final-20260824 uv run python -m tools.custometry_quality.validate_migration_lifecycle --mode runtime
  - uv run python -m tools.custometry_quality.check_ddd_boundaries
  - uv run python -m tools.custometry_quality.check_contract_drift
  - uv run python -m tools.custometry_quality.validate_delivery_tickets
  - uv run python -m tools.custometry_quality.validate_delivery_contract --contract /Users/daniildegtyarev/.codex/skills/delivery-orchestrator/references/delivery-contract-v1.md
  - uv run python -m tools.check --scope local
  - run final custometry-api:dev image import smoke read-only as UID 10001
  - git diff --check
observations:
  - W13 is accepted with passed evidence and its merge is present in the common base; the W14 ticket was made ready only after source-version, requirement-mapping, packaging, and permission-path drift was repaired.
  - The ticket maps UC-001, UC-024, CONNECTOR-002, CONNECTOR-003, CONNECTOR-004, CONNECTOR-006, and RBAC-017; it does not claim the full CONNECTOR-001 or V1-AC-026 matrix.
  - Thirteen focused unit and provider-contract tests passed; committed connection and import OpenAPI documents byte-match their independently versioned FastAPI providers.
  - Four real PostgreSQL/API integration tests passed after a clean alembic upgrade through 0004_source_intake.
  - PostgreSQL 17.5 discovery observed the deterministic retail catalog; preview masked email and loyalty-card values, and a repeatable-read read-only session returned the bounded expected 5000 receipt rows with a content hash and rejected reuse after close.
  - Quoted identifiers rejected an injection-shaped object name with SOURCE_QUERY_REJECTED while the receipts table remained discoverable; a future yandex_metrica connector was rejected before persistence.
  - Published-template-only CSV/XLSX validation observed typed parity, exact schema/sheet/header checks, bounded hashes/counts, redacted rejected-row codes, formula rejection, and no source-value echo.
  - Template/import permissions are separate from connection management; analyst creation failed closed and cross-workspace connection discovery returned NOT_FOUND without resource disclosure.
  - The deterministic demo manifest passed for seed 20260716 and 15 scenarios; no benchmark profile was activated.
  - Static migration validation passed and the final runtime lifecycle observed empty upgrade, repeated upgrade, downgrade, and re-upgrade across four revisions; the final API image imported all W14 modules read-only as UID 10001.
  - A real mount-path 404 and four cross-context DDD imports were found during proof, repaired within W14 scope, and all invalidated contract, integration, image, DDD, and lifecycle evidence was rerun to green.
  - Ruff passed, strict Pyright reported zero errors and warnings, DDD boundaries passed for 22 contexts, contract drift passed with three sources, ticket/contract validators passed, local profile passed, and whitespace validation passed.
  - "Contract impact is compatible-change: new source-intake API providers, shared ports, permissions, configuration fields, and revision 0004 are additive; source_system_id is immutable and no existing route, DTO, persisted identity, cache key, or consumer default was removed or redefined."
  - All W14 disposable integration and migration containers and temporary secret directories were absent after cleanup; the canonical lifecycle-produced local custometry-api:dev image remains only as local test output and was not pushed or deployed.
  - Foreign UI, blueprint, UI-program, W31-W37, localization, route-contract, and documentation changes were neither edited nor staged by W14; safe W14 hunk/path separation remained possible.
---

# W14 Source Connection and File Import Kernel Evidence

## Outcome and scope

- outcome: an authorized workspace can create a reference-only PostgreSQL
  connection, test and inspect a deterministic read-only source, use a bounded
  repeatable-read extraction session, and validate CSV/XLSX content only
  through a published immutable template with redacted results;
- requirement IDs: [UC-001, UC-024, CONNECTOR-002, CONNECTOR-003,
  CONNECTOR-004, CONNECTOR-006, RBAC-017];
- included: Connection Catalog and Data Documentation contexts, shared
  source-intake contracts, PostgreSQL and file adapters, additive API/config,
  revision 0004, image packaging, permissions, provider contracts, and focused
  unit/contract/real-PostgreSQL proof;
- exclusions: no MSSQL, MySQL, ClickHouse, Yandex, arbitrary SQL, W15
  immutable-artifact/ingestion/DQ/semantic processing, W16 projections, Web,
  browser, production deployment, recovery, performance, or release claim.

## Commands and observations

| Command or action | Result | Redacted observation |
|---|---|---|
| Readiness/source/foreign-change guard | pass | Accepted W13 and merge base were present; W14 source mapping and allowed packaging/policy paths were repaired; foreign paths remained disjoint. |
| `uv run pytest -q tests/unit/identity_access/test_policy.py tests/contract/source_intake` | pass | 13 unit and contract tests passed. |
| Disposable PostgreSQL 17.5 integration runner plus `uv run pytest -q tests/integration/source_intake` | pass | 4 real API tests passed against migrated control state and the deterministic demo source. |
| `uv run python -m tools.custometry_quality.validate_fixture_manifest` | pass | Demo seed `20260716`, 15 scenarios. |
| `uv run python -m tools.custometry_quality.validate_migration_lifecycle --mode static` | pass | One four-revision migration graph with a non-empty downgrade. |
| `CUSTOMETRY_MIGRATION_RUN_ID=w14-final-20260824 uv run python -m tools.custometry_quality.validate_migration_lifecycle --mode runtime` | pass | 4/4 lifecycle steps observed on disposable PostgreSQL. |
| Ruff and strict Pyright focused commands | pass | Ruff clean; Pyright 0 errors, 0 warnings. |
| `uv run python -m tools.custometry_quality.check_ddd_boundaries` | pass | 22 contexts; explicit shared actor/authorization/failure contract. |
| `uv run python -m tools.custometry_quality.check_contract_drift` | pass | Three registered contract sources remained synchronized. |
| `uv run python -m tools.check --scope local` | pass | Local grouped repository gate passed. |
| Final read-only API image import smoke | pass | W14 packages, plugins, contracts, routers, and composition root imported as UID `10001`. |
| `git diff --check` | pass | No whitespace errors. |

## Contract impact

`compatible-change`: additive independently versioned Source Connection and
File Import APIs, explicit source-intake ports, admin grants, reference-only
configuration, and PostgreSQL revision `0004_source_intake`. Existing identity
and organization APIs, DTOs, persisted identities, cache/request identity, and
consumer defaults are unchanged. Rollback removes only W14 catalog/template
state and restores revision `0003_organization_access`.

## Verdict

`passed` at `governed-postgresql-and-template-file-source-intake`. The full
connector matrix, ingestion artifacts and data quality, semantic registration,
sales/customer projections, browser behavior, production runtime, deployment,
release, recovery, and performance remain separate proof boundaries.
