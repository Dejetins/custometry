---
{
  "schema_version": "custometry-planning/v1",
  "framework_ref": {
    "path": "docs/architecture/planning/framework-v1/README.md",
    "version": "1.0.0"
  },
  "artifact_kind": "milestone",
  "doc_id": "MS-008",
  "title": "C04 supported-provider scope and comparison foundation",
  "version": "0.1.0",
  "planning_status": "accepted",
  "language": "en",
  "parent_ref": {
    "id": "WS-004",
    "path": "docs/architecture/planning/directions/DIR-004/workstreams/WS-004.md",
    "version": "0.2.3"
  },
  "direction_ref": "DIR-004",
  "baseline_ref": {
    "commit": "86055ce732640ebe68fd5415a55f7bbde3499181",
    "evidence_refs": [
      ".codex/delivery/evidence/MS-007/MS-007-S01/report.md",
      ".codex/delivery/evidence/MS-008/preparation/provider-inspection.md"
    ]
  },
  "requirement_refs": [
    {
      "source": "custometry-technical-blueprint-ru.md",
      "revision": "sha256:5b7232aaae21d226ac4ba0a05a5f24efcea9ae31d616e3606180c554ff21ecd5",
      "ids": [
        "ANALYTICAL-DOC-006",
        "COMPARE-001",
        "COMPARE-004",
        "COMPARE-005",
        "COMPARE-006",
        "COMPARE-008",
        "COMPARE-010",
        "FILTER-001",
        "FILTER-003",
        "FILTER-004",
        "FILTER-008",
        "FILTER-010",
        "FILTER-012",
        "FILTER-017",
        "BLOCK-BUILDER-004",
        "BLOCK-BUILDER-005",
        "REPORT-018"
      ]
    }
  ],
  "decision_refs": [
    "WS-004/DEC-06",
    "MS-008/DEC-01",
    "ADR-0007"
  ],
  "supersedes_ref": null,
  "execution_ref": {
    "path": ".codex/delivery/ledgers/MS-008.md"
  }
}
---
# MS-008 — C04 supported-provider foundation

## 1. Result, authority and boundaries

Parent: [WS-004 v0.2.3](../../directions/DIR-004/workstreams/WS-004.md).
[Owner continuation](../../../../../.codex/delivery/evidence/WS-004/owner-continuation-2026-10-07.md)
authorizes this exact v0.1.0 technical decomposition and sequential acceptance.
One executor, independent read-only review; no Goal or repeated owner checkpoint.

Before: C03 authors hierarchy but each block embeds independent period/store/grain
inputs; inherited origins and pair comparison are absent from composer. After:
versioned scope bindings and shared defaults resolve through the hierarchy, expose
effective/overridden/locked origins, validate links, and drive supported block
results and selected-pair comparison through existing Analytics ports.

This is a foundation milestone, NOT whole C04 closure. The accepted parent requires
complete composer-facing provider integration. General fields/registry/facets,
correlated expressions, sequences, aggregates, relative windows, population bindings,
previous/custom-period and other unsupported comparison modes remain unfulfilled
blocking dependencies. They are neither waived nor mocked; future C04 work must
satisfy them before the outcome is called complete. Focus drafts remain C09,
template/interaction semantics C05, generic Pivot C06, export channel parity C09/C11.

| Input | Observed evidence | Consequence |
|---|---|---|
| C03 | [report](../../../../../.codex/delivery/evidence/MS-007/MS-007-S01/report.md), accepted [journal](../../../../../.codex/delivery/ledgers/MS-007.md) | stable hierarchy, history, exact-save/access and block state |
| Existing Analytics/semantic ports | [provider inspection](../../../../../.codex/delivery/evidence/MS-008/preparation/provider-inspection.md) | only date/store and existing two temporal modes/pair may execute |
| FILTER/COMPARE/ANALYTICAL-DOC machine and human blueprints | exact metadata IDs; machine 14.0 precedence | user scopes cannot weaken security/source/system restrictions |
| Authoring/Web source contracts v20/v29 | canonical docs under docs/contracts and docs/architecture/ui | additive versioned rollout; preserve omitted metadata and old reads |

## 2. Decisions

| Decision | Target and reason | Impact / recovery | Proof |
|---|---|---|---|
| DEC-01 scope envelope | Optional versioned document scope configuration; typed store-set expressions, shared period/grain/calendar/comparison and explicit overrides; node IDs target document/chapter/page/section/block | additive prerelease composer contract; absent field stays omitted, legacy queries retain meaning | strict shape, refs/cycles, old roundtrip/hash |
| DEC-02 resolver | Presentation resolves structural ancestry and linked-target DAG; Analytics validates provider inputs and current capabilities. Filter intersection order: security/system/metric/source then document/chapter/page/section/block. Replace only an explicitly replaceable unlocked user field, never a trusted constraint | new public scope contract; no cross-context private access or browser evaluator | deterministic resolution/origins, forbidden override and nested DAG tests |
| DEC-03 identity | Server derives effective query and scope dependency digest; Analytics normalized request/result identity includes digest only for new scoped requests. Browser keys include scope changes but not unrelated presentation | compatible old identities; no client hash trusted as authorization; old snapshots unchanged | hash changes, safe reuse, save/verify parity and stale guards |
| DEC-04 capabilities | Explicit provider/version, supported dimension/operators/grains/calendars/modes and blockers. Existing metric eligibility is returned as locked provenance. No fabricated channel/population/estimate | provider output remains authoritative; unsupported request blocks before Run | malformed/capability/permission denial, no compute on preflight |
| DEC-05 comparison | Per-block temporal inherit/override; selected pair uses existing compare/verify public port, exact results and compatibility reason codes. No client totals or periods | existing immutable comparison artifacts; source/result mismatch fails closed | pair incompatibility/revocation, temporal parity, snapshot/result identity |
| DEC-06 UI | Shared defaults and scope editor in existing composer, explicit inherited/overridden/locked summary, linked targets; no global compute step. Pure scope draft edits do not auto-publish. Apply remains selected-block and Save has no compute | current C02 request/dirty/reconnect semantics retained; native controls/history and RU/EN | real API-backed browser editing, cancel/stale, reopen and unchanged layout identity |

