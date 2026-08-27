---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.10.0-draft
ticket_id: W16-SALES-CUSTOMER-RFM-API-PROJECTIONS
proof_boundary: governed-sales-customer-rfm-reportable-result-and-api-projection
proof_skills: [backend-quality-gates]
verdict: passed
redaction: Runtime database and source passwords remained file-backed and were never printed; no DSN, raw source row, raw customer identifier, environment dump, bearer token, absolute temporary artifact path, or provider payload is retained. Evidence records only safe loopback boundaries, aggregate values, hashes, stable codes, commands, and repository paths.
executed_checks:
  - git fetch origin main and verify origin/main 68ad124ac6c7400c67df8bdd75752fe1bd350e76
  - import independently scoped W15 commit d7511096433f1ce605639e9c24afa3936377c9c8 and verify W15 accepted with verdict passed
  - uv run python -m tools.custometry_quality.validate_delivery_tickets
  - uv run python -m tools.custometry_quality.validate_delivery_contract --contract /Users/daniildegtyarev/.codex/skills/delivery-orchestrator/references/delivery-contract-v1.md
  - uv lock
  - uv run ruff check packages/contracts/analytics packages/analytics_core apps/api/src/custometry_api/analytics apps/api/src/custometry_api/main.py apps/api/src/custometry_api/config.py migrations/versions/0006_analytics_projection.py tests/unit/analytics tests/contract/analytics tests/integration/analytics
  - uv run --package custometry-api pytest -q tests/unit/analytics tests/contract/analytics -rs
  - run W15 plus W16 unit contract and real PostgreSQL/filesystem integration tests against the owned development runtime
  - uv run --locked python -m tools.custometry_quality.validate_migration_lifecycle --mode runtime
  - uv run python -m tools.custometry_quality.check_ddd_boundaries
  - uv run python -m tools.custometry_quality.check_contract_drift
  - uv run python -m tools.custometry_quality.validate_fixture_manifest
  - source scripts/activate-toolchain.sh and uv run --locked python -m tools.check --scope local
  - git diff --check
observations:
  - W15 was transferred as one path-whitelisted local commit, remained accepted with passed terminal evidence, and its validators passed before W16 moved from draft to ready.
  - Seven focused domain/property tests and two API contract tests passed; the combined W15 plus W16 suite passed 26 tests.
  - Real PostgreSQL and filesystem execution consumed the accepted W15 semantic publication and four content-verified Parquet bindings, then produced immutable sales, customer-base, and RFM result metadata plus content-addressed JSON result manifests.
  - The deterministic retail golden expectation reconciled current 2025 plus prior-year 2024 net revenue to 897419.82 without header-to-item amplification.
  - Sales groups remained ordered as finance then commerce, raw numeric values remained distinct from compact labels, and typed filters rejected operator/value mismatches before artifact access.
  - Comparison output retained current and comparison values, absolute and percent changes, coverage, comparability, timezone, calendar version, explicit leap-day/ISO-week-53/incomplete-period policies, normalized filter hash, and policy hash; missing values were not silently replaced with zero.
  - Customer metrics used source-qualified canonical customer keys and receipt identity at header grain; RFM used an explicit as-of date, bounded deterministic tie scoring, versioned rule-set identity, and SHA-256 customer projections without raw identifiers.
  - Repeating the exact request returned the same result ID, request hash, storage URI, content hash, and manifest while PostgreSQL retained one row for that identity.
  - An authenticated but non-owner actor received NOT_FOUND for the hidden result and an empty collection with visible_count zero; no total or hidden-object count was exposed.
  - Runtime migration lifecycle observed upgrade_empty, upgrade_repeat, downgrade, and reupgrade across six revisions; the API image included the W16 domain and contract packages.
  - Ruff, DDD boundaries, contract drift, deterministic fixture, ticket/contract validators, exact OpenAPI snapshot, grouped local gate, and whitespace checks passed.
  - "Contract impact is compatible-change: additive independently versioned analytics HTTP endpoints, typed request/response schemas, public semantic-artifact projection view, immutable analytics_results table, filesystem result manifest identity, API image packages, and PostgreSQL revision 0006; no existing endpoint, DTO, route contract, config default, W15 persisted identity, cache key, or side-effect semantics were removed or redefined."
  - Foreign UI, blueprint, UI-program, route-contract, and documentation changes remained outside W16 ownership and were neither edited nor staged.
---

# Outcome and scope

W16 produced governed sales, customer-base, and RFM results from accepted W15
semantic/DQ/artifact projections. The authenticated API exposes only
policy-visible immutable results with typed filters, explicit current and
previous-year semantics, ordered compact metric groups, quality, freshness,
lineage, and stable result identity. Frontend/UI, forecasting, report delivery,
clustering, causal inference, publication, release, and deployment remained out
of scope.

# Commands and observations

Focused deterministic checks passed 9 tests. The combined W15 and W16 boundary
passed 26 tests, including the disposable real PostgreSQL, deterministic retail
source, W15 Parquet artifact, W16 filesystem result, and authenticated API path.
Migration lifecycle passed all four runtime steps across revisions 0001 through
0006. Repository-local static and grouped gates passed. Detailed safe
observations are retained in frontmatter; secrets and temporary paths are not.

# Verdict

`passed` at
`governed-sales-customer-rfm-reportable-result-and-api-projection`. This evidence
does not claim browser behavior, production recovery, performance, release,
supply-chain, deployment, or production readiness.
