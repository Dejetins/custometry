---
doc_id: ARCH-DEVELOPMENT-OPERATING-MODEL-001
title: Custometry development operating model
doc_version: 2
product_spec_version: 0.8.2-draft
visibility: internal
ship: false
owner: engineering
requirement_ids: [DOC-RULE-008]
status: accepted
proof_boundary:
  label: repository-development-policy
  exclusions: [github-protection-proof, ci-run-proof, staged-plan-authorization]
---

# Custometry Development and Acceptance Model

## 1. Development principle

Custometry evolves through contract-backed vertical slices. First, the project establishes a visible and navigationally coherent Web experience. Each bounded context then replaces its generated mock with real application, domain, and adapter implementations without changing the accepted contract, or through an explicit versioned migration.

Two extremes are prohibited:

- dozens of disconnected screens backed by manually invented mock shapes;
- a backend-first layer with no accepted user journey or browser acceptance.

The definition of progress is one user journey that reaches from its route and UI states to a real API, persistence, or artifact boundary, including failure, recovery, and documentation.

## 2. High-level workstreams

| No. | Workstream | Verifiable result |
|---|---|---|
| 0 | Repository Foundation | Reproducible toolchain, governance, CI, contracts, doctor, and compact installation scaffolding |
| 1 | Experience Platform | Frost design system, shell, route registry, generated mocks, system states, i18n/a11y, `/docs`, and `/help` |
| 2 | Local Data Lab | Control PostgreSQL, demo-source PostgreSQL, migrations, and deterministic retail fixtures |
| 3 | Identity and Control Plane | Real workspaces, sessions, RBAC, actor context, and audit |
| 4 | Execution and Artifact Spine | Runs, outbox, leases, fencing, reconciler, and immutable artifact commit |
| 5 | Data Foundation | Connections, catalog, ingestion, semantic model, and data quality |
| 6 | Analytics Vertical Alpha | First real reportable slice: typed filters, vs LY, ChartSpec/ECharts, Trust, and Focus |
| 7 | Operations | Runs/schedules/operator center/in-app notifications |
| 8 | Customer Intelligence | Customers, cohorts, lifecycle, segments, and Promotion Journal |
| 9 | Forecasting | Forecast specifications, rolling backtests, registry, predictions, and monitoring |
| 10 | Reporting and Knowledge | Dashboards, ReportSnapshot composition, Data Guides, and user email |
| 11 | Pipelines and Extensibility | Common-engine canvas, plugin contracts, and administrator lifecycle |
| 12 | Hardening | Security, upgrade, recovery, SBOM/license/provenance, performance, and target-specific Edge firewall/CNI enforcement |
| 13 | Universal XLSX | Final functional slice built on a stable ReportSnapshot |
| 14 | Final Acceptance | Release evidence without adding feature scope |

This order is an architectural dependency sequence. A detailed plan, iteration journal, and prompt pack are created only after the specific workstream is approved separately.

## 3. Common S00–S06 framework

| Stage | Entry | Required questions | Exit/evidence |
|---|---|---|---|
| S00 Discovery | Workstream scope accepted | current facts, users, non-goals, vocabulary, owners, dependencies, risk and failure cost | source-anchored scope and no unresolved ownership blocker |
| S01 UX + Contract | S00 accepted | routes/states, Penpot, commands/queries/events, OpenAPI/DTO/errors, examples, permissions | versioned schemas/examples, contract impact, browser scenario |
| S02 Domain/Application | S01 contract frozen | aggregates, invariants, policies, ports, idempotency, cancellation | framework-free core, focused unit/property/contract evidence |
| S03 Adapters | Core ports exist | PostgreSQL/artifacts/queue/source, migrations, timeout/retry/unknown state | real adapter evidence and clean migration path |
| S04 Web Integration | Real boundary usable | generated client, mock/real parity, loading/empty/degraded/forbidden/failed, en/ru/a11y | real browser flow without contract divergence |
| S05 Real-boundary Proof | Integrated slice | clean install/DB, Compose, restart, retry, cancellation, recovery, telemetry | reproducible nearest-boundary evidence and residual risks |
| S06 Acceptance | All previous exits observed | docs/runbook, requirement traceability, rollback, security/performance if triggered, cold review | no blocker; accepted artifact/evidence inventory |

Stage names standardize criteria but do not automatically create staged artifacts. When execution becomes staged, exactly `plan_doc + prompt_pack_dir + stage_ledger` applies, and reports are stored alongside the ledger.

## 4. Git workflow

