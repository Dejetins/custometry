---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "milestone",
  "doc_id": "MS-002",
  "title": "Guided installation, HTTPS and the first-run Web entry",
  "version": "1.0.0",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "WS-001",
    "path": "docs/architecture/planning/directions/DIR-006/workstreams/WS-001.md",
    "version": "1.0.7"
  },
  "direction_ref": "DIR-006",
  "baseline_ref": {
    "commit": "c5a5699876be70c83802c7fb0149db8da50eb921",
    "evidence_refs": [
      "docs/architecture/planning/milestones/MS-002/plan.md#current-state-evidence"
    ]
  },
  "requirement_refs": [
    {
      "source": "custometry-technical-blueprint-ru.md",
      "revision": "sha256:183d9d2f2070cb8e651eca46fa44244b0d0af2a914830bcee6e5716ae15fd163",
      "ids": [
        "GOAL-007",
        "SEC-001",
        "SEC-007",
        "SEC-009",
        "SEC-012",
        "SEC-016",
        "SEC-017",
        "SEC-018",
        "OPS-001",
        "OPS-002",
        "SCALE-003",
        "SCALE-004",
        "I18N-001",
        "I18N-002",
        "I18N-004",
        "A11Y-001",
        "A11Y-003",
        "A11Y-005",
        "A11Y-008",
        "WEB-ARCH-001",
        "WEB-ARCH-002",
        "WEB-ARCH-003",
        "WEB-ARCH-004",
        "WEB-ARCH-005",
        "WEB-ARCH-006"
      ]
    },
    {
      "source": "custometry-ui-blueprint-ru.md",
      "revision": "sha256:d989e250c12598179bb1c70a5e111bd9fc88839b2e24f3f5b7b55016e99023f6",
      "ids": [
        "UI-AUTH-002",
        "UI-AUTH-005",
        "UI-CORE-001"
      ]
    }
  ],
  "decision_refs": [
    "WS-001/DEC-03",
    "WS-001/DEC-05",
    "WS-001/DEC-07",
    "WS-001/DEC-08",
    "WS-001/DEC-10",
    "ADR-0002@2",
    "ADR-0007@2",
    "MS-002/DEC-01",
    "MS-002/DEC-02",
    "MS-002/DEC-03",
    "MS-002/DEC-04",
    "MS-002/DEC-05"
  ],
  "supersedes_ref": null,
  "execution_ref": {
    "path": ".codex/delivery/ledgers/MS-002.md",
    "schema_version": "prompt-pack-ledger/v1"
  }
}
---

# MS-002 — Guided installation, HTTPS and the first-run Web entry

This is the accepted L3 plan under [DIR-006](../../directions/DIR-006/direction.md)
and [WS-001/C03](../../directions/DIR-006/workstreams/WS-001.md).
The owner selected this outcome and incremental pilot alignment and resolved
DEC-02..04 on 2026-09-09: Python 3.12 with Docker, mkcert/UTM with Ubuntu ARM64,
and a second MacBook on the home Wi-Fi network. These choices are fixed; the
owner authorized this plan's five-stage pack and journal preparation on 2026-09-10.
This authorizes preparation/publication only; implementation starts on a separate
explicit stage-execution request.

## 1. Result and boundaries

| Item | Definition |
|---|---|
| Before / after | The accepted MS-001 bundle can be imported and exercised by a disposable engineering harness. After MS-002, an administrator runs a guided persistent installer, receives a verified HTTPS address and opens a truthful first-run screen using the accepted pilot's visual language. |
| Included | Internal bundle acquisition; engine/resource/path/port preflight; installation identity and file secrets; migration ordering; Edge HTTPS; safe local and explicit LAN entry; repeat/resume/stop; real readiness; first-run UI; a newly versioned bundle containing these changes; Mac and Linux VM evidence. |
| Excluded | Account/workspace creation, sign-in/logout and authenticated workspace navigation belong to C04. Staff administration, source connection, ingestion, analytics and reports follow the accepted map. No fabricated workspace, KPI or data-ready state; no complete pilot implementation in this milestone. |
| Preserved implementation | MS-001 bundle/reader and platform evidence; existing Compose/network topology, PostgreSQL/Alembic, API and frontend stack. Preserve the developer bootstrap and existing feature routes behind their current development boundary. |
| Requirement allocation | SEC-001/007/012/016/017 and OPS-001/002 apply to installation/transport/readiness now. SCALE-003 covers the installation-owned canonical artifact directory, not future worker qualification; SCALE-004 excludes remote topology. I18N/A11Y/WEB-ARCH apply to the shipped entry screen. UI-AUTH-002/005 and UI-CORE-001 are downstream consumers, not completion claims here. SEC-009 and production SEC-018 retain their separate official-release/target-hardening boundary. |
| Authority | The 2026-09-10 request accepts this plan as the pack source and authorizes validator repair, five prompts, one journal, verification and publication to main through a technical branch/PR, followed by synchronization and technical-branch deletion. It does not start product stages or host setup. Agent assignment remains with the owner. |

