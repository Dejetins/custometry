# MS-004-S04 — native workspace integration

Stage: `MS-004-S04`; iteration: 1. Implementation and required S04 verification
are complete and ready for receipt-backed acceptance. The journal alone records
acceptance. Publication and S05 remain disallowed.

## Authority and scope

Execute the accepted [MS-004 plan](../../../../../docs/architecture/planning/milestones/MS-004/plan.md)
through its [canonical journal](../../../ledgers/MS-004.md) in the existing
canonical checkout. Baseline is `6dcfc4d39840d898819a630ddfaec63a89256a91`.
No publication, deployment, dependency installation or original-checkout changes.
The existing claim remains owned by the executor session.

## Implemented behavior

The native pilot hosts `ConfiguredWorkspace` through `PilotDocument` and its typed
bridge. It retains the original document/SVG shell and generated runtime, while
adding the personal workset/card rail and docked Set/Card/Chart/Context inspector.
The catalog contains exactly three registered metrics. Copy allocates fresh
instance IDs; ordering, repeated cards, common/local stores, empty scope and bulk
applicability controls preserve the server contract. Six grains and fiscal basis
are explicit query settings. Formatting never calculates business metrics.

Apply prepares results; Save persists the complete configured report separately.
Display-only creator Save verifies existing result bindings, and reader own-view
Save uses verified bindings without requiring creator preparation or a calculation.
Selected Saved Views restore their own query/display/calendar/result scope.
Temporal values can be read directly from the selected verified result projection.
The table, chart and Focus share that projection and unit axes.

Workspace calendar settings use current administrative capability, revision CAS
and idempotency. The current default is separate from the report pin; adopting it
requires explicit creator action and Apply/Save. UI guards complement backend
checks. Late response-body decode is rejected after authorization-generation change.

## Criterion coverage

Requirements: METRIC-021/022/025/026/027/028/030, CHART-021,
COMPARE-013, A11Y-001 and I18N-001, as mapped by accepted MS-004 AC-01…11.

| S04 criterion | Implementation and proof |
|---|---|
| AC-01/04/08 | Native card rail/catalog/copy/order, common/local context, six grains, comparison projection and locale copy; focused identity tests and real browser interactions. |
| AC-05/09 | Separate Apply/Save, display-only reuse, exact read, competing-save retained draft, explicit empty scope, logout and obsolete-body generation guard. |
| AC-08/11 | Administrative fiscal form, old pin retained after default change, explicit creator adoption, disabled reader changes, keyboard inspector/Focus and three viewport classes. |
| AC-08 harness handoff | Own source/control PostgreSQL, actual intake/artifacts, production API, loopback Vite, explicit startup/readiness/cleanup and safe browser observations. |

The final focused test also proves that copying a selected workset clears old
card selection before bulk operations on the new instances.

The full criterion matrix, every same/different-unit scenario, all calendar
boundary oracles and owner acceptance remain S05 responsibilities.

## Verification

See [validation](validation.md) for actual commands, outcomes, boundary and
limitations. Eight scenario/viewport pairs have passing evidence: six unchanged
full-run cases plus the final two focused catalog/copy cases. The initial full-run
failures and subsequent corrections are recorded explicitly. Screenshot review
covers 1920, 768 and 400; no single all-green final full invocation is claimed.

## Contract impact

- Browser-visible behavior: `breaking-change` to fixed-UI assumptions, as
  intentionally accepted in the plan compatibility matrix/D08. Personal worksets,
  dynamic card selection and explicit context/Save behavior replace the fixed
  report interaction. Legacy creation/preview and S03 API compatibility do not
  make this browser interaction change backward-compatible.
- Public API/DTO, persistence, migration, server calculation and deployment:
  `none` in S04; generated clients and mounted APIs are reused.
- Client session lifecycle: `compatible-change`, obsolete JSON bodies cannot
  repopulate protected state after access-generation change.
- Test runtime: `compatible-change`, a task-owned loopback source/control DB/API/
  Vite harness is added. Its grant-change helper exists only in the isolated fixture.

## Documentation and ownership

Updated canonical authoring/Web-source contracts, architecture navigation and
RU/EN report help. The plan, stage prompts and consumed S01–S03 evidence remain
unchanged. `MS-004-S03/synchronization.md` belongs to the coordinator and is
excluded. The journal is shared only through the exclusive updater, never manual
editing. The final owned source manifest is [owned-files.json](owned-files.json).

## Handoff to S05

Consume `tests/e2e/ms-004-workspace/playwright.config.ts`, `real_api_fixture.py`,
`scenario.py`, the Vite config and browser specs. The fixture owns a uniquely named
PostgreSQL container, temporary source/control databases, six-entity ingestion,
artifact directory, API/Vite readiness and graceful cleanup. It uses an existing
local PostgreSQL image; `MS004_POSTGRES_IMAGE` can select another already present
compatible image. Do not reuse historical cleanup against unrelated resources.

The [corpus](corpus.json) records safe aggregate coverage and admitted source
identities. S05 must extend integrated AC-01…11 proof, including source SQL oracle,
all negative/legacy/fiscal cases, restart/recovery and owner demonstration.
Preserve existing S02/S03 evidence when its inputs remain valid.

METRIC-022 published-default reset is not implemented by a draft/base view.
Goals/shared sets/publication remain unavailable. Legacy bases do not expose v2
workspace bindings; a first personal view needs an authorized Apply, while existing
verified Saved Views support display-only reuse without calculation. No full
accessibility, packaged runtime, production or release readiness is claimed.

S05 remains disallowed until the coordinator reviews evidence, synchronizes via
technical branch/PR/Foundation gate/squash, confirms remote main and branch removal,
and advances the journal with current input/synchronization evidence. All seven
S05 declared entry files exist; its exact prompt was inspected. S04 does not
substitute for S05 or owner result acceptance.
