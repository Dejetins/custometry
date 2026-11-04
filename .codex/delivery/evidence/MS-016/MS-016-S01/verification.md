# MS-016 verification

Checkout `/Users/daniildegtyarev/.codex/worktrees/c67c/Custometry`; retained runtime41746
and data unchanged. Disposable PostgreSQL/API58147/browser41747, no publication.

- Focused Semantic real API suite:5 passed,6 deselected using the existing disposable
  `tests/integration/semantic/run_s01.py` and `-k "calendar and not scope_constraints"`.
  Covers current roles/CSRF/revocation, first configuration, atomic first-write race,
  both later concurrent updates denied, unchanged default, exact version reads,
  original idempotent replay (including absent zone provider), invalid rules/profile,
  and interrupted provisioning. New request after setup returns409 with explicit code.
- Backend compatibility/DST:51 passed from `tests/unit/analytics/test_zoned_calendar.py`,
  `test_year_comparison.py` and `tests/contract/presentation/test_workspace.py`.
  Frozen UTC outputs, pinned IANA rules and23/25h calculation remain unchanged.
- Frontend23 passed from mounted `composer-temporal-editor.test.tsx`,
  `temporal-comparison.test.tsx`, `composer-state.test.ts`. Existing edits expose no
  calendar version/zone settings, preserve pinned references and call no calendar GET.
- TypeScript, focused Ruff/Pyright (zero errors), client equality, docs index,
  `check --scope local`, `git diff --check`: pass. This is not CI/release proof.

Final real Playwright run `temporal.spec.ts timezone.spec.ts`:2 passed in1.1m.
A previously saved UTC report retains identical request/artifact hashes after first
company setup. On `/settings/policies`, actual administrator configures New_York;
reload shows fixed disabled settings. Existing report/block editing has no setup,
version selector or calendar GET. A new report obtains that configured calendar and
persists/reloads actual25h vs24h comparison values. A separate authenticated ordinary
reader is denied the settings UI and sees no input. Console pageerror collection is
empty. Earlier dedicated run passed; first attempt used wrong test-only close label
('Close' instead of actual 'Close settings'), corrected without product changes.

`company-calendar-once.png` and `timezone-dst.png` are sanitized synthetic UI evidence.
Raw traces/cookies/auth payloads remain temporary. Independent reviewer verified
175 prior evidence files unchanged and no change to the four calculation/identity
files in this stage. Source conformance review is distinct from executor runtime proof.

No full UI-ADMIN-004 policy, SLO, other calendar/provider or workstream completion
claim follows. Historical MS-015 UI assertions are superseded by this correction.

Final visual inspection also removed the inherited fixed-UTC settings hint and
separated controls using scoped layout CSS. Dedicated browser proof passed again
(1 scenario,32.7s); TypeScript/local gate remained green. No runtime policy changed
in that wording/layout repair. Both final images were inspected.
