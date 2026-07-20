---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: W19-LINEAR-REFERENCE-COMPLETION
proof_boundary: sanitized-reproducible-linear-reference-measurements-and-evidence-gap-closure
proof_skills: [browser-qa-evidence, playwright]
verdict: passed
redaction: No screenshots, recordings, cookies, tokens, browser profiles, storage state, account exports, provider payloads, raw accessibility snapshots, or private content are tracked; only hashes, aggregate geometry, timings, roles, counts, and explicit waivers are durable.
executed_checks:
  - confirm ROE-6 is Todo through Linear MCP without changing Linear
  - confirm W19 ticket is ready and local main equals freshly fetched origin/main
  - confirm no active worktree or ready-ticket owned-path overlap
  - confirm /Users/daniildegtyarev/Downloads/reference.zip SHA-256 equals the pinned ticket hash
  - verify all 16 screenshot hashes and raster metadata without tracking third-party captures
  - inspect the existing authenticated ROE-6 tab through sanitized Playwright-derived observations
  - exercise command menu, keyboard focus, sidebar resize/collapse/restore, popover, modal, Escape/focus return, route, and browser Back without mutating Linear data
  - observe 1440x900 and 1280x800 controlled desktop viewports and restore the original viewport/sidebar state
  - inspect bounded console warnings/errors and record unavailable network evidence truthfully
  - uv run python -m tools.custometry_quality.validate_delivery_tickets
  - source scripts/activate-toolchain.sh && uv run --locked python -m tools.check --scope local
  - git diff --check
observations:
  - The archive matched eb7b0ab070f64d553baafacefa90fdb2e87e51bc174c63db9af73bc77f8e41c2 and all 16 manifest screenshot hashes matched.
  - Chrome 150.0.7871.129 on macOS 15.7.4, Apple M3 Pro, 19327352832 bytes RAM was observed without reading authentication storage.
  - Sanitized browser evidence closed keyboard, resize, accessibility-structure, focus-return, and component-geometry gaps and partially closed command-menu evidence.
  - Seven explicit waivers retain downstream obligations for Custometry themes, project-owned server states, clean route/history/drawer proof, decomposed performance, archive CSS scale, reduced motion, and non-destructive command execution.
  - No console warning/error was observed; safe network timing/status telemetry was unavailable and is not claimed.
---

# W19-LINEAR-REFERENCE-COMPLETION Evidence

> Compact evidence for one terminal ticket. It is not another execution-state
> source or a replacement for the product specification.

## Outcome and scope

- outcome: the pinned Linear archive and one live authenticated reference tab
  now have a sanitized, reproducible measurement record; every originally
  listed evidence gap is either closed or explicitly waived with impact;
- requirement IDs: [WEB-ARCH-005, WEB-ARCH-006, WEB-PERF-001, WEB-PERF-002,
  THEME-001, THEME-008, A11Y-001, A11Y-003, MOTION-001, MOTION-012];
- included: source identity, screenshot hashes and physical raster metadata,
  live viewport/scale, component geometry, keyboard/focus, command menu,
  sidebar resize/collapse/restore, modal/popover focus return, bounded timings,
  console observation, redaction, and explicit waivers;
- exclusions: no Penpot, Custometry product code, Linear issue data, provider
  assets, recordings, browser state, auth/network manipulation, deployment, or
  release work. This does not prove a Custometry runtime.

## Commands and observations

| Command or action | Result | Redacted observation / durable reference |
| --- | --- | --- |
| Linear MCP `get_issue(ROE-6)` | pass | Issue was `Todo` at both the initial and immediate pre-write guards; no Linear status or content was changed. |
| Repository pre-write guards | pass | W19 was `ready`; `main` and freshly fetched `origin/main` were `4c6628cf4807cf7ff069f09e066007b7fead63cc`; the main worktree was clean; W11 ownership was disjoint. |
| Archive start probe | pass | Exact SHA-256 pinned match; 2,381,246 bytes; 16 screenshots and 16 macOS metadata entries. |
| Screenshot verification | pass | All 16 screenshot hashes matched the manifest; all were 2560x1440 physical pixels at PNG metadata 72 dpi. |
| Sanitized Playwright browser QA | pass with declared waivers | Measurements below retain only sanitized aggregates; no raw snapshot, screenshot, recording, profile, or auth state is tracked. |
| Viewport matrix | pass | 1440x900 and 1280x800 at device scale 1 were observed; default 1512x790 at scale 2 was restored. No document-level overflow at 1280x800. |
| Sidebar restore | pass | Final live sidebar width was 305 px after an initial 304 px measurement; original viewport was restored. |
| Console/network boundary | partial with waiver | Bounded console warning/error count was zero. Sanitized network status/timing was unavailable and is assigned to W20/W22/W23. |
| Evidence-gap reconciliation | pass | Manifest `missing_required_evidence` is empty because each original item has a `closed`, `closed_with_derived_measurements`, `waived`, or `partially_closed_with_waiver` disposition and explicit impact. Command execution is explicitly assigned to W22/W23. |
| `uv run python -m tools.custometry_quality.validate_delivery_tickets` | pass | `PASS validate_delivery_tickets (observed=true)` with 26 tickets. |
| `source scripts/activate-toolchain.sh && uv run --locked python -m tools.check --scope local` | pass | `PASS check:local (observed=true)` under Node 24.18.0, pnpm 11.13.0, and uv 0.9.26. |
| `git diff --check` | pass | No whitespace errors in the assembled W19 change. |

