---
doc_id: ARCH-RUNTIME-INSTALLATION-001
title: Custometry runtime network and installation contract
doc_version: 14
product_spec_version: 0.11.0-draft
visibility: internal
ship: false
owner: devops
requirement_ids: [SCALE-004, SEC-016, SEC-017, SEC-018]
status: accepted
proof_boundary:
  label: foundation-runtime-target-contract
  exclusions: [observed-m5-or-linux-vm-installation, release-artifact, future-egress]
---

# Custometry Runtime, Network, and Installation

## 1. Goals

The default installation must be small, understandable, and reproducible: the user receives a versioned launcher and Compose configuration, while pinned images and required assets are downloaded during installation. A multi-gigabyte standalone archive containing all layers, caches, and registries is not the primary delivery method.

After a successful pull and bootstrap, the core operates without Internet access. External access is granted only to the minimum required owners:

- connector path: reads from an explicitly configured source;
- report-delivery path: uses a configured mail transport;
- operational-notification path: Notifications-owned email and HTTPS webhook adapters use only their configured, versioned destinations when the v1 channels are enabled;
- update job: uses the approved release origin.

Web/API, PostgreSQL, Valkey, the chart renderer, scheduler/orchestrator, and other workers receive no arbitrary outbound Internet access. Edge is handled separately: Compose segmentation limits its adjacency, but its non-internal transport network may retain an ambient outbound route until target-specific production hardening is applied.

## 2. First target environment

- Apple Silicon Mac M5 Max with 36 GB host RAM, supplied by the owner on 2026-09-06;
- a Linux VM on that same Mac as the additional bounded installation test environment;
- the selected guest OS/architecture, hypervisor, engine and resource allocation are recorded before target proof; VM evidence does not qualify arbitrary Linux servers or x86_64;
- one selected Docker-compatible engine;
- normal `demo` ceiling: 6 GiB of RAM and 25 GiB of repository-owned/container data;
- CPU only, using no more than container-visible cores and the administrator cap;
- other operating systems and architectures are added only after separate platform proof.

`doctor` must detect concurrently active engines and contexts, architecture, CPU/cgroup limits, memory, disk, bind-port availability, and required CLI versions. Two parallel engines with separate images and caches are a configuration error, not additional capacity.

The 36 GB host capacity does not increase the existing demo ceilings. Only one
container engine/context is active for each target run; macOS and Linux VM tests
are sequential and report their distinct resource and network boundaries.

## 3. Download-first installation

Foundation exposes three Compose profiles/contracts:

- default core: Web, API and control PostgreSQL;
- `demo`: separate demo-source PostgreSQL in addition to core;
- `migration`: one-shot Alembic job that completes before application startup.

Full Stack developer bootstrap on the M5 Max target:

```bash
deploy/compose/bootstrap.sh --build
deploy/compose/bootstrap.sh --build --with-demo
```

This is the clean, complete `full-stack` boundary. It is required whenever a
ticket claims container, ingress, service-discovery, restart, or clean-lifecycle
behavior, but it is not the default per-save development loop. The
accepted [development runtime contract](./development-runtime-contract.md)
defines `fast-loop`, `hybrid`, `full-stack`, and `release`, including their
proof limits.

The accepted Hybrid path keeps Web/API on the host and starts only control and
demo-source PostgreSQL in containers. `scripts/dev up --mode hybrid` owns the
loopback-only infrastructure, host process groups, migration, readiness,
bounded logs, safe demo reset, and cleanup lifecycle. Generated mocks and
browser-visible mock/real switching remain separate Experience capabilities.

Release mode uses immutable GHCR references, `pull` and `--no-build`; a user installation must not silently compile the product from source. Public static `/docs` ships with the public Web surface. Authenticated operator/admin docs are excluded from that public docs image until the protected serving boundary is implemented.

The current Foundation implementation publishes only immutable SHA-scoped candidate
images after the protected `main` gate. It does not publish an accepted end-user bundle.
`bootstrap.sh --release` therefore remains a fail-closed target contract: its manifest
is parsed as strict data and must come from a future protected bundle workflow. Candidate
publication alone is not release acceptance.

The owner accepted [WS-001](planning/directions/DIR-006/workstreams/WS-001.md)
`1.0.0` on 2026-09-06. The administrator installs the supported container engine
before running the launcher; the installer checks it and gives actionable failure.
The supported path asks for the installation directory and explicit access
configuration, then handles configuration, local secrets, downloads, migrations
and readiness. It requires no source build, manual Compose/YAML or SQL editing.
First account/workspace creation happens in the browser. No separate native
graphical installer or automatic host engine installation is required.

The first delivery creates installation-owned state and need not import prior
experimental data. It preserves other installations and host resources. Repeat
installation/restart preserves identity, secrets and persistent data; migrations
remain explicit, versioned and fail closed. Whole-product updates and coherent
backup/restore qualification retain their later sequence allocation.

Target user flow:

1. Download a small signed and checksummed launcher or release configuration.
2. Run preflight for engine/context, architecture, RAM, disk, ports, filesystem, and secret-directory permissions.
3. Select and persist the ingress port and deployment identity.
4. Create secrets locally; do not obtain them from Git or print them to the terminal
   or logs. File-backed Compose secrets are plaintext host files and live only under an
   installation-owned directory with mode `0700`. Their leaf files use read-only mode
   `0444` because Compose implements file sources as bind mounts and cannot remap
   ownership for the non-root service UID; the private parent directory remains the
   host confidentiality boundary.
5. Download images by immutable digest and verify the expected platform and digest.
6. Run a separate migration job.
7. Start Compose and wait for dependency and application readiness.
8. Run protected browser/API smoke and display the actual URL.
9. Persist install state, versions and digests, and safe rollback metadata.

A build or pull exit code of `0` is insufficient: the installer checks manifest existence, platform, digest, runtime start/import, and post-start health. If the artifact was not published, the platform is unavailable, or the publication workflow was skipped, installation fails with the exact reason.

Optional air-gap export/import may be added later as a separate release artifact with inventory and checksums. It must not silently become the default and does not include build caches, package registries, or unnecessary platform layers.

### Accepted HTTPS and bootstrap boundary

