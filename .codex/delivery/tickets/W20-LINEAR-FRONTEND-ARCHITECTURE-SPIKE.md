---
artifact_kind: delivery_ticket
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.4-draft
ticket_id: W20-LINEAR-FRONTEND-ARCHITECTURE-SPIKE
status: ready
workstream_id: W20
summary: Prove the React, MobX, TanStack Query, styled-components, semantic-token, typed REST/SSE, reversible route-boundary, and performance-harness architecture before committing the full Custometry application shell.
requirement_ids: [WEB-ARCH-001, WEB-ARCH-002, WEB-ARCH-003, WEB-ARCH-004, WEB-ARCH-006, WEB-PERF-001, WEB-PERF-002, WEB-PERF-003, WEB-PERF-004, WEB-PERF-005, WEB-PERF-006, THEME-001, THEME-005]
blockers: [W19-LINEAR-REFERENCE-COMPLETION]
context_sources:
  - AGENTS.md
  - .codex/AGENTS.md
  - .codex/delivery/specs/custometry-linear-workspace-ui-transition.md
  - .codex/delivery/tickets/W19-LINEAR-REFERENCE-COMPLETION.md
  - docs/architecture/system-design.md
  - docs/architecture/ui/linear-workspace-ui-transition-standard-v1.md
  - docs/architecture/ui/linear-workspace-reference-manifest-v1.json
  - package.json
  - apps/web/package.json
  - apps/web/src/App.tsx
  - packages/contracts/routes/ui-route-contracts.json
change_scope:
  allowed_write_paths:
    - .codex/delivery/tickets/W20-LINEAR-FRONTEND-ARCHITECTURE-SPIKE.md
    - .codex/delivery/evidence/W20-LINEAR-FRONTEND-ARCHITECTURE-SPIKE.md
    - apps/web/**
    - packages/ui-foundation/**
    - package.json
    - pnpm-lock.yaml
    - tests/e2e/linear-architecture-spike.spec.ts
    - tests/performance/**
  forbidden_write_paths:
    - custometry-technical-blueprint-ru.md
    - custometry-technical-blueprint-human-ru.md
    - custometry-ui-blueprint-ru.md
    - docs/**
    - packages/contracts/**
    - apps/api/**
    - apps/worker_data/**
    - migrations/**
    - deploy/**
    - .codex/delivery/graphs/**
  mixed_file_policy: stop_if_safe_hunk_separation_is_impossible
repair_policy:
  allowed_within_scope: true
  retest_invalidated_evidence: true
validation:
  depth: browser
  proof_skills: [browser-qa-evidence, backend-performance-evidence, playwright]
  commands:
    - source scripts/activate-toolchain.sh
    - pnpm --filter @custometry/web lint
    - pnpm --filter @custometry/web typecheck
    - pnpm --filter @custometry/web test
    - pnpm --filter @custometry/web build
    - run the ticket-owned browser spike for reversible mounting, MobX local state, Query server state, REST cancellation, SSE update, theme switch, panel resize, and rollback
    - run the ticket-owned repeatable benchmark harness and report declared hardware plus p50 p75 p95 for client dispatch response-to-paint SSE-to-paint INP and long tasks
    - uv run python -m tools.custometry_quality.validate_delivery_tickets
    - git diff --check
  proof_boundary: browser-proven-custometry-frontend-architecture-and-local-performance-spike
  evidence_target: .codex/delivery/evidence/W20-LINEAR-FRONTEND-ARCHITECTURE-SPIKE.md
escalation_triggers: [normative_product_change, material_user_scope_change, external_or_irreversible_side_effect, secrets_or_production_authority, write_outside_allowed_scope]
evidence: []
---

# Outcome

A minimal browser slice proves the accepted frontend dependency direction,
state ownership, four-theme token boundary, reversible route cutover, REST/SSE
adapter behavior, and measurement method before the full shell is built.

# Non-goals

- Do not implement production route clusters, analytics semantics, Penpot, or
  backend changes.
- Do not treat mock-server timings as real API latency or release evidence.

# Work and repair boundary

Build only enough typed and tested infrastructure to falsify the architecture.
Keep the legacy shell callable as a real rollback path. Measure client overhead
separately from deterministic mock latency and document dependency/bundle costs.

# Acceptance evidence

The evidence records dependency versions, state-boundary tests, route fallback,
four-theme switching, keyboard resize, traces, benchmark method and results,
and an explicit proceed/change/stop decision for W21 and W22.
