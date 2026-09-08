# MS-001-S05 — Evidence acceptance and installation handoff

Plan: [MS-001 2.2.0](../../../../../docs/architecture/planning/milestones/MS-001/plan.md).
Parent: [WS-001 1.0.6](../../../../../docs/architecture/planning/directions/DIR-006/workstreams/WS-001.md).
[Canonical journal](../../../ledgers/MS-001.md); mode `manual_sequential`, S05 only.
The concrete result is ready for owner review; final acceptance is not inferred.

## Delivered result and decision packet

Accept the bounded internal supply and its [exact C03/C04 handoff](../../../../../docs/architecture/runtime-network-installation.md#s05-installation-author-handoff)?
The requested decision covers the criterion map below and the unchanged delivery
`0.1.0-internal.20260908.s03.3`, profile `internal-development`, at
`/Users/daniildegtyarev/.local/share/custometry/delivery/MS-001/0.1.0-internal.20260908.s03.3`.
Application `0.1.0-dev.0+sha.bc347d7e74c5`; source
`bc347d7e74c57640b42462c24cc2ed60d76ef055`; migration/read/write head
`0009_notifications`. Manifest SHA-256
`693cbe3b4dfcd5148c9aab6dd2b1e946d9b46ae0ce3c22a69b4a03111f1a735a`.
ZIP SHA-256 `6687d2a58ef194072634b462a7ab8750fcca3f32a47c81fd8989c3498dd77e49`.
The retained toolkit is selected by the [independent S03 inventory](../MS-001-S03/protected-files.json),
not an invented reader release tag. The complete copy includes six image archives,
portable ZIP, unpacked configuration/notices, toolkit and checksums.

Resume condition: an unambiguous owner answer accepts this reviewed bounded result,
then the original claiming session records that answer, rechecks documentation,
source/receipt bindings and creates a new immutable `ready` receipt. Until then,
the normal updater records `review_ready` / `needs_input`. No successor stage exists
inside MS-001. Acceptance completes this journal only; C03 is separately selected
installation work and does not start automatically.

## Criterion-to-evidence coverage under plan 2.2.0

| Criterion | Actual supporting evidence | Coverage and remaining boundary |
|---|---|---|
| AC-01 | [S03 manifest](../MS-001-S03/delivery-manifest.json), [S04 ARM64](../MS-001-S04/arm64-corrected-result.json), [S04 AMD64](../MS-001-S04/amd64-final/ms001-s04-consumer/result.json) | Core/demo resources, exact images, imports and packaged assets work; five healthy long-lived services plus one-shot migration. Broader declared unavailable capabilities remain unavailable |
| AC-02 | [Source reuse](../MS-001-S03/source-reuse.json), [actual S02 builds](../MS-001-S02/iteration-02/clean-builds.json), [S03 report](../MS-001-S03/report.md), both S04 results | Four successful API/Web platform builds reused at exact source/locks/image bytes; PostgreSQL upstream prebuilt subjects retained. No repeated build requirement under current plan |
| AC-03 | Both native results above; [hosted run identity](../MS-001-S04/hosted-final-run.json) | ARM64 M5 Docker 29.6.2 and AMD64 ubuntu-24.04 Docker 28.0.4, containerd store; same S03 archives, no source rebuild/emulation. ARM64 engine already contained images; hosted AMD64 consumer was fresh |
| AC-04 | [S03 actual checks](../MS-001-S03/actual-checks.json), [S04 actual negatives](../MS-001-S04/actual-negatives.json), [focused tests](../MS-001-S04/consumer-tests-final.txt), native results | Source/profile/file/image/platform checks before execution and altered hash/path/partial payload rejection. Platform negative records a KeyError rejection, not a polished user-error claim. Unsigned internal profile is explicit; release assurance not inferred |
| AC-05 | Both native results and [S04 report](../MS-001-S04/report.md) | Fresh packaged Alembic upgrade and repeat reach `0009_notifications`; strict legacy env tests reused. Unknown existing DB, installed upgrade/rollback remain unqualified |
| AC-06 | [Current availability/hash/mode check](entry-integrity.json), [transfer observation](../MS-001-S04/amd64-final/ms001-s04-transfer-observation.json), [cleanup](../MS-001-S04/remote-cleanup.json), S04 safety fixtures | Protected owner-local complete copy; authenticated exact transfer and anonymous 404 observed, finite transfer bounds; traversal/partial/overwrite rejection. Deleted temporary draft is not an endpoint; no new remote action |
| AC-07 | Both native results, [browser network](../MS-001-S04/browser-network.txt), [console](../MS-001-S04/browser-console.txt), [Web](../MS-001-S04/web.png), [docs](../MS-001-S04/docs.png) | Required imports, 5,000 seeded receipts via demo_reader, Edge/API/JS/CSS/docs 200; actual packaged Chromium smoke, 17 successful requests, zero console warnings/errors. No TLS/account/full product journey claim |
| AC-08 | [Runtime revision 20](../../../../../docs/architecture/runtime-network-installation.md#s05-installation-author-handoff), WS-001 appendix and this decision packet | Exact location, reader/hash pairing, copy/check/import commands, migration, config/secret/resource slots, platform/access/retention limits supplied. Final owner review remains pending |
| AC-09 | [S03 sizes/build observations](../MS-001-S03/report.md), [S04 timings/resources](../MS-001-S04/report.md), native JSON results | Actual single-run sizes/timings below; no repeated benchmark, peak measurement or performance certification |

## Sizes, timings and known findings

Six image archives total 476,247,552 bytes; portable ZIP 2,421,201 bytes. Actual
consumer copy is 478,784,861 bytes including selected toolkit/metadata. S02 build
seconds (API ARM64, Web ARM64, API AMD64, Web AMD64): 19.894, 6.372, 37.558, 28.923.
No build or runtime test was repeated in S05 because image bytes and proof inputs
remain unchanged. Current local availability was checked for the C03 handoff.

| Single-run seconds | ARM64 | AMD64 |
|---|---:|---:|
| Local acquisition / verification | 0.434 / 0.206 | 0.775 / 0.364 |
| API / Web / PostgreSQL import | 0.725 / 0.191 / 0.740 | 7.777 / 5.582 / 2.482 |
| Database startup | 5.698 | 11.035 |
| Fresh / repeat migration | 2.740 / 2.655 | 4.718 / 4.422 |
| Application startup | 17.448 | 17.598 |

Hosted outer download/hash/extraction was 3.379 seconds; temporary transfer size
478,787,131 bytes. These different machines/runs are not a comparative benchmark.
Sampled aggregate service memory was 137.215/131.913 MiB; configured caps including
migration total 3,154,116,608 bytes below 6 GiB. The 25 GiB owned-data ceiling remains;
S04 recorded 3,764,380 KiB for the local milestone tree, not a host-wide peak census.

Preserve [failed attempts and corrections](../MS-001-S04/runtime-corrections.md):
classic image-store manifest lookup failed, demo mount modes denied access, and an
initial secret format prevented seeding. The final corrected native runs resolve
those tested failures without changing the delivered image bytes. C03 must check
containerd store, validated mount permissions and the 64-hex demo reader secret.

SBOM and vulnerability scans remain `not_observed`; license metadata is report-only.
S03 records missing distribution notices for custometry-api, et_xmlfile 2.0.0 and
openpyxl 3.1.5 (project LICENSE retained separately), and historical Web notice gaps
including html-parse-stringify 3.0.1. No legal or security-clear verdict follows.
SEC-009 still requires official-release SBOM, vulnerability report and signed
provenance, with unresolved critical findings blocking release. Existing release
and license gates remain required before that separate boundary.

C03 owns persistent installation, M5/selected Linux VM proof, HTTPS/origin and LAN
access. C04 owns actual bootstrap/grants/authentication and account-lifetime AUTH
reconciliation. C05/C06 own recovery and full journey acceptance. Valkey/workers,
analytics writable storage and complete ingestion are not qualified here.

## Validation, documentation and ownership

Current plan/prompt/predecessor inputs and exclusive updater preflight passed;
S05 was allowed and claimed through the updater in the actual session.
Current protected files, sizes and modes match independently retained S03 hashes:
[entry check](entry-integrity.json). S03/S04 accepted reports/receipts remain unchanged.
Documentation checks and semantic binding inspection are recorded in
[checks](checks.json); these prove documentation/source bindings only, with native
runtime/browser evidence reused from S04 rather than upgraded by static checks.

Owned changes: runtime contract revision 19 to 20 (new S05 handoff section only),
WS-001 evidence appendix, architecture index row, S05 report/checks/immutable receipt,
and normal updater-owned journal transitions. Existing S03/S04 hunks in these mixed
files are preserved. The entire pre-existing dirty/untracked set, including producer,
tests, plan/prompts, prior evidence and retired Figma-prompt deletion, is excluded
from S05 ownership. No commit, publication, build, installation or subagent was run.

Contract impact: `none` for API, persistence, images, configuration and release
behavior; documentation clarifies the exact already-tested internal operational
pairing. Plan 2.2.0 bytes and WS-001 1.0.6 accepted scope/parent binding are unchanged;
the new execution-evidence appendix changes no planning decision or criterion.
Reciprocal report/runtime/parent/index links are maintained; docs/README.md is
generated and already lists all affected canonical documents, so no artificial
index edit is needed. Machine/human blueprints and accepted ADRs require no change:
SEC-009/012 and OPS-001/002 semantics and the installation/account division remain.

Final owner acceptance is the sole open S05 decision after successful checks.
