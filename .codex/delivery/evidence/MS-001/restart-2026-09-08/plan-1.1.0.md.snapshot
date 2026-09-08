---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "milestone",
  "doc_id": "MS-001",
  "title": "Reproducible versioned prebuilt delivery",
  "version": "1.1.0",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "WS-001",
    "path": "docs/architecture/planning/directions/DIR-006/workstreams/WS-001.md",
    "version": "1.0.3"
  },
  "direction_ref": "DIR-006",
  "baseline_ref": {
    "commit": "f9f39a75994d2f7a8e8d7a75df293c35579f842d",
    "evidence_refs": [
      "docs/architecture/planning/milestones/MS-001/plan.md#current-state-evidence"
    ]
  },
  "requirement_refs": [
    {
      "source": "custometry-technical-blueprint-ru.md",
      "revision": "sha256:183d9d2f2070cb8e651eca46fa44244b0d0af2a914830bcee6e5716ae15fd163",
      "ids": [
        "SEC-009",
        "SEC-012",
        "SEC-016",
        "SEC-017",
        "SEC-018",
        "OPS-001",
        "OPS-002",
        "SCALE-003",
        "SCALE-004",
        "WEB-PERF-001",
        "WEB-PERF-002",
        "WEB-PERF-003",
        "WEB-PERF-004",
        "WEB-PERF-005",
        "WEB-PERF-006"
      ]
    }
  ],
  "decision_refs": [
    "FRAME/DEC-03",
    "FRAME/DEC-06",
    "WS-001/DEC-02",
    "WS-001/DEC-04",
    "WS-001/DEC-08",
    "WS-001/DEC-10",
    "MS-001/DEC-01",
    "MS-001/DEC-02",
    "MS-001/DEC-03",
    "MS-001/DEC-04",
    "MS-001/DEC-05",
    "MS-001/DEC-06",
    "MS-001/DEC-07",
    "MS-001/DEC-08",
    "MS-001/DEC-09"
  ],
  "supersedes_ref": null,
  "execution_ref": {
    "path": ".codex/delivery/ledgers/MS-001.md",
    "schema_version": "prompt-pack-ledger/v1"
  },
  "proof_boundary": {
    "label": "accepted-milestone-intent-and-authored-prompt-pack",
    "exclusions": [
      "execution-readiness",
      "implemented-stage",
      "verified-delivery-artifact",
      "installation-readiness",
      "product-release"
    ]
  }
}
---

# MS-001. Reproducible versioned prebuilt delivery

**L3 plan 1.1.0, 2026-09-07; accepted intent, implementation not started.** Parent: [WS-001](../../directions/DIR-006/workstreams/WS-001.md) `1.0.3`, outcome **WS-001/C02**; direction: [DIR-006](../../directions/DIR-006/direction.md) `1.2.0`. This is the first development milestone. C01 inventory remains L2 preparation, not a separate milestone.

The user selected the supply and platform decisions, accepted the core/optional-demo contents and five-stage sequence, requested the complete plan and prompt pack, reserved execution organization, and required measurable interface/performance evidence with comparison references. Version 1.1.0 retains that accepted intent and completes the user-requested execution preparation. On 2026-09-07 the user explicitly requested an official working plan, a ready prompt pack, commit and publication to main through a temporary technical branch, followed by branch deletion. This authorizes the required local updater and repository publication; product stage execution, delivery-artifact publication and runtime deployment are not part of this preparation. No task assignees, agent roles or organization approval gate are encoded.

## 1. Result and boundaries

| Item | Definition |
|---|---|
| Before / after | Separate image candidates and a checkout-dependent release path become one identified internal delivery set that a clean consumer can retrieve, authenticate, validate and run for bounded artifact checks without building product source. C03 consumes this set to implement installation. |
| Included | Complete inventory for the declared Foundation capability set; API/Web and third-party image identities; required configuration/assets; embedded migrations; version and platform compatibility; authenticated bundle retrieval; signatures/provenance, SBOM/license and vulnerability evidence; repeat-build comparison; real image import/start and negative checks. |
| Excluded | Guided host installation, TLS issuance/activation, browser bootstrap, new business features, full analytics/worker integration, experimental-data migration, complete update/backup/restore, general Linux qualification and official/public product release. These remain allocated by WS-001 and MAP-001. |
| Preserved implementation | Existing GHCR/build workflow, digest-pinned bases and lockfiles, API/Web image split, shared API/migration image, Web/Edge image reuse, strict data parsing, separate migration job, existing runtime and supply-chain gate seams. |
| Owner-selected proof | Immutable retrieval plus controlled clean rebuild and explained comparison; byte-identical OCI rebuilds are not mandatory. Retrieve and start `linux/arm64` and `linux/amd64` images. Full installation proof remains C03 on M5 and a selected ARM64 Linux VM. |
| Access | Internal preliminary delivery; bundle retrieval requires authentication. Custometry images may remain public, and PostgreSQL remains an external public dependency. No repository-visibility change is selected. |
| Resource boundary | Preserve the L2 demo ceilings of 6 GiB RAM and 25 GiB owned data. Measure downloaded, unpacked and retained bytes separately; do not invent a new total-size target. Existing API/Web image-size limits are inputs to revalidate, not measured results here. |
| Requirements | Machine specification `0.11.0-draft`, sections 18.7–18.8, SEC-009/012, OPS-001/002 and section 24. Preserve MUST/SHOULD modality. SEC-009 is mandatory for an official release; this internal milestone proposes supply-chain checks without claiming official-release acceptance. SEC-016..018 and SCALE-003/004 constrain configuration without adding their full later proof to C02. |

