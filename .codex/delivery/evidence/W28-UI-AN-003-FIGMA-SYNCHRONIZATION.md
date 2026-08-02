---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: W28-UI-AN-003-FIGMA-SYNCHRONIZATION
proof_boundary: product-owner-accepted-local-html-equivalent-figma-ui-an-003-synchronization-plus-versioned-minimum-design-foundation-contracts-and-read-back-evidence
proof_skills: [figma:figma-use, figma:figma-generate-library, figma:figma-generate-design, better-layout, better-ui, better-accessibility, browser-qa-evidence, playwright-cli, contract-impact-analysis]
verdict: superseded
machine_conformance: not_ready
product_decision: not_inherited_from_W27
implementation_readiness: not_assessed
redaction: No credentials, cookies, browser storage, private product data, provider payloads, or unrelated Figma files were inspected or retained. Screenshots contain synthetic Northwind Retail UI data only.
executed_checks:
  - record the 2026-08-02 product decision that replaces the external synchronization route with repository-owned HTML code components registries manifests catalog and browser proof
  - confirm the W27 accepted status, product-owner decision, pilot_passed outcome, scale decision, and exact accepted visual source
  - inspect the exact Figma library and product files before mutation and preserve W21 node 40:536
  - reconcile active normative delivery language from index-first to accepted-HTML-first bounded Figma synchronization
  - capture fresh accepted HTML states at 1440 by 900 and 1024 by 768 with browser geometry and diagnostics
  - create and read back W28 semantic variables, text styles, icon components, and minimum UI-AN-003 foundation components in the exact library file
  - audit the library component group for detachment, raw icons, semantic-paint bindings, text-style bindings, dimensions, identities, and publication status
  - probe cross-file importability without publication
  - read back the exact product target after the initial failed mutation and after each of two deterministic repair passes
  - perform final product read-back after the repair budget was exhausted
  - parse the three durable JSON receipts with jq
  - uv run python -m tools.custometry_quality.validate_delivery_tickets
  - uv run python -m tools.custometry_quality.validate_delivery_contract
  - uv run python -m tools.custometry_quality.validate_blueprints
  - uv run python -m tools.custometry_quality.generate_requirement_index --check
  - git diff --check
observations:
  - W28 is no longer an active delivery dependency; W29-HTML-FIRST-UI-FOUNDATION replaces it in the current graph while this record preserves the prior blocked attempt truthfully.
  - W27 remained accepted and its accepted HTML source was not modified.
  - The exact library file now contains 53 W28 variables in two collections, 6 W28 text styles, 28 versioned icon components, and 23 versioned UI-AN-003 foundation components.
  - The 23-component read-back reported zero detached instances, zero unbound semantic paints, zero unbound text styles, and zero raw icons.
  - W28 library assets are UNPUBLISHED because ticket authority explicitly excludes publication; their keys cannot be imported cross-file.
  - The initial product mutation and both permitted repair passes failed on deterministic Figma host or instance-tree constraints.
  - Exact read-back after every failed product write found zero W28 product compositions and no partial product nodes.
  - Preserved W21 product node 40:536 remains readable and unchanged at 1440 by 900.
  - Figma product exports, same-viewport comparisons, Russian-copy stress, four-theme product receipts, repository foundation freeze, W22 handoff, delivery graph transition, UI-design gates, and the grouped local gate were not executed because the ticket stop condition fired.
  - Blocked-ticket, delivery-contract, blueprint, requirement-index, JSON, and whitespace consistency checks passed after durable evidence was written.
---

# Outcome and scope

On 2026-08-02 the product owner selected a repository-owned HTML-first UI
foundation and discontinued this synchronization route. This record preserves
the exact prior W28 attempt, mutations, read-backs, failures, and exclusions as
historical evidence; it does not convert the incomplete result into an accepted
foundation.

# Commands and observations

The documentation migration updated the active UI plan, specification,
delivery graph, migration registry, W22 dependency, and normative UI blueprint.
W28 was removed from the active graph and replaced by
`W29-HTML-FIRST-UI-FOUNDATION`. No historical external artifact was deleted,
published, retried, or relabeled as current proof.

