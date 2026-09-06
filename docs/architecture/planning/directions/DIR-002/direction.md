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
  "version": "1.1.0",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "MAP-001",
    "path": "docs/architecture/planning/project-map.md",
    "version": "1.1.0"
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
      "revision": "5a963ab0166bfa44d508679dcafa29723bbeb68b",
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
    "MAP-001/DEC-07"
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

> Accepted L1 scope and sequence links, version `1.1.0`, 2026-09-06. Parent: [MAP-001](../../project-map.md) `1.1.0`.
> MAP-001 records the owner-selected installation-first sequence and WS-001 entry.
> Detailed child acceptance, agent assignment and implementation remain separate decisions.

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
[human mirror](../../../../../custometry-technical-blueprint-human-ru.md), version `0.10.0-draft`. The
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

## Accepted sequence and first-block relationship

Follow [MAP-001's accepted sequence](../../project-map.md#accepted-delivery-sequence)
`1.1.0`. The selected starting document is [WS-001](../DIR-006/workstreams/WS-001.md) `0.1.0`, whose single
parent is DIR-006. Preserve storage/configuration and artifact-version ownership that constrains installation. Source, semantic and ingestion outcomes follow at MAP-001/SEQ-05..07.

This is a contribution/reference, not a second decomposition parent. No duplicate
WS or parallel dispatch is created. Actual provider contributions are bounded
inside the selected workstream; later contracts are resolved before their consumers.

## Relationships with other directions

These are interface relationships, not dependencies on completing an entire
direction. Future L2/L3 plans select actual provider milestones and acyclic hard
dependencies. Informational interactions do not create a cyclic execution graph.

| ID | Provider and version | Required output | Consumer | Needed before | Satisfaction proof / integration responsibility |
|---|---|---|---|---|---|
| DIR-002/DEP-01 | [DIR-001](../DIR-001/direction.md) `1.1.0` | Policy and common execution/fencing protocol | DIR-002 | Acceptance of the relevant scenario | Admission, access and attempt control. The owning milestone and its proof are selected at L2/L3. |
| DIR-002/DEP-02 | [DIR-006](../DIR-006/direction.md) `1.1.0` | Supported filesystem/storage environment and recovery procedure | DIR-002 | Acceptance of the relevant scenario | Durability and restore verification. The owning milestone and its proof are selected at L2/L3. |

**Outputs supplied:**

- [DIR-003](../DIR-003/direction.md) `1.1.0`: Versioned semantic datasets, metrics, relationships, readiness and marts.
- [DIR-004](../DIR-004/direction.md) `1.1.0`: Authorized manifests, data-as-of and lineage.
- [DIR-005](../DIR-005/direction.md) `1.1.0`: Source/mapping/DQ/Data Guide projections.
- [DIR-001](../DIR-001/direction.md) `1.1.0`: Published input generations and readiness events.
- [DIR-006](../DIR-006/direction.md) `1.1.0`: Immutable artifact/reference set and storage recovery ports.

Each consumer proves integration with the provider-owned contract. The common
snapshot/refresh ownership allocation is in [MAP-001](../../project-map.md). Actual public
contract changes remain with their accepted context owners.

## Owner decisions and next decomposition

| Decision ID | Decision or question | Authority / next condition | Effect |
|---|---|---|---|
| DIR-002/DEC-01 | This direction's L1 boundary and composition are accepted | Owner decision on 2026-09-06, recorded at [MAP-001 adoption](../../project-map.md) / MAP-001/DEC-05; version `1.0.0` | Settles L1 structure; does not accept an unwritten child plan. |
| DIR-002/DEC-02 | What is the next planning relationship? | Follow accepted MAP-001/DEC-06/07; WS-001 under DIR-006 is first. A separate child of this direction is not selected here | Contribute the declared prerequisites; select later owned L2 detail with the owner. |

Product exclusions, forecasting hold and XLSX sequencing in MAP-001 apply here.
No agent, calendar, worktree topology or parallel execution is assigned by this plan.

## History and document synchronization

| Version | Date | Change | Authority |
|---|---|---|---|
| 0.1.0 | 2026-09-06 | Russian owner-review draft | Initial draft request; historical authoring baseline |
| 1.0.0 | 2026-09-06 | L1 adopted in English; draft replaced; parent and interface versions synchronized | Owner acceptance and publication request; MAP-001/DEC-05 |
| 1.1.0 | 2026-09-06 | Apply accepted sequential priorities and first-block relationship; synchronize parent/provider versions; retain capability boundaries | Owner sequencing acceptance; MAP-001/DEC-06/07 |

MAP-001 registers this direction at `1.1.0`; metadata points back to that exact
parent version. Requirements, architecture and existing ticket state are unchanged.
Future edits update both sides of affected links. Publication/source checks and
their limits are recorded in MAP-001; no duplicate execution journal is created.
