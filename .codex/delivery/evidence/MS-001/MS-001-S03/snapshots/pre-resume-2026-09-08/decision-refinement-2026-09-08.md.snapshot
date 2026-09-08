# MS-001-S03 — Addendum to the paused decision packet

Date: 2026-09-08. Executor: `01a07e02-12a3-7953-8c82-122b33d8d8df`.
Requirements: MS-001/AC-02, AC-04, AC-06, AC-09; SEC-016, SEC-017, SEC-018.

This additive review record corrects the interpretation of repair authority and
artifact naming in the [frozen report](report.md) and
[pause receipt](receipts/2026-09-08-s03-pause-01.md). Neither is rewritten.
The [canonical journal](../../../ledgers/MS-001.md) remains `awaiting_input`,
S03 remains `needs_input`, and S04 remains disallowed. No resume or acceptance
transition occurs. The coordinator explicitly requested preserving that pause while
finishing this bounded clarification and the already authorized Git publication.

## Authority correction

The S03 prompt delegates technical decisions within its accepted scope. The original
task also authorizes necessary in-scope repairs. The earlier packet was too broad in
asking the owner to authorize a generic remediation route. A prohibition on broad
dependency upgrades or policy relaxation does not prohibit every targeted correction.
The work below does not need another routine permission request. It remains engineering
work to execute after the existing pause is reconciled through the supported runner;
this addendum does not claim that all nonpublication implementation is finished.

| Already delegated work | Concrete touched boundary and required proof |
|---|---|
| Refresh vulnerable runtime bases within existing roles and supported major lines | API Python 3.12 patch/base digest; Web Nginx 1.28 and Alpine security base; upstream PostgreSQL 17 patch/base. Update exact Dockerfile/Compose pins and corresponding inventories. Rebuild both native platforms, rerun subject-bound scans, functional comparisons and affected runtime checks. An Alpine minor change needs actual package/config compatibility evidence; availability alone is insufficient. |
| Synchronize a selected PostgreSQL 17 patch | The current schema has `postgres_version: const 17.5`; Compose, `delivery_bundle.POSTGRES_DIGEST`, supply metadata and fixtures repeat the selection. A patch requires coordinated reader/schema/manifest updates and fresh-owned database/migration proof. A changed pin or schema constant alone is not evidence that a new owner gate is required. The accepted installed-upgrade/rollback boundary remains unqualified. |
| Correct scanner/license mapping using actual shipped source evidence | Parse CycloneDX license expressions, recover installed classifiers/license files, identify non-package OS descriptors, resolve hash/descriptive license fields against real upstream text. Preserve original reports and audit every actual shipped package. Do not convert a real unlisted or review-required license into an allowed license. |
| Complete shipped Web/help/documentation inventory and vulnerability coverage | Map shipped generated/minified code to exact locked components and real notice sources; repair the current coverage gap and missing actual notices without inventing upstream license text. Existing SBOM success is insufficient for this boundary. |
| Correct vulnerability applicability using verifiable package/source/platform evidence | Preserve raw Trivy records and retain unresolved conflicts. A proved non-applicable binary/source finding is not a policy waiver; a blanket ignore rule or unsupported suppression is. |
| Align disabled producer naming with S01 | Update assembly, reconciliation, workflow descriptor and focused tests to the accepted full name. Preserve version-level immutability across attempts. This is a bounded implementation correction, not a request to redesign the frozen contract. |

The runner's `SKILL.md` workflow step 5 says: "for `awaiting_input`, consider only
the exact row whose resume condition is evidenced; otherwise remain awaiting input".
Step 9 requires atomic activation/resume before stage side effects; the canonical
lifecycle permits `needs_input -> in_progress` only with the exact resume evidence.
The coordinator explicitly requires keeping `needs_input` and not resuming here.
Therefore the already delegated naming repair is the first implementation step at
resume, not an owner choice or permission to adopt the incorrect shorter name.

No dependency/base implementation, gate policy, manifest schema or producer code is
changed by this post-pause addendum. Its only normative documentation edit clarifies
the already accepted name and the current implementation gap.

## Bounded security triage

The original [actual ARM64 scan summary](scans/summary.json) remains authoritative
for the observed subjects: API 9, Web 2 and PostgreSQL 6 raw critical records. Those
are scanner records, not 17 independently confirmed exploitable vulnerabilities.
All corresponding gates still fail. No fresh final-source or AMD64 scan is claimed.

