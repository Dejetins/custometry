# MS-002-S01 — Persistent installer and selected target preparation

Plan: [MS-002 1.0.0](../../../../../docs/architecture/planning/milestones/MS-002/plan.md).
[Journal](../../../ledgers/MS-002.md) owns state and permission; this is the S01
execution report. The actual owner stage request authorized implementation and
selected host setup. No publication, next-stage execution or subagent was used.

## Delivered scope and boundary

The new [installer](../../../../../tools/custometry_quality/installation.py),
[thin launcher](../../../../../deploy/compose/install.sh) and
[standalone packager](../../../../../deploy/compose/package-installer.py) implement
private persistent identity, engine binding, lock, atomic state, verified retained
reader acquisition, file secrets, owned Compose configuration, migration ordering,
status, stop and resume. The shared consumer now validates independent inventory
paths before copying. The original MS-001 reader, toolkit, bundle, domain schema
and `0009_notifications` bytes are preserved.

S01 always reports `ready: false`, URL null and `HTTPS_NOT_IMPLEMENTED` after
successful migration. API/Web/Edge have no published ingress and are not started
by this increment. S02 owns TLS validation/rotation, actual HTTPS mapping,
application startup and stronger readiness. No complete installation, UI, LAN,
bootstrap, production, release or peak-resource claim is made.

## Observed validation

- Entry preflight passed, and the actual session obtained the exclusive S01 claim.
- [Runtime 01](runtime-01.json): real ARM64 import and migration, standalone
  isolated interpreter, repeated install, stop/status/resume/status, preserved
  installation ID and secrets, retained PG-volume sentinel, 5,000 demo rows through
  `demo_reader`, and two foreign container identities/start times unchanged.
- [Migration failure 01](migration-failure-01.json): injected a real one-shot
  process exit 23 before Alembic in a second new owned core installation. It left
  state failed at acquired and an empty migration head. Normal resume reached
  `0009_notifications` with the same ID/secret; stop retained its volumes.
- [Runtime 02](runtime-02.json) repeats persistence proof against the current toolkit.
- [Negative runtime checks](negatives-runtime-01.json) prove competing root lock rejection and corrupt acquired archive rejection, followed by exact-byte restoration and successful resume.
- [Resource and input record](resources-inputs-01.json) captures selected prerequisites, accounting and original protected-input integrity.
- Focused installer/consumer/bundle tests: 77 passed. Focused Ruff and Pyright
  passed. Immutable command records and final current-byte checks are recorded
  at handoff; earlier tests are not stronger runtime proof.
- A runtime rerun harness initially queried the already-stopped primary DB and
  exited before its first assertion. Its setup was corrected to resume that
  same owned installation first; this was a harness prerequisite error, not a
  passing runtime observation.

## Criterion and requirement coverage

| Criterion / requirement | Evidence and actual boundary |
|---|---|
| AC-01; TECH-01/02; GOAL-007 | Standard-library toolkit under Python 3.12 `-I` outside the checkout; original trusted reader and independent inventory; matching native image subjects; hostile paths/digests/platform/store negative tests. No consumer builds |
| AC-02; TECH-03; SEC-007/012 | Random retained ID, exact context/engine binding, POSIX competing-process lock, protected file modes, safe codes, foreign-root/resource rejection, immutable config checks, secret/port preservation |
| AC-06; OPS-001/002 | Real failed one-shot, empty DB after failure, successful resume, persistent DB sentinel and non-destructive stop. Unknown heads fail for forward repair; no downgrade or adopted experimental DB |
| SCALE-003/004 | Fixed local canonical artifact mount, runtime UID ownership and no remote-engine topology. Broader workers remain out of scope |
| DEC-02/03 | Explicit Python 3.12.12; official mkcert 1.4.4 and UTM 4.7.5; verified Ubuntu 24.04.4 ARM64 ISO; selected 4 CPU/8 GiB/40 GiB bridged VM. Exact target completion/trust observations below |

## Target/input record

The primary owned installation is `custometry-a38aca6eda3ececd01c10b29`, using
retained delivery `0.1.0-internal.20260908.s03.3`. Docker 29.6.2 is native ARM64
with containerd store and about 7.75 GiB engine memory. All product service caps
including optional demo and migration total 3,154,116,608 bytes and four CPUs.
The 25 GiB ceiling, acquisition copies, native unpacked image accounting and
artifact temporary reserve are admission/accounting checks, not a live quota.

Official setup inputs:

