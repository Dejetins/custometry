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
  "version": "1.1.0",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "MAP-001",
    "path": "docs/architecture/planning/project-map.md",
    "version": "1.1.0"
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
      "revision": "5a963ab0166bfa44d508679dcafa29723bbeb68b",
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
    "DIR-006/DEC-02"
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

> Accepted L1 scope and sequence links, version `1.1.0`, 2026-09-06. Parent: [MAP-001](../../project-map.md) `1.1.0`.
> MAP-001 records the owner-selected installation-first sequence and WS-001 entry.
> Detailed child acceptance, agent assignment and implementation remain separate decisions.

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
[human mirror](../../../../../custometry-technical-blueprint-human-ru.md), version `0.10.0-draft`. The
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

## Selected first workstream

| Child ID + path + version | Intended outcome | Parent allocation | Contributions and next action |
|---|---|---|---|
| [WS-001. Installable platform and first administrator bootstrap](workstreams/WS-001.md) `0.1.0` | Versioned delivery -> installation -> first administrator/workspace -> protected Web access and restart persistence | Bounded first portion of DIR-006/C01/C02/C03/C06; later updates, whole-system backup and load acceptance remain allocated separately | DIR-001 Identity and DIR-005 Web contribute within one canonical workstream. Develop this L2 draft with the owner before selecting L3 children |

The owner selected this block in MAP-001/DEC-07. Selection does not accept the new
WS draft's candidate milestones. DIR-006 owns installed integration and closure;
the domain/client owners retain their contracts. The registry is a scope/link
table, not a second workstream-status source.

## Relationships with other directions

These are interface relationships, not dependencies on completing an entire
direction. Future L2/L3 plans select actual provider milestones and acyclic hard
dependencies. Informational interactions do not create a cyclic execution graph.

| ID | Provider and version | Required output | Consumer | Needed before | Satisfaction proof / integration responsibility |
|---|---|---|---|---|---|
| DIR-006/DEP-01 | [DIR-001](../DIR-001/direction.md) `1.1.0` | Real execution/access processes and operational projections | DIR-006 | Acceptance of the relevant scenario | Whole-system failure/recovery/load checks. The owning milestone and its proof are selected at L2/L3. |
| DIR-006/DEP-02 | [DIR-002](../DIR-002/direction.md) `1.1.0` | Storage durability and coherent backup input set | DIR-006 | Acceptance of the relevant scenario | Restore integrity and source refresh. The owning milestone and its proof are selected at L2/L3. |
| DIR-006/DEP-03 | [DIR-003](../DIR-003/direction.md) `1.1.0` | Reproducible calculations and golden expectations | DIR-006 | Acceptance of the relevant scenario | Semantic scenario acceptance. The owning milestone and its proof are selected at L2/L3. |
| DIR-006/DEP-04 | [DIR-004](../DIR-004/direction.md) `1.1.0` | Exact snapshots and prepared serving | DIR-006 | Acceptance of the relevant scenario | Ready-open, refresh and restore checks. The owning milestone and its proof are selected at L2/L3. |
| DIR-006/DEP-05 | [DIR-005](../DIR-005/direction.md) `1.1.0` | Real browser journeys | DIR-006 | Acceptance of the relevant scenario | Complete user-outcome verification. The owning milestone and its proof are selected at L2/L3. |

**Outputs supplied:**

- [DIR-001](../DIR-001/direction.md) `1.1.0`: Supported environment and resource-policy inputs.
- [DIR-002](../DIR-002/direction.md) `1.1.0`: Storage/recovery/environment constraints.
- [DIR-003](../DIR-003/direction.md) `1.1.0`: Reproducible test/runtime environment.
- [DIR-004](../DIR-004/direction.md) `1.1.0`: Observed performance and recovery results.
- [DIR-005](../DIR-005/direction.md) `1.1.0`: Verified combined build and UI runtime constraints.

Each consumer proves integration with the provider-owned contract. The common
snapshot/refresh ownership allocation is in [MAP-001](../../project-map.md). Actual public
contract changes remain with their accepted context owners.

## Owner decisions and next decomposition

| Decision ID | Decision or question | Authority / next condition | Effect |
|---|---|---|---|
| DIR-006/DEC-01 | This direction's L1 boundary and composition are accepted | Owner decision on 2026-09-06, recorded at [MAP-001 adoption](../../project-map.md) / MAP-001/DEC-05; version `1.0.0` | Settles L1 structure; does not accept an unwritten child plan. |
| DIR-006/DEC-02 | Develop delivery, installation and first administrator bootstrap first | Owner selected WS-001 on 2026-09-06; MAP-001/DEC-07 | Authorizes the first L2 draft and its discussion, not acceptance of candidate L3 children or implementation. |

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
