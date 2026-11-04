# MS-004 S05 — integrated local result

Status: **review_ready** — technical verification complete; explicit owner
acceptance of the demonstrated result is absent. The receipt-backed transition
records `needs_input` / `awaiting_input` under the existing S05 claim.

## Scope and result

The unit consumes accepted S01–S04 at baseline
`86055ce732640ebe68fd5415a55f7bbde3499181` and completes the accepted personal metric
workspace. The unchanged plan is 0.2.1, SHA-256
`9d0d590f7c3fccc581a6257365f0bcba961539f1fa9e0f93eec651e36255360e`.
Requirements and evidence are mapped in [criterion matrix](criterion-matrix.md).
The stage does not implement C02/C03, goals, publication/export or Forecasting.

Confirmed bounded repairs preserve the comparison artifact in personal Saved
Views, expose the same dates/values/deltas/reasons across chart/table/tooltip/Focus,
establish initial narrow-inspector focus when the iframe portal mounts, localize
metric/unit labels, and reject obsolete Apply/reload completions after context
changes. An actual held Apply body reproduced the stale projection bug; the
corrected generation guard passed both viewport projects.
See [causes and compatibility](repair-review.md). Registered metric formulas,
source intake, fiscal arithmetic and immutable version identity are unchanged.

## Changed modules and documentation

- `packages/contracts/presentation/workspace.py` and generated workspace/report
  schemas/clients: optional comparison with old absent-field serialization preserved.
- `packages/presentation/application/workspace.py`: admit the verified comparison
  with a Saved View and verify its scope/access/bytes on read, without GET compute.
- `apps/web/src/features/reports/ConfiguredWorkspace.tsx`: select stored comparison,
  clear superseded Apply state on view save, focus the mounted inspector, reject
  obsolete context completions and preserve Save's separate lifecycle.
- `apps/web/src/features/reports/WorkspaceProjection.tsx`: baseline dates, typed
  delta/reason display, consistent localized labels and explicit missing comparison.
- `apps/web/src/features/reports/workspace.css`: keep Focus clear of the native
  navigation rail and complete table dates/labels reachable through horizontal scroll.
- `tests/integration/presentation/test_workspace_s03.py` and the existing
  `tests/e2e/ms-004-workspace/` fixture/specs: real recovery, artifact parity,
  transport-delay, keyboard, fiscal and localized browser regression proof.
- Canonical authoring/recovery/Web source contracts and architecture index are
  synchronized; the UI blueprint now distinguishes the historical fiscal requirement
  from the locally implemented S04/S05 result awaiting owner acceptance. Its
  requirements revision is unchanged. The docs generator and local profile passed.

See [owned files](owned-files.json) for exact source hashes, including generated
files. This is iteration S05/1 and review-ready attempt 001, not owner acceptance.

## Proof and limits

See [validation](validation.md), [calculation reuse](reused-calculation-evidence.json)
and [demonstration](demonstration.md). Real isolated PostgreSQL source/control
storage, the actual intake/admission path, production Identity/API/Presentation,
immutable artifacts and a real browser establish local integration. Reconstructed
application plus fresh database connections proves the exercised durable reopen
boundary; it is not a host-reboot, installation or production recovery claim.

SavedView comparison is compatible for new readers of old data; old strict readers
reject new comparison-bearing payloads. Coordinate reader upgrades before new
writes and use forward repair after v2/custom calendar writes. No SQL migration
or old artifact rewrite is introduced by this unit.

The exact native pilot is retained. Screenshots are local synthetic-data evidence,
not evidence of a deployed product. MS-004 does not satisfy the published-default
reset portion of METRIC-022 because C01 operates on draft reports.

## Ownership and handoff

The original checkout is read-only. Coordinator-owned S04 synchronization evidence
and its journal advance are preserved. Source changes, generated contracts, tests,
canonical documentation and stage evidence belong to S05; the [ownership manifest](owned-files.json)
binds final bytes. The journal is updated only through the exclusive updater.
Accepted plan, stage prompts and consumed S01–S04 evidence remain unchanged.

No Git publication, branch, PR, image, dependency installation or deployment is
performed by this executor. The same executor records
review readiness and awaits actual finished-result owner acceptance. The
coordinator owns subsequent source synchronization. No successor is fabricated.

## Final checks and review packet

Real API corpus: 1 passed plus 2 legacy tests. Final Python source/unit/contract
suite: 108 passed; Web: 85 passed. Full browser integration: 14 passed before final
refinements; final context/label regression: 10 passed; final Focus/table/fiscal
layout and demonstration: 4 passed. No skipped checks are counted as evidence.
Local source profile, Ruff, Pyright, Web/browser-source typecheck, pilot generator,
docs index, prompt-pack validation and whitespace checks passed. Exact commands,
failures and reuse boundaries are in [validation](validation.md).

The [browser manifest](browser-manifest.json) binds admitted corpora, safe network/
console observations, parity payloads and screenshots to final sources. The
[owner demonstration](demonstration.md) links final-source fiscal chart/table and
temporal tooltip/Focus captures. The remaining input is the owner's decision on
that finished C01 result. Keep `next_stage:null` and `next_stage_allowed:false`.
No coordinator acceptance, publication success or stronger runtime boundary is
inferred. If corrections are requested, preserve this review snapshot/receipt and
create new evidence before another transition.
