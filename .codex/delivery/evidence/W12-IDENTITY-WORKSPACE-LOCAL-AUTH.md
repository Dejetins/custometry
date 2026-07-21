---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: W12-IDENTITY-WORKSPACE-LOCAL-AUTH
proof_boundary: postgres-backed-identity-workspace-local-auth-and-functional-authorization-api
proof_skills: [backend-quality-gates]
verdict: passed
redaction: No credentials, raw passwords, session tokens, invitation tokens, API tokens, DSNs, cookies, provider payloads, or environment dumps are retained; observations name only bounded resources, counts, safe module paths, and status classes.
executed_checks:
  - docker context show && docker compose version && docker info
  - scripts/dev validate && scripts/dev status && scripts/dev up --mode hybrid
  - reproduce imports in the pre-repair custometry-api:dev image
  - docker build --file apps/api/Dockerfile --tag custometry-api:w12-import-smoke .
  - import packages.identity_access, packages.identity_access.application.service, packages.identity_access.infrastructure.postgres, packages.contracts.identity, and custometry_api.main inside the built image
  - verify non-root image execution and absence of tests, Git metadata, caches, node_modules, runtime data, and secrets
  - uv run --locked pytest -q tests/unit/identity_access tests/contract/identity_access tests/integration/identity_access
  - uv run python -m tools.custometry_quality.validate_migration_lifecycle
  - uv run python -m tools.custometry_quality.validate_migration_lifecycle --mode runtime
  - uv run python -m tools.custometry_quality.check_contract_drift
  - uv run python -m tools.custometry_quality.check_ddd_boundaries
  - uv run python -m tools.custometry_quality.validate_delivery_tickets
  - uv run python -m tools.check --scope local
  - uv run pyright packages/identity_access packages/contracts/identity apps/api/src/custometry_api tests/unit/identity_access tests/contract/identity_access tests/integration/identity_access
  - git diff --check
observations:
  - W11 was accepted with passed terminal evidence and merge commit d12bcc8098968bb43b654bfb9ae101a9c4072a72 in the execution base before W12 became ready.
  - The original migration-image blocker reproduced as ModuleNotFoundError for the packages namespace after custometry_api.main mounted the Identity API.
  - C-CORE coordinator explicitly extended W12 ownership to the runtime/data graph and apps/api/Dockerfile for the bounded packaging repair.
  - The API image now copies only packages/identity_access and packages/contracts/identity into its pinned Python 3.12 site-packages; the base images, non-root UID 10001, read-only compatibility, Compose topology, and release manifests are unchanged.
  - Container import smoke resolved all five required module paths from the built image and found none of the excluded repository or runtime data paths.
  - The disposable migration validator observed upgrade of an empty PostgreSQL database, repeated upgrade, downgrade to base, and re-upgrade across two revisions.
  - Focused unit, property, provider-contract, OpenAPI-contract, and real PostgreSQL/API tests passed 17 tests.
  - Real PostgreSQL/API observations covered one-winner concurrent bootstrap, irreversible bootstrap disablement, invitations and revocation, membership, login, refresh rotation, refresh reuse family revocation, logout, session listing/revocation, password reset/change, scoped API tokens, functional permission ceilings, cross-workspace denial, and hash-only persistence.
  - Contract drift, DDD boundaries, ticket validation, grouped local checks, strict Pyright, and whitespace validation passed.
  - No custometry-migration containers, networks, volumes, temporary migration directories, or secret files remained; the dedicated w12-import-smoke image tag was removed and no foreign Docker resources were changed.
  - Contract impact is compatible-change because additive Identity API, persistence, configuration defaults, and required image modules are introduced without changing external topology or the release contract.
---

# W12 Identity Workspace Local Auth Evidence

## Outcome and scope

- outcome: local principals can bootstrap the first owner/workspace, authenticate,
  rotate or revoke sessions, detect refresh replay, accept bounded invitations,
  manage workspace membership, and use least-privilege expiring API tokens through
  stable API contracts backed by PostgreSQL;
- requirement IDs: [AUTH-001, AUTH-002, AUTH-003, AUTH-004, AUTH-005, AUTH-006,
  AUTH-007, AUTH-008, AUTH-009, AUTH-010, AUTH-011, RBAC-001, RBAC-002, RBAC-003,
  RBAC-004, RBAC-005, RBAC-006, RBAC-007, RBAC-008, RBAC-009, RBAC-010, RBAC-011,
  RBAC-012, RBAC-013, RBAC-014, RBAC-015, RBAC-016, RBAC-017, RBAC-018];
- included: Identity & Workspace domain/application kernel, PostgreSQL adapter,
  additive migration, local Identity API, browser-cookie/CSRF/origin boundary,
  CORS fail-closed configuration, provider-neutral future identity contract,
  committed Identity OpenAPI, and bounded API-image packaging;
- exclusions: no W13 organization hierarchy, OIDC runtime, UI/browser-product
  acceptance, ingestion, analytics, deployment, release, recovery, performance,
  production configuration, or immutable supply-chain proof.

## Commands and observations

| Command or action | Result | Redacted observation / durable reference |
|---|---|---|
| W11/readiness and ownership reconciliation | pass | W12 changed from `draft` to `ready` only after accepted W11 evidence/base and disjoint active ownership were observed. |
| Pre-repair image import reproduction | pass | `custometry_api.main -> custometry_api.identity.router -> packages.identity_access` failed because the image omitted the packages namespace. |
| Bounded Dockerfile repair and image build | pass | Only the two W12 runtime module trees were added to Python site-packages; non-root and pinned-image properties remained. |
| Container import/content smoke | pass | Five required imports resolved under `/app/.venv`; UID was 10001 and excluded paths were absent. |
| `uv run python -m tools.custometry_quality.validate_migration_lifecycle --mode runtime` | pass | Four real disposable PostgreSQL lifecycle steps were observed across two revisions. |
| Focused W12 pytest command | pass | 17 unit/property/contract/real-PostgreSQL API tests passed. |
| Negative authorization and session cases | pass | Analyst invitation administration, cross-workspace membership discovery, stale access after revoke/logout/password change, and refresh replay were denied. |
| Secret persistence inspection | pass | Password, invitation, session, refresh, and API token plaintext values were absent from persisted identity rows. |
| Contract/DDD/static migration/ticket/local gates | pass | All repository checks returned `PASS`; Identity OpenAPI matched its committed provider document. |
| Strict Pyright and `git diff --check` | pass | `0 errors, 0 warnings, 0 informations`; no whitespace errors. |
| Runtime cleanup audit | pass | No disposable migration resource or temporary secret directory remained; only repository-owned Hybrid resources stayed healthy. |

## Verdict

`passed` at `postgres-backed-identity-workspace-local-auth-and-functional-authorization-api`.
The remaining publication steps can establish GitHub CI and common-main merge
evidence, but they do not expand this ticket into browser, deployment, release,
recovery, performance, or production-readiness claims.
