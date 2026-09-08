# MS-001 preparation and publication

Scope: restore the S02 implementation boundary, use accepted plan 2.1.0 and
prepare a clean S03. The owner requested deletion of the abandoned attempt's
reports, scans, snapshots, claim and transition records. They are removed from
the working documentation and journal. S01/S02 receipts and accepted plan snapshot
remain; S03 is pending/allowed/unclaimed and S04/S05 remain pending/disallowed.

[Owner authority](owner-decision.md).
[Rollback paths](rollback-files.json).
[Current plan](../../../../../docs/architecture/planning/milestones/MS-001/plan.md).
No custom PyArrow/native build, v2 source-companion or S03 assurance implementation
remains. Existing upstream package pins are a starting point, not a security verdict.

## Verification

The previous preparation passed 120 focused producer/manifest/ledger tests, Ruff,
Pyright and local gates. After cleanup, the updated ledger tests passed 20 cases,
including retained acceptance with a changed future prompt and rejection of using
an obsolete prompt for a new handoff. Focused Ruff, `tools.check --scope ci`, prompt-pack validation and `git diff --check` passed on the canonical checkout. Publication-tree and hosted checks are recorded by the PR.

The earlier independent review covered the simplified plan and rollback; its
one Low issue (obsolete current-entry prose) was corrected. Current cleanup and receipt-consumer behavior also passed focused independent
read-only review with no material findings. Two Low stale-version references
were corrected; current plan/prompt/journal bindings were revalidated.
Review verdict: Release after fixes; unresolved findings: zero. No product stage, local container build or platform deployment is
performed by this preparation. Publication is authorized through a technical
branch/PR; only task-owned paths are published. Foreign changes remain local.

Publication checkout: 120 focused tests passed in 4.43 seconds. The contributor
index was regenerated against its 64 published documents, excluding a local-only
document; the CI-equivalent source gate then passed. The canonical checkout has
65 documents and retains its own generated index. This is source proof; hosted
CI and the merge result are recorded on the PR.
