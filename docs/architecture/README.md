---
doc_id: ARCH-INDEX
title: Custometry Architecture
doc_version: 19
product_spec_version: 0.10.0-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: []
status: active
proof_boundary:
  label: contributor-architecture-index
  exclusions: [runtime-readiness, release-readiness]
---

# Custometry Architecture

This directory contains accepted architecture decisions and shared engineering contracts. It does not replace the normative [machine blueprint](../../custometry-technical-blueprint-ru.md) and is not a journal of the current execution stage.

## Sources of truth

1. `custometry-technical-blueprint-ru.md` contains the normative product requirements, version `0.10.0-draft`.
2. `custometry-technical-blueprint-human-ru.md` is the synchronized human-readable mirror.
3. `custometry-ui-blueprint-ru.md` preserves UI/UX requirements and current inventory. The final interactive target pilot owns its demonstrated composition, behavior, and visual language; ADR-0007 owns frontend architecture.
4. Documents in this directory contain accepted architecture and process decisions within the blueprint.
5. Global Delivery Contract v1 and the owner-adopted [planning framework](planning/framework-v1/README.md) define hierarchical planning and milestone pack execution. Each milestone has one canonical iteration journal; independent tickets retain ticket state. Parent/child, dependency and execution-artifact links and affected documentation must be synchronized by agents without owner reminders. Goal mode requires explicit authority.

If sources conflict, the higher-precedence source applies. An architecture document does not introduce a new normative `MUST`: a new product obligation is first added to the machine blueprint and mirrored synchronously in the human-readable version.

## Document map

| Document | Purpose |
|---|---|
| [System Design](./system-design.md) | Complete `0.10.0-draft` target architecture, accepted decisions, flows, trust boundaries, compatibility, proof limits, and direction of evolution |
| [Bounded context map](./bounded-context-map.md) | Context ownership, public ports, dependency direction, consistency, and cross-context integration policy |
| [Governed population and analytical authoring](../contracts/analytical-authoring-contract.md) | Accepted customer segmentation/reporting requirements, target contract ownership, compatibility and implementing-ticket acceptance |
| [Source data adaptation and imperfect snapshot refresh](../contracts/source-data-adaptation-contract.md) | Accepted source readiness, daily rebuilds, degraded-input handling, typed mapping and derived-channel requirements |
| [Report refresh, prepared serving and recovery](../contracts/report-refresh-serving-recovery-contract.md) | Accepted version 1: document schedules/status, immutable current snapshots, artifact commit, mixed 50-author/100-viewer workload and coherent off-primary backup; numeric latency/recovery objectives remain unproven |
| [Artifact format registry](../contracts/artifact-format-contract.md) | Required output vocabulary, manifest meaning, reader compatibility and rollback |
| [Audit contract proposals](./planning/audit-contract-decisions-2026-09-06.md) | Proposed PVM, shared cancellation, endpoint-revocation and TLS contracts; no runtime acceptance |
| [Documentation audit reconciliation](./planning/documentation-audit-reconciliation-2026-09-06.md) | Accepted correction scope, finding disposition, compatibility and observed documentation evidence |
| [Executable UI route contract](../contracts/ui-route-contract.md) | Identity/execution manifest split, guard/permission/state/history semantics, agent resolution, and validation rules |
| [UI surface coverage contract](../contracts/ui-surface-contract.md) | Requirement-to-surface coverage, route decision policy, historical design provenance, and complete agent load order |
| [UI delivery governance ADR](../adr/0004-ui-delivery-governance.md) | Superseded historical decision; the owner retired and removed the G-program |
| [Collaboration, digital measurement, and compute reuse ADR](../adr/0005-collaboration-measurement-and-compute-reuse.md) | Audits comparable products and accepts the new collaboration/adoption, retail digital-measurement, and materialization/reuse boundaries |
| [Analytical documents, segments, and product analytics ADR](../adr/0006-analytical-document-retail-product-and-time-aware-segmentation.md) | Accepts one analytical-document composition/snapshot path, time-aware segment identity, retail product/category/inventory boundaries, compatibility, and migration direction |
| [Responsive Web frontend platform ADR](../adr/0007-responsive-web-frontend-platform.md) | Selects the version-pinned browser platform and fixes dependency direction, state/adapter/design-system ownership, responsive anchors, rollout, rollback, and later proof boundaries |
| [Comparable analytics platform capability audit](./ui/comparable-analytics-platform-capability-audit-v1.md) | Official-documentation audit of established multi-page authoring, collaboration, segments, digital/product analysis, adoption, and compute-reuse patterns plus Custometry's accepted response and deliberate non-copy boundary |
| [Target UI concept](./ui/target-pilot/README.md) | Preserved interactive pilot, byte-pinned resources, demonstrated composition and interactions, and proof limits |
| [UI program retirement](./ui/ui-program-retirement.md) | Removed materials, preserved requirements/code, historical recovery, and cleanup evidence |
| [Web implementation source contract](./ui/custometry-web-implementation-source-contract-v1.md) | Selected ticket or milestone-stage execution from the target pilot and product requirements, source precedence, and browser proof boundary |
| [Hierarchical planning framework](planning/framework-v1/README.md) | Required per-level templates, versions, owner checkpoints, mandatory document synchronization and milestone plan/pack/journal bindings |
| [Development direction map — MAP-001](planning/project-map.md) | Accepted version 1.0.0: six L1 directions, requirement allocation, interfaces and owner decisions; next L2 planning unit remains unselected |
| [Development operating model](./development-operating-model.md) | Observable outcomes, hierarchical planning, milestone packs, independent tickets, Git and CI/CD |
| [Agent delivery ADR](../adr/0003-agent-delivery-model.md) | Hierarchical-planning amendment, independent ticket route and historical staged-system retirement |
| [Development runtime contract](./development-runtime-contract.md) | Fast Loop, Hybrid, Full Stack, and Release modes, escalation rules, ownership, and proof boundaries |
| [Documentation platform](./documentation-platform.md) | Docs as code, `/docs`, `/help`, visibility, and publication |
| [Runtime, network, and installation](./runtime-network-installation.md) | Download-first installation, ports, networks, egress, resources, and container lessons |
| [Quality tooling](./tooling-gates.md) | Canonical commands, hook profiles, and mandatory execution points |
| [Repository architecture](./repository-layout.md) | Physical tree and ownership boundaries |

The overall Foundation operating model is recorded in [ADR-0001](../adr/0001-foundation-operating-model.md). The Edge role, separate `edge_to_web` and `web_to_api` networks, and independent production firewall/CNI hardening are recorded in [ADR-0002](../adr/0002-edge-ingress-network-segmentation.md). The runtime/data graph W11-W17 remains independent of Web implementation. The current Web frontier is the bounded [ticket graph](../../.codex/delivery/graphs/custometry-web-implementation-frontier-v1.json); ticket frontmatter, not the graph or a historical UI ledger, is status authority. Templates for new architecture and module documents are in [docs/contracts](../contracts/README.md).

## Status

These documents describe the target state and repository-preparation rules. A runtime or gate is not considered proven until it is implemented and observed at its real boundary. The existence of a document, empty directory, mock, unit test, or green static hook does not establish API, PostgreSQL, Compose, browser, recovery, performance, or release readiness.
