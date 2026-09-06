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
  "version": "1.0.0",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "MAP-001",
    "path": "docs/architecture/planning/project-map.md",
    "version": "1.0.0"
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
      "revision": "5a963ab0166bfa44d508679dcafa29723bbeb68b",
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
    }
  ],
  "decision_refs": [
    "FRAME/DEC-01",
    "FRAME/DEC-03",
    "FRAME/DEC-06",
    "MAP-001/DEC-01",
    "MAP-001/DEC-02",
    "MAP-001/DEC-05",
    "DIR-004/DEC-01"
  ],
  "supersedes_ref": null,
  "proof_boundary": {
    "label": "accepted-level-1-planning-boundaries",
    "exclusions": [
      "workstream-selection",
      "exhaustive-code-audit",
      "runtime-readiness",
      "implementation-authority"
    ]
  }
}
---

# DIR-004. Analytical documents and result delivery

> Accepted L1 scope, version `1.0.0`, 2026-09-06. Parent: [MAP-001](../../project-map.md) `1.0.0`.
> The owner accepted the six-direction structure and requested English adoption and publication.
> L2 selection, milestone acceptance, agent assignment and implementation remain separate decisions.

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
[human mirror](../../../../../custometry-technical-blueprint-human-ru.md), version `0.10.0-draft`. The
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
They are not accepted L2 plans or a selected execution order. After owner selection,
create the chosen WS document with stable ID, version, real path and reciprocal
parent link. No WS file, milestone or executable promise is initialized here.

| Local candidate ID | Large task | Intended result | Existing base / dependency |
|---|---|---|---|
| DIR-004/C01 | Document and publication | Common Dashboard/Workbook/Research model, stable blocks/pages and immutable snapshots. | Reuse accepted contracts while preserving content/presentation ownership. |
| DIR-004/C02 | Authoring, bindings and history | Filter/parameter bindings, notes/annotations, personal views, exact anchors and semantic diff. | Metric definitions come from DIR-002; analytical calculations and results from DIR-003; discussions from DIR-001. |
| DIR-004/C03 | Refresh and prepared results | after_ingestion/scheduled/manual, waiting_for_data, coalescing, atomic current and last-good. | REPORT-REFRESH-001..007; an open viewer applies updates explicitly. |
| DIR-004/C04 | Rendering and branding | One ChartSpec compiler, Web/static parity, BrandProfile and CompanyPack. | No renderer recomputes business values; render identity is versioned. |
| DIR-004/C05 | Delivery and exports | Exact-snapshot operations, report email policy/reconciliation and shared export adapters. | Report email remains separate from operational notifications. |
| DIR-004/C06 | Universal XLSX — late phase | One workbook renderer over stable ReportSnapshot. | Preserve its position as the final new functional v1 increment. |

The next authorized planning step produces those future documents; the owner is
not expected to supply them manually. Candidate presence is not entry readiness.

## Relationships with other directions

These are interface relationships, not dependencies on completing an entire
direction. Future L2/L3 plans select actual provider milestones and acyclic hard
dependencies. Informational interactions do not create a cyclic execution graph.

| ID | Provider and version | Required output | Consumer | Needed before | Satisfaction proof / integration responsibility |
|---|---|---|---|---|---|
| DIR-004/DEP-01 | [DIR-003](../DIR-003/direction.md) `1.0.0` | Result artifacts, normalized blocks, matrices and segment/finding references | DIR-004 | Acceptance of the relevant scenario | Document content. The owning milestone and its proof are selected at L2/L3. |
| DIR-004/DEP-02 | [DIR-002](../DIR-002/direction.md) `1.0.0` | Committed artifacts, readiness, data versions and lineage | DIR-004 | Acceptance of the relevant scenario | Safe publication and exact snapshots. The owning milestone and its proof are selected at L2/L3. |
| DIR-004/DEP-03 | [DIR-001](../DIR-001/direction.md) `1.0.0` | Policy, execution, schedules and collaboration ports | DIR-004 | Acceptance of the relevant scenario | Refresh, access and shared work. The owning milestone and its proof are selected at L2/L3. |

**Outputs supplied:**

- [DIR-005](../DIR-005/direction.md) `1.0.0`: Editing/read APIs, snapshot projections, refresh state and renderer.
- [DIR-006](../DIR-006/direction.md) `1.0.0`: Prepared serving path and coherent recovery set.
- [DIR-001](../DIR-001/direction.md) `1.0.0`: Versioned refresh demand and report-delivery events.

Each consumer proves integration with the provider-owned contract. The common
snapshot/refresh ownership allocation is in [MAP-001](../../project-map.md). Actual public
contract changes remain with their accepted context owners.

## Owner decisions and next decomposition

| Decision ID | Decision or question | Authority / next condition | Effect |
|---|---|---|---|
| DIR-004/DEC-01 | This direction's L1 boundary and composition are accepted | Owner decision on 2026-09-06, recorded at [MAP-001 adoption](../../project-map.md) / MAP-001/DEC-05; version `1.0.0` | Settles L1 structure; does not accept an unwritten child plan. |
| DIR-004/DEC-02 | Which large task is detailed first? | Not selected; owner chooses the next branch | Blocks selecting an L2 planning unit, not publication of this accepted L1. |

Product exclusions, forecasting hold and XLSX sequencing in MAP-001 apply here.
No agent, calendar, worktree topology or parallel execution is assigned by this plan.

## History and document synchronization

| Version | Date | Change | Authority |
|---|---|---|---|
| 0.1.0 | 2026-09-06 | Russian owner-review draft | Initial draft request; historical authoring baseline |
| 1.0.0 | 2026-09-06 | L1 adopted in English; draft replaced; parent and interface versions synchronized | Owner acceptance and publication request; MAP-001/DEC-05 |

MAP-001 registers this direction at `1.0.0`; metadata points back to that exact
parent version. Requirements, architecture and existing ticket state are unchanged.
Future edits update both sides of affected links. Publication/source checks and
their limits are recorded in MAP-001; no duplicate execution journal is created.
