---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.10.0-draft
ticket_id: W17-PEOPLE-CONTRIBUTOR-ACTIVITY-PROJECTION
proof_boundary: privacy-safe-contributor-projection-and-policy-filtered-people-api
proof_skills: [backend-quality-gates, contract-impact-analysis]
verdict: passed
redaction: The disposable PostgreSQL password remained file-backed and was never printed; no DSN, bearer token, invitation token, raw Audit event, exact login observation, raw provider payload, environment dump, email address from a runtime response, or hidden resource title/count is retained. Evidence records only commands, safe fixture labels, aggregate counts, hashes, stable codes, repository paths, and loopback boundaries.
executed_checks:
  - git fetch origin main and verify origin/main 68ad124ac6c7400c67df8bdd75752fe1bd350e76
  - verify W13 commit 3ec4ef11b19266b01d1584ad598c32ccd2b42977 and W16 commit 1772ec3d17a90caa14b05e3ebba7fcd8b3350aa9 are ancestors of the W17 base
  - verify W13 and W16 ticket status accepted and terminal evidence verdict passed
  - uv run python -m tools.custometry_quality.validate_delivery_tickets
  - uv run python -m tools.custometry_quality.validate_delivery_contract --contract /Users/daniildegtyarev/.codex/skills/delivery-orchestrator/references/delivery-contract-v1.md
  - uv run ruff check packages/contracts/people packages/identity_access/application/contributor_activity.py packages/identity_access/infrastructure/contributor_postgres.py packages/presentation apps/api/src/custometry_api/people apps/api/src/custometry_api/main.py packages/identity_access/application/__init__.py packages/identity_access/infrastructure/__init__.py packages/identity_access/domain/policy.py migrations/versions/0007_contributor_projection.py tests/unit/contributor_projection tests/contract/contributor_projection tests/integration/contributor_projection
  - uv run pyright packages/contracts/people packages/identity_access/application/contributor_activity.py packages/identity_access/infrastructure/contributor_postgres.py packages/presentation apps/api/src/custometry_api/people apps/api/src/custometry_api/main.py tests/unit/contributor_projection tests/contract/contributor_projection tests/integration/contributor_projection
  - uv run --package custometry-api pytest -q tests/unit/contributor_projection tests/contract/contributor_projection -rs
  - migrate an owned disposable repository-pinned PostgreSQL 17.5 database from 0001 through 0007 and run uv run --package custometry-api --group test pytest -q tests/integration/contributor_projection -rs
  - uv run python -m tools.custometry_quality.validate_migration_lifecycle --mode runtime
  - uv run python -m tools.custometry_quality.validate_repository_layout
  - uv run python -m tools.custometry_quality.check_ddd_boundaries
  - uv run python -m tools.custometry_quality.check_contract_drift
  - uv run python -m tools.custometry_quality.validate_migration_lifecycle --mode static
  - uv run python -m tools.custometry_quality.doctor --mode static
  - uv run python -m tools.custometry_quality.compose_lifecycle --mode static
  - uv run python -m tools.custometry_quality.browser_smoke --mode static
  - source scripts/activate-toolchain.sh and uv run --locked python -m tools.check --scope local
  - git diff --check
observations:
  - W13 and W16 were accepted with passed terminal evidence before W17 moved from draft to ready; both scoped predecessor commits remained in the ancestry of the W17 base.
  - Focused Ruff passed, focused Pyright reported 0 errors and 0 warnings, and the redaction, aggregation, visibility, and OpenAPI suites passed 9 tests.
  - Property evidence varied hidden-resource cardinality from zero through 25 and observed an invariant public response containing only one visible resource, no activity aggregate, and no hidden title or count influence.
  - Event intake accepted only eight explicit redacted domain-event types, rejected raw Audit/login-shaped events, arbitrary payload fields, email-shaped resource titles, cross-workspace batches, and profile/resource shape mixing.
  - The Identity-owned PostgreSQL adapter persisted only allowlisted projection fields; repeating ingestion and explicit rebuild retained one deterministic event set, three buckets, one profile, and an identical SHA-256 projection version.
  - The real authenticated API scenario observed self, scoped leader, explicit grantee, ordinary authorized viewer, and workspace-administrator variants. Self, leader, and grantee received filtered 30/90-day aggregates; the ordinary viewer received public metadata and visible resources without activity; the administrator without a contributor grant failed closed with NOT_FOUND and an empty listing.
  - Five events for a hidden PII resource did not affect returned resource count or aggregate values. Runtime responses and the committed schema exposed no hidden title, email, raw Audit surface, ranking, productivity score, peer percentile, or login history.
  - Cross-workspace candidate lookup failed closed, pagination counted only policy-visible people, and resource titles/counts were composed only after a current Organization policy decision for every resource.
  - Runtime migration lifecycle observed upgrade_empty, upgrade_repeat, downgrade, and reupgrade across seven revisions. The API runtime image imported the new People contract and Presentation package after the user-authorized additive Dockerfile packaging repair.
  - Repository layout, DDD boundaries, contract drift, static migration lifecycle, static doctor/Compose/browser manifests, ticket/contract validators, grouped local gate, and whitespace checks passed.
  - "Contract impact is compatible-change: additive independently versioned People HTTP endpoints, strict DTOs and owner ports, four new Identity-owned privacy-safe projection tables in revision 0007, policy-filtered contributor visibility semantics, additive role permission ceilings, and runtime image package copies; no existing endpoint, DTO, route contract, config default, Audit private table, cache/request identity, or side-effect semantic was removed or redefined."
  - The disposable PostgreSQL container and file-backed test credential were removed after observation; no W17 runtime container remains.
  - Frontend/UI, W18+, product blueprints, UI-program artifacts, route contracts, Audit private tables, deployment, release, publication, raw Audit browsing, ranking, productivity scoring, HR decisions, and exact-login surveillance remained outside W17 ownership.
---

# Outcome and scope

W17 provides a privacy-safe contributor activity projection from allowlisted,
redacted domain events and an independently versioned authenticated People API.
Every resource title, count, activity window, and pagination count is composed
only after current workspace, leadership/grant, and resource-policy checks.
Requirement IDs: `UC-029`, `RBAC-022`, `RBAC-027`, `TEST-INV-085`,
`TEST-INV-086`, `TEST-INV-087`, `TEST-INV-088`, and `V1-AC-043`.

# Commands and observations

Focused deterministic checks passed 9 tests. A clean disposable PostgreSQL 17.5
database migrated through revision `0007_contributor_projection`, and the real
authenticated projection/API scenario passed 1 test with repeat-ingest and
rebuild idempotency. Runtime migration lifecycle passed all four observations
across seven revisions. Repository-local static, contract, boundary, image
manifest, grouped local, and whitespace gates passed. Detailed privacy-safe
observations are retained in frontmatter.

# Verdict

`passed` at
`privacy-safe-contributor-projection-and-policy-filtered-people-api`. This
evidence does not claim browser runtime behavior, production recovery,
performance, SBOM/license, release, deployment, publication, or production
readiness. The next safe step is a separately authorized W18-or-later ready
ticket; no downstream work is implied by W17 acceptance.
