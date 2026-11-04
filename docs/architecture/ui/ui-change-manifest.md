# UI change manifest

Owner decision, 2026-10-10. Read this short entrypoint before changing UI.
It replaces mandatory pilot fidelity, not product semantics or frontend architecture.
Routing: [agent instructions](../../../.codex/AGENTS.md),
[implementation contract](custometry-web-implementation-source-contract-v1.md).

## Working principle

- **Preserve:** keep the shared visual tone of the current interface; do not
  treat every existing inconsistency as a standard.
- **Explore:** experiment in the selected area while preserving its surroundings.
- **Adopt:** when the owner explicitly selects a result, record it briefly as
  a reusable reference for similar tasks. It can evolve through later decisions.

## Before editing

1. Inspect the affected current screen and its implementation. If runtime and
   checkout differ, resolve the source for the affected work before editing it.
2. Identify what the owner wants to keep, change, or explore. The latest explicit
   owner decision supersedes older visual decisions within that scope. The
   [preserved pilot](target-pilot/README.md) and other prototypes are historical
   references, not mandatory templates; read them only when relevant.
3. Choose the closest suitable current composition and code to reuse. Preserve
   the surrounding interface's type hierarchy, density, spacing/alignment,
   surfaces, icons, control states and placement of actions unless those are
   being changed. Existing inconsistencies are not automatically standards.
   State the reference, intended change and any unresolved design choice briefly
   in the task; no separate inventory or design document is required.

## Choose the route

- **Existing pattern fits:** reuse its implementation; change only what the task
  needs. Routine reuse needs no additional owner approval.
- **Direction is unresolved:** make a small, reversible interactive experiment
  within authorized scope. Compare distinct alternatives only when useful.
  Ask about a missing material product choice, not every spacing or code choice.
- **Owner requests a redesign:** change the named surface, preserve unaffected
  decisions, and check shared consumers before changing shared styles. Neither
  old pilot fidelity nor existing code vetoes the request. An experiment does
  not become a platform standard without an explicit owner decision.

## Check and finish

Inspect the rendered result against the selected reference and intended changes:
composition, visual tone, affected states and the user's action. Use relevant
craft skills for a specific gap; use browser QA for changed behavior. Do not
launch a full design audit or creative redesign for an ordinary UI edit.
Batch visual corrections and confirm them; avoid open-ended optional polishing.
Report unresolved defects rather than declaring success at an iteration limit.
Follow the implementation contract for required boundary-specific checks.

When a decision becomes reusable, update the nearest existing source briefly:
what was selected, its scope and what it replaces. Update affected links/rules;
do not create a new registry, ledger or full-platform design map by default.
