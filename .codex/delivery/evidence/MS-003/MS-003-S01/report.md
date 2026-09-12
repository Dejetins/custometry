# MS-003-S01 — governed retail source and analyst session

Milestone: MS-003. Stage: MS-003-S01. Iteration: 1 (resumed after authorized runtime recovery).
Result: implemented and verified at the declared S01 boundary; submitted for receipt-backed acceptance.
Plan: [MS-003 0.2.0](../../../../../docs/architecture/planning/milestones/MS-003/plan.md).
Journal: [MS-003](../../../ledgers/MS-003.md).
Prompt: [MS-003-S01](../../../../agents/generated/MS-003/MS-003-S01.md).
Plan SHA-256: `4a6b1bf2a64a04b74e073bb22e46895795e187be57fe93b6711408069d6e7280` (preserved).

## Delivered behavior and criterion coverage

MS-003/AC-01: the actual unchanged demo PostgreSQL seed `20260716` was read through the readonly connector and production catalog/intake services, producing six raw, six canonical and one protected quarantine artifact. No fake user, quality, catalog or semantic success records were inserted by preparation. The source namespace is `northwind-retail`; the catalog source UUID remains separate.

| Entity | Raw | Canonical | Quarantined |
|---|---:|---:|---:|
| Customer | 1,000 | 1,000 | 0 |
| Product | 120 | 120 | 0 |
| Receipt | 5,000 | 5,000 | 0 |
| ReceiptItem | 15,000 | 14,995 | 5 |
| Store | 20 | 20 | 0 |
| Calendar | 1,830 | 1,830 | 0 |

`retail-report-orphan-product/v1` records the five known product-reference exceptions with raw artifact/key provenance. The canonical gate passes after rechecking keys/references; QualityReport finding details explicitly declare `allow_degraded`. Product relationship coverage is 14,995 / 15,000 (99.9667%); the excluded fraction is 5 / 15,000 (0.0333%). No waiver, duplicate collapse, fabricated Product or seed change was applied. Product/basket coverage stays degraded; unknown business impact/history completeness is not reported as zero or complete.

Excluded item net amounts, by receipt currency/date: EUR 316.62 on 2024-03-07; EUR 34.32 on 2024-09-22; EUR 564.45 on 2024-11-28; EUR 144.91 on 2025-06-15; EUR 174.66 on 2025-08-21. These are measured excluded item amounts, not an asserted business loss or reconciliation to receipt headers.

Independent readonly SQL and canonical Parquet agree on every currency aggregate: EUR 4,977 receipts / 893,057.90 net / 262 anonymous; SEK 23 receipts / 4,361.92 net / 1 anonymous. These include all source statuses and dates, and are preservation evidence, **not** S02's completed/EUR registered report metrics. All 263 anonymous receipts remain without fabricated Customer rows.

Six entity bindings, five qualified one-to-many relationships, separate dimension version keys and `retail-report-current-only/v1` are published together. Store synthetic validity reflects the actual batch observation; supplied Customer/Product validity is retained without historical join claims. Calendar 2020-12-28..2025-12-31 and its exact completeness flags, all stores, dates, currencies, hashes and limitations are available in the Semantic projection. No DSN or SQL is exposed. Artifact dependencies retain raw-to-derived lineage.

MS-003/AC-02 (S01 boundary): production Identity bootstrap/invitation/acceptance creates the setup owner and separate ordinary analyst. Actual HTTP through Vite `/api` proves cookie paths, HttpOnly/SameSite, session reads, Origin/CSRF rejection for analytics mutations, bearer support, setup permission denial, refresh, administrator revocation, logout and re-login. Real database tests prove bootstrap single-winner behavior, invitation/token/password/session rules and cross-workspace denial. Secure cookie configuration is tested at the mounted API boundary; installed HTTPS/browser UI remain S04/S05 proof.

The Identity-owned HTTP adapter supplies cookie authentication and method-appropriate mutation protection to Identity and analytics. Login/logout clear legacy `/identity` and current paths. Access/CSRF use `/`; refresh uses `/api/identity`. Default full-retail extraction and existing bearer/OpenAPI contracts remain supported.

