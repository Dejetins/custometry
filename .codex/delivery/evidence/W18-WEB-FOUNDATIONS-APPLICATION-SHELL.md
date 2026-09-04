---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: W18-WEB-FOUNDATIONS-APPLICATION-SHELL
proof_boundary: browser-rendered-frost-foundations-application-shell-and-system-presentation-with-contract-mocks
proof_skills: []
verdict: superseded
redaction: No sensitive data was inspected or recorded.
executed_checks: [reviewed the unexecuted W18 scope against the current owner authority reset, validated the supersession representation with the delivery-ticket validator]
observations: [W18 was ready but unexecuted, its Frost-only foundation is historical, the later unexecuted Linear/Penpot route was also withdrawn, no frontend implementation ticket is currently ready]
---

> Historical supersession record. Statements below about a future pre-G0
> program describe the original reset, not current execution authority.
> The owner selected the final target pilot and removed the G-program on
> 2026-09-04; see `docs/architecture/ui/ui-program-retirement.md` and the
> current Web implementation source contract. W18 remains `superseded`.

# W18 Web Foundations Application Shell Evidence

## Outcome and scope

- outcome: W18 is explicitly superseded before implementation;
- requirement IDs: [THEME-002, I18N-001, I18N-002, I18N-005, I18N-009, I18N-010, A11Y-001, A11Y-003, A11Y-008, A11Y-009, A11Y-010, ROUTE-001, ROUTE-004, ROUTE-009, ROUTE-012, MOTION-001, MOTION-002, MOTION-003, MOTION-011, MOTION-012, SYS-UI-001, SYS-UI-002, SYS-UI-003, SYS-UI-004, SYS-UI-005, HELP-001, HELP-002, HELP-003, HELP-004];
- included: the unexecuted W18 delivery authority and its current withdrawal reason;
- exclusions: no Web, browser, Penpot, accessibility-runtime, API, persistence,
  performance, release, or deployment behavior is claimed.

## Commands and observations

| Command or action | Result | Redacted observation / durable reference |
|---|---|---|
| Review W18 against `docs/adr/0004-ui-design-program-governance.md` | superseded | W18 and the later unexecuted successor route have no current target or execution authority. |
| Inspect current `custometry-ui-blueprint-ru.md` admission state | superseded | `active_program: null` and `visual_authority: null`; future UI work starts from pre-G0 intake. |

## Verdict

`superseded`. W18 was never accepted or implemented. The next safe action is
to record the owner's expanded product path and accepted pre-G0 visual direction
before initializing `ui-design-program` G0.
