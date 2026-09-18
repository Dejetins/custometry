---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "direction",
  "doc_id": "DIR-001",
  "title": "Shared platform and execution control",
  "version": "2.1.1",
  "planning_status": "in_review",
  "language": "en",
  "parent_ref": {
    "id": "MAP-001",
    "path": "docs/architecture/planning/project-map.md",
    "version": "2.1.1"
  },
  "direction_ref": "DIR-001",
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
        "GOAL-009",
        "GOAL-014",
        "GOAL-015",
        "AUTH-001",
        "RBAC-019",
        "EXEC-STATE-001",
        "EXEC-DISPATCH-001",
        "EXEC-CANCEL-001",
        "SCHEDULE-001",
        "MATERIALIZE-001",
        "COLLAB-001",
        "WATCH-001",
        "NOTIFY-001",
        "API-001"
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
    "DIR-001/DEC-01",
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

# DIR-001. Shared platform and execution control

> L1 sequence draft `2.1.1`, 2026-09-17. Parent: [MAP-001](../../project-map.md) `2.1.1`.
> Accepted capability boundaries remain; WS-002 is the first-report foundation. WS-003 1.0.0 is the accepted metric-workspace continuation under DIR-004.
> The broader checkpoint sequence remains under review; WS-002/MS-003 0.2.0 was accepted on 2026-09-13.

## Intent and boundaries

**Expected outcome:** Users operate within their authorized workspaces, while jobs execute, cancel and recover through consistent shared rules.

| Field | Accepted L1 definition |
|---|---|
| Included | Authentication, sessions, users, organizations and access; the common run/pipeline engine, schedules, outbox, retry/cancellation and fencing; materialization planning, single-flight and resource lanes; participants, discussions, subscriptions, adoption and watches; operational notifications and audit; shared API and trusted-extension compatibility. |
| Excluded / adjacent ownership | Metric definitions and meaning, ingestion and physical artifact lifecycle belong to DIR-002; analytical algorithms and results to DIR-003; document composition and current snapshot to DIR-004; screens to DIR-005; installation and operational perimeter hardening to DIR-006. |
| Existing architecture owners | Identity & Workspace; Execution Control; Collaboration & Adoption; Notifications; Audit. Shared API conventions and the trusted Plugin SDK remain technical boundaries, not new domain contexts. |
| Main requirement areas | Machine sections 9, 14.2.1–14.2.2, 15.7–15.8, 16 and 20; corresponding human sections 9, 14, 16 and 20. |
| Observable direction completion | Protected consumers enforce current policy; real domain jobs use one execution mechanism; retries, revoke, crashes and event delivery preserve contracts. Collaboration and notifications satisfy their distinct privacy rules. |

Normative meaning remains in the [machine blueprint](../../../../../custometry-technical-blueprint-ru.md) and
[human mirror](../../../../../custometry-technical-blueprint-human-ru.md), version `0.11.0-draft`. The
[context map](../../../bounded-context-map.md) doc_version 13
defines ownership. Metadata pins the source commit. Selected `requirement_refs`
are anchors, not an exhaustive direction acceptance inventory.

## Known current state

Accepted W12/W13 reports describe local-auth and organization-policy kernels; W17 covers the privacy-safe People projection; W36/W38/W37 cover run control, terminal events and inbox. These are bounded historical proofs. They do not establish complete production integration, collaboration or reuse.

| Claim ID | Observation | Evidence | Limit / next resolution |
|---|---|---|---|
| DIR-001/EV-01 | `documented_only`: recorded previous results | [W12-IDENTITY-WORKSPACE-LOCAL-AUTH](../../../../../.codex/delivery/evidence/W12-IDENTITY-WORKSPACE-LOCAL-AUTH.md); [W13-ORGANIZATION-ACCESS-CORE](../../../../../.codex/delivery/evidence/W13-ORGANIZATION-ACCESS-CORE.md); [W17-PEOPLE-CONTRIBUTOR-ACTIVITY-PROJECTION](../../../../../.codex/delivery/evidence/W17-PEOPLE-CONTRIBUTOR-ACTIVITY-PROJECTION.md); [W36-EXECUTION-CONTROL-OPERATOR-API](../../../../../.codex/delivery/evidence/W36-EXECUTION-CONTROL-OPERATOR-API.md); [W38-EXECUTION-TERMINAL-NOTIFICATION-EVENT](../../../../../.codex/delivery/evidence/W38-EXECUTION-TERMINAL-NOTIFICATION-EVENT.md); [W37-INAPP-NOTIFICATION-INBOX-API](../../../../../.codex/delivery/evidence/W37-INAPP-NOTIFICATION-INBOX-API.md) | Historical reports were inspected; recheck applicability before implementation. |
| DIR-001/EV-02 | `code_observed`: bounded static inspection | [apps/api/src/custometry_api/main.py](../../../../../apps/api/src/custometry_api/main.py) | Only this entrypoint/contract was inspected; no complete direction audit is claimed. |
| DIR-001/EV-03 | `unknown`: complete direction readiness | No current exhaustive requirement-to-code-to-proof matrix | Resolve within the selected L2 investigation; do not assign a completion percentage. |

## Candidate L2 composition

