# MS-001-S01 — Delivery contract and comparison baseline

Stage: `MS-001-S01`. Mode: `manual_sequential`. This report records the completed
source-level work; the [canonical journal](../../../ledgers/MS-001.md) alone owns
execution state. Plan: [MS-001 1.1.0](../../../../../docs/architecture/planning/milestones/MS-001/plan.md).
Source inspection: 2026-09-08, canonical checkout at
`d2e3c65b15f02f7970eac8c32feede3cbbd01ef9`. Product baseline:
`f9f39a75994d2f7a8e8d7a75df293c35579f842d`. The product/build zones are byte-identical
between those commits (`git diff --name-only` returned no paths).

## Result and criterion coverage

| Criterion | S01 contribution / observed evidence | Remaining boundary |
|---|---|---|
| MS-001/AC-01 | Closed schema; core/migration/demo service mapping; 335 tracked build-input hashes, 16 transitive Python roots, all 9 revision/hash pairs in [source inventory](source-inventory.json); runtime resource and mount inventory | S02 file/config/record relations and final-image closure; S04 isolated extraction/runtime |
| MS-001/AC-04 | Exact canonical subject, origins, signer/ref/issuer, independent trust bootstrap, immutable tool/action pins, subject-bound scanner policy | S03 actual signatures, image subjects and supply reports; S04 malicious signature/source/child tests |
| MS-001/AC-05 | Reader/config/platform floors, separate migration command and head/read/write compatibility, unchanged strict env reader with existing positive/negative tests | S02 cross-record comparison; S04 fresh/repeat DB and final-image proof |
| MS-001/AC-06 | Selected authenticated Actions mechanism, actual anonymous 401/authenticated 302 read-only probe, finite archive/path/redirect limits and stable failure interface | S03 publication identity; S04 retrieval bytes, revoked/expired credentials, hostile archives and resource postconditions |
| MS-001/AC-09 | Frozen commands, fixture hashes, timing boundaries, 5/30 run counts, cache modes and screenshot matrix below | S04 measured samples; S05 comparisons; timing acceptance has no selected numeric threshold |

Requirements consulted: machine/human 0.11.0-draft sections 18.7–18.8 and 24.3,
SEC-009/012/016/017/018, OPS-001/002, SCALE-003/004, WEB-PERF-001..006.
The scope retains their MUST/SHOULD meanings. SEC-009 official-release obligations
and full runtime/recovery/performance gates are not satisfied by this source work.

## Changed paths and ownership

- Created `deploy/compose/delivery-manifest.schema.json` and `delivery-verification-policy.json`.
- Created `deploy/compose/validate-delivery-manifest.py`: a small dependency-free structural reader for the actual finite schema vocabulary; does not execute input or claim bundle verification.
- Created `tests/tooling/test_delivery_bundle.py` and `tests/tooling/fixtures/delivery-manifest.valid.json`: real parser/CLI fixture tests. Synthetic digests in that fixture are explicitly not an artifact or supply evidence.
- Updated `docs/architecture/runtime-network-installation.md` to doc_version 9 with the additive v1 record, trust, failure, extraction and service/resource contract.
- Updated `docs/architecture/tooling-gates.md` to doc_version 10 with the focused structural-reader check boundary; `docs/architecture/README.md` removes its stale “implementation not started” assertion and points execution-state ownership to the journal.
- Regenerated `docs/README.md`; its bytes were unchanged (no new contributor document path).
- Created this report, `source-inventory.json`, `measurement-inputs.json`, `artifact-hashes.json`, `validation.txt`,
  `validation-final.txt` and the new receipt under this stage's evidence directory. The ledger is changed only by `stage_ledger claim/accept`.

The extra reader and fixture paths are needed for the prompt's explicit actual
parser-boundary tests; documentation/index/evidence maintenance is in-stage scope.
No product paths were deleted. The pre-existing deletion of
`.codex/agents/generated/w21-figma-master-elements-index/internal-figma-agent-prompt.md`
is foreign and preserved. All pre-existing local commits are preserved. No mixed
product files existed at entry, no stage-owned source overlaps foreign edits.
No commit, push, PR, branch/worktree/clone, subagent, dependency installation,
credential mutation, image/bundle publication, daemon start or deployment occurred.

## Inventory and compatibility assessment

