---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: W28-UI-AN-003-FIGMA-SYNCHRONIZATION
status: superseded
workstream_id: W28
summary: Consume the formally accepted UI-AN-003 HTML pilot, remove the remaining index-first design-contract drift, synchronize the accepted responsive candidate into the exact Custometry Figma library and product files, and freeze the minimum proven UI foundation v1 without changing HTML or production runtime behavior.
requirement_ids: [WEB-ARCH-003, WEB-ARCH-005, WEB-ARCH-006, THEME-001, THEME-002, THEME-003, THEME-005, THEME-008, UI-SHELL-001, UI-SHELL-002, UI-SHELL-003, UI-DENSITY-001, UI-DENSITY-002, UI-DENSITY-003, FILTER-001, FILTER-002, FILTER-003, FILTER-004, FILTER-010, COMPARE-001, COMPARE-002, COMPARE-003, CHART-001, CHART-002, CHART-006, FOCUS-001, FOCUS-002, FOCUS-003, FOCUS-004, FOCUS-005, FOCUS-006, FOCUS-007, FOCUS-008, FOCUS-009, FOCUS-010, A11Y-001, A11Y-003, A11Y-008, ROUTE-004]
blockers: [W27-UI-AN-003-HTML-CONTRACT-COMPLETION]
supersession_reason: The product owner accepted the repository-owned HTML-first UI foundation path on 2026-08-02; this external synchronization unit is retained only as historical evidence and is no longer an active delivery dependency.
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - .codex/delivery/tickets/W27-UI-AN-003-HTML-CONTRACT-COMPLETION.md
  - .codex/delivery/evidence/W27-UI-AN-003-HTML-CONTRACT-COMPLETION.md
  - .codex/delivery/evidence/W21-CONTRACT-COMPILED-UI-PILOT.md
  - .codex/delivery/specs/custometry-contract-compiled-ui-prototyping-pilot.md
  - custometry-ui-blueprint-ru.md
