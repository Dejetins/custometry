# MS-001-S03 — Internal development bundle

Stage: `MS-001-S03`; mode: `manual_sequential`. The [journal](../../../ledgers/MS-001.md)
alone owns state. Plan: [MS-001 2.1.0](../../../../../docs/architecture/planning/milestones/MS-001/plan.md).

## Result and actual boundary

Complete protected owner-local bundle: `/Users/daniildegtyarev/.local/share/custometry/delivery/MS-001/0.1.0-internal.20260908.s03.3`.
Delivery version `0.1.0-internal.20260908.s03.3`, profile `internal-development`, application
version `0.1.0-dev.0+sha.bc347d7e74c5`. Manifest SHA-256:
`693cbe3b4dfcd5148c9aab6dd2b1e946d9b46ae0ce3c22a69b4a03111f1a735a`. Portable ZIP SHA-256:
`6687d2a58ef194072634b462a7ab8750fcca3f32a47c81fd8989c3498dd77e49`.

The directory includes six retained OCI Docker image archives, portable ZIP and
unpacked payload, notices/findings, per-platform Compose env, independent toolkit
and SHA256SUMS. Directories are 0700 and files 0600, checked after final assembly.
[Protected file hashes](protected-files.json) bind the exact copy and toolkit.
Images are available entirely from retained archives; no Docker-store-only or
registry-download dependency remains. No publication, signing, official release,
security clearance, fresh database migration or full installation is claimed.

## Source and build reuse

Image source commit: `bc347d7e74c57640b42462c24cc2ed60d76ef055`. All 340 historical capture file
hashes were checked against that immutable Git commit. Current build-affecting
source/locks/Dockerfiles match that source. All four S02 local image IDs and rootfs
layer sequences match their accepted evidence. [Source reuse](source-reuse.json)
and [original actual build commands/timings](../MS-001-S02/iteration-02/clean-builds.json)
justify reuse explicitly permitted by AC-02. No new build or dependency installation
was needed. PyArrow remains upstream binary `20.0.0`; its two distribution notices
are retained. No version change, custom Arrow build, source fork or compiler graph
was introduced. Existing S02 imports/Parquet/image probes remain applicable to the
exact reused image bytes; no new IPC or broader artifact compatibility claim is made.

`source.commit` and `build_inputs` bind the application images. `producer.source_commit`
is the producer's Git baseline; its uncommitted internal-profile extension is separately
bound by exact toolkit hashes in `protected-files.json`. This does not claim that the
new producer is committed or published. The final repository producer adds only a
`list[tarfile.TarInfo]` typing annotation relative to the byte-bound retained toolkit;
its executable behavior is unchanged. API and migrate share one image, Web and Edge
share one image, control and optional demo databases share upstream PostgreSQL 17.5.
Migration head/read/write head are `0009_notifications`; all nine revision and
support-file identities are recorded in [the manifest](delivery-manifest.json).

## Identities, size and timing

[Image acquisition](image-acquisition.json) records exact archive hashes, original
engine IDs, config and platform manifest digests. The manifest uses platform manifest
IDs as `docker_id` for import and Compose; `image_id` is the separate OCI config digest.
API/Web combined index digests are null: no multi-platform registry index was published.
PostgreSQL retains its accepted upstream index digest and actual platform subjects.

| Role/platform | Archive bytes | Compressed layer bytes | Uncompressed layer-tar bytes | Save/retrieval seconds |
|---|---:|---:|---:|---:|
| api/arm64 | 105,873,920 | 105,826,444 | 355,354,112 | 1.017 |
| api/amd64 | 107,573,248 | 107,526,061 | 337,203,200 | 1.081 |
| web/arm64 | 22,763,008 | 22,727,240 | 55,393,792 | 0.282 |
| web/amd64 | 21,919,232 | 21,883,320 | 53,844,480 | 0.264 |
| postgres/arm64 | 107,318,272 | 106,646,096 | 272,513,536 | 2.242 |
| postgres/amd64 | 110,799,872 | 110,773,819 | 281,014,784 | 29.729 |

Retained image archives total **476,247,552 bytes**; ZIP is
**2,421,201 bytes**. Final verification/assembly/packing took
0.265 seconds once, excluding acquisition and notice collection.
These are observations, not a comparative benchmark. API/Web uncompressed counts
reuse exact S02 bytes; PostgreSQL counts come from [one streamed observation](postgres-unpacked-sizes.json).
The original `image-acquisition.json` PostgreSQL `unpacked_bytes` values were Docker
stored-size observations, not uncompressed size; this report and final manifest use
the corrected streamed counts. Network transfer was not separately measured. No
runtime memory/startup/migration timing is inferred. S02 build durations were 19.894,
6.372, 37.558 and 28.923 seconds for API ARM64, Web ARM64, API AMD64 and Web AMD64.
Image targets are advisory; the retained working copies stay below 25 GiB. Docker's
allocated memory was 8,319,213,568 bytes; the 6 GiB workload ceiling remains unchanged
and workload use is not measured by S03.

## Validation and limitations

