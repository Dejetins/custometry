---
doc_id: ADR-0001
title: Foundation operating model
doc_version: 2
product_spec_version: 0.8.2-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: [ARCH-PRINCIPLE-001, DOC-RULE-008, HELP-001, SCALE-004]
status: accepted
proof_boundary:
  label: accepted-foundation-decision
  exclusions: [runtime-readiness, github-protection-proof, release-readiness]
---

# ADR-0001: Foundation operating model

- status: `accepted`;
- date: `2026-07-16`;
- decision owners: project owner and architecture owner;
- scope: repository preparation and development operating model;
- supersedes: none;
- related: [System Design](../architecture/system-design.md), [development model](../architecture/development-operating-model.md), [runtime contract](../architecture/runtime-network-installation.md), [ADR-0002](./0002-edge-ingress-network-segmentation.md).

## Context

The repository is at the Foundation stage. We need to establish a tangible Web experience early without creating dozens of disconnected mocks; preserve the DDD modular monolith; make documentation part of the local installation; avoid a heavyweight self-contained container bundle; and avoid repeating failures involving multiple engines, caches, networks, ports, and false green exits.

## Decision

1. The repository remains public.
2. `main` is protected; changes go through pull requests, required checks, squash merges, and linear history; no `develop` branch is created.
3. The delivery contract uses contract-backed, UI-first vertical slices.
4. The first deployment proof is performed locally on a MacBook Pro M3 Pro / Apple Silicon.
5. The Web/API/data core is offline-capable and deny-by-default for egress. Edge is a separate, secretless infrastructure ingress adapter with limited adjacency, but Compose alone does not prove that Edge has no ambient outbound route. Future connector, mail, and update paths receive separate allowlists, while strict Edge policy is handled by the target-specific hardening defined in ADR-0002.
6. The normal local budget is 6 GiB of RAM and 25 GiB of owned disk; benchmarks are opt-in.
7. The default installation is download-first: pinned images and assets are downloaded and verified; a large full-offline bundle is not the default.
8. Public user and installation documentation is available locally; operator and administrator documentation requires authorization; architecture, ADRs, contracts, prompts, and iteration evidence are not included in the ordinary installation.
9. The target documentation runtime uses MkDocs Material to build `/docs`, while in-app `/help` uses the same permission-aware generated index. The Foundation contributor index alone does not prove that runtime.
10. Development data is a deterministic retail/e-commerce corpus with separate control and demo-source PostgreSQL boundaries.
11. Quality tools are composed into the `local`, `ci`, and `release` profiles; a required release observation cannot become successful by being skipped.
12. Every future block uses the common S00–S06 acceptance framework, but a detailed plan, ledger, and prompt pack are created only after separate approval.

## Alternatives

| Alternative | Why it was not selected |
|---|---|
| Backend-first before UI | Reveals incorrect workflows and contracts too late and provides no early browser proof |
| All route mocks first | Creates a parallel, inconsistent product model and expensive rework |
| Long-lived `develop` and context branches | Increase drift and lockstep integration for a single modular monolith |
| Multi-gigabyte autonomous bundle by default | Duplicates layers, caches, and platforms; complicates updates; and consumes unacceptable disk space |
| Public documentation only on GitHub or an external site | Breaks self-hosted and offline usability |
| One PostgreSQL instance for both control and demo source | Does not test the connector/trust boundary and conceals private-table coupling |

## Consequences

Benefits:

- UI and backend evolve against one versioned contract;
- failures are detected at the nearest meaningful real boundary;
- the local installation is smaller and can be updated by digest;
- documentation/help and security visibility are designed up front;
- CI and agents use the same deterministic tooling logic.

Costs:

- contract and schema discipline is required before implementation;
- generated mocks and clients must be maintained by tooling;
- clean Compose, browser, and recovery proofs cost more than unit tests;
- authenticated documentation requires a separate build and serving boundary;
- multi-platform release is deferred until the M3 Pro path is proven.

## Compatibility and migration

Until release consumers exist, this decision is a `compatible-change`. After the first stable consumer appears, changing a route, port precedence, visibility class, package ownership, image reference, or contract-generation rule requires compatibility assessment and migration/rollback.

## Verification

Foundation is accepted only after:

- tested quality tools and grouped profiles pass;
- a clean local bootstrap and Compose smoke test pass on the M3 Pro;
- actual port and network checks pass;
- documentation build, search, visibility, and browser checks pass;
- deterministic fixture and migration evidence exists;
- architecture and governance artifacts receive an independent cold review.

This ADR records the decision but is not itself runtime evidence.

## Re-evaluation triggers

- support for a second host, remote workers, or object storage;
- mandatory air-gapped deployment;
- a multi-tenant hosted control plane;
- a need for a different documentation engine;
- CI or runtime consistently exceeds the accepted M3 budget;
- an independent deployment cadence or trust boundary justifies service extraction.