The [human mirror](../../../../../custometry-technical-blueprint-human-ru.md) `0.11.0-draft` explains these clauses; inspected SHA-256 is `a8b027647e200e73dd66dbd017ae8f921b314e4e0c47a2d026768197ffca34c8`. The [runtime contract](../../../runtime-network-installation.md) doc_version 8 and [tooling gates](../../../tooling-gates.md) doc_version 9 distinguish candidates, local proof and accepted release. C02 does not weaken `check --scope release` or make an internal set eligible for the accepted end-user release entrypoint.

### Current-state evidence

The working tree was clean at inspection. Build, deployment, migration and application sources match the L2 code baseline `d9e1fddd2fd12ac51c88275544833d8b20b93728`; the comparison across application/package/deployment/workflow zones additionally found two changed route-contract JSON files. The published baseline is `f9f39a75994d2f7a8e8d7a75df293c35579f842d`, available from origin/main history. The earlier local inspection used `6664bd81fe5dae6ee47e3dbaf295c70776e9d800`; comparison confirms identical application, package, deployment, migration, workflow, Compose and lockfile bytes. Local-only governance commits are preserved locally and are not prerequisites for a fresh executor checkout.

| Claim ID | Capability | Observation | Evidence at baseline / external revision | Gap / next resolution |
|---|---|---|---|---|
| MS-001/EV-01 | Candidate producer | `code_observed` | [publish-candidates.yml](../../../../../.github/workflows/publish-candidates.yml): protected-main candidate sequence, two architectures, build provenance and SBOM requested, output digests recorded in job summary | No installable bundle producer or consumer verification is defined there. Complete the existing pipeline, retaining its candidate semantics. |
| MS-001/EV-02 | Hosted CI | `boundary_verified`: GitHub API status only | [Run 34054822070](https://github.com/Dejetins/custometry/actions/runs/34054822070), commit `f9f39a75994d2f7a8e8d7a75df293c35579f842d`, observed 2026-09-07: completed/success; two non-expired `.dockerbuild` artifacts | Success does not prove artifact retrieval or this local baseline. Package metadata request returned 403 for missing `read:packages`; package visibility and actual registry subjects remain unverified. No credential changes were made. |
| MS-001/EV-03 | Image contents | `code_observed` | [API Dockerfile](../../../../../apps/api/Dockerfile), [Web Dockerfile](../../../../../apps/web/Dockerfile), lockfiles, [.dockerignore](../../../../../.dockerignore) | API copies selected packages/plugins and migrations; Web contains built UI, public docs and Edge config. Test dependency/import/asset closure from a tracked clean checkout and from final images; do not infer it from COPY lines. |
| MS-001/EV-04 | Manifest consumers | `code_observed` | [validator](../../../../../deploy/compose/validate-release-manifest.py), [tests](../../../../../tests/integration/test_release_manifest.py), [release overlay](../../../../../deploy/compose/compose.release.yaml), [bootstrap](../../../../../deploy/compose/bootstrap.sh), [CI smoke](../../../../../deploy/compose/ci-smoke.sh), [Compose tooling](../../../../../tools/custometry_quality/compose_lifecycle.py) | Exactly three env keys, SemVer and fixed GHCR/digest allowlists; unknown keys fail. No signature, full inventory, platform or migration compatibility validation. These are the inspected direct readers; external consumers are not enumerated. |
| MS-001/EV-05 | Runtime inventory | `code_observed` | [compose.yaml](../../../../../compose.yaml), [demo resources](../../../../../deploy/demo-source/init/020_schema.sql) | Core uses three distinct image identities: API, Web and PostgreSQL. Edge reuses Web; migrate reuses API. Demo is optional and has checkout-relative init files. Valkey/workers are not current Compose services. |
| MS-001/EV-06 | Migration compatibility | `code_observed` | [migration environment](../../../../../migrations/env.py), [current head](../../../../../migrations/versions/0009_notifications.py), [lifecycle script](../../../../../deploy/compose/migration-lifecycle.sh) | Source graph ends at `0009_notifications`; inventory all revision/checksum pairs and obtain clean/repeat runtime proof from the selected image. A development downgrade drill does not establish installed upgrade or rollback safety. |
| MS-001/EV-07 | Verification seams | `code_observed` | [SBOM gate](../../../../../tools/custometry_quality/gate_sbom.py), [license gate](../../../../../tools/custometry_quality/gate_licenses.py), [license policy](../../../../../deploy/license-policy.json), [image-size check](../../../../../deploy/compose/check-image-size.sh) | Subject-bound SBOM checking exists, but the candidate workflow does not invoke these artifact gates. Extract/normalize real final-image evidence and resolve policy findings. Image-size checks currently default to API 350 MiB and Web 100 MiB; no new measurement was run. |
| MS-001/EV-08 | Installation path | `code_observed` | bootstrap derives repository-relative paths, requires host Python and Docker, creates local secrets, supports build/release and currently prints an HTTP URL | Reuse lifecycle mechanics where appropriate. C02 creates the portable supply input and verification seam; C03 owns guided launch, host prerequisites, HTTPS and safe installed-state lifecycle. |

### Dependencies and shared boundaries

| Dependency ID | Provider + required version | Required output | Consumer / needed before | Proof |
|---|---|---|---|---|
| MS-001/DEP-01 | WS-001 `1.0.3`, accepted scope inherited from `1.0.0` | C02 allocation, resources, subsequent C03–C06 ownership | All stages / decomposition | Parent decisions and this registered child |
| MS-001/DEP-02 | Runtime contract doc_version 8; tooling gates doc_version 8; development runtime at baseline | Candidate/release separation, network/storage constraints, existing gate boundaries | Contract and harness / before affected implementation | Source mapping and focused static/runtime evidence |
| MS-001/DEP-03 | Current source commit, locks, image bases and migration graph | One immutable build input record and complete package/asset inventory | Producer / S02–S04 | S01/S02 outputs, no dependency on completing another direction |
| MS-001/DEP-04 | User-selected access policy; artifact location and provider retention resolved by S01 within delegated technical scope | Authenticated bundle retention/retrieval, signer identity and authorized publication target | S03 external effects and S04 clean remote retrieval | ENG-01/02 below; existing GitHub/GHCR are reuse candidates, not invented target authority |
| MS-001/DEP-05 | Selected ARM64 runtime and AMD64 runtime, recorded before proof | Native image execution per architecture with engine/version/resource records | S04/S05 | Existing Linux AMD64 CI is a candidate; M5 can supply ARM64. If emulation is proposed instead, record its weaker boundary before acceptance. |

C03 is the consumer of C02, not an upstream prerequisite. Existing Identity/Web code is a packaging input, not a dependency on completing C04. Stages are sequential. The user arranges execution outside this plan; there is no assignee field or organization prerequisite.

## 2. Implementation decisions

### First delivery contents

| Component | Content and verification | Allocation |
|---|---|---|
| Small delivery bundle | Versioned manifest, exact Compose inputs, non-secret configuration schema/defaults, validator/verifier entrypoint, inventory/checksums, provenance/signature bundle, notices and bounded instructions | C02. Packaging must work outside a Git checkout; no source-build fallback. Full guided installer is C03. |
| API image | Application and transitive Python package/plugin/resource closure; release/source labels; migrations and required migration tooling | One digest supplies API and migration roles. Import/start and embedded-file inventory must match the manifest. |
| Web image | Built frontend, tracked static assets/fonts/notices, allowed public documentation, Web and Edge configurations | One digest supplies Web and Edge roles. Authenticated operator/admin docs remain outside the public docs surface. |
| PostgreSQL | Existing digest-pinned upstream image, both platform identities, required configuration and storage declarations | Explicit entry in the same inventory. Do not claim Custometry built or signed the upstream image; attest the selected upstream identity and retain available upstream evidence. |
| Demo source | Optional existing demo profile and its init/profile resources, separately inventoried if included | Accepted default: core-only delivery; include the existing demo profile/resources as an explicit optional component. Do not advertise an end-to-end data/demo capability before its later providers. |
| Required resources | Image-contained assets distinguished from bundle files, generated configuration, secret file slots, persistent volumes and bounded temporary space | Bundle includes no actual credentials, installation state, real customer data, caches or browser test runner. No speculative Valkey/worker images are added merely because the target blueprint lists them. |

An inventory does not certify every feature present in an image. S01 maps shipped routes and enabled services to their real dependencies. Existing incomplete capabilities require truthful unavailability or a bounded integration decision, not fabricated readiness, silent removal or new feature implementation hidden inside packaging.

### Versioned manifest proposal

Use one strict structured delivery record, provisionally `delivery-manifest.json`, with a separately versioned schema. This name and the following fields are a target proposal, not an existing file or finalized schema.

| Field group | Required meaning |
|---|---|
| Identity | Schema version, unique delivery SemVer, preliminary channel, exact full source commit, build workflow/run identity; version cannot be reassigned to different content. Keep application version, delivery version and manifest schema version distinct. |
| Capabilities | Enabled capability/profile identifiers, required service/resource references, explicit unavailable/deferred scope and observed evidence boundary. Do not use a product release label to imply untested features. |
| Images/platforms | Approved repository, OCI index digest and per-platform child digest/OS/architecture; service-to-image mapping, including PostgreSQL. Verify real descriptors and downloaded content. A local image-config ID is not interchangeable with an OCI index digest. |
| Files | Relative path, role, size and SHA-256 for every delivered configuration/resource/tool/notices file; bounded extraction and path rules. Verification must cover archive entries as well as declared files. |
| Compatibility | Manifest reader version, configuration schema, required Docker/Compose capability and tested versions, supported host/OCI platform distinction, exact application/image pairing and PostgreSQL version. Unknown major schema or platform fails closed. |
| Migrations/state | Embedded revision chain and file checksums, expected head, supported starting state, application read/write schema contract, migration command, downtime/irreversibility declaration and separately versioned artifact formats if actually used. Initially support a fresh owned database; do not invent compatibility with an earlier accepted product release. |
| Provenance and checks | Lock/base/toolchain identities; SBOM, license, vulnerability and build-comparison evidence references tied to actual subjects; signature bundle references. Signing covers exact canonical manifest bytes and its complete digest closure. |
| Resource/retrieval contract | Required bytes and declared resource ceilings; approved origins, exact remote artifact identity and retention/availability terms. Credentials are supplied through protected host/CI mechanisms, never in this record. |

Retain the existing strict `.release.env` format as a derived adapter for its known readers, without adding new keys or allowing arbitrary repositories. The canonical record owns PostgreSQL and file closure; the adapter and rendered Compose must agree with it. Bare legacy env data must never become evidence of a verified or accepted delivery. Internal verification uses an explicit candidate harness; it must not unlock the accepted end-user `--release` path before its required gates exist.

### Compatibility, trust and failure decisions

| ID / boundary | Current -> proposed | Classification and consumer | Rollout / recovery / proof |
|---|---|---|---|
| MS-001/IM-01: manifest readers | Three strict keys -> separate full record plus unchanged three-key projection | `compatible-change` proposed for the inspected legacy parser input only, conditional on byte-compatible validation. Directly inserting fields would be `breaking-change`: existing parser rejects them. New-format/old-reader combinations remain unsupported and must fail clearly. | Introduce schema/validator and fixtures first, then producer and consumer. Cross-check derived env, PostgreSQL and config identities; test old valid/invalid inputs and mismatched projection. |
| MS-001/IM-02: publication/access | SHA candidates and public source repository -> authenticated internal bundle referencing allowed image identities | `unknown` until location, retention, access semantics and current package visibility are verified | Preserve current public source policy. No promise of confidentiality for public image contents. Missing/expired/unauthorized artifacts block acceptance with a safe reason; never fall back to another version or source build. |
| MS-001/IM-03: authenticity | Requested BuildKit attestations -> verified signatures and source/subject binding | `compatible-change` for current candidate publication if retained; new verified-consumer contract needs direct proof | Proposed reuse: BuildKit provenance plus a pinned Sigstore/Cosign verifier, exact trusted repository/workflow identity and OIDC issuer. Trust policy must be provisioned independently of the untrusted bundle. ENG-02 resolves precise pins and initial verifier trust before implementation. |
| MS-001/IM-04: migration compatibility | Existing embedded graph -> explicit graph/head/hash and application compatibility record | `none` for current migration bytes if unchanged; installed-version transitions are `unknown` until a prior accepted release and compatibility policy exist | Fresh DB plus repeat-to-same-head proof from final API image. No down-migration promise. An existing incompatible database must be rejected by C03 before mutation; later C05 owns recovery drills. |
| MS-001/IM-05: configuration/resources | Checkout-dependent Compose and optional demo files -> closed portable configuration and declared resources | `unknown` until final render and consumer tests; repository development mode must remain valid | S02 inventories relative paths and host utility closure; S04 runs without checkout bind mounts. C03 owns installer-generated secrets, TLS inputs, permissions and persistent installation identity. |
| MS-001/IM-06: API/domain/UI contracts | Packaging and verification only; no proposed endpoint, domain schema, permission, event or browser-flow change | `none` for this draft's actual documentation edits; any later discovered product-code repair must be classified before inclusion | Existing authorization, private state ownership and locale-neutral core remain. Need for a material product change returns to the owner and its allocated milestone. |

For repeatability, build twice from the same tracked commit and locked inputs using isolated builders. Compare inventory, application assets and platform payloads; report OCI index/config/layer and attestation differences separately. Explain allowed build-time/signature metadata differences precisely. Unexplained application/dependency drift fails acceptance; a second arbitrary build is not sufficient. Preserve the selected delivery digests after publication, even if a later rebuild differs.

Publication is idempotent by delivery identity and complete content digest. A repeat may reuse identical content; conflicting content for an existing version fails. Make the complete verified manifest available only after referenced artifacts and evidence exist. On interrupted publication reconcile existing subjects before retry. Use staging paths and atomic finalization for local retrieval; partial, tampered or incompatible downloads must not reach execution or alter installed state. Retry transient transport failures within a declared finite budget; authentication, integrity and compatibility failures require correction. S01 specifies concrete limits instead of unbounded retries.

Technical references inspected on 2026-09-07: [Docker build attestations](https://docs.docker.com/build/metadata/attestations/) explains metadata attached to image indexes; [Sigstore verification](https://docs.sigstore.dev/cosign/verifying/verify/) documents identity/issuer verification. Tool configuration in source is not proof that a final artifact is signed or verified. Exact implementation versions remain ENG-02 outputs.

## 3. Work breakdown

These five accepted stage outcomes are encoded in the linked prompt pack. Current execution state lives only in the journal.

| Stage ID | Bounded result | Dependencies | Expected owned paths / zones | Output consumed by later work |
|---|---|---|---|---|
| MS-001-S01 | Freeze declared core/optional inventory, manifest/schema, reader compatibility, trust inputs and bounded failure semantics | Accepted plan; ENG-01/02 before affected external/trust implementation | Proposed delivery schema/tools under `deploy/compose/` and `tools/custometry_quality/`; focused tests; runtime/tooling contract amendments if required | Exact contracts, existing-source baseline and comparison protocol for S02/S03/S04 and C03. |
| MS-001-S02 | Build portable bundle and close final API/Web/migration/config/asset dependencies from tracked sources | S01 | Existing Dockerfiles, Compose release inputs, required tracked assets, new bounded packaging tool and tests; no broad application rewrite | Existing development paths retain their behavior. Output: deterministic inventory and artifact-producing inputs. |
| MS-001-S03 | Produce immutable candidates and authenticated preliminary bundle with complete supply evidence | S02; actual source/publication target authority before external effects | Existing candidate workflow plus bounded bundle job/workflow, gate adapters and redacted evidence | Publish only to the selected existing provider boundary. Output: retrievable identities, signatures, SBOM/license/vulnerability results and retention record. |
| MS-001-S04 | Retrieve selected bundle and all required platform images cleanly; prove imported-image closure and actual start/migrations | S03 remote artifacts, ENG-03 environments | Existing Compose lifecycle seams plus candidate verification harness and focused integration tests | Sequential target runs, explicit disposable resource ownership; no source build or hidden checkout asset mounts. Output: per-platform retrieval/start evidence and negative results. |
| MS-001-S05 | Explain rebuild comparison, close criterion coverage and hand off the supply contract to installation | S01–S04 | This plan's linked future journal/evidence, versioned delivery instructions and affected canonical documentation | Final result review with the user. Output: complete C03 handoff with exact subjects, tested limits and remaining installation work. |

## 4. Acceptance and proof allocation

| Criterion ID | Requirement / intent | Observable result | Proving stage / exact check or required input | Evidence / authority |
|---|---|---|---|---|
| MS-001/AC-01 | WS-001/AC-01; complete supply | Every enabled service, dependency, migration and file resolves from one verified record; no undeclared mount/resource or source checkout | S01/S02/S04: new schema/inventory checks and isolated extraction/render/import checks; command names finalized by S01 | Inventory and actual image/file evidence; technical acceptance |
| MS-001/AC-02 | DEC-01 reproducibility | Two clean locked builds have matching functional payload/dependency inventory or precisely explained permitted metadata differences; retrieval returns the selected immutable subjects | S03/S05: producer run pair and structured comparison tied to one source commit | Full hashes, builder inputs and difference disposition; unexplained functional drift blocks |
| MS-001/AC-03 | DEC-02 platform scope | Actual retrieval and start/import pass for required API/Web/PostgreSQL roles on both OCI architectures; migration tooling runs from the selected image | S04: native ARM64 and AMD64 target records; no cached/local-image substitution | Per-platform index/child identities, engine/resources and observed checks; does not qualify arbitrary hosts |
| MS-001/AC-04 | WS-001 delivery trust; SEC-009 relevance | Exact subject/source/producer binding is verified; wrong signature, issuer/identity, commit, file hash, digest or platform is rejected before execution | S03/S04: pinned verifier plus malicious/mismatched fixtures; final-image SBOM and license tools from tooling gates; vulnerability scanner/pin resolved in S01 | Real signatures/attestations, gate results and notices; required findings cannot be silently waived |
| MS-001/AC-05 | Compatibility; section 24.3 | Schema/config/application/migration pairing is explicit, unsupported combinations fail, fresh DB reaches declared head and repeat preserves it | S01/S04: legacy manifest tests, new producer/consumer tests; `alembic -c /app/migrations/alembic.ini upgrade head` inside selected image on disposable PostgreSQL; inspect head | Exact revision/checksum and actual DB evidence; no claim of previous-release rollback |
| MS-001/AC-06 | DEC-03/04 access and failure | Authorized retrieval succeeds; anonymous, expired/revoked credential and unavailable artifact cases fail safely; partial/archive traversal/symlink and identity substitution cases cannot execute or overwrite state | S03/S04: actual selected provider, protected credential handling and isolated hostile-input fixtures | Safe result codes and resource postconditions; no raw tokens/headers/provider payloads |
| MS-001/AC-07 | Boundary integration; OPS-002 | Final API/Web/docs/Edge artifacts start; readiness reflects tested dependencies; packaged migrations work; declared service/resource inventory matches runtime | S04: adapt candidate harness from existing lifecycle/CI smoke seams; check image size and import/start without a source build | Bounded engineering smoke, not HTTPS/browser-installation acceptance. Record enabled/untested capabilities explicitly. |
| MS-001/AC-08 | WS-001 C03 handoff | Installer author receives exact verified bundle/subjects, reader contract, resource/secret slots, migration/compatibility and error semantics, access/retention requirements and limitations | S05: criterion-to-evidence map, synchronized docs, owner acceptance of result | Canonical future journal receipt; remaining C03/C04/C05/C06 obligations are named |

Supply-chain checks apply to actual shipped dependencies, including upstream image contents and Web assets. Reuse the strict existing license policy; missing/unknown/review-required results remain unresolved until the appropriate decision, never automatically allowed because this is preliminary. SEC-009 critical unresolved findings preclude official release; this plan also proposes blocking the verified internal supply handoff on critical unresolved findings in shipped artifacts. Scanner freshness and evidence inputs are frozen in S01. No legal exception or vulnerability exemption is granted here.

Full `check --scope release`, installed HTTPS and browser journeys, restart/recovery and complete product performance remain their existing stronger boundaries. C02's successful subset does not produce a full release verdict. No real runtime, SBOM/license, vulnerability, rebuild or signature check was executed during this authoring task.

## 5. Execution and repair envelope

| Field | Envelope |
|---|---|
| Current preparation writes | Accepted plan, five prompts, canonical unstarted journal, tested local journal updater and schema validator, bound capability evidence, parent/navigation and tooling/adapter maintenance. Commit/PR/main synchronization and temporary branch deletion are explicitly authorized by the user. |
| Future allowed changes after execution authority | Delivery schema, packaging, relevant Dockerfiles and Compose supply inputs, candidate producer/verifier, focused tests and their canonical documentation. |
| Forbidden scope expansion | Domain/API redesign, implicit enabled feature removal, weakened release gates, TLS/bootstrap implementation assigned later, broad dependency upgrade, public release, repository visibility/credential changes, existing-installation mutation or host-wide cleanup. |
| Delegated engineering | File/field names, bounded implementation decomposition, exact fixture and inventory generation, compatible adapters and measured-size reporting within accepted requirements. |
| User review | Final milestone evidence and material scope/security changes. Interface/speed work includes visible references and metric comparisons. No routine intermediate contract-approval or task-assignment gate is added. Concrete external effects still require authority for their target. |
| In-scope repair | Repair demonstrated packaging/inventory/verification failures; rerun invalidated checks. A domain/runtime capability gap outside this scope remains explicitly allocated and is escalated with evidence. |
| Rollout / rollback | Preserve legacy input validation and development modes. Do not overwrite an existing version. Before DB mutation C03 checks compatibility; after an irreversible migration use its declared recovery/forward-repair policy. This milestone creates no downgrade promise. |
| Documentation effects | Runtime installation and tooling contracts, supply/installation instructions, GitHub governance when workflow meaning changes, architecture/parent links and generated index. Change product blueprints only if a separately accepted requirement amendment requires it. |
| Sensitive data | No keys, registry credentials, cookies, raw logs, environment dumps or local secret values in images, manifests, provenance or durable evidence. Build-time provenance must be inspected for sensitive build arguments before publication. |

### Remaining technical inputs

| Input | Resolution in the stage sequence | Needed before |
|---|---|---|
| MS-001/ENG-01 | S01 selects and verifies the smallest existing GitHub/GHCR-backed authenticated bundle location, exact artifact identity and provider retention. Prefer the existing Actions artifact mechanism if its observed access policy satisfies the accepted requirement; otherwise report the concrete mismatch. Record the retention horizon and preserve an installation-owned immutable handoff copy through C03–C06; do not silently treat expiring remote storage as permanent availability. Public repository status and unknown package visibility must not be mistaken for the bundle's access policy. | S03 external publication and S04 authenticated retrieval; provider retention is unrelated to user-account lifetime |
| MS-001/ENG-02 | S01 fixes signer workflow/ref/issuer, verifier/scanner/action versions, evidence format, safe trust bootstrap and retention. No keys/permissions are provisioned by planning. Additional host prerequisites must fit C03's guided installer contract. | Implementation of authentication/provenance verification and supply acceptance |
| MS-001/ENG-03 | S01 records available ARM64 and AMD64 native runners, engine/Compose versions and resource limits. C03 later records exact M5 host and ARM64 Linux guest/hypervisor installation inputs. | Per-platform runtime proof, not schema authoring |
| MS-001/ENG-04 | S01 enumerates actual shipped/available versus unavailable capabilities, including the accepted optional demo resources; preserve every declared dependency and present any material expansion to owner. | Final inventory acceptance and affected S02 packaging |

These are execution preparation outputs with named producing stages, not open user questions. Stage S01 resolves file/provider/tool details; it does not reopen the settled bundle authentication policy or ask for task assignments.

## 6. Execution artifact binding

| Field | Binding |
|---|---|
| `plan_doc` | `docs/architecture/planning/milestones/MS-001/plan.md`, accepted working version `1.1.0`; its current content digest is bound in the journal and each prompt. |
| `prompt_pack_dir` | [.codex/agents/generated/MS-001](../../../../../.codex/agents/generated/MS-001/), five stage prompts. |
| `stage_ledger` | [.codex/delivery/ledgers/MS-001.md](../../../../../.codex/delivery/ledgers/MS-001.md), the single technical execution journal. |
| Validation profile | Repository snapshot of Prompt Manager `prompt-pack/v1`: `python -m tools.custometry_quality.prompt_pack_validation`; read-only grouped gate `validate_prompt_packs`. The existing ledger/prompt/receipt schemas are preserved; accepted-plan SHA/version checks are added. |
| Claim/update mechanism | Implemented `custometry-stage-ledger/v1`, invoked with `python -m tools.custometry_quality.stage_ledger`. Local POSIX Git metadata lock, private session ownership, current-ledger SHA comparison, live input/receipt checks and atomic replacement; source and real-process test evidence are bound from the journal. See [tooling gates section 7](../../../tooling-gates.md#7-stage-journal-transactions). |
| Execution mode | `manual_sequential`. The journal remains `draft` until the first real claim; all rows are pending and unclaimed, with only S01 allowed. The plan is accepted and S01 is entry-ready; lifecycle `draft` means execution has not started. The user decides execution organization outside the artifacts. |

Before execution, recheck current source/capability hashes and authority, run the journal preflight, then atomically claim only the selected allowed stage. The updater is delivered by this preparation; S01 does not implement infrastructure for its own launch. The journal's small machine record is required by the selected pack format to preserve progress and prevent accidental repeated stages; it assigns nobody to any task.

## 7. Decisions and history

| Decision ID | Question / alternatives and consequence | Recommendation and basis | Decision / source / date / covered version |
|---|---|---|---|
| MS-001/DEC-01 | Immutable supply with repeat-build comparison versus mandatory byte-identical OCI rebuild | First option meets the supply/retrieval need while still detecting unexplained functional drift | Owner selected first option in this task, 2026-09-07; constrains draft `0.1.0` |
| MS-001/DEC-02 | Both existing OCI architectures versus ARM64 only | Keep ARM64+AMD64 image retrieval/start proof; full installation remains M5+ARM64 VM | Owner selected both, 2026-09-07; draft `0.1.0` |
| MS-001/DEC-03 | Internal authenticated preliminary bundle versus anonymous preview or official public product release | Internal C03 supply input; do not imply an accepted public release | Owner selected internal authenticated bundle, 2026-09-07; draft `0.1.0` |
| MS-001/DEC-04 | Authentication for bundle only versus all Custometry images | Bundle requires authentication; images may remain public; upstream PostgreSQL remains public | Owner selected bundle-only boundary, 2026-09-07; draft `0.1.0` |
| MS-001/DEC-05 | Core with optional demo and five stages | Accepted as proposed | User answers 1 and 2, 2026-09-07; version `1.0.0` |
| MS-001/DEC-06 | Task assignment and unnecessary process gates | No named task owners, roles or organization checkpoint in the plan/pack; user manages execution | User answer 4, 2026-09-07; version `1.0.0`. Pack authoring requested; execution/publication not requested |
| MS-001/DEC-07 | Interface and performance acceptance | Concrete metrics, comparison references and visible evidence; unmeasured budgets must not be described as passed | User answer 5, 2026-09-07; version `1.0.0`, implemented by the measurement contract below |
| MS-001/DEC-08 | Retention terminology and account lifetime | Bundle retention is technical artifact availability, not account expiry. Product account has no automatic lifetime expiry and remains until administrator disablement; session/token expiry and revocation remain separate | User answer 3, 2026-09-07; downstream C04 input, not a C02 identity-code change |

| MS-001/DEC-09 | Official working documents and a usable pack | Accept version 1.1.0, provide the tested local updater, enable only S01, publish through a technical branch to protected main and remove the branch after synchronization | Explicit user instruction, 2026-09-07; preserves DEC-01..08 and does not start product stages |

| Version | Date | Change and reason | References / authority |
|---|---|---|---|
| 0.1.0 | 2026-09-07 | First C02 draft and four initial owner inputs | Draft bytes preserved in task scratch before replacement |
| 1.0.0 | 2026-09-07 | Accepted core/optional-demo and five stages; no task assignments; explicit measurement/comparison contract; authorized five-prompt pack and draft journal | Current user answers 1–5 and request for complete plan/prompt pack |

| 1.1.0 | 2026-09-07 | Accepted working revision with tested repository updater and S01 entry readiness; product scope and measurement requirements unchanged | Current user instruction to finalize and publish; capability/check evidence in the canonical journal |

## 8. Measurable interfaces, size and performance

The user requires understandable measurements and something concrete to compare against. This is a measurement and evidence contract, not a claim that the product is fast. Every result table contains metric, unit, baseline identity/value, candidate identity/value, absolute and percentage delta where comparable, sample count/spread, criterion/source and verdict. Never write only “fast”, “optimized”, “works” or “no regression”.

| Metric / interface | Comparison reference | Required observation and criterion |
|---|---|---|
| Manifest/configuration contract | S01 versioned schema, verified fixtures and current strict three-key parser | 100% required field/file/service mappings covered; zero unknown accepted fields, unexplained inventory omissions or mismatched image/config/migration identities. All specified hostile-input cases reject before execution. |
| User-facing verifier output | S01 examples for valid, unauthorized, unavailable, tampered and unsupported inputs | Each case has a stable code, explicit result and next action; zero secret/token/DSN disclosures and zero success messages after failure. This is a CLI/data interface, not account login. |
| API/Web image sizes | Existing `check-image-size.sh`: API 367001600 bytes, Web 104857600 bytes; compare same-platform baseline image size too | Record unpacked image bytes per platform, downloaded compressed bytes separately, and retained bundle/resource bytes. Existing image caps pass/fail; no invented total bundle cap. |
| RAM and owned disk | WS-001 demo ceilings: 6 GiB RAM / 25 GiB owned data | Measure actual aggregate resource boundary during the bounded core and optional-demo checks, with engine allocation recorded separately. Preserve ceilings; never infer consumption from configured limits. |
| Retrieval | First successful real S03/S04 bundle retrieval establishes the baseline where the old workflow has no bundle | Record seconds, downloaded bytes and effective bytes/second; separate registry/auth/network time from local verification. Five cold and five cached runs per target when feasible within the disk cap; report median/min/max and all failures. Network conditions must match before comparative claims. |
| Verification and unpacking | Same input bytes, host, tool versions and cache mode; initial successful implementation becomes the versioned baseline | Record wall seconds and peak memory separately for signature/hash/schema verification and extraction. Five runs per mode, median/min/max. No fabricated before-value for a previously absent tool. |
| Image readiness | Existing source-built Foundation at the inspected baseline versus final pulled candidate, same host/platform, core profile, fresh owned DB and cache conditions | Measure container-start-to-ready seconds; migration seconds separately. Five comparable runs, median/min/max and failure count. Download/build duration is excluded from this boundary. If behavior differs, name the changed workload and limit the comparison. |
| Shipped Web fidelity | Clean prepackaging Web build from the same candidate commit/configuration, plus accepted target-pilot references only for demonstrated surfaces | Capture the same routes/states, RU/EN, browser build and desktop viewports 768x1024 and 1920x1080 before/after packaging. Require zero missing required assets, zero unexpected page/console/request errors and zero unexplained visible or interaction changes introduced by packaging. Report expected auth-denial responses separately. Image equality alone is not proof of behavior. |
| Shipped Web speed where C02 changes it | Same-commit prepackaging Web build on the same API fixture/host/browser and cache condition | Separately record navigation/request, response-to-stable-paint and relevant interaction-to-feedback milliseconds; at least 30 observations per declared journey/cache condition, empirical p50/p75/p95 with all raw samples and uncertainty. This is a bounded comparison, not a production percentile promise. |

S01 defines exact timer boundaries, deterministic fixtures, baseline commands and a compact source/target/screenshot matrix before dependent measurements. S02 preserves build inputs needed for the baseline. S04 gathers candidate data without retries chosen to obtain a passing result. S05 presents a concise before/after table and inspectable screenshots for any affected UI.

Existing numeric image/resource caps and exact contract/fidelity criteria are acceptance gates. There is no accepted millisecond budget or regression percentage for these new delivery timings. Record timing acceptance as `not assessed — threshold not specified` while still completing mandatory measurements and comparison; do not fabricate a `gate_performance` pass. Any requested performance improvement or material regression requires a baseline-backed proposal and an explicitly selected budget before that speed claim is accepted. This does not block unrelated packaging work. A missing required measurement is different: it blocks the measurement criterion, with a concrete unavailable input, rather than counting as zero or passing.

For subsequent C03/C04 UI work, carry WEB-PERF-001..006 forward: define representative installation/bootstrap/sign-in journeys, accepted numeric input-feedback/navigation/dispatch/paint budgets, realistic fixtures and user-visible comparison references before accepting those UI implementations. No historical threshold or static prototype measurement certifies the installed journey. C02 does not implement these later flows to populate a benchmark.

Additional criterion **MS-001/AC-09**: S01 establishes the measurement/reference protocol, S04 produces all applicable observations above, and S05 supplies baseline/candidate comparisons with valid gate verdicts and explicit unassessed speed budgets. It is a measurement-completeness criterion, not a claim that unspecified speed budgets passed.

### Downstream account clarification

The user states that the product account has no automatic age-based expiry and remains until administrator disablement. Before C04 implementation, reconcile this accepted user input into the machine/human AUTH requirements and that milestone's account/session tests. Do not extend this to immortal login sessions, refresh credentials, API tokens or registry credentials: AUTH-004/005/007/009 continue to apply. This C02 plan records the handoff without changing Identity code, the authentication policy of bundle retrieval, or the normative product blueprint in this unit.

## Mandatory documentation handoff

Parent WS-001 `1.0.3` registers this child and points back from `parent_ref`. Its patch adds navigation only; accepted L2 outcomes, criteria, decisions and five-child order retain their `1.0.0` meaning. DIR-006 and normative sources retain their exact WS-001 `1.0.0` accepted-scope bindings, preserved at baseline commit; this compatible navigation patch satisfies those unchanged obligations. L3 acceptance comes from the current user decisions, not from L2 inheritance. DIR-006 `1.2.0` remains this branch's direction source.

The architecture and generated contributor indexes register the new milestone. This preparation adds only the journal/tooling execution contract; product/API/schema/runtime policies, product blueprints and broader direction plans retain their accepted scope. Future C03/C04 still have no authored MS identity/path; their consumer obligations remain the existing WS-001 rows and the handoffs above. Exactly five prompts and one canonical unstarted journal are maintained; no separate ticket or duplicate progress register is created.

### Authoring verification — 2026-09-07

The initial draft passed documentation-index, link, blueprint and layout checks. Those observations remain historical for 0.1.0. Version 1.1.0 and its actual prompt/journal files are validated separately; current construction checks and the required independent review are recorded in the journal's authoring evidence section. The local updater is exercised in disposable Git fixtures; product code and runtime are not exercised by pack preparation. Future stage reports/receipts are not created or fabricated here.
