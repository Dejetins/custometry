---
id: CUSTOMETRY-REPORT-EDITOR-STRUCTURAL-REGROUPING
version: "1.0"
artifact: standalone-executor-prompt
language: en
user_report_language: ru
scope: report-editor-layout
---

# Task

Reorganize the existing Custometry report editor controls into a coherent information hierarchy. Implement a structural regrouping of the current pilot UI, not a visual redesign. Apply it to the shared editor used for both creating and editing reports.

The owner likes the current pilot's colors, buttons, sizes, corner radii, icons, metric cards and table. Previous image-generated concepts changed these too much. Do not reproduce their component styling. The selected concept contributes only separation of responsibilities and compact contextual menus.

## Authority and entry

- Read repository `AGENTS.md` and `.codex/AGENTS.md`. Resolve the applicable existing delivery unit before edits; do not revive retired packs or create a parallel execution ledger.
- Inspect the running editor and its serving checkout. Historical runtime: `http://localhost:41746`; workspace `70568e58-2a23-4de1-9cf7-17bb44e8ae8d`; existing report `9285c38c-574d-5ce3-a8d1-028e809cc1ff`.
- Existing route: `/w/70568e58-2a23-4de1-9cf7-17bb44e8ae8d/reports/9285c38c-574d-5ce3-a8d1-028e809cc1ff/edit`. Creation route uses `/reports/new/edit`.
- The server previously used `/Users/daniildegtyarev/.codex/worktrees/c67c/Custometry`. This is a discovery hint, not verified current state. Do not edit a different checkout and claim the served UI changed.
- Read the relevant portions of `custometry-ui-blueprint-ru.md`, `docs/architecture/ui/target-pilot/README.md`, ADR-0007 and affected machine/human blueprint requirements. Resolve real requirement IDs; never invent IDs.
- Initial source entrypoints in the main checkout: `apps/web/src/features/reports/ReportWorkspace.tsx`, `ConfiguredWorkspace.tsx`, `PilotDocument.tsx`, `PilotChrome.tsx`, `workspace.css`, `pilot.css`. Locate the actual owners in the serving checkout before editing.
- Preserve unrelated edits. This task authorizes bounded implementation and verification, not publication, deployment, resetting data, new dependencies or backend redesign.

## Source priority

1. This task's explicit preservation requirements.
2. Current running pilot and its source components/tokens.
3. Current product contracts and behavior.
4. Linear references for grouping and contextual disclosure only.
5. Generated concepts for broad structural inspiration only.

Local Linear reference notes, if available:
`/Users/daniildegtyarev/.codex/visualizations/2026/09/24/01a0d4d8-84af-7900-9cb3-3e5f40be1e67/linear-reference-2026-10-06/README.md`.

This prompt is self-contained; missing historical images do not block source-based implementation. Do not generate more images or copy Linear's task-specific features.

## Hard invariants: do not change

- Metric cards: retain the existing card components, dimensions, typography, background/selected treatment, values, metadata, selection behavior, checkboxes, settings affordance and switching between revenue/checks/average check. Moving the surrounding controls does not authorize changing card internals or replacing cards with bare KPI numbers.
- Current visual tokens: colors, fonts, button sizing, padding, icons, radii and established selected/hover states. Do not create a new theme or a larger Save button.
- Existing table renderer, column meaning, formatting, density, scrolling, export and empty/error states. Only relocate its surrounding controls as needed.
- Existing chart renderer and data semantics. No invented comparison series, percentages, totals or capabilities.
- Existing left navigation rail and its behavior. Docked navigation continues to reserve workspace width rather than overlay content.
- Existing calculation, automatic refresh, delayed loading indication, report persistence and test datasets. Do not reintroduce a global Apply step.
- Do not introduce decorative control outlines, focus rings or cyan selection edge strips. Retain keyboard operability and use existing non-outline focus treatment; do not remove focusability to hide focus.
- Do not redesign the report library, authentication, navigation destinations or unrelated screens.

## Target information hierarchy

Use the following order. Section names describe responsibilities; they do not require adding visible headings or large containers.

