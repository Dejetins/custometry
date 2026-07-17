---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.8.2-draft
ticket_id: W00-RESET-DELIVERY-MODEL
status: accepted
workstream_id: W00
summary: Remove the obsolete staged planning system and partial B01 work, leaving the accepted Foundation and a minimal ticket-first delivery adapter.
requirement_ids: [DOC-RULE-008]
blockers: []
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - docs/adr/0003-agent-delivery-model.md
  - docs/architecture/development-operating-model.md
  - docs/architecture/repository-layout.md
change_scope:
  allowed_write_paths:
    - AGENTS.md
    - CONTRIBUTING.md
    - README.md
    - SECURITY.md
    - pyproject.toml
    - .codex/**
    - docs/**
    - docs-site/docs/index.md
    - docs-site/docs/ru/index.md
    - tools/custometry_quality/**
    - tests/tooling/**
  forbidden_write_paths:
    - custometry-technical-blueprint-ru.md
    - custometry-technical-blueprint-human-ru.md
    - custometry-ui-blueprint-ru.md
    - apps/**
    - packages/**
    - plugins/**
    - deploy/**
    - migrations/**
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: tests
  proof_skills: []
  commands:
    - uv run pytest -q tests/tooling
    - uv run ruff check tools/custometry_quality tests/tooling
    - uv run python -m tools.custometry_quality.validate_delivery_contract
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - uv run python -m tools.custometry_quality.validate_agent_profiles
    - uv run python -m tools.custometry_quality.generate_docs_index --check
    - uv run python -m tools.custometry_quality.check_docs_links
    - uv run --locked python -m tools.check --scope local
  proof_boundary: repository-delivery-model-static
  evidence_target: .codex/delivery/evidence/W00-RESET-DELIVERY-MODEL.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: [.codex/delivery/evidence/W00-RESET-DELIVERY-MODEL.md]
---

# Outcome

The repository contains the accepted Foundation runtime and product/UI sources,
plus a minimal Global Delivery Contract v1 adapter. The standing program plan,
generated prompt packs, workstream plans, stage ledgers, old validators/tests,
and unaccepted B01 implementation are absent from the active tree.

# Non-goals

- Do not change normative platform or UI requirements.
- Do not implement a product feature or create a replacement master backlog.
- Do not claim browser, Compose, recovery, performance, supply-chain, release,
  or deployment readiness from this static migration.

# Work and repair boundary

Reset the unpublished local planning commit and dirty B01 work to the published
Foundation baseline. Preserve the new global delivery adapter, specification,
ticket and evidence templates, focused validators, and accepted architecture.
Remove stale references and generated indexes so the remaining tree is
self-consistent. Compatible repairs within the declared governance/tooling
scope are allowed and invalidate the affected static checks.

# Acceptance evidence

- Inventory and text searches find no active old-format plan, generated pack,
  stage ledger, program-matrix generator, or partial B01 implementation.
- Delivery adapter, ticket, profile, documentation, layout, and link validators
  pass with focused tooling tests and Ruff.
- The grouped local profile passes on the cleaned tree.
- Compact redacted evidence is stored at the declared target before the ticket
  becomes `accepted`.
