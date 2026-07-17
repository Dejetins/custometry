---
doc_id: ARCH-SYSTEM-DESIGN-001
title: Custometry Foundation System Design
doc_version: 3
product_spec_version: 0.8.2-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: [ARCH-PRINCIPLE-001, DOC-RULE-008, HELP-001, SCALE-004, SEC-016, SEC-017, SEC-018]
status: accepted
proof_boundary:
  label: accepted-foundation-target-design
  exclusions: [runtime-readiness, release-readiness, product-vertical-slice]
---

# Custometry — Foundation System Design

## Document status

- decision: accepted for repository foundation work;
- product source: `custometry-technical-blueprint-ru.md`, `0.8.2-draft`;
- target form: modular monolith, single-server Docker Compose through `v1_target`;
- first target: local Apple Silicon MacBook Pro M3 Pro;
- boundary: shared architecture and acceptance rules, without a standing delivery plan or ticket backlog;
- companion DOCX: `custometry-foundation-system-design.docx` is a visually verified snapshot of this decision; Markdown remains the only mutable execution/source artifact.

The DOCX is regenerated from this Markdown through artifact template package
`openai-templates@0.1.0`, resource `artifact-template-system-design/assets/reference.docx`
with SHA-256 `13504f6c221a42c1726460a9e865e563355539ff97d702d6c9b2267b4b261d76`.
The reference template is not vendored in the public repository. Before handoff,
the hash, OOXML package diff, fields and links, and every rendered page are verified.
Manually editing the DOCX without synchronizing this Markdown is prohibited.

## 1. Objective and non-goals

Custometry must provide a tangible Web experience early, then progressively replace contract adapters with real domain and infrastructure implementations. Every increment must be an observable end-to-end slice, not a collection of disconnected screens or technical layers.

Foundation establishes:

- a reproducible public monorepo and protected delivery process;
- an explicit DDD map and dependency rules;
- shared docs-as-code and quality contracts;
- a compact download-first installation;
- a local control PostgreSQL and a separate synthetic retail source;
- a minimal shared Web shell, route registry, and contract-generated mocks as the basis for future vertical slices.

Foundation does not claim that product APIs, analytics, forecasting, report
delivery, universal XLSX, or production deployment are complete. Future work
uses the smallest justified delivery artifact under Global Delivery Contract
v1.

## 2. Accepted decisions

| Area | Decision |
|---|---|
| Repository | Permanently public; no secrets, customer data, or private topology |
| Git | Protected `main`, mandatory pull requests and required checks, squash merge, linear history, no `develop` branch |
| First platform | MacBook Pro M3 Pro / Apple Silicon; other targets are added only after local proof |
| Runtime | Web/API/data core has no arbitrary outbound access; Edge is a separate infrastructure ingress adapter with limited adjacency but may retain ambient transport egress until production hardening |
| Installation | A small launcher/configuration downloads pinned images and assets, verifies digests, and starts the system; a very large self-contained bundle is not the default |
| Documentation | Local user/install documentation; operator/admin documentation requires authorization; architecture, ADRs, prompts, and iteration evidence are not included in the ordinary installation |
| Documentation UI | MkDocs Material provides versioned `/docs`; permission-aware in-app `/help` uses the shared generated index |
| Development data | Retail/e-commerce: stores, channels, customers, products, receipts/items, returns, promotions, and calendar |
| Resource budget | Normal demo: no more than 6 GiB RAM and 25 GiB of owned disk; benchmark profile is opt-in |
| UI delivery | Contract-backed Experience Platform followed by real vertical slices; mocks are generated from the same versioned contracts |

## 3. Architectural form

### 3.1. Dependency direction

```text
browser / CLI / scheduler / worker entrypoint
                    │
                    ▼
           inbound adapter / app
                    │
                    ▼
          application use cases
                    │
                    ▼
             domain model
                    │ owns outbound ports
                    ▼
       infrastructure adapter implementation
```

`apps/*` are composition roots. `packages/*` own domain/application code and the ports they require. Infrastructure adapters implement those ports and are wired only at a composition root. Domain/application code does not import FastAPI, Celery, a SQL driver, a filesystem implementation, or another context's private tables.

Contexts physically share one PostgreSQL instance but logically own their tables and write paths. Cross-context access occurs through an application contract, public projection, or versioned event/DTO. The shared kernel remains narrow: identifiers, locale-neutral primitive contracts, the error envelope, and trace metadata, but no business logic.

### 3.2. Bounded contexts

The target map contains fifteen contexts: Identity & Workspace, Connection Catalog, Semantic Model, Data Documentation, Ingestion, Artifact Lifecycle, Execution Control, Data Quality, Analytics, Promotion Journal, Forecasting, Presentation & Reports, Report Delivery, Notifications, and Audit. The complete ownership/dependency matrix is documented in [bounded-context-map.md](./bounded-context-map.md).

### 3.3. Runtime components