The [runtime contract, section 11](../../../../../docs/architecture/runtime-network-installation.md#11-internal-delivery-v1-contract-ms-001s01)
is the normative in-scope reader/closure specification. The source inventory is
source observation, not Docker layer contents or a completeness proof for dynamic
imports. AST traversal followed API/migration imports recursively into package and
plugin roots: all 16 reached roots appear in API Docker COPY rules. The additional
`packages/contracts/identity` COPY is retained. Every tracked source file under the
build zones, including migration support, demo init and public assets, has a hash.
S02 must also verify wheel/third-party/runtime imports and any generated assets
inside final images; no static scan can certify those.

Python runtime declarations are in `apps/api/pyproject.toml`: Alembic 1.16.2,
argon2-cffi 25.1.0, FastAPI 0.115.14, openpyxl 3.1.5, PyArrow 20.0.0,
psycopg[binary] 3.2.9, pydantic-settings 2.10.1, redis 6.4.0,
SQLAlchemy 2.0.41, Uvicorn[standard] 0.34.3; `uv.lock` binds the transitive closure.
The builder is uv 0.9.26/Python 3.12; final Python base 3.12.11, both digest-pinned.
Web build uses Node 24.18.0/pnpm 11.13.0 plus the exact pnpm lock and four workspace
packages: contracts, localization, chart_compiler_ts, ui-foundation. Final Web/Edge
uses digest-pinned nginx-unprivileged 1.28.0; docs build uses the locked Python docs
package, `mkdocs.yml`, public docs and generated CSP. Dockerfiles bind all exact
base digests. The Dockerfile frontend `docker/dockerfile:1.11` is currently a tag in source.
Read-only `docker buildx imagetools inspect docker/dockerfile:1.11 --format
'{{.Manifest.Digest}}'` resolved
`sha256:10c699f1b6c8bdc8f6b4ce8974855dd8542f1768c26eb240237b8f1c9c6c9976`;
policy records that immutable input. S02/S03 must apply it and bind actual builder
versions before repeat-build comparison. No layers were built or started.

Required shipped resources: built Web dist including `help-index.json`, eleven
tracked `ui-an-003-prototype/*.svg` assets, generated public docs/search/CSP,
Web and Edge Nginx configuration; migration env/ini/template and nine revisions;
demo `010_create_reader.sh`, `015_profile.sh`, `020_schema.sql`, `030_seed.sql`,
`040_grants.sql`. Source-selected CSS uses system-font fallback; no tracked WOFF
files were found in the build zones. S02 must inspect built font/icon/license
closure and include real notices, not infer distribution rights from CSS names.
No current generated dist, ignored asset, node_modules or cache is a build source.

The current bootstrap's host tools are Bash, Python 3, Docker CLI/Compose plugin,
OpenSSL, curl and POSIX dirname/mkdir/chmod/rm/awk/sed/grep/sleep utilities. Build
hosts additionally need Git, uv, Node/corepack/pnpm and Docker Buildx; optional QEMU
is a build aid only. The future standalone verification host needs trusted Python,
Cosign and HTTPS/auth retrieval; it must not require uv, Node, repository source,
a package install or a Docker daemon merely to validate structure/signatures.
Container tools include Python/Uvicorn, Alembic/SQLAlchemy/psycopg, Nginx/wget and
PostgreSQL/pg_isready/psql plus shell for demo init. S02 validates actual availability.

Route dependencies and missing configuration are explicit in runtime section 11.
Valkey host settings exist but no Compose Valkey service exists. There are no new
worker/Valkey images in the selected inventory. API mounts all eight domain router
groups; their presence is not readiness of bootstrap, demo-source connectivity or
analytics artifact persistence. Do not remove those routes to obtain a green test.

| Surface / supported interaction | Classification | Basis and transition |
|---|---|---|
| Known `.release.env` consumers: validator, bootstrap, ci-smoke, release overlay, compose_lifecycle | `compatible-change` for separate structured input plus unchanged projection | Old parser/code remain byte-unchanged; current valid/invalid subprocess tests pass. New keys in old format remain rejected. S02 derives the same three keys and checks equality. New-format input to old reader is intentionally unsupported, never silently accepted. |
| Structured delivery reader/config/policy | `compatible-change` additive v1 boundary | No prior structured reader/data existed. Structural pass is distinct from semantic/authenticity pass. Future major changes fail closed. |
| Publication/access and trust | `unknown` for end-to-end availability; selected mechanism has observed auth boundary | Existing artifacts authenticate download, but no delivery artifact/signature exists. S03 needs explicit publication authority; package visibility query returned 403. |
| PostgreSQL data/migration runtime, API/ports/domain behavior, cache/identity, browser runtime | `none` in S01 | No corresponding implementation/config files changed. Future manifest compatibility is fresh-owned DB only, downtime before app start, rollback unqualified. |
| Benchmark acceptance | `none` for existing gates; additive measurement protocol | Existing image/resource caps retained. `gate_performance` is unchanged; no threshold or input is manufactured. |

Search coverage is direct in-repository env readers, Compose, Dockerfiles, declared
source dependencies and runtime tooling. No claim about undiscovered external env
consumers is made. Static inventory does not establish image import/start, library
licenses, runtime asset availability or retained data behavior.

## Provider, signer and native targets — observed 2026-09-08

Read-only commands and bounded observations:

- `gh api repos/Dejetins/custometry --jq '{full_name,visibility,default_branch}'`: public, `main`.
- `gh api repos/Dejetins/custometry/actions/permissions/artifact-and-log-retention`: 90 days, maximum 90.
- `gh api repos/Dejetins/custometry/actions/runs/34054822070/artifacts`: IDs `9995733182` and `9995725485`, non-expired `.dockerbuild` records, expiry `2026-12-05T19:24:55Z`; these are not bundles.
- Read-only no-redirect GET of `/repos/Dejetins/custometry/actions/artifacts/9995733182/zip`: anonymous 401; existing authenticated credential 302 to `productionresultssa10.blob.core.windows.net`. Credential and signed URL never printed/persisted; archive bytes were not downloaded. This proves current endpoint authentication, not future bundle retrieval.
- `gh api users/Dejetins/packages/container/custometry-api`: HTTP 403, missing `read:packages`; visibility/content of GHCR packages remains unverified. No credential change requested or made.
- `gh api repos/Dejetins/custometry/actions/runners`: zero registered self-hosted runners.
- `uname -sm`, `sysctl -n machdep.cpu.brand_string`: Darwin arm64, Apple M5 Max. `docker context show`: `desktop-linux`; client 29.6.2, Compose 5.3.1, Buildx v0.35.0-desktop.2; Docker socket unavailable, no server version/runtime proof.

Selected smallest provider is Actions artifact, exact workflow/ref and origins in
policy. No new registry/account/repository is required. Authentication is not a
recipient allowlist: a user with public-repository read access may download after
sign-in. Images may be public. Ninety-day retention and a verified private handoff
copy are technical availability policy, not account expiry or an authorization to
create a new remote store. S03 records actual ID/digest/expiry after upload.

The existing native AMD64 source job uses `ubuntu-24.04`; its historical successful
run is [34054822070](https://github.com/Dejetins/custometry/actions/runs/34054822070).
GitHub documents `ubuntu-24.04-arm` as native ARM64 for this public-repository class.
Select these two Linux hosted labels for future C02 image proof after authorized
workflow publication, record actual `uname -m`/engine/resources in each run, and
fail if emulated/wrong platform. They are documented targets, **not jobs observed
in this stage**. M5 ARM64 runtime is an alternative once a single selected engine
is actually available. No Linux VM identity was supplied or invented; C03 owns its
M5/ARM64 VM installation target. The hosted disk allowance can be lower than 25 GiB;
that ceiling is not guaranteed free capacity. Preflight must fit the actual target.

Policy pins were read from official GitHub release asset metadata (Cosign v3.1.3,
Trivy v0.74.0, Syft v1.51.1) and existing source action commit pins. The asset SHA-256
values are metadata observations, not local binary execution evidence. Initial
trust comes from reviewed source/receipt and pinned official Cosign bytes, followed
by its independent Sigstore trust bootstrap. S03 must retain exact trusted-root,
scanner database identities and expiry and observe actual claims on the selected
workflow. No signing private key is provisioned; future keyless signer uses GitHub
OIDC with the exact identity/issuer policy. Critical/license findings cannot be
waived by this report.

Primary references consulted for current semantics:

- [GitHub artifact downloads](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/download-workflow-artifacts): authenticated repository readers and retention.
- [GitHub REST artifact API](https://docs.github.com/en/rest/actions/artifacts): artifact ID/run metadata, one-minute redirect, Actions read and unavailable response.
- [upload-artifact](https://github.com/actions/upload-artifact): immutable artifact ID/digest and overwrite/retention semantics; existing v4 commit retained.
- [GitHub hosted runner reference](https://docs.github.com/en/actions/reference/runners/github-hosted-runners): native `ubuntu-24.04` and `ubuntu-24.04-arm`.
- [Sigstore signature verification](https://docs.sigstore.dev/cosign/verifying/verify/) and [installation](https://docs.sigstore.dev/cosign/system_config/installation/): exact identity/issuer and independent binary trust.
- [Trivy vulnerability scanner](https://trivy.dev/docs/latest/scanner/vulnerability/): scanner/database evidence scope.
- [Cosign v3.1.3](https://github.com/sigstore/cosign/releases/tag/v3.1.3), [Trivy v0.74.0](https://github.com/aquasecurity/trivy/releases/tag/v0.74.0), [Syft v1.51.1](https://github.com/anchore/syft/releases/tag/v1.51.1): pinned asset metadata.

## Frozen measurement protocol v1

[measurement-inputs.json](measurement-inputs.json) binds 17 existing baseline/fixture
sources with exact hashes. Fixture: fresh owned empty DB before migration, no account,
no session, standard core and separately optional demo init; route workspace string
`northwind-retail`, not a claim that such a workspace is provisioned. All source
hashes are the same between the selected baseline and current inspection. Candidate
commit/config/fixture hashes are recorded before any later measurement. The reader's
positive synthetic manifest is for validation only, never a timing substitute for
a real signed bundle or image.

The later baseline source capture uses the exact selected commit in the following
command block. Capture to a new owned scratch directory, not another working
tree or clone; no such capture/build was performed by S01. S02 must preserve a
clean snapshot including its own packaging changes under an explicit source-input
identity; uncommitted bytes cannot be represented as an existing Git commit.

```sh
# Proposed later source capture/build recipe; not executed by S01.
git archive --format=tar f9f39a75994d2f7a8e8d7a75df293c35579f842d > "$MEASUREMENT_ROOT/baseline-source.tar"
# Extract this trusted Git archive to a new owned baseline directory, then:
COMPOSE_PROJECT_NAME=ms001-baseline docker compose -f compose.yaml build api web
# Same-commit prepackaging Web reference, within the preserved candidate snapshot:
source scripts/activate-toolchain.sh
pnpm --filter @custometry/web build
# Both baseline and candidate use explicit isolated runtime env/secret directories.
# Start only healthy DB, then time this separate migration process:
docker compose --profile migration run --rm --no-deps migrate
# After migration succeeds, time this startup and the probes defined below:
docker compose up --no-build -d api web edge
```

The previous snippet's Compose invocations require the S02/S04 harness to supply
`-f`, `--env-file`, project, selected platform and digest-pinned candidate config
arguments explicitly. They are command building blocks, not a current unattended
installer. Baseline images are source-built once outside timers; candidate images
are pulled before readiness timers. No source fallback occurs during candidate proof.
For baseline source build set application version `0.1.0-dev.0+sha.f9f39a75994d`
in its isolated env. Same-commit Web reference uses the candidate application version.

S02 freezes actual `delivery_bundle` producer/consumer CLI argv in its report.
S04 implements the dedicated timing/archive/browser harness using these boundaries;
that module does not exist yet and this report does not claim its commands ran.
Current source verification commands are recorded in the validation section below.

| Metric | Exact monotonic boundary / command surface | Modes / samples / aggregation |
|---|---|---|
| Retrieval | Start immediately before credentialed artifact metadata/download request; end after selected ZIP bytes are fully written and flushed. Record auth/metadata, redirect/network/body and disk-write spans separately, bytes and bytes/second. Registry pulls are a separate span per child. | 5 cold + 5 cached per target; cold uses a new owned artifact destination/cache without unrelated engine cleanup; warm repeats the exact artifact from owned cache after identity revalidation. Separate local cache and network measurements. Initial successful S03/S04 implementation is baseline. |
| Verification | Start before trusted verifier opens exact downloaded manifest/signature/payload; end on its terminal verification result, excluding extraction. Capture wall time and process-tree peak RSS separately. | Same bytes and toolchain, 5 per mode; new process each run; cold is empty owned verifier cache, warm prewarmed same cache. OS page cache is recorded as uncontrolled unless an authorized dedicated target controls it. |
| Extraction | Start before creation of private quarantine; end after all writes/checks/fsync and atomic promotion. Signature verification excluded and already passed. | 5 per mode using distinct empty owned destinations; never overwrite a prior result. Report peak RSS and bytes. First implementation is baseline. |
| Migration | Start immediately before spawning `compose ... run --rm --no-deps migrate`; end on child exit. DB is already healthy. Separately record Alembic operation span if available. | 5 fresh-owned DB runs per baseline/candidate target; repeat migration at declared head is a separate 5-run series. No existing DB reset. |
| Container readiness | Start immediately before spawning `compose ... up --no-build -d api web edge`; end at first successful post-migration API `/health/ready` plus Web/Edge `/health/live` probe set. Poll each 100 ms with 2 s timeout, record polling resolution and fail at 120 s. Pull/build/migration excluded. | 5 comparable baseline/candidate runs per target/profile/cache mode; new owned DB each fresh series. Record failed runs, container restarts and full distribution. |
| Image/disk/RAM | `docker image inspect --format '{{.Size}}' <child-ref>` per native platform; compressed OCI layer bytes separately. Sample total owned container memory and owned disk at 1 s intervals from DB startup through five minutes after readiness, including migration and optional demo. Measure quarantines, images, volumes, logs and harness data without double counting shared layers; engine allocation separately. | API <=367001600 B, Web <=104857600 B, aggregate <=6442450944 B RAM and <=26843545600 B owned data. Measured peaks and sampling resolution; no inference from mem_limit. Record available disk before each run and abort safely before exhaustion. |
| Web navigation/request | `performance.now()` immediately before `page.goto`/click to requestStart, responseStart and responseEnd via Performance API; total navigation split into dispatch/network/response intervals. | Same candidate commit/config/API fixture/browser/host; 30 observations per journey/cache condition. |
| Response-to-paint | Relevant responseEnd to expected route/state visible after `document.fonts.ready`, required image decode and two requestAnimationFrame ticks with unchanged target bounding boxes; report this stable-paint proxy explicitly. | At least 30 per journey/mode; record any animations or rendering variance rather than suppressing failures. |
| Interaction feedback | Trusted browser event dispatch to expected visible state and next two stable frames; separately event-to-request dispatch where a request exists. Language/menu/Back interactions with no request report dispatch as N/A. | 30 observations per interaction/mode; empirical nearest-rank p50/p75/p95, all samples, failure counts and uncertainty. |

All non-Web timings retain all five raw observations plus median/min/max and failure
count; no selected passing retries. For Web, retain all >=30 samples and empirical
p50/p75/p95; no production percentile claim. Report absolute and percent baseline
change only for identical boundary/semantics/hardware/cache/fixture; zero or absent
baseline produces N/A percentage. Record host OS/CPU/RAM/engine/browser build,
parallel activity, network path, image/manifest/fixture/tool hashes and clock method.
Tests run serially with retries zero; partial/failing runs remain evidence.
Cold browser = new context with empty storage/cache; warm = same context after one
untimed traversal, preserving the declared locale only. Server/OS caches are not
silently called cold because browser cache is empty.

Image/resource caps and zero unexplained contract/fidelity failures are gates.
Timing acceptance is **not assessed — threshold not specified**. `gate_performance`
requires a positive baseline and selected regression threshold, so no input or pass
is manufactured. Missing mandatory later observations block measurement completeness;
they are not zero values. This is benchmark design, not a measured performance claim.

### Frozen screenshot and interaction matrix

For each row use same-commit prepackaging Web versus packaged image, both locales
EN/RU, 768x1024 and 1920x1080, scale 1, identical Playwright 1.52.0 Chromium build,
UTC and same API fixture. Save paired screenshots only after the visible state,
fonts/assets and two stable frames; save DOM target/assertion and network/console
observations alongside. Use PNG names containing source role, route, locale,
viewport and state. Never persist cookies, tokens or browser storage.

| Route / state | Required interaction / comparison |
|---|---|
| `/` / ready shell | API readiness, language round trip; wide navigation expanded/collapsed, narrow navigation overflow open/closed with focus return |
| `/help` / generated links | Link count/content and local documentation target; Back/Forward preserves origin |
| `/docs/` / loaded, search results | Public docs, CSP, local search for `Foundation`, first result and return; no authenticated docs exposure |
| `/w/northwind-retail/analytics/sales` / unauthenticated unavailable | Real route and honest unavailable state; expected `/api/identity/me` and `/api/analytics/results` 401s recorded separately, no fake results |
| `/not-a-registered-surface` / 404 | Visible not-found and return to allowed Overview; no blank route |

Zero missing required assets, unexpected request/page/console errors or unexplained
visual/interaction changes. Compare actual source assertions and images, not pixel
identity alone. `tests/e2e/foundation.spec.ts` is the behavior reference; the older
`browser-smoke.json` still says “Planned surface”, which is stale for Sales. Its
static metadata is not an acceptance oracle. The default existing Playwright config
also lacks the specified viewports and has CI retry=1; S04 must use a dedicated
artifact config with the frozen viewports/retries=0. Existing fixture servers that
serve host Vite or inject app services do not prove final container assets. The target
pilot remains secondary for demonstrated composition; no new UI redesign is authorized.

## Checks, source synchronization and next-stage handoff

Initial/entry evidence is preserved in [validation.txt](validation.txt); the final
post-refinement command output is in [validation-final.txt](validation-final.txt).
All final commands exited 0: **61 tests passed**, Ruff passed, Pyright returned
zero diagnostics, both structural CLI inputs passed, `check --scope local` passed,
and `git diff --check` passed. [artifact-hashes.json](artifact-hashes.json) binds
the exact product/source bytes used for those checks. Focused
schema/policy/CLI and legacy env tests, Ruff, Pyright, direct JSON validation,
Markdown/index/blueprint/layout/prompt bindings and the grouped local source profile
are required. Initial focused run: 62 tests passed and Ruff passed; Pyright found
25 introduced narrowing errors in the new reader. Explicit type narrowing fixed
them, and the focused type check then returned zero diagnostics. The final run
below supersedes that intermediate count after fixture-policy refinements.
No tests were skipped to get a pass. No runtime, image, scanner, signature, browser,
`ci` or `release` result is claimed. Docker absence is a documented downstream
runtime prerequisite, not a failure of S01's source-level contract.

Synchronization review: parent WS-001 version 1.0.3 and direction links remain
unchanged and reciprocal; accepted plan 1.1.0/hash and all five prompt contracts
remain untouched. Runtime v9 is a compatible addition to the plan's v8 source; tooling v10 adds
the reader check to the existing source-gate contract without changing profiles;
architecture navigation directs mutable progress to the journal. Product blueprints,
UI contracts, ADRs and provider/consumer milestone allocations are unchanged.
No new status board, ticket, role assignment or owner checkpoint was added.

The exact S02 prompt was read completely. Its four entry inputs (accepted plan,
this report, schema, policy) are present. It requires S01 acceptance first. S01 may
be accepted without new user acceptance; no next-stage execution is performed by
this task. The receipt enables S02 only if its live entry checks pass; a new stage
request still supplies execution authority.

Concrete inputs/obligations:

- **S02:** consume schema/policy/source/measurement inventory; implement the producer, derived env and cross-record/file/archive checks; close actual image import/migration/asset/notices dependencies; package the demo mount; preserve a clean identified source snapshot and before-Web build; freeze real downstream CLI commands. The structural reader's pass is deliberately insufficient for authenticity/execution. Docker is currently unavailable, so collect image proof only on an actually available authorized target and preserve an unmet criterion otherwise.
- **S03:** prepare exact changes to the existing workflow, tools, source frontend/base pins and Sigstore trust snapshot; then obtain any newly required publication authority for `Dejetins/custometry` workflow/main, existing GHCR API/Web images and its Actions bundle. No such authority is granted by S01. Observe two actual runs at the same immutable source, all final child subjects, real SBOM/license/Trivy/signature results, immutable artifact ID/digest/expiry and retained handoff copy. Package visibility remains unknown; public images are permitted but retrieval must be tested.
- **S04:** consume those exact final artifacts on actual native AMD64/ARM64 targets; run authenticated/denied/revoked/expired/missing/tampered/wrong-subject/hostile-archive cases; test no writes outside quarantine and no success after failure; fresh/repeat migrations and all frozen measurement/screenshot cases. Do not substitute QEMU, host-source UI or a future C03 installation claim.

Remaining risks are precisely downstream evidence: real image size/import/assets,
license findings, scanner DB freshness, actual signer claims, hosted publication and
native runtime. No material owner decision is needed to complete S01. Current-stage
acceptance does not accept the whole milestone, qualify installation or publish a
public release.
