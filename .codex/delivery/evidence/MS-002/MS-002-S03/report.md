# MS-002-S03 — Pilot-derived first-run entry

[Plan MS-002 1.0.0](../../../../../docs/architecture/planning/milestones/MS-002/plan.md).
[Journal](../../../ledgers/MS-002.md) owns state and permission. This request
selects S03 only. Normal advance and the current session's exclusive claim were
used after reading S02 evidence and all declared entry inputs.

## Delivered scope

The existing root `/` renders a minimal installation entry using scoped shared
`pilot-entry/v1` primitives, React, styled-components, TanStack Query, i18next and
Lucide at the existing pins. The legacy FoundationHome remains a compatibility
source; unrelated route resolution and theme definitions are unchanged. No fake
workspace, navigation, analytics or disabled account-creation action is shown.

The typed operational adapter validates the S02 projection, supports real HTTP
503 component results, bounds transport to five seconds and requests no-store.
Query owns snapshots, cancellation, focus refetch and ten-second background
refresh. Failed refetches never expose retained successful Query data. Manual
retry announces checking; unchanged background results do not repeatedly announce.
Version and origin come from the current API response and browser location.
No domain/Identity state is inferred or stored. English default/fallback and full
Russian catalogs include a localized public help destination.

## Functional evidence

[Checks](checks-01.json) records exact commands and observed outcomes.
The owned Playwright configuration starts loopback host Vite, production FastAPI,
a fresh PostgreSQL instance migrated through the unchanged supported head, built
MkDocs public help and the preserved pilot server. Test controls operate only on
the disposable fixture; no API readiness probe or response is mocked.

The browser journey covers initial readiness/version/no-store, actual database
stop/start, unsupported schema, missing artifact directory, actual API stop/start,
retry recovery and stale-success removal. The storage failure is discovered by
background polling without clicking retry. It also covers RU/EN, reload, skip
link and keyboard focus restoration after retry, 200% CSS layout zoom, long-text
pseudo-locale, reduced-motion mode, help navigation and Back, console and network.
Browser exceptions and unexpected console errors are checked; expected 503 and
proxy 500 during deliberate faults are retained as negative evidence, not a clean
network claim. Unit checks separately cover malformed/contradictory DTO rejection
and timeout; the timeout test uses a fake transport and is not integration proof.

An initial four-project run passed before extending the proof. The extended run
failed after DB restart: a dedicated disposable reproduction confirmed Docker
reallocated its ephemeral published port. The fixture now reconciles that port
into its explicitly supplied Settings. Product API/readiness behavior was not
weakened. Earlier failed runs are not counted as final passing evidence. Focused
Python typing initially reported the upstream missing testcontainers stub and
nested decorated route usage. An exact missing-stub annotation and explicit
FastAPI route registration resolve those test-only diagnostics. The local gate
initially caught a new documentation anchor mismatch; the link was corrected.
The Web build emits a non-fatal chunk-size warning (603.15 kB main chunk); no
performance or bundle-size improvement is claimed.

## Visual evidence — separate from functional proof

[Comparison](visual-comparison.md) identifies inherited rules and derived layout.
Matched source/entry captures exist for 768x1024, 1024x768, 1440x900 and 1920x1080,
with representative English, Russian, failure, zoom and pseudo-locale views.
The source is the preserved HTML, SHA-256
`b54b8b77d677d57869b0065dbe3aa005f13070297dface19ba98938f50d83700`.
A green journey is not owner visual acceptance. The final functioning packaged
result and owner decision remain S04/S05 obligations.

## Requirements, compatibility and limits

| Source | Observed contribution |
|---|---|
| AC-05; I18N-001/002/004 | Real entry, en/ru catalog parity, English fallback, pseudo-locale, server codes translated only at presentation |
| AC-05; A11Y-001/003/005/008 | Keyboard/skip/focus, text plus icons for states, stable polite live region, layout zoom/reflow, reduced-motion mode |
| AC-05; WEB-ARCH-001..006; TECH-07 | Existing pinned stack; scoped shared primitives; typed server projection; unchanged product route identities; source-backed derived layout |
| AC-04 contribution | Current 503 or failed fetch replaces success; database/schema/storage/API faults and recovery observed |
| UI-AUTH-002/005; UI-CORE-001 | Downstream consumers only; no implementation or acceptance claim |

`breaking-change`: root visitors receive installation status instead of the
Foundation landing/workspace shell, as explicitly selected in TECH-07. New UI
requires the S02 operational endpoint; an older bundle fails safely and needs a
new S04 candidate. `compatible-change`: additive scoped UI-foundation exports
and localization/help content. `none`: API DTOs, server code, schema/migrations,
private Identity state, route identity JSON and old theme tokens are unmodified.
No cross-version deployment or rollback proof is claimed. The old component and
unrelated routes retain their compatibility seam.

Status live-region semantics and text updates were browser-verified; no actual
assistive-technology speech output or full WCAG certification is claimed. CSS
layout zoom doubles content and tests reflow; browser chrome zoom and Safari are
not this host Chromium evidence. No packaged HTTPS, second-computer LAN, full
product readiness, performance benchmark or production delivery is claimed.

## Ownership and documentation

Changed implementation: `apps/web/src/App.tsx`,
`apps/web/src/features/installation/`, `packages/ui-foundation/src/installation.tsx`
and its export, both Foundation catalogs, and the owned
`tests/e2e/ms-002-installation/` suite/config/lifecycle. Canonical Web/runtime docs,
architecture navigation, generated contributor index and this evidence are updated.
The two `docs-site/docs/{,ru/}install/local.md` help pages are outside the literal
expected-touches list but are separable, directly affected public help updates
explicitly required by the prompt's documentation work. No other scope expansion.

The checkout was clean at entry. No foreign edits were adopted. Plan, pack,
MS-001 artifacts and consumed receipts remain unchanged. The journal is changed
only by its updater. No branch, commit, publication, production mutation or new
upstream dependency was introduced. Disposable browser/API/DB resources belong
to this fixture and are cleaned by its lifecycle; repeat screenshots go to ignored
`test-results/` and cannot overwrite receipt-bound captures; previous installations remain
untouched. Immutable evidence contains no secrets or raw runtime logs.

## S04 handoff

The actual S04 prompt and declared inputs were read: accepted plan, this report
and the installer exist. S03 supplies the entry and host-browser harness. S04 owns
new bundle identity/build, target preparation, packaged HTTPS, Mac/Linux and
second-MacBook Safari LAN proof. These are not missing S03 entry conditions.
This request executes S03 only; S04 remains disallowed until its own request and
normal renewed advance/entry checks. S05 retains final owner visual acceptance.
