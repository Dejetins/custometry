---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "direction",
  "doc_id": "DIR-003",
  "title": "Analytics, segments and research",
  "version": "1.2.0",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "MAP-001",
    "path": "docs/architecture/planning/project-map.md",
    "version": "1.2.0"
  },
  "direction_ref": "DIR-003",
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
        "GOAL-003",
        "GOAL-006",
        "GOAL-011",
        "GOAL-013",
        "GOAL-016",
        "GOAL-018",
        "OUTLIER-001",
        "SEGMENT-029",
        "SEGMENT-034",
        "COMPARE-011",
        "PVM-001",
        "BLOCK-BUILDER-001",
        "PIVOT-001",
        "PARAM-001",
        "METHOD-001",
        "RESEARCH-001",
        "DIGITAL-001",
        "ATTRIBUTION-001",
        "UNIT-ECON-001",
        "PRODUCT-ANALYTICS-001"
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
    "DIR-003/DEC-01",
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

# DIR-003. Analytics, segments and research

> Accepted L1 scope and sequence links, version `1.2.0`, 2026-09-06. Parent: [MAP-001](../../project-map.md) `1.2.0`.
> MAP-001 records the owner-selected installation-first sequence and WS-001 entry. WS-001 1.0.0 now records the accepted M5/Linux, TLS, installation and first-account decisions.
> Detailed child acceptance, agent assignment and implementation remain separate decisions.

## Intent and boundaries

**Expected outcome:** Users obtain reproducible analytical results, reusable segments and research with explicit method limitations.

| Field | Accepted L1 definition |
|---|---|
| Included | Sales/customer/RFM/cohort/lifecycle; population treatment, relational/temporal segments and membership history; product/category/assortment/inventory, basket/store/channel, ABC/XYZ and discounts/PVM; normalized analytical blocks, matrices, parameters and comparisons; methods/cases/findings/products; digital journeys, attribution and unit economics; Promotion Journal; Forecasting as a retained held branch. |
| Excluded / adjacent ownership | Shared semantic input and ingestion belong to DIR-002; stored document layout/snapshots to DIR-004; editors to DIR-005; ordinary discussion comments to DIR-001. No activation, mass campaigns or automatic causal claims are added. |
| Existing architecture owners | Analytics; Methodology & Research; Digital Journey & Marketing Measurement; Promotion Journal; Forecasting. Digital remains a separate context; Products stays within Analytics. |
| Main requirement areas | Machine section 5 digital/promotion entities, section 6 methods/metrics, sections 12–13; corresponding human sections; analytical-authoring contract. |
| Observable direction completion | Selected methods satisfy semantic/golden and policy checks on declared inputs; report consumers receive identical values. Full direction completion includes forecasting obligations after separate hold resumption. |

Normative meaning remains in the [machine blueprint](../../../../../custometry-technical-blueprint-ru.md) and
[human mirror](../../../../../custometry-technical-blueprint-human-ru.md), version `0.11.0-draft`. The
[context map](../../../bounded-context-map.md) doc_version 13
defines ownership. Metadata pins the source commit. Selected `requirement_refs`
are anchors, not an exhaustive direction acceptance inventory.

## Known current state

W16 proves a bounded sales/customer/RFM result/API slice. Static source inspection found the analytics service and public result types. This does not prove the full builder, segmentation, product/digital analytics or Research. Forecasting remains on hold.

| Claim ID | Observation | Evidence | Limit / next resolution |
|---|---|---|---|
| DIR-003/EV-01 | `documented_only`: recorded previous results | [W16-SALES-CUSTOMER-RFM-API-PROJECTIONS](../../../../../.codex/delivery/evidence/W16-SALES-CUSTOMER-RFM-API-PROJECTIONS.md) | Historical reports were inspected; recheck applicability before implementation. |
| DIR-003/EV-02 | `code_observed`: bounded static inspection | [packages/analytics_core/application/service.py](../../../../../packages/analytics_core/application/service.py) | Only this entrypoint/contract was inspected; no complete direction audit is claimed. |
| DIR-003/EV-03 | `unknown`: complete direction readiness | No current exhaustive requirement-to-code-to-proof matrix | Resolve within the selected L2 investigation; do not assign a completion percentage. |

## Candidate L2 composition

These rows describe the accepted L1 scope at candidate workstream granularity.
The unselected rows are not accepted L2 plans. The selected first-block document
is referenced separately below. Other WS documents receive stable IDs, versions
and reciprocal parent links only after selection; no milestone is initialized here.

