---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "milestone",
  "doc_id": "MS-010",
  "title": "C04 published retail flat-filter provider",
  "version": "0.1.0",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "WS-004",
    "path": "docs/architecture/planning/directions/DIR-004/workstreams/WS-004.md",
    "version": "0.2.6"
  },
  "direction_ref": "DIR-004",
  "baseline_ref": {
    "commit": "86055ce732640ebe68fd5415a55f7bbde3499181",
    "evidence_refs": [
      ".codex/delivery/evidence/MS-009/MS-009-S01/report.md"
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
        "FILTER-010",
        "FILTER-017"
      ]
    }
  ],
  "decision_refs": [
    "WS-004/DEC-06",
    "MS-010/DEC-01"
  ],
  "supersedes_ref": null,
  "execution_ref": {
    "path": ".codex/delivery/ledgers/MS-010.md"
  }
}
---
# MS-010 — published retail flat-filter provider

## 1. Result and authority

Parent: [WS-004 v0.2.6](../../directions/DIR-004/workstreams/WS-004.md).
[Owner addendum](../../../../../.codex/delivery/evidence/WS-004/owner-continuation-addendum-2026-10-07.md)
authorizes this exact bounded plan and implementation. One executor; independent
security review. No renewed checkpoint, Goal, publication or deployment.

Before: MS-009 runs real DuckDB with a test authorization port. After: a real
provider resolves published retail Receipt inputs via Semantic/Artifact public
ports and current Identity permissions, returns a versioned non-PII field catalog
and executes supported expressions without row-wise Python filtering.

| Evidence / dependency | Observation | Required resolution / owner |
|---|---|---|
| MS-009 accepted journal | boundary_verified isolated adapter | reuse exact input/engine contracts |
| PostgresSalesSemanticRepository.sales_projection | code_observed published retail profile, immutable bindings/capabilities | Semantic publishes explicit bounded field versions |
| SalesArtifactStore | code_observed committed workspace manifests; current read path materializes rows | add public admission-only method, do not read private context tables from Analytics |
| ResourceAccessPort | code_observed current object permission and Store ceiling | composition adapter checks read/run and applies mandatory Store ceiling on Receipt |

Scope is the existing retail-report/v1 Receipt Store/date/status/currency fields.
No inferred channel or PII field. Unsupported dimensions/history/relational nodes
remain explicit C04 gaps. Existing workspace/composer/report paths unchanged.

## 2. Decisions and impacts

| Decision | Change / reason | Compatibility / recovery | Proof |
|---|---|---|---|
| DEC-01 | Semantic owns explicit bounded field catalog/version; real publication pins dataset and mapping | additive provider projection, no old serializer change | allowed fields/version stability and unavailable profile |
| DEC-02 | Artifact owner admits committed workspace/entity/content binding to a server-only materialized reference | additive port; no Analytics private table reads, no migration | cross-workspace/uncommitted/hash rejection on actual PostgreSQL |
| DEC-03 | apps/api composition adapter combines public Identity/Semantic/Artifact ports and trusted resource policy | not mounted yet; no global defaults, SQL or client grant | real current access/revoke and Store ceiling, no test allow-all provider |

No public HTTP endpoint/UI/persistence change. Resource policy is explicitly
supplied by trusted composition/test harness, never selected by client. Empty
allowed Store set yields empty membership. Existing artifact lifecycle remains
owner; engine repeats admission/current-policy check before delivery.

## 3. Work allocation

MS-010-S01: public admission/catalog contracts, owner implementations, composition
adapter and real disposable PostgreSQL/source/artifact integration test. Touch
contracts, semantic_model, artifacts, API analytics composition, tests/docs/evidence.
MS-009 source changes only for an exposed integration defect with focused reproof;
its accepted evidence remains historical. Single writer preserves foreign changes.

## 4. Acceptance

- AC-01: genuine published retail field catalog with stable IDs/version/dependencies;
  only supported non-PII fields; unavailable capability rejects, no invented fields.
- AC-02: artifact admission checks workspace, committed state, entity/hash and
  produces only a verified manifest reference through the owner public port.
- AC-03: current resource permission and Store row ceiling drive actual DuckDB
  execution on ingested published Receipt Parquet; exact expected membership/counts;
  empty ceiling, cross-tenant and revoke/change fail safely.
- AC-04: real disposable PostgreSQL/source/Identity/artifact integration (no retained
  DB truncation), focused tests/types/Ruff/local gate and independent review.

This port-only unit has no mounted HTTP/UI behavior; integration tests are its real
boundary, not proof of browser save/reopen. Such proof is required when mounting.
Full C04, sequences/populations/comparisons and C05–C11 are not accepted here.

## 5. Repair and documentation

Reversible implementation/owned disposable runtime setup is authorized. No new
business semantics, destructive retained-data action, migration or production.
Use existing local PostgreSQL image; do not print credentials or provider rows.
Keep local contract current, link parent/child and indexes, preserve old claims.

## 6. Execution binding

- plan_doc: `docs/architecture/planning/milestones/MS-010/plan.md`, v0.1.0.
- prompt_pack_dir: `.codex/agents/generated/MS-010`.
- stage_ledger: `.codex/delivery/ledgers/MS-010.md`.
- prompt-pack/v1 repository validator/receipt; existing exclusive POSIX updater.
- manual_sequential with current whole-plan continuation, no Goal.

## 7. Decisions and continuation

v0.1.0 accepted by delegated technical decision under WS-004 owner authority on
2026-10-07. After this provider is verified, mount real catalog/preview/apply and
persisted composer filter inputs, then expand required typed relational/window/
population execution. Do not confuse a provider subset with complete C04.
