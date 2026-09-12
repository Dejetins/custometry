---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "direction",
  "doc_id": "DIR-006",
  "title": "Operations, integration and system acceptance",
  "version": "2.0.2",
  "planning_status": "in_review",
  "language": "en",
  "parent_ref": {
    "id": "MAP-001",
    "path": "docs/architecture/planning/project-map.md",
    "version": "2.0.2"
  },
  "direction_ref": "DIR-006",
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
        "GOAL-007",
        "ARCH-PRINCIPLE-001",
        "SEC-001",
        "OPS-001",
        "OPS-009",
        "OPS-010",
        "TEST-INV-123",
        "TEST-INV-126",
        "COMPUTE-001",
        "SCALE-001",
        "REPORT-PERF-001",
        "REPORT-PERF-002",
        "V1-AC-068",
        "V1-AC-069",
        "V1-AC-070"
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
    "DIR-006/DEC-01",
    "MAP-001/DEC-06",
    "MAP-001/DEC-07",
    "DIR-006/DEC-02",
    "DIR-006/DEC-03",
    "MAP-001/DEC-09",
    "MAP-001/DEC-10",
    "MAP-001/DEC-11"
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

# DIR-006. Operations, integration and system acceptance

> L1 sequence draft `2.0.2`, 2026-09-12. Parent: [MAP-001](../../project-map.md) `2.0.2`.
> Accepted capability boundaries remain; the accepted next product L2 is WS-002, a working analyst report under DIR-004.
> The broader checkpoint sequence remains under review; WS-002/MS-003 0.2.0 was accepted on 2026-09-13.

## Intent and boundaries

**Expected outcome:** Custometry can be built and installed reproducibly on supported hardware, updated safely, observed and restored with verified end-to-end outcomes.

| Field | Accepted L1 definition |
|---|---|
| Included | Toolchain/CI/contract/documentation gates; Fast Loop/Hybrid/Full Stack/release environments; application/worker composition and migrations; single-server install/update/rollback; secrets/network hardening; observability; coordinated off-primary backup/restore; mixed-load/performance budgets; end-to-end qualification, runbooks and user documentation. |
| Excluded / adjacent ownership | Domain rules and feature-local tests stay with their owners. No automatic production deployment, SaaS/Kubernetes/multi-host expansion or invented hardware/SLO/RPO/RTO. External effects require current scoped authority. |
| Existing architecture owners | Composition roots, deployment/runtime boundaries, engineering tooling and release qualification. System integration/proof ownership does not create a new domain context. |
| Main requirement areas | Machine sections 18, 20–25, 26–28 and 30–32; corresponding human sections; runtime/network/tooling contracts. |
| Observable direction completion | The explicitly selected product scope has install/update, shared-runtime, required-security, agreed-load and backup/restore evidence. Missing criteria remain visible; one local green check never establishes a release label. |

Normative meaning remains in the [machine blueprint](../../../../../custometry-technical-blueprint-ru.md) and
[human mirror](../../../../../custometry-technical-blueprint-human-ru.md), version `0.11.0-draft`. The
[context map](../../../bounded-context-map.md) doc_version 13
defines ownership. Metadata pins the source commit. Selected `requirement_refs`
are anchors, not an exhaustive direction acceptance inventory.

## Known current state

W11 provides local Hybrid lifecycle evidence. Tooling contracts, runtime sources and test/CI infrastructure exist. The initial L1 inspection did not repeat runtime/CI checks or establish release, off-primary restore or 50+100 mixed-load readiness. Publication checks are separately recorded in MAP-001.

| Claim ID | Observation | Evidence | Limit / next resolution |
|---|---|---|---|
| DIR-006/EV-01 | `documented_only`: recorded previous results | [W11-HYBRID-DEVELOPMENT-RUNTIME](../../../../../.codex/delivery/evidence/W11-HYBRID-DEVELOPMENT-RUNTIME.md) | Historical reports were inspected; recheck applicability before implementation. |
| DIR-006/EV-02 | `code_observed`: bounded static inspection | [apps/api/src/custometry_api/main.py](../../../../../apps/api/src/custometry_api/main.py) | Only this entrypoint/contract was inspected; no complete direction audit is claimed. |
| DIR-006/EV-03 | `unknown`: complete direction readiness | No current exhaustive requirement-to-code-to-proof matrix | Resolve within the selected L2 investigation; do not assign a completion percentage. |
| DIR-006/EV-04 | `boundary_verified`: C02/C03 closure, read 2026-09-11 | [MS-001 journal](../../../../../.codex/delivery/ledgers/MS-001.md), [MS-002 journal](../../../../../.codex/delivery/ledgers/MS-002.md), [C04 handoff](../../../../../.codex/delivery/evidence/MS-002/MS-002-S05/report.md) | Preserve final owner-accepted target/resource limits; no C04 or complete update/recovery proof is transferred. |

## Candidate L2 composition

These rows describe the accepted L1 scope at candidate workstream granularity.
The unselected rows are not accepted L2 plans. The selected first-block document
is referenced separately below. Other WS documents receive stable IDs, versions
and reciprocal parent links only after selection; no milestone is initialized here.

