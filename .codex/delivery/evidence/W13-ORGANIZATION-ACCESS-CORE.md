---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: W13-ORGANIZATION-ACCESS-CORE
proof_boundary: postgres-backed-organization-ownership-and-effective-access-api
proof_skills: [backend-quality-gates]
verdict: passed
redaction: No credentials, database passwords, access/session/invitation tokens, cookies, DSNs, raw PII, provider payloads, environment dumps, or private resource content are retained; observations name only safe IDs by role, bounded counts, status classes, commands, and module paths.
executed_checks:
  - verify isolated branch and worktree at origin/main commit 1c70d5240bca22d83eb8433e2de161d5c1a90739 with W12 accepted and passed evidence
  - verify Linear ROE-16 Todo, Docker context, Docker Compose, Docker engine, disjoint active ownership, and clean W13 worktree before writes
  - perform coordinator-authorized W13 draft-to-ready ticket and graph ownership reconciliation
  - source scripts/activate-toolchain.sh
  - uv run --locked pytest -q tests/unit/organization_access tests/contract/organization_access tests/integration/organization_access
  - uv run --locked pytest -q tests/integration/identity_access
  - uv run python -m tools.custometry_quality.validate_migration_lifecycle
  - uv run python -m tools.custometry_quality.validate_migration_lifecycle --mode runtime
  - uv run python -m tools.custometry_quality.check_contract_drift
  - uv run python -m tools.custometry_quality.check_ddd_boundaries
  - uv run python -m tools.custometry_quality.validate_delivery_tickets
  - uv run python -m tools.check --scope local
  - uv run python -m tools.check --scope pre-push
  - uv run ruff check packages/identity_access packages/contracts/organization apps/api/src/custometry_api/organization apps/api/src/custometry_api/main.py migrations/versions/0003_organization_access.py tests/unit/organization_access tests/contract/organization_access tests/integration/organization_access
  - uv run pyright packages/identity_access packages/contracts/organization apps/api/src/custometry_api/organization apps/api/src/custometry_api/main.py tests/unit/organization_access tests/contract/organization_access tests/integration/organization_access
  - independently review the uncommitted authorization, persistence, migration, API, test, and evidence surface; repair all actionable W13 findings and rerun invalidated proof
  - build custometry-api:w13-final3 and import W13 runtime modules inside the built read-only non-root image without bind mounts or PYTHONPATH
  - fast-forward the isolated branch over disjoint accepted W20 frontend-only origin/main drift and rerun ticket, focused W13, local, pre-push, and whitespace gates
  - git diff --check
observations:
  - The execution base and remote main were the required W12 merge commit 1c70d5240bca22d83eb8433e2de161d5c1a90739; the original divergent dirty checkout was not modified, stashed, reset, or used for W13 product writes.
  - W12 was accepted with verdict passed; no other repository ticket was ready or active, the only foreign dirty worktree was disjoint, and ROE-16 moved from Todo to In Progress only after W13 validated as ready.
  - The additive 0003_organization_access migration observed empty upgrade, repeated upgrade, downgrade to base, and re-upgrade across three revisions on disposable PostgreSQL; a populated lifecycle also downgraded departed membership state safely, re-upgraded, attributed legacy roots to an actual workspace owner/member, and backfilled one fail-closed legacy-root assignment for every active membership.
  - Twelve focused W13 tests passed on a clean pinned PostgreSQL 17.5 container, and three W12 real identity integration regressions passed against the upgraded schema after the legacy-root integration.
  - Real API observations covered company, division, department, and team creation; stable keys; current-version mutation; stale-version rejection; structural cycle/invalid-parent rejection; and cross-workspace parent denial.
  - PostgreSQL exclusion state rejected overlapping effective primary assignments; transfer closed the prior assignment, changed the effective department immediately, re-evaluated an org-unit grant, and departure invalidated the old authenticated membership.
  - Unit, subtree, and workspace leadership assignments produced distinct bounded scopes; subject and issuer ceiling escalation attempts were rejected, leadership never replaced the subject functional permission, and Workspace Administrator had no implicit report/business-content access.
  - Department policy draft, publish, second draft, and version-2 publish were observed; missing or non-effective policy remained fail-closed.
  - Principal and org-unit cross-department grants were reasoned, resource/action bounded, effective-dated, expired or revoked immediately, and unable to override functional, object, explicit-deny, or PII ceilings.
  - Functional permission came from a server-owned resource/action registry, while object action, row, column, export, and PII inputs came from persisted server-side resource-policy bindings rather than caller fields; a cross-department run grant remained denied solely by the Viewer functional ceiling, the domain explicit-deny resolver remained deny-wins, and PII remained denied without an explicit functional PII ceiling.
  - Visibility candidates were loaded from authoritative current bindings before policy filtering, count, and pagination; one visible resource returned visible_count=1 while the hidden resource identifier and hidden count were absent, and caller-supplied policy fields were rejected by the strict API schema.
  - Resource binding kept creator attribution immutable, persisted trusted object/row/column/PII requirements, kept a principal-owned draft invisible to a same-department colleague, failed closed for legacy ownership without an authoritative ACL, created deterministic handover work, retained department-owned published resources after departure, and moved department ownership and policy projection only through successor merge handover.
  - Closing or merging a unit with members or resources failed without a valid same-workspace successor; the accepted successor preserved history and created a new effective ownership/assignment version.
  - The committed organization OpenAPI provider byte-matched generated output and remained independently mounted from the Foundation contract.
  - Future hierarchy version and membership-deactivation timestamps were rejected before mutation, so immediate lifecycle commands could not change current state prematurely; grants and leadership retained effective-range evaluation at decision time.
  - The API image retained pinned base images, UID 10001, and read-only compatibility. Built-image imports resolved packages.identity_access.application.organization, packages.identity_access.infrastructure.organization_postgres, packages.contracts.organization, custometry_api.organization.router, and custometry_api.main; tests, Git metadata, node_modules, and runtime data were absent. Runtime inspection confirmed the server-owned functional registry and server-fetched visibility implementation; the local image identity was sha256:7c66da47c6f4d94db09cd5ca84f170159f18ebe9034f00d0136f3ffb61c5c81a before cleanup.
  - Ruff, strict Pyright, contract drift, DDD boundaries, ticket validation, local profile, pre-push profile, and whitespace validation passed.
  - Contract impact is compatible-change because the Organization API, persistence revision, policy permissions, and packaged organization contract are additive inside the accepted Identity, Organization & Access bounded context; no existing route identity, release topology, or external stable consumer was removed or changed.
  - The final independent cold review returned ready_for_next_gate with no blocking findings on the repaired trust, ownership, migration-attribution, API, and evidence boundary; TEST-INV-087 remained explicitly outside the canonical W13 mapping.
  - All W13 disposable PostgreSQL containers, temporary password files/directories, and the custometry-api:w13-final2 and custometry-api:w13-final3 image tags were removed; existing Hybrid containers, networks, volumes, and foreign worktrees were not changed.
  - After proof collection, origin/main advanced to 63bbaeb1aeaa8698a2c288ae700d6071bb1deaef for accepted W20 frontend-only work. Its paths were disjoint from W13; the isolated branch was fast-forwarded without stash or reset, then ticket validation, 10 focused unit/contract tests, local, pre-push, and whitespace gates passed again on that base.