# Verdict

`superseded`. The historical execution below remains `not_ready` on its
original proof boundary. Current delivery must not resume it or use its partial
local assets as an operational source.

## Historical blocked record from 2026-08-01

# W28 UI-AN-003 Figma synchronization evidence

## Outcome

W28 is **not ready** and must not be accepted. The accepted HTML reference,
normative process reconciliation, browser reference package, and minimum local
W28 library foundation were completed and read back. The required product
compositions could not be created in the exact product file within the ticket's
two-pass deterministic repair budget. The final exact read-back contains no
partial W28 product nodes.

## Acceptance guard

| Required W27 value | Observed |
| --- | --- |
| Ticket status | `accepted` |
| Evidence product-owner decision | `accepted` |
| Terminal outcome | `pilot_passed` |
| Post-pilot decision | `scale` |
| Accepted visual source | `http://127.0.0.1:5173/w/northwind-retail/analytics/sales?view=html-prototype` |

The W27 record and prior browser observations were not altered.

## Normative reconciliation completed before the blocker

Active delivery language was changed from the superseded index-first target to
contract → responsive HTML → browser validation → explicit product-owner
acceptance → bounded Figma synchronization → production implementation in:

- `.codex/delivery/specs/custometry-contract-compiled-ui-prototyping-pilot.md`;
- `.codex/delivery/specs/custometry-linear-workspace-ui-transition.md`;
- `docs/architecture/ui/linear-workspace-ui-transition-standard-v1.md`;
- `custometry-ui-blueprint-ru.md`.

Historical `Master Elements Index`, `ghv0Cv3ddqMvv3zFVvR22p`, and index/detail
map references were retained only when explicitly marked historical,
superseded, or non-prerequisite. No W22, migration-registry, or delivery-graph
transition was made because W28 did not reach acceptance.

## Fresh HTML reference boundary

Nine fresh PNGs cover Chart, Data, Result Trust, Focus chart, Focus breakdown,
collapsed/hidden/resized Sidebar, and compact `1024 × 768`. Their dimensions,
SHA-256 digests, component axes, and browser diagnostics are recorded in
`assets/W28-UI-AN-003-FIGMA-SYNCHRONIZATION/browser-reference-receipt.json`.

Observed desktop axes include Sidebar `12,12,224,876`, application
`248,12,1180,876`, KPI `264,96,1152,72`, Chart `264,184,1152,390`, and
breakdown `264,586,1152,296`. At `1024 × 768`, the collapsed Sidebar is
`12,12,64,744`, application `88,12,924,744`, the root font remains `14px`, CSS
zoom is `1`, and document/client widths both equal `1024`. The browser session
ended with zero console errors and zero warnings and was closed.

## Figma start probe and preserved evidence

| Target | Before W28 | Final observed state |
| --- | --- | --- |
| Library `hX3nQOtcSdCc97uv26m9eG`, page `0:1` | `44` top-level roots, `42` local variables in `2` collections, `5` local text styles, registered W21 component/icon inventory readable | `95` top-level roots plus the W28 library assets below |
| Product `MXfxuhSFpIczbUtFmOSyPp`, page `0:1` | `8` top-level roots; W21 node `40:536` readable | `8` top-level roots; W21 node `40:536` still readable; `0` W28 product compositions |

No blocking pre-write identity drift was observed. The W21 accepted and
verification nodes were not deleted, relabeled, or mutated.

## W28 library mutation and read-back

The exact library file contains:

- `Custometry W28 / Theme v1`, collection
  `VariableCollectionId:54:231`, key
  `68dfb7a52a3babbbe41be541e375281099dd64f7`: `18` semantic colors and modes
  `abyss|graphite|frost|paper`;
- `Custometry W28 / Foundation v1`, collection
  `VariableCollectionId:54:250`, key
  `4fcf7378a4bd9cba066b7a9fc412d879edfe6c07`: `35` spacing, radius, size,
  stroke, and typography variables;
