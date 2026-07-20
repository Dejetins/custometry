---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.3-draft
ticket_id: W11-HYBRID-DEVELOPMENT-RUNTIME
status: accepted
workstream_id: W11
summary: Implement and prove the canonical Hybrid development runtime so host Web and API processes can use isolated loopback-only control and demo PostgreSQL infrastructure without rebuilding the full application stack on every edit.
requirement_ids: [ARCH-PRINCIPLE-001, DOC-RULE-008]
blockers: []
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - docs/architecture/development-operating-model.md
  - docs/architecture/development-runtime-contract.md
  - docs/architecture/runtime-network-installation.md
  - docs/architecture/repository-layout.md
  - docs/architecture/tooling-gates.md
  - compose.yaml
  - deploy/compose/bootstrap.sh
  - deploy/compose/compose.release.yaml
  - deploy/compose/ownership-manifest.json
  - deploy/compose/ci-smoke.sh
start_probe:
  boundary: local Docker engine and Docker Compose v2 used by the disposable Hybrid runtime
  read_only_check: docker context show && docker compose version && docker info
  stop_on: [unavailable, multiple_active_engines, incompatible_compose]
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W11-HYBRID-DEVELOPMENT-RUNTIME.md
    - .codex/delivery/evidence/W11-HYBRID-DEVELOPMENT-RUNTIME.md
    - .codex/delivery/graphs/custometry-runtime-data-stream-v1.json
    - scripts/dev
    - compose.dev.yaml
    - deploy/compose/development-runtime-policy.json
    - tools/custometry_quality/check.py
    - tools/custometry_quality/development_runtime.py
    - tests/tooling/__init__.py
    - tests/tooling/test_development_runtime.py
    - tests/integration/__init__.py
    - tests/integration/test_development_runtime.py
    - docs/architecture/development-runtime-contract.md
    - docs/architecture/runtime-network-installation.md
    - docs/architecture/tooling-gates.md
    - docs/README.md
    - docs/runbooks/development-runtime.md
  forbidden_write_paths:
    - custometry-technical-blueprint-ru.md
    - custometry-technical-blueprint-human-ru.md
    - custometry-ui-blueprint-ru.md
    - packages/contracts/routes/**
    - packages/localization/**
    - packages/identity_access/**
    - packages/connection_catalog/**
    - packages/ingestion/**
    - packages/data_quality/**
    - packages/semantic_model/**
    - packages/analytics_core/**
    - packages/analytics_customer/**
    - packages/analytics_sales/**
    - apps/web/src/**
    - apps/api/src/**
    - migrations/**
    - .codex/delivery/tickets/W10-PENPOT-093-ORGANIZATION-PEOPLE-DELTA-IMPLEMENTATION.md
    - .codex/delivery/evidence/W10-PENPOT-093-ORGANIZATION-PEOPLE-DELTA-IMPLEMENTATION.md
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: runtime
  proof_skills: []
  commands:
    - source scripts/activate-toolchain.sh
    - bash -n scripts/dev
    - docker compose -f compose.yaml -f compose.dev.yaml config
    - uv run --locked pytest -q tests/tooling/test_development_runtime.py tests/integration/test_development_runtime.py
    - start a fresh repository-owned Hybrid runtime through scripts/dev and observe loopback-only control and demo PostgreSQL readiness
    - observe host API and Web process ownership status and confirm repeated up is idempotent
    - observe bounded redacted logs and healthy/degraded/unavailable status behavior
    - prove reset-demo rejects a missing or incorrect confirmation and cannot select the control database or a foreign volume
    - prove compose.dev.yaml cannot enter the release composition or release validation path
    - stop the owned Hybrid runtime and verify no owned processes containers networks or temporary secret files remain while persistent data follows the declared policy
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - uv run python -m tools.check --scope local
    - git diff --check
  proof_boundary: local-hybrid-development-runtime-lifecycle-and-release-isolation
  evidence_target: .codex/delivery/evidence/W11-HYBRID-DEVELOPMENT-RUNTIME.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: [.codex/delivery/evidence/W11-HYBRID-DEVELOPMENT-RUNTIME.md]
---

# Outcome

Contributors have one deterministic `scripts/dev` entry point for Hybrid
development. It starts and reports repository-owned loopback infrastructure,
host Web/API processes, migrations, URLs, mode, and mock/real state without
rebuilding the full-stack images on every edit. `down`, `status`, bounded
`logs`, and confirmation-gated demo reset are idempotent and ownership-safe.

# Non-goals

- Do not implement product authentication, organization, ingestion, analytics,
  or new Web visuals.
- Do not modify the canonical Full Stack or release trust boundaries, publish
  an image, or claim production firewall/CNI evidence.
- Do not persist credentials in the repository, process arguments, logs, or
  committed runtime state.

# Work and repair boundary

Implement only the development orchestration and validation paths declared in
scope. The development override may publish required infrastructure ports only
on `127.0.0.1`, uses a distinct Compose project and volumes, and must be
rejected by release validation. Existing direct focused commands and the
canonical full-stack bootstrap remain valid.

# Acceptance evidence

Terminal evidence must observe the real Docker/host lifecycle, not only parse
the YAML or scripts. It records the selected Docker context, redacted owned
resource identities, actual loopback bindings, migration/readiness results,
idempotent repeat behavior, safe reset rejection and success, release-exclusion
proof, cleanup postconditions, focused tests, and static repository gates.
