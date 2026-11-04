# W39 owner correction 003 report

Date: 2026-09-23. [Ticket](../../../tickets/W39-REPORT-LOADING-SESSION-EFFICIENCY.md).
[Web source contract v20](../../../../../docs/architecture/ui/custometry-web-implementation-source-contract-v1.md).
Requirements: METRIC-025, COMPARE-013, CHART-021, A11Y-001, I18N-001, WEB-ARCH-004/006.

## Authority and scope

The owner authorized five bounded refinements: navigation spacing/alignment,
compact separate KPI surfaces, signed semantic-color tooltip deltas, bounded
adaptive normal-chart height/padded line ranges, and per-card aggregate YoY.
The new height policy supersedes the previous remaining-viewport interpretation.
The preserved pilot still owns shell/tokens/density. The Mindbox atlas01 shows
separate cards but crops their lower portion; no exact YoY component is inferred
from it. Current owner instruction explicitly supplies the YoY requirement.

Single executor, same W39/c67c unit, no new agents/tasks, publication/import or
MS-004 acceptance. Existing EUR/UTC removal, independent docks, Add guards and
trust boundaries remain. Original/575c and user draft/tab were not modified.
Preview remains http://localhost:41746, with existing API/DB processes and schemas unchanged.

Browser presentation impact: compatible-change. API/schema/calculation/units/
timezone/immutable identity impact: none. Owner January report was read-only.
This correction uses synthetic report `86d32ae7-c5cb-5a4f-87c9-45d0e33886a0`
bound to `w39-05@example.test` from the existing synthetic load fixture,
with transient Apply requests, not Save. No source seed data was modified.

## Causal evidence and source selection

Coordinator independently observed the initial 2688×1575 owner report in a
separate Browser QA tab: navigation 40 px high with asymmetric 0/12/7/18 padding;
160 px card strip with 1 px gaps, no per-card radius; 1020 px plot; January totals
43908.52 / 210 / 209.09 without YoY. These match source CSS and the previous
remaining-space height algorithm. The value axis omitted explicit data bounds,
allowing its default zero floor to compress the 6–7 count series near the top.

The server already provides each result's `temporal.changes[metric]` aggregate.
`packages/analytics_core/application/workspace_calculation.py` computes it using
period totals, prior totals and both coverage objects. The presentation service
requests the selected temporal alignment for each card's effective query. Frontend
binding lookup selects that card's result and bucket projection; no backend change
is needed. Aggregate percentages are never summed or derived from bucket values.

A read-only request for owner report `9285c38c-574d-5ce3-a8d1-028e809cc1ff` confirmed
January2025, complete31/31 current/prior coverage and authoritative changes:

| Metric | Absolute | Relative percent (display rounded) |
| --- | --- | --- |
| Net revenue | +10991.68 | +33.39% |
| Receipts | +5 | +2.44% |
| Average receipt | +48.518239256678… | +30.22% |

[Raw source evidence](owner-jan-source.json) preserves full server decimal strings.
The annual synthetic report separately has incomplete coverage and null aggregate
deltas. That annual limitation was not transferred to the owner's January data.

## Implementation

Header/navigation/main insets align at20 px, or12 px narrow. Navigation has10 px
vertical padding (8 px narrow) and retains automatic height. Cards use fixed124 px
height,10 px gaps and the existing10 px panel-radius token, independent borders
and surfaces. Gear/selection controls remain available; row allocation keeps
loading, unavailable and numeric YoY from shifting cards or plot origin.

KPI YoY reads `result.temporal.changes[binding.bucket_projection]` only after
matching the bound result. Display has signed absolute/percent, prior-year label
and semantic colors. Disabled comparison and unapplied context have explicit
states. Incomplete data shows a visible short explanation; zero baseline retains
any valid absolute change and shows unknown percentage with a visible baseline0
reason. Null/invalid values never become zero or infinity. Denied/untrusted data
remains behind the unchanged authorized workspace boundary.

Normal chart height is clamp320–520 px at44vh; Focus retains its larger viewport
layout. Per-unit axis ranges pad actual finite data and use readable intervals;
count intervals remain integers. Empty, constant, zero, negative and multiple-unit
cases are covered without changing series values. ECharts instance reuse remains.
Tooltip content is constructed through DOM `textContent`, with no interpolated
HTML or user renderer code. Positive/negative/neutral spans use `--positive`,
`--negative` and `--text-muted`; signed strings provide non-color cues.

## Local proof and independent Browser observations

[Validation](validation.md) records exact commands and outcomes. Three responsive
browser scenarios cover2688/1480/400, fixed card geometry, selected-card switching,
unchanged SVG identity/scroll/plot origin, bounded plot height and enlarged Focus.
A real API/browser scenario applies complete January, February and January1
contexts to a separate synthetic report. It checks all six KPI cards against their
own server metric aggregate and moves the mouse onto actual chart coordinates.
Rendered positive, negative and zero hover spans match semantic theme colors.
[Complete-context proof](complete-context-proof.json) records authoritative inputs
and observed tooltip text, colors and axes. No response interception substitutes
synthetic deltas for this numeric proof.

Coordinator task `01a0c02d-5267-7601-b735-5b43d11789c0` independently reported:

- 2688: navigation52 px with10/20 padding; header/main aligned atx83. Cards124 px,
  gap10/radius10, separate surfaces. Owner January YoY exactly matched the three
  displayed rows above, color rgb(98,199,170). Normal plot520 px.
- Receipts SVG labels5/6/7/8 place6–7 within the range. Selecting receipts/revenue
  preserves cardsy314 and ploty498. Card deltas stay metric-specific.
- Actual rendered tooltip via SVG point interaction: January4 receipts −1/−14.29
  both rgb(240,125,135); January1 zero both rgb(139,140,147); revenue January1
  +333.64/+30.64 both rgb(98,199,170). No surrogate chart-option display.
- 1480×969: normal plot426 px, cards124 px, navigation52 px, no vertical overflow
  in the observed three-card owner report.
- 400×850: no header/navigation overlap, horizontally contained124 px cards with
  visible10 px gaps/radius; first-card YoY readable. Focus plot767 px remains
  enlarged. Focus closed, viewport restored; console errors empty.

All five owner items were reported PASS in that independent Browser check.
Original user tabs/draft remained untouched.

## Boundary and next action

[Source/build identity](identity.json), [frozen inputs](frozen-input-check.json)
and [backend reuse](backend-source-check.json) identify the exact local boundary.
Earlier correction/performance records are preserved; their frontend timings
remain attached to the measured old bundles. No full backend, idle, latency or
previous regression matrix was repeated. Ticket remains active for owner review;
there is no publication, import, rollout or milestone acceptance claim.

### Final identity and gates

Production build manifest SHA256:
`fd98d970e90510bab9b10992b4378840da9089a74cc06b193e9706707b73a7d0`.
All169 frozen inherited inputs and23 prior backend-manifest files match their
recorded hashes. Build,105 web tests,4 targeted browser scenarios,1 focused
exact-series parity rerun, local source gate, generator check and diff check pass.
Per-file/per-asset hashes are in [identity](identity.json). Independent Browser
observations above cover the same product behavior; the final metadata typography
fit and tiny-number formatting were additionally checked locally. This remains a
local implementation checkpoint awaiting owner review, not a release.
