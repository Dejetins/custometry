# MS-001-S02 — Portable candidate packaging preparation

Stage: `MS-001-S02`; execution mode: `manual_sequential`.
The [journal](../../../ledgers/MS-001.md) alone owns execution state.
Plan: [MS-001 1.1.0](../../../../../docs/architecture/planning/milestones/MS-001/plan.md).
Executor: actual `CODEX_THREAD_ID=01a07dc8-dc34-7741-aa7b-d1c96e7f08b8`.
Inspection base: `d2e3c65b15f02f7970eac8c32feede3cbbd01ef9`, canonical `main` checkout.
Product comparison baseline remains `f9f39a75994d2f7a8e8d7a75df293c35579f842d`.

## Result and unresolved input

Portable configuration, deterministic bundle assembly, strict semantic validation,
source-bound image inventory, notice collection and local image checks are prepared.
This is **not an accepted S02 result**: no commit containing the S01/S02 packaging
inputs exists, and this execution explicitly lacks Git commit authority. The real
`capture` command rejects the current inputs with `DELIVERY_SOURCE_CAPTURE_REQUIRED`.
Local builds are identified as uncommitted preparation, never as clean-commit builds
or published candidates. The missing clean tracked build remains an S02 obligation.

The concrete requested decision is permission for local commit(s) on the current
canonical `main` checkout covering the reviewed S01/S02 delivery input changes and
their tests/documentation, while preserving existing history and excluding the
foreign deletion. No push, PR, package/bundle publication, credential change or
deployment is requested. Once authorized, resume this same claim, capture the exact
new commit, rebuild the selected images from its archive, repeat the affected image
and source checks, preserve this iteration and write a new report/ready receipt.
Do not accept S02 merely to move its clean-build obligation into S03.

The immutable pause receipt under `receipts/` is evidence for `stage_ledger pause`.
It is not a `prompt-pack-receipt/v1` acceptance receipt: that format requires a
finished result and passing required proof. Neither `ready` nor `review_ready` is
truthful for the incomplete source-build boundary. A new valid acceptance receipt
must be created after the missing decision and actual checks.

## Changed paths and preserved work

S02 changes only these product/tooling/documentation paths, plus this stage's
evidence directory and CLI-owned journal transitions:

- `apps/api/Dockerfile`: immutable frontend pin, project license, no generated `.pyc` layer.
- `apps/web/Dockerfile`: immutable frontend pin, deterministic Web/docs notices and project license.
- `deploy/compose/collect-web-notices.mjs`: installed-package notices, with missing text explicitly reported.
- `deploy/compose/compose.candidate.json`: finite core/migration/optional-demo topology without build directives.
- `deploy/compose/delivery-image-inventory.json`: exact required source/asset/migration file bindings.
- `tools/custometry_quality/delivery_bundle.py`: capture, assembly, projection, closure, packing and image-file observation.
- `tests/tooling/test_delivery_bundle_producer.py`: source-inventory, semantic, portable Compose, copied-toolkit and producer round-trip proof.
- `docs/architecture/runtime-network-installation.md`: doc_version 10, additive candidate implementation contract.
- `docs/architecture/tooling-gates.md`: doc_version 11, focused commands and image-size evidence semantics.

The additional collector, template, inventory and focused test file are within
the stage's packaging/asset/tooling zones. The new test file preserves S01 tests
byte-for-byte and keeps this iteration's proof separate. No source file was deleted.
All S01 report/evidence/receipt files and its schema/policy/reader/tests were retained.
The pre-existing architecture-index edit and all local commits were preserved.
The deletion of `.codex/agents/generated/w21-figma-master-elements-index/internal-figma-agent-prompt.md`
is foreign, unmodified and excluded. Existing runtime/tooling document edits from
S01 were retained before adding S02 sections; no active plan or prompt was amended.
No worktree, clone, branch, subagent, Goal, commit or external write was created.

## Contract impact and criterion coverage

