# Local composition verification

Date: 2026-09-17. Owner design acceptance: initial composition accepted after this
verification; see the [decision record](README.md#decision-record). No prototype
code or browser proof was changed by recording that decision.
Target: `http://127.0.0.1:8845/drafts/metric-workspace-v1/`.
Mechanic: Codex in-app browser through Computer Use.

The actual pilot CSS, SVG sprite and rail are reused. Saved Mindbox screenshots
01–10 were inspected for additional behavior. The composition intentionally
introduces configured cards and worksets; it does not claim identical report
contents or new production behavior. See [scope and decisions](README.md).

## Source comparison

The preserved pilot HTML and all ten Mindbox reference images were inspected.
The pilot's existing 1920 × 1080 reference
(`.codex/delivery/evidence/MS-003/MS-003-S04/browser/pilot-1920.png`) and this
draft's [1920 × 1080 overview](evidence/overview-1920.png) were opened together
in one comparison input. Native CSS equality and the exact original HTML hash
were also checked. The draft retains the charcoal shell, cyan selection, SVG
rail, document header, chart/table surface and docked inspector.

Intentional differences subsequently accepted as the initial composition: worksets above a configured-card
rail, visible per-card scope, Set/Card/Chart/Goals inspector sections, two-card
mode and monitoring goals below the analysis. These additions are the purpose
of the draft. This is a composition comparison, not a pixel-equivalence verdict:
content differs intentionally and in-app captures have softer text than the
existing source capture. Backend/source-data fidelity is not claimed.

## Observed interaction results

| Flow | Observation | Result |
|---|---|---|
| Catalog and duplicate instances | Search for average receipt, add it, Apply; rail grows from four to five independent cards | pass |
| Ordering | Activate the move-up control with Enter, Apply; receipt count moves before revenue | pass |
| Cancel versus Apply | Changing revenue to North and cancelling retains 15.98 million EUR; applying changes only that card to 6.07 million EUR | pass |
| Bulk scope preview | Selecting bulk store application names all four affected cards and explicitly reports no incompatible metrics in this bounded catalog | pass |
| Context intersection | Report Center plus card North renders no data and explains the disjoint filters | pass |
| Period comparison | Connector deltas and delta-trend mode render; the trend has a labeled percentage axis | pass |
| Table parity | January shows 1,620,000 / 1,380,000 EUR, difference 240,000 and +17.4%; all eight displayed months match the plotted fixture arrays | pass |
| Two cards | Revenue/count show labeled EUR/count axes; Center/North revenue cards share one EUR axis | pass |
| Workset selection and copy | Store set displays its three configurations; a personal copy appears without replacing the original | pass |
| Goals | Negative target is rejected; a positive revenue target and hypothesis create a clearly labeled draft goal | pass |
| Save disclosure | Save reports memory-only storage in the current tab; reload resets the fixture | pass |
| Focus | The analysis expands; Escape restores the report | pass |
| Narrow inspector | At 768px the inspector overlays; Tab enters its controls, Escape closes it and returns focus to the opener | pass |

## Layout and browser evidence

- Viewports: 1920 × 1080, 768 × 1024 and 400 × 900. No document-level horizontal
  overflow was observed; the metric rail deliberately scrolls within its bounds.
- Fixed an inherited fixed-height header that overlapped controls below 700px.
  Rechecked at 400px: action row bottom 91.24px, header/navigation boundary 98.24px.
- Fixed rotated connector labels; they now read horizontally.
- No console errors or warnings were observed in the prototype session. Rendered
  DOM inspection found one ECharts SVG and no external script/stylesheet URLs.
  This is not a full network trace or an external provider check.
- Screenshots: [card filter](evidence/card-filter-1920.png),
  [delta trend](evidence/delta-trend-1920.png),
  [two metrics](evidence/two-metrics-1920.png), [goal form](evidence/goal-1920.png),
  [768px overview](evidence/overview-768.png), [400px overview](evidence/overview-400.png).
- No API, container, application build, dependency install or packaged
  qualification was performed. Existing application/runtime resources were not
  changed. Full accessibility and EN localization are outside this Russian draft.

## Repository and authority checks

- `node --check docs/architecture/ui/drafts/metric-workspace-v1/composition.js`: pass.
- `uv run --locked python -m tools.custometry_quality.validate_prompt_packs`: pass,
  three journals. Explicit read-only entry checks reject both S05 and S06 with
  `Entry is not current authority`.
- `uv run --locked python -m tools.custometry_quality.generate_docs_index`: pass;
  refreshed contributor navigation after adding the draft/evidence documents.
- `uv run --locked python -m tools.check --scope local`: pass after fixing English
  documentation wording and refreshing the index. Earlier failed runs were not
  treated as passes. `git diff --check`: pass.
- Protected-path and structured comparisons: production code, tool/test/runtime
  sources, completed MS-001/MS-002, accepted MS-003 plan/prompts, S01–S04 rows,
  receipt transition history, all six stage contracts and original pilot assets
  remain unchanged.
- One independent read-only documentation/ledger review found no material issues.
  Its verdict covers authority and artifact consistency, not browser or product
  acceptance. It independently confirmed 82 preserved plan/prompt/evidence files.

No actionable P0/P1/P2 defects remain in the tested prototype boundary. The owner
subsequently accepted the initial composition. Implementation contract decisions
remain separate; see [README](README.md#accepted-composition-and-remaining-implementation-decisions).

## Subsequent acceptance and continuation documentation

On 2026-09-17 the owner accepted the initial composition and requested that
future owner requirements remain possible even when absent from the current
blueprints. [README version 2](README.md#decision-record) records that decision.
[WS-003 0.1.0](../../../planning/directions/DIR-004/workstreams/WS-003.md) proposes
the bounded continuation; it is not an accepted L3 or runnable pack. MAP/L1
navigation is synchronized at 2.1.0, with previous accepted child bindings kept.

Checks after the acceptance and planning amendments:

- `uv run --locked python -m tools.check --scope local`: pass.
- `uv run --locked python -m tools.custometry_quality.validate_prompt_packs`:
  pass, three journals; structural validation only.
- `git diff --check`: pass.
- Bounded link/metadata assertions: WS-003 links resolve; all seven current
  MAP/L1 versions and their reciprocal parent references are 2.1.0.
- SHA-256 comparison against the start of this amendment: 537 existing product,
  tool/test, stage-plan/prompt/journal, preserved-pilot and WS-002 files unchanged.
  This includes the already-deferred MS-003 journal; no stage state changed here.
- The three prototype code files match the hashes recorded in
  [source binding](source-binding.json). The existing preview returned HTTP 200;
  no new browser interaction claim is made for this documentation amendment.

No product code, new milestone pack, container, installation or Git publication
was performed in this amendment. The previous browser evidence remains applicable
to the unchanged prototype only. At that review boundary, WS-003's child sequence was still proposed. The owner
subsequently confirmed the order and C01 scope: see
[WS-003 1.0.0 decisions](../../../planning/directions/DIR-004/workstreams/WS-003.md#owner-decisions-and-next-child).
Goal semantics and shared-write contracts remain separate decisions.

## Subsequent L2 selection

On 2026-09-17 the owner explicitly confirmed the proposed sequence and first-stage
scope. [WS-003 1.0.0](../../../planning/directions/DIR-004/workstreams/WS-003.md#owner-decisions-and-next-child)
records acceptance of DEC-01/02. C01 L3 is now the next planning step; the request
to explain goals does not accept their unresolved progress/edit policies.
Composition document version 3 changes navigation only; prototype bytes and its
visual acceptance remain unchanged. MAP/L1 navigation is synchronized at 2.1.1.

`uv run --locked python -m tools.check --scope local` passed for this recording.
Bounded metadata assertions confirmed accepted WS-003 1.0.0 and reciprocal
MAP/L1 versions. A before/after SHA-256 comparison found all 533 selected existing
product/tool/test/milestone-plan/prompt/journal files unchanged. This proves
document consistency and preservation, not new product behavior or stage entry.

final result: passed