Edge terminates HTTPS with one narrow exception to its former blanket secret ban:
read-only installation TLS private-key and certificate-chain files. Business,
workspace, database, source, mail, API and master-key credentials remain forbidden.
Edge has no domain state, certificate-issuance client, acquisition egress or dynamic
upstream; it retains the fixed Web upstream and separate adjacency from API.

DevOps owns the installation TLS configuration: selected mode, approved origin,
file references, public fingerprint and configuration revision. Issuance and renewal
remain outside Edge under installation custody. Preflight verifies key/chain match,
trusted name/validity, readable protected mounts and the selected origin. Rotation
validates the new pair before activation and verifies the new handshake; an invalid
candidate preserves the last valid configuration. Expired or compromised material
requires forward repair and never falls back to HTTP. Keys stay out of environment
values, images, Git, diagnostic bundles and logs. Exact certificates, origin and
renewal procedure are target inputs to settle before runtime proof.

Local access stays the default. Explicit LAN mode must pass protected browser
access from another computer; bootstrap remains protected by its host-controlled
one-time token on the configured origin. The first account receives installation
administration plus explicitly disclosed initial roles in the first workspace.
Identity owns the reviewed initial grants, normal delegation ceiling and irreversible
closure; no implicit other-workspace or PII access is created.

These are accepted target decisions under [ADR-0002](../adr/0002-edge-ingress-network-segmentation.md)
doc_version 2. Current HTTP Foundation code is not proof of their implementation.
External TLS termination is not a required installation prerequisite.
Production firewall/CNI proof under SEC-018 remains separate.

## 4. Port contract

Only the proxy publishes host ingress. PostgreSQL, Valkey, Web, and API have no host-published ports by default.

Foundation stores `CUSTOMETRY_HTTP_PORT` in ignored `.runtime.env`. Edge host-port selection order:

1. Explicit `CUSTOMETRY_HTTP_PORT`, if valid and available.
2. The port previously saved for this installation identity, if available.
3. Docker ephemeral port (`0`), which bootstrap resolves to an actual available non-privileged port and stores atomically in `.runtime.env` before the stable restart flow.

An explicitly configured occupied port is not replaced silently: preflight returns a stable error and offers automatic selection or a different explicit port. Automatic selection is protected against TOCTOU by a second check immediately before binding. After startup, the actual published mapping is read from the engine and compared with install state.

The default bind address is `127.0.0.1`. LAN exposure requires a separate explicit bind address, CORS/origin allowlist, authentication preflight, and warnings. `0.0.0.0` is never introduced as a hidden default.

Internal container ports remain stable in Compose and service discovery; dynamic selection applies only to host ingress. Documentation and UI display the actual URL rather than an assumed `localhost:<constant>`. In Foundation, the separate Edge proxy is the only public ingress boundary; Web and API do not publish host ports.

## 5. Network zones

| Zone | Participants | Contract |
|---|---|---|
| `ingress_edge` | Foundation Edge only | Host ingress; non-internal transport bridge; may have an ambient outbound route and is therefore not an egress-denial boundary |
| `edge_to_web` | Edge and Web only | Internal; Edge's only direct application adjacency |
| `web_to_api` | Web and API only | Internal; Edge is not connected to this network |
| `control` | Foundation API/control DB; target PostgreSQL, Valkey, scheduler, orchestrator, outbox, reconciler, workers | Internal only |
| `demo_source` | Demo-source PostgreSQL + authorized future connector | Internal Foundation test/source boundary; the database port is not published |
| `artifact` | Authorized API/workers through a mounted root/port | Local filesystem; path normalization, no network |
| `connector-egress` | Data worker/connector adapter | Allowlisted scheme, host, IP, port, and source only; read-only source operations |
| `mail-egress` | Report-delivery adapter | Pinned configured mail endpoint/version only |
| `notification-egress` | Notifications-owned operational email/webhook adapters | v1-only; pinned endpoint version, verified email destination or HTTPS webhook with SEC-006 DNS/IP/redirect controls; no arbitrary Internet access |
| `update-egress` | Explicit update job | Approved release origin only; unavailable to the ordinary runtime |

In Foundation, `edge_to_web`, `web_to_api`, `control`, and `demo_source` use `internal: true`. Edge connects only to `ingress_edge` and `edge_to_web`; Web connects only to `edge_to_web` and `web_to_api`; API connects only to `web_to_api` and `control`. Exact membership is validated fail-closed: Edge and API share no network, and no unrelated service may connect to both ingress-path networks.

Edge is an infrastructure ingress adapter, not a new bounded context or an independently evolved product microservice. It reuses the immutable Web artifact, receives no secrets, writable mounts, environment overrides, business state, or user-controlled upstream, and runs a fixed Nginx configuration. This reduces the impact of possible network access but does not turn proxy configuration into a firewall.

Compose does not provide a portable ingress-only network primitive. In particular, on Docker Desktop an `internal: true` network cannot portably provide reliable host-port publication at the same time, while the non-internal `ingress_edge` network may give Edge an ambient outbound route. Foundation therefore does not describe Edge as having no egress. A fixed upstream restricts proxy routing only; the absence of secrets and business logic limits impact; the separate `edge_to_web` and `web_to_api` networks prevent direct Edge-to-API adjacency. The versioned runtime policy fixes the source Nginx configuration, the `web:8080` upstream, and allowed and denied ingress probes; the static gate rejects a dynamic resolver, an API or external upstream, and arbitrary `proxy_pass` targets. Web and API pass negative Internet probes, while the runtime gate separately checks successful `Edge → Web` access and failed `Edge → API` access.

Docker network names alone are insufficient for a production security claim. The connector allowlist includes DNS/IP validation, redirect policy, and protection of loopback, link-local, and private ranges according to deployment policy; the database-source allowlist specifies exact hosts and ports. The future connector, report-mail, operational-notification, and update egress zones in the table are target contracts, not active Foundation services. Operational email/webhook channels remain disabled in public MVP under NOTIFY-008 and AC-040. Their implementing ticket selects the bounded process/network adapter without granting Web, API, or the chart renderer ambient egress or moving Notifications state into Report Delivery.