start_probe:
  boundary: exact authorized Figma library hX3nQOtcSdCc97uv26m9eG page 0:1 and product file MXfxuhSFpIczbUtFmOSyPp page 0:1, including preserved W21 product node 40:536 and its registered library identities
  read_only_check: use figma:figma-use before any write to confirm both files are Figma Design targets, compare their current top-level and registered component inventory with W21 evidence and packages/contracts/ui-design, confirm node 40:536 is still readable, and capture any intervening drift without inspecting credentials, cookies, browser storage, or unrelated files
  stop_on: [unavailable, identity_mismatch, state_drift]
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W28-UI-AN-003-FIGMA-SYNCHRONIZATION.md
    - .codex/delivery/evidence/W28-UI-AN-003-FIGMA-SYNCHRONIZATION.md
    - .codex/delivery/evidence/assets/W28-UI-AN-003-FIGMA-SYNCHRONIZATION/**
    - .codex/delivery/specs/custometry-contract-compiled-ui-prototyping-pilot.md
    - .codex/delivery/tickets/W22-WEB-LINEAR-APPLICATION-SHELL.md
    - custometry-ui-blueprint-ru.md
    - docs/architecture/ui/custometry-linear-ui-migration-registry-v1.json
    - packages/contracts/ui-design/**
    - tools/custometry_quality/ui_design/**
    - tests/ui_design/**
    - external:figma/hX3nQOtcSdCc97uv26m9eG/**
    - external:figma/MXfxuhSFpIczbUtFmOSyPp/**
  forbidden_write_paths:
    - apps/web/**
    - packages/ui-foundation/**
    - packages/contracts/routes/**
    - packages/localization/**
    - apps/api/**
    - apps/worker_data/**
    - packages/analytics_core/**
    - packages/analytics_customer/**
    - packages/analytics_sales/**
    - migrations/**
    - deploy/**
    - external:figma/ghv0Cv3ddqMvv3zFVvR22p/**
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: browser
  proof_skills: [figma:figma-use, figma:figma-generate-library, figma:figma-generate-design, better-layout, better-ui, better-accessibility, browser-qa-evidence, playwright-cli, contract-impact-analysis]
  commands:
    - read AGENTS.md and .codex/AGENTS.md, then execute this ticket as one bounded unit without creating a Goal, branch, worktree, stash, prompt pack, deployment, or publication
    - before any Figma write, record the start_probe identity and drift result and stop rather than replaying a write when target state is unknown
    - confirm W27 ticket frontmatter has status accepted, W27 evidence frontmatter has product_owner_decision accepted, and the W27 Product-owner acceptance record body has terminal outcome pilot_passed, post-pilot decision scale, and the exact accepted visual source before any normative or Figma write
    - replace current operational index-first and Master Elements Index requirements, the ghv0Cv3ddqMvv3zFVvR22p target, and W22 index/detail-map inputs with the accepted contract to responsive HTML to browser validation to product-owner acceptance to bounded Figma synchronization to production implementation sequence; retain historical and supersession evidence as truthful history
    - preserve W21 accepted and verification nodes as historical evidence; create versioned W28 library components and product compositions instead of destructively overwriting W21 evidence
    - "synchronize only the accepted UI-AN-003 slice: semantic color spacing radius and typography tokens; expanded collapsed hidden and resizable Sidebar; Sidebar utilities Help User menu and Nav Item states; Icon Button and segmented controls; KPI rail; Chart toolbar; Context panel with compact filter and share rows; Result Trust trigger and drawer; Focus Explore shell; breakdown and percent versus absolute controls; required tables and chart containers"
    - render the accepted Sales Overview Chart and Data states, Result Trust drawer, Focus chart, Focus breakdown, expanded collapsed hidden and resized Sidebar states, and a compact smaller-desktop state into MXfxuhSFpIczbUtFmOSyPp using library instances from hX3nQOtcSdCc97uv26m9eG
    - require zero detached component instances, zero unknown component IDs, zero raw hand-drawn icons, zero unbound semantic paints, zero unbound text styles, exact registered icon identities, and no speculative components for routes outside the accepted slice
    - compare fresh 1440 by 900 and 1024 by 768 HTML reference captures with Figma exports; require exact token values, no clipping or overlap, matching content and control order, matching 32 px compact control heights, matching 12 px shell rhythm, and component bounding-box axes within 1 px at the same declared viewport
    - run Russian long-copy stress for the synchronized product states with no detected text overflow or clipped interactive labels; four-theme output is semantic-token verification and not four separate aesthetic acceptances
    - perform Figma read-back after every mutation group, reconcile uncertain writes by exact-target read-back before retry, allow at most two deterministic repair passes, and never blind-replay an external write
    - inherit product_decision accepted from W27 only when the Figma output is an objective within-tolerance synchronization with no new product or visual decision; otherwise preserve the candidate as not accepted and stop with exact findings without requesting or inventing product-owner approval
    - freeze the minimum proven UI foundation v1 by versioning tokens components icons manifest renderer and receipts, recording permitted variants and states, shell and responsive rules, Figma-to-frontend component contracts, and the explicitly deferred ECharts command palette More actions typed-filter and external share email download export boundaries
    - update the migration registry and delivery graph to the slice-first scale decision and make W22 consume W28 accepted foundation contracts rather than an index or detail maps
    - source scripts/activate-toolchain.sh
    - uv run python -m tools.custometry_quality.ui_design
    - uv run python -m tools.custometry_quality.ui_design.compile_render_plan --check
    - uv run pytest tests/ui_design
    - uv run python -m tools.custometry_quality.validate_blueprints
    - uv run python -m tools.custometry_quality.generate_requirement_index --check
    - uv run python -m tools.custometry_quality.validate_route_registry
    - uv run python -m tools.custometry_quality.check_i18n_parity
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - uv run python -m tools.custometry_quality.validate_delivery_contract
    - uv run python -m tools.check --scope local
    - git diff --check
  proof_boundary: product-owner-accepted-local-html-equivalent-figma-ui-an-003-synchronization-plus-versioned-minimum-design-foundation-contracts-and-read-back-evidence
  evidence_target: .codex/delivery/evidence/W28-UI-AN-003-FIGMA-SYNCHRONIZATION.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: [.codex/delivery/evidence/W28-UI-AN-003-FIGMA-SYNCHRONIZATION.md]
---

# Outcome

The explicit product-owner acceptance closes W27 as `pilot_passed` with
`scale`. The accepted responsive HTML candidate becomes the sole current visual
source for a non-destructive, versioned synchronization into `Custometry UI
Library` and `Custometry Authenticated Platform UI`. The repository and Figma
read back one minimum proven UI foundation v1 for the UI-AN-003 slice, while
HTML, production runtime code, backend behavior, and historical evidence remain
unchanged.

# Non-goals

- Do not redesign UI-AN-003, generate alternative directions, or introduce a
  new product, information-architecture, navigation, data, or interaction
  decision.
- Do not edit the accepted HTML prototype, its tests, `apps/web/**`, or
  `packages/ui-foundation/**`.
- Do not implement ECharts, command palette, typed filter expressions or chips,
  More page actions, or real share, email, download, and export side effects.
- Do not create a global component index, an all-route design system, detail
  maps, speculative components, UI-AN-004 or UI-AN-015 screens, runtime code,
  release artifacts, or deployment changes.
- Do not delete, relabel, or mutate W03-W10 Penpot evidence, W21 Figma pilot
  nodes, W24-W27 browser evidence, or the superseded W21 index-first artifacts.
- Do not claim production, API, persistence, complete accessibility,
  performance, release, or deployment readiness.

# Work and repair boundary

Execute this ticket autonomously in the following mandatory order:

1. **Acceptance guard.** Confirm W27 ticket/evidence contain the exact accepted
   fields authorized by the user on 2026-08-01. Treat any mismatch as a blocker
   and do not alter W27 historical browser observations.
2. **Normative reconciliation.** Remove operational index-first, Master
   Elements Index, old-target, and index/detail-map consumption requirements
   from current sources. Preserve historical descriptions only where clearly
   marked superseded or historical.
3. **Figma pre-write guard and synchronization.** Use the exact authorized
   files and current registered identities. Preserve W21 nodes, apply W28 as a
   new versioned slice, and read back after each mutation group.
4. **Foundation freeze.** Version only the proven contracts and update W22,
   the migration registry, and the delivery graph to consume them.
5. **Terminal proof.** Run every invalidated contract, Figma, browser-reference,
   repository, and diff gate before changing W28 to `accepted`.

The user has delegated exact-equivalence acceptance so the executor does not
need another live review when every objective gate passes and no new decision
is made. This delegation does not authorize invention. If the current Figma
state has drifted, a new decision is required, an external write remains
uncertain after read-back, the two-pass repair budget is exhausted, or an
allowed path is insufficient, stop with W28 unaccepted and record the smallest
next safe action. Do not ask for confirmation mid-run and do not broaden scope.

# Acceptance evidence

The terminal evidence must include:

- the exact accepted W27 status, product-owner decision, `pilot_passed`,
  `scale`, and accepted visual source consumed without alteration of prior
  observed proof;
- a bounded old/current drift inventory proving that current normative sources
  no longer instruct agents to use index-first, Master Elements Index,
  `ghv0Cv3ddqMvv3zFVvR22p`, accepted index, or detail maps for active delivery;
- before/after Figma inventories for both exact file keys, preserved W21 node
  identities, new versioned W28 node identities, and mutation receipts;
- token, component, icon, manifest, renderer, and receipt versions plus digests
  and compatibility classification;
- component-instance, detachment, raw-icon, semantic-paint, text-style, icon
  identity, geometry-axis, spacing, and clipping audits;
- fresh HTML reference and Figma export comparisons at `1440 × 900` and
  `1024 × 768`, plus Russian-copy and four-theme semantic-token receipts;
- screenshots for all required product states and a normalized read-back
  receipt proving the synchronized state inventory;
- every command result, repair attempt, target read-back after uncertain writes,
  contract impact, explicit proof exclusions, and residual risks;
- `machine_conformance: passed`, `product_decision: inherited_from_W27`,
  `implementation_readiness: not_assessed`, and final W28 `status: accepted`
  only when all required evidence passes.

The final agent report must be in Russian and state the actual changed paths,
Figma file and node identities, validation commands and results, observed proof
boundary, residual risk, and the next safe ticket. It must not stage, commit,
push, publish, deploy, or create another ticket unless separately authorized.
