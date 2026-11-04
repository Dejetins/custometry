# S05 bounded integration repairs

Baseline: `86055ce732640ebe68fd5415a55f7bbde3499181`. Scope: MS-004 D01/D04/D05/D06/D08,
AC-04/05/06/07/08/09; METRIC-022/028/030, CHART-021, COMPARE-013,
A11Y-001 and I18N-001. Plan and prompt contracts remain unchanged. The coordinator
confirmed that persisting the missing ComparisonArtifact implements accepted
Presentation ownership rather than introducing a new product decision.

## Confirmed causes

1. An actual granted reader applied the revenue/receipt pair, saved its personal
   view, lost report-run authorization and reopened the view. The admitted
   comparison had `UNIT_MISMATCH`; the reopened table had values but no reason.
   `SavedViewV1` lacked the comparison and `ConfiguredWorkspace` explicitly selected
   null for saved views. The first new test also sampled its before-table before
   result loading; this test-readiness mistake is disclosed and not the causal
   proof. The recorded API projection versus reopened table establishes the defect.
   Corrected readiness and the repaired persistence passed the focused real test.
2. Temporal Saved Views rendered a prior series named `2` when no live Apply
   comparison was present. The legend now uses the verified selected temporal
   mode. Chart/table/Focus use the same stored projection; display-only Save clears
   an obsolete Apply envelope so it cannot override the newly saved selection.
3. Initial narrow inspector focus was inactive for 30 seconds after the heading
   became visible. Its parent effect ran before the asynchronous iframe portal
   mounted. A stable callback ref focuses the actual mounted heading; the effect
   still handles section changes. The corrected 768 test passed initial reverse/
   forward traversal, Focus traversal and Escape return. No role bundle changed.
4. The inspected real temporal tooltip showed values and units but omitted the
   baseline dates, delta and unavailable reasons. The renderer now formats these
   fields from the same immutable projections as the table. It performs no metric
   aggregation, date remapping, subtraction or percentage calculation.

5. A transport fixture held the exact successful production Apply body after
   sending headers/one byte. The author reloaded the saved context before releasing
   the body. The old onSuccess then replaced the saved projection (31 restored days
   became the stale applied 30-day interval). A generation captured at dispatch
   now gates success/error publication; edits, explicit reload and Saved View
   selection invalidate previous generations. A reload response is similarly
   discarded if the context changes while it is pending. Reload and own-view
   selection are disabled during Save to preserve its separate commit lifecycle.
6. RU chart legends and table headings exposed canonical `receipt` units. Both
   now use the existing workspaceUnit and metricNames dictionaries, retaining the
   canonical units in immutable payloads and axis identity.

7. Final visual inspection of the 768 Focus screenshot found the fixed overlay's
   left edge/button behind the native workspace clip/62px navigation rail. The
   source used viewport inset 12px despite the retained rail. The overlay now
   offsets its inline start by the existing `--sidebar` token plus its margin.
   The inherited fixed table layout also ellipsized exact/baseline dates; the
   configured-result table now uses intrinsic width and its existing horizontal
   scroll region. A real full-visibility/left-edge hit test for Close Focus and
   cell scrollWidth/clientWidth assertions verify that dates are not clipped.

## Contract impact and compatibility

| Surface / supported interaction | Classification / conditions |
|---|---|
| New reader with old persisted Saved View | compatible-change: optional comparison defaults to absent and is omitted from serialization; canonical payload and existing creator companion hashes are preserved. No old row/artifact is rewritten. |
| New Saved View / new server and generated Web client | compatible-change: Save verifies existing result scope, creates/adopts the immutable comparison before committing the view, then read verifies mode, card/result/metric/unit/format identity and artifact bytes under current access. |
| Old strict Python SavedViewV1 reader / new comparison-bearing payload | breaking-change: its extra-forbid schema rejects the new field. Regenerate/deploy dual-compatible readers before new writes. Old binary rollback after these writes is unsupported, consistent with the existing v2 forward-repair policy. This is not labelled universally compatible merely because the field is optional. |
| Old generated TypeScript consumer | Its interface has no runtime extra-field rejection, but its UI omits the comparison; no semantic correctness or mixed-client parity claim. |
| New Web / old view or server lacking pair comparison | No invented deltas. Independent card results remain available; an unverified pair does not render a combined chart and the table explains that an explicit Apply/Save is needed for a verified comparison. |
| Read/no-run boundary | Preserved: GET only verifies existing artifacts and never computes/adopts a comparison. View-only Save verifies existing results and may admit a comparison without running source aggregation. Current report, dataset, personal ownership and policy checks remain mandatory. |
| Persistence/schema | JSON payload extension only; no SQL migration, backfill, pointer or transaction-order change. Result-comparison bytes precede the existing atomic view transaction; missing/corrupt comparison fails closed. |
| Calculation/calendar/metric definitions | none: registered formulas, aggregation, calendar identity and source-day alignment are unchanged. |
| Browser/focus | compatible-change for accepted flows: retained native pilot, corrected selected-view projection, initial focus, generation-checked Apply/reload completion, localized labels and disclosed comparison state. |

Source discovery covered the Saved View DTO/generator, Presentation materialization,
verification and repository, Analytics comparison/verification port, generated
clients, Web projection/controller, real fixture and relevant integration tests.
No claim is made about unknown external consumers. No dependency installation,
production change, deployment or publication is performed.

## Verification boundary

Exact final commands, results and evidence belong in `validation.md` and the
criterion matrix. Development failures include an incorrect English button name,
an early table sample, a restarted TestClient URL incorrectly prefixed `/api`
(the mounted app uses `/reports`), and selecting `base_definition` instead of the
creator's `definition`. These are test authoring defects, not concealed product
passes. Prior consumed reports/manifests/receipts remain unchanged; S05 evidence
records new source identities and the checks invalidated by its repairs.