| Local candidate ID | Large task | Intended result | Existing base / dependency |
|---|---|---|---|
| DIR-006/C01 | Development environment and integration | One reproducible combined build with real adapters and compatible contracts. | Reuse W11 and tooling; prove the actual combined build. |
| DIR-006/C02 | Installation and update | Single-server topology, configuration, migrations and compatible update/rollback. | Runtime/network sources constrain this work; this plan selects no deployment target. |
| DIR-006/C03 | Security and observability | Secrets, network/egress proof, audit/logging, health, metrics and incident runbooks. | Domain authorization stays with DIR-001 and its consumers. |
| DIR-006/C04 | Backup and recovery | Admin schedule/timezone/destination/retention, reference closure, keys and exact snapshots. | OPS-009/010 and V1-AC-070; off-primary backup does not alter primary storage. |
| DIR-006/C05 | Performance and resources | Cold/warm ready-open, page/filter latency, background refresh and 50+100 mixed load. | Agree budgets, hardware and corpus before acceptance; no values invented here. |
| DIR-006/C06 | Integrated acceptance and documentation | User journeys, failure/revoke/restart scenarios, qualification and operational/user docs. | Each direction supplies local evidence; DIR-006 verifies combined behavior. |

The agent produces future selected documents with the owner; the owner is not
expected to supply them manually. Candidate presence is not entry readiness.

## Retained installation workstream

| Child ID + path + version | Intended outcome | Parent allocation | Contributions and next action |
|---|---|---|---|
| [WS-001. Installable platform and first administrator bootstrap](workstreams/WS-001.md) `1.0.10` | Versioned delivery -> installation -> first administrator/workspace -> protected Web access and restart persistence | Bounded first portion of DIR-006/C01/C02/C03/C06; later updates, whole-system backup and load acceptance remain allocated separately | DIR-001 Identity and DIR-005 Web contribute within one canonical workstream. Accepted L2 scope 1.0.0 fixes five sequential outcomes; navigation 1.0.10 retains completed C02/C03 evidence and defers full C04–C06 until after the initial analyst workflow |

The owner selected this block in MAP-001/DEC-07. The L2 scope is accepted;
unwritten C04–C06 child plans retain their owner checkpoints. DIR-006 owns installed integration and closure;
the domain/client owners retain their contracts. The registry is a scope/link
table, not a second workstream-status source.

## Product-first sequence and contributions

