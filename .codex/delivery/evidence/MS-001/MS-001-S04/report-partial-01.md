# MS-001-S04 — Partial native consumer qualification

Plan [MS-001 2.2.0](../../../../../docs/architecture/planning/milestones/MS-001/plan.md).
The [canonical journal](../../../ledgers/MS-001.md) alone owns execution state.
Mode: `manual_sequential`; scope: S04 only. Native AMD64 proof is still unavailable,
so S04 is not accepted and S05 remains disallowed. The recoverable decision is the
[prepared temporary draft-release transfer](remote-operation.md).

## Observed local result

The exact S03 handoff `0.1.0-internal.20260908.s03.3` was copied to a new private
consumer directory `/Users/daniildegtyarev/.local/share/custometry/delivery/MS-001/s04-consumer-arm64-01`.
All independent toolkit/archive/ZIP hashes were checked before reader execution.
Manifest SHA-256 `693cbe3b4dfcd5148c9aab6dd2b1e946d9b46ae0ce3c22a69b4a03111f1a735a`;
image source `bc347d7e74c57640b42462c24cc2ed60d76ef055`; profile `internal-development`.
The six retained archives are unchanged. The actual engine was Docker 29.6.2,
Linux `aarch64`, 18 visible CPUs, 8,319,213,568 allocated bytes, on the M5 host.
This was fresh directory acquisition/import into the existing engine, not an empty
Docker image store. No application source build, checkout mount or registry pull occurred.

[Runtime observations](arm64-result.json) bind imported Docker subjects and exact
archive hashes. The isolated project `ms001s04-8ab4706e1b` started control and optional
demo PostgreSQL, API, Web and Edge; all five services were healthy. Packaged Alembic
reached `0009_notifications` on the fresh control database; a second upgrade succeeded.
API imports of `custometry_api.main`, `pyarrow`, `pyarrow.parquet`, `sqlalchemy`,
`psycopg` and `alembic` succeeded. Packaged JS/CSS, `/docs/`, Edge health and proxied
`/api/health/ready` returned HTTP 200.

| Observation | One actual run |
|---|---:|
| Exact retrieved file bytes | 478,784,861 |
| Local copy/hash retrieval | 0.404 s |
| Reader payload/image verification | 0.190 s |
| API / Web / PostgreSQL import | 0.719 / 0.199 / 0.750 s |
| Database startup | 6.227 s |
| Fresh migration / repeated migration | 2.713 / 2.492 s |
| API/Web/Edge startup | 17.459 s |

These are single-run observations, not a performance comparison or peak guarantee.
Docker stats sampled approximately 161.385 MiB aggregate across the five live services;
configured per-service caps total 3,154,116,608 bytes including the migration job,
below the 6 GiB ceiling. [Resource observation](arm64-resource-observation.json)
records 49,372/46,728 KiB in the two database data directories and 1,888,640 KiB
in the local milestone handoff tree before the transfer preparation. The retained
transfer plus its validation copy add approximately 914 MiB. Retained six-image
unpacked layer sizes are about 1.50 GiB from S03; no new image build/cache was added.
These owned working data remain below 25 GiB; neither a whole-host disk census nor
a measured workload peak is claimed. Actual mount inspection shows only generated
secret files, extracted demo initialization resources and owned DB volumes.
All five containers, project networks and both volumes were removed after browser
smoke; zero project containers/volumes remained. Generated local secrets were deleted.
Existing S03 images and all foreign Docker resources were retained.

## Representative browser evidence

Mechanic: existing `playwright-cli`, isolated session `ms001s04`, Chromium desktop
1280x720. Target: `http://127.0.0.1:55002/`, unauthenticated shipped Foundation shell.
Observed `API readiness: ready` and exact application version; browser `fetch` to
`/api/health/ready` returned 200 with `status=ready`. Clicked the observed
`Open local documentation` link and reached the packaged documentation page.
[Web screenshot](web.png), [docs screenshot](docs.png),
[network](browser-network.txt), [console](browser-console.txt).
All 17 observed requests returned 200, including docs search/worker/locale assets.
Console: zero errors/warnings. Browser session closed. No account, product journey,
TLS, mobile layout or broad accessibility qualification is claimed. No UI source
was changed. Packaging browser smoke: passed; stage readiness: not ready due to AMD64.

## Verification

Commands ran in the repository with `source scripts/activate-toolchain.sh`:

