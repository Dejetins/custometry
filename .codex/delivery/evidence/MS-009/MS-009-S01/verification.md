# MS-009-S01 local verification

Servicing checkout: `/Users/daniildegtyarev/.codex/worktrees/c67c/Custometry`.
No retained user dataset/runtime was changed. Tests create temporary Parquet inputs.

## Observed checks

- `uv add --package custometry-api 'duckdb==1.5.6'`: passed; installed project-local
  DuckDB 1.5.6. Compared API pyproject and lock against pre-command snapshots:
  exactly one dependency, its package resolution and references added; other
  resolved versions unchanged. Existing dirty dependency/lock work preserved.
- Initial real engine probe: in-memory connection with external access/extensions
  disabled successfully registered Arrow and returned the expected aggregate.
- `uv run --locked --no-sync pytest -q tests/integration/analytics/test_columnar_filters.py`:
  45 passed after resource repair. Initial 36 and then 43 passed before the review;
  those earlier passes did not expose the dictionary expansion defect.
- `uv run --locked --no-sync pytest -q tests/integration/analytics/test_columnar_filters.py tests/unit/analytics/test_workspace_scopes.py tests/contract/presentation/test_composer_scopes.py`:
  72 passed, including current Store/scope regression.
- `uv run --locked --no-sync pyright packages/contracts/semantic/filter_fields.py packages/contracts/analytics/columnar_filters.py packages/analytics_core/infrastructure/columnar_filters.py`:
  0 errors/warnings. First attempts failed on untyped PyArrow and a narrowing issue;
  corrected with an explicit dynamic Arrow infrastructure boundary and normal
  typed compiler narrowing. Public models/compiler use strict project checking.
- Focused `ruff check` for the three modules and integration test passed after
  correcting import placement and removing an unused test import. No lint rule
  disabled; formatting restricted to the four owned files.
- `uv run --locked --no-sync python -m tools.custometry_quality.generate_docs_index`:
  passed, contributor index synchronized.
- `source scripts/activate-toolchain.sh` then
  `uv run --locked --no-sync python -m tools.check --scope local`: passed twice,
  including after dictionary/cancellation repair. This is the local profile,
  not CI/release or runtime deployment proof.

## Engine evidence boundary

Actual tests cover typed exact decimals, known field NULL versus unavailable
observations, Boolean/NOT three-valued results, mandatory authorized row ceiling,
policy-sensitive identity and Boolean order canonicalization, reauthorization/
revocation, forbidden fields/versions/operators/values, parameter injection,
internal identifier isolation, input hash/path/symlink/type/grain checks, resource
preflight, pre-cancel, active native cancellation/deadline, connection cleanup and
recovery, file/network-loading primitives and config/extension restrictions.

The active-interrupt tests instrument the connection with a bounded native workload
before the ordinary generated query; DuckDB interruption itself is real. The Arrow
cancellation test decodes a real batch and signals cancellation at its boundary.
Neither proves hard interruption inside a single native decode or hard RSS limits.

Independent review exposed dictionary expansion: a small valid Parquet can decode
to much larger Arrow storage. Regression uses 10,000 strings of 4096 bytes and
asserts rejection before any dictionary cast. Input now keeps string dictionaries
encoded, preflights expanded bytes columnarly and materializes bounded batches.

Access-port fixtures model admission; there is no mounted production authorization
adapter, registry/facet API, composer editor integration or full C04 evidence here.
Browser testing is not applicable to this isolated stage's unchanged UI/API, and
remains mandatory for the subsequent mounted integration. No performance claims.