Requirements: SEC-009/012/016/017/018, OPS-001/002, SCALE-003/004 and the selected
MS-001 criteria. Machine/human clauses and accepted runtime source were consulted.
Their MUST/SHOULD modality, network separation, migration separation, capability
unavailability, internal-candidate status and full release gates are preserved.

| Surface | Before / after and classification | Evidence / limit |
|---|---|---|
| Legacy env consumers and accepted-release bootstrap | `compatible-change`: additive candidate seam; original parser, three-key projection, release overlay and bootstrap unchanged | Existing valid/invalid parser tests pass; candidate output never grants release eligibility |
| Candidate record, configuration and resource reader | `compatible-change`: additive finite v1 implementation | Exact template comparison, full migration/file/service mappings, unique identities and bounded input checks; future versions fail closed |
| API image payload | `compatible-change` for source/import behavior: license added, generated bytecode omitted | Local imports, Parquet round-trip and Alembic head pass; startup timing effect is unmeasured |
| Web/Edge artifact | `compatible-change` for packaging: notices added, application/public asset bytes retained | Actual image source hashes and Nginx checks; visual/browser fidelity remains S04 |
| Domain/API/identity, persisted schema, migrations, cache, feature readiness | `none`: no corresponding source change | No installed DB, rollback, TLS/bootstrap or business capability completion is claimed |
| Authenticated provider retrieval/signatures/final subject supply | `unknown` end to end, allocated to S03/S04 | This local producer does not authenticate a signature, download an archive or grant execution trust |

| Criterion | Actual S02 preparation | Still required before the applicable completion claim |
|---|---|---|
| MS-001/AC-01 | Deterministic bundle payload and complete declared configuration; actual image files checked against trusted inventory | S02 clean-commit rebuild; S04 hostile retrieval/extraction and installed artifact checks |
| MS-001/AC-02 | Pinned frontend/bases/locks, clean-source capture guard and deterministic ZIP fixture round-trip | S02 exact recorded candidate commit/build; S03 real repeat-build comparison |
| MS-001/AC-05 | Original env compatibility, exact role/version/resource pairing, all nine migration revisions/support hashes | S02 clean-image recheck; S04 fresh/repeat PostgreSQL migration proof |
| MS-001/AC-07 | Actual local imports, required Web/docs/assets/notices and Nginx configuration | S02 clean-image recheck; final subject readiness/platform/DB/browser evidence remains S04 |
| MS-001/AC-09 | Real compressed/uncompressed image measurements and preservation of S01 comparison inputs | Source-built historical baseline and complete runtime/timing/browser samples remain S04; no new speed threshold |

## Observed checks

[validation.txt](validation.txt) records 100 passing focused tests and passing Ruff.
The additional full `uv run --locked pyright` check fails with 33 diagnostics in
`validate_delivery_tickets.py` and `validate_route_registry.py`. A clean archive of
the inspection commit, same Python environment and same Pyright configuration
reproduces exactly the same normalized diagnostics; see
[pyright-comparison.json](pyright-comparison.json). Those existing validators were
not changed. This expanded check remains **failed**, not silently waived or repaired
outside S02. Focused Pyright for S02 passes in
[validation-runtime.txt](validation-runtime.txt), which also records actual image
probes and the rejected source capture. The final grouped source profile is recorded
separately after documentation synchronization.
The observed final `check --scope local` result is `PASS` in
[local-profile.txt](local-profile.txt); `generate_docs_index --check` also passes.
After the final source and documentation changes, the same scoped checks passed
again: [100 tests](tests-final.txt), [Ruff](ruff-final.txt),
[focused Pyright](pyright-focused-final.txt) and [local profile](local-profile-final.txt).
Final source bytes are bound in [source-inputs-final.json](source-inputs-final.json).

Docker Desktop initially had no socket. `docker desktop status` reported it stopped;
the authorized reversible `docker desktop start --timeout 45` succeeded. Observed
engine: 29.6.2, `aarch64`, 8,319,213,568 bytes engine memory. Docker's existing
containers/volumes/images were not removed or started. Each inspection container
was created by this run and removed after use. The engine remains available.
Docker/Compose availability is no longer the reason for the source-build pause.

