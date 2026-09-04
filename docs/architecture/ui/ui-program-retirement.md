# UI-program retirement and retained sources

## Owner decision

On 2026-09-04 the owner authorized removal of the G0-G6 design program and its
materials while retaining the final interactive target UI concept, product and
backend requirements, and working application code. Production UI alignment
with the concept is a subsequent implementation task. This decision supersedes
the earlier requirement to keep the frozen program in the current checkout.

## Retained sources

- [Target pilot](target-pilot/README.md), its exact HTML/runtime/license hashes,
  and compact concept notes with the original owner corrections and requirement
  bindings.
- Machine and human product blueprints, UI requirements/inventory, route and
  surface contracts, and architecture/backend decisions.
- Production frontend/backend code, existing implementation tickets, tests,
  and terminal implementation evidence. Accepted implementation status remains
  evidence for that historical boundary, not certification against the new
  target concept.

## Retired materials and recovery

The following exact subtrees were removed from the maintained tree after
extracting the pilot and its concept notes:

- `.codex/delivery/ui-design-programs/custometry-v1/`
- `.codex/delivery/ui-design-programs/custometry-v2/`
- `.codex/agents/generated/custometry-ui-design-g0-v2/`
- `.codex/agents/generated/custometry-ui-design-g4-v1/`
- `.codex/delivery/evidence/custometry-ui-design-program-v2/`

They include stage ledgers, generated executor prompts, G-stage contracts,
review boards, intermediate candidates, repeated inventories, screenshots,
receipts, and the now-obsolete suspension marker. The obsolete pre-G0 pilot
manifest is also retired. Earlier W03-W10/W24-W27 and production ticket evidence
remain historical records; no acceptance is fabricated or revoked.

All original bytes remain recoverable from the published commit
`d5f8aa29f83be90a0b3871ff2c886d48fc020901` in Git. For example:

```bash
git show d5f8aa29f83be90a0b3871ff2c886d48fc020901:.codex/delivery/ui-design-programs/custometry-v2/stage-ledger.md
git archive d5f8aa29f83be90a0b3871ff2c886d48fc020901 .codex/delivery/ui-design-programs/custometry-v2 | tar -t
```

Historical path/hash references in preserved implementation evidence resolve
against that commit. Recover a historical file into a separate scratch location
when needed; recovering it does not restore execution or design authority.
No Git history rewriting, force-push, or changes to other worktrees are part of
this retirement. Tree size reduction does not imply equivalent clone-size
reduction because prior commits remain in history.

## Compatibility and proof

Design/execution authority is deliberately changed to the owner's target pilot
and ticket-based implementation. Runtime APIs, ports, DTOs, persistence,
configuration, request/cache identities, service-call semantics, side-effect
idempotency, operational logs/alerts, and production browser dispatch are
unchanged. The performance-budget requirement retains its intent with a
ticket acceptance boundary instead of the removed G3 stage.

Verification must include exact pilot-byte preservation, bundled resource
loading and representative browser interactions, surviving requirement/route
identities, no application-code diff, reference validation, local/pre-push
profiles, and required remote CI before protected merge. Repository removal
and concept preservation do not prove that current production screens already
match the target pilot or that demo calculations meet backend requirements.

## Observed cleanup checks (2026-09-04)

- Base and independently queried remote `main`:
  `d5f8aa29f83be90a0b3871ff2c886d48fc020901`.
  Work ran in a separate clean worktree; the existing dirty primary checkout
  and its separate W15 worktree were not changed.
- Git reports 9,022 deleted paths / 531,669,066 deleted tracked bytes after
  rename detection. Three pilot resources were retained byte-for-byte
  (1,574,826 bytes); their SHA-256/size inventory is in the pilot manifest.
  Rename detection may choose an identical earlier ECharts copy; the explicit
  source comparison used the final `pilot-candidate-v3-metadata` copy.
- A Git/Node byte audit compared each relocated resource with `git show`
  from the base commit and checked the manifest hash/size: passed.
- The unique requirement-ID sets are unchanged: 1,141 in each product
  blueprint and 307 referenced IDs in the UI blueprint. In PR #46 the only
  machine/human requirement wording edit replaces the G3 timing in `WEB-PERF-002`
  with acceptance of the corresponding UI implementation.
- `git diff --name-only HEAD -- apps packages tests migrations deploy pnpm-lock.yaml uv.lock`:
  empty. Executable route/surface manifests and ticket statuses are unchanged.
- `generate_requirement_index` and `generate_docs_index`: passed; the
  requirement index needed no content change, and the contributor index was
  regenerated. These are the `tools.custometry_quality` modules invoked with
  `uv run --locked python -m` after activating the pinned toolchain.
- `uv run --locked python -m tools.check --scope local`,
  `--scope pre-push`, and `--scope ci`: passed. They include blueprint,
  reference, delivery, profile, route, and generated-index checks.
- `git diff --check` and `git diff --cached --check`: passed.

### Preserved-pilot browser smoke

The unchanged pilot was served only on
`http://127.0.0.1:8834/ru/source.html` with
`python3 -m http.server 8834 --bind 127.0.0.1 --directory docs/architecture/ui/target-pilot`.
The isolated `playwright-cli -s=custometry-cleanup` session observed:

- RU rendering at 1920x1080, chart-to-table switch, Focus dialog opening,
  and Escape returning to the report;
- profile/navigation context, report inspector, and the visible locale
  menu switching to `en` with heading `Customer base`;
- EN rendering at 768x1024 with the responsive inspector over the report;
- HTML and bundled ECharts requests returned 200; `echarts` was loaded;
  `console` reported zero errors and zero warnings.

Two inspected screenshots and CLI snapshots remain ignored local diagnostics,
not committed program evidence. This smoke proves resource relocation and
representative interactions only. It is not exhaustive UX/accessibility or
responsive acceptance; the narrow viewport can obscure content behind the
inspector. Prototype limitations are retained, not silently fixed or certified.

### Cold-head review

Cold-head review: completed. Mode: independent read-only subagent.
Scope: changed repository routing, source contract, target-pilot records,
ADR/UI authority, and affected historical ticket guidance. Instructions:
`architecture-review/references/cold-head-plan-prompt-pack-review.md`.
Verdict: Release. One W30 YAML indentation issue was fixed; subsequent local,
pre-push, and CI-profile checks passed. No unresolved Blocker/High findings.
This review does not replace the protected PR's required remote
`Foundation gate`, including disposable Compose/browser proof, before merge.

The main cleanup was published through PR #46 after Foundation CI run
`33914098501` passed all jobs, including
`CUSTOMETRY_RUN_BROWSER=1 ./deploy/compose/ci-smoke.sh`. Its squash commit is
`a59104806949543673a7a7b0cca2832957c9a3a1`.
A final repository-wide reference scan then found remaining program wording
in the root README, ADR index, ADR-0005/0006, route contract, technical
blueprints, and historical W18 guidance. The narrow follow-up synchronizes
those references and labels W18's old statements as history. `WEB-ARCH-001`,
`WEB-ARCH-005`, and `V1-AC-043` retain technology selection, pinned design
authority, complete Organization/People states, and real browser/accessibility
proof, but no longer require the deleted program as their delivery mechanism.
No business capability, ticket status, code, or preserved pilot bytes change.
