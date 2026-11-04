# Owner-requested local demonstration

The owner requested the actual implemented result with test data after the execution stop.
This is a bounded runtime/demo action, not resumption of WS-004 implementation.

Started the existing isolated real_api_fixture.py and Vite configuration from c67c
on 58147/41747, bound to 127.0.0.1. API launcher PID 6582; Web launcher PID 6583.
Logs remain temporary at /tmp/custometry-owner-demo-api.log and
/tmp/custometry-owner-demo-web.log; do not copy raw credentials or payloads here.
The fixture owns a fresh temporary Docker PostgreSQL source/control pair and
published synthetic Northwind Retail artifacts. Retained41746 data was untouched.

Workspace: e4b700ba-3de7-4572-af1c-95b4f84d6cd9.
Created report: 37f0be15-3232-44ac-a301-3721f35697ea.
URL: http://127.0.0.1:41747/w/e4b700ba-3de7-4572-af1c-95b4f84d6cd9/reports/37f0be15-3232-44ac-a301-3721f35697ea/edit

In-app browser proof: signed in using the fixture author, created two independent
monthly charts (revenue and receipts) and a standalone monthly revenue table for
2025-01-01 through 2025-11-30; applied each, saved, reopened via the library and
observed all three results with Saved status. Switched visible interface to Russian.
Final browser error-log query returned no entries. Screenshot:
/tmp/custometry-owner-demo.jpg. No product source edits or full regression claim.
Backend/browser integration is real local fixture execution, not mocked results.

Keep these processes alive for owner inspection. This harness is temporary:
stopping its API cleans its owned test database/artifacts, so do not promise the
report survives fixture teardown or machine restart. Recreating the fixture uses
new workspace/report identities. Do not run its automated Playwright suite while
these occupied ports are serving the owner. Original runtime remains separate.

## Owner-reported inspector scroll repair (2026-10-07)

Execution route: explicit tiny repair following the owner browser defect report;
no milestone resumption or journal mutation. Served checkout verified through
listener PID 7257 cwd (c67c/apps/web). Changed only two scoped CSS rules in
`apps/web/src/features/reports/composer.css`: prevent builder header shrink and
make its flex form independently scrollable with min-height zero, contained
overscroll, stable gutter and 4px focus clearance. Existing data handlers unchanged.

Confirmed cause: the 1601px form had overflow visible inside an 882px inspector
with overflow hidden. Bottom controls were clipped, with no user scroll surface.
After fix, the form had clientHeight 790 / scrollHeight 1609 and native wheel
scroll reached scrollTop 819 (the exact maximum); bottom Update block action
was visible while the header remained above the scrolling form. Screenshot:
/tmp/custometry-inspector-scroll-fixed.jpg. At 768x1024 keyboard Tab reached
Update block within panel bounds; form scrollWidth equalled clientWidth (654).
At 1920x1080 form height 911, scrollHeight 1609, no horizontal overflow (318/318).
Viewport override reset. Browser console error query returned no entries.

The CSS development update remounted the iframe and returned to the saved report:
the earlier unsaved UI state was not retained. No Save, Apply, or data mutation
was issued by this repair. Owner draft recovery was not verified.

Local gate passed (`source scripts/activate-toolchain.sh && uv run --locked python
-m tools.check --scope local`). Browser regression was observed before/after;
no CSS-mirroring unit test added. This proof covers inspector reachability only,
not overall editor acceptance or broader WS-004 completion.

Frontend `pnpm --filter @custometry/web build` passed (TypeScript + Vite);
Vite reported its chunk-size warning. No dependencies were added.

## Owner-reported composer chrome repair (2026-10-08)

Explicit bounded repair; no successor milestone or publication. On saved snapshot
`a743f20e-919a-4d55-92e4-9e300389900b`, legacy period/store buttons received empty
workspaceChrome values and no composer handlers. Composer now supplies one action
opening/focusing its existing scopes disclosure, labelled Saved filters and period
in immutable snapshot mode. Legacy controls are suppressed only within composer;
metric-workspace controls retain their previous behavior. Source queries, saved
identity and permissions are unchanged (compatible browser presentation repair).

Page navigation now uses the pilot pill-tab tokens and omits redundant search and
all-page selector when only one accessible page exists. Multi-page search, selector,
arrow navigation and activation remain covered by two new interaction tests.
Requirement touchpoints: ANALYTICAL-DOC-002, A11Y-001; no whole-clause completion claim.
Focused Vitest run: composer-page-navigation and composer-structure, 11/11 passed.

Final snapshot browser check after reload: legacy buttons display none; Enter on
Saved filters and period opened scopes and focused summary, showing actual saved
2025-01-01..2025-11-30 context. No mutation submitted. Page navigation had no
horizontal overflow at 768x1024 (651/651) or 1920x1080 (1768/1768); viewport reset.
Console error query empty. Screenshots /tmp/custometry-composer-chrome-fixed.jpg
and /tmp/custometry-saved-context-fixed.jpg. Frontend build and local gate passed;
Vite chunk-size warning remains. Editor/create routes were not browser-retested
in this repair; the shared structure component has focused test coverage.
