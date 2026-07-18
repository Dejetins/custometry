---
doc_id: foundation-workspace
title: Foundation workspace
doc_version: 1
product_spec_version: 0.9.1-draft
locale: en
visibility: public
ship: true
audiences: [user]
route: /docs/user-guide/foundation/
status: active
owner: product-documentation
requirement_ids: [HELP-001, HELP-003, HELP-004, UI-SHELL-001, UI-SHELL-002, UI-SHELL-003]
proof_boundary:
  label: foundation-workspace-user-guide
  exclusions: [product-analytics-readiness, authenticated-help-runtime]
reviewed_at: "2026-07-16"
---
# Foundation workspace

The Foundation workspace is intentionally small. It establishes a stable Frost shell, canonical route registry, collapsible icon navigation, English/Russian catalogs, local Help entry point, and visible API readiness.

Routes reserved by the product blueprint show a **Planned surface** state. That state is a contract boundary, not a product implementation or demo result.

## Available now

- Foundation home at `/`;
- Help entry point at `/help`;
- public local documentation at `/docs/`;
- proxied liveness, readiness, and version endpoints under `/api/`;
- keyboard-visible navigation and reduced-motion support.

Authentication, permission-aware Help, business data, analytics, jobs, exports, email, and administrative actions arrive only in their accepted vertical slices.
