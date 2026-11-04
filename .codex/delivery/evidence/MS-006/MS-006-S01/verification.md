# C02 observed verification

Target: c67c source checkout and owned disposable PostgreSQL/artifacts. Browser
http://127.0.0.1:41747; synthetic API 58147. Retained user data is untouched.

## Observed checks

- Presentation contracts/units: 108 passed (36 C01 DTO and 9 C02 service tests).
- Focused web: 29 passed (composer state/route, native preparation, library, projection).
- New runtime Python source: Ruff and strict Pyright passed after typing repairs.
- Web TypeScript: passed.
- Owned PostgreSQL/API rehearsal: passed. Fresh migration; pre-write downgrade/re-upgrade;
  four independent queries/six blocks; chart/table same result IDs; exact graph/ID
  save/reopen; saved results; old-reader 409; legacy report bytes; library; CAS/key
  conflicts; injected pre-pointer failure; concurrent identical saves; old exact
  snapshot; refusal of downgrade with new data; noncreator and revoked-session denial.
- Three real-browser scenarios: passed in 30.0s; expanded failure/reconnect scenario
  then passed in 18.1s. Four charts/two tables, Apply/Save/reload
  without new Apply; standalone table; independent duplicate/edit/delete; local
  injected 503/retry with sibling intact; keyboard inspector entry/Escape focus.
  Desktop 1440x1000, responsive observations at 768 and 390 pixels.
  Delayed Apply disables Save; stale response after input edit is discarded;
  returning to saved input reloads its exact result despite stale local state.
  Two offline/online reconnects preserve draft and dirty status. New calculation,
  committed Save with lost response, reconnect/remount and retry send identical
  POST including result references and idempotency key. Reopen retains the edit.
  [Desktop](browser/six-blocks-desktop.png), [768px](browser/six-blocks-768.png),
  [390px standalone table](browser/standalone-table-390.png) are inspected captures.
  The desktop viewport proves mixed chart/table placement; six blocks are verified
  in the browser, not all simultaneously visible in that viewport capture.
- Local gate: passed after documentation synchronization; final receipt gate recorded
  in the canonical journal transition.

## Reproduction and repair record

1. Browser SYS-404-QUERY: new composer query key was unregistered. Route regression
   reproduced red; final route uses existing `view=composer`, leaves registry and
   unknown-key rejection unchanged. Route test and original browser flow passed.
2. Metric step was visible but wrapping select label included its options. Explicit
   accessible names match visible labels; original browser flow then passed.
3. Screenshot showed fixed legacy header height clipping composer actions at 390px.
   Composer-only auto-height/wrapping/flex repair passed the browser width assertion
   and visual inspection.
4. API harness initially omitted Origin; corrected to configured synthetic origin.
   Logout refresh-cookie path differs for mounted TestClient URLs, so session
   revocation uses Identity-owned synthetic session rows in the disposable DB.
   Production guards were never weakened.
5. Initial chart assertion matched parent plus nested SVG. Test now selects the
   observed plot container; it still requires a visible rendered result.

6. Independent review found draft loss at reconnect, Apply/Save dirty race, and
   stale ready state suppressing saved-result GET. Draft is captured synchronously
   before remount, with actor check and true-access-reset purge; Save waits for
   calculations, and GET enablement compares the input key. Follow-up review found
   exact retry payload loss across remount: pending request is now immutable,
   authoring pauses until acknowledgment; definitive non-conflict 4xx permits repair.
7. Reconnect test initially emitted offline without online, leaving TanStack queries
   paused. Diagnostics showed Loading report with a mounted frame and no GET;
   correcting the harness event pair proved restoration. A duplicate status-text
   locator was replaced with the specific status role, preserving its assertion.
8. Store authorization validates both common/local selections against provider
   access and their intersection against the report ceiling, matching Analytics.
   Focused regression passed; no Presentation business calculation was introduced.

No raw auth/connection/provider payload is retained. Temporary harness secrets stay
in temporary files; cleanup removes only the task-owned container and volumes.
Successful browser data paths use real APIs; injected 503 is transport-failure
proof only. No performance, production, full provider/profile, publication or C10
accessibility acceptance. Composer reuses existing WorkspacePlot/WorkspaceTable
through deterministic per-block definitions; no second options compiler is added.
