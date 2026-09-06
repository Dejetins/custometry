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
  "version": "1.1.0",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "MAP-001",
    "path": "docs/architecture/planning/project-map.md",
    "version": "1.1.0"
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
      "revision": "5a963ab0166bfa44d508679dcafa29723bbeb68b",
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

# DIR-001. Shared platform and execution control

> Accepted L1 scope and sequence links, version `1.1.0`, 2026-09-06. Parent: [MAP-001](../../project-map.md) `1.1.0`.
> MAP-001 records the owner-selected installation-first sequence and WS-001 entry.
> Detailed child acceptance, agent assignment and implementation remain separate decisions.

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
[human mirror](../../../../../custometry-technical-blueprint-human-ru.md), version `0.10.0-draft`. The
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

## Accepted sequence and first-block relationship

Follow [MAP-001's accepted sequence](../../project-map.md#accepted-delivery-sequence)
`1.1.0`. The selected starting document is [WS-001](../DIR-006/workstreams/WS-001.md) `0.1.0`, whose single
parent is DIR-006. Provide first-administrator bootstrap, principal/workspace and session/policy contracts inside WS-001. Full member/role administration follows at MAP-001/SEQ-04.

This is a contribution/reference, not a second decomposition parent. No duplicate
WS or parallel dispatch is created. Actual provider contributions are bounded
inside the selected workstream; later contracts are resolved before their consumers.

## Relationships with other directions

These are interface relationships, not dependencies on completing an entire
direction. Future L2/L3 plans select actual provider milestones and acyclic hard
dependencies. Informational interactions do not create a cyclic execution graph.

| ID | Provider and version | Required output | Consumer | Needed before | Satisfaction proof / integration responsibility |
|---|---|---|---|---|---|
| DIR-001/DEP-01 | [DIR-002](../DIR-002/direction.md) `1.1.0` | Dataset versions, DQ/readiness and committed artifact references | DIR-001 | Acceptance of the relevant scenario | Domain data jobs and compatible reuse. The owning milestone and its proof are selected at L2/L3. |
| DIR-001/DEP-02 | [DIR-003](../DIR-003/direction.md) `1.1.0` | Domain specifications and calculation results | DIR-001 | Acceptance of the relevant scenario | Analytical jobs and watch evaluation. The owning milestone and its proof are selected at L2/L3. |
| DIR-001/DEP-03 | [DIR-004](../DIR-004/direction.md) `1.1.0` | Document refresh intent and publication policy | DIR-001 | Acceptance of the relevant scenario | Report preparation orchestration without owning its current pointer. The owning milestone and its proof are selected at L2/L3. |

**Outputs supplied:**

- [DIR-002](../DIR-002/direction.md) `1.1.0`: Policy decisions and execution protocol.
- [DIR-003](../DIR-003/direction.md) `1.1.0`: Policy, jobs, single-flight and resource admission.
- [DIR-004](../DIR-004/direction.md) `1.1.0`: Jobs, access, collaboration and operational events.
- [DIR-005](../DIR-005/direction.md) `1.1.0`: Safe API projections and actionable states.
- [DIR-006](../DIR-006/direction.md) `1.1.0`: Access/execution/event contracts and local failure/policy evidence.

Each consumer proves integration with the provider-owned contract. The common
snapshot/refresh ownership allocation is in [MAP-001](../../project-map.md). Actual public
contract changes remain with their accepted context owners.

## Owner decisions and next decomposition

| Decision ID | Decision or question | Authority / next condition | Effect |
|---|---|---|---|
| DIR-001/DEC-01 | This direction's L1 boundary and composition are accepted | Owner decision on 2026-09-06, recorded at [MAP-001 adoption](../../project-map.md) / MAP-001/DEC-05; version `1.0.0` | Settles L1 structure; does not accept an unwritten child plan. |
| DIR-001/DEC-02 | What is the next planning relationship? | Follow accepted MAP-001/DEC-06/07; WS-001 under DIR-006 is first. A separate child of this direction is not selected here | Contribute the declared prerequisites; select later owned L2 detail with the owner. |

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
