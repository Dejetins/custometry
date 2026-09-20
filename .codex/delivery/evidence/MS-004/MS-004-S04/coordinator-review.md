# S04 coordinator review

Date: 2026-09-21 local / 2026-09-20 UTC. Baseline:
`6dcfc4d39840d898819a630ddfaec63a89256a91`.
Executor task: `01a0c0a6-e6fb-7203-b2eb-af335765fc2f`.

## Decision and ownership

Accept the S04 source-backed integration and local browser-smoke boundary for
technical-branch publication. The original executor consumed receipt
`receipts/001-ready.md`; the journal records S04 accepted and S05 disallowed.
This review neither replaces that receipt nor claims final milestone acceptance.

The coordinator verified all 26 owned source hashes and all 24 browser observation
and screenshot hashes in the final manifests: 50 checks, zero mismatches. The 62
incoming changed/untracked paths consist only of those sources, S04 evidence,
the exclusively updated journal and the coordinator's S03 synchronization record.
No unexpected path was found. The executor is idle before coordinator mutation.
The original project checkout was not changed.

## Review and resolved findings

- Replaced the initial inline-form arrangement with the accepted workset/card
  rail, main chart/table and docked Set/Card/Chart/Context inspector inside the
  preserved native document. Maintained bridge source regenerates runtime.
- Corrected display-only creator Save to reuse verified results, separated it
  from explicit query Apply, and connected presentation selection to rendering.
- Preserved same-unit shared axes and named distinct-unit axes; formatted server
  decimals and replaced stale prototype context and raw state labels.
- Strengthened exact reopen from a title-only assertion to restored server card
  values and 31 table rows without calculation POSTs.
- Added actual keyboard catalog/inspector proof and redacted console/network
  observations. Focus/Escape return and 1920/768/400 screenshots were inspected.
- Corrected reader display-only Save and own Saved View query/result restoration.
  The actual regression uses a different 30-day period and withdraws report run
  authorization while retaining data-read policy; Apply is unavailable, Save and
  exact reopen work without an Apply POST. Pure viewer denial without
  `analysis.read` remains expected under D06; no server or role policy changed.
- The executor additionally retained draft CAS bases across navigation, guarded
  late JSON-body completion after authorization changes, and cleared old-card
  bulk selection when copying/removing/creating worksets.

The coordinator inspected the accepted composition references and actual final
1920/768 inspector captures, plus actual 400 reflow and reader/report captures.
The source, screenshots and tested interactions support the S04 integration
claim. This is not pixel-perfect prototype identity or application-wide a11y
certification.

## Validation and limits

Reuse the source-bound executor evidence in [validation](validation.md): 85 Web
tests, Web lint/typecheck, fixture Ruff/format/Pyright, native source generation
and local tooling profile passed. Eight browser scenario/viewport pairs have
passing evidence across invocations: six unchanged full-run passes and two final
focused catalog/copy passes. The earlier full invocation's two readiness failures
are disclosed, not relabelled as passes. No unexpected API errors or page
exceptions appear in the final observations; expected 401/409 events are separate.
The owned Docker fixture was cleaned up.

Coordinator checks: manifest/ownership audit, `validate_prompt_packs`,
`uv run --locked python -m tools.check --scope local` and `git diff --check`
passed. Publication still requires the remote Foundation gate,
squash merge, confirmed remote main and technical-branch removal.

S05 must still complete the accepted AC-01…11 matrix, including direct
chart/table/tooltip/Focus artifact parity, same/different-unit and Saved View
comparisons, negative/legacy/fiscal/restart cases and an owner demonstration.
Unchanged S02/S03 proof should be reused within its stated boundary. The
METRIC-022 published-default limitation, unavailable goals/shared actions and
absence of deployment/release authority remain unchanged.

## Publication whitespace correction

The staged check exposed one trailing space in newly added `workspace.css`, which
the earlier unstaged check did not include. The same executor removed that one
byte and added [a separate correction record](publication-whitespace-correction.md).
The coordinator independently verified both source hashes, non-whitespace
equivalence and the unchanged consumed report/validation/manifest/receipt/journal.
The original 26-file manifest remains historical; the addendum binds the corrected
CSS bytes. Browser evidence remains applicable without a rerun for whitespace.