- `main` is protected and always potentially releasable.
- Product changes use a short-lived `codex/<workstream>-<iteration>` branch and a mandatory pull request.
- `develop`, per-stage branches, and long-lived context branches are not used.
- Merge strategy is squash with linear history; the branch is deleted after merge.
- Required checks match the affected boundaries; bypass and force-push are prohibited.
- An agent does not create a branch merely because this policy exists: the current user request or an accepted workstream must explicitly authorize implementation and branch creation. A read-only review creates no branch.
- The public repository accepts no secret material, PII, raw external payloads, or private environment topology, even on a remote branch.

The minimum GitHub configuration for `main` requires pull requests, required status checks, resolved conversations, and linear history, and blocks force pushes and deletion. The required reviewer count and CODEOWNERS are added once stable owners exist.

## 5. CI contract

### Pull request

1. Blueprint/human mirror version, links, and requirement-index synchronization.
2. Repository layout, agent profiles, and staged-work artifact schema.
3. Locked `uv`/`pnpm` install; no uncommitted generated drift.
4. Backend format/lint/types/unit.
5. Frontend lint/types/unit/component.
6. PostgreSQL migration from empty + integration tests.
7. Contract drift: OpenAPI/JSON Schema/generated TypeScript client/mock examples.
8. Canonical OCI build and manifest/digest/platform validation.
9. Disposable Compose lifecycle.
10. Browser smoke for the shell, docs/help, and the changed vertical slice.

Heavy release matrices are not repeated on every pull request without need. Contract tests and the static evidence schema remain mandatory, however; the fail-closed release gate requires the real matrix.

### Main

- Repeat required checks against the merge SHA.
- Publish an immutable OCI artifact tied to the commit SHA and record its actual digest.
- Generate SBOM, provenance, and license evidence.
- Do not report success if publication was skipped or the manifest is missing.
- Downstream receives the digest from publication output rather than constructing a tag by assumption.

### Release/deploy

- Deployment is manual/protected and uses the digest.
- The first mandatory target is the local M3 Pro; subsequent platform targets are added through a separate verifiable matrix.
- Release verifies image existence and platform, migration, a clean Compose lifecycle, browser behavior, egress, recovery, license/SBOM, and performance thresholds. A production target additionally proves a firewall/CNI-equivalent policy: Edge accepts only approved ingress, reaches only Web, and cannot reach API, control, data, Internet, private, link-local, or metadata ranges.
- Automatic blind upgrade of a local installation is prohibited; update preflight presents compatibility, backup, and rollback.

## 6. Hook profiles

Canonical orchestrator:

```bash
uv run python -m tools.check --scope pre-commit
uv run python -m tools.check --scope local
uv run python -m tools.check --scope pre-push
uv run python -m tools.check --scope ci
uv run python -m tools.check --scope release
```

- `pre-commit` includes all 12 deterministic source checks: blueprints, generated indexes, links, layout, staged artifacts, profiles, DDD, contracts, routes, i18n, and fixtures.
- `local` is pre-commit plus `doctor --mode static`; it is the normal handoff profile.
- `pre-push` is local plus migration, Compose, and browser static contracts.
- `ci` has exact parity with pre-push and does not depend on a local hook.
- `release` is CI plus mandatory runtime, recovery, supply-chain, and performance observations; missing environment or evidence is a failure, not a skipped success.

The exact composition and change triggers are defined in [tooling-gates.md](./tooling-gates.md) and `.codex/AGENTS.md`. Git hooks may invoke `local`, but the Python tools remain the canonical logic so local hooks and CI do not diverge.

## 7. Acceptance and proof boundary

| Change surface | Insufficient evidence by itself | Nearest mandatory evidence |
|---|---|---|
| Domain function | docs/typing | focused unit/property/invariant tests |
| Port/adapter | fake/mock | contract test + real adapter boundary |
| API | generated OpenAPI | real request, auth/RBAC/error/DTO behavior |
| PostgreSQL | migration file review | empty upgrade, repeat/idempotence policy, supported downgrade/rollback |
| Web | screenshot/Penpot | browser flow, console/network, responsive/a11y/en/ru |
| Compose | `docker compose config` | clean pull/start/health/stop/restart with post-conditions |
| Image | build exit code | manifest, digest, platforms and runtime import/start |
| Recovery | runbook | observed drill and integrity checks |
| Performance | intuition/unit timing | comparable baseline/corpus/environment and threshold |
| Release | green unit tests | owned diff, CI, artifact provenance, install/update and post-start smoke |

## 8. Definition document for a future workstream

Before a detailed plan is created, the workstream definition is completed using [module-definition-template.md](../contracts/module-definition-template.md). It must include purpose and non-goals, vocabulary, aggregates, entities, value objects, lifecycle, commands, queries, events, schemas, data ownership, ports and adapters, permissions, idempotency, retry and unknown-state behavior, UI/help, observability, fixtures, acceptance, migration, and rollback.

Requirement terminal ranges are not copied manually. The document refers to stable IDs from the generated requirement index so adding a new ID does not silently make a role or template obsolete.
