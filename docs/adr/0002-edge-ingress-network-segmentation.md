---
doc_id: ADR-0002
title: Edge ingress adapter and network segmentation
doc_version: 1
product_spec_version: 0.9.0-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: [SEC-016, SEC-017, SEC-018]
status: accepted
proof_boundary:
  label: accepted-foundation-ingress-segmentation
  exclusions: [production-edge-egress-denial, production-firewall-proof, multi-host-topology]
---

# ADR-0002: Edge ingress adapter and network segmentation

- status: `accepted`;
- date: `2026-07-16`;
- decision owners: project owner, architecture owner and platform owner;
- scope: Foundation Compose ingress path and later production hardening;
- supersedes: shared `application` network assumption in the initial Foundation scaffold;
- related: [System Design](../architecture/system-design.md), [runtime contract](../architecture/runtime-network-installation.md), [ADR-0001](./0001-foundation-operating-model.md).

## Context

On Docker Desktop, a container attached to an `internal: true` network cannot portably serve as both a reliably published host ingress and a process proven to have no outbound route. A shared Edge/Web/API network simplified routing but left direct Edge-to-API adjacency. The statement that a fixed upstream means no egress also conflated two distinct properties: restricting reverse-proxy configuration and enforcing process-level network policy.

We need an explicit and accurate Foundation boundary that:

- preserves a single loopback host ingress;
- does not expose Web, API, or PostgreSQL on the host;
- gives Edge no direct container-network adjacency to API, control, or data services;
- does not attribute to Docker Compose a guarantee it does not provide portably;
- leaves strict production enforcement as a separate observable stage.

## Decision

1. Edge is an infrastructure ingress adapter, not a bounded context or an independently evolved product microservice.
2. Edge reuses the immutable Web image, runs a fixed Nginx configuration, remains secretless, read-only, and stateless, and receives no business logic, environment override, writable mount, or user-controlled upstream.
3. `ingress_edge` is the only non-internal transport network and contains only Edge.
4. `edge_to_web` is an internal network containing only Edge and Web.
5. `web_to_api` is a separate internal network containing only Web and API.
6. Edge and the API, control, and data services share no network adjacency; Web is the only bridge on the `Edge → Web → API` path.
7. Web and API pass negative Internet probes. Runtime smoke verifies `Edge → Web` and `Web → API`, while direct `Edge → API` access must fail.
8. Foundation does not claim strict Edge outbound denial: the non-internal transport network may retain an ambient outbound route.
9. Workstream 12, `Hardening`, applies a host firewall, CNI, or equivalent policy on each production target and observably denies Edge access to API, control, data, Internet, private, link-local, and metadata destinations, leaving only the approved ingress and `Edge → Web` path.

## Alternatives

| Alternative | Why it was not selected |
|---|---|
| Shared internal Edge/Web/API network | Leaves direct Edge-to-API adjacency and merges trust boundaries |
| Expose Web publicly without Edge | Moves host binding and transport concerns into the application container |
| Relax the Web/API network for portable host publication | Gives core services ambient outbound access and expands the attack surface |
| Call a fixed upstream a firewall | Incorrect: proxy routing configuration does not restrict every outbound socket call |
| Require one portable firewall mechanism in Compose | No such common mechanism exists across Docker Desktop and all future targets |

## Consequences

Benefits:

- compromise of Edge does not provide direct Docker adjacency to API, control, or data services;
- Web and API remain on internal networks and retain negative egress evidence;
- there is still one host ingress, loopback-only by default;
- the documentation explicitly separates Compose containment from production enforcement;
- Edge creates no new domain or service ownership.

Costs and limitations:

- Web participates in two internal networks and is an intentional ingress bridge;
- Edge may retain ambient transport egress until target hardening;
- production promotion requires target-specific firewall/CNI implementation, tests, and rollback;
- the runtime-policy schema and network membership must be updated atomically with Compose and the validator.

## Compatibility, rollout and rollback

| Surface | Classification |
|---|---|
| Public URL, browser routes, HTTP API | `none` |
| PostgreSQL schema, volumes, artifacts | `none` |
| Browser-visible behavior | `compatible-change` |
| Compose network names/membership | `breaking-change` |
| Runtime-policy schema v1→v2 | `breaking-change` |
| Production Edge egress readiness | `unknown` until target-specific evidence exists |

Rollout recreates Edge, Web, and API under one coordinated Compose version. Old and new Compose, policy, and validator versions must not be mixed. Rollback runs project-scoped `docker compose down --remove-orphans` without `--volumes`, restores the coordinated prior Compose/policy/validator trio, and repeats bootstrap. Host-wide network pruning is prohibited.

## Verification

Foundation evidence:

- the static validator requires exact `edge_to_web` and `web_to_api` membership;
- the versioned runtime policy fixes the source Nginx configuration, the `web:8080` upstream, and separate allowed and denied ingress probes; the static validator rejects a dynamic resolver, an external or API upstream, and any `proxy_pass` that bypasses the declared Web upstream;
- Edge/API network overlap fails closed;
- runtime and browser smoke tests verify host→Edge→Web→API;
- runtime smoke verifies successful Edge→Web access and failed Edge→API access;
- Web/API negative Internet probes continue to pass.

Production evidence must additionally observe target firewall/CNI enforcement, Edge outbound denial, denial of private, link-local, and metadata destinations, and rollback policy. This ADR is not itself such runtime evidence.

## Re-evaluation triggers

- a second production engine or operating system;
- LAN or external load-balancer ingress;
- Kubernetes/CNI deployment;
- service-mesh or gateway extraction;
- a separate Edge release cadence or the introduction of secrets;
- a change to the Web proxy role;
- multi-host topology.