| Local candidate ID | Large task | Intended result | Existing base / dependency |
|---|---|---|---|
| DIR-003/C01 | Core analytical results | Sales/customer/RFM, cohorts/lifecycle and comparisons with correct totals and coverage. | Reuse W16; identify supported calculations and explicit unavailable states. |
| DIR-003/C02 | Populations and segments | Rules, related entities, collections/composition, membership/time, outliers and history. | Preserve adopted relational/temporal scope beyond flat customer predicates. |
| DIR-003/C03 | Products, sales and promotions | Product/category/inventory, basket/store/channel, discounts/PVM and descriptive promotion history. | DIR-002 owns hierarchy semantics; Analytics owns calculations. |
| DIR-003/C04 | Methods and research | Methods, Analysis Cases, findings/decisions and reusable AnalyticalProducts. | Research owns analytical meaning and consumes DIR-004 composition. |
| DIR-003/C05 | Digital and economics | Event/identity/cost contracts, journeys, funnels, attribution and unit economics. | Dedicated domain context; connector credentials remain DIR-002-owned. |
| DIR-003/C06 | Shared analytical builder | Normalized block specifications, pivot results/totals, parameters and compatible combinations. | One calculation contract serves every presentation profile. |
| DIR-003/C07 | Forecasting — on hold | Series/features, baselines, CatBoost, backtests, registry, intervals and monitoring. | Target coverage only; implementation detail and execution await explicit resumption. |

The agent produces future selected documents with the owner; the owner is not
expected to supply them manually. Candidate presence is not entry readiness.

## Accepted sequence and first-block relationship

Follow [MAP-001's accepted sequence](../../project-map.md#accepted-delivery-sequence)
`1.2.0`. The accepted starting document is [WS-001](../DIR-006/workstreams/WS-001.md) `1.0.0`, whose single
parent is DIR-006. Analysis and reusable segments follow usable-input publication at MAP-001/SEQ-08. No speculative analytical or forecast implementation is required to finish WS-001.

This is a contribution/reference, not a second decomposition parent. No duplicate
WS or parallel dispatch is created. Actual provider contributions are bounded
inside the selected workstream; later contracts are resolved before their consumers.

## Relationships with other directions

These are interface relationships, not dependencies on completing an entire
direction. Future L2/L3 plans select actual provider milestones and acyclic hard
dependencies. Informational interactions do not create a cyclic execution graph.

| ID | Provider and version | Required output | Consumer | Needed before | Satisfaction proof / integration responsibility |
|---|---|---|---|---|---|
| DIR-003/DEP-01 | [DIR-002](../DIR-002/direction.md) `1.2.0` | Semantic metrics, relationships, canonical inputs, coverage and manifests | DIR-003 | Acceptance of the relevant scenario | Correct computation and explainable limitations. The owning milestone and its proof are selected at L2/L3. |
| DIR-003/DEP-02 | [DIR-001](../DIR-001/direction.md) `1.2.0` | Authorization, canonical execution and reuse | DIR-003 | Acceptance of the relevant scenario | Execution and reproduction of analysis. The owning milestone and its proof are selected at L2/L3. |

**Outputs supplied:**

- [DIR-004](../DIR-004/direction.md) `1.2.0`: Typed immutable results, semantic keys, segment snapshots and method/finding projections.
- [DIR-005](../DIR-005/direction.md) `1.2.0`: Builder validation, preview, explanation and capabilities.
- [DIR-001](../DIR-001/direction.md) `1.2.0`: Metric/watch evaluations and domain specifications.
- [DIR-006](../DIR-006/direction.md) `1.2.0`: Reproducible specifications, golden expectations and method limitations.

Each consumer proves integration with the provider-owned contract. The common
snapshot/refresh ownership allocation is in [MAP-001](../../project-map.md). Actual public
contract changes remain with their accepted context owners.

## Owner decisions and next decomposition

| Decision ID | Decision or question | Authority / next condition | Effect |
|---|---|---|---|
| DIR-003/DEC-01 | This direction's L1 boundary and composition are accepted | Owner decision on 2026-09-06, recorded at [MAP-001 adoption](../../project-map.md) / MAP-001/DEC-05; version `1.0.0` | Settles L1 structure; does not accept an unwritten child plan. |
| DIR-003/DEC-02 | What is the next planning relationship? | Follow accepted MAP-001/DEC-06/07; WS-001 under DIR-006 is first. A separate child of this direction is not selected here | Contribute the declared prerequisites; select later owned L2 detail with the owner. |

Product exclusions, forecasting hold and XLSX sequencing in MAP-001 apply here.
No agent, calendar, worktree topology or parallel execution is assigned by this plan.

## History and document synchronization

| Version | Date | Change | Authority |
|---|---|---|---|
| 0.1.0 | 2026-09-06 | Russian owner-review draft | Initial draft request; historical authoring baseline |
| 1.0.0 | 2026-09-06 | L1 adopted in English; draft replaced; parent and interface versions synchronized | Owner acceptance and publication request; MAP-001/DEC-05 |
| 1.1.0 | 2026-09-06 | Apply accepted sequential priorities and first-block relationship; synchronize parent/provider versions; retain capability boundaries | Owner sequencing acceptance; MAP-001/DEC-06/07 |
| 1.2.0 | 2026-09-06 | Revalidate unchanged direction boundary and MAP/WS links against accepted WS-001 1.0.0 and amended requirement sources | Owner finalization instruction; substantive changes are owned by WS-001 |

MAP-001 registers this direction at `1.2.0`; metadata points back to that exact
parent version. Direction boundaries and existing ticket state remain unchanged;
the bounded installation/TLS/bootstrap requirement amendment is owned by WS-001 1.0.0.
Future edits update both sides of affected links. Publication/source checks and
their limits are recorded in MAP-001; no duplicate execution journal is created.