| Input | Version / integrity | Observation |
|---|---|---|
| Python | 3.12.12, existing explicitly selected interpreter | No default PATH replacement, compilation or consumer package installation |
| [UTM official distribution](https://docs.getutm.app/installation/macos/) | 4.7.5; DMG SHA-256 `a8435c93cfb5f8bbfeea4b134cfad1ac66b67632b75e438c63b1a8ae043bef0e` | Matches official release asset digest; macOS code signature verified; application installed |
| [Ubuntu ARM64 ISO](https://cdimage.ubuntu.com/ubuntu/releases/24.04/release/) | 24.04.4; SHA-256 `9a6ce6d7e66c8abed24d24944570a495caca80b3b0007df02818e13829f27f32` | Matches official SHA256SUMS; booted in native VM, DHCP and Ubuntu mirror checks passed |
| [mkcert](https://github.com/FiloSottile/mkcert/releases/tag/v1.4.4) | 1.4.4 darwin-arm64 | Official prebuilt executable; isolated CA and local certificate generated; macOS trust verification passed |

VM `Custometry MS-002 Ubuntu 24.04 ARM64` is configured for native hypervisor,
4 CPU, 8192 MiB memory, sparse 40 GiB VirtIO disk and bridge on Wi-Fi. No host
shared folder or SSH service was added. The owner personally completed the guest
account/profile screen; no password was requested in chat or retained in evidence.
Ubuntu 24.04.4 is installed and booted from its disk (kernel 6.8.0-139-generic, aarch64). The owner completed guest sudo authentication. [Guest setup](guest-setup-02.json) confirms Python 3.12.3, Docker 29.6.2 (build dfc4efb), Compose 2.40.3 and containerd.io 2.3.5. Docker configuration validates with containerd snapshotter enabled; docker.service, docker.socket and containerd.service are inactive and disabled. The public CA is installed and OpenSSL verifies it through the guest trust store. The first setup script stopped at a case-sensitive CA filename mismatch on ISO; a separately inspected lowercase-file ISO completed that step without reinstalling packages. No guest product installation or second active engine is claimed.

CA trust installation through the native administrator command failed with
`The authorization was denied since no user interaction was possible`.
The owner subsequently ran the prepared `install-local-trust.command` with administrator authentication. An independent `security verify-cert` for the local certificate and 127.0.0.1 then returned exit 0 and certificate verification successful. CT/SCT informational output does not constitute public CT qualification. Public CA SHA-256 fingerprint:
`61837d1b968a0a914ffb5fb094eff810d0ed7bb7acb2f081fc8607794c8d2336`.
CA private key stays outside the installer root and every container. Generated
certificates are preparation, not HTTPS acceptance.

## Contract impact, ownership and documentation

`compatible-change`: a new isolated CLI/state/config lifecycle for fresh internal
installations. The existing disposable consumer and developer HTTP entry retain
behavior; the shared inventory check rejects hostile paths before writes.
`none`: API DTOs, business/domain schemas, migration bytes, existing bundle/image
identities and UI code. S02's planned transport/readiness changes are not delivered
here. State is versioned and tied to its engine; there is no cross-version upgrade,
rollback, uninstall or directory/volume adoption contract.

Owned paths: installer, launcher, packager, consumer inventory hunk,
[focused tests](../../../../../tests/tooling/test_installation.py), runtime contract
revision 21, architecture navigation, generated contributor index as applicable,
this evidence directory and normal updater-owned S01 journal transitions. The
checkout was clean on entry. Preserve all MS-001 bytes and unrelated host resources;
no broad staging, commits, branches, remote writes or cleanup were performed.

[Runtime runbook](../../../../../docs/architecture/runtime-network-installation.md#persistent-installer-increment--ms-002-s01)
links back to this report; architecture navigation links both. The plan hash and
parent/child planning bindings stay unchanged. Product requirements and accepted
ADRs require no amendment; no product or architecture decision is silently changed.

## Handoff and residual work

The real S02 prompt was read and its declared inputs checked: this report and the
installer are S01-produced inputs. S02 is not executed by this request. Its entry
permission is recorded separately by the journal after S01 acceptance, never
inferred from these local checks. Guest preparation and administrator trust are complete at the prerequisite boundary recorded above. The M5 owned installations are stopped with volumes retained; foreign resources remain preserved. S02 entry files exist and its prompt was inspected, but successor execution remains disallowed because this request authorizes S01 only. A separate S02 request and normal advance are required.

Final local documentation gate: `uv run --locked python -m tools.check --scope local` passed after target-record updates. Focused Python source hashes still match [checks 01](checks-01.json); runtime proof against that toolkit remains applicable. [Host trust](host-trust-01.json) and guest setup record the completed administrator operations. The receipt snapshots mutable source files so later stages can evolve them without altering consumed evidence.
