---
artifact_kind: ui_design_owner_review
program_id: CUSTOMETRY-UI-DESIGN-PROGRAM-V1
gate_id: G3
validation_profile: program_ready
review_revision: 5
accepted_baseline_revision: 4
accepted_baseline_validation_profile: program_ready
accepted_baseline_owner_decision_ref: owner-decision://eae547c42c2babd0ed1dffd9635c388205dd15ac69e04eaee86581540c42dd2c/.codex/delivery/ui-design-programs/custometry-v1/g3-owner-acceptance-r4.json?value_sha256=813053a1e977cab2d6baa38567fea7206220f0620d766ae660a3847a97f56828#/decisions/0
accepted_baseline_manifest_sha256: 9ef53c33260421a8d1131c0b2caef0649ffb666de130bd4fb0990ed1081c8880
manifest_sha256: e96ad11b8c334f896657409d075b225a9b92195b55de8d0e0b60d586044a498f
source_hashes:
  - .codex/AGENTS.md:62fc111d172c1d6382c60c5b7020f9b15a717aaa63af5061b5f429137bfb5b45
  - custometry-technical-blueprint-ru.md:197d6b8049db536d30c94f7bf84b5b2ba3882f7fc88c1c16ab63a42c2c0fe3f9
  - custometry-technical-blueprint-human-ru.md:593ba5a43d419e0c69fe7d49dd3ebdbe6e744d0df4e7a54accc5869ad191f6f9
  - custometry-ui-blueprint-ru.md:9ca1697652f3ee00a8062231c760d8d79ea82c3c43378d9c78de0f3cdd64fa6c
  - docs/architecture/system-design.md:eef5f8c3b78eb5ac39c8c703b19bb678ef3ca06adebc96e5487d67003b88f78a
mobile_scope: unauthorized
agent_self_acceptance: prohibited
---

# Owner review: chart rendering and user chart-type selection policy

## Review identity

- Program: `CUSTOMETRY-UI-DESIGN-PROGRAM-V1`.
- Proposed revision: `5`, status `review`, validation profile
  `program_ready`.
- Accepted baseline retained without rewriting: revision `4`,
  `program_ready`, exact acceptance and manifest hashes pinned above.
- This revision updates source hashes and the downstream G4 contract boundary.
  It does not accept a G4 family or advance to G5/G6.
- The user request that accepts this revision also authorizes preparation of
  the exact `manual_sequential` prompt-pack and stage-ledger links recorded in
  the manifest. Their presence does not execute or accept the pending stage.

## Owner-directed policy encoded in sources

The normative product and UI sources now require:

1. Apache ECharts is the actual renderer for every new chart-bearing G4+
   browser-proven or production Web surface. A hand-authored SVG, CSS, Canvas,
   or HTML chart substitute cannot prove that boundary.
2. Any authorized immutable dataset or derived chart-data artifact may be a
   chart source when its schema, grain, semantic roles, cardinality,
   bounded-data policy, and access policy pass versioned compatibility rules.
   This is not permission to force every dataset into every chart type.
3. The ordered `available_chart_types` and default are resolved for the exact
   dataset profile and report type. Different report types may expose different
   choices and defaults.
4. The user sees the current chart type and may select any compatible type.
   Unsupported types are unavailable with a localized reason. Saving the
   selection creates a versioned `ChartSpec` or versioned presentation binding
   without silently changing source, filters, grain, measures, permissions, or
   Result Trust.
5. Accessible chart table alternatives and product data grids remain separate
   HTML/React surfaces. ECharts `dataset` or `dataView` does not replace them.

The machine requirement IDs are `CHART-020`, `CHART-021`, `CHART-022`, and
`CHART-023`; `CHART-004` remains the existing ECharts-only v1 renderer lock.

## G4 consequence

- Every new G4 family screen contract containing a chart must name the real
  ECharts/ChartSpec/shared-compiler boundary and its chart-type selector state.
- Browser and raster acceptance for such a screen must observe actual ECharts
  output at every declared responsive-Web anchor. Placeholder chart geometry
  is not renderer proof.
- The accepted W27 `UI-AN-003` pilot remains truthful historical composition,
  shell, density, and geometry evidence. Its deferred/custom chart rendering is
  not reusable proof of ECharts and must be replaced or re-proven when the
  chart-bearing G4 contract executes.
- No G4 screen contract currently exists, so no accepted G4 contract or receipt
  is invalidated. The 17 family reuse hypotheses remain hypotheses.

## Contract impact

| Surface | Classification | Consequence |
|---|---|---|
| Product/UI documentation | compatible-change | Adds required chart-source compatibility and user-selection behavior before production implementation |
| Browser-visible behavior | compatible-change | Adds a chart-type selector and forbids new mock charts from claiming ECharts proof |
| `ChartSpec` DTO/schema | compatible-change before implementation | Adds source-backed selection metadata; concrete schema migration belongs to a future implementation ticket |
| API, persistence, cache/request identity | unknown until implementation | A future specification/ticket must define transport, persistence, versioning, and identity changes |
| Existing production runtime | none observed | ECharts and the compiler are not yet installed/implemented in the current Web runtime |

## Proof boundary

- `program_ready` validation proves source hashes, manifest structure,
  responsive coverage, and accepted-baseline continuity only.
- No ECharts package, compiler implementation, compatibility resolver, chart
  selector, API, persistence, browser, raster, accessibility, performance,
  release, or deployment work is included.
- Prompt-pack and ledger creation is limited to one pending G4 family stage;
  no executor claim or stage status advancement is included.
- Mobile remains `unauthorized`; no mobile chart composition is introduced.

## Exact owner decision

Choose one exact unchanged identity:

- `accept CUSTOMETRY-UI-DESIGN-PROGRAM-V1 revision 5 validation_profile program_ready`
- `reject CUSTOMETRY-UI-DESIGN-PROGRAM-V1 revision 5 validation_profile program_ready: <reason>`
- `request changes to CUSTOMETRY-UI-DESIGN-PROGRAM-V1 revision 5 validation_profile program_ready: <bounded changes>`

No agent may infer or record acceptance from the policy request alone. Revision
5 remains `review` until the owner names the exact program identity above.