| Zone | Belongs here | Must stay elsewhere |
| --- | --- | --- |
| Report header | Existing report name, saved/unsaved status, Save, report-level overflow, inspector toggle | Period, metric selection, chart appearance |
| Report navigation | Existing report page tabs only | Filters, palette, fonts, comparison |
| Data context | Period, report-level comparison, scope/filter entrypoints | Typography, palette, chart/table switch |
| Metric set toolbar | Set selector/tabs, add set, metric catalogue/count, set overflow | Global date range, report save, palette |
| Metric cards | Existing unchanged interactive card strip | Newly invented controls or redesigned KPI presentation |
| Visualization toolbar | Chart/table switch, contextual View menu, export, fullscreen and genuinely visualization-local actions | Report save, set creation, global data scope |
| Results | Existing chart or table | Persistent configuration inventory |

Keep a compact data context row under the report navigation and a compact set toolbar immediately above the cards. Keep visualization controls immediately above the results. Use existing spacing, alignment and subtle separators; do not wrap each zone in another large bordered panel.

### Contextual View menu

Group existing visualization settings in a compact anchored menu: applicable interval/grouping settings, series/change presentation, legend/grid controls and appearance settings, but only where those capabilities already exist. Separate presentation controls from appearance controls inside the menu using existing small labels or dividers.

Keep the chart/table switch directly accessible. Adapt menu contents to the active chart/table mode. Export and fullscreen remain local to the active result. Do not invent disabled settings to match a generated image.

### Comparison and scope

Inventory the current report-level comparison, chart comparison, card-to-card comparison and inheritance controls before moving them. Establish which are aliases and which have different scopes. Consolidate true duplicates only; preserve distinct semantics and label their scope clearly. Card-to-card selection remains intact, with its action near the visualization when relevant.

The product supports sales channels beyond physical stores. Do not use “All stores” as an umbrella label for all report filtering. Place supported channel/store/other dimension filters under a general data-filter entrypoint. Preserve the underlying supported dimensions and inheritance rules. Do not simply relabel a store-only selector as “All channels.” If the current pilot only implements store filtering, expose it honestly as the Store dimension within Filters and report the channel capability gap; do not fabricate options or expand backend scope.

## Execution sequence

1. Capture the current editor at the owner's desktop viewport, including metric cards, chart, table and open inspector. Record existing control roles and handlers.
2. Produce a short control relocation map: current location → target zone → unchanged behavior. Identify true duplicates and any unresolved semantic distinction.
3. Implement using existing components and local layout changes. Preserve state ownership, handlers and shared create/edit rendering. Avoid broad global CSS overrides.
4. Verify the structural result in the browser. Compare unchanged cards and controls to the baseline at the same viewport. Repositioning is allowed; restyling their internals is not.
5. Update only affected canonical UI documentation and required delivery evidence/links in the same unit. Follow the selected delivery route without creating an unnecessary plan pack.

Use `better-layout` for grouping. Use `better-accessibility` if menu focus/keyboard behavior changes, `browser-qa-evidence` for runtime verification, and the browser mechanism appropriate to the user's selected browser. Use other skills only at materially crossed boundaries.

## Acceptance and proof

- New and saved reports use the same regrouped editor shell.
- Cards retain baseline visuals and interactions, including metric switching, checkbox selection and settings.
- Header, navigation, data context, set management and visualization controls have distinct locations as specified above.
- Fonts/palette do not appear alongside dates and data scope.
- Existing controls remain reachable; no distinct comparison/scope behavior disappears during consolidation.
- Filter labels describe actual supported dimensions, without implying all data comes from stores.
- Chart/table switching, automatic recalculation, period changes, save/reopen, export and inspector opening/closing continue to work.
- No new persistent outlines, oversized controls, overlay navigation or duplicated primary action appears.
- At the baseline desktop width, controls align without accidental wrapping or overlap. Check narrower available width with navigation/inspector open; avoid clipping and preserve existing responsive behavior.
- Capture final screenshots of chart, table and the contextual View menu. Report observed behavior separately from assumptions and unavailable checks.
- Run focused existing frontend tests/build and the smallest applicable repository gates from `docs/architecture/tooling-gates.md`. Add tests for meaningful interaction changes, not assertions that merely mirror CSS. Do not claim implementation correctness from screenshots alone.

Resolve routine reversible layout choices independently. Ask only when moving a control requires an unresolved material product decision; continue independent work meanwhile. Do not ask the owner to approve the already-fixed card appearance again.

## Final handoff

Respond in Russian. Summarize what moved, what was preserved, verification results, remaining capability gaps and the local URL. Include screenshots and changed file links. Do not claim production delivery. Do not publish or reset the existing test data.
