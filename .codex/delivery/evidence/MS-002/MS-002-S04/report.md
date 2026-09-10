# MS-002-S04 — New installed candidate and target proof

**Accepted with limitations by the owner.** [Acceptance decision](owner-acceptance-06.json)
supersedes the earlier pause/stop notes retained below as execution history.
The journal records `accepted`; failed and unexecuted checks remain unverified.

[Plan MS-002 1.0.0](../../../../../docs/architecture/planning/milestones/MS-002/plan.md).
[Journal](../../../ledgers/MS-002.md) owns mutable execution state. The current
owner request selects S04 only. Normal advance, entry preflight and this session's
exclusive claim succeeded. S05 execution and publication are not authorized.

## Candidate and source identity

Delivery `0.1.0-internal.20260910.ms002.s04.2` contains application image version
`0.1.0-internal.20260910.ms002.s04.1`, the standalone installer, independently
selected reader/config inventory, six retained native image archives, payload ZIP
and independent trusted-file inventory. The application version did not change
for the toolkit-only CSP repair. [Manifest](delivery-manifest-02.json),
[trusted files](candidate-trusted-files-02.json), [images](images-01.json),
[builds](builds-01.json) and [source snapshot](source-snapshot-01.json) bind bytes.

The protected owner-local copy is under the task's `MS-002-S04/supply-02` preparation
root. The 385-file snapshot includes accepted S01–S03 implementation. Its Git
commit is a baseline, not a claim that the working-tree overlay is committed.
Application build inputs bind the snapshot; subsequent reader/installer-only
repairs are separately bound by the toolkit's trusted inventory. Builds ran from
that private snapshot; consumer commands run under isolated Python 3.12 outside
the checkout and never build images or require Node, pip or uv.

All four API/Web architecture builds completed using the existing Dockerfiles,
locked dependencies and ordinary upstream distributions. PostgreSQL archives
reuse unchanged accepted MS-001 subjects. No old bundle, image identity, plan,
receipt, report, reader or frozen repository image inventory is replaced.
License/scanner/SBOM assurance remains report-only/not observed, not an official
release gate or an excuse to replace dependencies.

## Demonstrated defects and bounded repairs

1. Web's ordinary `THIRD-PARTY.txt` differs by architecture. The former single
   shared embedded-file record cannot truthfully describe both hashes. The internal
   reader now accepts disjoint per-platform `embedded_files`, checks required Web
   files independently for every platform, and rejects duplicate/overlapping paths.
   Common files and independent source/migration inventory remain strict. Both
   original notice files stay in their images. The release profile is unchanged.
2. The first actual trusted packaged browser opened a blank page: `style-src 'self'`
   blocked styled-components' style elements. The installed Web configuration now
   injects a request-specific nonce before the application module and binds the
   script/style policy to the same nonce. It keeps the selected styling adapter,
   forbids unrestricted inline code, and preserves the separate pinned docs policy.
   HTML ETags and conditional modification responses are disabled for this path.
   Real browser checks verify different response nonces, matching executable style
   elements and the complete working entry. Images were unchanged; a new toolkit
   and delivery identity were issued instead of relabeling the first candidate.

The first metadata preparation omitted required evidence records and failed
`DELIVERY_LIMIT`. The second fresh root encountered Docker's exhausted address
pools. Only this stage's failed candidate containers/networks were removed, without
volumes; resume then reached readiness. No global prune or old-stage cleanup ran.
The first packaged test incorrectly demanded a gateway 502; the real Nginx upstream
timeout returned 504. The harness now admits either gateway failure while requiring
truthful failure UI and recovery. Earlier failures are not passing evidence.

## Observed Mac proof

[Checks](checks-01.json) separates source, browser and failed-attempt outcomes.
[Mac loopback runtime](mac-local-runtime-01.json) records exact root identity,
images/config, supported schema, actual service limits/samples, commands and results.

- Native Docker ARM64 29.6.2, Compose 5.3.1; fresh isolated standalone installation.
- Trusted loopback HTTPS; real restricted ingress, wrong Host/Origin, forbidden
  product endpoints/methods and no HTTP fallback.
- Actual invalid certificate/name/key/expiry and Nginx candidate rejection;
  unchanged active config, successful valid rotation and real readiness.
- CLI stop, corrupt retained archive rejection, byte-exact restoration and resume;
  installation ID, port, secret, supported schema and service-owned artifact retained.
- Foreign Roehub container IDs/start times unchanged through these checks. The owner
  subsequently authorized temporary Docker Desktop shutdown for sequential Linux
  work, retaining those containers' data/volumes.
- Four actual packaged Chromium journeys at all ADR anchors, with trusted TLS,
  real PostgreSQL/schema/read-only storage/API faults, stale-success removal,
  retry recovery, RU/EN, keyboard/focus, 200% CSS layout zoom and public help.
  Browser chrome zoom, assistive-technology speech and final owner visual acceptance
  are separate. [Screenshots](screenshots/web-1440-entry-ru.png) retain rendered proof.
- Explicit Mac LAN origin `https://192.168.0.120:8443` reaches the real entry with
  trust on the host. [Capture](mac-lan-01.png) is same-host LAN evidence only.

Source checks: 93 bundle tests, 21 installer tests, focused Ruff and Pyright passed.
The complete packaged browser run passed four tests in about 2.2 minutes. Actual
command parameters and boundary are in the check record. The grouped local handoff
gate passed after the owner-deferral update: [check record](checks-02.json).

## Remaining target proof

