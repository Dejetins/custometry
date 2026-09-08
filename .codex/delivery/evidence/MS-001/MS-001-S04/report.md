# MS-001-S04 — Native internal-bundle consumer qualification

Plan [MS-001 2.2.0](../../../../../docs/architecture/planning/milestones/MS-001/plan.md).
The [canonical journal](../../../ledgers/MS-001.md) alone owns execution state.
Mode: `manual_sequential`; scope: S04 only. Native ARM64 and AMD64 qualification
is complete at the boundaries below. S05 is the next entry candidate; it is not
executed here and owns final owner acceptance of the C03 handoff.

## Exact subjects and successful targets

Retained bundle: `0.1.0-internal.20260908.s03.3`, profile `internal-development`.
Owner-local acquisition root:
`/Users/daniildegtyarev/.local/share/custometry/delivery/MS-001/0.1.0-internal.20260908.s03.3`.
Image source: `bc347d7e74c57640b42462c24cc2ed60d76ef055`.
Manifest SHA-256: `693cbe3b4dfcd5148c9aab6dd2b1e946d9b46ae0ce3c22a69b4a03111f1a735a`.
Portable ZIP SHA-256: `6687d2a58ef194072634b462a7ab8750fcca3f32a47c81fd8989c3498dd77e49`.
The [trusted inventory](transfer.json) binds all six image archives and every
independently selected S03 toolkit file. All checks precede reader execution/import.
No image, application dependency, original Compose/migration payload or S03 artifact
was rebuilt or changed. Containers have no source-checkout mounts or registry pulls.