## Safe preparation and S02 inputs

```sh
source scripts/activate-toolchain.sh
scripts/dev up --mode hybrid
uv run --locked python -m apps.worker_data.prepare_retail_report
```

Owned runtime: `.runtime/development/383a7390af`; Compose project `custometry-hybrid-383a7390af`. Safe full publication output: `.runtime/development/383a7390af/retail-report-output.json`. Credentials are only in the mode-0600 `secrets/retail-report.json` beneath that protected runtime directory. Do not copy their contents into prompts, reports, URLs or browser storage.

| Input | Exact ID |
|---|---|
| Workspace | `1af52456-b651-4bd8-9703-f558cd7fd7f1` |
| Setup administrator | `ecb2bd6c-22da-424c-880f-c08ac4997a8f` |
| Ordinary analyst | `37fc7324-3a81-4db6-986e-53a898360e7c` |
| Connection | `d640cd5a-8bf1-4f54-9476-cdd322e7f58f` |
| Catalog source system | `65676f96-de65-4de1-9d3d-a9357fd1a445` |
| Batch | `7f3509cb-4cca-4073-a8fe-d95b3de7d41d` |
| Semantic dataset | `2a5a76a6-9530-4338-9386-0a8f9b9d8df5` |
| Published dataset version | `e81d5594-b690-5863-8650-9f21e1a8db84` |
| QualityReport | `c23cb37a-52b8-5597-8968-81508272b212` |

Source fingerprint: `6b483dbde58acaecf17bcf1ce6d0556dcf102b9522a88663b87d285ac20a7a3d`.
Repeated actual preparation returned the same IDs and fingerprint, with `reused=true`, and verified all 13 artifact hashes. Protected state conflicts, duplicate/null keys, unexpected product/store/receipt references, a mismatched source fingerprint, corrupted committed artifacts and failures during publication are covered by negative tests. No prepared data was reset by testing.

[Artifact reconciliation](artifact-reconciliation.json) lists each immutable artifact ID/hash/count/reference and exact relationship bindings. `PostgresSemanticRepository.get` is a workspace-scoped projection; consumers must resolve current authorization before invoking it. S02 consumes these inputs through owner ports and registers its own metric/result versions. It must preserve the quality evidence, use receipt grain and reject unsupported product/category/brand slicing.

The complete S02 prompt and all five declared current input paths were checked. The report and live runtime outputs exist; S02-owned metrics/results remain intentionally unproduced. The journal has current S02 authority, so receipt acceptance may enable its entry. Manual sequential mode stops after S01; no S02 claim or execution occurs here.

## Validation and proof boundary

All commands ran from the repository root after toolchain activation. [Validation evidence](validation-evidence.json) contains outcomes and current source hashes. The retained [test runner](run_tests.py) creates/upgrades only `custometry_ms003_s01_tests` on the owned control server and runs the destructive existing fixtures there; the prepared database is preserved. [Reconciliation script](verify_artifacts.py) contains the independent source SQL and hash/count checks. Both scripts reference protected runtime files without embedding secrets.

- Focused unit/contract/runtime regression suites: **32 passed**. Identity and analytics OpenAPI fixtures remain equal to providers.
- Real owned database/API suites: **18 passed**, one opt-in prepared HTTP test skipped in this invocation and executed separately.
- Actual prepared HTTP test: **1 passed** through the running Vite/API/database boundary.
- Focused production/runtime Pyright: **0 errors / 0 warnings**; Ruff: **passed**.
- Actual preparation/replay and independent SQL/Parquet reconciliation: **passed**.
- `uv run --locked python -m tools.check --scope local`: **passed**.
- `generate_docs_index`: **passed**, 68 contributor documents; `check_docs_links`: **passed**, 84 documents / 670 links; `git diff --check`: **passed**.

Initial failures were resolved rather than counted as passes: Docker pool exhaustion; missing host artifact-root wiring; old direct-path browser fixtures after the selected refresh-cookie path change; missing OpenAPI auth declarations after dependency refactoring; and strict type errors. No dependency upgrades or reduced assertions were used to obtain a pass.