The owner explicitly deferred second-MacBook CA trust setup and trusted Safari
proof to separate follow-up and removed that proof as an S04 completion blocker.
[Decision and observed boundary](owner-decision-02.json) record the current authority.
The page opened in Brave on that computer, with a not-secure indicator; trusted
HTTPS and Safari are **not verified**. This changes the S04 acceptance boundary
for AC-05/07, not the software TLS policy. The accepted plan bytes remain preserved.
Sequential Ubuntu ARM64 installation proof remains required and pending. The selected guest is Ubuntu 24.04.4 ARM64 at its observed bridged IPv4;
a prepared owner-local ISO carries prebuilt supply, guest leaf TLS inputs, public
CA and bounded test scripts. It contains no CA private key or source build target.
Guest agent access is unavailable; native keyboard automation was unreliable, so
precise owner-assisted mounting/execution is prepared rather than assuming success.

The ISO is attached to the selected UTM guest. Mac LAN was stopped through its
installer and the authorized Docker Desktop shutdown made its API unavailable
before guest Docker startup. Owner-assisted guest setup is pending.

S04 acceptance and its ready receipt are not claimed until the remaining Linux
evidence exists under the amended owner boundary. S05 execution remains unauthorized.

## Contract impact, ownership and handoff

`compatible-change`: new reader with old internal bundles; required per-platform
notices remain checked. `breaking-change`: an old reader rejects new per-platform
metadata, so this candidate requires its exact independently trusted toolkit.
`compatible-change`: installed nonce policy restores the selected entry under
restricted CSP, while preserving docs policy and fixed ingress. No schema head,
Identity/API DTO, dependency, architecture, external distribution or release change.

Owned repository implementation: `tools/custometry_quality/delivery_bundle.py`,
`tools/custometry_quality/installation.py`, focused producer regression and the new
`tests/e2e/ms-002-installation/packaged*` harness. Existing S03 app, localization,
UI foundation, help, evidence and journal changes are preserved as input; they are
not claimed as S04-authored. Runtime documentation and architecture navigation
receive separable S04 updates; journal changes use only the updater.

C04 continues to receive `0009_notifications`, versioned installation identity,
private file secrets and artifact root, explicit trusted origin, installation-only
GET ingress, the bounded operational DTO, and shared pilot entry primitives.
`ready_for_bootstrap`/`bootstrap_not_available` do not mean an account/workspace
exists. No full product, universal AMD64/Linux, production egress, cross-version
upgrade/rollback or official-release acceptance follows from this evidence.

## Linux preparation failure and recovery input

The first real Ubuntu attempt mounted the ISO successfully, then stopped with
`TLS_INPUT` before installation state persistence. The guest directory listing
confirmed `rootca.pem` while the harness requests `rootCA.pem`; all three PEM
file sizes match the prepared inputs. [Diagnosis](linux-tls-input-02.json) binds
the observed cause and narrow rename/retry instruction. The subsequent rename passed TLS validation. Three toolkit source paths were
then missing; hash-verified restoration succeeded. See the final handoff below.

## Final owner-requested stop

[Final evidence and remaining boundary](handoff-stop-05.json) supersede earlier
pending-action notes in this report. The owner requested stopping further work
after the Linux recovery result. No further guest commands are requested.

The exact candidate reached real Ubuntu loopback readiness through standalone
installer resume: `custometry-33f9c68221f6a375901b5054`,
`https://127.0.0.1:32768`, application `.s04.1`, delivery `.s04.2`.
The source-path repair verified expected hashes and retained the original harness
and installation. The subsequent read-only artifact drill timed out while waiting
for `STORAGE_UNAVAILABLE`. Its cause is undetermined. The harness has a finally
cleanup that restores the canonical API configuration; the supplied traceback
shows only the original assertion, but final readiness was not independently
rechecked. Linux LAN and the later rotation/preservation/resource checks did not
run. No complete Linux criterion map or successful target campaign is claimed.

S04 work is handed off with partial proof and `needs_input`, not `accepted`.
No ready receipt is issued. The second-MacBook trust/Safari deferral remains
authoritative and is unrelated to the remaining Linux evidence gap. Continuation
requires a new owner request; S05 and publication remain disallowed. Mac Docker
Desktop remains stopped as last observed; guest Docker is not shut down by this
handoff. All existing data and prior evidence are retained.

## Accepted boundary and criterion map

The owner accepts the completed macOS delivery and partial Linux result, explicitly
removing outstanding Linux/Safari proof as S04 acceptance blockers. No product
policy, certificate bypass, dependency or packaged byte changes accompany this
decision. Original plan and prompt bindings remain unchanged; current authority
is the immutable [owner acceptance](owner-acceptance-06.json).

| Criteria | Mac target | Linux target / limitation |
| --- | --- | --- |
| AC-01/07 packaging | New exact candidate, native consumer and retained dual-architecture archives verified | Exact trusted supply repaired and verified; standalone resume reached ready |
| AC-02/03/04/06/07 installation | Ownership, migration/schema/readiness, storage, recovery and resource observations in Mac runtime evidence | Ready observed; storage negative timed out; remaining campaign unverified and owner-accepted limitation |
| AC-05/07 packaged HTTPS | Trusted actual packaged Chromium journey passed; same-host LAN entry observed | LAN/browser campaign unexecuted; second-MacBook trusted Safari deferred |

S05 declared inputs (plan, this report, installer) exist and have been inspected.
It receives the exact candidate and these accepted limitations; it is not enabled
or executed by this S04-only request. C04 handoff and foreign-change exclusions
above remain applicable. Receipt readiness refers to this owner-amended boundary.
