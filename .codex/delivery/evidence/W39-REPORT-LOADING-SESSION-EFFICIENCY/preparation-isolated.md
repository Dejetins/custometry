# Isolated W39 preparation

Prepared on 2026-09-23. Verdict: ready for owner-started local implementation.
This record covers preparation only; the ticket remains `ready`.

## Working copy and inherited ownership

- Absolute task cwd: `/Users/daniildegtyarev/.codex/worktrees/c67c/Custometry`.
- Read-only baseline source: `/Users/daniildegtyarev/.codex/worktrees/575c/Custometry`.
- Base commit: `86055ce732640ebe68fd5415a55f7bbde3499181`.
- Destination was clean and already at the selected commit; no checkout switch was needed.
- Canonical HEAD matched the selected commit before transfer.
- Transferred 25 tracked files through `git diff --binary --full-index --no-ext-diff <base> --` and `git apply --check --binary -`, then `git apply --binary -`.
- Copied 168 untracked files selected from `git ls-files --others --exclude-standard -z`, restricted to the five owner-authorized file/prefix selections. Total transferred file bytes: 11,788,958.
- Every transferred source and destination file matched its recorded SHA-256. The destination binary tracked diff matched the captured source diff.
- [Inherited manifest](inherited-baseline.json) records every transferred path, hash, size, source, baseline and ownership. The captured binary patch is identified by hash in the [publication sanitization record](publication-sanitization.json); its bytes are excluded from publication. Reconstruction requires the base commit, the original patch and the explicit untracked inventory from the source, verifying every manifest hash.
- Inherited S05 corrections are not W39 implementation results and do not accept S05. Copied ledgers, receipts and MS-004 evidence are read-only historical inputs. The sole active MS-004 journal remains `/Users/daniildegtyarev/.codex/worktrees/575c/Custometry/.codex/delivery/ledgers/MS-004.md`.
- The inherited [coordinator preparation record](preparation.md) is preserved byte-for-byte. This separate record owns the isolated-copy observations.
- `/Users/daniildegtyarev/Projects/Custometry` and the canonical checkout were not edited. No commits, publication, dependency installation, Goal, agents, demo process changes or port operations were performed.

## Entry and source checks

All 13 context sources declared by the copied [ticket](../../tickets/W39-REPORT-LOADING-SESSION-EFFICIENCY.md) exist, including ADR-0007 and correction-002 report/validation. Root and adapter AGENTS, the ticket, tooling gates and activation script were read.

Toolchain activation with `COREPACK_ENABLE_NETWORK=0` passed: Node 24.18.0, pnpm 11.13.0, uv 0.9.26. Docker CLI 29.8.0 and Compose v5.5.1 are available. Docker daemon/runtime health was not probed in this task.

Existing Chromium executable `/Users/daniildegtyarev/Library/Caches/ms-playwright/chromium_headless_shell-1169/chrome-mac/headless_shell --version` returned `Chromium 136.0.7103.25` (exit 0). No browser journey was launched.

The isolated checkout has no `.venv` or `node_modules`. Source validators used the existing canonical Python 3.12.12 interpreter read-only, with bytecode disabled, offline uv and no environment synchronization. Repository imports resolved from this task cwd. No source-check result implies that the isolated runtime environment is installed.

Executed from this cwd, with `COREPACK_ENABLE_NETWORK=0 PYTHONDONTWRITEBYTECODE=1 UV_OFFLINE=1`, after `source scripts/activate-toolchain.sh` in bash:

```sh
uv run --no-project --no-sync --offline --python /Users/daniildegtyarev/.codex/worktrees/575c/Custometry/.venv/bin/python python -B -m tools.custometry_quality.validate_delivery_tickets --json
uv run --no-project --no-sync --offline --python /Users/daniildegtyarev/.codex/worktrees/575c/Custometry/.venv/bin/python python -B -m tools.check --scope local --json
git diff --check
```

All exited 0. Ticket validation: 40 tickets, W39 ready, no active tickets, no findings. Local profile: all 17 selected source/static checks passed, no findings; full result is in [local gate evidence](preparation-local-gates.json). uv reported that `--no-sync` has no effect alongside `--no-project`; no dependencies were installed. Static doctor observed 18 CPUs and 1479.81 GiB free disk; its owned-disk metric is scoped to its ownership manifest, not total transfer size. One preliminary search referenced nonexistent `tools/custometry_quality/orchestrator.py`; inspection continued with the actual `tools/custometry_quality/check.py` and does not support an absence claim.

## Proof limits and next action

Contract impact from this preparation: none; source bytes are inherited, and newly authored files are preparation evidence only. Requirement IDs and future implementation/compatibility scope remain those declared in the ticket.

Implementation, PostgreSQL/API behavior, browser regressions, event invalidation, retention, 50-user load/idle measurements and performance acceptance are not performed. MS-004 acceptance, CI, deployment and production readiness are not claimed. Missing local dependencies are routine execution setup, not a product blocker.

Stop after preparation. When the owner starts implementation here, follow the ticket, capture the comparable performance baseline before product edits, configure task-owned dependencies/ports/disposable databases, and leave the live demonstration untouched. Before separately authorized publication/integration, reconcile W39 changes against the inherited manifest and patch so inherited S05 changes are not attributed to W39.
