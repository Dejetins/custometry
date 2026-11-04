---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "milestone",
  "doc_id": "MS-021",
  "title": "C04 published aggregate report filters",
  "version": "0.1.0",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "WS-004",
    "path": "docs/architecture/planning/directions/DIR-004/workstreams/WS-004.md",
    "version": "0.2.17"
  },
  "direction_ref": "DIR-004",
  "baseline_ref": {
    "commit": "86055ce732640ebe68fd5415a55f7bbde3499181",
    "evidence_refs": [
      ".codex/delivery/evidence/MS-020/MS-020-S01/report.md"
    ]
  },
  "requirement_refs": [
    {
      "source": "custometry-technical-blueprint-ru.md",
      "revision": "sha256:5b7232aaae21d226ac4ba0a05a5f24efcea9ae31d616e3606180c554ff21ecd5",
      "ids": [
        "FILTER-001",
        "FILTER-002",
        "FILTER-003",
        "FILTER-004",
        "FILTER-005",
        "FILTER-006",
        "FILTER-007",
        "FILTER-008",
        "FILTER-009",
        "FILTER-010",
        "FILTER-011",
        "FILTER-012",
        "FILTER-013",
        "FILTER-014",
        "FILTER-016",
        "FILTER-017",
        "FILTER-018"
      ]
    }
  ],
  "decision_refs": [
    "WS-004/DEC-06",
    "MS-021/DEC-01",
    "MS-021/DEC-02",
    "MS-021/DEC-03",
    "MS-021/DEC-04",
    "MS-021/DEC-05"
  ],
  "supersedes_ref": null,
  "execution_ref": {
    "path": ".codex/delivery/ledgers/MS-021.md"
  }
}
---
# MS-021 — published aggregate report filters

## Outcome and authority

Parent [WS-004 v0.2.17](../../directions/DIR-004/workstreams/WS-004.md), existing
whole-workstream delegation and accepted MS-020 authorize this sequential unit.
Sources are FILTER-001–014/016–018, human §6.5, the accepted target pilot/ADR-0007,
MS-019 report authoring and MS-020 aggregate contracts/executor. Mount the verified
count/distinct/ratio capability in genuine published catalog, preview/facets,
block/hierarchy authoring, Apply, immutable Save and reopen.

## Decisions

DEC-01: Semantic supplies a public retail aggregate projection built from its own
published dataset and relationship fields. Publish two immutable count definitions:
observed item rows (line_id grain) and distinct observed products (product_id grain),
using parent Receipt.receipt_date under explicit utc_date/v1/all_observed_rows policy.
Read the actual immutable Semantic publication created_at through its public port;
pin exact UTC observation/knowledge snapshot cutoffs and existing observed date bounds.
Missing/invalid temporal metadata is a capability blocker, never a fabricated clock.
Retail relationship history remains incomplete regardless of transport/accounting.

DEC-02: an explicit receipt-filter/v3 and catalog/preview/facet capability advertise
aggregate support. Preserve v1/v2 DTO bytes and saved readers. Generated consumers
update together. Current Identity/Artifact access composes a trusted aggregate grant;
no child-root endpoint, client completeness/policy claims or private cross-context read.
The same executor serves previews, facets and calculation, with current access checks.

DEC-03: existing report scopes can combine v1/v2/v3 only against matching published
registries and the explicit legacy bridge. Deterministic request-local rebasing handles
aggregate operands/child scopes without rewriting field/metric/policy IDs. Correlated
or aggregate constraints cannot be weakened through child-field replacement. Preserve
locks, links and exact result reuse for presentation-only edits/copies.

DEC-04: extend the current receipt editor with explicit count-condition creation,
registered count/distinct choice, editable row predicates and half-open observation
windows, scalar/scoped/ratio operands and comparison operator. Display units, window,
null/empty/returns/history policy in readable RU/EN language. No browser evaluator.
Keep applied/draft/preview, reset/undo/cancellation and stale response protections.
Existing result evidence displays unknown membership; genuine current retail counts
are unknown under its incomplete-history policy, never fabricated zeros or certified
absence. Boolean combinations may retain independently confirmed root members.

DEC-05: reuse immutable report persistence/result evidence, bounded facets and current
preflight. No data migration, publication/deploy or calendar control changes. Fixed
UTC-date windows are explicitly labeled; financial metrics, relative/intraday windows,
sequences/populations and remaining C04/C05–C11 remain following work, not waived.

## Proof and impact

- AC-01: genuine published count metadata/identity/current Identity/Artifact HTTP
  catalog/preview/facets with independent source evidence and explicit unknown history.
- AC-02: strict old readers and v3 persisted request/result identity; mixed hierarchy,
  stable correlation IDs, locks and presentation-only reuse.
- AC-03: mounted browser count/distinct/ratio/window draft editing, validation/reset/
  undo, real Apply/Save/reload, RU/EN readable limitations and narrow viewport.
- AC-04: focused backend/frontend/static/local checks, independent read-only review,
  synchronized provider/consumer/requirements/UI documentation and immutable evidence.

Contract impact: additive explicit v3 query/catalog capability and generated consumers;
old v1/v2 remain supported and do not silently accept new nodes. Public Semantic
aggregate projection is new; no old projection shape needs an unversioned change.
Existing exact artifact authorization, CAS/replay and calendar setup stay unchanged.
Observed test boundaries must distinguish genuine provider/HTTP, browser and static
proof; none establishes production delivery or complete FILTER-014/C04 acceptance.

## Bindings

One executor, existing read-only reviewer, manual sequential. Plan v0.1.0 accepted
under delegated technical authority on2026-10-07. Triad:
`docs/architecture/planning/milestones/MS-021/plan.md`,
`.codex/agents/generated/MS-021`, `.codex/delivery/ledgers/MS-021.md`.
Maintain parent/source versions, authoring contract, requirement matrix/UI inventory,
generated contracts/indexes and evidence. Preserve retained runtime41746 and prior
accepted evidence. Continue authorized WS-004 after this unit.
