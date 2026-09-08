# MS-001-S03 — Reviewable supply preparation

Stage: `MS-001-S03`; mode: `manual_sequential`; executor:
`01a07e02-12a3-7953-8c82-122b33d8d8df`. The [journal](../../../ledgers/MS-001.md)
alone owns state. [Plan 1.1.0](../../../../../docs/architecture/planning/milestones/MS-001/plan.md),
S01/S02 reports, accepted receipts and prompt contracts remain unchanged.

## Resumed execution — current boundary

The [owner resolution](owner-resolution-2026-09-08.md) authorizes the exact supply
effects and necessary repairs. The original executor resumed this same claim using
the supported ledger CLI. S03 remains in progress; no signed complete bundle or
S04 readiness is claimed. Prior report/addendum/hash records are preserved under
`snapshots/pre-resume-2026-09-08/`. The sections below retain earlier observations
and the permission packet as history, not an outstanding approval request.

Current repairs and limits are recorded in [repair boundaries](resumed/repair-boundaries.md).
The full accepted artifact name is now enforced. The default license policy is
unchanged; parsing and narrowly bound review evidence do not fabricate approval.
Diagnostic API6 ARM64 passes application imports with psycopg 3.2.9 C implementation,
system libpq 17.11 and OpenSSL 3.5.7; psycopg-binary and vendored libcrypto under `/app`
are absent. Its actual Trivy 0.74.0 final-image scan has zero CRITICAL/UNKNOWN findings.
That count does **not** establish complete security coverage: subsequent direct
inspection found statically included OpenSSL 3.3.1 in the prebuilt PyArrow 20 wheel,
which the generated image SBOM omitted. A diagnostic source build of the same
PyArrow version removes the unused Flight/cloud/encrypted-Parquet dependency edge;
its ARM64 application imports, Parquet/IPC probes and three artifact-store tests
pass. See [source-build observations](resumed/arrow-source-probe.md). Final image,
compiled dependency inventory, licensing and both native platforms remain pending.
See [diagnostic hashes](resumed/diagnostic-hashes-02.json),
[imports](resumed/api6-imports.json) and [scan summary](resumed/api6-scan-summary.json).
The input was a diagnostic snapshot with overlays, not a final clean producer run.
Earlier failed builds remain evidence; the final native matrix is pending.

Web's actual local build records 173 included modules and 20 package identities,
with all package notice texts present. A separate diagnostic SBOM scan has zero
CRITICAL/UNKNOWN findings but covers a local build directory, not a final image.
Producer and assembler now enforce runtime graph/hash coverage. Generated docs,
vendored native libraries, substantive license obligations and both native platforms
still need complete proof. The [gosu observation](resumed/gosu-applicability-observation.json)
records extracted ARM64 symbols and primary advisories; production resolution and
AMD64 applicability checks are not yet integrated.

The v2 source-part schema/policy, strict descriptor/provider/ZIP checks and trusted
local-root whole-set verifier are implemented as work in progress. At the latest
focused checkpoint, 57 companion/set tests, Ruff and Pyright pass. Real local HTTP
tests enforce an absolute deadline for slow headers/body; atomic no-replace
promotion preserves an existing empty directory. The coordinator independently
reproduced both earlier defects and confirmed the fixes on Darwin. The same 57
tests also passed in an actual read-only/no-network Linux ARM64 container,
including Linux atomic no-replace and absolute HTTP deadline behavior. Current
combined bundle/producer/supply/companion/set tests: **184 passed**; `check:local`
passed. Publisher reconciliation, actual signatures/provider parts and source-obligation
bindings are still pending. No hosted CI result or complete supply gate is inferred.

## Historical preparation boundary before owner resolution

Local implementation prepares an explicitly disabled native producer matrix,
original-subject comparison against two no-cache builds, actual scanner adapters,
strict assembly, exact source/signature verification, immutable publication
reconciliation and an explicit transport-wrapper adapter. It does not constitute
completed S03, a signed bundle, official release, native S04 runtime acceptance,
performance acceptance or installed-user acceptance. Source-level verification
is separate from unobserved hosted supply execution.

Current authority permits scoped Git publication through a technical branch,
required CI and protected main, synchronization and branch deletion. New signed
bundle production/publication and its exact artifact target need separate authority.
Both new jobs have literal `if: ${{ false }}`; merging preparation does not enable
that effect. Existing automatic Foundation candidate behavior is preserved.

## Target and effect packet

