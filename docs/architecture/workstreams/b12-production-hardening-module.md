---
artifact_kind: module_definition
staged_schema_version: 1
doc_id: MODULE-B12-PRODUCTION-HARDENING
title: B12 Production Hardening module definition
doc_version: 1
product_spec_version: 0.8.2-draft
visibility: internal
ship: false
workstream_id: B12
owner: security-operations
status: initial
requirement_ids: [AC-014, AC-015, AC-034, ADMIN-002, ADMIN-004, ADMIN-006, ADMIN-007, ADMIN-010, ADMIN-011, CHART-019, GAP-017, GAP-018, GAP-019, OPS-001, OPS-002, OPS-003, OPS-004, OPS-005, OPS-006, OPS-007, OPS-008, SCALE-001, SCALE-002, SCALE-003, SCALE-004, SEC-001, SEC-009, SEC-018, TEST-INV-025, TEST-INV-046, TEST-INV-052, V1-AC-013, V1-AC-019]
proof_boundary:
  label: planned-b12-module-boundary
  exclusions: [feature-implementation-ownership, public-mvp-before-s05-proof, b11-operational-channel-implementation, production-promotion-without-firewall-cni, release-readiness]
---

# B12 Production Hardening — module definition

## Purpose and staged milestone boundary

B12 consolidates the product's production security, operations, recovery,
supply-chain, performance, and deployment evidence.

Its dependency rule is intentionally asymmetric:

- hard dependencies are B01–B10;
- B11 is soft for the public-MVP checkpoint;
- `public_mvp` closes at B12 S05 without activating B11 operational
  email/webhook;
- B12 S06 final v1 hardening is gated by B11 completion and must re-evaluate
  the new plugin/channel attack surface.

B12 owns proof and hardening, not product feature semantics.

## Ubiquitous language

| Term | Meaning |
|---|---|
| Production hardening profile | Versioned target-host security/ops configuration and proof obligations |
| Trust boundary | Explicit process/network/data authority boundary |
| Release candidate | Immutable code/image/config set under acceptance |
| Recovery point/objective | Measured restore data loss/time contract |
| Supply-chain receipt | SBOM, provenance, digest, license, and vulnerability evidence |
| Firewall/CNI-equivalent evidence | Target enforcement proving required ingress/egress policy |
| Edge adapter | Infrastructure ingress proxy, not a business microservice |
| Performance baseline | Comparable measured latency/throughput/RSS/disk result |
| Upgrade rehearsal | Supported-version migration and rollback/recovery proof |

## Security and operations invariants

- Secrets never enter images, Git, browser bundles, logs, traces, evidence, or
  public docs.
- Edge is an infrastructure adapter. Compose provides portable topology but not
  portable ingress-only enforcement; production promotion requires separate
  firewall/CNI-equivalent evidence.
- `edge_to_web` and `web_to_api` are separate; Edge has no direct API
  adjacency.
- Remote workers are rejected until a future distributed-topology ADR.
- Backups cover PostgreSQL and artifacts consistently and are restored in an
  isolated test environment.
- Upgrades use explicit compatibility windows, migration order, health gates,
  rollback triggers, and unknown-state reconciliation.
- Resource concurrency accounts for memory, workspace quotas, queues, temp
  disk, and CPU; not CPU alone.
- All collections, retries, logs, traces, metrics, and retention are bounded.
- SBOM, licenses, image digests, provenance, dependency vulnerabilities, and
  supported platform matrices are release evidence.
- Production admin lifecycle, service health, workers/queues, storage,
  backup/restore, audit, and limits expose safe state without secrets.

## Hardening surfaces

B12 coordinates:

- authentication/session/token/CSRF/security headers and browser storage;
- authorization/workspace isolation/PII/export enforcement;
- network topology, TLS termination assumptions, firewall/CNI, SSRF, egress,
  database exposure, and secrets;
- image/runtime least privilege, read-only filesystems, capabilities, users,
  temp storage, resource limits, and logging;
- PostgreSQL/artifact backup, restore, corruption, retention, and recovery;
- migration/upgrade/downgrade/reconciliation;
- observability, alerts, audit, runbooks, maintenance, and admin lifecycle;
- SBOM/license/provenance/vulnerability gates;
- performance/soak/capacity/resource and chart-renderer evidence;
- installation, upgrade, maintenance, and disaster-recovery documentation.

## Ports and dependencies

B12 consumes stable release slices and evidence from B01–B10. B11 remains a
soft dependency through public MVP, then becomes an explicit S06 entry gate for
final v1 hardening. B12 supplies hardening receipts and residual-risk decisions
to B13/W14.

No product context may import B12 as a domain dependency. Hardening adapters,
policies, deploy manifests, gates, and runbooks wrap or configure composition
roots.

## Evidence model

Every receipt records immutable source/image/config identity, target host,
commands/method, timestamps, result, logs/redaction, cleanup, proof boundary,
and residual risk. Evidence expires when relevant code, image, config, target,
secret policy, migration, or dependency changes.

Tests are not substitutes for target firewall, recovery, supply-chain,
performance, browser security, or upgrade proof.

## Contract impact and acceptance

Security defaults, network policy, secrets, backup formats, restore procedure,
retention, migration ordering, image identity, supported platforms, resource
limits, audit fields, and operational endpoints are contract dimensions.
Breaking changes require migration, rollout, rollback, and operator guidance.

B12 completes public MVP only at accepted S05 with B01–B10 evidence and the
minimum hardening profile. S06 cannot close final v1 hardening until B11 is
accepted and its plugin/email/webhook effects are re-proven. Final acceptance
requires independent cold review and no unresolved critical/high blocker.
