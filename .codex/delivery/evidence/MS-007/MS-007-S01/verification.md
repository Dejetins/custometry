# C03 observed verification

Target: c67c source checkout, owned disposable PostgreSQL/artifacts, synthetic
API 58147 and browser 41747. Retained user data/runtime remain untouched.

## Observed

- Final Presentation unit/contracts: 113 passed in 0.70s, including serializer compatibility.
- Focused Web: 37 passed across six files, including 8 structure and 3 original
  composer-state tests. Final geometry regression adds one: 9 structure tests passed
  in 295ms; the unchanged 29 tests retain their prior passing evidence.
- TypeScript, Ruff and strict Python checks passed at the affected boundaries.
- Complete C02+C03 browser regression: 6 passed in 39.9s after integration.
  Includes the open-Builder lock regression and stronger viewport assertions.
- C03 main real-browser scenario passed in 12.3s after the final geometry repair: chapter/page/nested section,
  keyboard tabs and active-page-only content, cross-page move, independent copy,
  pointer drop, layouts/density/resize, hide/lock/history and exact snapshot/page.
  Includes deletion while Builder is open and exact Undo restoration.
  One initial Apply; no extra Apply through structure changes, save and reopen.
- C03 RU/EN page recovery/overflow: 2 passed in 10.3s with strengthened viewport
  assertions after screenshot repair. Eight pages, Undo active-page creation,
  retained Redo, search/all-pages, dashboard profile and save/reopen.
  Zoom is CSS document zoom 200% in the real iframe (not native browser zoom).
  Both Save and all-pages remain in viewport, with Save bounded to viewport width.
- Owned PostgreSQL/API rehearsal: 1 passed in 9.32s. Old omitted metadata stays
  absent in saved/GET/replayed payloads; a new grouped dashboard revision carries
  lock/hide fields and the same result references. Old snapshot remains byte-equal.
  C02 CAS/concurrent replay/crash/permission/revocation/rollback assertions remain.

## Reproduction and repairs

Independent review found active-page Undo navigation loss, duplicate chapter order
following delete/add, and a Builder opened before a block was locked. Fixes preserve
valid active navigation/Redo, append unique orders, and recheck current block/ancestor
lock before commit. Locked affected nodes cannot be silently reordered by a neighbour.

A transient invalid page during local Undo/navigation initially remounted pending
UI; author draft now selects a surviving page during transition. The first RU harness
initialization reset locale on each navigation; corrected to initialize only when
absent. The first layout select lacked an explicit accessible name; corrected.
Generated legacy reports client was regenerated after closed DTO evolution.

The first 200% screenshots showed clipped header actions despite toBeVisible passing.
Scoped shell width/container wrapping and stronger viewport assertions repaired it;
new screenshot visually confirms Save and page selector are accessible. Original
legacy outer tabpanel semantics are removed only for the Composer page navigator.

Serializer preserves absent newly added fields instead of inserting defaults into
old immutable payloads/replay hashes. Independent in-memory probes confirmed nested
Save and TypeAdapter behavior, explicit false/null retention and closed output schema;
the later real API rehearsal covers the saved/replay/snapshot boundary.

Section moves originally repacked blocks even across compatible grids. The repair
preserves custom geometry across grid-to-grid subtree moves, grouping, same-parent
block moves and repeated layout selection. Conversion across grid/non-grid still
normalizes placement. A nested custom-span/row/row-span regression passes, and the
independent reviewer closed the finding. Cross-section vacancy fallback retains
block span and row span. Deleted-block settings close immediately; navigation also
closes transient settings so an orphan editor cannot recreate a deleted node.

Final affected TypeScript check passed. Independent review has no open material
findings. Narrative preview and both final zoom captures were visually inspected.

## Proof limits

Locks/hide are presentation controls, not ACL. Profiles are common composition only;
Research/live Dashboard/provider lifecycle is not accepted by these tests. Active-page
proof with a bounded fixture is not TEST-INV-101/V1-AC-049 or 100x30 qualification.
Native browser zoom, assistive technology and complete accessibility remain C10.
Successful data paths use real APIs; transport-failure injection is failure proof only.
No production migration, publication, deployment, dependencies or retained data writes.

Inspected captures: [narrative exact preview](browser/c03-narrative-preview.png),
[EN document zoom](browser/c03-en-zoom-200.png), [RU document zoom](browser/c03-ru-zoom-200.png).
