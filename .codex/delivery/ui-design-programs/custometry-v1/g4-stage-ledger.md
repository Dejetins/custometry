---
artifact_kind: ui_design_program_stage_ledger
ledger_status: superseded
execution_mode: manual_sequential
goal_artifact_required: false
plan_doc: /Users/daniildegtyarev/Projects/Custometry/.codex/delivery/ui-design-programs/custometry-v1/ui-design-program.json
prompt_pack_dir: /Users/daniildegtyarev/Projects/Custometry/.codex/agents/generated/custometry-ui-design-g4-v1
stage_ledger: /Users/daniildegtyarev/Projects/Custometry/.codex/delivery/ui-design-programs/custometry-v1/g4-stage-ledger.md
selected_ticket: /Users/daniildegtyarev/Projects/Custometry/.codex/delivery/tickets/W30-UI-AN-003-G4-ECHARTS-FAMILY-PROOF.md
iteration_report_template: /Users/daniildegtyarev/Projects/Custometry/.codex/agents/iteration_report_template.md
current_stage: none
Next stage allowed: false
mobile_scope: unauthorized
---

# Custometry UI Design G4 Stage Ledger

| Stage instance | Gate | Target ID | Prompt | Ticket | Status | Dependencies | Stage evidence | Ticket evidence | Owner decision | Executor claim | Claimed at |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `G4@FAM-ROUTE-WORKSPACE-OVERVIEW-BROWSE-FOCUS-CAPABLE-FOCUS-r1` | G4 | `FAM-ROUTE-WORKSPACE-OVERVIEW-BROWSE-FOCUS-CAPABLE-FOCUS@r1` | `/Users/daniildegtyarev/Projects/Custometry/.codex/agents/generated/custometry-ui-design-g4-v1/010-g4-ui-an-003-family-r1.md` | `/Users/daniildegtyarev/Projects/Custometry/.codex/delivery/tickets/W30-UI-AN-003-G4-ECHARTS-FAMILY-PROOF.md` | superseded | `CUSTOMETRY-UI-DESIGN-PROGRAM-V1@5` superseded by the 0.10.0/0.8.0 pre-G0 baseline | historical only | `/Users/daniildegtyarev/Projects/Custometry/.codex/delivery/evidence/W30-UI-AN-003-G4-ECHARTS-FAMILY-PROOF.md` | not applicable | — | — |

`completed`, `blocked`, and `superseded` are terminal for this stage-instance
ID. A rerun requires a new revisioned instance and an explicit dependency on
the prior terminal instance.

## Terminal status

- The owner replaced the program's product semantics and visual-authority
  contract before the G4 executor claim.
- This ledger is terminal `superseded`; it has no claimable row and cannot be
  migrated into a new G0-G6 program.
- Historical atlas, decisions, receipts, and review evidence remain readable.

## Historical validation before supersession

- Commands:
  - `python3 /Users/daniildegtyarev/.codex/skills/ui-design-program/scripts/validate_ui_design_program.py --profile program_ready --project-root /Users/daniildegtyarev/Projects/Custometry .codex/delivery/ui-design-programs/custometry-v1/ui-design-program.json`
  - `source scripts/activate-toolchain.sh && uv run python -m tools.custometry_quality.validate_delivery_tickets`
  - `source scripts/activate-toolchain.sh && uv run python -m tools.custometry_quality.validate_delivery_contract`
  - `python3 /Users/daniildegtyarev/.codex/skills/ui-design-program/scripts/ui_design_tool.py preflight`
  - `source scripts/activate-toolchain.sh && uv run python -m tools.check --scope local`
  - `git diff --check`
  - deterministic triad, source-hash, 62-profile, endpoint-anchor, one-prompt,
    ready-ticket, primary-skill, pending-stage, and mobile-boundary checks
- Observed boundary: accepted program, ready-ticket, prompt-pack, ledger, source,
  and repository-static structure only; no G4 executor claim, screen contract,
  browser, raster, accessibility, implementation, runtime, release, or
  deployment proof
- Result: passed; `program_ready` returned 0 errors and 0 warnings, delivery
  ticket and delivery contract validation passed, UI preflight passed, local
  grouped gate passed, and diff validation passed

