---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "milestone",
  "doc_id": "MS-011",
  "title": "C04 mounted retail filter authoring",
  "version": "0.1.0",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "WS-004",
    "path": "docs/architecture/planning/directions/DIR-004/workstreams/WS-004.md",
    "version": "0.2.7"
  },
  "direction_ref": "DIR-004",
  "baseline_ref": {
    "commit": "86055ce732640ebe68fd5415a55f7bbde3499181",
    "evidence_refs": [
      ".codex/delivery/evidence/MS-010/MS-010-S01/report.md"
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
        "FILTER-016",
        "FILTER-017",
        "FILTER-018"
      ]
    }
  ],
  "decision_refs": [
    "WS-004/DEC-06",
    "MS-011/DEC-01"
  ],
  "supersedes_ref": null,
  "execution_ref": {
    "path": ".codex/delivery/ledgers/MS-011.md"
  }
}
---
# MS-011 — mounted retail filter authoring

## 1. Result and authority

Parent: [WS-004 v0.2.7](../../directions/DIR-004/workstreams/WS-004.md).
The [owner addendum](../../../../../.codex/delivery/evidence/WS-004/owner-continuation-addendum-2026-10-07.md)
authorizes sequential implementation, dependencies, local runtime, tests and fixes.
MS-010 provides real published Receipt fields and current policy but is not mounted.
This stage connects that provider to the existing composer, preserving old queries.
One implementation executor; independent review of security/compatibility changes.

## 2. Decisions and compatibility

DEC-01: Add optional versioned Receipt filter input to analytical queries. Absent
input preserves old identity/values; present input pins registry, expression and
current permission/manifest identity. The existing typed DuckDB engine evaluates
expressions; no browser/Python predicate evaluator. PostgreSQL remains control DB.
Expose permission-filtered searchable fields and bounded authorized facets/preview.
Never return raw membership IDs from preview. The composer separates draft from
applied conditions and persists applied inputs. Show mandatory source/Store ceilings.
Resource policy is trusted server configuration with versioned identity, never client input.
New readers accept old documents; old readers reject new filter inputs rather than
silently discard them. Rollback preserves new bytes and uses compatible readers.

| Boundary | Impact | Required proof |
|---|---|---|
| Query, HTTP, composer persistence | compatible-change for old inputs; new-input old-reader rejection | old/new fixtures, API validation and save/reopen |
| Analytical identity | compatible-change only when absent input remains identical | expression/registry/policy change and layout invariance |
| Access and facets | no permission relaxation | denied/cross-workspace/revoke/empty ceiling before aggregation |
| Browser | additive filter authoring | real preview/apply/save/reopen, errors and stale requests |

## 3. Stage and touch zones

MS-011-S01 owns contracts/semantic and analytics ports, isolated adapter, workspace
orchestration, API composition/router, generated contracts, composer UI, relevant
tests, canonical docs and evidence. Preserve all baseline foreign changes recorded
in preparation. No historical receipt rewrite, production migration, deploy or send.

## 4. Acceptance and proof

- AC-01: authenticated bounded catalog/preview/facets return actual published fields
  and policy-filtered counts; invalid type/version, denied access and stale policy reject.
- AC-02: persisted composer filters affect actual backend results and identities;
  save/reopen retains them; absent-filter queries preserve their previous semantics.
- AC-03: real browser authoring with charts/tables and draft/apply distinction,
  readable applied/system context, error recovery and stale-response protection.
- AC-04: focused contracts/backend/frontend/integration tests, local profile,
  independent boundary review and synchronized evidence/docs all pass.

Use disposable test fixtures; preserve retained runtime/user data. Screenshots
prove appearance only. This stage does not accept relational/sequence/population
C04 obligations or C05–C11. Continue those under existing authority after acceptance.

## 5. Binding and continuation

- plan_doc: `docs/architecture/planning/milestones/MS-011/plan.md`, v0.1.0.
- prompt_pack_dir: `.codex/agents/generated/MS-011`.
- stage_ledger: `.codex/delivery/ledgers/MS-011.md`.
- Repository prompt-pack/v1 validator and exclusive POSIX updater.
- manual_sequential with explicit whole-workstream continuation; no Goal.

Version 0.1.0 accepted under delegated technical authority on 2026-10-07. Existing
product holds remain. Missing implementation is work to perform, not an owner gate.
