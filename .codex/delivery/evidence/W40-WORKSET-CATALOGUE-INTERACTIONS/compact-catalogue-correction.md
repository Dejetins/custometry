# Compact catalogue and scope controls correction

Owner browser feedback on 2026-09-24 supersedes the inline picker and Cancel-footer choices in [previous correction](feedback-2026-09-24.md). Execution remains within the [W40 frontend boundary](../../tickets/W40-WORKSET-CATALOGUE-INTERACTIONS.md).

## Changes

- Workset popovers omit Cancel and its footer, use reduced padding and width, and retain outside-click / Escape dismissal without committing a name.
- Header store summary is a selected/available count instead of concatenated names. Existing common/local scope semantics are unchanged. StoreScopePicker provides search, count and a bounded single-column checkbox list; inherited scopes hide the disabled list. Local metric filters explicitly inherit the common filter.
- Add metric and metric edit open a native modal dialog with catalogue search, metrics on the left and filters on the right. Native modality contains keyboard focus and blocks background actions; closing restores the trigger focus. Apply changes the draft; Cancel, close and Escape discard staged edits.
- Inspector contains selected cards only; the duplicated Sales/available-checkbox list is removed.

## Validation

`corepack pnpm --filter @custometry/web build`: passed (TypeScript + Vite, existing chunk-size warning). `corepack pnpm --filter @custometry/web test`: 22 files / 111 tests passed. Local grouped gate and diff whitespace check passed.

Real-browser preview checks: no Cancel in creation popover; Escape dismisses; no duplicated Sales heading; catalogue matches native `:modal`; applying Receipts increases card count from 3 to 4; Escape leaves the draft unchanged and restores Add metric focus; selecting three of twenty stores produces a short header counter; searching Store 10 returns one row. At 390x844 the modal bounds remain within the viewport. No report save request was made; browser test changes remain in the isolated test-session draft.

Visually inspected [desktop modal](catalogue-modal.png), [narrow modal](catalogue-modal-narrow.png), [store summary](store-summary.png), and [compact creation](compact-create-menu.png). Screenshots contain synthetic local fixtures only. Final local-filter copy distinguishes inheritance from common all-permitted scope.

Scope: WorksetControls, MetricCatalogue, MetricPickerDialog, StoreScopePicker, ConfiguredWorkspace and workspace.css. Browser contract change is compatible; API, persistence and backend are unchanged. No production publication or broader channel-filter implementation is claimed.