ARM64 API and Web builds use application version `0.1.0-dev.0+s02.preparation`.
[local-images.json](local-images.json) records local identities, not remote OCI
platform provenance. [api-files.json](api-files.json) contains 111 actual image file
records; [web-files.json](web-files.json) contains 94. Required source bytes,
eleven public SVG assets, help index, generated docs/search/CSP and notice files
were observed. The standalone copied standard-library reader and real Compose CLI
rendering outside the repository pass in tests, using explicitly synthetic subjects.
No synthetic fixture was represented as an image, supply or runtime observation.

| ARM64 measurement | Before bytecode repair | After repair | Criterion / observation |
|---|---:|---:|---|
| API compressed layer bytes | 115,010,255 | 105,825,956 | Local stored content; not registry transfer bytes |
| API streamed uncompressed layer-tar bytes | 381,197,312 | 355,354,112 | Conservative upper bound including tar metadata; below 367,001,600 after repair |
| Web streamed uncompressed layer-tar bytes | 55,403,008 | 55,403,008 | Before final deterministic notice-order rebuild; final measurement recorded separately; limit 104,857,600 |

These are exact byte counts, one observation per immutable local image; sample
spread is not a meaningful statistic for the same bytes. The only API source change
between these two measured builds is `UV_COMPILE_BYTECODE=1` to `0`: generated `.pyc`
files accounted for 24,756,364 payload bytes. Total uncompressed layer-tar reduction
is 25,843,200 bytes (including metadata). Import and Parquet checks were repeated.
This is an S02 local repair comparison, **not** the S01 historical baseline or a
startup/performance result. The legacy `Size`-field check alone would have missed
the initial unpacked cap violation on this image store. Compressed layer bytes,
uncompressed bytes and actual network downloads are distinct measurements.

## Notice and proof limits

The Web notice collector reports no unknown declared license identifiers, but
five installed ARM64 packages have no root license text: `@esbuild/linux-arm64@0.25.12`,
`@rollup/rollup-linux-arm64-musl@4.62.2`, `html-parse-stringify@3.0.1`, `saxes@6.0.0`
and `stackback@0.0.2`. The collector deliberately includes build/test dependencies;
four are not Web runtime dependencies. `html-parse-stringify` is a runtime
dependency. Its installed metadata/README declare MIT; the upstream `v3.0.1` tag
resolves to `ed405e32a6ad5afc583001b238a34772e7340bac`, and a read-only GitHub contents
query at that commit also returned no LICENSE file. No license text, exemption or
legal acceptance was fabricated. S03 must bind the actual shipped-component SBOM,
license findings and required notice resolution to final subjects. This preparation
does not claim `gate_licenses`, SBOM, vulnerability or signature acceptance.

Actual authenticated bundle retrieval, native AMD64 host proof, fresh/repeat DB
migrations, browser fidelity, runtime RAM/disk aggregates and timing samples were
not performed here. Emulated cross-platform preparation is labeled separately.
No images/bundles were published, and no host installation or existing data changed.

### Final local cross-platform preparation

Both architectures were built from the reviewed uncommitted preparation, with
locked dependencies and pinned base/frontend images. The final Web rebuild sorts
Python notice distributions/files deterministically; earlier local Web evidence
above is preserved. [local-images-final.json](local-images-final.json) binds all
four final local identities. [image-validation-final.txt](image-validation-final.txt)
records successful source-file observations, API imports/Parquet and Alembic heads,
and both Nginx configuration checks for each architecture. Native engine platform
is ARM64; AMD64 execution is explicitly **emulated**, not S04 native-host proof.

| Final local image | Compressed layer bytes | Uncompressed layer-tar bytes | Existing unpacked cap |
|---|---:|---:|---:|
| API ARM64 | 105,825,956 | 355,354,112 | 367,001,600 — below cap |
| API AMD64 | 107,526,279 | 337,203,200 | 367,001,600 — below cap |
| Web ARM64 | 22,728,714 | 55,403,008 | 104,857,600 — below cap |
| Web AMD64 | 21,884,756 | 53,853,696 | 104,857,600 — below cap |

