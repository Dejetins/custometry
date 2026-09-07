---
doc_id: ARCH-WORKING-COPY-SYNC-20260906
doc_version: 1
status: accepted
visibility: internal
ship: false
owner: engineering
requirement_ids: []
proof_boundary:
  label: source-reconciliation-and-local-tooling
  exclusions: [application-runtime, browser-runtime, deployment, hosted-ci]
---

# Working-copy synchronization evidence

## Authority and sources

On 2026-09-06 the owner requested complete synchronization of remaining local
changes into main, without additional branches. This follows the
[planning framework adoption](framework-v1/adoption-evidence.md) and preserves
the [published documentation reconciliation](documentation-audit-reconciliation-2026-09-06.md).
The adopted [framework](framework-v1/README.md), owner participation and mandatory
document synchronization remain in force.

The comparison used old local base `80cd0976c434b6db62d3e415bc638cbe4a9468c2`,
current main `2d370f6ef1cd5cf9ddb09afa7987004b9412042c` and captured working bytes.
Of 282 dirty paths, 236 matched the old base exactly; their apparent changes
were checkout drift. Those paths were restored from current main. Remaining
paths were compared individually against both versions before reconciliation.
No new branch or history rewrite was needed for this synchronization.

## Reconciliation decisions

- Preserve published application code, migrations, target-pilot authority and
  documentation corrections. Older draft claims that implemented backend
  packages were placeholders had already been superseded by the published
  reconciliation and were not reapplied.
- Retain local source edits to the root/project instructions, nine role profiles,
  ticket template, delivery-contract validator and its regression tests. Keep
  the adopted planning hierarchy and current UI implementation source contract
  while removing duplicate global rules and stale routing references.
- Use Custometry contracts for analytical role work; the Work-only methodology
  skill is not a Custometry route. Validate the execution-unit rule in its
  canonical global AGENTS owner rather than requiring a duplicate in its reference.
- Update root navigation and the generated contributor index with durable links.

The temporary browser snapshot `.playwright-mcp/page-2026-09-04T23-15-17-138Z.yml`,
`report-editor-check.png` and superseded
`docs/architecture/ui/custometry-pre-g0-pilot-manifest-v1.json` were preserved
outside the source tree at
`/private/tmp/custometry-full-sync-20260906/local-artifacts/`, with their relative
paths intact. They are local recovery artifacts, not durable runtime evidence or
current pilot authority. Per-path comparison snapshots and dispositions are in
the same task scratch directory.

Product requirement IDs: not applicable; this changes engineering instructions
and tooling. API, persistence, product and runtime contract impact: none.
Process impact: compatible-change to the adopted framework and correction of
the optional installed-source validator's rule ownership.

## Validation

Commands use `source scripts/activate-toolchain.sh` and the locked offline Python
environment described in [tooling gates](../tooling-gates.md).

- `uv run --locked --offline pytest -q tests/tooling/test_static_quality_tools.py -k delivery_contract`:
  six tests passed, including rejection of a rule present only in the wrong owner.
- Scoped `ruff check`: passed. Initial scoped `ruff format --check` identified
  the new test's comprehension formatting; the formatter corrected that test.
- `uv run --locked --offline python -m tools.check --scope local`: passed after
  source reconciliation. This profile checks static source consistency and local
  prerequisites; it does not execute application or browser journeys.
- Final scoped Ruff lint/format checks and the explicit installed-source
  `validate_delivery_contract --contract` audit: passed.
- After adding this report and regenerating the contributor index, the local
  profile and six focused tests passed again. `git diff --check` passed, and
  application, package, migration and deployment paths matched current main.
- `uv run --locked --offline python -m tools.check --scope pre-commit`: passed.
  The actual commit also invokes the repository pre-commit hook.

## Independent instruction review

Cold-head review: completed. Mode: independent subagent. Verdict: Release.
One read-only reviewer inspected the resulting instruction/tooling diff and this
report using the installed cold-head plan/prompt-pack checklist. Findings:
none; resolved/unresolved: 0/0. Nine inspection-based routing scenarios covered
all role boundaries, milestone authoring/execution, owner decisions, documentation
synchronization and browser proof. Local follow-up check: completed.

The review assessed source consistency against current main; it did not replay
every historical working byte or launch runtime role agents. Residual limitation:
these checks establish repository source/tooling consistency only. No application,
browser, deployment or hosted-CI readiness is asserted. The detailed review is
preserved locally at
`/private/tmp/custometry-full-sync-20260906/independent-review.md`.