Security restrictions are server-resolved and never stored as editable user claims.
C03 presentation locks do not replace data policy. New locked user bindings cannot
be silently bypassed by child replacement; structural authoring locks still apply.
Unsupported provider nodes receive actionable blockers; no AST node is dropped.
No new engine, database migration, dependency or external runtime is introduced.
General preflight resource policy is a provider dependency; do not invent budgets.

## 3. Ordered work and ownership

| Stage | Result | Dependencies | Owned zones / consumer |
|---|---|---|---|
| MS-008-S01 | Strict scope/default/override contracts, deterministic hierarchy/DAG resolver, provenance and compatibility tests | C03 accepted | packages/contracts, Presentation domain/application pure resolver, focused tests and docs; consumed by S02 |
| MS-008-S02 | Mounted API/preflight/result identity integration, scope/pair UI and real disposable proof | S01 accepted | Analytics normalize/public port adapter, reports API, Web composer, generated clients, tests, docs/evidence |

One writer; preserve all foreign changes and completed receipts. Both stages use
independent review before acceptance. General provider expansion is not smuggled
into S02; absent required capabilities remain explicit C04 blockers in final report.

## 4. Acceptance and proof allocation

| Criterion | Proving stage / required observation |
|---|---|
| AC-01 | S01: versioned closed scope/default/binding shapes, valid hierarchy refs, unambiguous ordering and linked-target DAG; reject cycles/duplicates/dangling refs |
| AC-02 | S01: deterministic effective context and provenance for all five scopes; supported Boolean store-set semantics, explicit inheritance/replacement, immutable system/source constraints; unit/contract negative tests |
| AC-03 | S02: authoritative effective query used by Apply/Save/reopen/result verify, new identity includes resolved dependencies, old omitted schemas/hashes stay compatible, invalid/forbidden input blocked before run |
| AC-04 | S02: explicit capability/preflight and locked eligibility summary, shared defaults/local override and selected pair consume existing server calculation and immutable comparison, no fabricated unsupported channels/estimates |
| AC-05 | S02: real API/browser scope edits/linked targets/Undo/Save/reopen, stale cancellation and no accidental compute; RU/EN/native keyboard smoke, existing C02/C03 regression |
| AC-06 | Both: focused types/tests, local profile, independent review, exact report/receipt and synchronized documentation; final report enumerates open C04 provider clauses |

S01 tests are sufficient only for pure contracts/resolution and cannot prove UI or
live authorization. S02 requires isolated real PostgreSQL/API/browser proof through
the existing harness (58147/41747). Retained runtime/data on 41746 stay untouched.
No publication/deployment claim. Compiler checks may reuse unchanged evidence.

## 5. Repair, rollback and documentation

Technical reversible implementation and repairs are delegated. Preserve old v1/v2
and C02/C03 exact snapshot bytes; new scoped documents require new reader capability.
Never strip scopes for old clients. Snapshot bound docs before changing versions.
Update analytical-authoring contract, Web source contract and Russian UI inventory
only as their behavior changes; update parent/child links, indexes and stage evidence.
Credentials/provider payloads remain outside durable evidence. New product semantics,
dependencies/installations, publication or production actions need covering authority.
Do not mistake an unavailable provider for owner rejection of the accepted plan.

## 6. Execution binding

- plan_doc: `docs/architecture/planning/milestones/MS-008/plan.md`, v0.1.0.
- prompt_pack_dir: `.codex/agents/generated/MS-008`.
- stage_ledger: `.codex/delivery/ledgers/MS-008.md`.
- profile: prompt-pack/v1; repository validate_prompt_packs and stage_ledger.
- existing POSIX exclusive updater; live source-digest preflight, claim and receipts.
- manual_sequential under owner whole-plan continuation; no direct ledger writes.

## 7. Decisions and continuation

| Version | Decision / authority |
|---|---|
| 0.1.0 | 2026-10-07: bounded C04 foundation accepted under WS-004/DEC-06; full C04 obligations remain open where provider-dependent |

After S01, preflight and claim S02 under existing delegation. After S02, inspect
remaining C04 provider outputs and resolve their concrete dependency path. Do not
report C04/WS-004 complete or silently advance dependent acceptance over missing
required semantics. Independent authorized work may continue without fabricating
provider completion; canonical journal owns only this milestone's execution state.
