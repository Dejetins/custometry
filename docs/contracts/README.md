# Documentation and boundary contracts

This directory contains reusable contributor templates and descriptions of inter-module contracts. It is not published in the standard product documentation artifact.

## Templates

- [Architecture document](./architecture-document-template.md) — durable architecture decision or target state.
- [Contract document](./contract-document-template.md) — versioned API/DTO/event/port/artifact boundary.

## Accepted contracts

- [Executable UI route contract](./ui-route-contract.md) - canonical identity/execution manifest split, guard and permission semantics, route state/history policy, and agent usage.
- [UI surface coverage contract](./ui-surface-contract.md) - complete use-case binding across routes, overlays, system surfaces, and reusable cross-surface capabilities.

A template is not an accepted decision or executable ticket. Remove all
placeholders, distinguish facts from proposals, and obtain stable requirement
IDs from the generated requirement index.

## Foundation contract drift manifest

`contract-drift.json` lists the OpenAPI document, external JSON Schemas, and the
deterministically generated TypeScript client. `openapi_schema_bindings` explicitly
binds only external schemas that describe the same payload as an OpenAPI component. The
gate compares requiredness, types, unions, object shape, and validation constraints, then
checks the client byte for byte. Standalone schemas, such as the route registry, remain
digest sources without receiving a false binding to an unrelated API component.