## Historical cold-head review receipt

- Cold-head review: completed
- Mode: independent subagent
- Review scope: accepted revision-5 program, single G4 prompt, pending ledger,
  owner evidence, and their direct repository/skill contracts
- Review instructions:
  `architecture-review/references/cold-head-plan-prompt-pack-review.md`
- Verdict: release after fixes
- Blockers fixed: added ready ticket
  `W30-UI-AN-003-G4-ECHARTS-FAMILY-PROOF` and exact
  `.codex/agents/iteration_report_template.md` cross-links
- High findings fixed: `staged-plan-runner` is now primary; screen-contract
  validation first asserts exactly 144 JSON files and passes their sorted file
  list to the validator
- Medium findings fixed: ledger now carries the ticket evidence target and the
  same compact expected-touch envelope as the prompt and ticket
- Local follow-up check: completed; no second reviewer used
- Residual risk: owner evidence intentionally pins the immutable review-state
  manifest hash `e96ad11b8c334f896657409d075b225a9b92195b55de8d0e0b60d586044a498f`
  plus canonical accepted identity hash
  `9ccfd5f5fc21dbc6c0fa59da99dec4cbdf96a43762c06e2ab1f918892e662fbe`;
  the acceptance-state manifest has a different reported byte hash because it
  contains the resulting self-referential owner-decision URI

## Historical expected touch zones

Before supersession, the pending stage and ready ticket shared this write
envelope. It is retained for provenance and grants no current write authority:

- `.codex/delivery/tickets/W30-UI-AN-003-G4-ECHARTS-FAMILY-PROOF.md`
- `.codex/delivery/evidence/W30-UI-AN-003-G4-ECHARTS-FAMILY-PROOF.md`
- `.codex/delivery/evidence/assets/W30-UI-AN-003-G4-ECHARTS-FAMILY-PROOF/**`
- `.codex/delivery/ui-design-programs/custometry-v1/screen-contracts/ui-an-003/**`
- `.codex/delivery/ui-design-programs/custometry-v1/evidence/g4-fam-workspace-overview-browse-focus-r1/**`
- `.codex/delivery/ui-design-programs/custometry-v1/g4-owner-review-ui-an-003-r1.md`
- `.codex/delivery/ui-design-programs/custometry-v1/g4-stage-ledger.md`
- `packages/chart_compiler_ts/**`
- `packages/contracts/ui-design/**`
- `packages/ui-foundation/**`
- `apps/web/package.json`
- `apps/web/src/sales-overview-prototype/**`
- `apps/web/tests/sales-overview-prototype.test.tsx`
- `apps/web/tests/sales-overview-prototype/**`
- `pnpm-lock.yaml`

## Historical file manifest summary

- created:
  - `.codex/agents/generated/custometry-ui-design-g4-v1/010-g4-ui-an-003-family-r1.md`
  - `.codex/delivery/tickets/W30-UI-AN-003-G4-ECHARTS-FAMILY-PROOF.md`
  - `.codex/delivery/ui-design-programs/custometry-v1/g4-chart-rendering-policy-owner-acceptance-r5.json`
  - `.codex/delivery/ui-design-programs/custometry-v1/g4-chart-rendering-policy-owner-review-r5.md`
  - `.codex/delivery/ui-design-programs/custometry-v1/g4-stage-ledger.md`
- modified:
  - `.codex/AGENTS.md`
  - `.codex/delivery/ui-design-programs/custometry-v1/ui-design-program.json`
  - `custometry-technical-blueprint-ru.md`
  - `custometry-technical-blueprint-human-ru.md`
  - `custometry-ui-blueprint-ru.md`
  - `docs/architecture/system-design.md`
  - `docs/generated/requirement-index.json`
- deleted: []
- outside_expected_paths: []
- foreign_changes_excluded: true

## Handoff

- Residual risk: the historical evidence remains truthful but does not cover
  the owner's expanded analytical-document, segment, digital, product/category,
  adoption, or performance requirements.
- No executor may claim or resume this row. A future authorized UI program must
  create a new revisioned pre-G0 path from the current blueprints and pilot
  manifest; it must not migrate this terminal row into a claimable state.
- Next stage allowed: false
