# MS-004-S01 validation evidence — 2026-09-20

All commands ran in the canonical checkout after
`source scripts/activate-toolchain.sh`. No production target or source checkout
was used. These are observed local outcomes; no CI/publication result is claimed.

| Command / check | Observed outcome |
|---|---|
| `uv sync --locked --all-groups --all-packages` | Passed; repository-pinned existing dependencies only, no lockfile change |
| `corepack pnpm install --frozen-lockfile` | Passed; 206 existing locked packages reused, no lockfile change |
| `uv run --locked --package custometry-api python -m packages.contracts.generate_workspace_client` | Passed; schemas/OpenAPI/TS produced through existing renderer |
| `uv run --locked --package custometry-api --all-groups pytest -q tests/unit tests/contract` | 136 passed; includes required Presentation unit/contract suites, Identity contracts and all generated-file comparisons |
| `uv run --locked --package custometry-api --all-groups python tests/integration/semantic/run_s01.py --image sha256:5d004e058f520673f1f6edbad6b1603d5dab4c818e257c041889ef64672a8cc4` | 9 passed, 0 skipped, 13.72 s; actual isolated PostgreSQL, migration, Identity sessions and API; container/volume/secret cleanup completed |
| `corepack pnpm --filter @custometry/contracts typecheck` | Passed, generated clients compile |
| `uv run --locked ruff check apps/api/src migrations tests/contract/presentation/test_workspace.py tests/integration/semantic packages/contracts/semantic packages/contracts/analytics/workspace.py packages/contracts/presentation/workspace.py packages/contracts/generate_workspace_client.py packages/semantic_model/application/calendar.py packages/semantic_model/infrastructure/calendar.py` | Passed |
| `uv run --locked pyright apps/api/src tests/integration packages/contracts/semantic packages/contracts/analytics/workspace.py packages/contracts/presentation/workspace.py packages/semantic_model/application/calendar.py packages/semantic_model/infrastructure/calendar.py` | Passed, 0 errors/warnings |

Final focused rerun after the coordinator's null-hash finding:
`ruff check migrations/versions/0012_metric_workspace.py tests/integration/semantic`
and `pyright tests/integration/semantic` passed. The final nine-test DB run includes
explicit rejection of a custom calendar version with SQL NULL request_hash;
PostgreSQL CHECK UNKNOWN can no longer admit it. The pre-fix failure was identified
by source logic, not represented as a previously executed failing regression.

The real-boundary runner covers: additive backfill and original persisted v1
payloads; immutable creator and calendar versions; safe downgrade/re-upgrade;
same-workspace/report Saved View FKs; separate lossy-downgrade refusals for report,
Analytics, Saved View and custom calendar; role/session/CSRF/scope/invalid-profile
checks; two concurrent default writes; exact pinned reads and replay after newer
writes; transaction rollback on injected pointer failure; interrupted provisioning
recovery; report/Analytics v2 routes remaining unmounted.

Initial non-passing attempts are retained here as diagnoses, not counted as proof:
root-only Python lacked API packages, then API-only test environment lacked httpx;
the repository's existing all-package/all-group locked setup resolved those
prerequisites. First real fixture run used a UUID-leading workspace key and
`inactive` membership status; PostgreSQL correctly rejected them. The task-owned
fixture was corrected to existing Identity's key format and `suspended` status.
No production constraint was relaxed. Initial authoring lint/typing issues were
fixed in the new files; final gates above passed. Required real boundary checks
were not replaced with mocks or skips.

Documentation/index check: `generate_docs_index` passed (73 documents);
`check --scope local` passed; `validate_prompt_packs` passed (four journals);
`git diff --check` passed. Required v1 DTO/OpenAPI/client, MetricVersion definitions
and both lockfiles were compared with HEAD and are unchanged. These static checks
are rerun on the final handoff before receipt creation. Stage state remains in
the journal.
