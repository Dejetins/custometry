---
artifact_kind: workstream_plan
staged_schema_version: 1
workstream_id: B12
plan_maturity: initial
program_plan: docs/architecture/program/custometry-program-plan.md
module_definition: docs/architecture/workstreams/b12-production-hardening-module.md
plan_doc: docs/architecture/workstreams/b12-production-hardening-plan.md
prompt_pack_dir: .codex/agents/generated/b12-production-hardening
stage_ledger: docs/architecture/workstreams/b12-production-hardening-stage-reports/b12-production-hardening-stage-ledger.md
execution_mode: manual_sequential
hard_dependencies: [B01, B02, B03, B04, B05, B06, B07, B08, B09, B10]
soft_dependencies: [B11]
stage_ids: [S00, S01, S02, S03, S04, S05, S06]
release_milestones: [public_mvp, v1_feature_freeze, v1_target]
spec_version: 0.8.2-draft
requirement_ids: [AC-014, AC-015, AC-034, ADMIN-002, ADMIN-004, ADMIN-006, ADMIN-007, ADMIN-010, ADMIN-011, CHART-019, GAP-017, GAP-018, GAP-019, OPS-001, OPS-002, OPS-003, OPS-004, OPS-005, OPS-006, OPS-007, OPS-008, RISK-008, SCALE-001, SCALE-002, SCALE-003, SCALE-004, SEC-001, SEC-002, SEC-003, SEC-004, SEC-005, SEC-006, SEC-007, SEC-008, SEC-009, SEC-010, SEC-011, SEC-012, SEC-013, SEC-014, SEC-015, SEC-016, SEC-017, SEC-018, TEST-INV-025, TEST-INV-046, TEST-INV-052, V1-AC-013, V1-AC-019]
---

# B12 Production Hardening — Initial Plan

## Objective and milestone gates

Consolidate security, deployment, upgrade/recovery, supply-chain, performance,
capacity, observability, admin lifecycle, and target firewall/CNI evidence.

The public-MVP checkpoint is B12 S05 and hard-depends on B01–B10 only. B11 is
soft so post-MVP operational email/webhook cannot block public MVP. B12 S06
final v1 hardening is explicitly gated by accepted B11 and re-proves the
plugin/channel attack surface before B13/W14.

## Dependencies and activation

Hard dependencies are B01 through B10. B11 is soft at activation and public-MVP
S05, then mandatory for S06. The dormant ledger requires explicit user
authority and exact registry links.

## Requirement groups

| Group | IDs | Planned evidence |
|---|---|---|
| Security | `SEC-001`–`018`, `TEST-INV-046`, `V1-AC-013` | threat/contract tests, browser/API/database/runtime penetration evidence |
| Deployment/network/admin | `AC-034`, `ADMIN-002`, `004`, `006`, `007`, `010`, `011`, `OPS-001`–`008`, `TEST-INV-052` | Compose/host, Edge-Web-API, firewall/CNI, lifecycle, observability, system surfaces |
| Recovery/supply chain/performance | `AC-014`, `AC-015`, `GAP-017`–`019`, `SCALE-001`–`004`, `TEST-INV-025`, `V1-AC-019` | install/upgrade/restore drills, SBOM/licenses/provenance, benchmarks/capacity |
| Additional hardening risks | remaining routed IDs | chart resource limits, audit, retention, rollout, residual-risk evidence |

The plan intentionally includes security requirements owned by earlier feature
workstreams as contributor inputs. Their baseline implementation cannot be
deferred to B12; B12 consolidates and re-proves the cross-cutting production
profile at its milestone gates.

## Stage outline

| Stage | Planned outcome | Exit boundary |
|---|---|---|
| `S00` | Inventory target topology, threat model, secrets, recovery, supply chain, performance, operations, and all evidence gaps. | Source-anchored hardening backlog |
| `S01` | Freeze security/ops/deploy/recovery/performance contracts, target profiles, runbooks, and acceptance receipts. | Versioned hardening contract |
| `S02` | Implement policy cores and validators for security, retention, limits, compatibility, evidence, and release gates. | Policy/unit evidence |
| `S03` | Implement deployment, secrets, observability, backup/restore, upgrade, supply-chain, and benchmark adapters. | Real adapter/integration evidence |
| `S04` | Integrate admin/system surfaces and browser security/accessibility behavior. | Browser/security evidence |
| `S05` | Prove B01–B10 public-MVP install, upgrade, recovery, security, supply-chain, performance, and target ingress/egress baseline. | Public-MVP terminal checkpoint |
| `S06` | Require accepted B11; re-run affected hardening, reconcile v1/feature-freeze, cold review, and final B12 acceptance. | v1 hardening acceptance |

## Contracts, rollout, and rollback

Every target profile freezes images, digests, network policy, secrets,
resources, storage, migrations, backup format, retention, observability, and
supported platforms. Evidence is invalidated by relevant code/config/image/
target changes. Upgrade and rollback define compatibility windows, health
gates, stop triggers, unknown-state reconciliation, and data-preserving
recovery.

## Validation and proof

Required evidence includes clean install, upgrade, backup/restore, corruption
and disaster drills, workspace/PII isolation, auth/session/CSRF/browser storage,
Edge-to-Web/Web-to-API topology, production firewall/CNI equivalent, SSRF/
egress, least privilege, SBOM/license/provenance/vulnerability, benchmark/
soak/capacity, admin/system browser flows, and cold independent review.

## Completion rule

S05 may close public MVP only with B01–B10 and all public-MVP hardening evidence.
S06 cannot accept without B11 and affected channel/plugin re-proof. B12 is
complete only with terminal stages, complete traceability, current evidence,
documented residual risks, and no unresolved critical/high blocker.
