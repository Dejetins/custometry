---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "direction",
  "doc_id": "DIR-004",
  "title": "Analytical documents and result delivery",
  "version": "2.1.1",
  "planning_status": "in_review",
  "language": "en",
  "parent_ref": {
    "id": "MAP-001",
    "path": "docs/architecture/planning/project-map.md",
    "version": "2.1.1"
  },
  "direction_ref": "DIR-004",
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
        "GOAL-012",
        "GOAL-017",
        "ANALYTICAL-DOC-001",
        "ANALYTICAL-DOC-014",
        "CHART-001",
        "REPORT-015",
        "REPORT-016",
        "REPORT-REFRESH-001",
        "REPORT-REFRESH-005",
        "REPORT-REFRESH-006",
        "REPORT-MAIL-001",
        "XLSX-001",
        "BRAND-001",
        "V1-AC-068",
        "V1-AC-069"
      ]
    },
    {
      "source": "custometry-technical-blueprint-ru.md",
      "revision": "sha256:28c52edab5c48b3f0a01aaf08c02792d2c4988beee3b27960562ef31c77c651f",
      "ids": [
        "METRIC-025",
        "METRIC-026",
        "METRIC-027",
        "METRIC-028",
        "METRIC-029",
        "CHART-021"
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
    "DIR-004/DEC-01",
    "MAP-001/DEC-06",
    "MAP-001/DEC-07",
    "MAP-001/DEC-09",
    "MAP-001/DEC-10",
    "MAP-001/DEC-11",
    "MAP-001/DEC-12",
    "MAP-001/DEC-13",
    "MAP-001/DEC-14"
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

# DIR-004. Analytical documents and result delivery

> L1 sequence draft `2.1.1`, 2026-09-17. Parent: [MAP-001](../../project-map.md) `2.1.1`.
> Accepted capability boundaries remain; WS-002 is the first-report foundation. WS-003 1.0.0 is the accepted metric-workspace continuation under DIR-004.
> The broader checkpoint sequence remains under review; WS-002/MS-003 0.2.0 was accepted on 2026-09-13.

## Intent and boundaries

**Expected outcome:** Users compose, save and publish exact documents from prepared results, refresh them safely and consume consistent Web/email/XLSX representations.

| Field | Accepted L1 definition |
|---|---|
| Included | Shared document/page/section/block composition; root/page snapshots and exact result references; filters/personal views and lineage; notes/annotations and semantic diff; refresh policy/current snapshot; prepared serving; ChartSpec/compiler and shared static rendering; BrandProfile/CompanyPack composition; report delivery and final universal XLSX. |
| Excluded / adjacent ownership | Analytical values, pivot totals and segment membership belong to DIR-003; physical artifact commit/retention to DIR-002; scheduler mechanics to DIR-001; drag-and-drop/inspector/components to DIR-005; measured serving capacity and full restore drill to DIR-006. |
| Existing architecture owners | Presentation & Reports; Report Delivery; chart_compiler_ts as the shared deterministic compiler. Research findings and discussions retain their own context owners. |
| Main requirement areas | Machine sections 14, 15.4.2 and 23.6; human sections 14–15 and 23; demonstrated target-pilot decisions remain authoritative. |
| Observable direction completion | One publication has consistent values across supported channels; refresh preserves history and monotonic current state; readers obtain a safe prepared snapshot. Closure includes real data, analytical and Web integration. |

Normative meaning remains in the [machine blueprint](../../../../../custometry-technical-blueprint-ru.md) and
[human mirror](../../../../../custometry-technical-blueprint-human-ru.md), version `0.11.0-draft`. The
[context map](../../../bounded-context-map.md) doc_version 13
defines ownership. Metadata pins the source commit. Selected `requirement_refs`
are anchors, not an exhaustive direction acceptance inventory.

## Known current state

The target contracts and pilot exist. A presentation package does not establish a completed composer: the inspected PeopleService serves people projections. Common document persistence, refresh, prepared serving, email and XLSX readiness are not established by this inspection.

| Claim ID | Observation | Evidence | Limit / next resolution |
|---|---|---|---|
| DIR-004/EV-01 | `documented_only`: recorded previous results | [W17-PEOPLE-CONTRIBUTOR-ACTIVITY-PROJECTION](../../../../../.codex/delivery/evidence/W17-PEOPLE-CONTRIBUTOR-ACTIVITY-PROJECTION.md) | Historical reports were inspected; recheck applicability before implementation. |
| DIR-004/EV-02 | `code_observed`: bounded static inspection | [packages/presentation/application/people.py](../../../../../packages/presentation/application/people.py) | Only this entrypoint/contract was inspected; no complete direction audit is claimed. |
| DIR-004/EV-03 | `unknown`: complete direction readiness | No current exhaustive requirement-to-code-to-proof matrix | Resolve within the selected L2 investigation; do not assign a completion percentage. |

## Candidate L2 composition

These rows describe the accepted L1 scope at candidate workstream granularity.
The unselected rows are not accepted L2 plans. The selected first-block document
is referenced separately below. Other WS documents receive stable IDs, versions
and reciprocal parent links only after selection; no milestone is initialized here.

| Local candidate ID | Large task | Intended result | Existing base / dependency |
|---|---|---|---|
| DIR-004/C01 | Document and publication | Common Dashboard/Workbook/Research model, stable blocks/pages and immutable snapshots. | Reuse accepted contracts while preserving content/presentation ownership. |
| DIR-004/C02 | Authoring, bindings and history | Filter/parameter bindings, notes/annotations, personal views, exact anchors and semantic diff. | Metric definitions come from DIR-002; analytical calculations and results from DIR-003; discussions from DIR-001. |
| DIR-004/C03 | Refresh and prepared results | after_ingestion/scheduled/manual, waiting_for_data, coalescing, atomic current and last-good. | REPORT-REFRESH-001..007; an open viewer applies updates explicitly. |
| DIR-004/C04 | Rendering and branding | One ChartSpec compiler, Web/static parity, BrandProfile and CompanyPack. | No renderer recomputes business values; render identity is versioned. |
| DIR-004/C05 | Delivery and exports | Exact-snapshot operations, report email policy/reconciliation and shared export adapters. | Report email remains separate from operational notifications. |
| DIR-004/C06 | Universal XLSX — late phase | One workbook renderer over stable ReportSnapshot. | Preserve its position as the final new functional v1 increment. |

The agent produces future selected documents with the owner; the owner is not
expected to supply them manually. Candidate presence is not entry readiness.

## Product-first sequence and contributions

Follow the proposed checkpoint order in [MAP-001 2.1.1](../../project-map.md#proposed-product-checkpoints).
This direction is the parent of the accepted WS-002 scope: a working analyst report
using the C01/C02 document and authoring scope. Start with useful blocks, period/
filter controls, backend save/reopen and reproducible results. DIR-005 owns Web,
DIR-002/003 provide actual inputs/calculations and DIR-001 supplies bounded policy
support. The owner selected preparation of [WS-002 0.2.0](workstreams/WS-002.md) and [MS-003 0.2.0](../../milestones/MS-003/plan.md); the concrete 0.2.0 plans and pack were accepted on 2026-09-13.
The existing [WS-001](../DIR-006/workstreams/WS-001.md) `1.0.10` retains its
accepted scope and completed evidence, but full C04–C06 is no longer the next
universal prerequisite. The selected first product workstream is registered below; no agent dispatch is authorized.

## Development cadence for this direction

Follow [MAP-001 2.1.1](../../project-map.md#development-and-delivery-cadence),
DEC-12 (owner decision, 2026-09-17). Develop and accept the selected feature
locally, reusing the current implementation and the real provider boundaries
needed for its claim. Do not add candidate builds, container qualification or
final-delivery checks merely because a stage or milestone ends. Packaging and
its target compatibility proof are a separately selected delivery task.
The [metric-workspace composition](../../../ui/drafts/metric-workspace-v1/README.md)
is an accepted initial design baseline; [WS-003 1.0.0](workstreams/WS-003.md) records the accepted continuation.
MS-003 S05/S06 remain deferred in their canonical journal.
Capability boundaries and completed evidence remain unchanged.

## Relationships with other directions

These are interface relationships, not dependencies on completing an entire
direction. Future L2/L3 plans select actual provider milestones and acyclic hard
dependencies. Informational interactions do not create a cyclic execution graph.

| ID | Provider and version | Required output | Consumer | Needed before | Satisfaction proof / integration responsibility |
|---|---|---|---|---|---|
| DIR-004/DEP-01 | [DIR-003](../DIR-003/direction.md) `2.1.1` | Result artifacts, normalized blocks, matrices and segment/finding references | DIR-004 | Acceptance of the relevant scenario | Document content. The owning milestone and its proof are selected at L2/L3. |
| DIR-004/DEP-02 | [DIR-002](../DIR-002/direction.md) `2.1.1` | Committed artifacts, readiness, data versions and lineage | DIR-004 | Acceptance of the relevant scenario | Safe publication and exact snapshots. The owning milestone and its proof are selected at L2/L3. |
| DIR-004/DEP-03 | [DIR-001](../DIR-001/direction.md) `2.1.1` | Policy, execution, schedules and collaboration ports | DIR-004 | Acceptance of the relevant scenario | Refresh, access and shared work. The owning milestone and its proof are selected at L2/L3. |

**Outputs supplied:**

- [DIR-005](../DIR-005/direction.md) `2.1.1`: Editing/read APIs, snapshot projections, refresh state and renderer.
- [DIR-006](../DIR-006/direction.md) `2.1.1`: Prepared serving path and coherent recovery set.
- [DIR-001](../DIR-001/direction.md) `2.1.1`: Versioned refresh demand and report-delivery events.

Each consumer proves integration with the provider-owned contract. The common
snapshot/refresh ownership allocation is in [MAP-001](../../project-map.md). Actual public
contract changes remain with their accepted context owners.

## Selected first product contribution — 2026-09-12

[WS-002](../DIR-004/workstreams/WS-002.md) `0.2.0` and
[MS-003](../../milestones/MS-003/plan.md) `0.2.0` now define the next first-report
accepted scope, with six prompts and one canonical journal. The owner accepted
WS-002/MS-003 0.2.0 on 2026-09-13; initial entry is recorded in that journal. This
contribution is implemented once in MS-003, not duplicated into another pack.

This is the decomposition parent for WS-002. C01/C02/C04 contribute the bounded draft composition, snapshot and chart path; publication, scheduled refresh, rich composition and delivery remain allocated to their later units.

## Next product continuation — 2026-09-17

[WS-003 — Configured metric workspace](workstreams/WS-003.md) `1.0.0` records
the accepted next bounded workstream under C01/C02/C04, using the owner-accepted initial
composition and existing report foundation. Its sequence is worksets/cards/context/
comparisons, then monitoring goals, then explicit shared worksets. Analytics owns
calculation contributions; Web owns the production interaction. The owner
confirmed this order and C01 scope on 2026-09-17. Detail C01 L3 next; goals and
shared-write policies remain open for their children. No new pack is initialized here.

## Owner decisions and next decomposition

| Decision ID | Decision or question | Authority / next condition | Effect |
|---|---|---|---|
| DIR-004/DEC-01 | This direction's L1 boundary and composition are accepted | Owner decision on 2026-09-06, recorded at [MAP-001 adoption](../../project-map.md) / MAP-001/DEC-05; version `1.0.0` | Settles L1 structure; does not accept an unwritten child plan. |
| DIR-004/DEC-02 | Previous WS-001-first selection | Historical MAP-001/DEC-06/07; next-selection priority superseded by MAP-001/DEC-10 on 2026-09-12 | Retain completed base and deferred scope; proposed product contributions are described above. |

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

MAP-001 2.1.1 registers this sequence draft at 2.1.1 with reciprocal draft
parent/provider links. Capability boundaries remain accepted at their earlier
basis; this draft does not change public/domain contracts or accept an unwritten
child. WS-001 navigation 1.0.10 keeps scope 1.0.0 and its recorded DIR-006 1.2.0
parent basis; its unimplemented C04–C06 remain allocated for later selection.
Completed milestones preserve exact historical plan/pack/journal/evidence bytes.
The map owns the proposed checkpoint order and records its validation.
