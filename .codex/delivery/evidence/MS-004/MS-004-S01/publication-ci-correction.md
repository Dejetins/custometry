# MS-004-S01 publication CI correction — migration head assertions

Date: 2026-09-20. Baseline commit:
`c851de5eb299c5b2ff72fe5c92ed0b33aff427d1` on the coordinator's technical branch.
Authority: explicit coordinator request to repair the two failing publication
checks in this original executor task. No production code or migration changed.
S01 remains accepted; this is append-only publication evidence, not a new stage.

## Confirmed cause and scope

The coordinator supplied the red [Foundation run for PR #85](https://github.com/Dejetins/custometry/actions/runs/35532407511):
2 failed, 449 passed, 39 skipped. Both actual PostgreSQL migration tests reached
`0012_metric_workspace`, but their final exact-head assertion still expected
`0011_presentation_drafts`. Static/typing passed in that run; frontend was not
reached. These CI observations are attributed to the coordinator's inspection,
not represented as a separate CI run by this executor.

Direct source inspection confirmed the stale literals at operator API line 541
and notification inbox line 552. Each was changed to the new committed exact
head `0012_metric_workspace`. All calls to migrate to head, downgrade targets
`0007_contributor_projection` / `0008_execution_control`, table absence/presence
assertions and re-upgrade operations remain byte-for-byte unchanged. No dynamic
head lookup, weaker assertion, fixture replacement or unrelated refactor.
Contract impact: none for production API/persistence behavior; these are exact
expected-head test maintenance changes required by the added migration.

| Changed source | Before SHA-256 | After SHA-256 |
|---|---|---|
| `tests/integration/execution_control/test_real_operator_api.py` | `ffb09a27756a3782cf8e9674ce58fa7c01eea78b1bc1ffe23443bc1cc81b5066` | `f6d8bb78adfd01109232a70d7b247ab642c9ece0cecf5c81f26d52351bea6097` |
| `tests/integration/notifications/test_real_notification_inbox.py` | `dbfc02b4b8d69fc7985557702aea403341cc3e8c855fcb43d9dbda8f783d5b39` | `c63782cf3fb6d16391d578a06812ee239131ee9cb8e663c4e9e4ffcdc9efbfc0` |

## Actual local verification

After `source scripts/activate-toolchain.sh`, the exact focused command was:

```sh
DOCKER_HOST=unix:///Users/daniildegtyarev/.docker/run/docker.sock TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE=/var/run/docker.sock uv run --locked --package custometry-api --all-groups pytest -q tests/integration/execution_control/test_real_operator_api.py::test_z_real_postgresql_migration_repeat_downgrade_and_reupgrade tests/integration/notifications/test_real_notification_inbox.py::test_z_real_postgresql_migration_repeat_downgrade_and_reupgrade
```

Result: **2 passed, 0 skipped, 11.05 s**. The existing fixture mechanisms provisioned
isolated PostgreSQL databases; Execution's fixture also used its real Valkey
boundary. Both tests actually performed repeated upgrade, downgrade, table
assertions and re-upgrade to 0012. No shared database or source checkout was used.
Fixture context managers completed teardown; no container remained under the
`org.testcontainers=true` label after the run. This proves these two local
migration lifecycles, not the entire operator/inbox product or a new green CI run.

Additional checks, all passed:

- `uv run --locked ruff check tests/integration/execution_control/test_real_operator_api.py tests/integration/notifications/test_real_notification_inbox.py`.
- `uv run --locked pyright tests/integration/execution_control/test_real_operator_api.py tests/integration/notifications/test_real_notification_inbox.py`: zero errors/warnings.
- `uv run --locked python -m tools.check --scope local`.
- `git diff --check`; final source diff contains exactly the two expected literals.

No gratuitous failing rerun was performed: supplied CI red evidence and direct
source inspection established the cause. Coordinator must commit/push this
correction and observe the new Foundation result; that work remains unperformed
by this executor.

## Preserved accepted/history bytes

- `.codex/delivery/evidence/MS-004/MS-004-S01/coordinator-review.md`: `cece2a3055ebb2c5586029e5c9a296d9b3ea2d88c987221c1d239c7b8119a6be`.
- `.codex/delivery/evidence/MS-004/MS-004-S01/owned-files.json`: `44f10863d8746e45494a9c0bfc344d6449ecbba971889145f43113208f841bcd`.
- `.codex/delivery/evidence/MS-004/MS-004-S01/publication-newline-correction.md`: `25560e5658eb1606570bb34df3a9d94b62a29731e3185c1e1e8db9470e14ec3e`.
- `.codex/delivery/evidence/MS-004/MS-004-S01/receipts/001-ready.md`: `4f9502ef626e9a8e52c8d1804074a138daea0515fdd1d55c4bf459de7b08caf6`.
- `.codex/delivery/evidence/MS-004/MS-004-S01/report.md`: `3669c3c4965750b92e9d4eeb4bc7ed456e401e6820cea7a556fbbe250c243e33`.
- `.codex/delivery/evidence/MS-004/MS-004-S01/validation.md`: `6031a95aa0193cf5626ae9beb0f2cc74f485076f4c27be8debcd2bc01a406113`.
- `.codex/delivery/ledgers/MS-004.md`: `83f1006479589b6a2d730e3be80563e78f109b459ee5ec06f456a6c72d6aaa69`.

Only the two tests and this new evidence file are owned by this repair. Accepted
report, validation, owned manifest, receipt, journal, coordinator review and prior
newline correction were not rewritten. No claim reset, runtime transition, S02,
staging, commit, push, PR or branch mutation was performed. Leave publication and
branch cleanup to the coordinator after successful synchronization.