Observed boundary: actual owned source/control PostgreSQL, committed Parquet/DQ/Semantic publication and Identity HTTP. No browser UI, report persistence, packaged images/HTTPS, VM/LAN campaign, source wizard, historical refresh, workload-scale, release or production claim. S02–S06 remain their declared execution units.

## Compatibility and documentation

| Surface | Classification / evidence |
|---|---|
| Default full-retail / existing semantic artifacts | `compatible-change`: explicit additive profile; existing default suites pass; no old artifacts or schema migrations changed |
| Ingestion request identity | `compatible-change` for matching retries; mismatched connection/source/dataset now explicitly rejected; profile idempotency namespace is required for the new profile |
| Quality/Semantic JSON | `compatible-change`: optional finding details and a separate profile's bindings/summary; old report serialization unchanged when details are absent; existing tests pass |
| Bearer API/OpenAPI | `compatible-change`: accepted existing headers/routes preserved, plus session support on analytics; matching contract tests and HTTP bearer proof |
| Browser cookie path | `breaking-change` for legacy direct-path refresh cookies, intentionally selected by TECH-02; cleanup and re-login required; `/api` session integration verified |
| Hybrid configuration | `compatible-change` within loopback-only development: owned storage/source/Identity configuration; Secure remains the HTTPS setting; production config untouched |
| Rollback | No schema migration; old artifacts remain. Legacy code must not consume the new profile as if it were the old profile; reverting cookie policy requires re-login. No packaged rollback proof claimed |

Runtime contract `doc_version 4` and source adaptation contract `doc_version 2` document only delivered behavior and link reciprocally to this stage. Architecture index navigation was updated. [Immutable documentation snapshots](snapshots/) preserve the exact reviewed versions; the accepted plan's older dependency versions remain its unmodified baseline, with the compatible additive changes assessed above. Product blueprint requirements did not change. No planning-level scope/acceptance changes or new planning artifacts were introduced.

## Owned manifest, foreign changes and recovery

Exact created/modified source/test/doc paths and hashes are in validation evidence. No paths were deleted. New files: preparation entrypoint, shared Identity HTTP adapter, DQ/semantic report-profile modules, three focused test modules, and this stage's report/evidence/snapshots/receipt. Modified files: runner and ingestion model/repository, DQ finding DTO, artifact and semantic repositories, Identity/analytics routers, developer runtime/test, existing prefix-aware Identity fixtures, runtime/source docs and architecture navigation. The journal changes use only the exclusive updater.

Necessary integration hunks beyond narrowly named entrypoints: the Connection Catalog router factory was exposed for production preparation composition; `tests/tooling/test_development_runtime.py` proves the runtime storage fix. These are covered by the prompt's preparation/auth/focused-test zones. No frontend, seed, dependency, migration, installer or release code changed.

Pre-existing foreign changes were preserved: six MS-003 prompt plan-hash annotations; accepted MS-003/WS-002 planning changes and preparation evidence; MAP/DIR/workstream/roadmap/operating-model navigation changes; and the journal's owner-acceptance draft baseline. In the shared architecture index, only the S01 journal/evidence navigation was added. Completed MS-001/MS-002 plan/pack/journal/evidence bytes remain untouched. No branch, worktree, stash, commit, push, merge or deployment was performed.

The original interruption remains in [entry attempt 1](entry-attempt-1.md). After the owner's explicit authorization, exactly two empty networks were rechecked and removed; [recovery authorization](network-recovery-authorization.md) records the action. No volumes, containers, images, other networks or Docker configuration were removed/reset. A separate confirmed Hybrid readiness defect was fixed by supplying the owned artifact root; database/schema readiness already passed. Runtime remains running for the next stage.

Residual limitations: protected runtime files and owned Docker state must remain available; explicit reconciliation is required for conflicting/interrupted setup identity, not automatic adoption/reset. Current-only dimensions and degraded item coverage remain product limitations. Final milestone/user acceptance and installed HTTPS proof are not implied by S01 acceptance.
