---
doc_id: docs-home
title: Custometry documentation
doc_version: 3
product_spec_version: 0.11.0-draft
locale: en
visibility: public
ship: true
audiences: [installer, user]
route: /docs/
status: active
owner: product-documentation
requirement_ids: [HELP-001, HELP-003, HELP-004]
proof_boundary:
  label: foundation-public-documentation-home
  exclusions: [permission-aware-help-runtime, authenticated-document-serving]
reviewed_at: "2026-07-16"
---
# Custometry documentation

Custometry is a self-hosted customer analytics and forecasting platform. This documentation is shipped with the installed release and remains available without an external documentation service.

!!! info "Foundation status"
    The current runnable surface proves the application shell, local documentation, API health boundary, control-plane PostgreSQL migration, and deterministic demo source. The bounded sales report workflow is described separately below; other product capabilities remain outside this baseline.

## Start here

- [Install on a local machine](install/local.md)
- [Understand the network boundary](install/network-boundary.md)
- [Explore the Foundation workspace](user-guide/foundation.md)

Operator and administrator runbooks require authentication and are intentionally absent from this public static documentation artifact. Architecture documents, ADR internals, delivery tickets/evidence, and iteration journals are not included in an ordinary installation.

[Sign in and use the sales report workspace](user-guide/reports.md). This guide covers the bounded report feature; installed availability depends on the candidate version.
