---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.2-draft
ticket_id: W10-PENPOT-W08-OVERLAP-RECOVERY
proof_boundary: canonical-penpot-W08-baseline-visual-overlap-recovery
proof_skills: ["product-design:audit"]
verdict: passed
penpot_file_id: 7cd71457-8d32-8044-8008-549f83bb4645
penpot_start_revision: 196
penpot_end_revision: 197
repository_fingerprint: 95be9344f85e907a03b6d53e2f9dba608dd45ea04a5b9ef252d0c9476272b108
redaction: No credentials, customer data, Penpot document payloads, browser state, or environment dumps were retained.
executed_checks:
  - confirm W08, W08 analytics baseline recovery, and W09 are accepted with passed terminal evidence
  - compute the ordered SHA-256 context_sources fingerprint before the first Penpot write and repeat it before verdict
  - confirm the canonical Penpot file ID, revision 196, and exact pre-write target structure before the first write
  - retain one W08 delta board per target and remove only the 18 specified non-stable sibling boards it covered
  - individually export and visually review all nine repaired targets
  - scan all 140 stable frames for root geometry, direct-child bounds, sibling-board geometry, and z-order; export every non-contained sibling-board candidate for visual classification
  - confirm UI-AN-002 and UI-AN-011 remain visually intact and contain no direct foreign W08 child board
  - confirm exactly 110 route frames, 25 overlay/state frames, and 5 system surfaces with no duplicate, missing, orphaned, renamed, or deleted stable UI-ID
  - confirm C25, the six W10 routes, and flow 10 remain absent while flow 09 remains present
  - confirm Penpot currentFile.validate returns no errors and two terminal reads remain revision 197
  - uv run python -m tools.custometry_quality.validate_route_registry
  - uvx check-jsonschema --schemafile packages/contracts/routes/ui-route-contracts.schema.json packages/contracts/routes/ui-route-contracts.json
  - uvx check-jsonschema --schemafile packages/contracts/routes/ui-surface-contracts.schema.json packages/contracts/routes/ui-surface-contracts.json
  - uv run python -m tools.custometry_quality.validate_delivery_tickets
  - git diff --check
observations:
  - Canonical Penpot file 7cd71457-8d32-8044-8008-549f83bb4645 moved only through this scoped recovery from revision 196 to terminal revision 197.
  - All 140 contract-backed stable root frames remained reconciled at 110 routes, 25 overlays, and 5 systems; duplicate, missing, orphan, root-collision, and direct-child-out-of-bounds lists were empty.
  - The repeated ordered repository fingerprint was 95be9344f85e907a03b6d53e2f9dba608dd45ea04a5b9ef252d0c9476272b108 before the first Penpot write and before verdict.
  - The historical W10 pre-write incident was revision 191 to 192 before any W10 mutation; it is recorded here only as context for the next W10 terminal evidence and is not attributed to this recovery modification.
---

# W10-PENPOT-W08-OVERLAP-RECOVERY Evidence

## Outcome and scope

The canonical Penpot baseline no longer contains a late W08 board that covers
an obsolete panel, table, or chart. Each of the nine affected stable route
frames now has exactly one retained integrated W08 content board positioned at
the replaced content origin. The retained boards preserve the accepted W08
content and stable parent route IDs; only eighteen obsolete, non-stable direct
siblings were deleted.

No W10 route, component, component board, target-frame update, or flow was
created. `C25`, all six W10 route identities, and flow 10 remain absent; flow
09 remains present. Product blueprints, architecture, executable contracts,
localization, and accepted predecessor artifacts were not modified. This is
Penpot design proof only; it does not prove browser/runtime behavior,
accessibility-runtime, authorization, persistence, calculation, export,
performance, deployment, or release readiness.

## Scoped Penpot changes

| Stable route | Retained integrated board | Deleted non-stable sibling IDs |
| --- | --- | --- |
| UI-DATA-008 | `33a2a659-d0eb-80bd-8008-5af954859110` | `e451483d-aae3-807d-8008-54a99ff214ba`, `e451483d-aae3-807d-8008-54a99ff214cb` |
| UI-DATA-010 | `33a2a659-d0eb-80bd-8008-5af95c65c564` | `e451483d-aae3-807d-8008-54a9a09abd4d`, `e451483d-aae3-807d-8008-54a9a09aea90` |
| UI-DATA-013 | `33a2a659-d0eb-80bd-8008-5af96438ec98` | `e451483d-aae3-807d-8008-54a9a1d1a801` |
| UI-DATA-014 | `33a2a659-d0eb-80bd-8008-5af96be2d2fc` | `e451483d-aae3-807d-8008-54a9a24000da`, `e451483d-aae3-807d-8008-54a9a24000eb` |
| UI-DATA-021 | `33a2a659-d0eb-80bd-8008-5af9740fbd54` | `3e34a4ec-283e-800b-8008-5932e011f896`, `3e34a4ec-283e-800b-8008-5932e059cdb7` |
| UI-DATA-022 | `33a2a659-d0eb-80bd-8008-5af97c1ff69d` | `3e34a4ec-283e-800b-8008-5932e09ed7c3`, `3e34a4ec-283e-800b-8008-5932e09ed7c4`, `3e34a4ec-283e-800b-8008-5932e0e38045` |
| UI-AN-010 | `33a2a659-d0eb-80bd-8008-5afa3721ad71` | `e451483d-aae3-807d-8008-54a9bb4658b2`, `e451483d-aae3-807d-8008-54a9bb46baaf` |
| UI-AN-012 | `33a2a659-d0eb-80bd-8008-5af9c379a1aa` | `e451483d-aae3-807d-8008-54a9bc3e9d18`, `e451483d-aae3-807d-8008-54a9bc3e9d33` |
| UI-AN-014 | `33a2a659-d0eb-80bd-8008-5af9c8b501c7` | `3e34a4ec-283e-800b-8008-593261aa6074`, `3e34a4ec-283e-800b-8008-593261aa6076` |

