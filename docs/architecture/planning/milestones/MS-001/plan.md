---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "milestone",
  "doc_id": "MS-001",
  "title": "Versioned internal delivery on upstream prebuilt dependencies",
  "version": "2.2.0",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "WS-001",
    "path": "docs/architecture/planning/directions/DIR-006/workstreams/WS-001.md",
    "version": "1.0.6"
  },
  "direction_ref": "DIR-006",
  "baseline_ref": {
    "commit": "b0e51705616a2deb5472a7af26a3b6daa79c2250",
    "evidence_refs": [
      ".codex/delivery/evidence/MS-001/restart-2026-09-08/owner-decision.md"
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
    "MS-001/DEC-09",
    "MS-001/DEC-10",
    "MS-001/DEC-11",
    "MS-001/DEC-12",
    "MS-001/DEC-13"
  ],
  "supersedes_ref": {
    "id": "MS-001",
    "version": "2.1.0",
    "path": ".codex/delivery/evidence/MS-001/s04-entry-2026-09-08/plan-2.1.0.md.snapshot",
    "reason": "Owner-approved S04 environment preparation within unchanged dual-platform acceptance"
  },
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

# MS-001. Versioned internal delivery on upstream prebuilt dependencies

**Accepted version 2.2.0, 2026-09-08.** The owner approved preparing the AMD64
verification path inside S04 and requested the corresponding plan, prompt and
journal updates. Native ARM64/AMD64 acceptance remains unchanged. Version 2.1.0
remains the immutable basis for accepted S03; S01/S02 retain their 1.1.0 basis.
[Current decision](../../../../../.codex/delivery/evidence/MS-001/s04-entry-2026-09-08/decision.md).
[Earlier internal-delivery decision](../../../../../.codex/delivery/evidence/MS-001/restart-2026-09-08/owner-decision.md).

Parent: [WS-001](../../directions/DIR-006/workstreams/WS-001.md) 1.0.6, C02.
Direction: DIR-006, accepted scope 1.2.0. State and claims belong only to the
[journal](../../../../../.codex/delivery/ledgers/MS-001.md).

## 1. Outcome and boundaries

Produce one understandable, versioned internal development bundle containing the
portable Compose/configuration/resources and exact prebuilt image identities
needed for installation work. API and migration share the API image; Web and Edge
share the Web image; PostgreSQL is an upstream image. Core plus explicit optional
demo and ARM64 + AMD64 remain in scope. No checkout or source build is needed by
the consumer. C03 owns guided installation/TLS; C04 owns first-account bootstrap;
C05/C06 own recovery and end-to-end acceptance.

The product blueprint 0.11.0-draft sections 18.7–18.8, SEC-009/012, OPS-001/002 and
section 24 remain the source. SEC-009 requires SBOM, vulnerability evidence and
signed provenance for an official release. This milestone no longer extends that
complete release gate to every internal build. The machine/human blueprint pair
already makes this distinction; no product-wide license waiver is introduced.

## 2. Accepted engineering requirements

| ID | Required behavior | Boundary |
|---|---|---|
| MS-001/REQ-01 | Use upstream prebuilt packages, ordinary package managers and standard base images, with versions/locks/digests recorded | Prefer a compatible supported binary release, including a bounded version update. No PyArrow source build, custom native-library variant, private distro assembly or fork without a separate owner decision explaining why ordinary packages cannot satisfy a concrete feature. |
| MS-001/REQ-02 | Build and assemble the complete local bundle before expanding assurance tooling | Start from the restored S02 producer. Reuse its inventory, strict legacy release-env parser and configuration. A local unsigned internal output is a valid S03 result when its declared profile, source and hashes are verified. |
| MS-001/REQ-03 | Collect existing upstream notices and available dependency/license/scan reports without automatic internal-build rejection for their findings | Unknown/review-required/unlisted metadata is reported honestly. A missing report is `not_observed`, never a fabricated pass. Do not require per-file legal adjudication, a custom SPDX engine, source-companion format or native compiler graph to finish this internal milestone. Actual third-party redistribution conditions still apply before redistribution. |
| MS-001/REQ-04 | Record actual security findings and prefer ordinary updates; assess a demonstrated reachable risk in the tested configuration | A scanner label alone does not trigger a custom rebuild or unbounded investigation. Report-only internal findings are not a security-clear verdict. Official release still blocks on unresolved critical findings under SEC-009. |
| MS-001/REQ-05 | Report image/download size and one observed build/retrieval/start duration per actual run | API 350 MiB and Web 100 MiB are advisory for this internal milestone. Keep hard disk/memory/ownership safeguards. Do not strip useful OS files or rebuild libraries solely to meet these image targets. |
| MS-001/REQ-06 | Keep one stable version/commit, image/platform digests, portable file hashes, migration identity and bounded verification before execution | Missing required payload, wrong digest/platform, escaping archive paths, secrets in payload or broken runtime remain real blockers. Do not overwrite an existing delivery identity with different bytes. |
| MS-001/REQ-07 | Separate `internal-development` from the existing release verification path explicitly | Missing signature/scan evidence is allowed only for explicitly selected internal development. Never silently relax the release reader or invent signatures, findings, hashes or credentials. No automatic promotion from this bundle to official release. |
| MS-001/REQ-08 | Finish one selected stage and reuse current evidence | No whole-repository audit, custom delivery framework or repeated independent reviews of every helper. Run focused checks for changed behavior; rerun only when inputs changed or a specific failure invalidates evidence. A large new subtask returns with its smallest ordinary alternative before implementation. |
| MS-001/REQ-09 | Prepare the consumer test environment as S04 work; distinguish entry from completion | Accepted S03, its available complete local handoff and a valid unclaimed S04 are entry inputs. A ready AMD64 job or remote transfer route is not an entry prerequisite. Native ARM64/AMD64 runtime evidence remains mandatory before accepting S04 or allowing S05. |

## 3. Current state and reuse

| Evidence | Observed state | Consequence |
|---|---|---|
| S01/S02 accepted journal records and immutable receipts | Delivery v1 schema/policy, portable configuration producer and original image packaging exist | Preserve acceptance for those exact historical inputs; new internal-profile behavior needs focused proof in S03. |
| Rollback baseline b0e51705616a2deb5472a7af26a3b6daa79c2250 | Historical S02 boundary used for the completed restart | The abandoned custom Arrow/source-review implementation remains removed; the subsequently accepted S03 adds the ordinary internal-profile producer. |
| Existing candidate workflow and S02 Dockerfiles | Standard upstream packages and ordinary prebuilt candidates | Reuse them; resolve only observed failures. The restored old pins are a rollback baseline, not an assertion of current security. |
| [Accepted S03 report](../../../../../.codex/delivery/evidence/MS-001/MS-001-S03/report.md) | The journal records acceptance under 2.1.0; the owner-local handoff retains six image archives and the exact reader | Reuse the accepted bundle and source identities without rebuilding S03. Its earlier AMD64 availability reservation is superseded by DEC-13 for entry only. |
| [S04 entry amendment](../../../../../.codex/delivery/evidence/MS-001/s04-entry-2026-09-08/decision.md) | Owner requested documentation and next-entry preparation | Only S04 can be enabled; this amendment makes no consumer runtime or S04 completion claim. |

## 4. Work breakdown and acceptance

| Stage | Result | Depends on | Owned paths / handoff |
|---|---|---|---|
| MS-001-S01 / S02 | Retained historical acceptance under 1.1.0 | Existing accepted records | No rerun; source-level compatibility is rechecked only where S03 changes it. |
| MS-001-S03 | A complete versioned internal bundle from ordinary upstream packages | S02 | Existing Dockerfiles, Compose/delivery schema-policy-producer, relevant candidate workflow, focused tests, runtime/tooling docs. Produce actual bundle, source/platform identities and short finding report. |
| MS-001-S04 | Prepare the native test targets and exact-bundle transfer, then prove clean retrieval/import/start on ARM64 and AMD64; packaged Web and fresh/repeat migration smoke | S03 | Existing lifecycle/delivery tools, a bounded verification workflow under .github/workflows, focused integration/browser checks and affected runtime/tooling docs. No source build or hidden checkout mounts on the consumer. |
| MS-001-S05 | Owner acceptance and exact C03 installation handoff | S04 | Existing plan/parent/runtime docs, reports and one journal; no new product work. |

| Criterion | Observable acceptance | Proof |
|---|---|---|
| MS-001/AC-01 | Every enabled service, migration and required configuration/asset resolves from the bundle | S03 inventory checks; S04 clean consumption |
| MS-001/AC-02 | One actual successful build per required platform from recorded immutable source/locked inputs; selected content is stable when retrieved | S03 source/digests; S04 verification. Mandatory double clean rebuild/comparison is removed from this internal milestone. |
| MS-001/AC-03 | ARM64 and AMD64 API/Web/PostgreSQL import/start proof | S04 completion requires both native runs; environment preparation is S04 work. No claim from emulation alone. |
| MS-001/AC-04 | Source, profile, image and file hashes/platforms are checked before execution; altered/mismatched inputs reject | S03/S04 positive and relevant negative checks. Signatures and clean license/vulnerability reports are not mandatory internal acceptance inputs; preserve truthful reports and official-release requirements. |
| MS-001/AC-05 | Configuration/application/migration pairing is explicit; fresh owned DB reaches declared head; repeating migration succeeds | S04 actual packaged Alembic and PostgreSQL; legacy three-key env validation remains strict |
| MS-001/AC-06 | One protected retrievable internal copy; no traversal, partial promotion, identity overwrite or credential exposure | Owner-local protected directory is sufficient. If remote retrieval is selected, use actual authorized access and finite timeout/retry; validate denial once. |
| MS-001/AC-07 | Required imports, API/Web/assets/Edge configuration and migrations work from selected prebuilt images | S04 actual smoke; no HTTPS/bootstrap/product-wide functional acceptance |
| MS-001/AC-08 | Installer author receives exact location, profile/reader, identities, configuration/resource/secret slots, platform and known limitations | S05 owner-reviewed handoff to WS-001/C03 |
| MS-001/AC-09 | Actual sizes and single-run build/retrieval/start/migration timings, clear tested/untested scope | S03/S04 observations; no mandatory five-run or thirty-sample benchmark, performance certification or packaging screenshot matrix |

### S04 entry, work order and completion

Entry checks establish accepted S03, the complete local bundle/reader and bound
report, current plan/prompt/journal agreement, and the exclusive updater. Use the
normal `advance` transaction if the unclaimed S04 is still disallowed. Do not
treat `Entry is not allowed` as an instruction to find a new server: inspect
the current decision and perform the authorized advancement. No runtime result
or ready remote job is required merely to begin environment preparation.

Within the claimed S04:

1. Inspect the handoff and prepare one focused consumer harness. Use the available
   M5 Docker engine for native ARM64. Retain the existing image bytes and metadata.
2. Implement the native AMD64 check using the selected `Dejetins/custometry`
   GitHub-hosted `ubuntu-24.04` target. A self-hosted runner is not required.
   Prepare a small verification job and an ordinary authenticated transfer of
   the exact retained archive set, portable payload and independently selected
   reader. Resolve the concrete transfer channel from existing access during S04;
   do not require the owner to supply infrastructure before local work starts.
3. Run available local integrity, native ARM64, migration and packaged-Web checks
   while the AMD64 job/transfer is being prepared. Agent organization remains
   owner-controlled; these are work dependencies, not a delegation instruction.
4. On the native AMD64 runner, verify trusted hashes, import the same archives
   and execute the consumer harness. Record the workflow/run, engine/architecture
   and exact subjects. An ordinary CI source rebuild cannot replace this proof.
5. Accept S04 only after both native targets and all applicable AC-01/03/04/05/06/07/09
   checks pass. Enable S05 only from that complete, receipt-backed result.

Preparation may edit the verification harness/workflow and its documentation.
Before upload or workflow execution, use the existing authorized repository,
access and audience; prepare the concrete transfer operation first. If a new
account, wider audience, credential or external action outside current authority
is actually needed, finish independent work and report that specific decision
with the smallest proposed operation. Pause at that boundary with `needs_input`;
do not ask generically for an AMD64 server or mark partial proof accepted.
No new registry service, runner fleet, public release, custom transport framework,
dependency rebuild, or reopened S03 is part of this clarification.

## 5. Delivery, compatibility and publication

Reuse the S02 v1 structure; add the smallest explicit internal-profile distinction
needed to represent unsigned/report-only output honestly. Existing signed-release
validation remains strict; old readers must reject unsupported new combinations.
Do not create v2 source-companion archives or a second generic delivery stack.
Changed input fixtures must test internal versus release behavior and digest/path
rejection. This is a deliberate compatible extension only if existing valid and
invalid release inputs retain behavior; otherwise version the specific boundary
and reject unsupported readers. No domain/API/migration redesign is authorized.

Default first output: owner-local protected directory under
`/Users/daniildegtyarev/.local/share/custometry/delivery/MS-001/`, with a unique
version subdirectory, directory mode 0700 and file mode 0600. This is an internal
working artifact and a C03 input, not an official release. Use existing immutable
registry subjects where suitable or retain locally built images/archives in the
protected handoff. List any retained Docker-store dependency so S04 can prove clean
retrieval; do not silently substitute a local tag for an immutable subject.

Earlier target authorization remains evidence for the selected GitHub repository,
workflow, native runners and 90-day artifact retention. Local output does not
require waiting for hosted signing/publication. Before using a remote target,
check actual current authority/access and its audience. A local report-only result
does not authorize ignoring license conditions when distributing images externally;
keep an artifact owner-local until applicable conditions are met. No automatic
public-registry upload or hidden remote side effect follows from building locally.
If Git publication is selected for implementation, follow protected main/PR policy.
The owner authorized publication of these changes through a technical branch and
PR to main, followed by synchronization and deletion of that branch. This does
not start S03 or deploy the platform.

## 6. Decisions and migration

| Decision | Accepted change and reason |
|---|---|
| MS-001/DEC-10 | Owner accepted ordinary upstream dependencies and internal-first delivery on 2026-09-08. Replaces the 1.1.0 internal critical-zero/license-clear/signature and repeat-build prerequisites; image targets become advisory. Avoid maintaining custom third-party builds. |
| MS-001/DEC-11 | Restore the accepted S02 implementation boundary and start S03 cleanly. The owner explicitly requested removal of the abandoned attempt, including its prompt, claim, transition entries, reports and snapshots. Update S04/S05 for the new internal handoff. |
| MS-001/DEC-12 | Preserve S01/S02 immutable contracts and receipts against the exact 1.1.0 snapshot. This is historical acceptance, not proof of new 2.1.0 behavior. Reconciliation uses the existing exclusive journal mechanism; never copy another session identity or reset the journal to draft. |
| MS-001/DEC-13 | Owner approved S04 environment/CI and exact-archive transfer preparation as work inside the stage, with local checks continuing independently. The AMD64 availability reservation in the S03 handoff no longer prevents entry. Native dual-platform acceptance and remote-action authority remain unchanged. Preserve S03 prompt/report/receipt bytes against the 2.1.0 snapshot; update only pending S04/S05 contracts and normal next-entry permission. Source: current decision linked above, 2026-09-08; covered version 2.2.0. |

DEC-02 platform coverage, DEC-03/04 internal audience and permitted image access,
DEC-05 core/optional demo, DEC-06 owner control of agents, and DEC-08 account
lifetime remain. DEC-01 mandatory repeat builds and DEC-07 repeated benchmark
sampling are superseded for this internal milestone. Details of earlier decisions
remain in the 1.1.0 snapshot. S03 requires its own explicit execution request; publication does not start it.

## 7. Execution artifact binding and checks

`plan_doc`: this accepted 2.2.0 document. `prompt_pack_dir`:
[MS-001](../../../../../.codex/agents/generated/MS-001/). `stage_ledger`:
[MS-001](../../../../../.codex/delivery/ledgers/MS-001.md). The journal alone records stage status and permission.
The 2026-09-08 amendment preserves S01/S02/S03 accepted results and updates the two
unclaimed successor prompts. S04 is the only next-entry candidate; S05 depends on
its complete acceptance. Default mode is `manual_sequential`.

The standard `prompt-pack/v1` validator and `custometry-stage-ledger/v1` updater
remain. A terminal row may bind its immutable historical plan snapshot and explicit
reconciliation evidence; active/pending prompts bind only this current plan.
The existing capability already supports terminal historical-plan bindings.
Preserve S03's exact 2.1.0 plan, prompt and receipt; the current DEC-13 evidence
explains the compatible future-stage amendment. Claims and execution receipts
are not created during this document update. Normal advancement records S04
permission separately from the accepted S03 receipt.

### Downstream account clarification

An account has no automatic age-based expiry and remains until administrator
disablement. C04 must reconcile this accepted input with AUTH requirements before
implementation. Session, refresh-token, API-token and registry credential expiry
remain separate; no identity implementation changes are made here.

## Mandatory documentation handoff

WS-001 1.0.6 registers this compatible execution detail while preserving the L2
five-outcome scope. The architecture index follows the exact child versions.
Accepted S03 runtime/tooling documentation and implementation remain unchanged by
this amendment; S04 updates those documents when its actual consumer path exists.
Product blueprints and L1/L2 acceptance stay unchanged. Run prompt/ledger validation,
read-only S04 entry preflight and the local documentation/source gate; record the
independent review and preservation check in the linked amendment checks. No
container build, product test matrix or runtime execution is needed for authoring.

| Version | Date | Change / authority |
|---|---|---|
| 1.1.0 | 2026-09-07 | Original accepted plan, preserved in the immutable restart snapshot |
| 2.1.0 | 2026-09-08 | Owner accepted simplified requirements, full S03 rollback and preparation of S03; S01/S02 acceptance retained |
| 2.2.0 | 2026-09-08 | Owner approved compatible S04 environment and transfer preparation; unchanged dual-platform completion, accepted S03 preserved and S04 next-entry enabled through the updater |