## Sanitized measurements

### Source and viewport

| Field | Observation |
| --- | --- |
| Archive | 2,381,246 bytes; 16 screenshots plus 16 macOS metadata entries; every screenshot hash matched the manifest. |
| Raster | Every screenshot is 2560x1440 physical pixels at PNG metadata 72 dpi, with browser chrome included. CSS viewport and scale are not embedded. |
| Archive geometry | Browser content begins near physical `y=108`; primary boundary near `x=256`; secondary Inbox column `x=257..656` (399 px); content begins near `x=657`; projects detail pane near `x=2156..2542` (386 px); customize-sidebar modal near `x=1041..1519` (478 px). |
| Live browser | Google Chrome 150.0.7871.129 on macOS 15.7.4 arm64, Apple M3 Pro, 19,327,352,832 bytes RAM. |
| Default viewport | 1512x790 CSS px at device scale 2. |
| Controlled viewports | 1440x900 and 1280x800 CSS px at device scale 1. At 1280x800 the document had no root horizontal or vertical overflow. |

Archive coordinates are physical pixels only and cannot be converted to CSS
tokens without an independently declared scale.

### Live geometry and interaction

| Surface | Observation |
| --- | --- |
| Expanded shell | At 1440x900 the initial navigation width was 304 px; main began at `x=304`, width 1128 px, height 856 px. |
| Resize | One 7 px high-span `col-resize` target. Observed expanded widths included 220, 249, 283, 304/305, and a bounded maximum of 330 px. |
| Collapse/restore | Collapse produced an approximately 48 px rail boundary and an accessible `Menu` restore control. Final default-viewport sidebar width was restored to 305 px, within 1 px of the initial measurement. |
| Command menu | `Meta+K` produced one active expanded `Command menu` combobox/listbox with text entry and active descendant; Escape closed it. Execute was waived because available commands mutated issue state or copied provider content. |
| Issue popover | One non-modal dialog/listbox about 211x522 px autofocuses `Filter…`; Escape returned focus to `Issue options`. |
| Create modal | `aria-modal=true`, 1440x900 wrapper, issue-title autofocus, computed 0.3 s wrapper transition; Escape created nothing and returned focus to `Create new issue`. |
| Route/history | Cold navigation from the claimed ROE-6 tab to Inbox reached the route in 3,190 ms. Back restored a pre-existing different issue entry, so claimed-tab history is not deterministic continuity proof; the tab was returned directly to ROE-6. |

Pointer-gesture wall times (225-380 ms) include browser-control transport and
are not frame or animation measurements.

### Accessibility structure

The sanitized snapshot exposed navigation, main, skip link, buttons, links,
textboxes, combobox/listbox, dialog, modal, status, and switch semantics. A
15-step Tab sample began with the skip link and continued through workspace,
search, create, primary navigation, group controls, and settings. Named links
and controls generally exposed a one-pixel outline or focus box; two sampled
group toggles had no direct outline/box-shadow, so their visual focus treatment
is not accepted as a target. The collapsed navigation snapshot contained 24
interactive descendants, 19 with a derived name and 14 directly focusable.
This is reference structure, not an accessibility-conformance verdict.

### Timing samples

These are wall-clock Playwright observations through the Chrome extension and
include automation transport. They are not a client/network/API/render split.

| Interaction | n | Samples (ms) | p50 | p75 | p95 | Interpretation |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| Command menu open, warm | 12 | 121, 66, 65, 68, 65, 61, 64, 63, 70, 65, 316, 63 | 65 | 68 | 316 | One retained outlier prevents a passing p95 claim. |
| Issue popover open, warm | 8 | 328, 332, 330, 331, 340, 318, 328, 345 | 330 | 332 | 345 | Transport-dominated; computed open-state transition was 0 s. |
| Create modal first open | 1 | 357 | n/a | n/a | n/a | Structure/focus only; wrapper computed transition 0.3 s. |
| Inbox cold route | 1 | 3190 | n/a | n/a | n/a | Provider/network work cannot be decomposed. |

No recurring-main-thread-task, network, API, or render conclusion is made.
The bounded console warning/error count was zero; sanitized network telemetry
was unavailable.

## Explicit waiver summary

The waivers do not turn unknown provider behavior into accepted Custometry
behavior. They allocate the remaining proof to the tickets that own it:

1. W21 owns the project-designed four-theme representation; W22/W23 own the
   real four-theme browser matrix.
2. W22/W23 own loading, error, stale/degraded, forbidden, and session-expired
   project states using local fixtures.
3. W20 owns state and benchmark seams; W22/W23 own clean route, history,
   drawer, network/API/render, frame-cadence, and reduced-motion browser proof.
4. Archive pixels remain physical-only; later evidence must declare exact CSS
   viewport and scale.
5. W22/W23 must execute a project-owned non-destructive command and verify its
   result and focus return.

ROE-11/W20 and ROE-14/W21 were not changed or started.

## Verdict

`passed` at the declared sanitized-reference boundary. The durable pack makes
the reference geometry, interaction grammar, proof gaps, and downstream
obligations inspectable without distributing third-party captures or retaining
authentication state. It does not claim provider accessibility compliance,
Custometry runtime readiness, CI/release readiness, or deployment evidence.