- `uv run --locked python -m tools.custometry_quality.stage_ledger preflight --ledger .codex/delivery/ledgers/MS-001.md --stage MS-001-S04`: passed; S04 already allowed under DEC-13.
- Normal `claim` with that returned hash: passed; this session owns S04. No foreign claim was used.
- `uv run --locked python -m tools.custometry_quality.delivery_consumer --source /Users/daniildegtyarev/.local/share/custometry/delivery/MS-001/0.1.0-internal.20260908.s03.3 --work /Users/daniildegtyarev/.local/share/custometry/delivery/MS-001/s04-consumer-arm64-01 --trust .codex/delivery/evidence/MS-001/MS-001-S03/protected-files.json --architecture arm64 --keep-for-browser`: passed; exact runtime result linked above.
- `uv run --locked pytest -q tests/tooling/test_delivery_consumer.py tests/tooling/test_delivery_bundle.py tests/tooling/test_delivery_bundle_producer.py`: [101 passed](tests.txt), including 92 unchanged producer/release checks.
- `uv run --locked pytest -q tests/tooling/test_delivery_consumer.py`: [9 passed](consumer-tests-final.txt) after the final destination-symlink guard and formatting changes. No runtime-affecting code changed after the passing runtime run.
- `uv run --locked ruff check tools/custometry_quality/delivery_consumer.py tests/tooling/test_delivery_consumer.py`: [passed](ruff.txt).
- `uv run --locked pyright tools/custometry_quality/delivery_consumer.py`: [zero errors](pyright.txt).
- [Actual negative probes](actual-negatives.json): changed archive SHA, changed platform, escaping image path and missing Compose payload all rejected by the retained reader. No hostile fixture was imported or run.
- [Transfer preparation](transfer-preparation.json): actual 478,787,131-byte transfer ZIP unpacked locally and every retained file hash matched; workflow YAML parsed. Hosted execution/denial remain `not_run`.
- `uv run --locked python -m tools.check --scope local`: see [source profile](local-profile.txt); this verifies source/docs, not native AMD64 or installation.

Initial pyright found an inferred empty-list type in the new harness; explicit
annotation fixed it. An initial ad-hoc platform-negative probe accidentally assigned
the existing platform and therefore did not reject; the corrected probe selects the
opposite actual architecture and rejects. Neither initial attempt is reported as a
passing negative test. There was no observed application packaging regression.

## Contract impact and remaining criteria

Applied `contract-impact-analysis` to the new CLI, extraction, test resources and
prepared remote interaction against accepted S03. Inspected delivery producer,
retained Compose, lifecycle helpers, existing workflow and their direct docs/tests.

| Surface | Classification and basis |
|---|---|
| Existing release/internal reader, manifest/Compose schema, API, Web, migration source and dependencies | `none`: no edits; exact image/reader identities retained; existing release tests pass |
| New consumer CLI and bounded local extraction | `compatible-change`: separate opt-in command, new owned directory only, no change to supported producer/reader calls; hostile-path and partial-promotion tests pass |
| New GitHub draft bridge / runner import interaction | `unknown`: prepared only; actual credential visibility, engine archive identity support and runtime need hosted verification |

| Criterion | Actual contribution / gap |
|---|---|
| AC-01 | Core/demo resources and packaged paths work on ARM64; AMD64 remains open |
| AC-03 | Native ARM64 passes; native AMD64 has not run, so criterion is unsatisfied |
| AC-04 | Trusted source/profile/file/image checks plus relevant hostile input fixtures pass |
| AC-05 | Fresh/repeat packaged migration to declared head passes on ARM64; AMD64 remains open |
| AC-06 | Protected fresh local copy and safe extraction pass; proposed remote success/denial remains unobserved |
| AC-07 | ARM64 imports, readiness, assets and Edge plus one actual-browser smoke pass; AMD64 remains open |
| AC-09 | Actual sizes and one-run durations recorded; remote timing remains unobserved |

S03 notices and report-only license findings are unchanged. SBOM/vulnerability scan
status remains `not_observed`; no official-release, legal/security clearance or
redistribution waiver is inferred. Product SEC-009/012 and OPS-001/002 meaning is
unchanged. No custom dependency build, registry, runner fleet or new account exists.

## Owned changes and documentation synchronization

Added `tools/custometry_quality/delivery_consumer.py`,
`tests/tooling/test_delivery_consumer.py`, `.github/workflows/verify-internal-bundle.yml`
and this evidence directory. The new harness/test files fall within S04's declared
isolated delivery integration evidence zone. Updated only the S04 documentation
sections and version 19 in `docs/architecture/runtime-network-installation.md` and
`docs/architecture/tooling-gates.md`, preserving prior S03 changes in those mixed files.
Only the exclusive updater changes the journal's claim/pause state.

Foreign pre-existing changes excluded: S03 producer and tests, internal profile and
S03 evidence; S04/S05 prompt amendment, plan, parent/architecture index; retired Figma
prompt deletion. No stage-owned Git publication, branch, worktree or subagent was made.
Plan 2.2.0, WS-001 1.0.6 and architecture registry reciprocal bindings stay intact.
No new planning node, product requirement or provider milestone is introduced;
parent contracts therefore need no semantic revision. Runtime/tooling docs link this
report and its workflow/operation, and this report links the current plan/journal.
The generated contributor index is unchanged and its check passes. S03 accepted
report/receipt and original handoff bytes were preserved.

## Next safe action

Resolve only the named temporary draft bridge decision in [remote-operation.md](remote-operation.md).
Resume this same stage under its original claim, publish the prepared owned workflow
through the protected PR route, upload the exact archives, and observe native AMD64
verification and anonymous denial. Remove the draft after evidence retrieval. Diagnose
only a concrete remote failure. Accept via a new immutable ready receipt only after
all mandatory proof is complete; none is fabricated for this partial report. S05
remains unavailable. No new server is requested.
