# MS-002-S05 — Installation closure and C04 handoff

[Plan 1.0.0](../../../../../docs/architecture/planning/milestones/MS-002/plan.md),
[parent WS-001](../../../../../docs/architecture/planning/directions/DIR-006/workstreams/WS-001.md),
[journal](../../../ledgers/MS-002.md), and
[current runbook](../../../../../docs/architecture/runtime-network-installation.md#c03-closure-and-c04-handoff--ms-002-s05).
The journal alone owns mutable execution and final acceptance. This report records
the reviewable result; no final owner decision is inferred from the execution request.

## Candidate and evidence lineage

Final delivery is `0.1.0-internal.20260910.ms002.s04.2`; application images are
`0.1.0-internal.20260910.ms002.s04.1`. Manifest SHA-256 is
`57d182c056b949e470e67100fd422d9a16e993842ca5c8feba81ad82365facce`.
The [S04 trusted inventory](../MS-002-S04/candidate-trusted-files-02.json) binds
its independent toolkit, ZIP and six image archives. S05 rechecked all 19 retained
supply files with zero mismatches. No rebuild or candidate-byte modification occurred.

[S01](../MS-002-S01/report.md) used the older MS-001 bundle for incremental
installer/migration proof; [S02](../MS-002-S02/report.md) used a newly built API
for real TLS/readiness; [S03](../MS-002-S03/report.md) used host Vite and real
API/PostgreSQL for UI development proof. These are producer evidence, not assertions
that every test ran against the final package. [S04](../MS-002-S04/report.md)
built the source snapshot containing those increments and repeated the packaged
journey. Its first candidate failed CSP; the exact toolkit-only nonce repair
produced delivery .s04.2 without changing image version .s04.1. Per-platform
upstream notices remain intact. See [source snapshot](../MS-002-S04/source-snapshot-01.json),
[builds](../MS-002-S04/builds-01.json), and [images](../MS-002-S04/images-01.json).

All four predecessor receipts and their 142 directly bound references match
current bytes: [integrity check](predecessor-integrity-01.json). S04's
[actual acceptance with limitations](../MS-002-S04/owner-acceptance-06.json)
supersedes its earlier pause narrative. It does not establish S05 owner acceptance.

## Eight-criterion map

| Criterion | Observed proof | Declared limit / disposition |
|---|---|---|
| MS-002/AC-01 | S01 standalone Python 3.12 consumer and hostile-input tests; S04 new native package, exact hashes and no consumer source build; S05 retained supply integrity | S01 is an earlier candidate. Final package acceptance is internal, without official release assurance. |
| MS-002/AC-02 | S01 lock/ownership/foreign-resource and identity/secret preservation; [S04 Mac runtime](../MS-002-S04/mac-local-runtime-01.json) repeat/stop/corrupt-archive recovery; S05 same LAN ID and config restored to ready | Linux ownership/recovery campaign incomplete; accepted S04 limitation. S05 loopback restart encountered exhausted engine network pools. |
| MS-002/AC-03 | S02 actual adjacency/TLS negatives; S04 trusted loopback and [same-host LAN](../MS-002-S04/mac-lan-runtime-01.json), wrong Host/Origin/method rejection, valid rotation and no HTTP fallback; S05 trusted LAN entry | Second MacBook showed Brave page with insecure indicator; trusted Safari and Linux LAN unverified. No production SEC-018 egress proof. |
| MS-002/AC-04 | S01 actual failed one-shot migration and recovery; S02 DB/schema/storage negatives; S04 packaged browser real DB, unsupported schema, read-only storage and API-loss journeys; S05 actual ready status | Linux read-only-storage drill timed out; cause remains undetermined and final guest readiness was not rechecked. Failed/unexecuted checks are not passes. |
| MS-002/AC-05 | S03 normalized pilot comparison, RU/EN, long text, keyboard, four ADR anchors and layout zoom; S04 four trusted packaged Chromium journeys; S05 EN/RU, retry, 1440x900 screenshot and zero console messages | Owner behavior and visual decisions remain separate and required. No Safari, screen-reader speech, browser chrome zoom or full WCAG claim. |
| MS-002/AC-06 | S01 failed migration/stop/resume; S02 rejected TLS preserves active revision; S04 corrupt archive rejection, exact restoration, retained ID/port/secret/schema/artifact and unchanged foreign containers | No cross-version upgrade/downgrade, account/session persistence or coherent backup/restore qualification. S05 leaves loopback stopped and LAN running; no volume deletion. |
| MS-002/AC-07 | S04 native Mac ARM64 complete bounded proof; exact package reached Ubuntu 24.04.4 ARM64 loopback ready; [resource accounting](../MS-002-S04/resources-integrity-01.json) retained | Linux later rotation/persistence/resource/LAN/browser checks unexecuted. S04 owner accepted these limits. Same-host LAN is not second-computer proof; no universal Linux/AMD64 claim. |
| MS-002/AC-08 | This single map, current runbook and C04 contract below; concrete running entry and representative visual source linked | Final milestone closure requires actual owner behavior/visual acceptance, including disclosed limits, and a final ready receipt in the journal. |

WS-001/AC-01 receives bounded internal supply proof; AC-02 receives Mac plus
partial Linux observations; AC-05 receives scoped preservation/recovery evidence.
These contributions do not complete the whole workstream or C04/C05/C06.

## Current review target and runtime recovery

The review entry is [the installed LAN page](https://192.168.0.120:8443/),
installation `custometry-994f905f29496190b375245d`, on the original Mac engine
29.6.2 / Compose 5.3.1. S05 restored this existing instance with the exact retained
toolkit. [Current runtime record](runtime-review-01.json) binds config and state.
The [current screenshot](entry-1440-ru.png) and
[matched pilot screenshot](../MS-002-S03/screenshots/web-1440-pilot-ru.png) are
1440x900. [S03 comparison](../MS-002-S03/visual-comparison.md) explains the derived
installer layout: shared graphite surfaces, typography, borders and controls;
no analytical rail or fabricated workspace before account setup. The current
capture is readable with no clipped status/actions; this is executor observation,
not owner visual approval.

At entry Docker Desktop was stopped and the selected Ubuntu VM was running.
The VM was suspended with saved state before starting Mac Docker; guest data and
execution state were retained. Initial loopback resume failed after DB migration:
Docker could not allocate missing ingress networks because all predefined address
pools were fully subnetted. A direct, ownership-checked Compose reproduction
confirmed this error. One diagnostic attempt used the wrong helper name `lock`
and failed before any action; the actual helper is `locked`. No product fix or
network pruning occurred. Loopback was stopped normally with volumes retained.
The existing LAN installation already had all four networks and resumed to ready.
This restores review availability but does not repair engine pool exhaustion;
fresh or network-recreating installs need separately scoped resource reconciliation.

Chromium opened the actual HTTPS entry without bypassing certificate errors,
showed ready EN/RU state and correct version/origin, and repeated the status check
successfully. Status requests returned HTTP 200; console had zero errors/warnings.
The earlier refused loopback navigation is a failed availability check, not a
browser pass. Full fault/viewport campaigns were reused from unchanged S04 proof.
Mac LAN remains running for owner review; Ubuntu remains suspended. Do not run
both target engines concurrently when continuing the sequential target workflow.

Resource limits remain 6 GiB and 25 GiB, not expanded by the 36 GB host or 40 GiB
sparse VM disk. S04 conservatively accounted 4,738,071,800 bytes excluding Docker
volume data; recorded Mac running-service memory caps total 1,811,939,328 bytes.
Samples are not peak measurements and disk admission is not a filesystem quota.

## Exact C04 prerequisites

- Candidate and toolkit: use the delivery/image identities above and the exact
  independent trusted inventory. Old readers cannot read the new per-platform
  notice metadata. Protected source and image supply remain owner-local.
- Root: select the existing installation by the full ID above and confirm its
  `installation.json` (`custometry-installation/v1`), saved canonical root,
  engine/context, origin, ownership labels and `config/compose.json` hash.
  Private host paths are retained in local state, not copied into public evidence.
- Persistence: retain private file secrets, declared volumes and canonical
  `/var/lib/custometry/artifacts` bind; schema head remains exactly
  `0009_notifications`. No Identity schema change or bootstrap token was supplied.
- Status: `GET /api/installation/status` projects
  `custometry-installation-status/v1`, `ready_for_bootstrap` / `not_ready`,
  three `ready` / `not_ready` components and `bootstrap_not_available` with no-store;
  failures return HTTP 503 and stable database/schema/storage codes. Readiness is
  operational and reads no Identity private state.
- Ingress: installed GET-only root/assets/docs/health/version/status allowlist
  currently denies bootstrap and all other product routes. C04 must explicitly
  replace this restriction through its accepted auth/CSRF/Origin contract before
  exposing mutation or authenticated navigation; do not broadly open the proxy.
- UI: reuse `packages/ui-foundation/src/installation.tsx` (`pilot-entry/v1`),
  existing localization and generated Foundation client. Account/workspace creation,
  bootstrap context, initial disclosed roles/organization membership, sessions,
  recovery and authenticated pilot shell remain Identity/C04 work.
- Account lifetime: accounts are not arbitrarily time-limited; expiry/revocation
  of sessions, refresh families, invites and API tokens are separate concerns.
  Reconcile retained AUTH wording and persisted reader/writer behavior in C04;
  no auth-policy amendment or implementation occurs in S05.

C04 is a separately selected future milestone, not a successor prompt in this pack.
No source connection, fake account, bootstrap, release or publication is created.

## Documentation, validation and ownership

Contract impact is `none` for application/API/schema/config/dependencies; this unit
consolidates evidence, restores the unchanged review target and adds documentation
navigation. Runtime contract and parent/index links point to this report and the
single journal. Parent navigation patch inherits delegated editorial authority;
accepted MS-002 plan/prompt hashes and previous exact version bindings are preserved.
Public help already distinguishes development commands from installed status and
truthfully denies account availability; its packaged bytes remain unchanged.

Owned changes: this evidence directory, runtime contract, WS-001 navigation patch,
architecture index, generated `docs/README.md` if changed, and updater-only journal
transitions. Checkout was clean on entry. All MS-001 artifacts and all S01–S04
reports/receipts remain unchanged. No branches, commits, remote writes, dependency
installation or foreign cleanup were performed.

[Checks](checks-01.json) records actual local/documentation/profile outcomes;
[receipts](receipts) contains immutable transition evidence. Structural validation
proves bindings only. A review-ready receipt has no successor and pauses the same
stage for the real owner decision. Final acceptance requires a new ready receipt;
this report and the original receipt must remain unchanged when that decision arrives.