Follow the proposed checkpoint order in [MAP-001 2.0.2](../../project-map.md#proposed-product-checkpoints).
Reuse the completed supply/installation base while product outcomes are built.
Provide changed-runtime and packaged proof without introducing a new full-install
prerequisite for each feature. Remaining WS-001/C04–C06 and broader administration/
operation qualification follow the selected analyst workflow.

## Development cadence for this direction

Follow [MAP-001 2.0.2 draft](../../project-map.md#development-and-delivery-cadence).
Maintain the reusable build/installation base as feature contents evolve.
Provide scoped runtime and delivery proof at the selected boundaries; full target
campaigns are not default prerequisites for each local edit or unrelated feature.
Use existing L2/L3 fields for the local, packaged and delivery proof allocation.
Development cadence remains accepted; this draft changes priority and next-L2
selection. Original scope evidence remains historical.

## Relationships with other directions

These are interface relationships, not dependencies on completing an entire
direction. Future L2/L3 plans select actual provider milestones and acyclic hard
dependencies. Informational interactions do not create a cyclic execution graph.

| ID | Provider and version | Required output | Consumer | Needed before | Satisfaction proof / integration responsibility |
|---|---|---|---|---|---|
| DIR-006/DEP-01 | [DIR-001](../DIR-001/direction.md) `2.0.2` | Real execution/access processes and operational projections | DIR-006 | Acceptance of the relevant scenario | Whole-system failure/recovery/load checks. The owning milestone and its proof are selected at L2/L3. |
| DIR-006/DEP-02 | [DIR-002](../DIR-002/direction.md) `2.0.2` | Storage durability and coherent backup input set | DIR-006 | Acceptance of the relevant scenario | Restore integrity and source refresh. The owning milestone and its proof are selected at L2/L3. |
| DIR-006/DEP-03 | [DIR-003](../DIR-003/direction.md) `2.0.2` | Reproducible calculations and golden expectations | DIR-006 | Acceptance of the relevant scenario | Semantic scenario acceptance. The owning milestone and its proof are selected at L2/L3. |
| DIR-006/DEP-04 | [DIR-004](../DIR-004/direction.md) `2.0.2` | Exact snapshots and prepared serving | DIR-006 | Acceptance of the relevant scenario | Ready-open, refresh and restore checks. The owning milestone and its proof are selected at L2/L3. |
| DIR-006/DEP-05 | [DIR-005](../DIR-005/direction.md) `2.0.2` | Real browser journeys | DIR-006 | Acceptance of the relevant scenario | Complete user-outcome verification. The owning milestone and its proof are selected at L2/L3. |

**Outputs supplied:**

- [DIR-001](../DIR-001/direction.md) `2.0.2`: Supported environment and resource-policy inputs.
- [DIR-002](../DIR-002/direction.md) `2.0.2`: Storage/recovery/environment constraints.
- [DIR-003](../DIR-003/direction.md) `2.0.2`: Reproducible test/runtime environment.
- [DIR-004](../DIR-004/direction.md) `2.0.2`: Observed performance and recovery results.
- [DIR-005](../DIR-005/direction.md) `2.0.2`: Verified combined build and UI runtime constraints.

Each consumer proves integration with the provider-owned contract. The common
snapshot/refresh ownership allocation is in [MAP-001](../../project-map.md). Actual public
contract changes remain with their accepted context owners.

## Selected first product contribution — 2026-09-12

[WS-002](../DIR-004/workstreams/WS-002.md) `0.2.0` and
[MS-003](../../milestones/MS-003/plan.md) `0.2.0` now define the next first-report
accepted scope, with six prompts and one canonical journal. The owner accepted
WS-002/MS-003 0.2.0 on 2026-09-13; initial entry is recorded in that journal. This
contribution is implemented once in MS-003, not duplicated into another pack.

S05 integrates the first product feature using the existing producer/installer and native M5 candidate. Preserve MS-001/MS-002 historical proof and WS-001 C04–C06 deferrals; do not repeat the full VM/LAN installation campaign for ordinary feature edits.

## Owner decisions and next decomposition

| Decision ID | Decision or question | Authority / next condition | Effect |
|---|---|---|---|
| DIR-006/DEC-01 | This direction's L1 boundary and composition are accepted | Owner decision on 2026-09-06, recorded at [MAP-001 adoption](../../project-map.md) / MAP-001/DEC-05; version `1.0.0` | Settles L1 structure; does not accept an unwritten child plan. |
| DIR-006/DEC-02 | Develop delivery, installation and first administrator bootstrap first | Owner selected WS-001 on 2026-09-06; MAP-001/DEC-07 | Historical first-draft selection; DIR-006/DEC-03 now accepts WS-001 1.0.0. Unwritten L3 plans and implementation remain separate. |
| DIR-006/DEC-03 | Accept WS-001 1.0.0 and its five sequential milestone outcomes | Owner accepted six proposals with M5 Max/36 GB and Linux VM correction on 2026-09-06 | C02 was selected first; current child planning follows the WS-001 registry. No product execution is selected by this L1 record. |

Product exclusions, forecasting hold and XLSX sequencing in MAP-001 apply here.
No agent, calendar, worktree topology or parallel execution is assigned by this plan.

## History and document synchronization

| Version | Date | Change | Authority |
|---|---|---|---|
| 0.1.0 | 2026-09-06 | Russian owner-review draft | Initial draft request; historical authoring baseline |
| 1.0.0 | 2026-09-06 | L1 adopted in English; draft replaced; parent and interface versions synchronized | Owner acceptance and publication request; MAP-001/DEC-05 |
| 1.1.0 | 2026-09-06 | Apply accepted sequential priorities and first-block relationship; synchronize parent/provider versions; retain capability boundaries | Owner sequencing acceptance; MAP-001/DEC-06/07 |
| 1.2.0 | 2026-09-06 | Revalidate unchanged direction boundary and MAP/WS links against accepted WS-001 1.0.0 and amended requirement sources | Owner finalization instruction; substantive changes are owned by WS-001 |
| 1.2.1 | 2026-09-10 | Refresh child-planning navigation to WS-001 1.0.7 and C03/MS-002 1.0.0; L1 boundary unchanged | Owner requested next iteration; delegated editorial synchronization |
| 1.3.0 | 2026-09-11 | Apply MAP-001 development cadence and synchronize reciprocal parent/provider links; preserve capability boundaries and closed milestone evidence | Owner accepted approach and requested general planning amendment; MAP-001/DEC-09 |
| 2.0.0 | 2026-09-12 | Draft product-first ordering and analyst-report L2 contributions; retain accepted scope | Owner priority correction, MAP-001/DEC-10; detailed sequence under review |
| 2.0.1 | 2026-09-12 | Register WS-002/MS-003 review candidates and exact first-product contributions; synchronize navigation | Owner requested documentation, prompts and journal; MAP-001/DEC-11 |
| 2.0.2 | 2026-09-12 | Refresh reciprocal navigation for WS-002/MS-003 0.2.0; L1 scope and checkpoint order unchanged | Owner requires Customer and Product data in the selected child; editorial reference maintenance |

MAP-001 2.0.2 registers this sequence draft at 2.0.2 with reciprocal draft
parent/provider links. Capability boundaries remain accepted at their earlier
basis; this draft does not change public/domain contracts or accept an unwritten
child. WS-001 navigation 1.0.10 keeps scope 1.0.0 and its recorded DIR-006 1.2.0
parent basis; its unimplemented C04–C06 remain allocated for later selection.
Completed milestones preserve exact historical plan/pack/journal/evidence bytes.
The map owns the proposed checkpoint order and records its validation.
