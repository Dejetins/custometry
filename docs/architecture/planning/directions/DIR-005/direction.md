---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "direction",
  "doc_id": "DIR-005",
  "title": "Web interface and user journeys",
  "version": "2.0.2",
  "planning_status": "in_review",
  "language": "en",
  "parent_ref": {
    "id": "MAP-001",
    "path": "docs/architecture/planning/project-map.md",
    "version": "2.0.2"
  },
  "direction_ref": "DIR-005",
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
        "GOAL-010",
        "UI-SHELL-001",
        "UI-DENSITY-001",
        "ROUTE-001",
        "FOCUS-001",
        "THEME-001",
        "I18N-001",
        "A11Y-001",
        "MOTION-001",
        "SYS-UI-001",
        "HELP-001",
        "WEB-ARCH-001",
        "WEB-PERF-001",
        "REPORT-REFRESH-007",
        "DATA-MAP-007"
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
    "DIR-005/DEC-01",
    "MAP-001/DEC-06",
    "MAP-001/DEC-07",
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

# DIR-005. Web interface and user journeys

> L1 sequence draft `2.0.2`, 2026-09-12. Parent: [MAP-001](../../project-map.md) `2.0.2`.
> Accepted capability boundaries remain; the accepted next product L2 is WS-002, a working analyst report under DIR-004.
> The broader checkpoint sequence remains under review; WS-002/MS-003 0.2.0 was accepted on 2026-09-13.

## Intent and boundaries

**Expected outcome:** Each role completes its work through an accessible RU/EN interface with real APIs, truthful states and actionable recovery.

| Field | Accepted L1 definition |
|---|---|
| Included | Shell/navigation/workspace/history; components/tokens/themes, RU/EN, keyboard/accessibility/responsive Web; auth/org/admin; source/mapping/DQ/Data Guide; analytics/segments/research; compact composer, reader/Focus and controls; collaboration/inbox/operators; branding/help/system surfaces; safe API integration and error/retry/empty/stale behavior. |
| Excluded / adjacent ownership | No browser-owned business calculations or independent authorization policy. No alternative design program, live Figma/Penpot or newly authorized mobile-specific IA/composition. Forecast UI follows the forecasting hold. |
| Existing architecture owners | apps/web, ui-foundation, localization and client adapters; ADR-0007 defines frontend architecture. UI does not own server-domain business rules. |
| Main requirement areas | Technical sections 15 and 18.6; UI blueprint at navigation/family scope; human section 15; target-pilot README/manifest and ADR-0007. |
| Observable direction completion | Selected families, roles, states and journeys are proven in a real browser at their required API/data boundaries, retaining target-pilot decisions, RU/EN, keyboard, responsive and recovery semantics. Screen count alone is not completion evidence. |

Normative meaning remains in the [machine blueprint](../../../../../custometry-technical-blueprint-ru.md) and
[human mirror](../../../../../custometry-technical-blueprint-human-ru.md), version `0.11.0-draft`. The
[context map](../../../bounded-context-map.md) doc_version 13
defines ownership. Metadata pins the source commit. Selected `requirement_refs`
are anchors, not an exhaustive direction acceptance inventory.

## Known current state

The final target pilot is preserved. W31–W35 describe a production shell and bounded sales/connections/runs/inbox routes. W32 includes real W16/API/PostgreSQL integration and explicit unavailable analytical functions. Complete screen coverage and pilot conformance remain unproven.

| Claim ID | Observation | Evidence | Limit / next resolution |
|---|---|---|---|
| DIR-005/EV-01 | `documented_only`: recorded previous results | [W31-WEB-PRODUCTION-SHELL-ROUTING](../../../../../.codex/delivery/evidence/W31-WEB-PRODUCTION-SHELL-ROUTING.md); [W32-WEB-SALES-OVERVIEW](../../../../../.codex/delivery/evidence/W32-WEB-SALES-OVERVIEW.md); [W33-WEB-CONNECTIONS](../../../../../.codex/delivery/evidence/W33-WEB-CONNECTIONS.md); [W34-WEB-OPERATOR-RUNS](../../../../../.codex/delivery/evidence/W34-WEB-OPERATOR-RUNS.md); [W35-WEB-NOTIFICATION-INBOX](../../../../../.codex/delivery/evidence/W35-WEB-NOTIFICATION-INBOX.md) | Historical reports were inspected; recheck applicability before implementation. |
| DIR-005/EV-02 | `code_observed`: bounded static inspection | [apps/web/src/features/analytics-sales/analytics-sales-api.ts](../../../../../apps/web/src/features/analytics-sales/analytics-sales-api.ts) | Only this entrypoint/contract was inspected; no complete direction audit is claimed. |
| DIR-005/EV-03 | `unknown`: complete direction readiness | No current exhaustive requirement-to-code-to-proof matrix | Resolve within the selected L2 investigation; do not assign a completion percentage. |

## Candidate L2 composition

These rows describe the accepted L1 scope at candidate workstream granularity.
The unselected rows are not accepted L2 plans. The selected first-block document
is referenced separately below. Other WS documents receive stable IDs, versions
and reciprocal parent links only after selection; no milestone is initialized here.

