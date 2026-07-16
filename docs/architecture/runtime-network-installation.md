---
doc_id: ARCH-RUNTIME-INSTALLATION-001
title: Custometry runtime network and installation contract
doc_version: 4
product_spec_version: 0.8.2-draft
visibility: internal
ship: false
owner: devops
requirement_ids: [SCALE-004, SEC-016, SEC-017, SEC-018]
status: accepted
proof_boundary:
  label: foundation-runtime-target-contract
  exclusions: [observed-m3-installation, release-artifact, future-egress]
---

# Custometry Runtime, Network, and Installation

## 1. Goals

The default installation must be small, understandable, and reproducible: the user receives a versioned launcher and Compose configuration, while pinned images and required assets are downloaded during installation. A multi-gigabyte standalone archive containing all layers, caches, and registries is not the primary delivery method.

After a successful pull and bootstrap, the core operates without Internet access. External access is granted only to the minimum required owners:

- connector path: reads from an explicitly configured source;
- report-delivery path: uses a configured mail transport;
- update job: uses the approved release origin.

Web/API, PostgreSQL, Valkey, the chart renderer, scheduler/orchestrator, and other workers receive no arbitrary outbound Internet access. Edge is handled separately: Compose segmentation limits its adjacency, but its non-internal transport network may retain an ambient outbound route until target-specific production hardening is applied.

## 2. First target environment

- Apple Silicon MacBook Pro M3 Pro;
- one selected Docker-compatible engine;
- normal `demo` ceiling: 6 GiB of RAM and 25 GiB of repository-owned/container data;
- CPU only, using no more than container-visible cores and the administrator cap;
- other operating systems and architectures are added only after separate platform proof.

`doctor` must detect concurrently active engines and contexts, architecture, CPU/cgroup limits, memory, disk, bind-port availability, and required CLI versions. Two parallel engines with separate images and caches are a configuration error, not additional capacity.

## 3. Download-first installation

Foundation exposes three Compose profiles/contracts:

- default core: Web, API and control PostgreSQL;
- `demo`: separate demo-source PostgreSQL in addition to core;
- `migration`: one-shot Alembic job that completes before application startup.

Full Stack developer bootstrap on the M3 target:

```bash
deploy/compose/bootstrap.sh --build
deploy/compose/bootstrap.sh --build --with-demo
```

This is the clean, complete `full-stack` boundary. It is required for S05 and
CI/runtime proof, but it is not the default per-save development loop. The
accepted [development runtime contract](./development-runtime-contract.md)
defines `fast-loop`, `hybrid`, `full-stack`, and `release`, including their
proof limits.

The target Hybrid path keeps Web/API on the host and starts only required
stateful infrastructure in containers. It is not implemented yet:
`compose.dev.yaml`, the unified `scripts/dev` interface, infra-only port
publication, API hot reload, and mock/real switching remain planned
capabilities.

Release mode uses immutable GHCR references, `pull` and `--no-build`; a user installation must not silently compile the product from source. Public static `/docs` ships with the public Web surface. Authenticated operator/admin docs are excluded from that public docs image until the protected serving boundary is implemented.

The current Foundation implementation publishes only immutable SHA-scoped candidate
images after the protected `main` gate. It does not publish an accepted end-user bundle.
`bootstrap.sh --release` therefore remains a fail-closed target contract: its manifest
is parsed as strict data and must come from a future protected bundle workflow. Candidate
publication alone is not release acceptance.

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
| `update-egress` | Explicit update job | Approved release origin only; unavailable to the ordinary runtime |

In Foundation, `edge_to_web`, `web_to_api`, `control`, and `demo_source` use `internal: true`. Edge connects only to `ingress_edge` and `edge_to_web`; Web connects only to `edge_to_web` and `web_to_api`; API connects only to `web_to_api` and `control`. Exact membership is validated fail-closed: Edge and API share no network, and no unrelated service may connect to both ingress-path networks.

Edge is an infrastructure ingress adapter, not a new bounded context or an independently evolved product microservice. It reuses the immutable Web artifact, receives no secrets, writable mounts, environment overrides, business state, or user-controlled upstream, and runs a fixed Nginx configuration. This reduces the impact of possible network access but does not turn proxy configuration into a firewall.

Compose does not provide a portable ingress-only network primitive. In particular, on Docker Desktop an `internal: true` network cannot portably provide reliable host-port publication at the same time, while the non-internal `ingress_edge` network may give Edge an ambient outbound route. Foundation therefore does not describe Edge as having no egress. A fixed upstream restricts proxy routing only; the absence of secrets and business logic limits impact; the separate `edge_to_web` and `web_to_api` networks prevent direct Edge-to-API adjacency. The versioned runtime policy fixes the source Nginx configuration, the `web:8080` upstream, and allowed and denied ingress probes; the static gate rejects a dynamic resolver, an API or external upstream, and arbitrary `proxy_pass` targets. Web and API pass negative Internet probes, while the runtime gate separately checks successful `Edge → Web` access and failed `Edge → API` access.

Docker network names alone are insufficient for a production security claim. The connector allowlist includes DNS/IP validation, redirect policy, and protection of loopback, link-local, and private ranges according to deployment policy; the database-source allowlist specifies exact hosts and ports. The future connector, mail, and update egress zones in the table are target contracts, not active Foundation services.

Development topology is intentionally separate. A future
`compose.dev.yaml` may publish required infrastructure ports only to
`127.0.0.1`, use development-owned project names and volumes, and omit Edge
when ingress is not under test. Release validation must reject that override,
source bind mounts, reload/debug commands, mock flags, development credentials,
mutable image tags, and host-published core ports. Full Stack and Release
continue to use the canonical topology and never inherit Hybrid convenience
settings.

## 6. Separate production-hardening stage

Foundation verifies portable Compose segmentation but not strict Edge outbound denial. For every supported production target, Workstream 12, `Hardening`, must:

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

The ownership manifest lists created installation paths, volumes, images and digests, temporary roots, and permitted cleanup actions. Cleanup:

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

The release installation gate on the M3 Pro must observe:

- clean machine/engine-context preflight;
- download by digest without a build-cache dependency;
- platform `linux/arm64` availability;
- port-conflict handling and a persisted automatically selected port;
- loopback-only default ingress;
- no published PostgreSQL/Valkey ports;
- positive `Edge → Web` and `Web → API` probes, plus a negative direct `Edge → API` probe;
- Web/API outbound negative probes and allowlisted connector positive and negative probes;
- for a production target, separate firewall/CNI-equivalent evidence that denies Edge outbound access and direct control/data adjacency;
- migration, start, browser/API/docs smoke;
- restart with preserved state;
- update rollback metadata;
- cleanup dry-run/apply against synthetic owned resources;
- disk/RAM ceiling evidence.

Until these observations exist, the documentation describes a target contract, not a proven installation.