---

# W13 Organization Access Core Evidence

## Outcome and scope

- outcome: authorized actors can manage a versioned organization hierarchy,
  assignments, scoped leadership, department policies, bounded grants, and
  resource ownership while protected consumers receive explainable deny-wins
  access decisions backed by PostgreSQL;
- requirement IDs: [UC-028, RBAC-019, RBAC-020, RBAC-021, RBAC-022, RBAC-023,
  RBAC-024, RBAC-025, RBAC-026, RBAC-028, TEST-INV-076, TEST-INV-077,
  TEST-INV-078, TEST-INV-079, TEST-INV-080, TEST-INV-081, TEST-INV-082,
  TEST-INV-083, TEST-INV-084, V1-AC-037, V1-AC-038, V1-AC-039, V1-AC-040,
  V1-AC-041, V1-AC-042];
- included: Identity, Organization & Access domain/application code, PostgreSQL
  adapter and migration, organization API composition, committed OpenAPI,
  bounded image packaging, and focused unit/contract/real-PostgreSQL API tests;
- exclusions: no ContributorActivityProjection, People & Creators runtime,
  Department Hub UI, Web/Penpot, HRIS/SCIM/OIDC, physical department data
  copies, W14 connectors/import, deployment, release, browser, recovery,
  performance, production configuration, or supply-chain claim.

`TEST-INV-079` and `V1-AC-042` are represented here only by their shared W13
leadership-scope, hidden-count, administrator, and PII authorization substrate.
Their ContributorActivityProjection and People & Creators outcomes remain the
explicit later vertical seam and are not claimed as accepted runtime behavior by
this evidence.

## Commands and observations

| Command or action | Result | Redacted observation |
|---|---|---|
| Readiness and ownership guard | pass | Exact W12 common base, accepted predecessor evidence, Linear Todo, Docker availability, clean isolated worktree, and no active path owner were observed before writes. |
| W13 readiness reconciliation | pass | Only the ticket, W13 graph ownership, and authorized API Dockerfile path were added before ticket validation; W13 was re-read as ready before Linear moved to In Progress. |
| Migration static/runtime lifecycle | pass | Three revisions completed empty upgrade, repeat, downgrade, and re-upgrade; populated departed-state downgrade and active-membership backfill also passed. |
| Exact focused W13 pytest command | pass | 12 unit, provider-contract, and real PostgreSQL/API tests passed. |
| W12 integration regression | pass | 3 local-authentication, workspace, session, and token integration tests passed on the W13 schema. |
| Hierarchy, assignments, lifecycle | pass | Versioning, conflict, parent/workspace guards, primary exclusion, transfer, departure, successor merge, and durable handover were observed. |
| Leadership, policy, and grants | pass | Unit/subtree/workspace scope, subject/issuer functional ceilings, policy draft/publish/v2, grant active/expired/revoked states, and transfer re-evaluation passed. |
| Effective access negative cases | pass | Server-owned policy inputs, tampering rejection, administrator content denial, deny-wins, server-fetched hidden count, snapshot action separation, PII ceiling, stale/missing policy, and cross-workspace denial passed. |
| Contract, DDD, Ruff, Pyright, local, pre-push | pass | All repository and focused static gates returned PASS with strict Pyright at zero errors/warnings. |
| Built-image packaging/import smoke | pass | Required modules imported under UID 10001 in a read-only container; excluded repository/runtime paths were absent. |
| Runtime cleanup audit | pass | No W13 disposable container, temp secret path, or import-smoke image tag remained. |

## Contract impact

`compatible-change`: additive Organization API, resource-policy projection,
legacy-root membership integration, and persistence within the accepted
Identity, Organization & Access context. Rollback maps `departed` to the prior
`suspended` state, removes the new revision/provider capability, and restores
the prior membership-status constraint; no stable consumer or topology was
removed or changed.

## Verdict

`passed` at
`postgres-backed-organization-ownership-and-effective-access-api`.
Publication, common-main merge, GitHub CI, browser, deployment, release,
recovery, performance, and production readiness remain separate boundaries.
