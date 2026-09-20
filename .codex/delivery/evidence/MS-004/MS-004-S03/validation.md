# MS-004-S03 validation

All required S03 local checks passed on the final source manifest. These are
local API/PostgreSQL/artifact results, not browser, proxy-network, CI, deployment
or finished-milestone owner acceptance. Run dates use the session's 2026-09-20
local date. Existing Node 24.18.0 / pnpm 11.13.0 / uv 0.9.26 toolchain was used;
no dependency installation or candidate image build occurred.

## Real API, database and immutable artifact proof

After `source scripts/activate-toolchain.sh`:

```sh
MS004_S03_EVIDENCE_PATH=/tmp/ms004-s03-terminal-corpus.json uv run --locked python tests/integration/presentation/run_s03.py --image 5d004e058f52
```

Exit 0. The runner creates fresh source/control databases in a loopback-only
owned PostgreSQL container, applies current migrations, seeds actual source
retail tables and executes production intake and actual Identity/Presentation/
Analytics API handlers. It then creates another fresh control database at 0011
for the legacy suite. Its final cleanup succeeded; `docker ps` filtered by the
S03 ownership label returned no remaining containers.

- `tests/integration/presentation/test_workspace_s03.py`: **1 passed in 260.88s**.
- `tests/integration/presentation/test_drafts.py` and `test_report_context.py`:
  **2 passed in 5.01s**, with successful teardown. No skipped real tests.
- The assertions cover the complete Presentation integration test set, using
  separate schema starting points for the migrated API and historical fixture.
- [Corpus](corpus.json): six admitted source-artifact hashes, registered metric
  versions, synthetic dataset/snapshot/result IDs and comparison manifest.
- Helper-observed HTTP outcomes: 200=50, 400=2, 401=12, 403=41, 404=11, 409=9,
  413=1, 422=1, 503=2. Counts exclude separately asserted cookie, unauthenticated
  and concurrent-save TestClient calls; they are not performance measurements.
- Every new report/editor/snapshot/Apply/Save/own-view and direct Analytics
  result/context/catalog/comparison route has real cross-workspace and revoked
  session checks. Denied data bindings, scope narrowing, unsupported policies,
  no-run verification-only reuse and private result/overlay boundaries are tested.
- Fresh connections prove unchanged report/view pointers after injected artifact
  failure, DB failure, dual-CAS conflicts and access revocation at precommit.
  Exact replay, old-schema v1 migration, unchanged old snapshots, missing/corrupt
  result/comparison bytes, fiscal pin/adoption and retired IDs are asserted.

During development, the extra legacy run first exposed an old-schema fixture
writer using the current discriminator, then teardown exposed an immutable
calendar backfill FK. The fixture now writes the historical column shape before
migration and cleans only its task-owned calendar records in teardown; production
immutability is unchanged. Both failures are resolved by the final run above.
Earlier successful runs are supplementary, not substitutes for this final run.

## Focused regression and static checks

```sh
uv run --locked pytest -q tests/unit/presentation tests/contract/presentation tests/contract/analytics tests/unit/analytics tests/unit/identity_access tests/integration/analytics/test_workspace_s02.py::test_v2_routes_require_current_authentication
```

**109 passed in 1.06s**. This includes creator/schema/strict-union and generated
route inventory contracts, existing Analytics logic, deny-wins scope tests and
the current authentication requirement replacing S02's historical unmounted gate.
The S02 real SQL/calculation proof remains linked from its immutable report;
S03 does not claim to have rerun its entire fiscal corpus.

```sh
corepack pnpm --filter @custometry/contracts typecheck
corepack pnpm --filter @custometry/contracts test
```

TypeScript: exit 0. Existing contract package tests: **4 passed**, one file.
This is generated contract/client source proof, not Web UI/browser proof.

Ruff checked all 27 changed Python files; Pyright checked all 20 changed production
Python files: **0 errors, 0 warnings**. Actual path sets are recorded below and
bound by [owned files](owned-files.json). The tool's optional Pyright update notice
is informational; no installation was performed.

```sh
uv run --locked ruff check apps/api/src/custometry_api/analytics/router.py apps/api/src/custometry_api/analytics/workspace_access.py apps/api/src/custometry_api/analytics/workspace_errors.py apps/api/src/custometry_api/analytics/workspace_router.py apps/api/src/custometry_api/reports/router.py apps/api/src/custometry_api/reports/workspace_composition.py apps/api/src/custometry_api/reports/workspace_router.py packages/analytics_core/application/snapshot_verification.py packages/analytics_core/application/workspace_service.py packages/contracts/generate_workspace_client.py packages/contracts/identity/access.py packages/contracts/presentation/workspace.py packages/contracts/presentation/workspace_ports.py packages/identity_access/application/resource_access.py packages/identity_access/infrastructure/organization_postgres.py packages/identity_access/infrastructure/resource_access.py packages/presentation/application/reports.py packages/presentation/application/workspace.py packages/presentation/infrastructure/postgres.py packages/presentation/infrastructure/workspace.py tests/contract/presentation/test_reports.py tests/integration/analytics/test_workspace_s02.py tests/integration/presentation/conftest.py tests/integration/presentation/run_s03.py tests/integration/presentation/test_drafts.py tests/integration/presentation/test_workspace_s03.py tests/unit/presentation/test_workspace_access.py
uv run --locked pyright apps/api/src/custometry_api/analytics/router.py apps/api/src/custometry_api/analytics/workspace_access.py apps/api/src/custometry_api/analytics/workspace_errors.py apps/api/src/custometry_api/analytics/workspace_router.py apps/api/src/custometry_api/reports/router.py apps/api/src/custometry_api/reports/workspace_composition.py apps/api/src/custometry_api/reports/workspace_router.py packages/analytics_core/application/snapshot_verification.py packages/analytics_core/application/workspace_service.py packages/contracts/generate_workspace_client.py packages/contracts/identity/access.py packages/contracts/presentation/workspace.py packages/contracts/presentation/workspace_ports.py packages/identity_access/application/resource_access.py packages/identity_access/infrastructure/organization_postgres.py packages/identity_access/infrastructure/resource_access.py packages/presentation/application/reports.py packages/presentation/application/workspace.py packages/presentation/infrastructure/postgres.py packages/presentation/infrastructure/workspace.py
```

## Generation, documentation and handoff checks

```sh
uv run --locked python -m packages.contracts.generate_workspace_client
uv run --locked python -m packages.contracts.generate_reports_client
uv run --locked python -m packages.contracts.generate_sales_client
uv run --locked python -m tools.custometry_quality.generate_docs_index
uv run --locked python -m tools.check --scope local
uv run --locked python -m tools.custometry_quality.validate_prompt_packs
git diff --check
```

Generators succeeded; docs index reports 73 documents. The local profile passed,
including contract drift and documentation links. Prompt-pack validation passed
for four journals, proving structure/file binding only. Diff whitespace passed.
Final source hashes were checked unchanged during and after the final real run.
The accepted plan hash remains
`9d0d590f7c3fccc581a6257365f0bcba961539f1fa9e0f93eec651e36255360e`.

S04's exact prompt was read and every declared entry path exists: accepted plan,
ReportWorkspace.tsx, PilotDocument.tsx, pilot/seams.json and the S03 report.
S04 remains pending/disallowed; no preflight success, claim or execution is
inferred. Its new browser config/fixture are its own outputs. Coordinator review,
PR/Foundation synchronization and branch deletion must precede a fresh advance.
No source PR, Git branch, commit, merge, deployment or release was performed here.