| Native target | Actual evidence |
|---|---|
| M5 Docker Desktop, Linux `aarch64`, Docker 29.6.2, containerd store, 18 visible CPUs, 8,319,213,568 allocated bytes | [Corrected ARM64 result](arm64-corrected-result.json); new task directory `s04-consumer-arm64-03`, project `ms001s04-3494596a4f` |
| GitHub `Dejetins/custometry`, `ubuntu-24.04`, Linux `x86_64`, Docker 28.0.4, containerd store, 4 CPUs, 16,765,374,464 allocated bytes | [Run 34275373622](https://github.com/Dejetins/custometry/actions/runs/34275373622), [AMD64 result](amd64-final/ms001-s04-consumer/result.json), [store evidence](amd64-final/ms001-s04-store-observation.json), [run/commit/artifact identity](hosted-final-run.json) |

Both targets imported their exact API/Web/PostgreSQL archives, started five healthy
core/demo services, read 5,000 seeded receipts as `demo_reader`, ran packaged Alembic
on a fresh control database to `0009_notifications`, and repeated the upgrade
successfully. Required API imports passed. Edge, API readiness, shipped JS/CSS and
public documentation returned 200. The ARM64 engine already held image bytes;
its acquisition directory and DB volumes were fresh. AMD64 used a fresh hosted
consumer and selected image store. Neither result qualifies arbitrary engines.

## Retrieval, size and single-run observations

The authorized unpublished draft `ms001-s04-transfer-20260908-01` contained one
478,787,131-byte `transfer.zip`, SHA-256
`c89759d1459ec2e09f4e89b08b10cf725df0357fc04f63ec6268cb6d1cdb1b77`.
GitHub [upload evidence](remote-upload.json) confirms release `385035881`, asset
`551236330`, uploaded state, size and digest. Authenticated runner retrieval/hash
verification succeeded; representative anonymous access returned 404 locally and
on the runner. [Transfer observation](amd64-final/ms001-s04-transfer-observation.json)
records 3.379 s for download plus outer hash/extraction. No credential or signed
redirect URL is retained. The [owner authorization](owner-resolution-01.md)
resolved the earlier [prepared-operation pause](remote-operation.md).

| Final-run observation | ARM64 seconds | AMD64 seconds |
|---|---:|---:|
| Verified local acquisition copy | 0.434 | 0.775 |
| Payload/image reader verification | 0.206 | 0.364 |
| API / Web / PostgreSQL import | 0.725 / 0.191 / 0.740 | 7.777 / 5.582 / 2.482 |
| Core/demo database startup | 5.698 | 11.035 |
| Fresh migration | 2.740 | 4.718 |
| Repeat migration | 2.655 | 4.422 |
| API/Web/Edge startup | 17.448 | 17.598 |

Each consumer copied 478,784,861 verified bytes before extraction. S03 retains six
image archives totaling 476,247,552 bytes and a 2,421,201-byte portable ZIP. These
are single-run observations on different machines, not comparative performance or
peak certification. Docker stats sampled about 137.215 MiB aggregate on final ARM64
and 131.913 MiB on final AMD64. Configured service caps, including migration, total
3,154,116,608 bytes, below 6 GiB. Engine allocation is distinct from workload use.

The local milestone tree after retained attempts/transfer validation occupies
3,764,380 KiB (`du -sk`). Six retained images have about 1.50 GiB of unpacked layers
from S03, with no new image build/cache. Earlier [mount/data observations](arm64-resource-observation.json)
record the disposable volume paths and baseline sizes; final run BlockIO is in
its stats. Hosted work contains two copies of the sub-0.5-GB transfer plus the
verified images and tiny disposable databases. The bounded operation fits the
25 GiB owned-data ceiling; a full host census or peak-disk measurement is not claimed.

All owned Compose projects/volumes were removed. Final local zero-container and
zero-volume postconditions were checked by project label, and generated secrets
were deleted. Hosted cleanup succeeded; the disposable runner removed transfer and
secret files. [Remote cleanup](remote-cleanup.json) confirms the draft/asset were
deleted and an authenticated follow-up lookup returned 404. Only the redacted
Actions observation artifact remains: ID `10075519806`, expiry
`2026-12-07T20:32:17Z`, requested retention 90 days. The owner-local S03 copy remains
the actual acquisition endpoint; the deleted draft is not a live download location.

## Browser proof

One actual `playwright-cli` Chromium session, `ms001s04`, desktop 1280x720, opened
`http://127.0.0.1:55002/` through packaged Edge. The shipped shell showed
`API readiness: ready` and the exact application version; browser fetch of
`/api/health/ready` returned 200/ready. Clicking `Open local documentation` reached
packaged `/docs/`. All 17 observed requests returned 200, including docs search,
worker, locale and stylesheet assets. Console had zero errors/warnings.
[Web](web.png), [docs](docs.png), [network](browser-network.txt), [console](browser-console.txt).
The session was closed. This evidence remains valid for unchanged image bytes;
subsequent corrections only affect host store, mount permissions and demo secrets.
No account/TLS/product-journey, mobile or broad accessibility verdict is inferred.

## Failures, corrections and tests

[Runtime corrections](runtime-corrections.md) preserves failed runs and causal
observations. The first runner store lost manifest-ID lookup; enabling the standard
containerd store resolved it. Extracted demo permissions then denied PostgreSQL
access; restoring the validated mount modes removed that error. Finally URL-safe
secret generation violated the packaged 64-hex contract; hex generation plus an
actual demo-reader row-count assertion resolved initialization. The original
ARM64 health-only observations do not prove seeded demo completeness; final proof
uses the corrected runs above. [Initial partial report](report-partial-01.md) remains
historical evidence. No failed/cancelled attempt is counted as a pass.

Commands run from the activated repository toolchain:

- `uv run --locked pytest -q tests/tooling/test_delivery_consumer.py tests/tooling/test_delivery_bundle.py tests/tooling/test_delivery_bundle_producer.py`: [101 passed before runtime corrections](tests.txt), including the unchanged 92 producer/release tests.
- `uv run --locked pytest -q tests/tooling/test_delivery_consumer.py`: [10 passed with the mode regression](consumer-tests-corrected.txt). The final secret/seed behavior is directly proved by both native PostgreSQL runs.
- `uv run --locked ruff check tools/custometry_quality/delivery_consumer.py tests/tooling/test_delivery_consumer.py`: [pass](ruff-complete.txt).
- `uv run --locked pyright tools/custometry_quality/delivery_consumer.py`: [zero errors](pyright-complete.txt).
- [Actual negative probes](actual-negatives.json): changed archive digest/platform, escaping archive path and missing Compose reject. Tests additionally cover ZIP traversal, symlinks, duplicates, corrupt partial extraction, limits and existing identity overwrite. No hostile fixture was imported/run.
- [Transfer preparation](transfer-preparation.json): actual outer ZIP unpacked locally and all retained file hashes matched; workflow YAML/embedded Python syntax passed. Final hosted evidence supersedes its historical `not_run` fields.
- `uv run --locked python -m tools.custometry_quality.delivery_consumer --source <complete-S03-root> --work <new-owned-directory> --trust .codex/delivery/evidence/MS-001/MS-001-S03/protected-files.json --architecture arm64`: final local invocation used `s04-consumer-arm64-03`. Hosted exact command/ref is in the bound run, using the same harness and `--architecture amd64`.
- `uv run --locked python -m tools.check --scope local`: [final local profile](local-profile-complete.txt), source/docs boundary only.
- `uv run --locked python -m tools.custometry_quality.check_docs_links`: [pass](docs-links-complete.txt) after the final current-plan link correction.
- Protected GitHub Foundation CI for PRs #60/#61 is separate from exact-archive runtime proof; [publication records](publication.json) confirm both PRs merged with green Foundation gates.

## Criterion and contract map

| Criterion | Bounded result |
|---|---|
| AC-01 | Core, optional demo, configuration, initialization resources and packaged assets run on both native targets |
| AC-03 | Native ARM64 and AMD64 API/Web/PostgreSQL import/start pass for exact S03 archives |
| AC-04 | Independent trust, profile/source and all file/image hashes checked before execution; relevant negative cases reject |
| AC-05 | Packaged migration and configuration match; fresh and repeated upgrade reach declared head on both platforms |
| AC-06 | Protected owner-local copy plus actual authenticated transfer/anonymous denial; safe extraction; temporary remote object deleted |
| AC-07 | Imports, readiness, JS/CSS/docs and Edge pass on both targets; one actual packaged-browser smoke passes |
| AC-09 | Actual bytes, single-run timings, sampled resource use and explicit unobserved limits retained |

`contract-impact-analysis`: existing release/internal reader, API/DTO/domain,
image/dependency and migration contracts have impact `none` because their exact
bytes/calls remain unchanged. The opt-in consumer and host resource preparation
are `compatible-change` for the selected internal profile: they add a separate
command, protect existing destinations and match the retained init contract.
Classic image-store consumption is unsupported by these observations; C03 must
check containerd store availability. The final runner interaction is observed,
not inferred from a mock or ordinary source-rebuild CI.

S03 upstream notices/license findings remain report-only. SBOM/vulnerability status
remains `not_observed`. SEC-009/012 and OPS-001/002 meaning is unchanged. No legal,
security-clear, official-release, installation, TLS or bootstrap claim is made.

## Owned paths and handoff

Published implementation: `tools/custometry_quality/delivery_consumer.py`,
`tests/tooling/test_delivery_consumer.py`, `.github/workflows/verify-internal-bundle.yml`
and this directory's `transfer.json`. Updated local canonical docs:
`docs/architecture/runtime-network-installation.md` and
`docs/architecture/tooling-gates.md`, version 19, preserving their foreign S03 hunks.
Added immutable observations/reports in this evidence directory. Only the exclusive
updater owns journal claim, pause, resume and receipt-backed acceptance.

Pre-existing S03 producer/tests/profile/evidence, S04/S05 prompt/plan/parent/index
amendments and retired Figma-prompt deletion remain excluded from S04 publication.
No broad staging, stash, worktree, subagent or later-stage execution occurred.
The local checkout is synchronized with the merged implementation while preserving
foreign changes. Both temporary local/remote branches are deleted; final main commit
is `c3ae01eebc2a8f010ec2c10c51281bc2c4078e1a`. Source/docs hashes are in
[the final file manifest](changed-file-hashes-complete.json). S03 accepted reports/receipts and bundle bytes are unchanged.

The existing plan 2.2.0 / WS-001 1.0.6 / architecture index reciprocal bindings remain
valid. No new planning node or product requirement was introduced. Runtime/tooling
docs link the current report, workflow and acquisition constraints. Generated docs
index needs no content change. S05's actual plan, report, schema, policy, producer
and predecessor inputs exist; its own final owner-acceptance checkpoint remains.
Stop after S04 acceptance and next-entry validation; do not claim S05 or begin C03.
