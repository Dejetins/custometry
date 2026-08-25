# Blueprint rebind r5 control-plane blocker

## Requested change

- Owner authority: the current blueprint changes are accepted.
- Required route: `product_semantics_scope_or_mobile`.
- Earliest valid restart gate: `G0`.
- Invalidation boundary: the current `G0` through `G6` authority chain requires a successor revision.
- Visual checkpoint policy: execute sequentially and stop at each owner visual checkpoint.

## Bound source

- Change record: `.codex/delivery/ui-design-programs/custometry-v2/evidence/blueprint-rebind-r5/change-record.json`
- Change-impact request: `.codex/delivery/ui-design-programs/custometry-v2/evidence/blueprint-rebind-r5/change-impact-request.json`
- Accepted G0 anchor: `.codex/delivery/ui-design-programs/custometry-v2/artifacts/g0-r4/ui-design-program.snapshot.json`
- Accepted G0 anchor SHA-256: `ceca5cacb2516ba4b175e8efeb1f629aca11d17a14de37a29725626f2478bb3a`

## Released-tool result

The canonical command exited with status `1` before producing a change-impact receipt:

```bash
python3 /Users/daniildegtyarev/.codex/skills/ui-design-program/scripts/assemble_change_impact.py \
  --request .codex/delivery/ui-design-programs/custometry-v2/evidence/blueprint-rebind-r5/change-impact-request.json \
  --project-root /Users/daniildegtyarev/Projects/Custometry \
  --ledger .codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md \
  --output .codex/delivery/ui-design-programs/custometry-v2/evidence/blueprint-rebind-r5/change-impact-receipt.json
```

The primary current-source diagnostics are accepted `G3` and dependent `G4` closure bindings to the superseded `custometry-ui-blueprint-ru.md` hash. The same full validator also reports accepted `G4@family.auth.shell-auth.baseline-exception-auth-r5` raster/provenance closure failures.

The latter failures were reproduced after restoring the exact previously accepted UI blueprint blob (`cbf4cbc...`) in a read-only temporary repository copy. This establishes that they predate the current blueprint change under the released validator.

The current full diagnostic set is deterministically bounded:

- error count: `451`;
- canonical diagnostic SHA-256: `bcc8ffa53c97df384d611ae53bcd2c1157ca73707ace9364e1e4e8875e62b08e`;
- `G3@CUSTOMETRY-UI-DESIGN-PROGRAM-V2-r4`: `8`;
- `G4@family.auth.shell-auth.baseline-exception-auth-r5`: `440`;
- `G4@family.auth.shell-workspace.baseline-r4`: `3`;
- UI blueprint bindings: `19`;
- G4 receipt bindings: `96`;
- G4 live raster checks: `144`;
- G4 visual provenance checks: `192`;
- diagnostics outside those categories: `0`.

The matrix-derived affected set is the exact `35` current-authority rows:

- `G0`: `1`;
- `G1`: `1`;
- `G2`: `1`;
- `G3`: `1`;
- `G4`: `26`;
- `G5`: `4`;
- `G6`: `1`.

## Route gap

- `assemble_change_impact.py` requires the source ledger to be fully semantically valid before assembling a receipt.
- `migrate_historical_control_plane.py` accepts the released active contract only for `active_semantic_compatibility` with a `g3_realization_inside_accepted_baseline` change and an exact `G3`-`G6` successor suffix.
- No released route can admit the exact diagnostics that will be invalidated by a `G0` product-semantics successor while rejecting unrelated corruption.

No receipt was forged, no validation was skipped, and the sole stage ledger was not mutated or claimed.

## Required authority expansion

A narrow shared-skill repair is required under `/Users/daniildegtyarev/.codex/skills/ui-design-program/**`. It must add a typed G0 product-semantics active-compatibility route that:

1. snapshots and SHA-binds the source ledger, plan, registry, and complete diagnostic set;
2. admits only diagnostics belonging to the exact affected current-authority cover;
3. rejects unrelated source-ledger failures;
4. exact-covers and invalidates the current G0-G6 authority chain;
5. validates the successor plan, prompt pack, and ledger before a compare-and-swap apply;
6. includes focused release tests and one independent cold-head review.

The minimum released-skill surface is now known:

- extend `historical-control-plane-migration-request.schema.json` to admit the typed `product_semantics_scope_or_mobile` active-compatibility request;
- make `source_validation` bind the exact exempted affected-row set rather than one G3-only stage;
- generalize `validate_active_semantic_source_errors()` to accept only diagnostics whose stage IDs and diagnostic classes match the matrix-derived affected cover;
- keep ordinary `validate_ledger()` strict and expose exemptions only through the canonical migration caller;
- generalize successor topology validation from the exact G3-G6 suffix to the matrix-derived earliest gate and exact affected cover;
- preserve the final candidate's ordinary, exemption-free validation and shared compare-and-swap apply;
- preserve the stable `1.0.0` registry identity because earlier immutable migration receipts hash-bind `contract-versions.json`; extend the backward-compatible schema, contract prose, apply-time exact-binding checks, and focused self/release tests together.
