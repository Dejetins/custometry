---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.2-draft
ticket_id: W07-GOVERNED-DISCOUNT-METHODOLOGY-CONTRACT
proof_boundary: static-discount-methodology-product-ui-architecture-and-executable-contract-synchronization
proof_skills: []
verdict: passed
redaction: No credentials, customer data, Penpot document payloads, browser state, or environment dumps were retained.
executed_checks:
  - uv run python -m tools.custometry_quality.validate_blueprints
  - uv run python -m tools.custometry_quality.generate_requirement_index --check
  - uv run python -m tools.custometry_quality.validate_route_registry
  - uvx check-jsonschema --schemafile packages/contracts/routes/ui-route-contracts.schema.json packages/contracts/routes/ui-route-contracts.json
  - uvx check-jsonschema --schemafile packages/contracts/routes/ui-surface-contracts.schema.json packages/contracts/routes/ui-surface-contracts.json
  - uv run python -m tools.custometry_quality.validate_delivery_tickets
  - uv run python -m tools.custometry_quality.check_docs_links
  - uv run python -m tools.custometry_quality.generate_docs_index --check
  - uv run --locked pytest -q tests/tooling/test_static_quality_tools.py -k 'blueprint or route_registry or delivery_ticket'
  - uv run python -m tools.check --scope local
  - uv run python -m tools.check --scope ci
  - pnpm check
  - git diff --check
observations:
  - Machine and human blueprints contain the same 890 requirement IDs at product version 0.9.2-draft.
  - The executable UI registry contains 110 routes, 25 overlays, 5 system surfaces, 20 cross-surface capabilities, and 27 use-case bindings.
  - W06 is accepted with passed Penpot evidence at canonical revision 164; W07 did not write to Penpot.
  - Static validation proves synchronized documentation and contracts only; runtime calculations, browser interaction, exports, and design implementation remain unverified.
---

# Outcome and scope

Product `0.9.2-draft` and UI `0.6.2-draft` now define one governed model for
receipt-line discount components, policy versioning, stacking and cap rules,
discount attribution quality, exact price-volume-mix reconciliation, metric
certification, and method availability. The machine blueprint, explanatory
mirror, UI workflow, architecture projection, route execution references, and
surface manifest use the same requirement vocabulary and version boundary.

The contract distinguishes promotion, loyalty, bonus redemption, other
discount, commercial discount, customer benefit, and recognized net revenue.
It treats a first-client 50% cap and stacking behavior as a versioned
CompanyPack example rather than a platform default. Historical cap breaches
remain immutable diagnostics, while simulated policy breaches block
publication. Future methodology families are visible as roadmap states but are
not represented as runnable capabilities.

This ticket intentionally changed no application runtime, persistence, API,
worker, database migration, browser UI, Penpot object, email renderer, or XLSX
renderer. W05 and W06 evidence remains historical and unmodified.

# Commands and observations

| Command or evidence | Result | Observation |
| --- | --- | --- |
| Blueprint parity validator | pass | Both product blueprints expose 890 identical requirement IDs at `0.9.2-draft`. |
| Requirement-index check | pass | Generated index contains 890 current requirements. |
| Route registry validator | pass | 110 routes, 25 overlays, 5 systems, 20 capabilities, and 27 use-case bindings. |
| Route-contract JSON Schema | pass | The expanded executable route contract remains schema-valid. |
| Surface-contract JSON Schema | pass | `UI-CAP-020` and `UC-027` coverage remain schema-valid. |
| Delivery-ticket validator | pass | W07 terminal evidence and W08 ready-ticket dependencies are valid. |
| Documentation links and generated index | pass | 42 documents and 91 local links are valid; the 26-document contributor index is current. |
| Focused tooling tests | pass | 14 relevant tests passed; 28 unrelated tests were deselected. |
| Repository local gate | pass | The grouped static repository gate passed after this durable evidence record was added. |
| Repository CI gate | pass | The stronger grouped CI profile passed for the synchronized contract change. |
| `pnpm check` | pass | Lint, typecheck, 12 tests, and production build completed successfully. |
| `git diff --check` | pass | No whitespace errors were found. |

# Verdict

`passed`. W07 provides the accepted static contract required by the next
Penpot write-ticket. Its proof boundary does not establish calculation
correctness, runtime behavior, browser accessibility, rendered exports,
performance, or release readiness. W08 must independently verify the exact
canonical Penpot file, revision `164`, repository fingerprint, affected-frame
visuals, and final stable-ID inventory before it may record a terminal verdict.
