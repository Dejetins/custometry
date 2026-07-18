---
doc_id: USER-GUIDE-INDEX
title: Custometry user guide
doc_version: 1
product_spec_version: 0.9.0-draft
visibility: public
ship: false
audiences: [installer, user]
routes: [/help]
error_codes: []
status: draft
owner: product-documentation
requirement_ids: [HELP-001, HELP-002, HELP-003, HELP-004]
proof_boundary:
  label: documentation-information-architecture-only
  exclusions: [built-docs-site, runtime-help, authorization, offline-browser-proof]
reviewed_at: 2026-07-16
---

# Custometry user guide

This directory contains governance and templates for future metadata-driven user documentation. The current Foundation public MkDocs artifact includes only explicitly safe articles from `docs-site/docs/**`; this directory is not copied automatically into the product image. Until the visibility-aware builder is implemented, this directory does not claim that the Help Center is ready.

A new guide is created from the [user/install guide template](./user-install-guide-template.md), then receives an actual `doc_id`, owner, requirement IDs, proof boundary, and `visibility`. It may be marked `ship: true` only after verification.

Planned safe sections:

1. requirements, installation, and first launch;
2. workspace, roles, and navigation;
3. demo retail data;
4. Data Foundation and Data Quality;
5. analytics, filters, vs LY, and Result Trust;
6. forecasting, promotions, dashboards, and reports;
7. exports and user-initiated email;
8. keyboard/accessibility;
9. error/status code reference;
10. version/compatibility/support.

Operator/admin material uses `authenticated` visibility and must not enter the public static artifact. Contributor architecture, ADRs, contracts, prompts, and iteration evidence are not copied here.
