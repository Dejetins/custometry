# MS-001-S02 — Portable candidate packaging

Stage: `MS-001-S02`; execution mode: `manual_sequential`.
The [journal](../../../ledgers/MS-001.md) alone owns execution state.
Plan: [MS-001 1.1.0](../../../../../docs/architecture/planning/milestones/MS-001/plan.md).
Executor: actual `CODEX_THREAD_ID=01a07dc8-dc34-7741-aa7b-d1c96e7f08b8`.

## Result and authority

The S02 packaging contribution is complete: bounded candidate assembly/validation,
portable configuration, source-bound image inventories and actual clean-source
API/Web builds for ARM64 and AMD64. The exact tracked build commit is
`bc347d7e74c57640b42462c24cc2ed60d76ef055`; application version is
`0.1.0-dev.0+sha.bc347d7e74c5`. The clean archive contains 340 declared build files,
with no uncommitted overlay or checkout mount. All four builds and required local
image probes pass. This is candidate packaging proof, not an accepted release.

The missing Git authority was resolved by the owner's
[2026-09-08 instruction](owner-resolution-2026-09-08.md). The original claim resumed
through the ledger CLI. [PR #55](https://github.com/Dejetins/custometry/pull/55)
published only the scoped S01/S02 delta and clean-build evidence, with all required
Foundation CI jobs successful. Protected-main merge commit is
`2090b366c01ff8d5f8e807b3b468f5eff6092eda`.
[Publication evidence](iteration-02/publication.json) binds the observed head,
merge, checks and empty review-thread inventory. Normal GitHub CI effects are
within authority; no manual image/bundle publication or deployment was performed.
This report and its new ready receipt are the evidence-only closure publication.

## Changed paths and preservation

S02 changes these product/tooling/documentation paths plus its evidence directory
and CLI-owned journal transitions:

- `apps/api/Dockerfile`: immutable frontend pin, project license, no generated `.pyc` layer.
- `apps/web/Dockerfile`: immutable frontend pin, deterministic Web/docs notices and project license.
- `deploy/compose/collect-web-notices.mjs`: installed-package notices, reporting missing text.
- `deploy/compose/compose.candidate.json`: finite core/migration/optional-demo topology without build directives.
- `deploy/compose/delivery-image-inventory.json`: exact required source/asset/migration bindings.
- `tools/custometry_quality/delivery_bundle.py`: capture, assembly, strict semantic closure, projection, packing and actual image-file observation.
- `tests/tooling/test_delivery_bundle_producer.py`: inventory, hostile substitution, portable Compose, copied-toolkit and deterministic round-trip proof.
- `docs/architecture/runtime-network-installation.md`: candidate contract and completed source-build evidence, doc_version 11.
- `docs/architecture/tooling-gates.md`: focused commands and size evidence semantics, doc_version 11.

No source file was deleted. S01 schema/policy/reader/tests and all accepted S01
report/evidence/receipt bytes remain unchanged; publication merely committed those
existing inputs. Active plan, prompts and stage contracts remain unchanged.
The pre-existing deletion of
`.codex/agents/generated/w21-figma-master-elements-index/internal-figma-agent-prompt.md`
is foreign and excluded. Pre-existing local-only governance commits remain local;
the scoped publication branch starts at the actual remote base and includes no
such commits. Local preservation merges are not publication inputs. Canonical
checkout synchronization must preserve this history before deleting technical
branches. No worktree, clone, stash, subagent or Goal was created.

The old report is preserved byte-for-byte at
[report-pause-2026-09-08.md](report-pause-2026-09-08.md), SHA-256
`a71b27cfc05d4b12fd6c27fa02508d1fc55ed7de4cc02a3290bb4eb95583c7be`,
and at its original path in commit `475ef389dbb291f4f27f11ed069ef56819ba5608`.
The [old pause receipt](receipts/2026-09-08-s02-pause-01.md), old hash manifests,
uncommitted-preparation evidence and failed-check observations were not rewritten.
Their original report-path bindings describe those historical bytes, not this
replacement report. New clean-source evidence is under `iteration-02/`.

## Contract impact and criterion coverage

Requirements: SEC-009/012/016/017/018, OPS-001/002, SCALE-003/004 and selected
MS-001 criteria. Network/migration separation, unavailable capabilities, candidate
status and full release gates are preserved.

| Surface | Classification and resulting behavior | Observed boundary |
|---|---|---|
| Legacy env/accepted-release bootstrap | `compatible-change`: additive candidate seam; original strict three-key parser, overlay and bootstrap unchanged | Existing valid/invalid parser tests pass; candidate output grants no release eligibility |
| Candidate record/config/resources | `compatible-change`: additive finite v1 producer and reader | Exact trusted template, migration/file/service mapping, unique identities, bounded inputs and out-of-tree Compose checks |
| API payload | `compatible-change`: license added, generated bytecode omitted, source behavior retained | Actual imports, Parquet round-trip and Alembic head pass; timing effects unmeasured |
| Web/Edge payload | `compatible-change`: notices added, application/public assets retained | Actual source/asset hashes and both Nginx config checks |
| Domain/API/identity/persistence/migrations/cache/capabilities | `none` | No corresponding source or schema change |
| Authenticated retrieval/signatures/final supply | `unknown` end to end; S03/S04 allocation retained | Local producer does not authenticate an archive or grant execution trust |

| Criterion | Completed S02 contribution | Remaining milestone proof |
|---|---|---|
| MS-001/AC-01 | Closed declared bundle/config inventory, actual image files, deterministic fixture extraction/render outside checkout | S04 hostile retrieval/extraction and final installed-artifact checks |
| MS-001/AC-02 | Exact clean tracked source commit, pinned inputs/locks and deterministic producer ZIP round-trip | S03/S05 real repeat-build comparison and immutable retrieval |
| MS-001/AC-05 | Original env compatibility, exact role/version/resource pairing, all nine migration revision/support hashes and image head | S04 fresh/repeat PostgreSQL migrations on final subjects |
| MS-001/AC-07 | Clean-image API imports, Web/docs/assets/notices and Web/Edge Nginx checks on both architectures | S04 final subject/platform/DB/browser readiness |
| MS-001/AC-09 | Preserved S01 source/protocol inputs, actual compressed and conservative unpacked image sizes | S04/S05 historical baseline, runtime/timing/browser observations and comparison |

No S02 clean-source or available image check is deferred. The remaining cells
are the accepted later-stage allocation, not milestone-wide acceptance here.

## Validation and actual images

The earlier focused suite passed 100 tests; [tests-final.txt](tests-final.txt),
[ruff-final.txt](ruff-final.txt), [pyright-focused-final.txt](pyright-focused-final.txt)
and [local-profile-final.txt](local-profile-final.txt) preserve exact results.
The unchanged code then passed the CI-equivalent source checks:

- `source scripts/activate-toolchain.sh` followed by `uv run --locked python -m tools.check --scope ci`: PASS, [evidence](iteration-02/ci-source-profile.txt).
- `uv run --locked ruff check apps/api/src migrations tests tools`: PASS, [evidence](iteration-02/ci-ruff.txt).
- `uv run --locked pyright apps/api/src tests/integration`: zero errors, [evidence](iteration-02/ci-pyright.txt).
- `uv run --locked pytest -q`: 336 passed, 15 skipped; skips are not runtime proof, [evidence](iteration-02/pytest-all.txt).
- Hosted [Foundation CI run 34165630457](https://github.com/Dejetins/custometry/actions/runs/34165630457): static/unit/contracts, disposable Compose/browser proof and required Foundation gate all success on PR head `829b1c10096e0e0f170889baf9734699b2ebf237`.

The optional expanded `uv run --locked pyright` remains failed with 33 diagnostics
in unchanged `validate_delivery_tickets.py` and `validate_route_registry.py`.
[pyright-comparison.json](pyright-comparison.json) reproduces exactly the same
normalized diagnostics at the original inspection commit using the same environment
and configuration. This is not a required passing profile and is not reported as
passed. No unrelated validator repair was included.

[source-capture.json](iteration-02/source-capture.json) records the clean archive
and each declared source hash. [clean-builds.json](iteration-02/clean-builds.json)
records the four exact build commands, source directory and successful exits.
Build inputs were rechecked unchanged after building. The build command template,
instantiated for both roles and architectures in that evidence, is:

```sh
docker build --platform linux/arm64 --load -t custometry-ms001-s02-clean-api:arm64 --build-arg CUSTOMETRY_VERSION=0.1.0-dev.0+sha.bc347d7e74c5 -f apps/api/Dockerfile .
```

[image-checks.json](iteration-02/image-checks.json) records actual source inventory,
API imports/Parquet, absence of pytest, application version, Alembic
`0009_notifications` head, and both Nginx config checks. Each architecture has
111 API file records and 94 Web file records; source bytes match the trusted
inventory. The inventories are
[API ARM64](iteration-02/api-arm64-files.json),
[API AMD64](iteration-02/api-amd64-files.json),
[Web ARM64](iteration-02/web-arm64-files.json) and
[Web AMD64](iteration-02/web-amd64-files.json).
Temporary stopped inspector containers use no source mount or implicit image pull
and are removed after observation. Existing Docker workloads/data were untouched.

| Clean image | Compressed layer bytes | Uncompressed layer-tar bytes | Existing unpacked cap |
|---|---:|---:|---:|
| API ARM64 | 105,826,444 | 355,354,112 | 367,001,600 |
| API AMD64 | 107,526,061 | 337,203,200 | 367,001,600 |
| Web ARM64 | 22,727,240 | 55,393,792 | 104,857,600 |
| Web AMD64 | 21,883,320 | 53,844,480 | 104,857,600 |

All four conservative unpacked upper bounds fit the existing caps.
[clean-images.json](iteration-02/clean-images.json) binds image IDs, rootfs layers,
labels, archive hash and method. The uncompressed total includes layer-tar metadata;
compressed local content is not registry network transfer. The engine is Linux
ARM64 (Docker 29.6.2); AMD64 execution is emulated. One immutable-byte observation
per image is sufficient for these counts and does not establish speed or native
AMD64 acceptance. The old pause report retains the measured causal bytecode-size
repair comparison; it is not a historical product performance baseline.

## Notice and downstream proof limits

The Web collector reports five installed ARM64 packages without root license text:
`@esbuild/linux-arm64@0.25.12`, `@rollup/rollup-linux-arm64-musl@4.62.2`,
`html-parse-stringify@3.0.1`, `saxes@6.0.0`, `stackback@0.0.2`.
Four are build/test-only; `html-parse-stringify` is a runtime dependency with MIT
metadata/README. Its upstream v3.0.1 commit
`ed405e32a6ad5afc583001b238a34772e7340bac` also has no LICENSE file. Available actual
notices and metadata are retained. No license text, exception or legal acceptance
was fabricated. S03 must bind the shipped-component SBOM and license resolution to
final subjects; `gate_licenses`, vulnerabilities, signatures and supply acceptance
are not claimed here.

Local build tags are not final registry subjects. Native final-image platform
proof, fresh/repeat DB migrations, authenticated retrieval, final-bundle browser
checks, runtime RAM/disk aggregates and timing samples remain S03/S04/S05 work.
The normal CI disposable Compose/browser check is real but does not establish
those final-bundle or installed-product boundaries.

## Handoff and documentation

The exact S03 prompt and its producer inputs were inspected. Producer, schema,
policy, trusted template/inventory, Dockerfiles and this report are available.
S03 requires a separate execution request and authority for its external supply
operations. It remains disallowed by this handoff; no S03 action was performed.
The new [ready receipt](receipts/2026-09-08-s02-ready-02.md) binds this live report,
plan, prompt, stage contract and actual evidence. S02 does not require a separate
owner acceptance of its finished result; Git authorization is not represented as
such acceptance.

Commands available to a later authorized producer, using actual run inputs:

```sh
python -m tools.custometry_quality.delivery_bundle capture --commit "$SOURCE_COMMIT" --output "$SOURCE_ARCHIVE"
python -m tools.custometry_quality.delivery_bundle observe-image-files --image "$API_IMAGE" --role api --output "$API_FILES"
python -m tools.custometry_quality.delivery_bundle observe-image-files --image "$WEB_IMAGE" --role web --output "$WEB_FILES"
python -m tools.custometry_quality.delivery_bundle assemble --record "$ACTUAL_METADATA" --payload "$PAYLOAD_INPUTS" --output "$ASSEMBLED"
python -m tools.custometry_quality.delivery_bundle check --record "$ASSEMBLED/delivery-manifest.json" --payload "$ASSEMBLED"
# Independent signing/verification precedes publication or execution.
python -m tools.custometry_quality.delivery_bundle pack --record "$ASSEMBLED/delivery-manifest.json" --payload "$ASSEMBLED" --signature "$SIGSTORE_BUNDLE" --output "$NEW_ARCHIVE"
```

Metadata retains all v1 fields except derived `files/services/resources`. Payload
inputs contain referenced actual evidence, notices and selected optional demo
files; the producer supplies config/env/policy. Trusted toolkit code/template and
inventory must be supplied independently of an untrusted bundle. Fixture tests
prove isolated standard-library execution and real portable Compose rendering.
`DELIVERY_CANDIDATE_PREPARED` is the only success claim; packing does not authenticate
the separately supplied signature.

Parent WS-001, plan version, triad bindings, S01 decisions and navigation remain
valid. No planning child or product decision changed. Runtime/tooling docs link
the candidate implementation and evidence. Final documentation/source checks are
captured in [closure-validation.txt](iteration-02/closure-validation.txt), and the
ledger transition is made only by its exclusive CLI before the final handoff.
