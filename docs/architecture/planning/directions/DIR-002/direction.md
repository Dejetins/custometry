---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "direction",
  "doc_id": "DIR-002",
  "title": "Data and semantic model",
  "version": "2.2.0",
  "planning_status": "in_review",
  "language": "en",
  "parent_ref": {
    "id": "MAP-001",
    "path": "docs/architecture/planning/project-map.md",
    "version": "2.2.0"
  },
  "direction_ref": "DIR-002",
  "baseline_ref": {
    "commit": "5a963ab0166bfa44d508679dcafa29723bbeb68b",
    "evidence_refs": [
      "docs/architecture/planning/project-map.md#sources-and-proof-boundary"
    ]
  },
  "requirement_refs": [
    {
      "source": "custometry-technical-blueprint-ru.md",
      "revision": "sha256:183d9d2f2070cb8e651eca46fa44244b0d0af2a914830bcee6e5716ae15fd163",
      "ids": [
        "GOAL-001",
        "GOAL-002",
        "CONNECTOR-002",
        "INGEST-008",
        "INGEST-020",
        "DATA-MAP-001",
        "DATA-MAP-007",
        "METRIC-001",
        "FILTER-013",
        "DQ-INPUT-001",
        "DQ-REMEDIATE-001",
        "MART-GRAIN-001",
        "ARTIFACT-COMMIT-001",
        "ARTIFACT-COMMIT-003",
        "V1-AC-063",
        "V1-AC-067"
      ]
    }
  ],
  "decision_refs": [
    "FRAME/DEC-01",
    "FRAME/DEC-03",
    "FRAME/DEC-06",
    "MAP-001/DEC-01",
    "MAP-001/DEC-02",
    "MAP-001/DEC-05",
    "DIR-002/DEC-01",
    "MAP-001/DEC-06",
    "MAP-001/DEC-07",
    "MAP-001/DEC-09",
    "MAP-001/DEC-10",
    "MAP-001/DEC-11",
    "MAP-001/DEC-12",
    "MAP-001/DEC-13",
    "MAP-001/DEC-14",
    "MAP-001/DEC-15"
  ],
  "supersedes_ref": null,
  "proof_boundary": {
    "label": "accepted-level-1-planning-boundaries",
    "exclusions": [
      "unwritten-child-acceptance",
      "exhaustive-code-audit",
      "runtime-readiness",
      "implementation-authority"
    ]
  }
}
---

# DIR-002. Data and semantic model

> L1 sequence draft `2.2.0`, 2026-09-17. Parent: [MAP-001](../../project-map.md) `2.2.0`.
> Accepted capability boundaries remain; WS-002 is the first-report foundation. WS-003 2.0.0 is the accepted metric-workspace continuation under DIR-004.
> The broader checkpoint sequence remains under review; WS-002/MS-003 0.2.0 was accepted on 2026-09-13.

## Intent and boundaries

**Expected outcome:** A company connects its sources, maps them into an explainable common model and refreshes data safely while preserving provenance, quality and history.

| Field | Accepted L1 definition |
|---|---|
| Included | Connections, files and SQL sources; pull/push/readiness; full/incremental/partition refresh; canonical identity, grain, returns and history; typed mapping and derived channels; metrics/filters/capabilities and Data Guide; DQ/remediation; reusable marts; manifests, commit, retention and artifact repair through owner ports. |
| Excluded / adjacent ownership | Analytical calculation and segmentation belong to DIR-003; generic orchestration to DIR-001; mapping/DQ UI to DIR-005; coordinated installation backup to DIR-006. An off-primary backup destination does not authorize a remote primary ArtifactStore. |
| Existing architecture owners | Connection Catalog; Ingestion; Semantic Model; Data Documentation; Data Quality; Artifact Lifecycle. Canonical facts and marts retain accepted ownership. |
| Main requirement areas | Machine sections 4–8, 10–11, particularly 6.1 and 7; corresponding human sections; source-data-adaptation contract. |
| Observable direction completion | Supported real sources satisfy the agreed ingestion/refresh matrix; meaning, quality, history and access are reproducible; publication failures, retries and cleanup preserve valid results. |

Normative meaning remains in the [machine blueprint](../../../../../custometry-technical-blueprint-ru.md) and
[human mirror](../../../../../custometry-technical-blueprint-human-ru.md), version `0.11.0-draft`. The
[context map](../../../bounded-context-map.md) doc_version 13
defines ownership. Metadata pins the source commit. Selected `requirement_refs`
are anchors, not an exhaustive direction acceptance inventory.

## Known current state

W14 proves bounded PostgreSQL/file intake; W15 describes one retail snapshot through Parquet, DQ and semantic publication. This base does not prove the complete connector matrix, daily rebuild without updated_at, or later durable commit/recovery obligations.

