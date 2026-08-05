---
doc_id: network-boundary
title: Network boundary
doc_version: 2
product_spec_version: 0.10.0-draft
locale: en
visibility: public
ship: true
audiences: [installer, operator]
route: /docs/install/network-boundary/
status: active
owner: product-documentation
requirement_ids: [HELP-001, HELP-003, HELP-004, SEC-016, SEC-017, SEC-018]
proof_boundary:
  label: foundation-network-boundary-guide
  exclusions: [connector-egress-runtime, production-network-hardening]
reviewed_at: "2026-07-16"
---
# Network boundary

The Foundation application services have no general outbound internet route. Web, API and PostgreSQL stay on internal Docker networks. A separate secretless, read-only `edge` container owns the loopback host binding and forwards to the fixed `web:8080` upstream.

Edge is an infrastructure ingress adapter, not a product microservice or bounded context. It owns no business logic, credentials, writable state, or user-selected destination. `edge_to_web` connects only Edge and Web; `web_to_api` connects only Web and API. Edge and API do not share a Docker network.

Docker Compose does not provide a portable ingress-only network primitive. Host port publishing requires Edge to attach to a non-internal transport bridge on supported Docker Desktop targets, and that bridge may give Edge an ambient outbound route. The fixed upstream limits proxy routing but is not a firewall and does not prove egress denial. This is not a business-egress permission: Web and API remain internal and are checked with negative internet probes.

Strict Edge outbound denial is a separate production-hardening step. Each production target must apply a host firewall, CNI, or equivalent policy that permits only the approved host ingress and `Edge → Web`, denies direct Edge access to API, control/data services, internet, private/link-local/metadata ranges, and verifies those rules with positive and negative runtime probes.

## Published interfaces

| Boundary | Default |
|---|---|
| Edge → Web and proxied API | Random free port on `127.0.0.1` selected by bootstrap |
| Control PostgreSQL | Internal only |
| Demo source PostgreSQL | Internal only, optional `demo` profile |
| Web/API internet egress | Disabled and checked with negative probes |
| Edge → Web | Internal `edge_to_web`; positive runtime probe |
| Web → API | Separate internal `web_to_api`; Edge is not a member |
| Direct Edge → API | Denied by network segmentation and checked with a negative probe |
| Edge transport egress | May exist in Foundation; strict denial requires target firewall/CNI evidence |

The browser reaches `/`, `/docs/`, and `/api/*` through the single Edge endpoint; Web proxies the API route across `web_to_api`. Database credentials are generated into ignored local secret files and mounted only into the services that require them; Edge receives none.
