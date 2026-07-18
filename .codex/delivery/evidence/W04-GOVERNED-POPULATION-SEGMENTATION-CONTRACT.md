---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.1-draft
ticket_id: W04-GOVERNED-POPULATION-SEGMENTATION-CONTRACT
proof_boundary: static-product-ui-architecture-and-executable-contract-synchronization
proof_skills: []
verdict: passed
redaction: No credentials, customer data, Penpot payloads, browser state, environment dumps, or external-provider data were retained.
executed_checks:
  - uv run --locked pytest -q tests/tooling/test_static_quality_tools.py -k 'route_registry or blueprint or delivery_ticket'
  - uv run --locked python -m tools.custometry_quality.validate_blueprints
  - uv run --locked python -m tools.custometry_quality.generate_requirement_index --check
  - uv run --locked python -m tools.custometry_quality.validate_route_registry
  - uvx check-jsonschema --schemafile packages/contracts/routes/ui-route-contracts.schema.json packages/contracts/routes/ui-route-contracts.json
  - uvx check-jsonschema --schemafile packages/contracts/routes/ui-surface-contracts.schema.json packages/contracts/routes/ui-surface-contracts.json
  - uv run --locked python -m tools.custometry_quality.validate_delivery_tickets
  - uv run --locked python -m tools.custometry_quality.check_docs_links
  - uv run --locked python -m tools.custometry_quality.generate_docs_index --check
  - uv run --locked python -m tools.check --scope local
  - uv run --locked python -m tools.check --scope ci
  - uv run --locked ruff check apps/api/src migrations tests tools
  - uv run --locked pyright apps/api/src tests/integration
  - uv run --locked pytest -q
  - uv run --locked mkdocs build --strict --config-file mkdocs.yml
  - pnpm check
  - git diff --check
observations:
  - Product specification 0.9.1-draft and UI specification 0.6.1-draft contain 827 synchronized requirement IDs.
  - "The route inventory remains 110 routes: 91 Penpot-baseline routes and 19 explicit Penpot-backlog routes."
  - The UI surface contract now contains 25 overlays, 5 system surfaces, 19 cross-surface capabilities, and exactly one binding for each UC-001 through UC-026.
  - TypeScript route and localization tests assert all 110 normative routes instead of the historical 91-frame Penpot baseline.
  - Governed population treatment supports versioned quantile, IQR, and MAD methods with flag, exclude, and winsorize actions, shared versus-LY bounds, sensitivity evidence, policy ceilings, and immutable result references.
  - Governed segmentation supports rule, bucket, stratified, and exact-K KMeans methods with reproducible fit/assignment semantics, diagnostics, versioned memberships, and CPU-only execution.
  - Accepted W03 evidence remains unchanged and truthful for Penpot revision 124 and repository-input fingerprint db4a400c3591eb725906f8c5dc44aa3baba91ba2948070b335215ce911f31e37.
  - docs/architecture/system-design.md is the sole maintained System Design source; the duplicate DOCX mirror was removed, ignored against reintroduction, and is no longer an acceptance dependency.
---

# Outcome and scope

Custometry now has one synchronized product, UI, architecture, and executable
contract for governed population treatment and segmentation. A user chooses the
population and feature set, applies a versioned treatment policy where needed,
selects rule, bucket, stratified, or exact-K KMeans segmentation, previews the
distribution and sensitivity evidence, and publishes an immutable definition
and membership snapshot. The same treatment and membership identities can be
referenced by analyses, research, reports, email, and XLSX without changing
canonical source data or metric definitions.

The change deliberately does not add a route solely for a control. The 110
canonical route identities remain unchanged. Existing Analytics and Segment
routes receive explicit requirement bindings, while `UI-OVR-025`,
`UI-CAP-018`, and `UI-CAP-019` own the reusable treatment and segmentation
surfaces. `UI-OVR-024` remains the separately documented comments-drawer
backlog found by W03.

W03 is preserved as historical read-only evidence. Its canonical Penpot file
remained at revision 124 with 91 of 91 baseline routes, 23 of 24 then-declared
overlays, and 5 of 5 system surfaces. This W04 contract delta does not claim
that the new surfaces have been drawn in Penpot.

# Documentation authority decision

`docs/architecture/system-design.md` is the only maintained System Design
artifact. The previous DOCX was a generated presentation of the same content
and had no independent runtime, product, delivery, regulatory, or acceptance
consumer. Keeping it introduced avoidable binary review and synchronization
cost. It has therefore been removed from the current architecture contract.
The repository ignore policy prevents regenerated System Design DOCX exports
from accidentally becoming maintained architecture artifacts again.

A PDF or DOCX may still be generated for a named external handoff, but such an
export is ephemeral, non-authoritative, and is not committed or required by a
standard documentation change. Historical W01 and W02 tickets/evidence retain
their DOCX statements because those records describe checks that actually ran
at their own accepted proof boundaries.

# Commands and observations

| Boundary | Result | Observation |
| --- | --- | --- |
| Blueprint parity | pass | 827 synchronized requirement IDs at product specification `0.9.1-draft` |
| Route and UI-surface semantics | pass | 110 routes, 25 overlays, 5 systems, 19 capabilities, 26 use-case bindings |
| Portable JSON schemas | pass | route execution and UI surface manifests validate against Draft 2020-12 schemas |
| Focused tooling tests | pass | 14 passed, 28 deselected |
| Full Python workflow | pass | Ruff and Pyright report no findings; 109 tests pass; strict MkDocs build succeeds |
| Full frontend workflow | pass | lint, typecheck, 12 Vitest tests, and production build succeed across the pnpm workspace |
| Delivery tickets and docs links/indexes | pass | ticket schema, local links, contributor index, and shipped-doc version parity are consistent |
| Grouped local gate | pass | repository-local static checks pass after synchronizing shipped docs and agent templates to `0.9.1-draft` |
| Whitespace and patch integrity | pass | `git diff --check` reports no findings |

# Proof boundary and residual risk

This evidence proves static agreement among the accepted draft blueprints,
architecture projection, route/surface manifests, schemas, documentation
indexes, and delivery records. It does not prove analytical correctness on a
reference dataset, persistence or API behavior, authorization enforcement,
browser interaction, Penpot visual fidelity, email/XLSX output, CPU capacity,
runtime recovery, deployment, performance, or release readiness.

The next Penpot write ticket must consume the W04 delta without rewriting W03.
The first implementation slice must separately prove treatment-boundary
determinism, shared current/LY bounds, fit-versus-assignment semantics, stable
membership identity, policy ceilings, privacy, cancellation, and reference
dataset performance at their real boundaries.

# Verdict

`passed`. The declared static contract boundary is internally consistent, the
duplicate DOCX mirror is retired, and the delta is ready for a separate Penpot
write ticket followed by implementation tickets with real analytical, browser,
runtime, and authorization evidence.