### Current-state evidence

All code observations below refer to the baseline commit in metadata. They are
selective evidence for C03, not a fresh audit of the entire platform.

| Claim ID | Capability / requirement | Observation | Evidence + revision | Gap / uncertainty | Next resolution |
|---|---|---|---|---|---|
| MS-002/EV-01 | Prebuilt supply | `boundary_verified`: MS-001 supplies the internal bundle, exact reader, native ARM64/AMD64 import and packaged Web/API evidence | [S05 handoff](../../../runtime-network-installation.md#s05-installation-author-handoff), runtime doc_version 20; [completed journal](../../../../../.codex/delivery/ledgers/MS-001.md) and linked owner acceptance | This is not persistent installation, TLS or bootstrap proof | Reuse the supply mechanism; produce a new bundle after C03 code changes |
| MS-002/EV-02 | Installation lifecycle | `code_observed`: [bootstrap.sh](../../../../../deploy/compose/bootstrap.sh) manages repository-relative HTTP startup; [delivery_consumer.py](../../../../../tools/custometry_quality/delivery_consumer.py) verifies/imports a disposable bundle | Baseline files; [S04 corrections](../../../../../.codex/delivery/evidence/MS-001/MS-001-S04/runtime-corrections.md) | Neither is the persistent guided installer; the consumer deletes owned volumes by default | S01, reuse bounded acquisition/validation logic, never run the destructive smoke lifecycle as an installer |
| MS-002/EV-03 | Ready signal | `code_observed`: [health.py](../../../../../apps/api/src/custometry_api/health.py) checks DB connectivity and presence of `platform_metadata`; [main.py](../../../../../apps/api/src/custometry_api/main.py) exposes small health/version DTOs | Baseline source and existing integration tests | Table existence does not establish the required migration head, writable artifact storage or actual HTTPS origin | S02 |
| MS-002/EV-04 | UI conformity | `code_observed`: current [FoundationHome](../../../../../apps/web/src/app/shell/CompatibilitySurfaces.tsx) and [S04 screenshot](../../../../../.codex/delivery/evidence/MS-001/MS-001-S04/web.png) show a generic Foundation landing page | Accepted [pilot](../../../ui/target-pilot/README.md), HTML SHA-256 `b54b8b77d677d57869b0065dbe3aa005f13070297dface19ba98938f50d83700` | Runtime success did not prove pilot conformity; the pilot does not depict an installer screen | S03: carry shared visual rules into the entry screen; name derived layout decisions and compare them with the source |
| MS-002/EV-05 | Target availability | `boundary_verified`, read-only observation on 2026-09-09: current context `desktop-linux`, Linux/aarch64 Docker `29.6.2`, containerd image store; Docker.app exists | `docker context show`; selected fields from `docker info`; bounded command lookup | UTM and mkcert were not found in the checked app/PATH locations; no guest or second-computer proof observed. PATH `python3` is 3.14.6; repository Python is 3.12 | DEC-02..04 and authorized S01 environment preparation; do not change host defaults |

### Dependencies and sources

| Dependency ID | Provider + exact basis | Required contribution | Consumer / needed before | Satisfaction / integration owner |
|---|---|---|---|---|
| MS-002/DEP-01 | [MS-001](../MS-001/plan.md) 2.2.0, runtime handoff 20, completed journal | Internal delivery `0.1.0-internal.20260908.s03.3`; migration/read/write head `0009_notifications`; protected trusted file inventory and retained toolkit | S01 design and acquisition reuse | Existing handoff; DIR-006 owns installed integration. Preserve the exact old reader for the old bundle |
| MS-002/DEP-02 | [WS-001](../../directions/DIR-006/workstreams/WS-001.md) 1.0.7, unchanged accepted scope 1.0.0; [MAP-001](../../project-map.md) accepted sequence 1.2.0 | C03/C04 separation, M5/Linux, HTTPS, explicit LAN, resource/ownership rules | All stages | Accepted sources; this plan resolves ENG-02/03/06 within C03 |
| MS-002/DEP-03 | [Runtime contract](../../../runtime-network-installation.md) 20; [ADR-0002](../../../../adr/0002-edge-ingress-network-segmentation.md) 2 | Edge TLS custody, fixed upstream, separate networks, installation lifecycle | S01/S02 | Infra integration owner; no new context or cross-domain table access |
| MS-002/DEP-04 | [UI source contract](../../../ui/custometry-web-implementation-source-contract-v1.md) 3; pilot hash above; [ADR-0007](../../../../adr/0007-responsive-web-frontend-platform.md) 2; [context map](../../../bounded-context-map.md) 13 | UI source/technology/ownership and separate runtime/conformity evidence | S03 | DIR-005 owns presentation; DIR-006 packages it in S04 |
| MS-002/DEP-05 | [Machine blueprint](../../../../../custometry-technical-blueprint-ru.md) 0.11.0-draft; [human mirror](../../../../../custometry-technical-blueprint-human-ru.md), SHA-256 `a8b027647e200e73dd66dbd017ae8f921b314e4e0c47a2d026768197ffca34c8`; UI 0.9.0-draft | Selected requirement clauses, unchanged business/security meaning | All stages | Exact revisions above; no new product requirement is silently created by this plan |
| MS-002/DEP-06 | Owner-accepted DEC-02/03/04 and target record | Python 3.12 with Docker; mkcert; Ubuntu ARM64 in UTM; second MacBook on home Wi-Fi | Decisions resolved; concrete versions, addresses, reachability and trust setup before S04 proof | Engineering records these execution inputs in existing stage evidence; owner assists with the second MacBook when needed |

There is one linear stage chain. C03 does not wait for completion of DIR-001 or
DIR-005. Identity account/permission state remains untouched and owned by C04.

## 2. Implementation decisions

The following choices are binding for this pack. Agents implement them;
discovering a gap does not authorize another architecture.

| Decision / boundary | Current design | Selected proposal and reason | Owner / source | Compatibility | Migration / recovery | Proof |
|---|---|---|---|---|---|---|
| MS-002/TECH-01 — installer | Repository Bash launcher plus standard-library Python bundle tools | One small Python 3.12 CLI under the existing quality tooling, with a thin distributable launcher. Use `argparse`, `pathlib`, `json`, `subprocess`, `ssl`, `secrets`, `fcntl`; call Docker Compose and OpenSSL. Reuse the reader and safe extraction/hash checks. No pip/uv/Node requirement on the consumer, Python package dependency, installer framework or native GUI | DIR-006; DEC-02 accepted by owner on 2026-09-09 | `compatible-change`: separate internal installer entry; developer bootstrap remains supported | Trusted toolkit distributed alongside bundle; no execution from an unverified archive, no host Python replacement | AC-01/02 |
| MS-002/TECH-02 — supply | MS-001 internal owner-local directory plus trusted inventory | Same internal-development profile and protected local handoff. S04 rebuilds changed API/Web contents into a new version/digest and retains both existing image architectures. Load the matching architecture only; no consumer source build or new registry/signing stack | MS-001 + runtime 20 | `compatible-change` for fresh installations of the newly identified bundle; old bundle identity stays immutable | Verify trusted inventory before reader execution/import; failed acquisition leaves installed state intact | AC-01/07 |
| MS-002/TECH-03 — ownership | Repository env file and Compose volumes | User-selected empty private root, persistent random installation ID/Compose name, pinned engine context, atomic JSON state, file secrets and one artifact root. Explicitly define layout and retry rules below | DIR-006 / ENG-06 | `compatible-change`: new isolated installation contract; no adoption of unknown directories or experimental DBs | Preserve identity on retry; no uninstall, global prune or automatic data deletion | AC-02/06 |
| MS-002/TECH-04 — HTTPS | Edge HTTP, fixed Web upstream | Existing Nginx Edge terminates HTTPS on internal 8443, with read-only key/chain. Local test issuance by mkcert outside Edge; existing OpenSSL verifies pair/name/chain/expiry. Support supplied PEM key/chain/trust-root file references through the same path. No ACME service, custom CA code or automatic certificate renewal daemon | ADR-0002; DEC-03 | `breaking-change` for an HTTP client moved onto the new installed ingress; required accepted transport change. Developer HTTP mode stays separate | Validate candidate, test Nginx config, activate, test trusted handshake; preserve last valid revision on failure, never HTTP/expired/revoked fallback | AC-03 |
| MS-002/TECH-05 — safe first entry | API mounts existing product routes; generic Web shell | Installed C03 ingress serves only `/`, required same-origin static assets, public `/docs/`, and GET health/version/installation status. All other API paths/methods and product routes are denied. No bootstrap token is generated or mounted yet. C04 explicitly replaces this installation-only ingress configuration when its protected journey is ready | SEC-012/016; WS-001 C04 boundary | `breaking-change` relative to unrestricted Foundation smoke ingress, intentionally confined to this new installed profile; existing development/API consumers remain | Keep restriction in a separately generated installed config; no runtime admin bypass or user-controlled upstream | AC-03/04 |
| MS-002/TECH-06 — readiness | DB/table boolean | Keep existing `/health/live`, `/health/ready`, `/version` DTOs; strengthen readiness to check DB, exact supported migration head and artifact-root probe. Add the bounded read-only status DTO below; installer separately checks configured files, image identity and real TLS/port before declaring installation successful | OPS-002; API composition owns operational health | `breaking-change` to the weak readiness guarantee when schema/storage are invalid; wire this intentionally with the new storage/config in one candidate. New status endpoint is additive for the new UI | Never apply migrations from a readiness request. Wrong schema or missing storage stays not ready; redacted stable reasons | AC-04 |
| MS-002/TECH-07 — UI | Existing React app, shared theme/components and FoundationHome | Reuse ADR-0007 and `packages/ui-foundation`; introduce pilot-derived entry components/tokens there, scoped to the installation entry until later consumers migrate. Render the existing root entry in a minimal installation shell, without a workspace rail before a workspace exists. No new UI library, copied prototype scripts, chart engine or parallel design system | DIR-005; accepted pilot + current owner correction | `breaking-change` to the installed root's displayed content, expected; route path remains `/`. Existing product route identities and other theme behavior are preserved | Keep shared token additions scoped; no global restyling of unrelated screens. C04 consumes the same primitives for its authenticated shell | AC-05 |

### Installer contract and bounded failure behavior

The selected target CLI is `custometry-install` with `install`, `status`, `resume`, `stop`
and `rotate-tls`. `install` guides directory, protected supply location, access
mode, certificate file references and optional demo selection; it also accepts
equivalent explicit arguments. These are target commands to implement in S01/S02,
not existing runnable commands. Keep one JSON state schema
`custometry-installation/v1`; do not build a workflow engine.

| Boundary | Fixed implementation choice |
|---|---|
| Root layout | `<root>/installation.json`, `config/`, `secrets/`, `tls/`, `artifacts/`, `acquisition/`, `logs/`. Root/private directories 0700; state/config/logs 0600; mounted secret/key leaves read-only 0444 under private parents, as required by the current non-root bind-mount contract. Artifact mount uses the API's existing runtime UID, writable only to the owning service; never solve permissions with world-writable directories. |
| Identity and lock | Generate one `custometry-<random-id>` and pin Docker context/engine identity. POSIX file lock under the private root excludes simultaneous mutation commands. Parse state as data, never shell-source it. Write via temporary sibling + atomic replacement. Unknown schema, symlink escape, foreign directory/volume labels or engine mismatch fails closed. |
| Volume ownership | Exact Compose-owned `control_db_data`; `demo_source_data` only if explicitly selected. Bind the canonical `artifacts/` directory to `/var/lib/custometry/artifacts`. Record volume labels, path ownership, image digests and selected platform; image presence does not grant image deletion authority. No additional DB or installer tables. |
| State / retry | States: `prepared`, `acquired`, `migrated`, `ready`, `failed`, `stopped`; record `last_completed_step` and stable failure code. Resume reconciles actual Docker/DB/filesystem state and reruns only idempotent incomplete operations. Preserve secrets, identity, data and selected port. A crashed migration is inspected against actual Alembic state before retry; unknown/partially incompatible state requires forward repair. |
| Preflight | Check explicitly selected Python 3.12 interpreter, Docker/Compose, native Linux architecture, containerd image store, one active target engine, engine/context identity, available RAM/CPU/disk, root and secret permissions, ports and TLS inputs. Reject unsupported engine/store with actionable instructions; never switch stores/contexts or install host software silently. |
| Resources | Retain 6 GiB workload and 25 GiB owned-data ceilings. Set total service limits within the RAM budget, CPU cap to 4 vCPUs or fewer available, whichever is lower. Account for archive/layer expansion, artifact temporary data and retained candidate files in disk preflight. Reject insufficiency before acquisition/start; no arbitrary performance SLO, new storage-quota service or large benchmark. |
| Origin and ports | Default `https://127.0.0.1:<port>` with loopback bind. Explicit unprivileged port, else retained installation port, else engine-selected available port persisted after inspection. Explicit occupied port fails; never silently change a saved origin. LAN requires one explicit interface IPv4 and matching exact origin/certificate SAN. No `0.0.0.0`, wildcard CORS, Internet exposure, DNS service or public hostname requirement. |
| Secrets | Use standard `secrets.token_hex(32)`; persist once, never regenerate on resume. Reuse MS-001's 64-hex demo reader password and validated mount modes. No secret contents in argv, env values, URL, browser storage, evidence or output. TLS CA private key never enters the installation bundle or any container. |
| Migrations | Start control DB, wait for its final TCP server, run the existing one-shot Alembic job, then API/Web/Edge. Keep `0009_notifications` as this milestone's schema head; no domain migration planned. Unknown existing head or failed migration prevents normal application readiness. No down-migration/experimental-state adoption. |
| Bounded waits | Retain 2-second DB connect timeout; installer readiness deadline 120 seconds with 2-second polls, individual probe timeout 5 seconds; migration/import command deadline 10 minutes. These are operational defaults, not measured SLOs. Timeout records a safe error and preserves retryable owned state; no endless retries or automatic repeated image rebuilds. |
| Stop and diagnostics | `stop` stops only the recorded Compose project without removing volumes. `status` reconciles real readiness and returns safe codes/version/URL. Installer diagnostics contain selected versions, stage, code and owned-resource identifiers; public/browser errors exclude host paths, SQL, credentials and raw process output. Keep one bounded stage report and relevant failing/successful receipts, not repeated inventories. |

### TLS and test-target selection

DEC-03 selects [mkcert](https://github.com/FiloSottile/mkcert) for this internal
development installation only. It provides local certificate issuance and trust
setup; the installer configures Nginx separately. Trust-store modification is an
explicit administrator setup step. Distribute only the public root certificate
to the selected test client; never copy its CA private key. The provided-PEM mode
keeps future production certificate custody separate. No production certificate
or automatic-renewal acceptance is claimed.

| Target | Preselected proposal | Required observation before proof |
|---|---|---|
| Mac | Owner's M5 Max, 36 GB; existing Docker Desktop/containerd engine; native ARM64 bundle; explicit Python 3.12 executable without changing PATH defaults | Exact engine/Compose/interpreter versions, resource allocation, install root, TLS issuer fingerprint and approved local/LAN origins |
| Linux | [UTM](https://docs.getutm.app/installation/macos/), native ARM64 virtualization; [Ubuntu Server 24.04 LTS ARM64](https://cdimage.ubuntu.com/ubuntu/releases/24.04/release/), 4 vCPU, 8 GiB guest RAM, 40 GiB sparse virtual disk; Docker Engine with containerd image store, Compose v2, Python 3.12 | Exact UTM/guest/engine versions and image checksum; effective product RAM/data usage separately from guest OS overhead. Guest capacity is not a waiver of the 6/25 GiB product limits |
| LAN client | Owner's second MacBook on the same home Wi-Fi network; use its standard Safari browser for the second-computer check | Record actual OS/Safari versions, IP/origin, approved certificate trust and direct reachability before S04. The owner confirmed the target, not observed connectivity or installed trust. Use bridged guest networking for LAN proof; if unavailable, report the concrete gap rather than substitute localhost/tunnelling evidence |

Run Mac and guest trials sequentially; stop the other target engine. S01 can
prepare this already-selected target when execution/host-setup authority exists.
Recording available patch versions, checksums and addresses is execution input
bookkeeping; changing the tool family, architecture or topology requires amendment.
UTM/mkcert availability was checked during planning, not installed or qualified.

### Readiness and UI contract

New API-local `GET /installation/status` (through Web at
`/api/installation/status`) returns only:

```json
{
  "schema_version": "custometry-installation-status/v1",
  "state": "ready_for_bootstrap",
  "version": "<application version>",
  "components": {"database": "ready", "schema": "ready", "storage": "ready"},
  "next_action": "bootstrap_not_available"
}
```

Allowed component values are `ready` / `not_ready`; `state` is
`ready_for_bootstrap` / `not_ready`. Return HTTP 503 when a component is not ready,
with one stable `code` (`DATABASE_UNAVAILABLE`, `SCHEMA_INCOMPATIBLE` or
`STORAGE_UNAVAILABLE`). Set `Cache-Control: no-store`. API probes only operational
state; it does not read Identity's private tables or claim that an account exists.
The name `ready_for_bootstrap` means technical prerequisites are ready, while
`next_action` states that this internal build does not implement bootstrap yet.
Generate the matching browser types/client through the existing contract path.

The screen shows product identity, installed version, a concise status summary,
the three component states, the actual browser origin, language control, retry
and public local help. On success, explain that installation is ready and account
creation is the next delivery step; do not display a dead “Create account” button.
On timeout/API loss, clear the success state and offer a bounded retry. No terminal
commands, database names, milestone IDs or internal architecture labels in the
normal user flow. Technical diagnostics stay in the operator CLI/help boundary.

Pilot inheritance is concrete: use its graphite surfaces, typography scale,
spacing, borders, icon treatment, button/input/focus states and restrained panel
composition through the existing UI foundation. Since the pilot has no installer
screen, its exact report layout is not copied here. Do not insert the old large
Foundation hero/sidebar or create a competing appearance. C04 adds the real
compact navigation rail/context once account/workspace flows exist. Analytical
tabs, filters, inspector and charts are implemented with their later consumers.

S03 compares the source and new entry at matched viewports and documents which
rules are inherited and which entry-specific layout is derived. Use the four
ADR anchors (768×1024, 1024×768, 1440×900, 1920×1080), RU/EN and a long-text check.
Retain one compact comparison and representative screenshots; test keyboard,
focus, status announcements and 200% zoom. Functional browser proof and owner
visual acceptance are separate entries in the final criterion map.

## 3. Work breakdown and ownership

| Stage | Bounded result | Dependencies | Expected owned paths / zones | Shared writer constraint | Output consumed later |
|---|---|---|---|---|---|
| MS-002-S01 | Persistent guided installer, trusted acquisition, ownership/state/lock, preflight, migration sequencing and stop/resume. Prepare the preselected test environment when authorized | Accepted plan, DEC-02/03; DEP-01 | Proposed `tools/custometry_quality/installation.py`, thin `deploy/compose/install.sh`; existing delivery helper seams; focused `tests/tooling/`; installation runbook | One stage owns installer/state/config writes; preserve MS-001 bundle/toolkit/evidence bytes | Installer contract and real owned resources; S02 adds TLS/readiness. S01 cannot claim completed installation |
| MS-002-S02 | Direct HTTPS, validated origins/ports/rotation, installation-only ingress, stronger readiness and bounded status DTO | S01 | `deploy/edge/`, installed Compose/config generator, `apps/api/src/custometry_api/{config,health,main}.py`, new bounded operational module if needed; API contracts/generated clients; integration tests | One owner for API/schema generation and installed config; do not alter private Identity/domain state | Verified API/TLS contract consumed by S03; failure/retry observations consumed by S04 |
| MS-002-S03 | Pilot-derived first-run UI with real status, safe failure/retry, RU/EN, keyboard and responsive behavior | S02 | `apps/web/src/app/` root/shell routing; proposed `apps/web/src/features/installation/`; `packages/ui-foundation`, localization; owned `tests/e2e/ms-002-installation/` harness | Shared primitives remain scoped; preserve unrelated route/theme behavior and pilot source | Working UI plus separate functional/conformity evidence; no throwaway mockup or additional approval board |
| MS-002-S04 | New versioned internal bundle and actual installation on Mac and Linux VM, local and second-computer LAN; focused negative/retry/rotation tests | S03, exact target inputs including DEC-04 | Existing bundle producer/config inventory; proposed MS-002 runbook/evidence paths; in-scope repairs to S01–S03 | Fix owned causes; reissue bundle when its bytes change, rerun affected proof only. No hosted AMD64 rerun required merely to duplicate MS-001 evidence | Exact delivered candidate identity, per-target proof, limitations and C04 handoff |
| MS-002-S05 | Consolidated criterion map, current runbook/help and C04 input handoff; owner accepts installed behavior and visual result | S04 | This plan's permitted evidence links; canonical journal through updater; stage report and affected indexes | No new feature scope and no second status register | Accepted C03 result and exact C04 prerequisites; otherwise a precise repair request |

Stages are sequential. The owner chooses agents and any delegation inside a stage.
S01 environment preparation is assigned work, not a requirement that the owner
manually complete all setup before an agent can begin. An unavailable second
computer blocks its S04 proof and final closure, not S01–S03 implementation.

## 4. Acceptance and proof allocation

| Criterion | Requirement / owner intent | Observable result | Stage | Check / real environment | Evidence / authority |
|---|---|---|---|---|---|
| MS-002/AC-01 | WS-001/AC-01; internal-first supply | Trusted versioned bundle installs without source checkout/build, pip, uv or Node on consumer; wrong digest/platform/store fails safely | S01, S04 | Standalone CLI outside checkout; real engine import; wrong checksum/platform and unsupported-store fixtures | Redacted acquisition/candidate IDs and command results; technical |
| MS-002/AC-02 | WS-001/AC-02/05; ENG-06 | Guided fresh install owns only declared root/volumes; repeat/resume retains identity, secrets, data and port; concurrent mutation/foreign root/context/occupied explicit port denied | S01, S04 | Focused CLI tests plus actual fresh and interrupted installation; pre-created foreign resource remains unchanged | Ownership/retry observations, resource accounting; technical |
| MS-002/AC-03 | SEC-001/007/012/016/017 | Trusted HTTPS on actual local and explicit LAN origins; correct security headers; no HTTP fallback, wrong-host/origin acceptance or product API exposure; only Edge publishes a port, networks remain separated | S02, S04 | Real Nginx/TLS and browser, valid/expired/wrong-name/mismatched candidates, safe rotation, second-computer access; direct allowed/denied adjacency probes | TLS public fingerprints and sanitized network/browser evidence; technical. Compose does not prove production SEC-018 egress denial |
| MS-002/AC-04 | OPS-001/002 | Missing DB, unsupported schema, unwritable artifact root and migration failure cannot produce successful installation/UI readiness; supported head succeeds fresh and on repeat | S02–S04 | Real PostgreSQL/Alembic and mounted storage; actual API success/503; installer inspects HTTPS mapping and files, not just process exit | Cause-to-safe-code mapping and recovery instructions; technical |
| MS-002/AC-05 | Pilot; I18N/A11Y/WEB-ARCH | Shipped first-run UI uses pilot-derived foundation, shows real states, has no fake workspace/data or dead actions; RU/EN, retry, keyboard and responsive behavior work | S03, S04/S05 | Owned Playwright suite against host Vite/API in S03; same core journey against the actual packaged HTTPS Web in S04, no ignored TLS errors; normalized pilot comparison | Functional browser result separately from visual comparison and owner's final visual decision |
| MS-002/AC-06 | WS-001/AC-05; OPS-001 | Stop/start and failed acquisition/migration/readiness preserve owned persistent state and foreign resources; readable recovery steps lead back to the valid candidate | S01/S02, S04 | Real failure/resume/restart drills; no destructive cleanup or downgrade used as repair | Bounded observations; technical. Account/session persistence and coherent backup/restore remain C05/SEQ-12 |
| MS-002/AC-07 | WS-001/AC-02; M5/Linux decision | One newly identified bundle is installed on native Mac-engine ARM64 and the selected Linux VM, each with local and explicit LAN proof and within resource budget | S04 | Sequential actual installations, exact bundle/image/config identities; no product source checkout on consumers | Per-target result; unavailable proof stays unobserved. No universal Linux/AMD64/production claim |
| MS-002/AC-08 | Owner workflow and documentation | All prior criteria mapped once; known limits disclosed; C04 receives installed config/schema/API/UI prerequisites and retained account-lifetime clarification | S05 | Criterion/evidence review and owner inspection of functioning entry | Single journal's final receipt plus owner decision; no closure solely from a green command |

Use the existing focused tooling/API tests and repository lint/type commands for
changed code; exact new test paths/selectors are written with the implementation.
No claim is made that those future checks already exist. Existing stable commands
include `pnpm --filter @custometry/web typecheck`, the owned Playwright config,
and, after `source scripts/activate-toolchain.sh`,
`uv run --locked python -m tools.check --scope local`.
Use `pre-push`/CI when the selected publication workflow needs it. Do not run the
official `release` profile to decide an internal-development milestone.

Preserve ordinary upstream dependencies and existing notices. License/scanner/SBOM
findings retain MS-001's internal report-only disposition; they do not trigger a
replacement library, transitive-package rewrite, new assurance project or repeated
image builds. Integrity, trustworthy inputs, secret handling and the real required
installation checks above remain necessary. Add a test for changed behavior or a
demonstrated failure; do not expand into unrelated whole-platform QA.

## 5. Execution and repair envelope

| Field | Bound |
|---|---|
| Allowed changes | Only installer, its installed config/health/status/UI integration, newly versioned packaging, focused tests and directly affected contracts/help/evidence. Reuse existing upstream packages and repository components. |
| Delegated decisions | Functions/classes/file splits inside the named zones, names not fixed by a public contract, ordinary local implementation and repair, patch-version/checksum recording within the accepted tool family, precise test selectors and redacted evidence paths. No new business threshold is delegated. |
| Fixed choices / escalation | No new dependency or major upgrade, custom replacement for an upstream library, generalized installer/state machine/PKI, new service/database/queue/UI stack, public release, change of origin/target topology, auth semantics, schema head or milestone scope. A demonstrated need becomes one concise amendment: failed requirement, existing alternative, smallest proposed change and affected proof. Continue unrelated authorized work. |
| In-scope repairs | Repair observed installer/TLS/API/UI/packaging failures within these decisions. Rebuild only after packaged bytes change; rerun checks invalidated by the repair. Existing S04 permissions/image-store corrections are inputs, not investigations to repeat. |
| Rollout / rollback | Install into a new owned root. No experimental-data migration. Before schema change, stop and amend; this plan permits none. Invalid TLS/config keeps the last valid version; never restore expired/revoked credentials. No installed cross-version upgrade/DB rollback claim. |
| Publication / host changes | DEC-05 authorizes publication of this preparation through a technical branch/PR into main and branch deletion after synchronization. Product-stage execution and selected local VM/software/trust setup require the actual stage request; OS authentication can require owner interaction. This preparation starts no host setup or external bundle distribution and grants no publication authority for later product changes. |
| Documentation | Update runtime installation contract, developer/installed-entry distinction, operational health/API contract, Web source/conformity evidence, actual public help, parent/child/index links and journal receipts when their behavior changes. Preserve MS-001 accepted bytes and history. |
| Evidence | One canonical journal, one concise report per stage and meaningful immutable receipts. Store sensitive runtime state outside Git under the owned root. No cookies, TLS/DB/CA keys, tokens, raw logs or browser storage in evidence. |

## 6. Execution artifact binding

| Field | Binding |
|---|---|
| `plan_doc` | This accepted 1.0.0 plan; its exact SHA-256 is bound identically in all five prompts and the journal |
| `prompt_pack_dir` | [Five stage prompts](../../../../../.codex/agents/generated/MS-002/MS-002-S01.md) in `.codex/agents/generated/MS-002/` |
| `stage_ledger` | [MS-002 iteration journal](../../../../../.codex/delivery/ledgers/MS-002.md), the sole execution-state source |
| Validation | `tools.custometry_quality.validate_prompt_packs`; `prompt_pack_validation --check draft/entry`; `stage_ledger preflight`; see [tooling gates](../../../tooling-gates.md#7-stage-journal-transactions) |
| Claim/update | Existing `custometry-stage-ledger/v1` POSIX lock, session ownership, CAS and atomic replacement; [current capability evidence](../../../../../.codex/delivery/evidence/MS-002/preparation/journal-capability.md) binds the repaired implementation and tested behavior |
| Mode | `manual_sequential`; initial journal `draft`, all five stages `pending`, `current_stage=null`, no claims/receipts. Only S01 may be marked entry-ready after actual checks and independent review; this is not execution authority |

Prompts preserve DEC-02..04 and distinguish future producer outputs from real
entry blockers. Exactly one independent pack review and the authoring/entry
checks are recorded in [preparation evidence](../../../../../.codex/delivery/evidence/MS-002/preparation/report.md).
The owner selects the agent and asks it to execute a stage; no Goal or later-stage
execution is implied by this pack's preparation or publication.

## 7. Owner decision packet and history

| Decision | Question / real alternative | Recommendation and consequence | Decider / status | Blocks / source |
|---|---|---|---|---|
| MS-002/DEC-01 | Next iteration and UI scope | C03 installation + pilot-derived shared entry foundation, then C04 account/workspace + authenticated shell, then data/analytics/report consumers in MAP order. No complete UI now | Owner selected this direction in the current discussion, 2026-09-09; selected scope carried into accepted plan 1.0.0 | Scope selection resolved; DEC-05 authorizes this accepted plan as the pack source |
| MS-002/DEC-02 | Internal installer prerequisites | Python 3.12 together with Docker is accepted. Reuse the existing reader/lifecycle code; no new runtime bundler or implicit Docker-only redesign | Owner explicitly answered yes on 2026-09-09; accepted, covered by 0.2.0 | Decision closed; actual interpreter selection is S01 preparation |
| MS-002/DEC-03 | Local test TLS/VM tooling | mkcert with explicit trust setup; native Ubuntu 24.04 ARM64 in UTM | Owner explicitly accepted the proposed tools on 2026-09-09; accepted, covered by 0.2.0 | Decision closed; actual installation/trust/runtime proof remains execution work |
| MS-002/DEC-04 | Second computer for LAN proof | Owner's other MacBook on the same home Wi-Fi network. Use Safari; record actual versions, addresses, trust setup and reachability before S04 | Owner identified the MacBook and home Wi-Fi on 2026-09-09; target selection resolved, covered by 0.2.0 | No further target-choice question; second-computer proof and owner interaction remain S04 inputs |
| MS-002/DEC-05 | Plan source, pack and publication | Use the current plan with resolved DEC-02..04 to author S01–S05 and one journal; repair the historical validator; verify and publish through a technical branch/PR into main, synchronize and delete the technical branch | Owner explicitly instructed execution of these four preparation steps and publication on 2026-09-10; accepted, covered by 1.0.0 | Preparation/publication authorized. Product stage execution, host changes and external bundle distribution are not started |

There are no reopened business-scope, licensing-policy, first-account-role or
source/report-order questions for C03. C04 retains its own Identity decisions and
the [account-lifetime clarification](../MS-001/plan.md#downstream-account-clarification).

| Version | Date | Change and reason | Affected references | Authority |
|---|---|---|---|---|
| 0.1.0 | 2026-09-09 | Initial C03 draft after accepted MS-001, including concrete installer/TLS/readiness/UI decisions and limits on executor discretion | WS-001 1.0.7, current navigation/indexes; completed MS-001 unchanged | Owner requested next-iteration planning and advance decision-making; exact draft not yet accepted |
| 0.2.0 | 2026-09-09 | Record owner answers: Python 3.12 with Docker, mkcert/UTM/Ubuntu ARM64, second MacBook on home Wi-Fi; close DEC-02..04 selection questions | Updated current child-version references; stage scope, criteria and MS-001 evidence unchanged | Explicit owner answers in this task; no implied execution or publication |
| 1.0.0 | 2026-09-10 | Accept the current plan as source for the authorized five-prompt pack and journal; bind preparation evidence and current updater; publish through technical branch/PR | Canonical triad, parent/index navigation and tooling contract; MS-001 remains immutable | Explicit owner preparation and publication instruction in this task |

## Mandatory documentation handoff

WS-001 registers C03/MS-002 1.0.0; project/direction navigation and contributor
indexes link the same version. Product requirements, five L2 outcomes and the
12-step MAP sequence are unchanged. Preserve completed MS-001 plan/pack/journal,
receipts and reports byte-for-byte. Update operational/API/UI docs when the
corresponding stage actually implements behavior; this plan is not runtime proof.

The 0.1.0/0.2.0 documentation checks passed; their grouped local gate exposed
live-file comparison of completed MS-001 documentation. The authorized narrow
repair now resolves only completed validation-source documents and historical
updater implementation bindings against exact retained Git bytes at the same
path. Active inputs and immutable receipts/reports remain strict. CI must retain
Git history; unavailable or mismatched bytes fail rather than rewriting acceptance.

Actual preparation checks, review, initial entry preflight and publication
outcome belong in [preparation evidence](../../../../../.codex/delivery/evidence/MS-002/preparation/report.md).
This keeps the plan digest stable while observations are added. No S01 result,
claim, synthetic product acceptance or stronger runtime proof is created here.