Development topology is intentionally separate. `compose.dev.yaml` publishes
the control and demo PostgreSQL ports only to `127.0.0.1`, uses a
repository-specific Hybrid project plus separately labelled volumes, and omits
Edge from the selected service lifecycle when ingress is not under test.
Its two database bridges override `internal` to `false` because Docker Desktop
cannot reliably publish host ports from an internal network; loopback host
binding, exact service membership, and repository ownership remain mandatory.
Release validation rejects that override,
source bind mounts, reload/debug commands, mock flags, development credentials,
mutable image tags, and host-published core ports. Full Stack and Release
continue to use the canonical topology and never inherit Hybrid convenience
settings.

## 6. Separate production-hardening stage

Foundation verifies portable Compose segmentation but not strict Edge outbound denial. For every supported production target, the current bounded hardening task must produce the following evidence before production qualification; an old workstream number or accepted historical ticket does not substitute for it:

1. apply a host firewall, CNI, or equivalent target-specific policy;
2. permit host ingress only on approved addresses and ports;
3. permit Edge to reach only Web on port `8080`;
4. deny Edge direct access to API, control/data services, Internet, private, link-local, and metadata ranges;
5. preserve the required positive `Web → API` and `API → control` paths;
6. run positive browser and health probes plus negative outbound and direct-adjacency probes;
7. verify network-policy rollback separately from application-image and volume rollback.

Until that evidence is observed, production readiness for Edge egress remains unproven. The Compose static gate and runtime smoke must not make a stronger claim.

## 7. Readiness model

| Level | Question | Example evidence |
|---|---|---|
| Process liveness | Is the process alive? | container/process health |
| Dependency readiness | Are mandatory dependencies available? | PostgreSQL accepts the expected query; artifact root is writable |
| Application readiness | Are versions, configuration, and migrations compatible? | readiness endpoint with stable components |
| Business enabled | Can the user perform the capability? | permission/capability/policy and source health |

Compose `healthcheck` does not substitute for the final two levels. The UI shows the exact unavailable capability and next action rather than a generic green process status.

## 8. Storage and cleanup

The target installation ownership manifest lists created installation paths, volumes, images and digests, temporary roots, and permitted cleanup actions. The existing repository cleanup CLI has a narrower boundary: it accepts repository-local disposable paths only, as specified in tooling-gates.md. It does not prove or authorize installed-resource cleanup outside that root. A download-first installer must supply and verify its installation-owned cleanup boundary before claiming this lifecycle; the shared manifest/confirmation shape is not permission to broaden the repository tool. Cleanup:

- is dry-run by default;
- requires `--apply --ownership-manifest <path> --confirm DELETE-CUSTOMETRY-OWNED-PATHS` for deletion;
- never deletes foreign engine resources based on guessed labels or names;
- validates root normalization and symlink escape;
- prints a bounded manifest without secrets;
- verifies the post-condition and reclaimed size after execution;
- defines TTL/policy for build cache, incomplete artifacts, and benchmark data.

Install/update preflight reserves space not only for the compressed download, but also for unpacked layers, migration, artifact temporary data, and the rollback window. Reaching the normal 25 GiB ceiling blocks further uncontrolled growth and offers owner-safe cleanup.

## 9. Lessons from the previous container build

| Failure | Established rule |
|---|---|
| Colima and Docker Desktop ran simultaneously with separate 8 GiB allocations and caches | `doctor` permits exactly one selected engine/context |
| Cache and VM consumed tens of GiB | Disk/resource preflight, TTL, and ownership cleanup are mandatory |
| SBOM/license validation occurred too late | The gate runs when a dependency or image is added and repeats against the release OCI artifact |
| Mutable bases, timestamps, and build IDs made builds nondeterministic | Digest pinning, controlled build metadata, and clean-build comparison |
| A command succeeded with `No services to build` | Validate manifest, digest, platform, and runtime rather than the exit code alone |
| Lifecycle depended implicitly on local registry, cache, or profile names | Clean pull/start test without accumulated cache or a hardcoded local registry |
| An internal network broke host UI, followed by excessive egress being granted | Separate `ingress_edge`, `edge_to_web`, `web_to_api`, control, and egress; do not call Compose ingress-only; verify positive and negative paths |
| Liveness was mistaken for business readiness | Use the four status levels in section 7 |
| Incorrect self/upstream URL semantics caused a 502 | Typed configuration schema and protected-route browser smoke |
| Bootstrap ticket expired before smoke and a CLI dependency was missing | Just-in-time credentials; smoke every shipped entrypoint and dependency closure |
| UI/assets worked only from ignored local files and were absent from the CI checkout | Build releases from a fresh tracked checkout; validate generated/required asset inventory before image build |
| The CI scenario implicitly depended on a missing host utility | Locked toolchain/runner dependency closure and `doctor`; install the utility only in its owning job or image |
| Path-permission validation incorrectly rejected standard sticky `/tmp` | Platform-aware safety predicates and negative tests for world-writable paths, sticky root, and symlink escape |
| A SHA image was published before the complete release verdict | A candidate published by commit digest is not an accepted installer or release until SBOM, license, runtime, recovery, and performance gates pass |
| Shell cleanup damaged `PATH` and deleted nothing | Versioned Python cleanup, dry-run allowlist, and post-condition validation |

## 10. Release acceptance

The release installation gate on the M5 Max and selected Linux VM must observe:

- clean machine/engine-context preflight;
- download by digest without a build-cache dependency;
- platform `linux/arm64` availability;
- port-conflict handling and a persisted automatically selected port;
- loopback-only default ingress;
- no published PostgreSQL/Valkey ports;
- positive `Edge → Web` and `Web → API` probes, plus a negative direct `Edge → API` probe;
- Web/API outbound negative probes and allowlisted connector positive and negative probes;
- for v1 operational email/webhook channels, Notifications-owned endpoint-version, bounded retry and positive/negative egress evidence for both channels; verified destination/recipient evidence for email; HTTPS/signature and SSRF/redirect evidence for webhooks under NOTIFY-008 through NOTIFY-011 and TEST-INV-029; public MVP proves these channels remain disabled;
- for a production target, separate firewall/CNI-equivalent evidence that denies Edge outbound access and direct control/data adjacency;
- migration, start, browser/API/docs smoke;
- restart with preserved state;
- update rollback metadata;
- cleanup dry-run/apply against synthetic owned resources;
- disk/RAM ceiling evidence.