These rows describe the accepted L1 scope at candidate workstream granularity.
The unselected rows are not accepted L2 plans. The selected first-block document
is referenced separately below. Other WS documents receive stable IDs, versions
and reciprocal parent links only after selection; no milestone is initialized here.

| Local candidate ID | Large task | Intended result | Existing base / dependency |
|---|---|---|---|
| DIR-001/C01 | Access and organization | Complete identity/workspace/policy lifecycle and revocation. | Reuse W12/W13; reconcile policy with every actual consumer. |
| DIR-001/C02 | Execution and extensions | One guided/pipeline path, attempts, cancellation, retries, schedules and trusted SDK. | Reuse W36/W38 and W15; reconcile composition without introducing a second engine. |
| DIR-001/C03 | Reuse and resources | Materialization planning, invalidation, single-flight, fairness and shared resource budgets. | Requirements exist; inspect implementation coverage separately. |
| DIR-001/C04 | Collaboration | Participants, discussions, subscriptions, usage/adoption and metric watches without employee ratings. | W17 proves only selected projections, not the complete lifecycle. |
| DIR-001/C05 | Notifications, audit and APIs | Safe shared contracts, inbox and supported operational channels. | Reuse W37; email/webhook and other boundaries require their own proof. |

The agent produces future selected documents with the owner; the owner is not
expected to supply them manually. Candidate presence is not entry readiness.

## Product-first sequence and contributions

Follow the proposed checkpoint order in [MAP-001 2.1.1](../../project-map.md#proposed-product-checkpoints).
Supply only the prepared identity/workspace, persistence and execution support
required by the early real product outcome. Full first-administrator onboarding,
member management, invitations and access-management UI follow the initial
analyst workflow; server-owned policy remains in force from the first consumer.
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
is an accepted initial design baseline; [WS-003 1.0.0](../DIR-004/workstreams/WS-003.md) records the accepted continuation.
MS-003 S05/S06 remain deferred in their canonical journal.
Capability boundaries and completed evidence remain unchanged.

## Relationships with other directions

These are interface relationships, not dependencies on completing an entire
direction. Future L2/L3 plans select actual provider milestones and acyclic hard
dependencies. Informational interactions do not create a cyclic execution graph.

| ID | Provider and version | Required output | Consumer | Needed before | Satisfaction proof / integration responsibility |
|---|---|---|---|---|---|
| DIR-001/DEP-01 | [DIR-002](../DIR-002/direction.md) `2.1.1` | Dataset versions, DQ/readiness and committed artifact references | DIR-001 | Acceptance of the relevant scenario | Domain data jobs and compatible reuse. The owning milestone and its proof are selected at L2/L3. |
| DIR-001/DEP-02 | [DIR-003](../DIR-003/direction.md) `2.1.1` | Domain specifications and calculation results | DIR-001 | Acceptance of the relevant scenario | Analytical jobs and watch evaluation. The owning milestone and its proof are selected at L2/L3. |
| DIR-001/DEP-03 | [DIR-004](../DIR-004/direction.md) `2.1.1` | Document refresh intent and publication policy | DIR-001 | Acceptance of the relevant scenario | Report preparation orchestration without owning its current pointer. The owning milestone and its proof are selected at L2/L3. |

**Outputs supplied:**

- [DIR-002](../DIR-002/direction.md) `2.1.1`: Policy decisions and execution protocol.
- [DIR-003](../DIR-003/direction.md) `2.1.1`: Policy, jobs, single-flight and resource admission.
- [DIR-004](../DIR-004/direction.md) `2.1.1`: Jobs, access, collaboration and operational events.
- [DIR-005](../DIR-005/direction.md) `2.1.1`: Safe API projections and actionable states.
- [DIR-006](../DIR-006/direction.md) `2.1.1`: Access/execution/event contracts and local failure/policy evidence.

Each consumer proves integration with the provider-owned contract. The common
snapshot/refresh ownership allocation is in [MAP-001](../../project-map.md). Actual public
contract changes remain with their accepted context owners.

## Selected first product contribution — 2026-09-12

[WS-002](../DIR-004/workstreams/WS-002.md) `0.2.0` and
[MS-003](../../milestones/MS-003/plan.md) `0.2.0` now define the next first-report
accepted scope, with six prompts and one canonical journal. The owner accepted
WS-002/MS-003 0.2.0 on 2026-09-13; initial entry is recorded in that journal. This
contribution is implemented once in MS-003, not duplicated into another pack.

S01 supplies the ordinary analyst/session and minimum policy seams; full admin, roles UI and scheduler work stay in their later selected product units.

## Owner decisions and next decomposition

| Decision ID | Decision or question | Authority / next condition | Effect |
|---|---|---|---|
| DIR-001/DEC-01 | This direction's L1 boundary and composition are accepted | Owner decision on 2026-09-06, recorded at [MAP-001 adoption](../../project-map.md) / MAP-001/DEC-05; version `1.0.0` | Settles L1 structure; does not accept an unwritten child plan. |
| DIR-001/DEC-02 | Previous WS-001-first selection | Historical MAP-001/DEC-06/07; next-selection priority superseded by MAP-001/DEC-10 on 2026-09-12 | Retain completed base and deferred scope; proposed product contributions are described above. |

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