## Final visual QA verdicts

| Board/frame | Final visual verdict |
| --- | --- |
| UI-DATA-008 | pass — Discount mapping is a single compact composition below the stepper; source roles and attribution/coverage are visible with no covered form or summary. |
| UI-DATA-010 | pass — Effective policy and cap/publish actions are fully visible; no full-width board hides the policy form. |
| UI-DATA-013 | pass — Metric certification registry is visible as one complete table composition; no second screen covers the registry. |
| UI-DATA-014 | pass — Certification and evidence/replacement panels are readable together without a covered form or summary. |
| UI-DATA-021 | pass — Method availability registry is visible without a covered table or contract-focus strip. |
| UI-DATA-022 | pass — Method version and robustness/sensitivity remain readable as one detail composition. |
| UI-AN-010 | pass — Discount components, cap diagnostics, exact PVM waterfall, margin/revenue, and Result Trust are simultaneously visible without an obscured chart or table. |
| UI-AN-012 | pass — Immutable result and Trust/disclosure content are visible without a covering W08 layer. |
| UI-AN-014 | pass — Research evidence and limitations/publication blocks are visible without a covered chart or research block. |
| UI-AN-002 | pass — recovery composition remains unclipped and overlap-free; Configuration and capability preflight are both visible. |
| UI-AN-011 | pass — recovery composition remains unclipped and overlap-free; Configuration, Metric groups, and preview right rail remain visible. |

## Global visual-overlap audit

The terminal audit covered 49 pages, 140 contract-backed stable root frames,
and all direct sibling-board pairs. Stable root-frame intersections and
direct-child out-of-bounds lists were empty. The former nine W08 candidates no
longer exist: their stable parents have one `Integrated W08 content / UI-ID`
board and no direct `W08 / …` child.

The geometry pass produced only pre-existing compact-layout candidates. Fresh
exports of every affected frame classified them as intentional, unobscured
composition: a narrow shared border seam between wizard stepper and form
regions on `UI-AUTH-005`, `UI-DATA-008`, `UI-DATA-026`, and `UI-FCST-002`; and
a compact Result Trust control inside the chart card on `UI-CORE-001`,
`UI-DQ-001`, `UI-DQ-004`, `UI-FCST-003`, `UI-FCST-004`, `UI-FCST-006`,
`UI-DASH-002`, `UI-RPT-003`, `UI-ADMIN-001`, `UI-ADMIN-005`, and
`UI-ADMIN-006`. None covers content or introduces clipping. This distinction
was made from fresh exports, not `currentFile.validate()` alone.

Intentional overlay states remain outside the repair scope and visually retain
their expected host/overlay relationship; the scan does not classify them as
the W08 sibling-board defect.

## Commands and observations

| Command or action | Result | Observation |
| --- | --- | --- |
| Pre-write predecessor guard | pass | W08, W08 analytics baseline recovery, and W09 are `accepted`; each terminal evidence record has `verdict: passed`. |
| Canonical-file and revision guard | pass | File ID matched and all nine target structures matched exactly at revision `196` before the first scoped write. |
| Ordered fingerprint before and after | pass | `95be9344f85e907a03b6d53e2f9dba608dd45ea04a5b9ef252d0c9476272b108` both times. |
| Scoped Penpot repair | pass | Retained nine W08 boards and removed exactly eighteen named non-stable covered siblings; no stable ID was edited, renamed, created, or deleted. |
| Product Design visual audit | pass | Individual exports of nine repaired frames, UI-AN-002/011, and every global sibling-geometry candidate were inspected for clipping, covered content, hierarchy, and density. |
| Stable-ID reconciliation | pass | Exactly `110/25/5`; duplicate, missing, orphan, root-collision, and direct-child-out-of-bounds lists were empty. |
| W10 non-goal reconciliation | pass | C25, all six W10 routes, and flow 10 were absent; flow 09 remained present. |
| Penpot file validation and terminal reads | pass | `currentFile.validate()` returned `[]`; two sequential reads remained canonical revision `197`. |
| Route registry and both JSON Schema checks | pass | Registry and both contract documents validate. |
| Delivery-ticket validation | pass | 13 tickets validated before terminal transition; terminal validation is repeated after the transition. |
| `git diff --check` | pass | No whitespace errors. |

## Historical W10 incident

The earlier W10 run observed revision drift from `191` to `192` before it made
any Penpot mutation. That blocker record remains historical pre-write context;
it is neither a recovery modification nor evidence that this recovery changed
W10 scope. The next W10 terminal evidence must retain that distinction.

## Verdict

`passed`. Revision `197` is the repaired canonical baseline. The blocking W08
visual composition defect is closed within its own ticket; W10 may be
reconciled against this terminal baseline before any W10 write.
