---
doc_id: ARCH-DEVELOPMENT-RUNTIME-001
title: Custometry development runtime contract
doc_version: 4
product_spec_version: 0.9.0-draft
visibility: internal
ship: false
owner: engineering
requirement_ids: [ARCH-PRINCIPLE-001, DOC-RULE-008]
status: accepted
proof_boundary:
  label: accepted-development-runtime-policy-and-hybrid-interface
  exclusions: [full-stack-runtime-acceptance, browser-product-runtime, release-readiness, production-hardening]
---

# Custometry Development Runtime Contract

## 1. Objective and non-goals

Custometry uses the smallest runtime that can prove the boundary under change.
Ordinary source edits must not rebuild or restart the entire container stack,
but lower-cost feedback must never be presented as Compose, release, or
production evidence.

This contract defines four canonical modes:

1. `fast-loop`;
2. `hybrid`;
3. `full-stack`;
4. `release`.

The Hybrid launcher and development Compose override are implemented by W11.
Generated mocks, browser-visible mock/real disclosure, complete Full Stack
acceptance, and a release bundle remain separately owned outcomes.

## 2. Current-state fact ledger

| Type | Current fact | Repository evidence | Consequence |
|---|---|---|---|
| Fact | The Web can run on the host through Vite on `127.0.0.1:5173`. | `apps/web/package.json`, `apps/web/vite.config.ts` | Part of `fast-loop` exists. |
| Fact | Python tools, tests, and the API package run through the pinned uv workspace. | `pyproject.toml`, `apps/api/pyproject.toml`, toolchain scripts | Host-side domain/application work is supported, but no canonical API reload command exists. |
| Fact | The repository has one full Foundation Compose topology and a build-capable bootstrap. | `compose.yaml`, `deploy/compose/bootstrap.sh` | `full-stack` exists for Foundation proof; it is not the default edit loop. |
| Fact | CI can exercise disposable migration, Compose, and browser boundaries. | `.github/workflows/ci.yml`, quality-tool profiles | Clean-stack evidence is available without making every local edit container-first. |
| Fact | Immutable SHA-scoped candidate images and a fail-closed release launcher contract exist. | `.github/workflows/publish-candidates.yml`, `deploy/compose/compose.release.yaml` | This is not an accepted end-user release bundle. |
| Fact | `compose.dev.yaml` and `scripts/dev up --mode hybrid` provide infra-only startup, host API/Web processes, status, bounded logs, safe demo reset, and owned cleanup. | W11 implementation and terminal evidence | Hybrid claims require the observed W11 lifecycle; generated mocks and browser-visible mock/real disclosure remain separate Experience work. |

## 3. Canonical modes

| Mode | Runs on host | Runs in containers | Primary use | Evidence it may support | Evidence it cannot claim |
|---|---|---|---|---|---|
| `fast-loop` | Web, framework-independent Python, focused tests; later API reload when implemented | none required | UI/component work, domain/application logic, contracts, generated mocks | lint, types, unit/property/component tests, contract/mock parity, local Web behavior | PostgreSQL adapters, container networking, clean installation, restart/recovery, release |
| `hybrid` | Web and API with reload | stateful infrastructure such as control PostgreSQL and demo-source PostgreSQL; later Valkey or other owned infrastructure | real adapters and end-to-end development without rebuilding application images | API/database integration, migrations against local disposable state, browser-to-real-API flows | production image behavior, Edge segmentation, clean full-stack lifecycle, release |
| `full-stack` | only controlling tools and browser | the complete supported disposable application topology | ticketed runtime proof, pre-push/CI runtime checks, ingress/network behavior, restart and clean lifecycle | Compose health, Edge/Web/API paths, migrations, browser smoke, restart and cleanup | immutable release publication, supply chain, target firewall/CNI, accepted installer |
| `release` | launcher, verification tools, and browser only | immutable digest-pinned release composition | protected release/install/update acceptance | digest/platform, migration, install/update/rollback, recovery, SBOM/provenance/license, target security and performance | development convenience behavior or mutable source/build state |

The mode is a proof boundary, not a quality rank. A focused domain test in
`fast-loop` can be the correct nearest evidence for an invariant. It becomes
insufficient only when the changed behavior crosses a database, browser,
container, network, recovery, performance, or delivery boundary.

## 4. Selection and escalation

Use this decision order:

1. Start with `fast-loop` when the changed outcome can be proved without real
   stateful infrastructure.
2. Escalate to `hybrid` when a real database, migration, queue, source adapter,
   or browser-to-real-API path is part of the claim.
3. Escalate to `full-stack` when container image behavior, Edge routing,
   service discovery, health/readiness, restart, cleanup, or clean-machine
   reproducibility is part of the claim.
4. Escalate to `release` only when a milestone or change requires immutable
   artifact, install/update, recovery, supply-chain, target-security, or
   performance evidence.