Until these observations exist, the documentation describes a target contract, not a proven installation.

## Accepted amendment — 2026-09-06

Version 8 records WS-001 owner decisions: M5 Max/36 GB plus Linux VM, local and explicit LAN access, Edge TLS-only credentials, guided installation and first-account policy, and no experimental-data migration obligation. Earlier M3 runtime evidence remains historical. No runtime, public release or production qualification is claimed by this amendment.

## 11. Internal delivery v1 contract (MS-001/S01)

This additive contract implements the source-level contribution of
[MS-001 1.1.0](planning/milestones/MS-001/plan.md), AC-01/04/05/06/09.
The [schema](../../deploy/compose/delivery-manifest.schema.json),
[verification policy](../../deploy/compose/delivery-verification-policy.json) and
[structural reader](../../deploy/compose/validate-delivery-manifest.py) are delivery
inputs. The policy owns finite trust/resource limits; it is not execution state.
The [S01 report](../../.codex/delivery/evidence/MS-001/MS-001-S01/report.md) binds
source inventory, protocol, provider observations and downstream obligations.
Version 9 adds this contract to version 8 without altering its target installation,
network or first-account decisions. The bound milestone plan still selects its
version 8 baseline; this compatible addition requires no active-plan rewrite.

### Record, identity and compatibility

`delivery-manifest.json` is a strict `custometry-delivery/v1` object. Every object
is closed and every declared field required. The separately versioned
`custometry-delivery-policy/v1` object is validated against the schema's
`verificationPolicy` definition. The source-level reader accepts only the exact
finite schema vocabulary present in the checked-in schema and rejects unknown
keywords/references. It loads no network schema and installs no dependencies.
Its CLI checks structure only; S02 adds record/file/Compose closure and S04 proves
archive/authenticity/runtime rejection. Structural success never permits execution.

```sh
python3 deploy/compose/validate-delivery-manifest.py delivery-manifest.json
python3 deploy/compose/validate-delivery-manifest.py --policy deploy/compose/delivery-verification-policy.json
```

The delivery SemVer identifies an immutable internal set; application version
identifies the shared API/Web application build; reader major identifies the
format. Do not reuse a delivery version for different manifest bytes. A rerun
with different content gets a new version, while comparison records retain both
run IDs/attempts. Existing build inputs remain locked. Compare the application
version against both image labels, API `/version`, and the env projection.
Do not silently substitute the delivery version for application version.

The compatibility floor is Docker API 1.43 and Compose 2.24.4 (the existing
`!reset` overlay needs a compatible Compose reader). Actual tested engine and
Compose versions are separate manifest observations, never fabricated minima.
OCI platforms are exactly `linux/amd64` and `linux/arm64`; the consumer host may
be Darwin with a Linux ARM64 engine. Both descriptor sets and actual execution
must agree. Resumed S03 selects PostgreSQL 17.11 at its source-pinned upstream
identity, retaining major 17. Frozen S01/S02 history records 17.5; this patch
selection does not qualify an installed upgrade or downgrade.
Unknown reader major/config schema/platform and mismatched application pairs fail.

### Canonical signature and complete closure

Canonical bytes are ASCII JSON, lexicographically sorted object keys, compact
`,`/`:` separators, no whitespace outside strings and no trailing newline. Arrays
retain order; producers sort inventories by path, images by platform, services
by name, and migration revisions by chain. Only booleans, null, strings and exact
integers within schema bounds are allowed; reject duplicate keys, floats, NaN,
Infinity, BOM, non-ASCII strings, controls, trailing data and excessive depth.
Require incoming manifest bytes to equal canonical reserialization before signature
validation. Hash canonical bytes with SHA-256; sign those exact bytes using Cosign
`sign-blob`, with the Sigstore bundle in `delivery-manifest.sigstore.json`.

Avoid circular identities: `files` lists every payload file but excludes the
manifest and its detached signature. Those two are the only envelope exceptions.
The signature binds the manifest, whose file hashes transitively bind payload,
notices, policy copy, configuration, verifier and evidence. The signature file is
validated cryptographically against that manifest, never trusted by its name.
The final GitHub ZIP SHA-256, artifact ID, run ID/attempt, manifest SHA-256 and
expiry are recorded in the authenticated handoff receipt **after** upload, outside
the archive; the archive cannot include its own digest or post-upload artifact ID.
No sidecar is allowed to redefine trust or grant runtime acceptance.

Each image has an approved repository, OCI index digest and two real platform
child manifest digests with compressed/unpacked sizes. Verify the index descriptor
for each child, the child's platform/config, and all downloaded content digests.
BuildKit attestation descriptors are separately identified evidence, not runnable
platform children. Never use a local config/image ID as an index or child digest.
API and migrate resolve to `images.api`; Web and Edge to `images.web`; both database
roles to `images.postgres`. The upstream selection is attested by Custometry;
Custometry does not claim authorship or an upstream signature it did not verify.

The semantic consumer must reject duplicate logical image platforms, service
names, resource IDs, revision IDs, file paths (also case-folded collisions), omitted
core/migration services, unsupported profiles, dangling references, cyclic service
or migration dependencies, and mismatched declared/configured identities. Exactly
five core/migration roles exist, with `demo-source-db` and its resources only when
the explicit optional demo component is present. Every capability names its real
services and a truthful enabled/unavailable/deferred reason. A green health endpoint
does not upgrade capability status.

File closure covers both declared files and **every archive entry**, including
metadata and ignored-looking names. Image-contained files have separate root-relative
inventory; migrations include their chain, `env.py`, `alembic.ini` and supporting
files. Build inputs bind source paths, locks, Dockerfiles, pinned bases and tool
versions; final SBOM/license/vulnerability/provenance/rebuild evidence names actual
image subjects. Evidence references also appear in the payload file inventory.