| Claim ID | Observation | Evidence | Limit / next resolution |
|---|---|---|---|
| DIR-002/EV-01 | `documented_only`: recorded previous results | [W14-SOURCE-CONNECTION-FILE-IMPORT-KERNEL](../../../../../.codex/delivery/evidence/W14-SOURCE-CONNECTION-FILE-IMPORT-KERNEL.md); [W15-INGESTION-DQ-SEMANTIC-VERTICAL-SLICE](../../../../../.codex/delivery/evidence/W15-INGESTION-DQ-SEMANTIC-VERTICAL-SLICE.md) | Historical reports were inspected; recheck applicability before implementation. |
| DIR-002/EV-02 | `code_observed`: bounded static inspection | [apps/api/src/custometry_api/main.py](../../../../../apps/api/src/custometry_api/main.py) | Only this entrypoint/contract was inspected; no complete direction audit is claimed. |
| DIR-002/EV-03 | `unknown`: complete direction readiness | No current exhaustive requirement-to-code-to-proof matrix | Resolve within the selected L2 investigation; do not assign a completion percentage. |

## Candidate L2 composition

These rows describe the accepted L1 scope at candidate workstream granularity.
The unselected rows are not accepted L2 plans. The selected first-block document
is referenced separately below. Other WS documents receive stable IDs, versions
and reciprocal parent links only after selection; no milestone is initialized here.

| Local candidate ID | Large task | Intended result | Existing base / dependency |
|---|---|---|---|
| DIR-002/C01 | Source connection and admission | Agreed source contracts, SQL matrix, governed CSV/XLSX, readiness and push/pull. | Reuse W14; other sources and transport modes need direct proof. |
| DIR-002/C02 | Refresh and history | Repeatable refresh, late corrections, absence/reappearance and uncertain rekey. | Reuse W15; test sequential full snapshots without row updated_at. |
| DIR-002/C03 | Semantics and metrics | Versioned entities, relationships, dictionaries, channels, metrics, filters and capabilities. | Reconcile the W15 kernel with remaining registries. |
| DIR-002/C04 | Quality and data explanation | DQ, quarantine/coverage, remediation/waivers, Data Guide and safe preview. | Readiness is capability-specific; errors never silently become zero. |
| DIR-002/C05 | Marts and artifact lifecycle | Shared granular marts, immutable artifacts, durable publication, retention and repair. | Compare W15 with ARTIFACT-COMMIT-001..003; no new fault proof is claimed. |

The agent produces future selected documents with the owner; the owner is not
expected to supply them manually. Candidate presence is not entry readiness.

## Product-first sequence and contributions