- `6` Inter text styles;
- `28` versioned icon components;
- `23` minimum UI-AN-003 foundation components, from
  `55:231` (`W28/Control/Icon Button/Default/v1`) through
  `55:943` (`W28/Focus/Explore Shell/v1`).

The normalized identities and dimensions are in
`assets/W28-UI-AN-003-FIGMA-SYNCHRONIZATION/figma-library-readback.json`.
Read-back found `0` detached instances, `0` unbound semantic paints, `0`
unbound text styles, and `0` raw icons. Small rectangle findings were named
semantic rules rather than icon substitutes.

Every W28 library asset reports `UNPUBLISHED`. Publication was not attempted:
the ticket explicitly forbids publish. A read-only import probe from the exact
product file returned `Component ... not found`, so W28 local keys could not be
presented as cross-file library identities.

## Product mutation attempts and stop condition

| Attempt | Finding | Exact read-back |
| --- | --- | --- |
| Initial mutation | Host rejected `setPluginData`; `setSharedPluginData` is required | `0` W28 nodes |
| Repair pass 1 | Figma rejected an `Application surface` `x` override inside an instance | `0` W28 nodes |
| Repair pass 2 | `findOne` encountered missing instance-child `I131:2254;10:31` while building independent bound surfaces | `0` W28 nodes |
| Final read-back | Repair budget exhausted | Product top-level count `8`; W28 count `0`; W21 `40:536` preserved |

The normalized attempt receipt is
`assets/W28-UI-AN-003-FIGMA-SYNCHRONIZATION/figma-product-final-readback.json`.
No write was blindly replayed: every uncertain failure was followed by exact
target read-back. The initial attempt was followed by exactly two deterministic
repair passes, so the ticket-mandated stop condition now applies.

## Proof not reached

Because no W28 product composition exists, the following acceptance gates are
unobservable and were not claimed:

- product-state component identity, detachment, raw-icon, paint, and text-style
  audits;
- Figma exports and HTML-versus-Figma visual comparison at `1440 × 900` and
  `1024 × 768`;
- bounding axes within `1 px`, clipping/overlap and content/control-order proof;
- Russian long-copy and four-theme product receipts;
- repository token/component/icon/manifest/renderer/receipt freeze and digests;
- W22, migration registry, and delivery graph consumption changes;
- UI-design compile/test gates, route/i18n gates, and the grouped local gate.

The following limited consistency checks did pass after the blocked record was
written: JSON parsing for all three receipts,
`validate_delivery_tickets` (`32` tickets), `validate_delivery_contract`,
`validate_blueprints` (`958` requirement IDs),
`generate_requirement_index --check` (`958` requirements), and
`git diff --check`. These checks validate the blocked record and documentation
consistency only; they cannot substitute for the missing synchronization proof.

Therefore `machine_conformance: not_ready`,
`product_decision: not_inherited_from_W27`, and
`implementation_readiness: not_assessed` are the only truthful terminal values.

## Contract impact and residual risk

- Process documentation: compatible reconciliation of active delivery order;
  no product, route, API, persistence, or runtime behavior changed.
- Figma library: additive local W28 assets exist and are audited, but they are
  neither published nor accepted as a complete foundation because the product
  half and terminal proof are absent.
- Figma product: unchanged after final read-back; W21 node `40:536` remains the
  last accepted identity.
- Production, API, persistence, browser-runtime implementation, complete
  accessibility, performance, recovery, release, and deployment remain outside
  the observed boundary.

## Next safe action

Do not continue W28 under the exhausted repair budget. A separately authorized
successor execution unit must build product compositions from independently
created bound surfaces and top-level published W21 instances without traversing
or overriding nested instance children, then rerun exact read-back, exports,
same-viewport comparisons, Russian/theme receipts, repository foundation
freeze, W22/graph/registry handoff, and every terminal gate. Until then W28
remains blocked and W22 must not consume W28 as accepted.