The `.release.env` adapter contains exactly `CUSTOMETRY_VERSION` (application
version), `CUSTOMETRY_API_IMAGE` and `CUSTOMETRY_WEB_IMAGE` in that order, newline
terminated, ASCII, mode 0600, with the unchanged expected GHCR origins and lowercase
index SHA-256 references. Run the existing parser and compare its values against
the manifest before rendering. Never add fields to that adapter. The structured
record, PostgreSQL reference, rendered Compose and embedded migrations must agree.
Bare env input has no bundle-verification or accepted-release meaning.

### Extraction and state safety

The independent verifier treats all downloaded files as data. It never invokes a
bundled script, imports a bundled module, evaluates env/shell syntax, renders
untrusted Compose or starts an image until authenticity and closure pass. The
verified bundle may contain a later-stage consumer, but cannot bootstrap its own
trust. C02 uses a separately selected candidate harness; accepted end-user release
eligibility remains the stronger contract in section 10.

Version 1 uses one GitHub ZIP with stored/deflated regular files only. Reject
absolute paths, drive/UNC prefixes, backslashes, percent encodings, empty or dot
segments, traversal, controls, non-ASCII names, trailing slash entries, symlinks,
hardlinks, directories, devices, FIFOs, encrypted entries, unsupported compression,
duplicate entries, case-fold collisions, overlapping local records and conflicting
central/local names or sizes. Producers omit directory entries; the verifier creates
parents itself. Never rely on `extractall`, `tar`, shell or a path-normalization
repair to make an unsafe archive acceptable.

The policy caps metadata at 1 MiB, policy at 64 KiB, JSON nesting at 32, ZIP at
128 MiB, streamed expanded payload at 512 MiB, each file at 64 MiB, entry count at
2048, ratio at 100:1, path at 240 bytes, redirects at two and network operations
at 300 seconds. These are hostile-input safety ceilings for the **small bundle**,
not a new product total-size acceptance budget. Measure image bytes separately.
Check declared and streamed bytes/ratio, CRC and SHA-256; abort on truncation or
excess even when archive headers claim smaller sizes. Never recursively unpack a
payload archive during validation. Enforce limits before and during reads.

Extract only to a new private owned quarantine directory; create files exclusively,
reject pre-existing destinations and symlinked parent components, use no-follow
opens and check containment on every operation. Discard only owned partial data
on failure. Promote atomically only after all checks; existing installation paths,
secrets, volumes and earlier verified sets remain intact. Install state and real
credentials are never bundle contents. Expiry of an artifact is unrelated to the
lifetime of a product account.

### Migrations, services and resources

The current source chain has nine revisions, ending at `0009_notifications`.
The S01 inventory binds each revision/down-revision and file SHA-256. The producer
must compare these against the **embedded** image bytes. Expected migration head,
application read head and write head agree. Initially supported starting state is
only a fresh owned PostgreSQL database. A repeat upgrade at the same declared head
must preserve state. Foreign/nonempty unknown schemas, multiple/unknown heads or
hash changes fail before application start. The one-shot command remains
`alembic -c /app/migrations/alembic.ini upgrade head` using the API image.
Migration failure leaves application readiness false and requires forward repair;
installed upgrade/downgrade/rollback and analytics artifact-format compatibility
are `not-qualified`, not inferred from a development downgrade drill.

| Role / profile | Image | Required resources and dependencies |
|---|---|---|
| `control-db` / core | PostgreSQL | `control_db_data`, password file slot, `control`, `pg_isready` |
| `migrate` / migration | API | Healthy control DB, same password slot, `control`, 32 MiB `/tmp`, Alembic/SQLAlchemy/psycopg |
| `api` / core | API | Healthy control DB, password slot, `control` + `web_to_api`, 64 MiB `/tmp`, Python app/import closure |
| `web` / core | Web | Healthy API, `edge_to_web` + `web_to_api`, 64 MiB `/tmp`, Nginx config, built UI/help/public docs/CSP/assets |
| `edge` / core | Web | Healthy Web, fixed `/etc/nginx/edge.conf`, `ingress_edge` + `edge_to_web`, 32 MiB `/tmp`, only loopback host ingress |
| `demo-source-db` / demo | PostgreSQL | `demo_source_data`, admin/reader password slots, `demo_source`, five `deploy/demo-source/init` files |

The only current checkout-relative content mount is the demo init directory; the
producer copies its five files into the bundle and renders a contained relative
mount. Secret paths become installation-owned slots, never files shipped from
`.runtime-secrets`. Volumes and networks remain per-project owned resources.
Source mounts, build directives, implicit host state, Valkey and worker additions
are forbidden in the portable candidate configuration.

Current routes compose Identity, Organization, Connections, Imports, Analytics,
People, Execution and Notifications plus health/version. Their package/plugin
imports are source-inventoried; business enablement is not established by packaging.
Bootstrap has no configured token; demo credentials/network are not mounted on API;
analytics defaults to `/var/lib/custometry/artifacts` without a writable volume;
Valkey/workers and full ingestion/analytics execution are absent. Preserve honest
unavailability and existing routes. C03/C04 and later capability providers own those
integrations; do not silently enable them or claim successful end-to-end demo data.

### Retrieval, independent trust and failure interface

Use an immutable Actions artifact in `Dejetins/custometry` from
`.github/workflows/publish-candidates.yml` on `refs/heads/main`. Name it
`custometry-delivery-<delivery-version>-<run-id>-<attempt>`, upload once with
`overwrite: false`, fail on missing files, and request 90-day retention. Record
provider-returned expiry; no permanent availability guarantee follows. A public
GitHub release attachment would allow anonymous bundle retrieval and is not the
selected mechanism. The repository remains public; this is authentication, not a
private-recipient confidentiality promise.

Download by exact artifact ID using the GitHub API, verify run/ref/source/digest,
and follow only the authenticated API's HTTPS redirect to an approved provider
host. Do not forward Authorization across hosts; do not record signed redirect
URLs. Initial credentials come from existing host keychain/`gh` integration or CI
secret injection, scoped to Actions read. Do not embed credentials in commands,
URLs, logs, files in the archive or image build args. Validate the provider's one-minute
redirect when used and reacquire for the same artifact if it expires; never switch
to a different artifact. Overall bounded failure ends without a success message.
Keep the independently verified handoff copy in an explicit consumer-owned private
location before expiry; record its same manifest and archive hashes. No new hosted
mirror or account-policy mutation is implied. After expiry/deletion, only the exact
already-verified retained copy is usable; otherwise report unavailable and obtain a
new, separately versioned delivery. No latest-tag or source-build fallback.