Follow the proposed checkpoint order in [MAP-001 2.2.0](../../project-map.md#proposed-product-checkpoints).
Supply one real prepared input path for the first report, with the necessary
semantics, quality admission and version identity. The user-facing connection,
mapping and refresh journey then extends that path. Do not require the entire
connector catalogue or data-management UI before the first usable report.
The existing [WS-001](../DIR-006/workstreams/WS-001.md) `1.0.10` retains its
accepted scope and completed evidence, but full C04–C06 is no longer the next
universal prerequisite. The selected first product workstream is registered below; no agent dispatch is authorized.

## Development cadence for this direction

Follow [MAP-001 2.2.0](../../project-map.md#development-and-delivery-cadence),
DEC-12 (owner decision, 2026-09-17). Develop and accept the selected feature
locally, reusing the current implementation and the real provider boundaries
needed for its claim. Do not add candidate builds, container qualification or
final-delivery checks merely because a stage or milestone ends. Packaging and
its target compatibility proof are a separately selected delivery task.
The [metric-workspace composition](../../../ui/drafts/metric-workspace-v1/README.md)
is an accepted initial design baseline; [WS-003 2.0.0](../DIR-004/workstreams/WS-003.md) records the accepted continuation.
MS-003 S05/S06 remain deferred in their canonical journal.
Capability boundaries and completed evidence remain unchanged.

## Relationships with other directions

These are interface relationships, not dependencies on completing an entire
direction. Future L2/L3 plans select actual provider milestones and acyclic hard
dependencies. Informational interactions do not create a cyclic execution graph.

| ID | Provider and version | Required output | Consumer | Needed before | Satisfaction proof / integration responsibility |
|---|---|---|---|---|---|
| DIR-002/DEP-01 | [DIR-001](../DIR-001/direction.md) `2.2.0` | Policy and common execution/fencing protocol | DIR-002 | Acceptance of the relevant scenario | Admission, access and attempt control. The owning milestone and its proof are selected at L2/L3. |
| DIR-002/DEP-02 | [DIR-006](../DIR-006/direction.md) `2.2.0` | Supported filesystem/storage environment and recovery procedure | DIR-002 | Acceptance of the relevant scenario | Durability and restore verification. The owning milestone and its proof are selected at L2/L3. |

**Outputs supplied:**

- [DIR-003](../DIR-003/direction.md) `2.2.0`: Versioned semantic datasets, metrics, relationships, readiness and marts.
- [DIR-004](../DIR-004/direction.md) `2.2.0`: Authorized manifests, data-as-of and lineage.
- [DIR-005](../DIR-005/direction.md) `2.2.0`: Source/mapping/DQ/Data Guide projections.
- [DIR-001](../DIR-001/direction.md) `2.2.0`: Published input generations and readiness events.
- [DIR-006](../DIR-006/direction.md) `2.2.0`: Immutable artifact/reference set and storage recovery ports.

Each consumer proves integration with the provider-owned contract. The common
snapshot/refresh ownership allocation is in [MAP-001](../../project-map.md). Actual public
contract changes remain with their accepted context owners.

## Selected first product contribution — 2026-09-12

[WS-002](../DIR-004/workstreams/WS-002.md) `0.2.0` and
[MS-003](../../milestones/MS-003/plan.md) `0.2.0` now define the next first-report
accepted scope, with six prompts and one canonical journal. The owner accepted
WS-002/MS-003 0.2.0 on 2026-09-13; initial entry is recorded in that journal. This
contribution is implemented once in MS-003, not duplicated into another pack.

S01 supplies genuine prepared PostgreSQL intake/DQ/admission; S02 adds only the three metric/mart projections. The next own-data UI workstream follows this first report and retains the real-source adaptation requirements.

## Owner decisions and next decomposition

| Decision ID | Decision or question | Authority / next condition | Effect |
|---|---|---|---|
| DIR-002/DEC-01 | This direction's L1 boundary and composition are accepted | Owner decision on 2026-09-06, recorded at [MAP-001 adoption](../../project-map.md) / MAP-001/DEC-05; version `1.0.0` | Settles L1 structure; does not accept an unwritten child plan. |
| DIR-002/DEC-02 | Previous WS-001-first selection | Historical MAP-001/DEC-06/07; next-selection priority superseded by MAP-001/DEC-10 on 2026-09-12 | Retain completed base and deferred scope; proposed product contributions are described above. |

Product exclusions, forecasting hold and XLSX sequencing in MAP-001 apply here.
No agent, calendar, worktree topology or parallel execution is assigned by this plan.

## History and document synchronization

| Version | Date | Change | Authority |
|---|---|---|---|
| 0.1.0 | 2026-09-06 | Russian owner-review draft | Initial draft request; historical authoring baseline |
| 1.0.0 | 2026-09-06 | L1 adopted in English; draft replaced; parent and interface versions synchronized | Owner acceptance and publication request; MAP-001/DEC-05 |
| 1.1.0 | 2026-09-06 | Apply accepted sequential priorities and first-block relationship; synchronize parent/provider versions; retain capability boundaries | Owner sequencing acceptance; MAP-001/DEC-06/07 |
| 1.2.0 | 2026-09-06 | Revalidate unchanged direction boundary and MAP/WS links against accepted WS-001 1.0.0 and amended requirement sources | Owner finalization instruction; substantive changes are owned by WS-001 |
| 1.3.0 | 2026-09-11 | Apply MAP-001 development cadence and synchronize reciprocal parent/provider links; preserve capability boundaries and closed milestone evidence | Owner accepted approach and requested general planning amendment; MAP-001/DEC-09 |
| 2.0.0 | 2026-09-12 | Draft product-first ordering and analyst-report L2 contributions; retain accepted scope | Owner priority correction, MAP-001/DEC-10; detailed sequence under review |
| 2.0.1 | 2026-09-12 | Register WS-002/MS-003 review candidates and exact first-product contributions; synchronize navigation | Owner requested documentation, prompts and journal; MAP-001/DEC-11 |
| 2.0.2 | 2026-09-12 | Refresh reciprocal navigation for WS-002/MS-003 0.2.0; L1 scope and checkpoint order unchanged | Owner requires Customer and Product data in the selected child; editorial reference maintenance |
| 2.0.3 | 2026-09-17 | Apply local feature acceptance and separately selected packaging; synchronize parent/provider navigation | MAP-001/DEC-12; owner correction |
| 2.1.0 | 2026-09-17 | Record accepted initial metric-workspace composition and register WS-003 0.1.0 continuation proposal; synchronize navigation without changing L1 scopes | MAP-001/DEC-13 |
| 2.1.1 | 2026-09-17 | Record owner acceptance of WS-003 1.0.0 sequence and C01 scope; preserve deferred goal and shared-write policies | MAP-001/DEC-14; editorial navigation synchronization |
| 2.2.0 | 2026-09-20 | Register WS-003 2.0.0 owner decisions: six grains, goal modes/recurrence/run rate and creator-only report authoring; retain child order | MAP-001/DEC-15; owner numbered answers |

MAP-001 2.2.0 registers this sequence draft at 2.2.0 with reciprocal draft
parent/provider links. Capability boundaries remain accepted at their earlier
basis; this draft does not change public/domain contracts or accept an unwritten
child. WS-001 navigation 1.0.10 keeps scope 1.0.0 and its recorded DIR-006 1.2.0
parent basis; its unimplemented C04–C06 remain allocated for later selection.
Completed milestones preserve exact historical plan/pack/journal/evidence bytes.
The map owns the proposed checkpoint order and records its validation.
