# MS-017 verification

Servicing checkout `/Users/daniildegtyarev/.codex/worktrees/c67c/Custometry` only.
Retained runtime41746 unchanged. No API/browser or production actions in this stage.

- `uv run --locked pytest tests/integration/analytics/test_relational_filters.py tests/integration/analytics/test_columnar_filters.py -q`:85 passed in0.57s.
  Actual temporary Parquet and native DuckDB; trusted access grants are synthetic.
  Covers same-row vs independent scopes, nested relationships, root grain, complete/
  incomplete/null truth, Boolean normalization, old-reader v2 rejection, typed field/
  scope/registry/relationship denial, current-grant change, mandatory ceilings,
  duplicate/orphan/null keys, fan-out/work/row/byte/depth/node/value limits, integrity,
  actual native interruption/deadline cleanup and successful recovery.
  Existing flat tests retain hostile input/path/SQL/external-IO/resource coverage.
- Independent review identified a stricter per-input policy being replaced by global
  quotas and omitted from identity. Four new regressions failed before repair and
  passed afterward: row/byte/node limits and resource version fingerprint. An empty
  grant also now produces the declared binding error with its own regression.
- Focused Ruff and Pyright on changed contracts/adapters/tests:pass, zero type errors.
- Generated docs index, `check --scope local` and `git diff --check`:pass.
  Local is the observed gate profile; no CI/release claim.

The source retail publisher declares unknown business-history completeness and has
quarantined items. Synthetic complete-scope tests do not override that publication.
The next genuine adapter must carry unknown absence into preview and persisted result
meaning. No full FILTER-013/016–018 or complete C04 proof follows from this foundation.
