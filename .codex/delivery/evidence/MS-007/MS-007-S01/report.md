# MS-007-S01 — C03 hierarchy and reversible layouts

Status: technically complete within the accepted C03 boundary. Canonical acceptance
and execution state belong exclusively to the receipt-backed stage journal.

## Result and ownership

The composer now manages optional chapters, pages, nested sections and blocks through
immutable commands. Rename, reorder, group/move, independent copy with fresh IDs and
origin, hide/lock/unlock, delete and bounded Undo/Redo retain analytical identity.
Grid/flow/narrative layouts, density and dashboard/workbook_report/narrative_research presentation
profiles use the shared renderers. Pointer drop has native command equivalents.
Compatible moves preserve custom grid geometry; layout conversion normalizes it.

Searchable grouped tabs and all-pages navigation mount only the active page. Exact
snapshot links pin the selected page and omit hidden content and author controls.
Current permissions, creator checks, immutable artifact/CAS/replay and per-block
Apply remain unchanged. Structural commands never call Analytics.

Owned additions: composer-structure commands/tests, ComposerStructure controls,
strict optional metadata and tests. Owned changes: composer DTO/service capabilities,
client/schema generation, ComposerWorkspace/Builder/state/copy/CSS, small scoped
PilotDocument page-navigation integration, integration/browser tests and canonical
documentation. Foreign dirty files/hunks are preserved; no broad ownership claim.

## Criteria and observed evidence

| Criterion | Proof |
|---|---|
| AC-01 | Strict metadata/profile DTO and nested serializer tests; omitted fields retain old payload/replay identity, explicit false/null retained; real API old snapshot byte equality |
| AC-02 | 9 structure tests cover identity/lineage, graph mutation, inherited locks, order, deletion/history, nested movement; real browser creation/copy/group/hide/lock/Undo/Redo |
| AC-03 | Validated placement/collision/reading order and custom subtree geometry regression; real pointer target assertion, command resize/density and layout changes; no recomputation |
| AC-04 | Keyboard/search/all-pages/overflow and active-page-only mounting, saved page preview, hidden reader content; RU/EN 200% CSS zoom viewport checks and inspected captures |
| AC-05 | Owned PostgreSQL/API revision/replay/exact snapshot and real browser save/reopen, same result references and no extra Apply; C02 lifecycle regressions retained |
| AC-06 | Focused Python/Web/types/generated checks, disposable browser/API, local profile, independent review and synchronized canonical docs/evidence |

[Verification](verification.md) records tests, repairs, captures and limits;
[independent review](review.md) records closed findings. Final Presentation suite:
113 passed (0.70s). Focused Web combined run: 37 passed; final geometry regression
expanded the structure suite to 9 passing tests (the other 29 retain prior evidence).
TypeScript, Ruff and strict Pyright passed. Real owned API: 1 passed (9.32s).
Combined browser: 6 passed (39.9s); final affected C03 scenario: 1 passed (12.3s).
RU/EN stronger viewport checks: 2 passed (10.3s). Unchanged compiler C01 evidence
is reused. Local profile and receipt bindings are checked before journal acceptance.

Relevant implemented clauses: ANALYTICAL-DOC-001/002/003/005/007/010/012/014/015,
DASHBOARD-006, REPORT-001/018 and bounded A11Y-001/005 behavior. This stage does not
claim complete requirement-family acceptance beyond its selected clauses.

## Compatibility and continuation

Schema/browser: compatible-change for reading existing snapshots; additive prerelease
composer evolution requires generated clients deployed together, with no old-writer
forward compatibility claim. Legacy v1/v2 payloads and renderer remain intact.
Persistence/migration and Analytics identity: none. Presentation hide/lock are not
ACL. Profiles select composition only; Research lifecycle, live Dashboard refresh,
publication and additional content remain C07/C08. History retains 50 transient
steps until Save, without imposing a pages/blocks cardinality cap.

Documentation: analytical-authoring contract v20, Web source contract v29, Russian UI
inventory, WS-004 v0.2.2/MS-007 links, architecture/contributor indexes. Bound v19/v28
sources preserved in preparation evidence; accepted C01/C02 artifacts unchanged.

Proof is local disposable infrastructure only. CSS zoom is not native browser zoom;
assistive technology, full accessibility and 100x30 resource qualification remain C10.
No installation, production migration, publication, deployment or retained user data
writes. After acceptance, continue C04 scopes/comparison under existing delegation.
