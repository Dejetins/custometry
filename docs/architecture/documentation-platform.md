---
doc_id: ARCH-DOCUMENTATION-PLATFORM-001
title: Custometry documentation platform
doc_version: 2
product_spec_version: 0.8.2-draft
visibility: internal
ship: false
owner: product-documentation
requirement_ids: [HELP-001, HELP-002, HELP-003, HELP-004]
status: accepted
proof_boundary:
  label: documentation-governance-and-target-information-architecture
  exclusions: [permission-aware-help-runtime, authenticated-docs-serving, penpot-acceptance]
---

# Custometry Documentation Platform

## 1. Goal

Human-readable documentation is part of the locally installed product. A user must not depend on GitHub, a CDN, or an external website to install, use, operate, or diagnose Custometry.

The authoring source is Markdown in the repository. The target static engine is MkDocs Material. A separate React route, `/help`, uses the same generated index and connects page context to permitted articles, stable error codes, keyboard shortcuts, and published Data Guides.

## 2. Three distinct types of knowledge

| Type | Source of truth | Delivery |
|---|---|---|
| Product documentation | Versioned Markdown in Git | `/docs`, as a built release artifact |
| Contextual help | Generated allowlisted index + route/error mappings | `/help` and inline Help in Web |
| Workspace Data Guides | Versioned runtime content in PostgreSQL/artifacts | Permission-aware `/help` and Data Guide UI |

A Data Guide is not stored as a customer-specific Git document. Architecture, ADRs, prompts, and iteration evidence are not indexed in the user installation.

### Foundation source split

Until the visibility-aware product index is implemented, fail-closed boundaries are separated physically:

- `docs-site/docs/**` is the only source for the current public MkDocs artifact;
- `docs/**` contains contributor architecture, contracts, templates, evidence, and the generated contributor `docs/README.md`;
- `docs/user-guide/**` currently contains governance and template contracts and is not copied automatically into the product image.

One article must not have two semantically different copies. Moving product documentation to one metadata-driven source is a separate compatible change after a tested visibility builder exists; until then, the public build allowlist is exactly `docs-site/docs/**`.

## 3. Visibility contract

Every publishable Markdown document has frontmatter:

```yaml
---
doc_id: install-local
title: Local installation
doc_version: 1
product_spec_version: 0.8.2-draft
locale: en
visibility: public | authenticated | internal
ship: true | false
audiences: [installer, user, operator, administrator, developer]
route: /docs/en/install/local/
status: draft | active | deprecated
owner: <role-or-team>
requirement_ids: [<stable-id>]
proof_boundary:
  label: <exact-observed-boundary>
  exclusions: [<what-this-does-not-prove>]
reviewed_at: "YYYY-MM-DD"
---
```

Every listed field is required for every Markdown document under `docs-site/docs/**`, regardless
of `ship`. `doc_id` is a stable lower-kebab identifier shared by language variants; generated
`help-index.json` exposes it as `id` for compatibility with the current Web consumer. `doc_version`
is a positive integer, and `product_spec_version` exactly matches the current `spec_version` in the
machine blueprint. `locale` is either `en` or `ru`; `audiences` is a non-empty, duplicate-free list
containing only `installer`, `user`, `operator`, `administrator`, and `developer`. `route` is the
single canonical `/docs/.../` route determined by the source path; contextual `/help` mappings are
not duplicated in this field and belong to a separate route/help contract.

`owner` uses a lower-kebab role or team identity. `requirement_ids` is a non-empty list of stable
IDs that actually exist in the machine blueprint. `proof_boundary.label` and the non-empty
`proof_boundary.exclusions` list record the observed boundary and what the article does not prove.
`reviewed_at` is a quoted ISO date. A `draft` document cannot have `ship: true`; an `internal`
document can never have `ship: true`.

The current `audience=shipped` builder creates a public static artifact and therefore accepts
`ship: true` only with `visibility: public`. An `authenticated` source may exist only with
`ship: false` until a separate server-side authorized builder and route are implemented. Client-side
filtering of public `help-index.json` is not, and is never treated as, a security control.

| Visibility | Included content | Access |
|---|---|---|
| `public` | Safe installation, first-run, and user guides, plus release and version support | Available locally without workspace membership; contains no private topology or secret examples |
| `authenticated` | Operator and administrator procedures, runtime health, backup, access, and workspace operations | Only after authentication and a permission check; a static asset must not bypass the guard |
| `internal` | Architecture, ADRs, contracts, prompt packs, stage/iteration evidence, and contributor internals | Never included in the ordinary installation artifact |

`visibility` is a security boundary; `ship` is explicit permission to include the document in the product build. Classification errors, missing fields, or `ship: false` block publication. Client-side hiding is not authorization: authenticated documentation is either served through a protected route or built as a separate protected artifact.

## 4. Information architecture

### `/docs`