- `uv run --locked pytest -q tests/tooling/test_delivery_bundle.py tests/tooling/test_delivery_bundle_producer.py`: **92 passed**, [output](tests.txt). Includes original valid/invalid release inputs, unsigned assembly/pack, unsupported reader/profile pairs and archive hash/path/config/manifest negatives.
- `uv run --locked ruff check tools/custometry_quality/delivery_bundle.py tests/tooling/test_delivery_bundle_producer.py`: pass, [output](ruff.txt).
- `uv run --locked pyright tools/custometry_quality/delivery_bundle.py`: zero errors, [output](pyright.txt).
- [Actual independent toolkit checks](actual-checks.json): final bundle and six archives pass; altered archive hash, escaping archive path, changed image digest and release profile reject. Both platform Compose files render six services and resolve to the matching local image architecture with `pull_policy: never`.
- [Actual image import](import-identity.json): all six exact archive hashes imported successfully into the existing Docker engine; original S02 tags were restored. This is not a clean-engine/native AMD64 runtime result. The engine is Linux ARM64; S04 owns native ARM64/AMD64 consumer runtime.
- New API/Web embedded-file observations are linked below; actual retained image IDs match historical builds. Archive checks stream SHA-256 and validate bounded regular OCI manifest/config blobs without extraction or execution.
- `uv run --locked python -m tools.check --scope local`: recorded in [local source profile](local-profile.txt). This is source/documentation validation only; no full release gate was invoked.

[API ARM64](api-arm64-files.json), [API AMD64](api-amd64-files.json),
[Web ARM64](web-arm64-files.json), [Web AMD64](web-amd64-files.json).

An initial owner-local `.s03` candidate used config digests for Docker lookup;
actual lookup rejected them. `.s03.2` corrected import identities but still carried
Docker stored-size values for PostgreSQL. Both preparation copies and their
[assembly observations](assembly-initial.json) / [second observation](assembly-second.json)
are retained; neither is the final handoff identity. `.s03.3` corrects both issues.
The focused type check initially reported 18 unknown-type diagnostics for an empty
list; an explicit TarInfo list annotation resolves that introduced issue. The
[initial type output](pyright-initial.txt) is preserved. Initial helper startup with system Python failed on missing PyYAML, then the project
uv environment was used; no dependency was installed. Failed intermediate attempts
are not counted as passes. Image imports were reused across the metadata-only final
revision because all six archive hashes are unchanged.

## Notices and findings

Upstream images and installed distributions retain their files unchanged. Available
application LICENSE/NOTICE text, Python package/version/license metadata, Web/docs
notices and OS package databases are copied under bundle `notices/`. PostgreSQL
upstream files remain in its archives; no image stripping was performed.
`trivy` and `syft` executables were unavailable: vulnerability/SBOM status is
`not_observed`; none was installed. Package inventories are not mislabeled SBOMs.
License results are report-only, not a legal or security approval. Python distribution
notice-file enumeration found no dist-info notice for `custometry-api`, `et_xmlfile`
2.0.0 and `openpyxl` 3.1.5; project LICENSE is retained separately. Historical Web
collector missing-text findings remain in the retained notices, including
`html-parse-stringify` 3.0.1. Missing metadata is not a fabricated pass or waiver.
The artifact remains owner-local. Applicable third-party conditions must be met
before any external redistribution; SEC-009 remains mandatory for official release.

## Contract impact and criterion map

Requirements: MS-001/REQ-01–08, SEC-009/012, OPS-001/002; existing runtime role separation
and migration contracts preserved.

| Surface | Classification | Evidence / consequence |
|---|---|---|
| Existing release schema/policy, strict env parser, candidate workflow | `compatible-change` at producer CLI; underlying release files unchanged | Original positive/negative tests pass; missing release signature rejects |
| Internal profile / local archives / Compose env | `compatible-change`, explicitly new supported interaction | New reader with old release data works; old reader with internal data rejects. Internal flag and exact toolkit required; no automatic promotion |
| API/domain/persistence/migrations/dependency versions | `none` | No source changes; exact S02 builds reused |
| Clean consumer / arbitrary Docker engines / native AMD64 runtime | `unknown` operational compatibility | Import into current engine only; S04 qualification required |

| Criterion | Bounded S03 result |
|---|---|
| AC-01 | Six services, complete configuration/demo/assets/image/migration inventory; consumer runtime remains S04 |
| AC-02 | Exact source/locks and four accepted actual builds verified for permitted reuse; six immutable retained image archives |
| AC-04 | Explicit unsigned profile, real payload/archive/OCI checks; tamper and release-reader negatives |
| AC-06 | Unique protected complete local copy, no overwrite of final identity, hash-bound toolkit, no secrets or external publication |
| AC-09 | Actual archive/ZIP/layer sizes, single-run acquisition/import/assembly observations and explicit unobserved boundaries |

## Changed paths and documentation handoff

Owned implementation paths: `tools/custometry_quality/delivery_bundle.py`,
`deploy/compose/delivery-internal-profile.json`,
`tests/tooling/test_delivery_bundle_producer.py`. Updated canonical docs:
`docs/architecture/runtime-network-installation.md` and `docs/architecture/tooling-gates.md`
(version 18), plus this evidence directory and updater-owned journal transitions.
No Dockerfile, dependency lock, product blueprint, migration, release schema/policy
or candidate workflow was changed. The foreign deletion of
`.codex/agents/generated/w21-figma-master-elements-index/internal-figma-agent-prompt.md`
is excluded. No agent, branch, worktree, Goal or external publication was created.

The plan/WS-001 parent binding and stage contracts are unchanged; no planning node
was added. Runtime/tooling docs link the new profile and report; report/journal/receipt
link back to the current triad. No product meaning or localized blueprint change is
needed. Receipt creation and acceptance use the exclusive updater only.

Exact acquisition, checksum, verification and import commands are in the
[runtime contract](../../../../../docs/architecture/runtime-network-installation.md#s03-owner-local-bundle-and-reader)
and actual-check evidence. Copy the complete protected directory including images
and toolkit; the ZIP alone is not complete. Trust the handoff manifest/SHA256SUMS from
the owner, not a checksum obtained solely from an unknown copy.

S04 inputs now exist, but S04 remains disallowed pending a current availability check
of its selected native AMD64 target and independent next-entry readiness. No remote
target was probed or used by S03. Stop after accepting S03; do not resume a controller
or launch S04. No finished-result owner acceptance is required for S03.