The policy pins the signer to
`https://github.com/Dejetins/custometry/.github/workflows/publish-candidates.yml@refs/heads/main`
and issuer `https://token.actions.githubusercontent.com`; regex identities and
transparency-log bypasses are forbidden. S03 adds signing in that workflow after
source gates, with `id-token: write`; image publication needs `packages: write`,
checkout `contents: read`, and consumer download `actions: read`. Resolve actual
workflow certificate/ref/source claims and Rekor inclusion, not merely issuer text.

Bootstrap trust is independent: obtain the reviewed policy/verifier hashes from the
accepted repository source/receipt over the administrator's existing trusted channel.
Retrieve Cosign from its official GitHub release with the policy's asset SHA-256;
check bytes before execution. Its upstream Sigstore trust bootstrap is independent
of the candidate bundle. Pin/archive the actual trusted-root/TUF metadata used in
S03 evidence, verify metadata expiry, and reject bundle-supplied trust replacements.
The policy records exact Cosign, Syft, Trivy and action pins resolved on 2026-09-08;
those are proposed producer inputs, not evidence that binaries ran. Subsequent pin
changes require compatibility and current checks before new signatures are accepted.

Use real final-image Syft CycloneDX output with the existing `gate_sbom` and
`gate_licenses`; the license policy remains fail-closed including review/unknown
findings. Trivy scans every shipped platform child, including PostgreSQL, with all
vulnerabilities reported (no ignore-unfixed/ignorefile filtering), zero unresolved
critical findings, and report plus vulnerability-database age at most 24 hours at
handoff. Record DB digest/update time and scanner version. Missing/stale/offline DB
without a qualifying retained snapshot is unavailable proof, never a clean scan.

| Code | Result / stable user message | Next action |
|---|---|---|
| `DELIVERY_VERIFIED` | Pass: selected delivery verified | Continue the explicitly authorized candidate check |
| `DELIVERY_STRUCTURE_VALID` | Pass: structure only validated | Complete independent authenticity and closure checks |
| `DELIVERY_UNAUTHORIZED` | Fail: bundle access denied | Supply a current permitted credential through the protected host mechanism |
| `DELIVERY_UNAVAILABLE` | Fail: selected artifact unavailable | Obtain the exact retained verified copy or a newly identified delivery |
| `DELIVERY_TAMPERED` | Fail: authenticity, source or content mismatch | Discard owned quarantine and obtain intact input; do not execute |
| `DELIVERY_UNSUPPORTED` | Fail: unsupported schema/platform/compatibility | Obtain a supported reader or matching delivery |
| `DELIVERY_LIMIT` | Fail: input exceeds verification limits | Obtain a compliant delivery; do not increase limits to pass |

Structural JSON/schema failures use bounded `DELIVERY_JSON_*`/`DELIVERY_SCHEMA_*`
codes. Every terminal result has `result`, `code`, `next_action` and nonzero exit
on failure (CLI code 2). No raw input, path, DSN, token, headers or provider response
is returned. Only `DELIVERY_STRUCTURE_VALID` and structural failures are implemented
by S01; later verifier codes are the fixed S02/S04 interface contract.

### Candidate packaging implementation (MS-001/S02)

Version 10 adds the bounded [candidate producer](../../tools/custometry_quality/delivery_bundle.py),
[portable template](../../deploy/compose/compose.candidate.json) and
[image file inventory](../../deploy/compose/delivery-image-inventory.json).
The [S02 report](../../.codex/delivery/evidence/MS-001/MS-001-S02/report.md) records
clean tracked-source builds, actual image checks and protected-main publication. These additions do not
change the accepted installation or release entrypoint. Stage state belongs only
to the journal, and a locally prepared candidate is not an accepted release.

The producer's `assemble` command accepts v1 metadata with exactly the derived
`files`, `services` and `resources` fields omitted. All other data, including real
image subjects/platform sizes, source/build inputs, embedded inventories, migration
chain, tested engines and evidence, must come from the actual producer run.
It never invents those observations. A separate payload directory contains the
five demo files when selected, actual evidence referenced by metadata, and notices.
The tool materializes `compose.json`, the unchanged `.release.env` projection and
the independently selected policy copy, then creates canonical manifest bytes.
`prepare` supports an already complete record; `check` validates its local closure.

The core-only configuration omits demo services, volumes, networks and secret
slots. The demo configuration retains the five init files under `demo/init` and
preserves executable mode for the two shell scripts. Secrets must be supplied
through `CUSTOMETRY_SECRETS_DIR` outside the payload. Set an explicit isolated
`COMPOSE_PROJECT_NAME`; loopback ingress and per-project network/volume ownership
are preserved. No source build, fallback image, external artifact store, new worker,
TLS/bootstrap or domain feature is added. Candidate configuration fixes the demo
dataset to `demo` and excludes the separately authorized benchmark mode.

The semantic check requires exact service/dependency/profile/role mappings, both
image platforms, pinned upstream PostgreSQL, unique inventories, the full current
migration chain and its embedded hashes, required source/asset bytes, generated Web
assets, exact env values, resource mappings, policy bytes and evidence file hashes.
It compares Compose against the independently selected template rather than
rendering arbitrary candidate configuration. The inventory is version-specific:
packaging/source changes must update it and rerun image observation. The focused
source test detects stale hashes. Generated Web asset identities come from images.

`observe-image-files` reads an existing, explicitly authorized local API/Web image
through a temporary stopped container, without a source mount or implicit pull.
It verifies the source-bound files and inventories built Web content. It removes
only its own temporary container and filesystem copy. Import/start, native platform,
signature and registry identity checks remain separate evidence.