[sizes-all-final.json](sizes-all-final.json) records method, archive size and SHA-256.
Actual network-transfer bytes and a retained signed bundle do not exist here.
The final per-architecture file lists contain 111 API records and 94 Web records.
All cross-platform Web file hashes agree except `notices/THIRD-PARTY.txt`, which
names platform-specific installed build packages. This is a file comparison, not
a browser fidelity or repeat-build verdict. The inspector never starts an image,
mounts source, or implicitly pulls a missing local image.

Final source and build evidence includes the exact commands:

```sh
docker build --platform linux/arm64 --load -t custometry-ms001-s02-api:local --build-arg CUSTOMETRY_VERSION=0.1.0-dev.0+s02.preparation -f apps/api/Dockerfile .
docker build --platform linux/arm64 --load -t custometry-ms001-s02-web:local --build-arg CUSTOMETRY_VERSION=0.1.0-dev.0+s02.preparation -f apps/web/Dockerfile .
docker build --platform linux/amd64 --load -t custometry-ms001-s02-api:amd64-local --build-arg CUSTOMETRY_VERSION=0.1.0-dev.0+s02.preparation -f apps/api/Dockerfile .
docker build --platform linux/amd64 --load -t custometry-ms001-s02-web:amd64-local --build-arg CUSTOMETRY_VERSION=0.1.0-dev.0+s02.preparation -f apps/web/Dockerfile .
```

These successful build invocations use the explicitly disclosed working source.
They cannot fulfill the remaining clean tracked commit criterion. A source archive
of the existing commit was used only to reproduce the unrelated Pyright errors;
it is neither a new checkout/clone nor the candidate build snapshot.

## Handoff and documentation synchronization

The S03 prompt and all declared input paths were inspected. Its files can consume
the new producer after S02 is actually accepted; S03 remains disallowed now.
It must not consume these local tags as final published identities or use this
report as a substitute for a completed S02 clean-source build.

Commands retained for the later authorized producer (use actual run inputs):

```sh
python -m tools.custometry_quality.delivery_bundle capture --commit "$SOURCE_COMMIT" --output "$SOURCE_ARCHIVE"
python -m tools.custometry_quality.delivery_bundle observe-image-files --image "$API_IMAGE" --role api --output "$API_FILES"
python -m tools.custometry_quality.delivery_bundle observe-image-files --image "$WEB_IMAGE" --role web --output "$WEB_FILES"
python -m tools.custometry_quality.delivery_bundle assemble --record "$ACTUAL_METADATA" --payload "$PAYLOAD_INPUTS" --output "$ASSEMBLED"
python -m tools.custometry_quality.delivery_bundle check --record "$ASSEMBLED/delivery-manifest.json" --payload "$ASSEMBLED"
# Independent S03 signing/verification precedes any publication or execution.
python -m tools.custometry_quality.delivery_bundle pack --record "$ASSEMBLED/delivery-manifest.json" --payload "$ASSEMBLED" --signature "$SIGSTORE_BUNDLE" --output "$NEW_ARCHIVE"
```

`ACTUAL_METADATA` contains every required v1 field except derived
`files/services/resources`; actual evidence records retain their exact hashes and
`evidence` role. `PAYLOAD_INPUTS` contains only referenced evidence, project/third-party
notices and optional demo init files. Generated config/env/policy are supplied by
the producer. The independently trusted toolkit selects the image inventory and
template version; an arbitrary bundle cannot replace them.

Parent WS-001, accepted plan version, triad bindings and S01 decision/source
versions remain unchanged: no new planning child, policy decision or product
requirement was introduced. Runtime/tooling docs link this implementation and
evidence; existing architecture navigation still points to the canonical journal.
The documentation index and source/link profile are checked in this iteration.
Only the supported CLI changes the journal. No next stage or milestone is started.

The requested pause is bound by the new immutable
[pause receipt](receipts/2026-09-08-s02-pause-01.md). It records the specific source
decision and all current hashes, without a fabricated acceptance status.