- Repository/workflow/ref: `Dejetins/custometry`, `.github/workflows/publish-candidates.yml`, `refs/heads/main`.
- Existing image packages: `ghcr.io/dejetins/custometry-api` and `ghcr.io/dejetins/custometry-web`; consume exact index outputs of the ordinary existing candidate jobs, then exact `linux/amd64` and `linux/arm64` children. PostgreSQL remains upstream `docker.io/library/postgres@sha256:5d004e058f520673f1f6edbad6b1603d5dab4c818e257c041889ef64672a8cc4`. No extra image publishing job or package is proposed.
- New proof artifacts: `custometry-supply-proof-<run_id>-<run_attempt>-amd64` and `custometry-supply-proof-<run_id>-<run_attempt>-arm64` in that repository's Actions storage, 90 days.
- New signed bundle artifact: `custometry-delivery-0.1.0-ms001.<run_id>`, following S01's `custometry-delivery-<delivery_version>` contract. No actual future run ID, artifact ID, signer result or digest is invented.
- Signing effect: GitHub OIDC `id-token: write` in the gated aggregation job, keyless Cosign v3.1.3 signature and transparency-log entry for exact manifest bytes. No long-lived signing key or credential change.
- Protected handoff target proposed for the actual verified copy: `/Users/daniildegtyarev/.local/share/custometry/delivery/MS-001/<delivery_version>/`, new directory mode 0700 and files mode 0600, retained through C03–C06. It is not created or treated as permanent remote storage by preparation.
- Required next authority: enable these two jobs and execute this specific supply path, including its proof/final Actions artifacts and signer effect, then authenticated retrieval to that protected copy. This does not request a public product release, repository visibility change, extra service or deployment.

## Transport and immutable identities

There are three non-interchangeable hashes: authenticated provider archive digest,
exact opaque inner `delivery.zip` digest, and Cosign-authenticated canonical manifest
digest. The final job publishes all three in its descriptor summary; provider ID and
expiry are read after upload. The provider wrapper contains exactly one regular
`delivery.zip`, uploaded with compression level 0. `unwrap` validates its fixed name,
regular-file type, hash, encryption/compression, size and ratio limits and expected
inner hash before creating a private new file. It never opens or extracts the inner
archive. S04 still verifies the exact signed inner archive and every payload entry,
with S01 quarantine, no recursive payload extraction and atomic promotion unchanged.

