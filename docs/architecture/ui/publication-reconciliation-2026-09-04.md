---
doc_id: ARCH-PUBLICATION-RECONCILIATION-20260904
title: Source checkout publication reconciliation, 2026-09-04
doc_version: 1
product_spec_version: 0.10.0-draft
visibility: internal
ship: false
owner: engineering-productivity
requirement_ids: [DOC-RULE-008, WEB-ARCH-001, WEB-ARCH-005]
status: observed
proof_boundary:
  label: publication-source-reconciliation-and-local-gates
  exclusions: [hosted-ci-until-observed, deployment, full-product-acceptance]
---

# Source checkout publication reconciliation, 2026-09-04

## Authority and source identity

The owner authorized publication of all existing Custometry changes, including
pre-existing product work and the removal of the two UI skills, through the
repository-required PR, Foundation CI, and squash merge to protected main.
The owner subsequently excluded every change belonging to the separate task
`01a06e21-7bba-7ce1-bb34-f2a66a3b1435`.

The original checkout was at `80cd0976c434b6db62d3e415bc638cbe4a9468c2`.
The reconciled publication starts from current remote main
`94672bf97a402d9c90e96ac8b783b6a0e30adba0`, preserving its integrated product
code and accepted target UI concept. The original checkout and Git index were
not modified. An external snapshot recorded every changed path and the hashes
of all existing changed files before reconciliation.

## Complete source-change accounting

The initial source inventory contained 4,036 paths: 27 modified tracked files,
4,005 tracked deletions, and four untracked files. One initial untracked file
belonged to the excluded planning task. Its later outputs are excluded too.

| Source change group | Publication decision |
|---|---|
| 4,003 generated UI workflow, prompt, ledger, atlas, board and evidence deletions | Already absent in remote main; keep deleted |
| Remaining old retirement evidence | Delete as requested; the current retirement record remains |
| Old ADR-0004 path and new replacement | Rename the current superseded ADR to `0004-ui-delivery-governance.md`; preserve the newer target-pilot decision |
| Machine/human blueprints, requirement index and route/surface product additions | Three-way comparison confirms the product additions already exist in main; retain current main byte-for-byte |
| UI blueprint, system design, architecture/source contracts, README and ticket template | Preserve newer accepted-main semantics; do not reintroduce pre-G0 prerequisites or downgrade the target pilot |
| Agent router and frontend/product role profiles | Remove the unavailable skill routes; repair stale section references and select `playwright-cli` for terminal browser mechanics |
| W05/W08/W10 historical tickets | Carry the local tooling-retirement edits; preserve ticket status and historical acceptance |
| W18/W30 tickets and evidence | Remove unavailable routes/commands, retain superseded status, and explicitly label edited historical metadata |
| Two early RU/EN HTML pilots | Publish byte-for-byte under `docs/architecture/ui/pilots/`, with historical manifest and current-target link |
| Current `target-pilot` HTML, ECharts, license and notes | Preserve all files byte-for-byte from remote main |
| `docs/architecture/planning/**` and corresponding index entries | Excluded by the owner's later instruction; no content from that task is included |
| Documentation indexes and links | Regenerate/update only for the selected publication paths |

The excluded planning task owns its audit, roadmap, and coverage JSON. It was
still active during publication. No snapshot of those files, their content,
or their index entries is part of this change. Temporary logs, dependency
caches, browser state, external backups, and source snapshots remain outside
Git. Global skill-library and Roehub changes are outside this repository.

## Preservation and risk review

Every original tracked deletion remains absent in the reconciled tree. The
source files and deletion state were checked against the initial snapshot;
new concurrent planning outputs do not enter the publication allowlist.

Both early HTML files match the supplied hashes and sizes:

- RU: `9d82b59fdf766ccc2b72616fa2c0945d99e1110794be4698c049f232425be780`, 108,920 bytes.
- EN: `233b3c94723a14dde1eb41f1c54610bc157b311d7cf1e42338302cf839f4e8f4`, 106,664 bytes.

The current target HTML remains
`b54b8b77d677d57869b0065dbe3aa005f13070297dface19ba98938f50d83700`;
its bundled ECharts and license also match the current manifest. Historical
pilots do not regain current design authority or establish browser proof.

The full resulting diff changes documentation, routing, and preserved visual
references only. `apps`, `packages`, migrations, deployment, workflows, the
three product/UI blueprints, and current target-pilot files have no diff
against the publication base. A high-confidence credential-pattern scan of
selected files found no matches; no temporary/archive candidates were selected.

## Contract impact

| Dimension | Classification and rationale |
|---|---|
| Public API, ports, DTOs and persisted schemas | `none`; product implementation remains unchanged |
| Runtime configuration | `none` |
| Request/cache/persistence identity | `none`; existing product requirements are preserved, not newly implemented |
| Service auth, timeout, retry and error semantics | `none` |
| External side-effect/idempotency semantics | `none` |
| Runtime logs, metrics, traces, audit and redaction | `none` |
| Agent routes and contributor documentation paths | Intentional `breaking-change`; retired tooling is unavailable and the ADR path is renamed with live references updated |
| Alert/runtime runbooks | `none` |
| Rollout gates | `none`; existing protected-main/CI requirements remain |
| Browser behavior and hot-path performance | `none`; historical source preservation is not frontend implementation |