The Foundation runtime is intentionally smaller than the full target topology. The default core contains Edge, Web, API, and control PostgreSQL; the `demo` profile adds a separate demo-source PostgreSQL; the `migration` profile runs one-shot Alembic. Edge is a secretless, read-only infrastructure ingress adapter, not a bounded context or a new product microservice. It owns a persisted dynamically allocated loopback-only port and uses a fixed upstream that proxies only to Web. `edge_to_web` connects only Edge and Web, while `web_to_api` connects only Web and API, so Edge and API have no direct network adjacency. Valkey, execution processes, and workers are introduced by the corresponding vertical slice rather than being declared as implemented empty services.

Compose does not provide a portable ingress-only network primitive on Docker Desktop: publishing a host port requires a non-internal Edge transport network, which may provide an ambient outbound route. A fixed upstream constrains proxy routing but is not a firewall. Foundation therefore proves segmentation and negative egress for Web/API, but does not describe Edge as entirely without egress. The strict Edge policy belongs to the separate Workstream 12 `Hardening` and requires target-specific host firewall or CNI-equivalent enforcement with positive and negative runtime evidence.

Target topology through `v1_target`:

```text
user browser
    │ loopback by default; LAN only by explicit policy
    ▼
Edge infrastructure adapter
    │ edge_to_web: Edge + Web only
    ▼
Web
    │ web_to_api: Web + API only
    ▼
API
    │
                    internal control network
    │
        postgres · valkey · scheduler · orchestrator
        outbox-dispatcher · reconciler · workers
    │
                    local immutable artifacts

worker-data ── allowlisted connector egress ── external source only
worker-report ── allowlisted mail egress ── configured mail transport only
update job ── allowlisted update egress ── approved release origin only
```

Future egress lines are target boundaries, not active Foundation services.

PostgreSQL is the source of truth for the control plane and run state. Valkey delivers tasks and stores ephemeral cache/locks but does not determine final state. Bulk results are stored as immutable local artifacts with a manifest, hash, and lineage. Web and Guided/Pipeline flows use one execution engine.

## 4. Primary data flows

### 4.1. Contract-backed UI

1. The route registry, DTO/OpenAPI/JSON Schema, and UI state contract are versioned.
2. The mock adapter is generated from the same examples and schemas.
3. The browser flow runs against the mock boundary without a separate "mock product model."
4. Domain/application code and real adapters implement the same contract.
5. The contract parity gate compares the mock, generated client, and real API.
6. Acceptance requires real browser/API/PostgreSQL or artifact proof appropriate to the slice.

### 4.2. Job execution

1. In one PostgreSQL transaction, the API persists the command/run and outbox intent.
2. The outbox dispatcher delivers a versioned task with an idempotency identity.
3. The worker obtains a lease/fencing token, writes a staging artifact, and regularly reports progress and ETA.
4. The immutable artifact becomes visible only after an atomic manifest commit.
5. The worker persists terminal state; the reconciler repairs lost delivery, expired leases, and aggregate state.
6. The UI reads authoritatively persisted state and preserves the previous result during a safe refresh.

### 4.3. Local test data

Control PostgreSQL and demo-source PostgreSQL are separate services and trust boundaries. The generator accepts `profile`, `seed`, `schema_version`, and scenario flags, creates a manifest with expected counts/KPI/hash, and never requires committing a large dump.

Profiles:

- `smoke` — minimal deterministic fixtures for CI;
- `demo` — a human-readable retail dataset within the 6 GiB/25 GiB budget;
- `benchmark` — an opt-in corpus with a separate resource preflight.

The dataset covers returns, missing products, duplicates, SCD, late arrival/corrections, multiple currencies, promotions, leap day/week 53, incomplete periods, and PII classes.

### 4.4. Boundary contracts

| Boundary | Contract rule |
|---|---|
| Browser → API | OpenAPI with stable errors/scopes; generated TypeScript client; bounded pagination/sort/filter allowlists |
| Long operation | `202 Accepted` + operation/run ID + status URL; no HTTP wait for compute result |
| Draft mutation | ETag/`If-Match`; stale edit returns current revision conflict |
| Repeatable side effect | Workspace/actor/route-scoped `Idempotency-Key` + payload hash |
| Execution delivery | Versioned task/event, at-least-once, attempt identity, lease/fencing and reconciliation |
| Bulk result | Immutable artifact manifest/hash/schema/grain/key/lineage/PII; bounded internal JSON only |
| Visualization | Product-owned validated `ChartSpec`; ECharts compiler adapter; raw options/code/network assets rejected |
| Report | Immutable `ReportSnapshot` pins result/data/ChartSpec/theme/locale/timezone/Data Guide identities |
| External source/mail/update | Explicit adapter, allowlist, secret reference, timeout/retry classes and unknown-state rule |

Schemas are owned by the provider context, versioned before consumers, and accompanied by positive, negative, and limit examples. An API DTO, domain object, and persistence row are not treated as one universal type.

## 5. UI-first delivery slices

Delivery starts from the smallest coherent user journey and follows accepted
bounded-context dependencies. The Web route, complete UI states, accessibility,
and mock/real disclosure are designed with the versioned contract. Domain,
application, adapter, and real-boundary work then complete the same vertical
outcome. The repository does not maintain a fixed block sequence: the next
slice is selected from current product priority, accepted dependencies, and the
nearest provable boundary.