| Local candidate ID | Large task | Intended result | Existing base / dependency |
|---|---|---|---|
| DIR-005/C01 | Shared Web platform | Shell, routing/history, access adapters, foundation, themes, RU/EN and accessibility. | Reuse W31; verify runtime conformance to the current target pilot. |
| DIR-005/C02 | Access and administration | Authentication, workspaces, organization/people, permissions and administration. | API kernels exist; complete UI journeys still need verification. |
| DIR-005/C03 | Data onboarding and understanding | Connections, import, mapping preview, DQ/remediation and Data Guide. | Reuse W33; a connection list alone does not prove source-to-usable-data behavior. |
| DIR-005/C04 | Analytical work | Sales/product/digital, segments, methods, Research and explanations. | Reuse W32; complex filters and matrices consume DIR-003 providers. |
| DIR-005/C05 | Document interaction | Compact composer, tabs, inspector, reader/Focus, snapshots, refresh and delivery UI. | Preserve demonstrated pilot decisions; resolve missing states with the owner. |
| DIR-005/C06 | Operations and communication | Runs, schedules, inbox, discussions/adoption, backup UI, help/system journeys. | Reuse W34/W35; a UI command does not prove backup or external email effects. |

The agent produces future selected documents with the owner; the owner is not
expected to supply them manually. Candidate presence is not entry readiness.

## Product-first sequence and contributions

Follow the proposed checkpoint order in [MAP-001 2.0.2](../../project-map.md#proposed-product-checkpoints).
Build the analyst-facing workspace and report interactions from the accepted
pilot alongside real API/persistence. Data setup and analytical controls expand
through usable checkpoints. Full onboarding, people, roles and administration
screens follow the initial analyst workflow; retain truthful states throughout.
The existing [WS-001](../DIR-006/workstreams/WS-001.md) `1.0.10` retains its
accepted scope and completed evidence, but full C04–C06 is no longer the next
universal prerequisite. The selected first product workstream is registered below; no agent dispatch is authorized.

## Development cadence for this direction

Follow [MAP-001 2.0.2 draft](../../project-map.md#development-and-delivery-cadence).
Develop the selected journey against real provider contracts, reusing the
accepted pilot and shared foundation. Use host Web/API feedback, then packaged
browser proof for the delivered behavior; retain separate visual acceptance.
Use existing L2/L3 fields for the local, packaged and delivery proof allocation.
Development cadence remains accepted; this draft changes priority and next-L2
selection. Original scope evidence remains historical.

## Relationships with other directions

These are interface relationships, not dependencies on completing an entire
direction. Future L2/L3 plans select actual provider milestones and acyclic hard
dependencies. Informational interactions do not create a cyclic execution graph.

| ID | Provider and version | Required output | Consumer | Needed before | Satisfaction proof / integration responsibility |
|---|---|---|---|---|---|
| DIR-005/DEP-01 | [DIR-001](../DIR-001/direction.md) `2.0.2` | Access, jobs, people, collaboration and inbox APIs | DIR-005 | Acceptance of the relevant scenario | Real administrative and operational journeys. The owning milestone and its proof are selected at L2/L3. |
| DIR-005/DEP-02 | [DIR-002](../DIR-002/direction.md) `2.0.2` | Source, mapping, semantic and DQ APIs | DIR-005 | Acceptance of the relevant scenario | Working data onboarding. The owning milestone and its proof are selected at L2/L3. |
| DIR-005/DEP-03 | [DIR-003](../DIR-003/direction.md) `2.0.2` | Analysis/segment/method capabilities and results | DIR-005 | Acceptance of the relevant scenario | Analytical journeys without browser-owned calculations. The owning milestone and its proof are selected at L2/L3. |
| DIR-005/DEP-04 | [DIR-004](../DIR-004/direction.md) `2.0.2` | Document/snapshot/refresh/render contracts | DIR-005 | Acceptance of the relevant scenario | Composition, reading and delivery. The owning milestone and its proof are selected at L2/L3. |

**Outputs supplied:**

- [DIR-006](../DIR-006/direction.md) `2.0.2`: Integrated browser journeys and build-bound evidence.
- [DIR-001](../DIR-001/direction.md) `2.0.2`: User commands and agreed UI states.

Each consumer proves integration with the provider-owned contract. The common
snapshot/refresh ownership allocation is in [MAP-001](../../project-map.md). Actual public
contract changes remain with their accepted context owners.

## Selected first product contribution — 2026-09-12

[WS-002](../DIR-004/workstreams/WS-002.md) `0.2.0` and
[MS-003](../../milestones/MS-003/plan.md) `0.2.0` now define the next first-report
accepted scope, with six prompts and one canonical journal. The owner accepted
WS-002/MS-003 0.2.0 on 2026-09-13; initial entry is recorded in that journal. This
contribution is implemented once in MS-003, not duplicated into another pack.

S04 implements the existing report/login route identities through the accepted pilot with real API persistence; S05 proves the same feature through HTTPS. Full administration and unrelated screens are not prerequisites.

## Owner decisions and next decomposition

| Decision ID | Decision or question | Authority / next condition | Effect |
|---|---|---|---|
| DIR-005/DEC-01 | This direction's L1 boundary and composition are accepted | Owner decision on 2026-09-06, recorded at [MAP-001 adoption](../../project-map.md) / MAP-001/DEC-05; version `1.0.0` | Settles L1 structure; does not accept an unwritten child plan. |
| DIR-005/DEC-02 | Previous WS-001-first selection | Historical MAP-001/DEC-06/07; next-selection priority superseded by MAP-001/DEC-10 on 2026-09-12 | Retain completed base and deferred scope; proposed product contributions are described above. |

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

MAP-001 2.0.2 registers this sequence draft at 2.0.2 with reciprocal draft
parent/provider links. Capability boundaries remain accepted at their earlier
basis; this draft does not change public/domain contracts or accept an unwritten
child. WS-001 navigation 1.0.10 keeps scope 1.0.0 and its recorded DIR-006 1.2.0
parent basis; its unimplemented C04–C06 remain allocated for later selection.
Completed milestones preserve exact historical plan/pack/journal/evidence bytes.
The map owns the proposed checkpoint order and records its validation.