Recovery remains in Git and the owner's verified external backup. Recovering
old files does not authorize restarting a retired workflow.

## Local checks

Exact toolchain: Node `24.18.0`, pnpm `11.13.0`, uv `0.9.26`, activated with
`source scripts/activate-toolchain.sh`; Python dependencies use the locked
workspace. The following checks were observed in the isolated publication tree:

| Command/check | Result |
|---|---|
| `uv sync --locked --all-groups --all-packages` | PASS |
| `corepack pnpm install --frozen-lockfile` | PASS |
| `uv run --locked python -m tools.check --scope local` | PASS |
| `uv run --locked python -m tools.check --scope ci` | PASS |
| `uv run --locked ruff check apps/api/src migrations tests tools` | PASS |
| `uv run --locked pyright apps/api/src tests/integration` | PASS, zero errors/warnings |
| `uv run --locked pytest -q tests/unit tests/contract` | PASS, 82 tests |
| `uv run --locked pytest -q` | 215 passed, 15 skipped, 17 environmental setup errors: local Docker daemon/socket unavailable |
| `uv run --locked mkdocs build --strict --config-file mkdocs.yml` | PASS |
| `corepack pnpm check` | PASS: 83 tests across workspace packages, including 74 Web tests; type/lint/build passed |
| Installed-source `validate_delivery_contract --contract .../delivery-contract-v1.md` | PASS |
| `validate_agent_profiles` | PASS, 9 profiles |
| Pilot size/SHA-256 verification; excluded-path check | PASS |
| Staged whitespace check for edited text | PASS; original HTML has one preserved trailing-whitespace line per file |

The byte-pinned HTML files each retain their original whitespace at line 1277.
Their staged checks suppress only `blank-at-eol` for these two files; all other
selected paths use the normal `git diff --cached --check`. Altering historical
bytes to remove whitespace would invalidate the supplied hashes.

The existing frontend bundle-size warning is not introduced by this change.
Full local pytest is not claimed green. Required hosted Foundation CI must
observe its Docker-backed tests and disposable Compose/browser boundary before
merge. Local source checks do not establish runtime, recovery, performance,
release qualification or deployment.

## Independent review

Cold-head review uses exactly one independent read-only subagent and
`architecture-review/references/cold-head-plan-prompt-pack-review.md`.
Verdict: `Release` within the reviewed source/routing boundary.
No Blocker/High finding was identified. One inherited Low finding concerned
stale role-profile section references and legacy browser routing; it was fixed,
and the local profile/installed-contract validators passed afterward.

Routing canaries for ordinary ready Web tickets, screenshot-led audit,
source-fidelity work, and attempted retired workflow continuation were checked.
Current target authority, conditional proof routing, and the continuation ban
remain intact. The separate planning task is excluded from review/publication.

## Publication boundary

This committed receipt records source reconciliation and local verification.
Hosted checks, the PR, squash-merge SHA, and remote-main verification are
reported by the publication task after they are observed. No deployment is
requested or performed. The repository may run its existing immutable-candidate
workflow on main; that is not a deployed application or release acceptance.

## Post-merge bootstrap repair

PR #48 merged as `de8d68d9cb598cdeb4b5f8c4d2413dc4ad2d7692` after all
required PR checks passed. Main workflow `33919251301` then failed twice before
migration/browser startup, immediately after starting `control-db`. The same
SHA passed the parallel candidate workflow's Foundation runtime. This exposed
an existing intermittent readiness defect, rather than a product-source diff.

The readiness commands omitted a host and therefore observed the local Unix
socket. The [official PostgreSQL entrypoint](https://github.com/docker-library/postgres/blob/master/docker-entrypoint.sh)
starts a socket-only initialization server, stops it, and then starts the final
server. The bootstrap could leave its loop on that temporary server and fail
its next probe during restart. The logs locate the failing phase; they do not
contain PostgreSQL's internal startup trace. A deterministic executable-shell
regression reproduced that early-success/next-probe-failure sequence on the
unmodified bootstrap.

The bounded follow-up changes only database readiness probes in
`deploy/compose/bootstrap.sh`, `deploy/compose/ci-smoke.sh`, and `compose.yaml`
to use container-local TCP at `127.0.0.1`. This also prevents Compose health
admission and demo-data verification from using the temporary server. Retry
budgets, image pins, ports, secrets, data and migrations are unchanged.

`tests/integration/test_bootstrap_lifecycle.py` now simulates initialization,
restart and final TCP readiness through the existing subprocess test seam. The
new regression failed before the repair and passes afterward; the complete
bootstrap file has five passing tests. Focused Ruff/Pyright and the grouped
`pre-push` profile passed. Hosted PR/main CI supplies the real container/browser
proof; the fake-command regression alone does not establish it.

Risk review: readiness semantics are `compatible-change`, implementing the
existing requirement that databases be ready before dependents start. API,
persistence, identity, authorization, external side effects and publication
policy are `none`. Rollback is a normal Git revert of this narrow change, with
the known readiness race returning. The separate planning-task exclusion and
source-checkout preservation remain in force for this repair.