`pack` emits a deterministic ZIP of regular files, sorted names, fixed timestamps
and preserved file modes. It consumes canonical manifest bytes, matching payload
and a separately produced signature file; it does **not** verify that signature.
The assembled directory and ZIP must be verified independently before execution.
No command here emits `DELIVERY_VERIFIED`; success is
`DELIVERY_CANDIDATE_PREPARED`, with an explicit instruction to complete authenticity
and runtime checks. `capture` requires an exact current commit and a clean tracked
set of declared build paths, then uses `git archive`; unrelated journal/evidence
edits and the preserved foreign prompt deletion do not enter that source snapshot.
Uncommitted packaging inputs fail with `DELIVERY_SOURCE_CAPTURE_REQUIRED`.

The reader uses only Python's standard library. An independently reviewed toolkit
copy needs `tools/custometry_quality/delivery_bundle.py` and these files under
`deploy/compose`: both existing manifest readers, the schema, policy, candidate
template and image inventory. A fixture test executes that copied toolkit with
isolated Python outside the checkout. It must not load a verifier from an untrusted
bundle to establish trust. Authenticated retrieval, malicious archive extraction,
signature verification and native final-subject runtime evidence retain their
S03/S04 allocations.

API packaging keeps Python sources and disables generated bytecode. Resumed S03
retains the Python 3.12.14/venv/application closure and actual ELF dependencies in
a scratch final stage. Exact distro package metadata and copyright remain available
to scanners. The container-only `psycopg[c]` extra compiles the same 3.2.9 driver;
hash-pinned Debian runtime packages supply system libpq 17.11. Local development
keeps its existing binary extra. Native repeatability/import/migration proof remains
required; S04 measures the same workload. The already unavailable Tk module remains
outside the headless closure.

Web packaging records Rollup's included module/package graph, source and metadata
hashes, and final chunk hashes. The notice collector verifies these inputs and
collects those packages' real texts, including the repository license for exact
owned workspace packages. Supply assembly binds the graph and notices to the image
filesystem and rejects missing product JavaScript chunks. Generated documentation
and other embedded assets need separate coverage evidence. Graph construction alone
does not prove license or vulnerability acceptance. Historical conservative S02
notice findings remain preserved in its report.

## 13. Internal supply producer preparation (MS-001/S03)

### S03 amendment: mandatory corresponding-source companions (target)

Decision status: selected target under the owner's 2026-09-08 necessary S03 repair
authority. The coordinator's primary-source GCC review confirms that separately
shipped libstdc++/libgcc object libraries retain GPL source-distribution obligations.
The complete matching source package is the justified delivery choice; artificial
source-tree reduction is not required. No v2 reader or companion delivery is claimed
complete by this amendment.
The [exact source selection](../../.codex/delivery/evidence/MS-001/MS-001-S03/resumed/debian-source-selection.json)
uses authenticated Debian Sources metadata and matches every represented source
version in diagnostic API6. Full source archives total 278044212 bytes after
deduplication. The GPL/LGPL/DB source-package subset currently under review totals
144216140 bytes; GCC's original source archive alone is 94299633 bytes. These are
metadata-declared exact archive sizes, not a claim that all archives were downloaded
or that the final minimum legal obligation set was approved. Component reviews must
finish that selection and retain exact build/patch inputs.

Complete upstream source-archive delivery cannot fit v1's 64 MiB file
ceiling. Increasing that ceiling or disguising split sources as recursively unpacked
payloads would break the small-bundle promise. URL-only source references and a
fabricated written offer do not establish fulfilled distribution obligations.
Introduce `custometry-delivery/v2`, reader major 2 and independently
selected `custometry-delivery-policy/v2`. Keep the main bundle's existing 128 MiB,
512 MiB expanded and 64 MiB file ceilings. Preserve v1 schema/history as a distinct
format; the v1 reader must reject a v2 manifest before execution. This is a breaking
change to v1's single-ZIP closure promise. The legacy three-key `release.env`
projection and its behavior remain unchanged. No database/application API changes
follow from the format change.

The canonical signed v2 manifest is the single source of truth for the entire set:
main payload plus every mandatory corresponding-source companion. Each companion
declares its part number, exact delivery version/run/attempt name, authenticated
Actions artifact ID, provider ZIP SHA-256/size, expiry, and every contained file's
path/SHA-256/size. The existing source/SBOM/component reviews bind which source files
fulfill which obligations. Provider IDs are learned from actual uploads; future IDs
and expiry are never guessed. Source companions contain only listed regular files,
including opaque upstream source archives; verification never recursively unpacks
or executes those archives. Producer-side substantive source inspection is separate.

Finite independent policy limits: at most 16 companions, 512 MiB per provider ZIP
and per expanded companion, 256 MiB per contained file, 4096 source entries across
the set, and 4 GiB combined expanded companion bytes. Existing path, compression,
CRC, digest, redirect, timeout, duplicate/collision and no-link restrictions apply.
These limits are separate from and cannot enlarge the main bundle limits. The
consumer must account for quarantine, promotion, retained copies and other owned
data within the existing 25 GiB budget; limits are ceilings, not permission to
allocate beyond available owned storage.

Use the same authenticated Dejetins/custometry Actions provider, workflow/ref,
signer and trust root, 90-day retention and private handoff. Target names are
`custometry-delivery-sources-<delivery-version>-<run-id>-<attempt>-<part>` with
two-digit consecutive part numbers starting at 01. No payload-supplied host,
credential, alternate provider or fallback is allowed. The independent trusted
reader first verifies the main signature and v2 policy/schema, then retrieves and
checks all required companions into a private quarantine. Missing, expired,
foreign, duplicated, truncated or altered parts fail the entire set. No success,
execution, promotion or handoff is permitted until all parts and their obligation
bindings pass. Atomic promotion covers the complete verified set, with private
directory/file permissions and retained source bytes alongside the main payload.

Publication ordering: complete local subject/obligation/source checks; publish and
retrieve-verify exact source companions; bind their observed identities in the
canonical manifest; sign and independently verify; publish and retrieve-verify the
main bundle; promote the complete private copy. A partial upload is an incomplete
set and cannot receive a delivery success claim. Reconciliation checks the entire
version across attempts; it reuses only identical existing parts with valid expiry,
never overwrites or silently extends retention, and rejects conflicting content.
After uncertain upload outcomes, reconcile provider state before retrying. A failed
main publication may leave bounded proof/source artifacts but no accepted delivery.
No existing published artifact is mutated for migration or rollback; before success,
recovery uses only task-owned quarantine cleanup and a new version when bytes change.