Failures never fall back silently to a cheaper mode. For example, a failed
Hybrid database check cannot be replaced by a repository fake, and a failed
Full Stack network probe cannot be replaced by Vite behavior.

## 5. Ticket proof-mode selection

Each ready ticket declares the smallest mode that can observe its proof
boundary. Pure policies, schemas, components, and generated clients normally
use `fast-loop`; real stateful adapters and browser-to-real-API paths require
`hybrid`; container image, Edge routing, service discovery, restart, and clean
lifecycle claims require `full-stack`; immutable candidate, install/update,
recovery, supply-chain, target-security, and performance claims require
`release`. A failed higher mode cannot be replaced by evidence from a cheaper
mode.

## 6. Hybrid topology

The accepted developer path is:

```text
Browser
  -> host Vite on 127.0.0.1:5173
  -> host API on 127.0.0.1:8000
  -> containerized stateful infrastructure through loopback-only development ports
```

Rules:

- application source is mounted or executed on the host; application images
  are not rebuilt on every save;
- only infrastructure required by the current slice starts;
- every development-published port binds to `127.0.0.1` by default;
- control and demo-source PostgreSQL remain separate databases and ownership
  boundaries;
- the Hybrid topology uses a separate project identity and does not attach to
  release volumes;
- developer secrets live only in ignored, runtime-owned local files and
  are never embedded in Compose, logs, prompts, or generated mocks;
- Edge is omitted unless ingress behavior is the subject of the check;
- a browser-visible development indicator must disclose generated-mock versus
  real-API mode without becoming an authorization mechanism.

## 7. Developer interface

W11 establishes the canonical Hybrid orchestration interface:

```text
scripts/dev up --mode hybrid
scripts/dev down
scripts/dev status
scripts/dev logs [service]
scripts/dev reset-demo --confirm RESET-DEMO
scripts/dev validate
```

The exact process manager may evolve, but these Hybrid semantics are stable:

- `up` is idempotent and reports actual URLs, processes, containers, and mode;
- `down` stops only resources owned by the current development identity;
- `status` distinguishes healthy, ready, degraded, and unavailable;
- `logs` redacts secrets and has bounded output;
- `reset-demo` affects only repository-owned demo data, is dry-run or
  confirmation-gated, and cannot target control or foreign databases.

Direct `pnpm` and `uv` commands remain valid Fast Loop tools. The existing
`deploy/compose/bootstrap.sh --build [--with-demo]` remains the canonical Full
Stack launcher. Adding those modes to `scripts/dev` requires a later ticket and
must not blur their different proof boundaries.

## 8. Compose development override and release isolation

`compose.dev.yaml` is an explicit development override, not a
second product topology. It may publish loopback-only infrastructure ports,
enable development-only health aids, and select infra-only profiles. It must
not weaken the canonical `compose.yaml` or `compose.release.yaml`.

The shared quality profiles run the development-runtime validator. Release
entrypoints must not reference the override, and validation fails when a
release path acquires a development override reference. Release composition
must also reject any of the following:

- `compose.dev.yaml` or a development-only profile;
- source bind mounts, hot-reload commands, debug servers, or mutable image
  tags;
- generated-mock flags or development banners;
- development credentials or repository-relative secret defaults;
- host-published PostgreSQL, Valkey, API, or Web ports outside the accepted
  release ingress contract;
- reuse of development project names, networks, or volumes.

Production firewall/CNI proof remains a separate B12 responsibility. A clean
Full Stack Compose check does not establish that proof.

## 9. Ownership

| Owner | Runtime responsibility |
|---|---|
| `W00 Repository Foundation` / engineering productivity | pinned host toolchain, common runner conventions, initial quality profiles |
| `B01 Experience Platform` | Fast Loop Web experience, generated contract mocks, mock/real disclosure, browser integration |
| `B02 Local Data Lab` | infra-only control/demo PostgreSQL lifecycle, deterministic fixtures, safe demo reset |
| `B03 Identity and Control Plane` | canonical host API development boundary, sessions/RBAC behavior, control-plane configuration |
| `B04 Execution, Compute and Artifact Spine` | local execution workers, progress/ETA, leases, artifacts, and their development composition |
| `B05`–`B13` | real adapters and runtime needs owned by each bounded context |
| DevOps/runtime ownership | `scripts/dev`, Compose override mechanics, project/resource isolation, lifecycle diagnostics |
| QA/evidence ownership | independent real-boundary proof and evidence retention |
| Production hardening owner | release isolation, target firewall/CNI, recovery, performance, and supply-chain gates |
| Release acceptance owner | final immutable release evidence without adding feature scope |

## 10. Contract impact and migration