| Observed finding | Specific repair or unresolved evidence |
|---|---|
| API GnuTLS `3.7.9-2+deb12u5`, OpenSSL `3.0.17-1~deb12u2` | Scanner fixes are `3.7.9-2+deb12u7` and `3.0.19-1~deb12u2`; first evaluate a same-distribution base refresh rather than a general application dependency upgrade. |
| Web/PostgreSQL OpenSSL `3.3.5-r0` / `3.3.4-r0` | Scanner reports fixed `3.3.7-r0`; a targeted upstream base refresh is a concrete candidate. |
| PostgreSQL four Go stdlib findings | These bind `/usr/local/bin/gosu`, built with Go `v1.18.2`, rather than the PostgreSQL engine. Inspect the selected official image's replacement helper/version and rescan. Do not introduce a new custom PostgreSQL package repository implicitly. |
| API SQLite CVE-2025-7458 | Debian lists bookworm vulnerable with no fixed package; trixie has a fix. This remains unresolved. A distribution migration has broader compatibility costs than a patch and is not selected by this evidence. |
| API zlib CVE-2023-45853 | Debian explains that bookworm does not build the affected contrib/minizip binary package. This supports investigating package applicability; it does not authorize ignoring every zlib record. |
| API Perl CVE-2026-42496 / CVE-2026-8376 | The first concerns Archive::Tar; the second explicitly concerns 32-bit Perl. Exact installed-module and native-platform facts must determine applicability rather than the umbrella Debian source name alone. |
| API Perl CVE-2026-13221 | Debian's vulnerable-version table and its note that introduction occurred in v5.37.10 conflict for the installed 5.36 line. Exact source/backport resolution remains engineering work; do not suppress on the note alone. |

