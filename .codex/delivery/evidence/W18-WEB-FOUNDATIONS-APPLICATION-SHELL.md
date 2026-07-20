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
executed_checks: [compared W18 scope with the accepted Linear-workspace transition specification and migration registry, validated the supersession representation with the delivery-ticket validator]
observations: [W18 was ready but unexecuted, its Frost-only foundation conflicts with the four-theme Linear-workspace target, W19-W23 are the accepted replacement path]
---

# W18 Web Foundations Application Shell Evidence

## Outcome and scope

- outcome: W18 is explicitly superseded before implementation;
- requirement IDs: [THEME-002, I18N-001, I18N-002, I18N-005, I18N-009, I18N-010, A11Y-001, A11Y-003, A11Y-008, A11Y-009, A11Y-010, ROUTE-001, ROUTE-004, ROUTE-009, ROUTE-012, MOTION-001, MOTION-002, MOTION-003, MOTION-011, MOTION-012, SYS-UI-001, SYS-UI-002, SYS-UI-003, SYS-UI-004, SYS-UI-005, HELP-001, HELP-002, HELP-003, HELP-004];
- included: the unexecuted W18 delivery authority and its replacement mapping;
- exclusions: no Web, browser, Penpot, accessibility-runtime, API, persistence,
  performance, release, or deployment behavior is claimed.

## Commands and observations

| Command or action | Result | Redacted observation / durable reference |
|---|---|---|
| Compare W18 with `.codex/delivery/specs/custometry-linear-workspace-ui-transition.md` | superseded | W18 is Frost-only; the accepted successor requires React/MobX/Query/styled-components, four themes, Penpot vNext, reversible routing, and measured response-to-paint proof. |
| Inspect `docs/architecture/ui/custometry-linear-ui-migration-registry-v1.json` | superseded | W19-W23 replace the old shell ticket without rewriting accepted W03-W10 evidence. |

## Verdict

`superseded`. W18 was never accepted or implemented. The next safe action is
W19, followed by the dependency-ordered W20-W23 transition graph.