| Surface | Classification | Migration and rollback |
|---|---|---|
| Public API, DTOs, persisted product data | `none` | No product contract changes. |
| Contributor runtime selection | `compatible-change` | The modes name existing and target paths; current focused commands remain usable. |
| `scripts/dev` Hybrid interface | `compatible-change` | Introduced additively; direct focused and Full Stack commands remain available. Removing or changing stable command semantics later requires migration. |
| `compose.dev.yaml` | `compatible-change` | Explicit development override; deletion rolls back to Fast Loop and Full Stack paths after owned Hybrid resources are stopped. |
| Ticket proof-mode declarations | `compatible-change` | Existing focused commands remain valid; each new ticket names the required mode and proof boundary. |
| Release composition/security | `none` now; fail-closed compatibility requirement for implementation | Development topology must remain unreachable from release workflows. |
| Browser-visible development disclosure | `compatible-change` | Visible only in development builds; production validation rejects it. |

## 11. Validation and proof boundary

Documentation acceptance requires metadata, links, documentation index, and a
cold self-review proportional to the change. W11 implementation acceptance
requires:

- focused tests for mode selection and resource ownership;
- real infra-only PostgreSQL startup, migration, reset, and cleanup evidence;
- real host Web/API ownership and reload-capable process behavior;
- negative validation showing development overrides cannot enter release;
- static confirmation that the canonical Full Stack and release entrypoints do
  not load the Hybrid override; real Full Stack lifecycle remains a separate
  proof boundary;
- unchanged release fail-closed behavior.

This document and source tree define the accepted interface. Only W11 terminal
evidence proves the observed Hybrid lifecycle. Generated mocks, browser-visible
mock/real disclosure, complete Full Stack acceptance, and an accepted release
bundle remain outside this proof boundary.

## 12. Residual risks

| Risk | Owner | Mitigation/review trigger |
|---|---|---|
| Host and container behavior diverge. | DevOps + owning ticket | Require Full Stack proof whenever image/runtime behavior changes. |
| Generated mocks drift from real contracts. | Experience + contract owner | Generate both from one versioned source and verify parity before real integration. |
| Development ports or secrets leak into release. | Production hardening owner | Keep the development-runtime release-entrypoint exclusion in every quality profile and retain separate release runtime evidence. |
| A single CLI becomes opaque or destructive. | DevOps | Print owned resources and actual commands; scope cleanup; confirmation-gate data reset. |
| Developers overuse Full Stack and lose feedback speed. | Engineering productivity | Keep focused host commands first-class and measure startup/reload time when the CLI is implemented. |


## 11. Prepared retail report source and analyst (MS-003/S01)

S01 adds an explicit local preparation command after Hybrid reports healthy:

```sh
source scripts/activate-toolchain.sh
scripts/dev up --mode hybrid
uv run --locked python -m apps.worker_data.prepare_retail_report
```

Hybrid creates a mode-0700 artifact root inside its owned runtime directory and
passes it to API readiness and analytics. It supplies the loopback source endpoint
and reader secret file. The explicit loopback-only developer configuration uses
`identity_cookie_secure=false`; packaged HTTPS retains Secure cookies. These
settings do not alter the release topology or its storage readiness requirement.

Preparation checks the owned database containers, locks its own state, and uses
production Identity bootstrap/invitation/acceptance and Connection Catalog services.
It creates a setup owner and a separate ordinary analyst in one workspace. Runtime
credentials live in mode-0600 `secrets/retail-report.json` inside the protected
runtime directory; never copy its contents to a report, journal, command line or
browser storage. `retail-report-output.json` contains safe IDs, immutable artifact
references and the exact semantic/calendar/store/quality projection. The command
prints only safe identifiers and navigation instructions. It never inserts fake
Identity, DQ or semantic records.

Repeat preparation verifies the same owner/analyst and source fingerprint, returns
the committed IDs, and rechecks artifact hashes. A changed identity/profile/source,
unsafe state file, unavailable artifact or conflicting partial setup fails explicitly;
it never resets the database or adopts another workspace. Source fingerprinting is
rechecked within the actual extraction snapshot. Interrupted setup before a durable
identity binding may require explicit reconciliation rather than guessing ownership.

Browser traffic uses the existing same-origin Vite `/api` proxy. Identity's shared
HTTP adapter preserves bearer authentication and applies Origin plus CSRF to cookie
mutations; safe reads need the authenticated session. Access and CSRF cookie paths
are `/`; refresh is `/api/identity`. Login/logout clear legacy `/identity` and current
paths. Existing direct-path browser fixtures must use the prefix; bearer clients
retain their routes. Old browser sessions may require login again. Secure remains
enabled in HTTPS settings; S01 HTTP evidence is not installed HTTPS acceptance.

The six-table profile and limitations are documented in the
[source adaptation contract](../contracts/source-data-adaptation-contract.md#ms-003s01-bounded-implementation).
Actual run IDs, counts and proof are linked from the
[S01 report](../../.codex/delivery/evidence/MS-003/MS-003-S01/report.md).
Use a separate disposable database for existing integration suites: their fixtures
truncate tables. Never point those suites at the prepared workspace database.
