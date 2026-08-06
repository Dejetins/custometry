# Custometry UI Design Program V2 — G1 Atlas Evidence

- Stage instance: `G1@atlas-r1`
- Gate: `G1`
- Result: `passed`
- Validation profile: `atlas_gate`
- Program artifact: `.codex/delivery/ui-design-programs/custometry-v2/ui-design-program.json`
- Rendered atlas: `.codex/delivery/ui-design-programs/custometry-v2/artifacts/g1/screen-atlas.md`
- Resolved atlas: `.codex/delivery/ui-design-programs/custometry-v2/artifacts/g1/screen-atlas.resolved.json`

## Actual scope

G1 reconciled the accepted G0 intake and immutable source indexes into an
exact-cover program atlas. It created hash-pinned G1 screen and journey shards,
bound them into the program manifest, and rendered the generated atlas. No
screen design, G2 family/wave assignment, frontend implementation, browser
runtime, Figma work, or mobile information architecture was performed.

## Atlas outcome

- Screens represented exactly once: `175`
- Journeys represented exactly once: `9`
- In-scope design surfaces: `151`
- Internal or non-visual surfaces: `22`
- Historical exclusions: `2`
- Route screens: `112`
- Route flows: `5`
- Persistent shells: `4`
- Route-backed transients: `1`
- Overlays: `24`
- System-state families: `5`
- Mobile scope: `unauthorized`

The `151` in-scope entries intentionally retain only the G2-owned unresolved
fields `design_family_id`, `wave_id`, and `coverage_profile`. All excluded and
internal entries are disposition-complete at G1. Journey entry and terminal
semantics are present for all nine journeys; graph criticality and transition
structure remain G2-owned.

## Evidence and validation

- The incoming G0 transition receipt SHA-256 matched the ledger binding and
  passed `validate_stage_transition.py` with `readiness_status: ready` and
  `next_stage_allowed: true`.
- `build_g1_artifacts.py` verified every G0 shard hash and identity, checked
  exact coverage against the intake and admission inventory, and emitted the
  G1 shards and indexes.
- `validate_ui_design_program.py --profile atlas_gate` passed with no errors or
  warnings and `can_close_active_gate: true`.
- `render_screen_atlas.py` emitted `175` screens and `9` journeys. A second
  render reproduced both output hashes exactly.
- The resolved `codex.ui-screen-atlas/v1` artifact passed its bundled schema
  validation.
- `uv run python -m tools.check --scope local` passed after activating the
  repository toolchain.
- Typed preflight evidence covers `current_gate`, `source_freshness`,
  `next_stage_inputs`, `write_scope`, `foreign_changes`, `execution_route`, and
  `handoff_artifact`.

## Control-plane binding repair

The incoming G0 receipt was hash-valid before the G1 claim, but it referenced
the mutable live program path. Once G1 populated the atlas, strict ledger
validation correctly reported the accepted G0 artifact binding as stale. G1
preserved the original receipt at
`.codex/delivery/ui-design-programs/custometry-v2/evidence/g0/stage-transition.mutable-program-binding.json`
with its original SHA-256
`9e69224a2fdcc145006148ab60f18ae776aa0e4429307c8a8a97260e6f50c3f0`,
created the byte-identical immutable G0 program snapshot at
`.codex/delivery/ui-design-programs/custometry-v2/artifacts/g0/ui-design-program.snapshot.json`
with the original accepted artifact SHA-256
`f95aad34ecc7ae5f7b15b1496816bd402003f1979cc7a6c925478e532880059a`,
and reassembled the live G0 transition receipt against that snapshot. No G0
product meaning, accepted intake, baseline, or gate result changed.

The outgoing G1 receipt likewise binds the immutable
`.codex/delivery/ui-design-programs/custometry-v2/artifacts/g1/ui-design-program.snapshot.json`
snapshot, whose SHA-256 equals the validated live atlas program at G1 closure.
This keeps the accepted G1 evidence valid when G2 later evolves the live
program.

## Proof boundary

Observed proof is limited to machine-rendered exact-cover atlas reconciliation,
hash-pinned artifact identity, deterministic rendering, and static contract
validation. It provides no target-screen design, browser/runtime behavior,
responsive-behavior, accessibility-conformance, performance, deployment, or
production proof.

## Foreign changes and residual risk

Pre-existing G0 documentation changes under `docs/**` were preserved and not
modified by G1. The program manifest and ledger are mixed-lifecycle control
files but contain only the scoped G1 additions recorded by this stage.

G2 must still assign criticality, exact source-backed journey transitions,
families, coverage profiles, workload-bounded waves, and baseline inheritance.
The accepted atlas does not imply that any of those G2 structures exist yet.
