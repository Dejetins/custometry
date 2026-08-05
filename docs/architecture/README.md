---
doc_id: ARCH-INDEX
title: Custometry Architecture
doc_version: 13
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
3. `custometry-ui-blueprint-ru.md` is the accepted pre-G0 UI/UX intent and current-inventory baseline; its hash-pinned pilot is visual-language authority only, not exact composition or frontend architecture authority.
4. Documents in this directory contain accepted architecture and process decisions within the blueprint.
5. Global Delivery Contract v1 defines artifact choice and ticket authority. A ready Custometry delivery ticket is the current execution source for one execution unit; a platform Goal is optional and requires explicit user or platform authority. Custometry keeps no standing program plan, generated prompt-pack inventory, or execution ledger. `validate_delivery_contract` validates the portable adapter and can optionally inspect an installed global source.

If sources conflict, the higher-precedence source applies. An architecture document does not introduce a new normative `MUST`: a new product obligation is first added to the machine blueprint and mirrored synchronously in the human-readable version.

## Document map

| Document | Purpose |
|---|---|
| [System Design](./system-design.md) | Complete `0.10.0-draft` target architecture, accepted decisions, flows, trust boundaries, compatibility, proof limits, and direction of evolution |
| [Bounded context map](./bounded-context-map.md) | Context ownership, public ports, dependency direction, consistency, and cross-context integration policy |
| [Executable UI route contract](../contracts/ui-route-contract.md) | Identity/execution manifest split, guard/permission/state/history semantics, agent resolution, and validation rules |
| [UI surface coverage contract](../contracts/ui-surface-contract.md) | Requirement-to-surface coverage, route decision policy, historical design provenance, and complete agent load order |
| [UI design program governance ADR](../adr/0004-ui-design-program-governance.md) | Retires the previous Linear/Penpot target, defines the pre-G0 boundary, and routes future product-wide UI work through `ui-design-program` |
| [Collaboration, digital measurement, and compute reuse ADR](../adr/0005-collaboration-measurement-and-compute-reuse.md) | Audits comparable products and accepts the new collaboration/adoption, retail digital-measurement, and materialization/reuse boundaries |
| [Analytical documents, segments, and product analytics ADR](../adr/0006-analytical-document-retail-product-and-time-aware-segmentation.md) | Accepts one analytical-document composition/snapshot path, time-aware segment identity, retail product/category/inventory boundaries, compatibility, and migration direction |
| [Comparable analytics platform capability audit](./ui/comparable-analytics-platform-capability-audit-v1.md) | Official-documentation audit of established multi-page authoring, collaboration, segments, digital/product analysis, adoption, and compute-reuse patterns plus Custometry's accepted response and deliberate non-copy boundary |
| [Pre-G0 pilot manifest](./ui/custometry-pre-g0-pilot-manifest-v1.json) | Hash-pins the accepted RU/EN `renderable_html` visual-language/density anchor and its explicit exclusions |
| [Development operating model](./development-operating-model.md) | UI-first vertical slices, ticket-first execution, optional coordination artifacts, Git, and CI/CD |
| [Agent delivery ADR](../adr/0003-agent-delivery-model.md) | Ticket-first execution and removal of the obsolete staged planning system |
| [Development runtime contract](./development-runtime-contract.md) | Fast Loop, Hybrid, Full Stack, and Release modes, escalation rules, ownership, and proof boundaries |
| [Documentation platform](./documentation-platform.md) | Docs as code, `/docs`, `/help`, visibility, and publication |
| [Runtime, network, and installation](./runtime-network-installation.md) | Download-first installation, ports, networks, egress, resources, and container lessons |
| [Quality tooling](./tooling-gates.md) | Canonical commands, hook profiles, and mandatory execution points |
| [Repository architecture](./repository-layout.md) | Physical tree and ownership boundaries |

The overall Foundation operating model is recorded in [ADR-0001](../adr/0001-foundation-operating-model.md). The Edge role, separate `edge_to_web` and `web_to_api` networks, and independent production firewall/CNI hardening are recorded in [ADR-0002](../adr/0002-edge-ingress-network-segmentation.md). The runtime/data graph W11-W17 remains independent of the retired UI route. No frontend implementation graph is currently ready; the next product-wide UI path begins only after `ui-design-program` admission. Templates for new architecture and module documents are in [docs/contracts](../contracts/README.md).

## Status

These documents describe the target state and repository-preparation rules. A runtime or gate is not considered proven until it is implemented and observed at its real boundary. The existence of a document, empty directory, mock, unit test, or green static hook does not establish API, PostgreSQL, Compose, browser, recovery, performance, or release readiness.
