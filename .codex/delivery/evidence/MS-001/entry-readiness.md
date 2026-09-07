# MS-001 entry-readiness evidence

This immutable preparation evidence supports the accepted [MS-001 plan 1.1.0](../../../../docs/architecture/planning/milestones/MS-001/plan.md) and its [canonical journal](../../ledgers/MS-001.md). It is not another execution-state register or a product-stage receipt. The user authorized final working documents, the ready pack and publication through a technical branch to main on 2026-09-07. The five product stages remain unstarted.

## Verified capability

<!-- stage-ledger-capability:v1 -->
```json
{
  "mechanism": "custometry-stage-ledger/v1",
  "result": "pass",
  "implementation": [
    {
      "path": "../../../tools/custometry_quality/stage_ledger.py",
      "sha256": "dc0089c21db2e95d6160fe096b57a814379e0a74a7536727fc4f7a339d981788"
    },
    {
      "path": "../../../tools/custometry_quality/prompt_pack_validation.py",
      "sha256": "e642bc4d323607c391d8fb42e2e6179d52e87c085c4bd194f6713101dd5da688"
    },
    {
      "path": "../../../tools/custometry_quality/validate_prompt_packs.py",
      "sha256": "cf46ea007ca0619cd22086517fd30f5047d0ab71bf6fd0fd9a229320a684fe49"
    },
    {
      "path": "../../../tests/tooling/test_stage_ledger.py",
      "sha256": "596798a1120f44fd917b5a1771a9f393dd3e9ab37a3bcbf911e4f0035a8bff05"
    }
  ]
}
```

The bindings identify the implemented local updater, its portable schema validator,
source gate and focused tests. Commands use the checked-out source and the locked
Python environment. No hypothetical lock or uninstalled executor is selected.
Availability and ownership are rechecked under the actual lock at stage entry.
The accepted [CLI contract](../../../../docs/architecture/tooling-gates.md#7-stage-journal-transactions)
defines one local POSIX Git checkout, a persistent lock inode, atomic replacement,
private session ownership and explicit rejection of stale or foreign claims.
The [adapter](../../../AGENTS.md) selects it for milestone execution.

## Observed implementation checks

- `uv run --locked --offline --no-sync pytest -q tests/tooling/test_stage_ledger.py`: 18 passed. Actual subprocess contention admits one claimant; process death releases the transaction lock while durable ownership persists; stale writes, foreign sessions, changed bound files and stale receipt evidence fail without changing the journal. A two-stage fixture exercises pause/resume, successor entry and final user acceptance. A failed atomic replacement preserves the previous bytes.
- Focused `ruff check` on the three new tooling modules and test: passed.
- Focused `pyright` on the same paths: zero errors, warnings or informational diagnostics.
- Tests use disposable Git fixtures. The actual MS-001 journal is not claimed or activated.

## Proof boundary and retained limits

The updater provides local cooperative concurrency, source/receipt binding and
explicit lifecycle operations. It cannot establish the truth of a test report or
user decision; the runner must inspect those inputs. Separate checkouts and
network/distributed execution need an explicitly supported coordination mechanism.
No force-steal, direct ledger edit, invented recovery, public delivery or product
runtime proof follows from this evidence. Product timings remain future S04 data,
with the accepted comparison protocol and numeric-budget limits unchanged.

The existing deleted retired Figma prompt is a foreign working-tree change and
is excluded from this publication.


## Independent review and correction evidence

Cold-head review: completed. Mode: independent read-only subagent, using the
installed `architecture-review/references/cold-head-plan-prompt-pack-review.md`.
Scope: plan, all five prompts, journal/capability, updater/validator/tests, direct
adapter/tooling and parent/index links. Initial verdict: Block. Findings: one High
(later successor advancement unavailable) and two Medium (lost input prevented
pause/block; path aliases allowed receipt reuse). All three were repaired with
focused regression tests. Local follow-up verdict: Release after fixes; findings
resolved/unresolved: 3/0. A second independent review was not run.

The added tests observe `accept(next=false) -> advance -> claim` while preserving
the accepted row and receipt, both pause and block after a required file disappears,
and rejection of replaced historical receipts through relative, dot and absolute
path aliases. Focused tests: 18 passed; Ruff passed; Pyright: zero diagnostics.
Earlier tooling suite before these corrections: 109 passed. Final suite and
source gates are rerun after the corrections and binding refresh below.

## Final local readiness verification

After all three review corrections, `uv run --locked --offline --no-sync pytest
-q tests/tooling` passed **115 tests**. `python -m tools.check --scope local` passed.
The actual `stage_ledger preflight` for `MS-001-S01` returned `status: pass` and
`proof_boundary: entry-inputs-and-exclusive-updater-availability` without a claim.
The installed Prompt Manager helper also passed `--check entry --stage MS-001-S01`.
`git diff --check` passed. Capability bindings are refreshed after this evidence
update; the final source profile and preflight are checked again before commit.

Result: accepted working documents and `entry_ready` for **MS-001-S01 only**.
All five stages remain pending, with null claims and no product-stage receipts.
The journal stays `draft` until the runner performs the first actual claim.
Publication uses a temporary branch based on `origin/main`, excluding pre-existing
local-only governance history and the foreign working-tree deletion. Those local
commits are preserved when bringing the published result back into local main.

## Publication-tree verification

The technical branch contains only the 18 task-owned paths above `origin/main`.
On this exact publication tree, `python -m tools.check --scope ci` passed and
`python -m pytest -q tests/tooling` passed **114 tests**. The local-only governance
history includes one additional existing test, explaining its earlier 115 total.
An initial attempt to link the existing virtual environment into the temporary
checkout failed the ownership-path gate and test import resolution. The symlink
was removed; using the existing locked environment explicitly and `python -m`
from the publication checkout passed both checks. No dependency installation,
credential change or source-gate waiver was used. Hosted CI remains a separate
publication check on the actual PR SHA.

The plan baseline is bound to published commit `f9f39a75994d2f7a8e8d7a75df293c35579f842d`. A direct Git comparison confirms that the previously inspected local commit has identical application/package/deployment/migration/workflow/Compose/lockfile bytes. A new executor therefore does not need unpublished local history.