One ready ticket is one execution unit. A specification precedes tickets only
when behavior, invariants, failure semantics, or the proof seam are unresolved.
Acceptance requires the ticket's declared contract, UI, real-boundary,
documentation, compatibility, and rollback evidence; it does not depend on a
fixed stage taxonomy.

## 7. Reliability, security, and operations

- Every external side effect has a destination, authority, idempotency key, retry classes, timeout, unknown-state reconciliation, and audit trail.
- Process liveness, dependency readiness, application readiness, and business-enabled status are distinct signals.
- A Compose health check proves only its declared startup/liveness boundary.
- Secrets are supplied only through secret files/references and never enter the public repository, URLs, logs, or generated examples.
- Web/API/data core services have no arbitrary outbound Internet access. The chart renderer operates without network access. In Compose, Edge has only ingress plus Web adjacency, while strict outbound denial for Edge is proven later by a target-specific firewall/CNI policy.
- PII classification and redaction are applied before pagination, previews, exports, logs, and samples.
- Backup/restore, migration lifecycle, browser flow, supply chain, and performance have separate release gates.

## 8. Documentation contract

Markdown in Git is the authoring source for platform documentation. Foundation fails closed and publishes only `docs-site/docs/**`; contributor `docs/**` and its index are not automatically included in the image. The target visibility builder publishes allowlisted classes, MkDocs Material serves local `/docs`, and the application builds `/help` from the same permission-aware search index and adds permitted Data Guides. See [documentation-platform.md](./documentation-platform.md) for details.

Repository-authored engineering documentation is written in English by default. The normative `*-ru.md` product specifications and declared localized product content under `docs-site/docs/<locale>/**` are explicit exceptions. Unless the user requests another language for the current task, only the final user-facing completion report defaults to Russian; durable repository artifacts and handoffs remain English.

## 9. Contract impact

| Surface | Classification | Rationale |
|---|---|---|
| Foundation public API | `compatible-change` | Added `/health/live`, `/health/ready`, `/version`, OpenAPI, an external JSON Schema, and a generated TypeScript client; the product API is not yet implemented |
| Foundation persistence | `compatible-change` | Added the initial Alembic revision `platform_metadata`; domain tables and product state are absent |
| Repository/process defaults | `compatible-change` | Added Foundation policies before the first implementation consumer |
| Browser contract | `compatible-change` | Added the Frost shell, canonical route registry, planned states, en/ru, `/help`, and local documentation without claiming that product surfaces are complete |
| Deployment/network | `breaking-change` | Runtime-policy schema v2 and network names/membership change atomically: `edge_to_web` and `web_to_api` replace the shared `application` network; the public host URL/API/persistence do not change, but old and new Compose/policy/validator versions cannot be mixed |
| Documentation visibility | `compatible-change` | A public-only MkDocs source and generated Help index exist; authenticated serving remains a future security boundary |

After the first consumer exists, changes to route, port precedence, module ownership, schema, generated-client contract, or visibility class require a separate compatibility/migration assessment.

## 10. Proof boundaries and risks

This document proves only the accepted direction. Separate observable gates are required for:

- a GitHub-hosted CI run for the published change;
- a clean release installation/start on the M3 Pro from published digest-pinned images;
- recovery and performance evidence;
- legal resolution of license findings and a final accepted installer manifest;
- documentation authorization and offline navigation;
- target-specific Edge outbound denial through firewall/CNI controls and shared egress-allowlist enforcement;
- multi-target build reproducibility beyond the locally verified Foundation boundary.

The primary risk is mistaking a static scaffold or contract-generated mock for a complete product. Mandatory real-boundary acceptance for every vertical slice mitigates this risk.

## 11. Considered trade-offs

| Decision | Benefit | Cost/constraint |
|---|---|---|
| Modular monolith instead of microservices | Simple transactions, one deployment, fast domain evolution | Requires automated enforcement of module boundaries |
| UI-first contract-backed slices | An early tangible product and validated workflows | Contracts, examples, and generated clients are required before backend implementation |
| One control PostgreSQL | Clear durability and coordination truth | Logical ownership cannot be automatically enforced by separate databases |
| Local artifacts through v1 | Simple single-host reproducibility | Remote workers/object storage remain impossible without a future ADR |
| Download-first images | Small installer, layer reuse, and digest-based updates | First start requires Internet access or a separate air-gap export |
| Segmented Edge→Web→API plus non-internal Edge transport | No direct Edge→API adjacency; portable loopback publishing; Web/API retain negative egress | Compose does not prove ingress-only networking or Edge outbound denial; a fixed upstream is not a firewall; production requires target host/CNI hardening |
| Physical public-document source split | Fails closed: internal content cannot be packaged accidentally | Temporarily maintains two documentation areas; requires a future metadata builder without content duplication |
| M3 Pro first | Fast proof on a real target | Multi-architecture and other-OS readiness remain unverified |