[Actual provider observations](transport-observation.json) distinguish a Docker-native
gzip `.dockerbuild` artifact from a real `upload-artifact` ZIP. Both downloaded hashes
match authenticated metadata. The initial ZIP parse of the Docker build record failed;
root cause is confirmed native gzip format, not altered transport bytes or a downloader
failure. No existing artifact was changed. The `/zip` endpoint suffix is not a format
oracle. Primary references: [pinned upload-artifact source](https://github.com/actions/upload-artifact/tree/ea165f8d65b6e75b540449e92b4886f43607fa02),
[artifact API](https://docs.github.com/en/rest/actions/artifacts), and
[Cosign v3.1.3 verification flags](https://github.com/sigstore/cosign/blob/v3.1.3/doc/cosign_verify-blob.md).

Publication checks the exact global artifact name, rejects duplicate/expired/missing
or different-byte existing content, and reuses only identical inner bytes after
validating the provider hash. Upload never overwrites/deletes an existing version.
A re-sign or changed run attempt changes bytes and is rejected for an existing version;
retry is not permission to replace a prior result. Native partial proof artifacts cannot
be accepted as a delivery. Existing artifact retention is not extended by reuse.
Actual provider expiry and a protected retained copy remain mandatory before acceptance.

## License observations

The [notice audit](notice-audit.json) observes the actual S02 Web ARM64 image config
identity and exact shipped notice hash. Its conservative 269-component inventory
includes Web notice declarations and installed APK declarations; it is not a complete
minified dependency SBOM or a final OCI-subject supply result. The actual existing
`gate_licenses` [result](notice-license-gate.json) fails against the unchanged policy.
Input is retained in [notice-audit-sbom.json](notice-audit-sbom.json).

The findings include `geoip: LGPL-2.1-or-later`, OS GPL declarations, compound license
expressions and additional identifiers outside the finite allowlist. No unknown or
review-required value was silently reclassified. `html-parse-stringify@3.0.1` remains
runtime-relevant with a missing root license text; its exact upstream commit
`ed405e32a6ad5afc583001b238a34772e7340bac` contains README and package metadata but no
LICENSE. [Upstream source](https://github.com/HenrikJoreteg/html-parse-stringify/tree/ed405e32a6ad5afc583001b238a34772e7340bac)
and [S02 evidence](../MS-001-S02/report.md) agree. Four other missing root texts are
build/test package notices. No license text, legal exception or supply acceptance
was fabricated. Final shipped-subject scanning and targeted notice/license resolution
remain required; broad dependency updates and policy relaxation are outside this unit.

## Contract impact and stage criteria

Requirements: SEC-009/012 and section 18.8, relevant MS-001/AC-02/04/06/09.

| Surface | Classification | Supported transition and evidence |
|---|---|---|
| Existing Foundation candidate and protected-main policy | `none` for enabled behavior | Existing jobs, triggers and permissions preserved; new jobs literal-disabled |
| Supply producer, CLI and provider envelope | `compatible-change` additive | New trusted transport adapter separates wrapper from unchanged v1 signed archive; legacy parser/bootstrap unchanged |
| Manifest schema, policy, signatures and original S01/S02 contracts | `none` for existing representation | Schema/policy bytes unchanged; new producer supplies actual data under those existing contracts |
| Publication/retrieval end to end | `unknown` until authorized execution | Actual provider format/hash checks exist; no S03 final artifact/signature exists |
| Domain/API/identity/cache/persistence/migrations/browser behavior | `none` | No corresponding product implementation changed |

| Criterion | Current S03 contribution | Unmet acceptance boundary |
|---|---|---|
| AC-02 | Clean-capture extension, complete filesystem comparison and two isolated native builder recipe | Two actual source-bound hosted producer runs and explained differences |
| AC-04 | Subject-bound SBOM/scanner adapters, pinned independent trust and exact signer/source verification | Actual final-subject gates, resolved license/notice findings, full shipped dependency coverage and real signature |
| AC-06 | Explicit bounded transport adapter, immutable reconciliation, concrete authenticated target | Final artifact upload, actual signed-payload retrieval and protected retained copy; S04 hostile/runtime cases |
| AC-09 | S01 measurements preserved, provider and inner bytes explicitly separated | All S04 measurement/native-platform obligations remain unchanged; no timing budget pass |

## Changed paths, checks and synchronization

Product/tooling: `.github/workflows/publish-candidates.yml`,
`tools/custometry_quality/delivery_bundle.py`,
`tools/custometry_quality/delivery_supply.py`,
`deploy/compose/collect-web-notices.mjs`,
`deploy/compose/delivery-supply-tools.json`,
`deploy/compose/install-supply-tools.py`, `tests/tooling/test_delivery_supply.py`.
The new supply module is a bounded producer/gate adapter in the prompt's existing
supply-chain touch zone. Existing producer capture now includes that adapter and
workflow so clean-source checks cannot omit them.

Documentation: `docs/architecture/runtime-network-installation.md` v12,
`docs/architecture/tooling-gates.md` v12, and
`docs/runbooks/github-repository-governance.md` v3. This report, immutable check evidence,
new pause receipt and CLI-owned advance/claim/pause are in-stage evidence maintenance.
The accepted plan, parent WS-001 links/versions, source requirements and S01 measurement
protocol do not change. No new plan, status board, ticket, Goal, subagent, worktree,
clone or stash was created. No product path was deleted.

The pre-existing retired Figma prompt deletion and local-only governance history are
preserved and excluded from publication. S01/S02 terminal rows, reports and receipts
are immutable. Required source checks and actual Git publication evidence are recorded
below before final pause; unavailable supply checks cannot be replaced with a ready
receipt. The exact S04 prompt is inspected before handoff and remains disallowed.


## Actual local supply observations — existing ff43baa8 subjects

[Pinned scanner evidence](scans/summary.json) binds actual registry index/ARM64 child
manifests, downloaded image config bytes, Docker-save archive hashes, Syft source
image IDs and the real Trivy database hash. Policy-pinned Linux ARM64 Syft/Trivy
archives were downloaded into task-owned scratch, checked against S01 hashes and
executed in the existing S02 Linux ARM64 image with no Docker socket or credentials
mounted. No project dependency version or system installation changed. Registry
reads/pulls and scanner DB downloads do not publish a new bundle.

| Existing subject | SBOM components | License findings | Critical vulnerabilities | Supply verdict |
|---|---:|---:|---:|---|
| API ARM64 | 3466 | 563 | 9 | fail |
| Web ARM64 | 1303 | 61 | 2 | fail |
| PostgreSQL ARM64 | 873 | 41 | 6 | fail |

All three subject-bound `gate_sbom` checks pass. License and vulnerability gates
fail; counts are scanner findings, not unique confirmed exploitable vulnerabilities
or adjudicated legal conclusions. Each complete gate input/result and exact affected
package/fix version is retained in `scans/`. Examples: API OpenSSL/GnuTLS plus
SQLite/Perl/zlib findings; Web OpenSSL; PostgreSQL OpenSSL and bundled Go stdlib.
Several API records have no fixed version in the selected distribution. No critical
finding is ignored, waived or reported as resolved. The frozen image/base selection
cannot be called verified supply merely because Foundation CI succeeds. A bounded
remediation/source-selection decision is required before completing supply acceptance;
this preparation does not perform broad base/dependency upgrades or alter license policy.

The initial local Docker identity assertion failed because containerd reports the
child manifest ID instead of the config ID. Actual descriptor, RepoDigests and
saved config hashes established the cause; code now handles both stores while
preserving separate child/config identities. Docker also canonicalizes the upstream
repository name to `postgres`; only that exact known alias is accepted.

Real scanner output and filesystem inventories also exposed that the S01 manifest
JSON serializer intentionally rejects multiline/Unicode strings and CVSS floats.
Using it for opaque evidence was a producer bug. Evidence now uses a separate bounded,
duplicate-rejecting JSON path; strict manifest parsing remains unchanged and regression
tests prove that distinction. No S01 schema/policy was relaxed.

Cross-platform S02 Web inventories differ only in notices for native compiler binaries
that remain in the build stage. The collector now omits only native `@esbuild/linux-*`
and `@rollup/rollup-linux-*` package notices while retaining common esbuild/rollup
upstream text and all other notices. This repairs platform-neutral manifest inventory
without removing shipped runtime code, inventing notices, or hiding remaining runtime
license-text gaps. A focused real Node fixture verifies that exact behavior; final
images incorporating this change still require the subsequent authorized producer run.

## Actual local repeat builds

[Four clean builds](rebuilds/builds.json) use published immutable source
`ff43baa87e4fed13f751831c1e9bc6b70ae0f773`, a plain trusted Git archive (not another
checkout), `linux/arm64`, exact application version `0.1.0-dev.0+sha.ff43baa87e4f`,
frozen lockfiles/base digests and separate no-cache BuildKit v0.24.0 instances at
`sha256:6eceb8971ce4fceb3daca562832642706238b7eea72941fcf9896c93c3c4a53e`.
Each role was actually built twice; all four build exits are zero. No image was pushed,
signed or deployed. Owned builders were removed after each run; existing workloads,
images and data were preserved. This is local native ARM64 rebuild evidence for the
existing source, not final new-S03-source/hosted/native-AMD64 acceptance.

Web's [comparison](rebuilds/web/comparison.json) has zero raw/content differences.
API's first [comparison](rebuilds/api/comparison.json) failed with exactly two raw
file differences. Inspection of exact bytes and
[uv 0.9.26 source](https://github.com/astral-sh/uv/blob/0.9.26/crates/uv-cache-info/src/cache_info.rs)
confirmed local build timestamp and source-directory inode cache metadata in
`uv_cache.json`; `RECORD` changes only the hash of that same metadata file. The
[reviewed comparison](rebuilds/api/comparison-reviewed.json) verifies raw hash/size
binding and normalizes only those fields, retaining every other row, owner, mode,
link and application/dependency byte comparison. It passes with zero unexplained
functional differences. Original failed evidence is preserved. Negative tests reject
changed source metadata and a tampered RECORD. No broad path-ignore rule was added.

The first inventory serialization attempt failed on valid non-ASCII filesystem
metadata; after separating evidence JSON from manifest JSON, the already completed
image was re-observed rather than rebuilt or relabeled. No failed image build was
hidden. The collector's subsequent platform-neutral notice repair is not present
in ff43baa8, so these builds do not certify that later source change; its focused
Node test and required Foundation CI are the current narrower proof.

## Verification and downstream readiness

[Exact commands and outcomes](checks/commands.json) bind the focused producer suite,
Ruff, scoped Pyright, required CI source profile, required CI Pyright, all pytest and
diff checks. Initial introduced lint/type errors were corrected; no failing gate was
weakened. The optional expanded Pyright baseline's prior 33 errors are not reclassified
or repaired by this task. Hosted Foundation CI and protected-main Git publication are
separate from the unmet supply gates and never substitute for them.

S04 entry artifacts exist syntactically, but its necessary signed descriptor, final
bundle, native AMD64 subjects/proof and authorized retained copy are not ready. S04
remains disallowed; no later stage or milestone was started. S01 timing boundaries,
5/30 sample obligations, 768x1024/1920x1080 EN/RU reference matrix and both native
platform requirements are preserved without a new timing threshold.

The new immutable pause receipt binds this report and actual evidence for the
supported CLI `pause` transition. It does not claim `ready`/`review_ready` or acceptance.
Natural-language owner decisions must cover both the exact new supply effects above
and the bounded remediation route for actual critical/license findings. Keep current
policy strict; recommended next step is targeted base/dependency and license-source
remediation, then fresh final-subject scans, rather than any blanket exception.