```text
Getting started
  What is Custometry
  Requirements and installation
  First run and workspace
  Demo data

User guide
  Data Foundation
  Data Quality
  Analytics and vs LY
  Forecasting
  Promotions
  Dashboards, reports and exports

Reference
  Roles and permissions
  Concepts and glossary
  Filters, metrics and Result Trust
  Stable error/status codes
  Keyboard shortcuts

Operations (authenticated)
  Installation health
  Capacity and resources
  Backup/restore
  Upgrades and rollback
  Network/egress and mail
  Troubleshooting/runbooks

Version and support
  Release notes
  Compatibility
  Licenses/SBOM/provenance
```

### `/help`

- permission-aware search;
- contextual articles for the current canonical route;
- stable error-code lookup;
- keyboard shortcuts;
- Data Guides visible to the current workspace and role;
- version information, support-bundle guidance, and deterministic deep links;
- no leakage through titles, snippets, counts, or cached results.

## 5. Docs-as-code lifecycle

1. Locate the current canonical document; do not create a new file if the existing one can be updated safely.
2. Change a product requirement first in the machine blueprint, then synchronize the human-readable mirror.
3. A behavior change updates user/operator documentation and contextual mapping in the same pull request.
4. An operational failure mode updates the versioned runbook, alert trigger, and safe evidence/redaction guidance.
5. Foundation `generate_docs_index --check` verifies both committed artifacts: the deterministic contributor index and the minimal shipped Help index. Shipped mode fails closed and validates complete frontmatter, the current specification version, requirement IDs, canonical route, identity/locale uniqueness, H1/title parity, and shipping policy. The Web JSON retains only `id`, `title`, `visibility`, `locale`, `route`, and `path`. `check_docs_links` separately validates real relative links and anchors. These static checks do not prove permission-aware search or server-side authorization.
6. The build publishes only allowlisted visibility classes, local assets and fonts, and a fixed product version.
7. Browser smoke verifies navigation, search, direct deep links, 404/forbidden behavior, en/ru support, and the absence of network fetches to a CDN.
8. A deprecated document remains available only according to version policy and points to its replacement; silently deleting a stable deep link is prohibited.

CI never auto-commits a generated index. The author runs the generator, reviews the diff, and commits the result; CI uses `--check`.

## 6. Style and templates

- Repository-authored engineering documents, templates, prompts, ledgers, and reports are written in English by default.
- The normative `*-ru` blueprints and localized product content under `docs-site/docs/ru/**` are explicit standing exceptions. Any other Russian artifact requires an explicit request for that artifact.
- Only the final user-facing completion report defaults to Russian; intermediate repository artifacts and engineering evidence remain in English.
- Contributor mode in `generate_docs_index` enforces this English-default authoring policy fail-closed while allowing only the explicit exceptions above.
- Code identifiers, routes, stable IDs, and error codes remain literal.
- A heading describes the user's task rather than an internal package name.
- The first section answers: for whom, what result, which prerequisites, and which permissions.
- A procedure contains numbered steps, the expected result, safe rollback, and the next action on failure.
- Secret and PII examples use obvious placeholders; real payloads are prohibited.
- Commands are copyable and state the working directory or platform when material.
- Every runtime claim matches observed proof; a future target is labeled as a target.
- A diagram supplements the text rather than replacing an accessibility-readable explanation.

An architecture document uses [architecture-document-template.md](../contracts/architecture-document-template.md), a cross-module contract uses [contract-document-template.md](../contracts/contract-document-template.md), and a module definition uses [module-definition-template.md](../contracts/module-definition-template.md). The repository also uses the [ADR template](../adr/adr-template.md), [runbook template](../runbooks/runbook-template.md), and [user/install guide template](../user-guide/user-install-guide-template.md).

## 7. Versioning and synchronization

- The product documentation build has its own immutable release version and refers to the application/specification version.
- `/help` shows a documentation/application mismatch and does not present an obsolete action as safe.
- Machine and human-readable blueprints must have the same `document_family_id`, `spec_version`, mutual links, and requirement IDs.
- The UI route registry ↔ help mapping is validated automatically.
- en/ru catalogs and localized documentation navigation labels pass a parity check.
- A Data Guide version is pinned in `ReportSnapshot` when it is used for explanation or export.

## 8. Penpot design scope

Before the documentation UI is implemented, a dedicated Penpot design pass must cover:

- documentation home and navigation;
- an article containing code, a table, a callout, and a diagram;
- search, results, and no-results states;
- contextual Help drawer and deep link;
- authenticated/operator boundary;
- version-mismatch and deprecated banners;
- 403, 404, and offline states;
- Data Guide editor, preview, validation, publication, and history;
- keyboard, focus, reduced-motion, and responsive behavior.

Penpot proves layout and interaction intent, but not authorization, search correctness, offline delivery, or runtime accessibility. Those properties are accepted through browser and integration gates.

## 9. Content excluded from delivery

The ordinary installation does not contain:

- `docs/architecture/**`;
- `docs/adr/**`;
- `docs/contracts/**` contributor contracts;
- `docs/iterations/**`;
- `.codex/**`, prompts, ledgers, or agent reports;
- raw CI logs, environment dumps, or private deployment examples.

Contributor documentation may be published separately on a public project site, but it is not mixed with permission-aware product documentation and is not included in `/help`.
