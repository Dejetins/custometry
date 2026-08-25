# G4 r3 auth family execution report

## Scope

- Executed only `G4@family.auth.shell-auth.baseline-exception-auth-r3`.
- Produced the finished `/auth/sign-in` review result for representative screen `UI-AUTH-001` across `initial`, `loading`, `populated`, `error`, `permission_denied`, and `recovery`.
- Recorded reuse, without individual design or acceptance, for `UI-AUTH-002`, `UI-AUTH-003`, and `UI-AUTH-004`.
- Preserved the blocked r2 row and all adjacent G4/G5/G6 rows.

## Result

- Family artifact: `.codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r3/family-auth-shell-auth-baseline-exception-auth/family-acceptance.json`
- Review board: `.codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r3/family-auth-shell-auth-baseline-exception-auth/review-board.html`
- Gate: `family_review_ready`
- Owner checkpoint: pending
- Next stage allowed: false

The corrected result now uses the accepted pilot's exact neutral Graphite/cyan palette, compact surface hierarchy, 7-15 px radii, typography density, focus treatment, and reduced-motion behavior. The former marketing panel and promotional copy were removed; the screen contains only functional auth labels, instructions, state feedback, and actions. The `baseline-exception-auth` surface intentionally omits workspace header and navigation. Auth composition, fixtures, and state semantics remain source-backed and do not reuse unrelated pilot analytical meaning.

The sign-in surface width is now `420px`, reduced from `520px`. This is derived from the accepted pilot's `--context-width: 420px` working panel rather than its `510px` dialog width, so the auth task reads as a compact contextual surface while retaining approximately `370px` usable field width.

The `recovery` state is now a distinct recovery flow rather than sign-in markup with different status copy. It contains only the workspace email, `Send recovery link`, `Back to sign in`, and a dedicated live result. The password field, ordinary sign-in form, disabled continue control, diagnostic action, and generic state panel are forbidden in the recovery contract. `state-distinction-r3-04.json` compares the sign-in and recovery element inventories and fails the builder if they become identical or if a forbidden sign-in element returns.

The review board is now a self-contained HTML artifact: it embeds the target document, has no image or local subresource dependencies, exact-covers six rendered `data-review-entry` controls, switches state and RU/EN content, and exposes the form action inside the live preview. This makes the same artifact usable from a local file open as well as the canonical loopback QA route.

## Evidence boundary

- Canonical capture runtime `1.6.0` and visual-QA assembler `1.5.0`.
- Accepted pilot captured unchanged as `visual_authority_reference` under common deterministic conditions.
- Target captured as `screen_implementation` with exhaustive regions/elements/actions, unexpected-region closure, fixture/font/asset bindings, responsive-Web anchors, keyboard/focus, reduced motion, RU/EN stress, 200% zoom, console/network review, and accessibility smoke.
- Four Web anchors (`768`, `1024`, `1440`, `1920`) exact-cover six states: 24 target and 24 visual-authority captures, 48 render-provenance receipts, 24 supporting raster receipts, 24 visual-QA receipts, and six screen-acceptance receipts.
- Raster comparison is supporting visual-language evidence only, not primary same-screen fidelity proof.
- Corrective browser smoke verified all six state controls, RU/EN switching, recovery submission by pointer and keyboard, return to the sign-in state, a three-control recovery tab order, a visible 2 px focus outline, zero console warnings/errors, zero failed network requests, and no horizontal overflow at 768 px. The canonical terminal mechanic intentionally blocks direct `file:` navigation, so file-protocol behavior is supported structurally by the absence of subresources while all interactions were exercised on the loopback route.

This evidence does not prove production implementation, deployment, performance, full WCAG conformance, mobile-specific behavior, or individual acceptance of non-representative auth screens.

## Changed paths

- `.codex/delivery/ui-design-programs/custometry-v2/build_g4_auth_r3_artifacts.py`
- `.codex/delivery/ui-design-programs/custometry-v2/artifacts/g4-r3/family-auth-shell-auth-baseline-exception-auth/**`
- `.codex/delivery/ui-design-programs/custometry-v2/evidence/g4-r3/family-auth-shell-auth-baseline-exception-auth/**` except preserved pre-existing repair evidence
- `.codex/delivery/evidence/custometry-ui-design-program-v2/g4-r3/family-auth-shell-auth-baseline-exception-auth-family-report.md`
- `.codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md` limited to the r3 lifecycle and review checkpoint
- `.codex/agents/generated/custometry-ui-design-g0-v2/40-g4-02-family-auth-shell-workspace-baseline-r2.md` limited to the adjacent-stage transition-contract marker (`owner_review_target`); no family scope or execution content changed

## Foreign changes

All pre-existing working-tree changes outside the authorized stage paths were preserved. Pre-existing repair evidence and the accepted G0-G3 artifacts were not modified. The shared ledger was updated only for the authorized replacement lifecycle and current review checkpoint.

## Residual risk and next action

Owner acceptance is intentionally pending. The strict post-owner `family_gate` and adjacent execution remain unavailable until a canonical owner response accepts this exact review board; bounded corrections resume the same r3 row.
