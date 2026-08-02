---
artifact_kind: delivery_spec
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
status: accepted
---

# Custometry HTML-first UI foundation specification

## Outcome

Custometry uses one repository-owned UI source from accepted visual decision to
production implementation: semantic CSS tokens, typed React/HTML components,
stable code identities, machine-readable registries, screen manifests, an
interactive component catalog, and browser receipts.

W27's accepted `UI-AN-003` candidate is the sole visual source for the first
foundation slice. The first implementation unit extracts reusable components,
rebuilds Sales Overview from them, proves browser equivalence, and renders the
accepted Focus/Explore composition as independent reuse evidence.

## Invariants

- Product semantics, routes, permissions, actions, data meaning, and required
  states come only from the normative blueprints and executable route/surface
  contracts.
- Historical visual-tool artifacts are evidence only and are never current
  generation input, acceptance targets, or implementation dependencies.
- Tokens own semantic visual values; components own anatomy and behavior;
  manifests own ordered composition; browser receipts own observed proof.
- Components expose stable IDs, versions, typed props, declared variants and
  states, slots, accessibility names, required tokens, and implementation
  identities.
- Catalog and product screens render the same component implementation.
- Screen manifests cannot contain arbitrary visible markup, raw visual values,
  unknown icons, unknown actions, or unregistered components.
- The renderer fails closed on identity, version, schema, action, accessibility,
  or provenance drift.
- Accepted screenshots are evidence, not source input for another executor.

## Eight-point delivery boundary

1. Supersede the previous external synchronization path and require no
   publication or additional external acceptance.
2. Retain earlier unpublished artifacts as immutable historical evidence only.
3. Freeze W27's accepted HTML candidate and browser receipt as the visual
   source for `UI-AN-003`.
4. Extract semantic tokens and at least four reusable component families needed
   by the accepted Sales and Focus/Explore compositions.
5. Version token, icon, component, screen-manifest, and render-receipt schemas
   with repository code identities and fail-closed negative tests.
6. Rebuild Sales Overview from registered components without copying the
   original screen markup.
7. Prove structural and visual equivalence in a real browser across declared
   viewports, states, themes, locales, keyboard, and accessibility checks.
8. Render the accepted Focus/Explore composition from the same foundation as a
   second manifest and reuse proof.

## Source chain

```text
normative product and route contracts
  → W27 accepted visual decisions
  → semantic token contract
  → typed component implementation and registry
  → schema-valid screen manifest
  → deterministic React/HTML render
  → DOM provenance and browser visual audit
  → product decision and immutable receipt
  → later production data integration
```

## Proof seam

The implementation unit must observe:

- exact W27 accepted source identity and unchanged reference screenshots;
- token and code-identity digests;
- positive and negative registry/schema tests;
- component catalog coverage for required states;
- registered-only DOM provenance for Sales and Focus/Explore;
- `1440×900` and `1024×768` geometry and screenshot comparisons;
- `abyss|graphite|frost|paper`, `en|ru`, long-copy, keyboard, focus,
  reduced-motion, clipping, overflow, console, and network evidence;
- one second-composition receipt proving reuse;
- explicit deferral of real ECharts, command palette, typed filters, More
  actions, external share/email/download/export side effects, API integration,
  persistence, performance, release, and deployment.

## Compatibility

- Backend/API/persistence/cache/service-call contracts: `none`.
- Route/product semantics: `none`.
- Accepted browser behavior: `compatible-change`; equivalence is mandatory.
- UI delivery and component identity contracts: `breaking-change` before the
  first stable UI consumer.
- Historical evidence: retained without active dependency.

## Execution authority

This specification defines behavior and proof. One ready delivery ticket owns
the component extraction, registry migration, Sales rebuild, browser QA, reuse
composition, durable evidence, and bounded repair. W22 remains draft until that
ticket is accepted.
