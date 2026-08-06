# G0 cold-head review resolution

- Review mode: independent read-only subagent
- Initial verdict: `Not ready`
- Follow-up mode: local verification against the review checklist after fixes
- Final disposition: all material findings resolved; no second independent reviewer was used

## Resolutions

1. Visual authority now uses a canonical `codex.ui-owner-decision/v1` receipt assembled from the accepted owner task. The program, intake, baseline, and prompts share one exact repository-owned pilot identity and scope. A narrow revisioned adapter preserves compatibility with the current baseline/intake validator and is hash-bound to the canonical receipt.
2. The exact owner task is copied and hash-pinned inside the V2 evidence boundary. `owner-intent.json` durably carries included and excluded scope, nine critical journeys, source hierarchy, pilot limits, responsive-Web-only scope, and V1/Penpot historical-only status.
3. The ledger now uses the G3 report as G3 evidence, binds the accepted G0 receipt into G1 by exact path and SHA-256, records the completed G0 claim, and identifies G1 as the sole claimable adjacent row.
4. Every prompt now declares `decision_policy`, `decision_packet`, `resume_condition`, `resume_evidence_ref`, `execution_allowed`, and `Next stage allowed`, plus the required post-validation ledger handoff contract. G2/G3/G6 remain non-executable placeholders.

## Follow-up checks

- `validate_ui_design_program.py --profile intake_ready`: passed.
- `validate_ui_design_program.py --profile baseline_ready`: passed.
- `validate_ui_design_program.py --profile draft`: passed with the expected pre-G1 empty-atlas warning.
- `validate_stage_ledger.py`: passed.
- `validate_stage_transition.py`: passed.
- Post-transition G1 context: bounded, `8/8` files and about `20,948/40,000` tokens.
- Repository grouped local gate: passed.

The proof boundary remains documentation and static contracts. No browser, rendered responsive behavior, accessibility conformance, performance, deployment, or production claim is made.
