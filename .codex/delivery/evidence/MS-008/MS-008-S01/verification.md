# MS-008-S01 observed verification

Activated repository toolchain; commands used `uv run --locked --no-sync`.
- Focused scopes: 22 passed in 0.12s.
- Presentation contract/unit suites: 135 passed in 0.65s, including existing C01–C03.
- Strict Pyright on four new runtime files: 0 errors, 0 warnings.
- Ruff on four runtime files and new scope tests: pass after formatting new files.
- `python -m tools.check --scope local`: PASS, observed=true.
- Docs index generation and `git diff --check`: pass.

Tests cover all five scope levels and nested sections, explicit replacement and
source intersection, context inheritance/locks, direct linked expression semantics,
DAG self/cycle/dangling/kind/ID/order failures, Boolean empty/complement semantics,
forbidden values in all branches, unsupported AST denial, dataset mismatch at both
boundaries, stable normalized hash under Boolean reorder/layout changes, semantic
hash changes, exact empty-scope old query and strict JSON roundtrip/schema.

First Pyright run identified generic empty factory/set inference, fixed with typed
factories. First test lint found compact multi-statement lines, fixed by formatting
only new files. Self-review added explicit dataset pin/rejection and stable effective
binding sorting; focused and full checks above ran after that change.

No new API or browser behavior is mounted in S01. No test claims current permission
resolution, database durability, general registry/evaluator or supported UI. Those
are S02/provider obligations. No dependency install, retained-runtime/data write,
publication, production migration or deployment.
