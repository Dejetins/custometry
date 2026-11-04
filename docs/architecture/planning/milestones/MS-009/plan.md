---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "milestone",
  "doc_id": "MS-009",
  "title": "C04 isolated typed columnar execution and input admission",
  "version": "0.1.0",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "WS-004",
    "path": "docs/architecture/planning/directions/DIR-004/workstreams/WS-004.md",
    "version": "0.2.5"
  },
  "direction_ref": "DIR-004",
  "baseline_ref": {
    "commit": "86055ce732640ebe68fd5415a55f7bbde3499181",
    "evidence_refs": [
      ".codex/delivery/evidence/MS-008/MS-008-S02/report.md",
      ".codex/delivery/evidence/WS-004/owner-continuation-addendum-2026-10-07.md"
    ]
  },
  "requirement_refs": [
    {
      "source": "custometry-technical-blueprint-ru.md",
      "revision": "sha256:5b7232aaae21d226ac4ba0a05a5f24efcea9ae31d616e3606180c554ff21ecd5",
      "ids": [
        "FILTER-001",
        "FILTER-003",
        "FILTER-004",
        "FILTER-005",
        "FILTER-006",
        "FILTER-016",
        "FILTER-017",
        "FILTER-018"
      ]
    }
  ],
  "decision_refs": [
    "WS-004/DEC-06",
    "MS-009/DEC-01",
    "MS-009/DEC-02"
  ],
  "supersedes_ref": null,
  "execution_ref": {
    "path": ".codex/delivery/ledgers/MS-009.md"
  }
}
---
# MS-009 — isolated typed columnar execution

## 1. Result, authority and boundaries

Parent: [WS-004 v0.2.5](../../directions/DIR-004/workstreams/WS-004.md).
[Current owner authority](../../../../../.codex/delivery/evidence/WS-004/owner-continuation-addendum-2026-10-07.md)
authorizes this exact v0.1.0 bounded decomposition and sequential implementation.
Before: no project DuckDB execution dependency or safe typed columnar provider.
After: a real isolated DuckDB adapter executes a strictly validated flat Boolean
filter subset on authorized integrity-checked materialized inputs, with three-state
coverage, resource preflight and cancellation. This is substrate, not full C04.

| Evidence | Observation | Gap / resolution |
|---|---|---|
| MS-008 completed journal and S02 report | boundary_verified for Store/date/pairs | preserve old behavior; no general-provider claim |
| Existing LocalAnalyticsArtifactStore | code_observed hash/path checks and row materialization | add isolated columnar input admission, no row-wise filter fallback |
| FILTER-001/003/004/005/006/016/017/018 and human §6.5 | documented normative invariants | prove the declared flat subset on real DuckDB |

| Dependency | Provider / output | Consumer / before | Proof / owner |
|---|---|---|---|
| DEP-01 | approved DuckDB package, Arrow interchange | S01 execution | exact lock diff and local tests; single executor |
| DEP-02 | existing artifact/identity public binding and policy | S01 input admission | no arbitrary path or client authorization assertion; input hash and current policy recheck |
| DEP-03 | workspace resource policy supplied by trusted caller | execution | explicit versioned limits, reject excess before query; no invented product default |

## 2. Decisions and contract impacts

| Decision | Target / reason | Impact / recovery | Proof |
|---|---|---|---|
| DEC-01 | per-operation in-memory DuckDB; generated SQL from closed typed nodes, bound values, internal identifiers only; no external access or automatic extensions | compatible-change to project runtime dependency; old API and persisted results untouched | forbidden reads/writes/extensions, injection and isolation tests |
| DEC-02 | explicit registry/version/policy/input identity and typed admission; fields selected from authorized registry, columnar row ceiling before predicate; distinguish field NULL and unavailable observations | additive public internal contracts; no changes to old v1/v2 serializers | unknown/NOT/AND/OR, exact decimal, forbidden fields/rows and changed policy tests |
| DEC-03 | bounded rows/bytes/depth/nodes/parameters/time/memory/threads, no disk spill; cancellation interrupt and sanitized error codes | trusted resource policy is explicit, no production SLO invented | preflight denials, interrupted operation and connection cleanup |

No new HTTP route, UI behavior, production migration or existing cache identity change
in this milestone. New execution identity pins all supported inputs and dependencies.
Unsupported relational/sequence/population nodes fail closed; they are later work.

## 3. Work and ownership

| Stage | Result | Dependencies | Touch zones / consumer |
|---|---|---|---|
| MS-009-S01 | typed contracts, safe input admission, columnar adapter, real execution tests, independent review | MS-008 terminal; current authority | contracts/analytics, analytics_core infrastructure/application, API dependency, uv.lock, tests and docs; next C04 integration consumes this substrate |

One executor preserves all existing dirty changes; no parallel implementation.
Read-only independent review required for the new security boundary.

## 4. Acceptance and proof

| Criterion | Required observation / S01 proof |
|---|---|
| AC-01 | closed typed versioned expressions and fields; reject unsupported ops/types/versions, arbitrary identifiers and unbounded plans; canonical identity changes for semantic dependencies |
| AC-02 | real Arrow/materialized-input DuckDB execution; exact decimals and Boolean truth tables; NULL policy distinct from incomplete observation; no confirmed membership from unknown |
| AC-03 | workspace/current-policy/field/row checks and artifact integrity before computation; no raw path or user SQL execution; isolation/settings and forbidden operation tests |
| AC-04 | trusted versioned limits; preflight row/byte/depth/node denial; timeout/cancellation and cleanup; sanitized failures without provider data |
| AC-05 | focused pytest, Ruff, strict types, local profile, independent review and synchronized docs/evidence; exact dependency/lock delta inspected |

Real adapter tests are the nearest boundary: this stage exposes no browser/API
behavior, so browser screenshots or existing composer scenarios cannot prove it.
Browser/API save/reopen proof remains mandatory when the later integration mounts
this provider. No full C04, production, performance SLO or release claim.

## 5. Repair and documentation

Necessary dependency/lock/.venv changes are authorized. No destructive data action,
publication, deployment or product-hold change. Preserve immutable accepted plan,
prompt and receipt bytes. Add the bounded provider contract under docs/contracts;
update parent and architecture navigation and generated contributor index. No
credentials, environment dumps, row payloads or sessions in durable evidence.

## 6. Execution binding

- plan_doc: `docs/architecture/planning/milestones/MS-009/plan.md`, v0.1.0.
- prompt_pack_dir: `.codex/agents/generated/MS-009`.
- stage_ledger: `.codex/delivery/ledgers/MS-009.md`.
- profile: prompt-pack/v1, repository validate_prompt_packs/stage_ledger.
- exclusive POSIX updater with exact source digests and session claim.
- manual_sequential with explicit whole-plan continuation; no Goal.

## 7. Decisions and continuation

v0.1.0 accepted by delegated technical decision on 2026-10-07 under the current
owner addendum. No material new business policy selected. After S01 acceptance,
prepare the next bounded C04 provider integration milestone under the same authority:
registry/capability outputs, supported dimensions and temporal/population plans,
then mounted API/browser proof. Full C04 remains open until every required clause
has real execution evidence. Independent C05–C11 work remains authorized.