Primary triage sources: Debian trackers for
[SQLite](https://security-tracker.debian.org/tracker/CVE-2025-7458),
[zlib/minizip](https://security-tracker.debian.org/tracker/CVE-2023-45853),
[Archive::Tar](https://security-tracker.debian.org/tracker/CVE-2026-42496),
[32-bit Perl](https://security-tracker.debian.org/tracker/CVE-2026-8376), and
[Perl introduction conflict](https://security-tracker.debian.org/tracker/CVE-2026-13221).
These source statements support triage; this addendum grants no exception.

[Read-only candidate observations](repair-candidate-observations.json) verify exact
OCI index hashes and availability of AMD64/ARM64 descriptors for Python
`3.12.14-slim-bookworm`, Nginx `1.28.2-alpine3.23` and PostgreSQL
`17.11-alpine3.23`. The file contains their full digest references. These are
available candidates, not selected, built, scanned or accepted repairs.

## License decisions are narrower than the raw finding count

The 563 / 61 / 41 license findings include parser and metadata problems as well as
real policy questions. They are not counts of adjudicated legal violations.
[Installed API distribution metadata](installed-license-metadata.json) shows MIT
classifiers and real license-file hashes for FastAPI and annotated-types, despite
the scanner/gate reporting unknown licenses. Project metadata omits its own license;
the root project license can be bound explicitly. An OS descriptor such as `debian`
or `alpine` is not itself a licensable package; every installed package still needs
coverage. Hash-only and split descriptive license fields require real source mapping.

Greenlet actually declares `MIT AND PSF-2.0` and ships both license texts. Fixing
expression parsing is delegated, but PSF-2.0 remains outside the current allowlist.
The shipped runtime also contains components with GPL/LGPL obligations, including
glibc in API and BusyBox in Alpine roles. The existing policy's allowed list is
Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, MIT and PostgreSQL; review-required and
unlisted licenses cannot be silently admitted. After source normalization, a proposal
to retain such components under an expanded policy needs an explicit policy decision,
with exact components, license texts and distribution obligations. A compatible
replacement that satisfies the current policy remains an engineering option.

The missing root LICENSE in upstream `html-parse-stringify` does not alone prove a
legal violation. Preserve real MIT metadata/README and determine the actual shipped
notice obligation. Never fabricate a license file. An unresolved required notice or
a proposal to waive it must remain visible; fixing actual notice collection is delegated.

## Naming conflict and its correction

S01's report explicitly selects runtime contract section 11 as the normative reader
and closure specification. That section, already present before S03 (Git `0333423e`),
requires `custometry-delivery-<delivery-version>-<run-id>-<attempt>`.
The JSON schema only matches `^custometry-delivery-[A-Za-z0-9.+_-]+$`; its structural
reader does not enforce equality to delivery version/run/attempt. The fixture's short
name therefore demonstrates schema permissiveness, not an accepted naming override.

The paused producer currently uses `custometry-delivery-<delivery_version>` in
assembly and `custometry-delivery-0.1.0-ms001.<run_id>` in reconciliation. A focused
test asserts that implementation; it does not override S01. Section 13 and the frozen
report incorrectly attributed the shorter format to S01. Runtime contract version 13
now states the accepted full name and labels the implementation divergence explicitly.
The frozen report/receipt remain historical evidence, with this correction adjacent.

Before activation, use `delivery_version = 0.1.0-ms001.<run_id>` and artifact name
`custometry-delivery-0.1.0-ms001.<run_id>-<run_id>-<run_attempt>`.
The bounded repair follows the existing full name; no alternative name is proposed.
Reconciliation must also check prior attempts for that same delivery version and
reject different content; adding an attempt suffix must not permit immutable-version
replacement. No existing artifact uses either proposed supply name in this task.

## Exact remaining external authority and material exceptions

The existing Git commit/push/PR/required-CI/protected-main/synchronization/branch-cleanup
authority is already granted. The concrete new supply effect to authorize is:

- Run the two currently disabled jobs in `Dejetins/custometry`, workflow
  `.github/workflows/publish-candidates.yml`, `refs/heads/main`, after the engineering
  blockers above pass. Consume existing `ghcr.io/dejetins/custometry-api` and
  `ghcr.io/dejetins/custometry-web` candidate outputs and upstream PostgreSQL.
- Create `custometry-supply-proof-<run_id>-<run_attempt>-amd64` and
  `custometry-supply-proof-<run_id>-<run_attempt>-arm64`, plus the S01 full-name
  signed bundle artifact described above, with 90-day Actions retention.
- Use GitHub OIDC `id-token: write`, Cosign keyless signing and its transparency
  record for the exact canonical manifest.
- Retrieve and verify the same bundle into the proposed private handoff directory
  `/Users/daniildegtyarev/.local/share/custometry/delivery/MS-001/<delivery_version>/`,
  directory 0700/files 0600, retained through C03–C06. The directory is not created.

Separate material decisions would include admitting actual unlisted/review-required
licenses, waiving required security/notice evidence, changing a supported database
major or installed-data upgrade contract, or adding a new image publisher/repository.
None is requested or silently selected merely because a technical pin needs updating.

## Publication and validation boundary

[Publication evidence](publication-57.json) records PR #57, required Foundation CI
success and protected-main merge `6ca4d6d77acfc01ea6efde96246036796fc531b7`.
Both ordinary post-merge workflows succeeded; the two new supply jobs were observed
`skipped`. The technical branch was deleted locally and absent remotely. Local
unpublished ancestry and the foreign retired-prompt deletion remain preserved.

This supplement and the runtime documentation correction are published separately
under the existing authority. Relevant checks are documentation links/index, prompt
pack validation and diff whitespace; outcomes are retained in
[addendum checks](checks/addendum-2026-09-08.json). Prior 119 focused tests and
371 total tests (15 skipped), four ARM64 builds and failed supply scans keep their
original proof boundaries. No product code changes here invalidate those source tests.
The artifact hashes in publication evidence prove that the journal, report, original
hash manifest and pause receipt remain unchanged during this clarification.
The original 45-file `artifact-hashes.json` is a historical snapshot at stable
pre-addendum commit `6ca4d6d77acfc01ea6efde96246036796fc531b7`; verify those hashes
against that commit's file bytes, not later edited working files. Runtime contract
version 13 intentionally differs from its historical version 12 hash. The new
[addendum file hashes](addendum-artifact-hashes.json) bind this corrected slice;
its containing Git commit and publication PR identify the separate snapshot.

Contract impact: `none` for runtime behavior in this supplement; documentation is
corrected to the existing accepted retrieval contract. Disabled producer compliance
remains incomplete and prevents activation/acceptance. No S04 readiness, completed
S03, signed bundle, full release or installed-user acceptance is asserted.
