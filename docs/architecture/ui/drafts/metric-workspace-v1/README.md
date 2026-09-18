---
doc_id: UI-METRIC-WORKSPACE-COMPOSITION-001
title: Metric workspace composition baseline
doc_version: 3
product_spec_version: 0.11.0-draft
requirements_revision: 2026-09-17.1
visibility: internal
ship: false
owner: product
requirement_ids: [METRIC-025, METRIC-026, METRIC-027, METRIC-028, METRIC-029, CHART-021]
status: accepted
proof_boundary:
  label: local-interactive-composition-prototype
  exclusions: [production-implementation, backend-computation, permission-proof, packaged-delivery]
---

# Metric workspace composition

The owner accepted this composition as the starting baseline on 2026-09-17 and
requested that it be recorded and developed further. This is acceptance of the
overall layout and interaction direction, not a frozen final design. The separate
[owner decision](../../../../../.codex/delivery/evidence/MS-003/local-composition-20260917/owner-decision.md)
already selects local development and defers MS-003 S05/S06. Approving this visual
composition does not approve unselected backend contracts or a release.

The owner also explicitly retained the ability to request capabilities absent
from current requirements. Such requests are valid inputs to development; see
[handling new requirements](#handling-new-requirements). The accepted
continuation is [WS-003 1.0.0](../../../planning/directions/DIR-004/workstreams/WS-003.md).
The owner separately confirmed its order and first-child scope; C01 L3 is next.
Goal policies and unwritten milestone plans remain separate. The existing preview
URL remains stable.

## Open and inspect

```bash
python3 -m http.server 8845 --bind 127.0.0.1 --directory docs/architecture/ui
```

Open [the interactive draft](http://127.0.0.1:8845/drafts/metric-workspace-v1/).
No dependency installation, application build, API or container is required.
The [reference gallery](reference.html) displays the already saved source images.

The prototype uses Russian UI copy; control names below are English descriptions.

1. Switch between **Sales overview** and **Store comparison**. Click a card to
   select the chart metric; in two-card mode a click changes the second card.
2. Open **Configure workset**, search/add a metric, move it with the arrows and
   apply. Adding the same metric twice produces independent configured cards.
3. Use a card's settings to change its store. Cancel leaves applied data intact;
   Apply changes the working configuration. Bulk apply previews affected cards.
4. Use **Report context** to change the common store/period. Disjoint common and
   card stores show no data, rather than silently changing scope or returning zero.
5. In **Chart**, try connectors, delta trend, two cards and value labels. The
   table contains the same fixture values; Focus expands the same analysis area.
6. Copy a set and create a goal example. **Save in prototype** marks an in-memory
   configuration as saved; reloading resets the draft. There is no backend save.

## Composition and source mapping

| Surface | Accepted composition choice | Source / implementation consequence |
|---|---|---|
| Shell, SVG icons, rail, header, density, inspector | Derive from the actual preserved pilot document and its complete stylesheet | [Pilot](../../target-pilot/README.md), exact hash in [source binding](source-binding.json); preserve the production native-pilot foundation |
| Worksets | Compact row above the card rail, within the report rather than a second global navigation | Atlas 01/04; configured collection with explicit scope and copy-as-new |
| Cards | Four compact slots initially; metric identity, value, change and inherited/local scope stay visible | Atlas 01/02/03/09; replace fixed KPI positions with configured instances, not new formulas |
| Editing | One docked inspector with Set / Card / Chart / Goals; narrow screens use the same inspector as an overlay | Atlas 02/03/06/08; no unrelated second settings system |
| Report and card context | Common context in the toolbar; local scope on each card; explicit intersection preview | METRIC-026/027; extend the existing effective-context contract before final polish |
| Comparison | One analysis area, explicit period versus two-card mode; shared axis for the same metric, separate labeled axes for different metrics | Atlas 05/06/07/09; extend typed ChartSpec/ComparisonArtifact, keep a trusted renderer |
| Goals | Compact strip below the analysis and creation through the inspector | Atlas 08; a monitoring object tied to a card and fixed period, not a target action or forecast |
| Segments and campaigns | Reserve segment use in the existing document navigation and typed card filters; do not manufacture campaign data | Atlas 10 establishes future context, not authority for an unplanned CRM module |

The larger configured-card rail and new workset row intentionally change the
report's composition. The owner accepted these additions; they are not presented as a
byte-identical reproduction of the old report. Mindbox supplies interaction
references, while Custometry retains the visual language.

## Preserve, change once, then extend

Keep the current real source intake, registered receipt metrics, immutable result
artifacts, report persistence and native pilot integration. Their existing proof
is in [MS-003's journal](../../../../../.codex/delivery/ledgers/MS-003.md) and the
[native-pilot report](../../../../../.codex/delivery/evidence/MS-003/MS-003-pilot-native/report.md).
This prototype neither reruns nor certifies those boundaries.

Change the fixed KPI selection, report/card context, chart mode and serialized
configuration together. Do not polish these overlapping surfaces before settling
their shape. New goals extend the model; reusable segments later connect through
the typed population/filter seam. No new chart library, custom data library,
generic UI engine or separate service is selected.

Next: settle the bounded persistence/API migration and comparison/goal decisions,
prepare the corresponding L2/L3/pack with the owner,
implement the intersecting behavior locally, then finish visual polish and real
browser proof. Package only at a separately selected delivery boundary. There
is no new runnable milestone or implicit S05/S06 continuation from composition acceptance.

## Accepted composition and remaining implementation decisions

- Keep worksets **inside a report**, with personal/shared scope explicitly shown.
  One inspector edits the set, selected card, chart or goal.
- Retain one main chart/table/Focus surface. Distinguish temporal comparison from
  descriptive two-card comparison; do not overlay every mode simultaneously.
- Keep goals below the analysis; start their implementation only after agreeing
  direction, period aggregation, edit/version behavior and access rules.
  The illustrated higher-is-better sum goal is a proposal, not a product rule.
- WS-003 confirms starting implementation with the three registered receipt metrics;
  Customer/Product sources remain available to later agreed calculations.
  Department-specific catalogs, CRM formulas and complete segmentation are not
  implied by this composition.

The draft uses invented January–August 2025/2024 receipt series and two fictitious
store shares. It does not read the six-table demo database or copy vendor values.
Fixture arithmetic is for display only; production computations remain server
owned. Shared-scope choices illustrate UX and do not verify permissions.

## Handling new requirements

The baseline guides current work and may evolve through concrete owner requests.
An absent requirement is a documentation gap to resolve, not a reason to reject
an authorized change. Preserve unaffected decisions. For each actual addition,
update the affected machine/human/UI requirements and the selected plan/prompt
before dependent implementation; record the decision once and link its consumers.
Do not rewrite all plans or require a separate change-request document by default.

The agent identifies intersections with current work and explains material scope,
data, permission or migration consequences. Ask only about a missing product
choice or material conflict; implementation details inside the agreed boundary
remain delegated. Do not invent new capabilities, libraries or business rules
under the cover of this flexibility. A new requirement neither erases prior
evidence nor silently claims that existing implementation already satisfies it.

## Decision record

| Decision | Authority and date | Scope |
|---|---|---|
| UI-METRIC-WORKSPACE-COMPOSITION-001/DEC-01 | Owner response, 2026-09-17: the draft provides sufficient understanding; record it and proceed with improvements | Initial composition accepted; the prototype remains fixture-backed and the production contracts are separate |
| UI-METRIC-WORKSPACE-COMPOSITION-001/DEC-02 | Same response: the owner may request work absent from general requirements | Evolving requirements with focused synchronization; no automatic scope invention |

| Version | Date | Change |
|---|---|---|
| 1 | 2026-09-17 | Local interactive composition prepared and verified for owner review |
| 2 | 2026-09-17 | Record initial owner acceptance, future requirement handling and the WS-003 continuation proposal |
| 3 | 2026-09-17 | Editorial navigation update for accepted WS-003 1.0.0 sequence/C01 scope; composition and prototype code unchanged |

## Verification

See [design and interaction evidence](design-qa.md). Source CSS/SVG/rail are
retained in `index.html`; original demo scripts are removed. `composition.js`
mounts only the proposed surfaces. ECharts is the existing local 6.1.0 asset;
the original pilot, asset, license and manifest are unchanged.
