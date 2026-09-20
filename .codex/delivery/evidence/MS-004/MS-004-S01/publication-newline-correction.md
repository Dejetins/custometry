# MS-004-S01 publication correction — terminal newline

Date: 2026-09-20. Authority: coordinator's explicit narrow publication correction
in the original S01 executor task. Stage S01 remains accepted. No claim, stage
transition, implementation expansion or Git publication is performed here.

## Reason and change

Coordinator's staged whitespace check found
`packages/contracts/src/workspace-contracts.ts:520: new blank line at EOF`.
The initial unstaged check did not inspect this then-untracked generated file.
The existing `_types` helper intentionally ends in a separator before appended
client code. Normalize only the standalone workspace output to exactly one final
newline, leaving that helper and the calendar client's assembled bytes unchanged.
Regenerate only `workspace-contracts.ts`. There is no schema, type or runtime
behavior change. Contract impact: `none` for API/DTO/runtime semantics.

| Changed path | Before SHA-256 | After SHA-256 |
|---|---|---|
| `packages/contracts/generate_workspace_client.py` | `7238328b04d55603f686742ead2fa31aae287cdfda9deeea22392bb7b0281bbd` | `5e83b98c3a6ee13d12496a83761108c4f93c559e45cf1461999e8b459eca8634` |
| `packages/contracts/src/workspace-contracts.ts` | `91396ee598b490f4024bcf44ac01e1b999b1efd82b4bcf71cb01ef71ea0316fc` | `8e8e45625a8ba257d507351038980562529cc2504946b0181716cb9e5de65e3b` |

Adding exactly one newline byte back to the regenerated output reproduces its
original SHA-256. These two paths are staged; pre-existing staged changes are
preserved. This new evidence is left for coordinator staging.

## Observed checks

- Targeted generation via `packages.contracts.generate_workspace_client.outputs`
  wrote only the standalone TypeScript output.
- `uv run --locked --package custometry-api pytest -q tests/contract/presentation/test_workspace.py::test_generated_schema_openapi_and_typescript_are_current`:
  passed, one test; compares every generated output, including calendar client.
- `uv run --locked ruff check packages/contracts/generate_workspace_client.py`:
  passed.
- `git diff --check` and `git diff --cached --check`: passed after staging only
  the two correction paths.
- Byte comparison verified that calendar-client and all protected accepted-stage
  evidence/journal files below remain unchanged.

## Preserved bytes

- `packages/contracts/src/workspace-calendar-client.ts`: `70e7845a575abf36b85ce9e0bd3a0f49e4dc890a17eb412e42285be412be0bda`.
- `.codex/delivery/evidence/MS-004/MS-004-S01/report.md`: `3669c3c4965750b92e9d4eeb4bc7ed456e401e6820cea7a556fbbe250c243e33`.
- `.codex/delivery/evidence/MS-004/MS-004-S01/validation.md`: `6031a95aa0193cf5626ae9beb0f2cc74f485076f4c27be8debcd2bc01a406113`.
- `.codex/delivery/evidence/MS-004/MS-004-S01/owned-files.json`: `44f10863d8746e45494a9c0bfc344d6449ecbba971889145f43113208f841bcd`.
- `.codex/delivery/evidence/MS-004/MS-004-S01/receipts/001-ready.md`: `4f9502ef626e9a8e52c8d1804074a138daea0515fdd1d55c4bf459de7b08caf6`.
- `.codex/delivery/ledgers/MS-004.md`: `83f1006479589b6a2d730e3be80563e78f109b459ee5ec06f456a6c72d6aaa69`.

The accepted report, validation, owned manifest and consumed receipt remain
immutable historical evidence. This append-only correction explains the two
source-hash deltas for coordinator publication reconciliation; it does not
rewrite the original manifest or acceptance. No S02 execution, commit, push, PR,
Git identity/configuration edit or technical-branch cleanup was performed.

Final handoff checks: `check --scope local` and `validate_prompt_packs` passed
(four journals). Working and staged whitespace checks passed; the new evidence
file was also checked separately because it remains untracked.
