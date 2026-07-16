---
doc_id: ARCH-INDEX
title: Custometry Architecture
doc_version: 2
product_spec_version: 0.8.2-draft
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

1. `custometry-technical-blueprint-ru.md` contains the normative product requirements, version `0.8.2-draft`.
2. `custometry-technical-blueprint-human-ru.md` is the synchronized human-readable mirror.
3. `custometry-ui-blueprint-ru.md` is the derived UI/UX contract.
4. Documents in this directory contain accepted architecture and process decisions within the blueprint.
5. Future staged work uses exactly `plan_doc + prompt_pack_dir + stage_ledger`, and only the ledger reports current execution state.

If sources conflict, the higher-precedence source applies. An architecture document does not introduce a new normative `MUST`: a new product obligation is first added to the machine blueprint and mirrored synchronously in the human-readable version.

## Document map

| Document | Purpose |
|---|---|
| [System Design](./system-design.md) | Overall architecture, accepted decisions, flows, proof boundaries, and direction of evolution |
| [Bounded context map](./bounded-context-map.md) | Data ownership, dependencies, shared kernel, and integration rules |
| [Development operating model](./development-operating-model.md) | UI-first vertical slices, workstream sequence, S00–S06, Git, and CI/CD |
| [Documentation platform](./documentation-platform.md) | Docs as code, `/docs`, `/help`, visibility, and publication |
| [Runtime, network, and installation](./runtime-network-installation.md) | Download-first installation, ports, networks, egress, resources, and container lessons |
| [Quality tooling](./tooling-gates.md) | Canonical commands, hook profiles, and mandatory execution points |
| [Repository architecture](./repository-layout.md) | Physical tree and ownership boundaries |

The overall Foundation operating model is recorded in [ADR-0001](../adr/0001-foundation-operating-model.md). The Edge role, separate `edge_to_web` and `web_to_api` networks, and independent production firewall/CNI hardening are recorded in [ADR-0002](../adr/0002-edge-ingress-network-segmentation.md). Templates for new architecture and module documents are in [docs/contracts](../contracts/README.md).

## Status

These documents describe the target state and repository-preparation rules. A runtime or gate is not considered proven until it is implemented and observed at its real boundary. The existence of a document, empty directory, mock, unit test, or green static hook does not establish API, PostgreSQL, Compose, browser, recovery, performance, or release readiness.
