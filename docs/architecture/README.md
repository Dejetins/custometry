---
doc_id: ARCH-INDEX
title: Custometry Architecture
doc_version: 10
product_spec_version: 0.9.4-draft
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

1. `custometry-technical-blueprint-ru.md` contains the normative product requirements, version `0.9.4-draft`.
2. `custometry-technical-blueprint-human-ru.md` is the synchronized human-readable mirror.
3. `custometry-ui-blueprint-ru.md` is the derived UI/UX contract.
4. Documents in this directory contain accepted architecture and process decisions within the blueprint.
5. Global Delivery Contract v1 defines artifact choice and ticket authority. A ready Custometry delivery ticket is the current execution source for one execution unit; a platform Goal is optional and requires explicit user or platform authority. Custometry keeps no standing program plan, generated prompt-pack inventory, or execution ledger. `validate_delivery_contract` validates the portable adapter and can optionally inspect an installed global source.

If sources conflict, the higher-precedence source applies. An architecture document does not introduce a new normative `MUST`: a new product obligation is first added to the machine blueprint and mirrored synchronously in the human-readable version.

## Document map

| Document | Purpose |
|---|---|
| [System Design](./system-design.md) | Complete `0.9.4-draft` target architecture, accepted decisions, flows, trust boundaries, compatibility, proof limits, and direction of evolution |
| [Bounded context map](./bounded-context-map.md) | Context ownership, public ports, dependency direction, consistency, and cross-context integration policy |
| [Executable UI route contract](../contracts/ui-route-contract.md) | Identity/execution manifest split, guard/permission/state/history semantics, agent resolution, and validation rules |
| [UI surface coverage contract](../contracts/ui-surface-contract.md) | Requirement-to-surface coverage, route decision policy, Penpot baseline identity, and complete agent load order |
| [Linear-workspace transition standard](./ui/linear-workspace-ui-transition-standard-v1.md) | Shared React/MobX/Query/styled-components baseline, four themes, workspace behavior, motion, responsiveness, performance budgets, and migration method |
| [Linear reference manifest](./ui/linear-workspace-reference-manifest-v1.json) | Sanitized source hashes, observed reference states, viewport metadata, and evidence gaps without shipping third-party captures |
| [Custometry UI migration registry](./ui/custometry-linear-ui-migration-registry-v1.json) | Project-owned legacy authority, target stack, W19-W23 route, and supersession mapping |
| [Custometry UI transition specification](../../.codex/delivery/specs/custometry-linear-workspace-ui-transition.md) | Accepted compatibility and delivery boundary for the authenticated Web replatform |
| [Custometry UI transition graph](../../.codex/delivery/graphs/custometry-linear-workspace-ui-transition-v1.json) | Executable dependency and path-ownership graph; ticket frontmatter remains status authority |
| [Development operating model](./development-operating-model.md) | UI-first vertical slices, ticket-first execution, optional coordination artifacts, Git, and CI/CD |
| [Agent delivery ADR](../adr/0003-agent-delivery-model.md) | Ticket-first execution and removal of the obsolete staged planning system |
| [Development runtime contract](./development-runtime-contract.md) | Fast Loop, Hybrid, Full Stack, and Release modes, escalation rules, ownership, and proof boundaries |
| [Documentation platform](./documentation-platform.md) | Docs as code, `/docs`, `/help`, visibility, and publication |
| [Runtime, network, and installation](./runtime-network-installation.md) | Download-first installation, ports, networks, egress, resources, and container lessons |
| [Quality tooling](./tooling-gates.md) | Canonical commands, hook profiles, and mandatory execution points |
| [Repository architecture](./repository-layout.md) | Physical tree and ownership boundaries |

The overall Foundation operating model is recorded in [ADR-0001](../adr/0001-foundation-operating-model.md). The Edge role, separate `edge_to_web` and `web_to_api` networks, and independent production firewall/CNI hardening are recorded in [ADR-0002](../adr/0002-edge-ingress-network-segmentation.md). The runtime/data graph W11-W17 and UI graph W19-W23 may progress in parallel only in separate branches or worktrees with disjoint path ownership; W23 joins the streams after W16 and W22. Templates for new architecture and module documents are in [docs/contracts](../contracts/README.md).

## Status

These documents describe the target state and repository-preparation rules. A runtime or gate is not considered proven until it is implemented and observed at its real boundary. The existence of a document, empty directory, mock, unit test, or green static hook does not establish API, PostgreSQL, Compose, browser, recovery, performance, or release readiness.
