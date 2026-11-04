---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "milestone",
  "doc_id": "MS-023",
  "title": "C04 published customer event provider",
  "version": "0.1.0",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "WS-004",
    "path": "docs/architecture/planning/directions/DIR-004/workstreams/WS-004.md",
    "version": "0.2.20"
  },
  "direction_ref": "DIR-004",
  "baseline_ref": {
    "commit": "86055ce732640ebe68fd5415a55f7bbde3499181",
    "evidence_refs": [
      ".codex/delivery/evidence/MS-022/MS-022-S01-R1/report.md"
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
        "FILTER-013",
        "FILTER-014",
        "FILTER-015",
        "FILTER-016",
        "FILTER-017",
        "FILTER-018"
      ]
    }
  ],
  "decision_refs": [
    "WS-004/DEC-06",
    "MS-023/DEC-01",
    "MS-023/DEC-02",
    "MS-023/DEC-03",
    "MS-023/DEC-04",
    "MS-023/DEC-05"
  ],
  "supersedes_ref": null,
  "execution_ref": {
    "path": ".codex/delivery/ledgers/MS-023.md"
  }
}
---
# MS-023 — published customer event provider

## Outcome, authority and current evidence

[WS-004 v0.2.20](../../directions/DIR-004/workstreams/WS-004.md) and whole-workstream
technical delegation authorize the next C04 backend integration. MS-022-S01-R1 proves
typed sequence execution over real synthetic Parquet. Genuine retail publication
already carries Customer, Receipt, ReceiptItem artifacts, UTC receipt_datetime and
current-only Customer→Receipt nullable and Receipt→ReceiptItem nonnullable mappings.
It does not certify business/property history. Existing report filters remain rooted
at Receipt and must not silently change grain. FILTER-001–006/013–018, human §6.5 and
the accepted bounded-context map govern the new public provider/HTTP boundary.

## Decisions

DEC-01: Semantic supplies a separate published customer-events projection from its
own immutable retail publication. Reuse exact artifact hashes/namespace and existing
receipt/item meanings; add Customer source/customer/version identity and Receipt
customer_id with explicit published current-only policy. Register observed receipt
rows at native recorded receipt_datetime (UTC microseconds), all observed rows,
not a fabricated purchase/status-transition event. Pin exact publication created_at,
observed date extent and current-only limitations. Event and relationship completeness
remain false regardless of transport/accounting flags. Do not publish customer PII
attributes, inferred dimension history, lifecycle transitions or certified absence.

DEC-02: introduce an additive nullable relationship capability, leaving old semantic
relationship DTOs unchanged. The published Customer edge allows null customer_id as
an unlinked receipt; required namespace keys stay nonnull. Nonnull missing references
still fail. Unlinked receipts never become a fabricated customer or root member.
No old provider/grant is silently upgraded to nullable semantics.

DEC-03: current Identity resolves analysis.read/run and store ceilings; Artifact
admission verifies each immutable input. Customer root universe is explicitly the
current published customers with at least one authorized observed receipt. Enforce
that mandatory semijoin inside the same SQL plan, before membership/count delivery,
using a new trusted root-restriction grant. Receipt row ceilings carry store policy;
item predicates inherit a correlated authorized receipt. Apply no browser/Python
customer-ID collection or client-supplied grant/completeness. Root restriction,
nullable policy and current evidence enter identity and final access recheck.

This explicit observed-customer universe avoids exposing customers tied only to
forbidden stores. It does not claim the complete Customer population or all segment
universe policies; those remain later population-provider work. Preserve exact old
grant/request identity when the new root restriction is absent.

DEC-04: add separately versioned customer-event catalog and count-only preview HTTP
capabilities, server-bound to current workspace/actor/root Customer. Offer authorized
field/event/relationship metadata, exact cutoffs and visible mandatory universe/
store/current-history limits. Never expose membership IDs, raw rows or private paths.
Request accepts only typed sequence expression with matching published registry and
event pins; old receipt v1/v2/v3 endpoints remain unchanged. GET reauthenticates; POST
requires CSRF/current authorization and supports cancellation. Generate the client
contract if exposed through the existing composer router, but do not mount UI yet.

DEC-05: keep Semantic→Analytics contracts→API composition ownership, shared executor
and immutable storage. No private cross-context table reads, new service, migration,
calendar setup, retained-runtime rebuild or production/deploy action. Real provider
and HTTP tests use an owned fresh PostgreSQL/source/publication fixture. Customer
cohort projection into saved receipt reports and mounted editor form the next unit.

## Proof and impact

- AC-01: actual published native time/event/Customer edge and Artifact input, independent
  source SQL for authorized observed customer universe and positive ordered events.
- AC-02: nullable/unlinked and required/nonexistent keys, mandatory root/child store
  ceilings, empty access, current-policy changes, current-only unknown absence and
  exact identity are verified at real DuckDB/provider boundaries.
- AC-03: authenticated count-only catalog/preview HTTP, server-bound actor/workspace,
  CSRF/revocation/forged-definition/old-endpoint denial and genuine published meaning.
- AC-04: focused old/new/static/local checks, independent read-only review, synchronized
  contracts/matrix/index/generated consumers and immutable evidence/journal transition.

Compatible additive nullable relationship, root restriction, public Semantic projection
and explicit HTTP/client capability; no widening of old DTOs or saved receipt payloads.
Rollback leaves old endpoints/providers intact and removes unmounted new consumers;
no data migration. Tests do not establish UI, complete Customer universe, full FILTER-015,
C04 or C05–C11 completion. MS-016 company-calendar policy and C10 latency work remain.

## Bindings

Plan0.1.0 accepted under existing delegated technical authority2026-10-07. One executor
and existing read-only reviewer. Triad: this plan, `.codex/agents/generated/MS-023`,
`.codex/delivery/ledgers/MS-023.md`; journal alone owns execution status. Preserve prior
receipts/reconciliation and retained41746. Continue authorized WS-004 after acceptance.