S03 must implement and prove schema/reader/CLI/producer agreement, old-reader rejection,
malicious/missing/expired/foreign-part rejection, complete-set immutability, real
same-provider retrieval/retention, signatures and private retained closure on both
native platforms. Synthetic tests alone do not meet that boundary. All existing S04
runtime and comparison measurements remain required. S01/S02 terminal records and
receipts remain historical evidence; this amendment does not rewrite acceptance.

The existing candidate workflow contains disabled `supply_native` and `supply_bundle`
jobs. The owner resolution authorizes their exact supply effects; both remain literal
`if: ${{ false }}` while final coverage and fail-closed repairs are incomplete.
Ordinary protected-main Git publication therefore keeps its existing
Foundation candidate effects. Prepared code is not evidence of a signed delivery.
The [S03 report](../../.codex/delivery/evidence/MS-001/MS-001-S03/report.md) records
actual proof and remaining criteria; the canonical journal owns execution state.

The [producer](../../tools/custometry_quality/delivery_supply.py) selects the original
API/Web index outputs, resolves and hashes exact native child manifests, pulls those
children, and compares each complete exported filesystem with two fresh no-cache
builds in separate pinned BuildKit instances from the same clean source archive.
Modes, owners, links and file contents are compared; only tar order, mtimes and four
Docker-generated container files are excluded explicitly. The exact uv 0.9.26
local-wheel cache timestamp and source-directory inode are normalized only after
checking their shape and the matching wheel RECORD hash/size; all other RECORD
rows, source identity and file content remain compared. Raw differences remain
in evidence. Application/dependency differences fail. Native `ubuntu-24.04` and `ubuntu-24.04-arm` jobs fail on a mismatched
host/engine architecture. These preparation checks do not replace S04 runtime proof.

Syft source metadata must identify the exact child before adding the subject property
required by existing SBOM/license gates. Trivy version, report time, DB update/expiry
and actual DB file hashes are retained. Critical or unknown-severity findings fail;
license policy is unchanged. Web notice declarations supplement cataloging, and
missing notice text fails explicitly. Scanner execution and further coverage/remediation
must be observed before enabling signing; no claim of complete minified JavaScript or
generated documentation vulnerability coverage follows from static preparation.
Cosign verifies exact canonical manifest bytes, source commit, workflow repository/ref,
exact signer/issuer and the source-pinned independent trusted root. No root supplied by
an untrusted payload establishes initial trust. The tool bootstrap downloads only S01
binary pins and the additional [supply pins](../../deploy/compose/delivery-supply-tools.json)
into a new owned CI directory; it does not provision credentials.

### Provider transport versus signed payload

The accepted S01 artifact name remains
`custometry-delivery-<delivery-version>-<run-id>-<attempt>`, as specified in section 11.
Resumed S03 assembly and record validation enforce this full name. Reconciliation
checks the same delivery version across all attempts, including the earlier short
name, and rejects duplicate, expired or changed payloads. The frozen S03 report's
attribution of the shorter name to S01 is corrected by the
[addendum](../../.codex/delivery/evidence/MS-001/MS-001-S03/decision-refinement-2026-09-08.md).
No existing artifact is renamed.

The GitHub artifact contains one opaque file named `delivery.zip`. There are three separate
identities: (1) provider archive SHA-256 from the authenticated REST artifact record,
(2) exact inner `delivery.zip` SHA-256 in the authoritative producer descriptor,
and (3) exact canonical manifest SHA-256 authenticated by Cosign. The manifest retains
the complete payload digest closure; neither the final provider ID nor an archive's
own digest is inserted recursively into the signed record.

The trusted `delivery_supply unwrap` transport adapter verifies the provider hash,
requires exactly one regular `delivery.zip` entry, rejects links, duplicates, unknown
paths, encryption and unsupported compression, and bounds both compressed and expanded
bytes by the existing 128 MiB archive limit and 100:1 ratio. It checks the independently
expected inner hash before writing a new private file. It never opens or recursively
extracts that inner archive. S04 then applies S01 signature, strict inner entry/file
closure, quarantine and atomic promotion to those exact bytes. The prohibition on
recursive **payload** archive extraction remains unchanged. A `.dockerbuild` artifact
is not an alternative bundle: real observation found native gzip bytes despite the
API endpoint suffix `/zip`; trusted content validation must not rely on that suffix.

```sh
# After S04's authenticated, bounded download to a private new transport file:
uv run --locked python -m tools.custometry_quality.delivery_supply unwrap \
  --transport "$PROVIDER_ZIP" --provider-digest "$PROVIDER_DIGEST" \
  --payload-sha256 "$EXPECTED_PAYLOAD_SHA256" --output "$NEW_PRIVATE_DELIVERY_ZIP"
# After S04's quarantine reader exposes exact manifest/signature and closed payload:
uv run --locked python -m tools.custometry_quality.delivery_supply verify \
  --record "$QUARANTINE/delivery-manifest.json" \
  --signature "$QUARANTINE/delivery-manifest.sigstore.json" \
  --trust-root "$INDEPENDENT_TRUST_ROOT" --commit "$EXPECTED_SOURCE_COMMIT"
```

These commands use the independently selected producer toolkit. The standalone,
no-checkout consumer remains S04 work; never execute a tool obtained from an unverified
payload. Provider archive bytes and inner bytes are measured separately in S04 timings.

The final upload occurs only after assembly, gates, signing and signature/closure
verification. `overwrite: false` and source-scoped workflow concurrency prevent silent
replacement. Reconciliation lists the exact global artifact name, rejects duplicates,
expired/unavailable artifacts and different inner bytes, and reuses only identical
inner bytes with a verified provider hash. A re-signed payload or changed run attempt
is different content and fails for an existing version; it is not automatically an
idempotent retry. Partial native proof artifacts have separate run/attempt/platform
names and never constitute a delivery. Do not delete an existing version to retry.

Retention is 90 days from actual provider creation, with exact `expires_at` checked
post-upload; reruns do not extend existing retention. S03 must retain a verified private
installation-owned copy through C03–C06 before acceptance. No new store, target credential,
public release, account lifetime policy or installed database change is authorized here.
