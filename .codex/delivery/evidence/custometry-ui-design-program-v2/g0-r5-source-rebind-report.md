# G0 r5 source rebind report

## Outcome

`G0@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r5` rebound the owner-approved blueprint semantics to the current UI program while preserving the accepted visual authority and standard bytes as inherited, hash-pinned inputs.

## Bound scope

- Current semantic source: `custometry-ui-blueprint-ru.md` SHA-256 `3ac695caddf50260728e9f40422f14a87e66818557e7ee324021215dd9a38d24`.
- Successor intake: `.codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r5/ui-program-intake.json`.
- Inherited baseline: `.codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r5/platform-ui-baseline.json`.
- Immutable G0 program snapshot: `.codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r5/ui-design-program.promotion-candidate.json`.
- Accepted source visual remains `.codex/delivery/ui-design-programs/custometry-v2/evidence/pilot-candidate-v3-metadata/ru/source.html` SHA-256 `b54b8b77d677d57869b0065dbe3aa005f13070297dface19ba98938f50d83700`.
- Mobile-specific design, production implementation, publication, and deployment remain out of scope.

## Change-impact route

- Change kind: `product_semantics_scope_or_mobile` (product semantics only; mobile scope remains unauthorized).
- Earliest gate: `G0`.
- Exact affected authority cover: 35 rows across G0-G6.
- Canonical migration receipt: `.codex/delivery/ui-design-programs/custometry-v2/evidence/blueprint-rebind-r5/active-semantic-migration/prepared/historical-control-plane-migration-receipt.json`.
- The successor plan and sole stage ledger were applied through their compare-and-swap routes; historical rows and evidence remain intact.

## Validation

- `validate_ui_design_program.py --profile intake_ready`: passed, zero warnings.
- `validate_ui_design_program.py --profile baseline_ready`: passed, zero warnings.
- `validate_ui_design_program.py --profile draft`: passed, zero warnings.
- `validate_stage_ledger.py`: passed.
- Shared `ui-design-program` release validator: passed, including negative migration cases and no shipped Python bytecode.
- Independent cold-head prompt-pack review: passed after local follow-up; no unresolved Blocker or High finding.

## Adjacent-stage readiness

`G1@atlas-r4` is the unique pending successor, depends only on this G0 row, has a current prompt, and may rebuild the all-screen atlas from the rebound intake without a visual-owner checkpoint.

## Proof boundary

This report proves current-contract source binding, exact change-impact migration, complete G0 inputs, and adjacent G1 readiness. It does not prove later-stage screen semantics, rendered UI, browser behavior, production implementation, publication, deployment, mobile-specific design, or full WCAG conformance.
