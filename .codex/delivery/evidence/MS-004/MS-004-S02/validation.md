# MS-004-S02 validation — 2026-09-20

Commands ran in the canonical checkout after `source scripts/activate-toolchain.sh`.
The baseline is `b4aaa1680cfff5885fe61ff98fe7e69cf4934df0`; no source checkout,
shared database, deployment, Git publication or external source was mutated.

## Focused source checks

- `uv run --locked --package custometry-api --all-groups pytest -q tests/unit tests/contract`:
  160 passed. Includes preserved v1 Analytics and Presentation tests, 24 new
  workspace calculation invariants and generated DTO/schema/client parity.
- `uv run --locked --package custometry-api python -m packages.contracts.generate_workspace_client`:
  passed; all affected schemas, components-only OpenAPI and TypeScript regenerated.
- `uv run --locked ruff check` and `uv run --locked pyright` over the exact Python
  paths listed below: passed, no lint findings or type errors/warnings.
- `corepack pnpm --filter @custometry/contracts typecheck`: passed.
- `uv run --locked python -m tools.custometry_quality.generate_docs_index`:
  passed, 73 documents; generated index unchanged because document inventory/titles
  are unchanged. Authoring/recovery contracts were updated in place.
- `uv run --locked python -m tools.check --scope local`: passed.
- `uv run --locked python -m tools.custometry_quality.validate_prompt_packs`:
  passed, four journals. This proves artifact consistency, not stage execution.
- `git diff --check`: passed. Bounded diff inspection confirms unchanged v1
  calculation/request/MetricVersion files, main app composition and accepted plan.

Exact lint/type targets:

```text
packages/contracts/analytics/workspace.py
packages/contracts/generate_workspace_client.py
packages/analytics_core/application/workspace_calculation.py
packages/analytics_core/application/workspace_service.py
packages/analytics_core/infrastructure/postgres.py
packages/artifacts/infrastructure/workspace.py
apps/api/src/custometry_api/analytics/workspace_router.py
tests/unit/analytics/test_workspace_calculation.py
tests/integration/analytics/run_s02.py
tests/integration/analytics/test_workspace_s02.py
```

## Real boundary

Command (optional output path points to task-owned scratch; only its redacted JSON
is copied into `corpus.json` after success):

```bash
MS004_S02_EVIDENCE_PATH=<task-scratch-json> uv run --locked --package custometry-api --all-groups python tests/integration/analytics/run_s02.py --image sha256:5d004e058f520673f1f6edbad6b1603d5dab4c818e257c041889ef64672a8cc4
```

Final outcome: **3 passed, 0 skipped, in 101.20 s**. Includes the original v1
real-intake regression, the full v2 corpus/matrix and main-app unmounted-route
proof. The v2 test checked 2,838 current buckets plus mapped baseline buckets and
full-period SQL totals. The source had 6,573 eligible receipts, 1,095 observed
days, three observed stores, 1,095 Calendar dates and 1,094 declared-complete
dates; six admitted IDs/hashes and per-store coverage are in `corpus.json`.
Container/volume/secret cleanup completed successfully.

The runner owns one disposable loopback PostgreSQL container and fresh source and
control databases, migrates to existing 0012, seeds actual PostgreSQL tables, uses
production PostgreSQLConnector/DataPipelineRunner and verifies actual immutable
artifacts and repository transactions. It removes its own container/volumes and
private secret file. The API adapter test uses a separate test-only app; main app
probes verify v2 is unmounted. No mocked database, intercepted intake, fabricated
rows substituted after extraction or skipped required boundary is accepted.

The main v2 test performs the 6 grains × 2 bases × 3 fiscal starts × 2 label
conventions matrix. SQL independently generates the current/prior date mapping,
including the year-crossing week; production baseline date lists are checked
against that mapping before the SQL receipt oracle consumes them. Exact numeric
bucket/current/baseline totals, ratios, natural/exclusive boundaries, FY labels
and coverage are asserted. Other cases cover full leap-crossing April–March,
unmatched and excluded leap dates, missing baseline receipts, missing/incomplete
Calendar, observed partial current values, zero baseline, all three unit pairs,
period/grain/calendar mismatch, equivalent contexts, disjoint/empty/denied stores,
policy partition/revocation seam, concurrent winner/dependencies and input/output
corruption/missing output. The original v1 real-intake oracle runs unchanged first.

`Access` is a trusted test projection double. Its denial and policy-change cases
prove application-port handling, not real Identity object/data authorization.
The production router is deliberately unmounted until S03 supplies that proof,
including real authentication/CSRF and direct-caller negative cases. Source SQL
and artifact persistence are real; browser, saved-report transactions and owner
milestone acceptance are outside S02.

## Non-passing attempts and corrections

Initial new code had typing/lint annotation findings; corrected in new files before
final gates. First real corpus failed admission because it omitted the existing
profile's exactly-five known product sentinels. Source inspection of the admission
rule established the cause; fixture setup now retains those five quarantined
ReceiptItems without weakening production DQ. The first unmounted-route test also
passed Settings positionally to a keyword-only factory; fixed its invocation.

The next oracle attempt used `day`/`begin` as SQL aliases and failed syntax parsing;
the test query now uses `dt`/`bucket_begin`. Its teardown exposed new immutable
calendar references to the fixture principal; a task-owned fixture finalizer now
truncates only its disposable database's Semantic calendar tables before existing
fixture cleanup. No shared teardown/migration or production guard was relaxed.

The repaired baseline real run passed 3 tests in 81.92 s. After comparison envelope
and additional adapter/pair coverage, 3 passed in 94.82 s. The strengthened
independent mapping/label run passed 3 in 95.55 s. Final explicit current totals and
partial-current assertions are included in the terminal run recorded above.
These earlier passes are not substituted for a pass on the final sources.
