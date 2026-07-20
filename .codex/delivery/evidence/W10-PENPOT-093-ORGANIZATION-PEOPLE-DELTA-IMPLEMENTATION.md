---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.3-draft
ticket_id: W10-PENPOT-093-ORGANIZATION-PEOPLE-DELTA-IMPLEMENTATION
proof_boundary: canonical-penpot-product-0.9.3-ui-0.6.3-organization-access-ownership-and-people-visual-delta
proof_skills: [penpot-design-delivery]
verdict: passed
penpot_file_id: 7cd71457-8d32-8044-8008-549f83bb4645
penpot_start_revision: 197
penpot_end_revision: 213
repository_fingerprint: f062de8a4c738ed18d6de0feb68e97ca819ecf4ca6edecac0178cc2afc194018
redaction: No credentials, customer data, Penpot document payloads, browser state, or environment dumps were retained.
executed_checks:
  - confirm W08, W08 analytics baseline recovery, and W09 are accepted with passed terminal evidence
  - read-only semantic reconciliation of every one of the 25 declared context_sources against the accepted W09 organization/access contract
  - exact ordered 25-source SHA-256 fingerprint twice at the controlled terminal rebase snapshot
  - canonical Penpot file ID, current revision, and currentFile.validate read-only checks
  - exact contract-to-Penpot stable-ID reconciliation for 116 routes, 25 overlays, and 5 system surfaces
  - C25 inventory, Company navigation, named flow 10, and flow-interaction chain inspection
  - fresh individual Penpot PNG visual review of C25, six new routes, four declared existing routes, and both flow bridge boards
  - target direct-child overlap and containment scan
  - uv run python -m tools.custometry_quality.validate_route_registry
  - uvx check-jsonschema --schemafile packages/contracts/routes/ui-route-contracts.schema.json packages/contracts/routes/ui-route-contracts.json
  - uvx check-jsonschema --schemafile packages/contracts/routes/ui-surface-contracts.schema.json packages/contracts/routes/ui-surface-contracts.json
  - uv run python -m tools.custometry_quality.validate_delivery_tickets
  - git diff --check
observations:
  - Canonical Penpot file 7cd71457-8d32-8044-8008-549f83bb4645 remained at revision 213 across the final structural and terminal reads; currentFile.validate returned an empty list.
  - The controlled terminal-rebase source fingerprint was f062de8a4c738ed18d6de0feb68e97ca819ecf4ca6edecac0178cc2afc194018 at both checks.
  - The final exact stable-ID reconciliation found 116 routes, 25 overlays, and 5 system surfaces with no duplicate, missing, or orphan ID.
  - The user explicitly authorized this controlled terminal rebase after read-only reconciliation found no product-scope or contract change.
---

# W10 Penpot Organization, People & Admin Delta Evidence

> Terminal evidence for one accepted design-delivery ticket. It records the
> governed source rebase and does not change the product specification or any
> predecessor ticket/evidence record.

## Outcome and scope

- outcome: the canonical Penpot file visibly represents the accepted
  organization, department access/ownership, and privacy-safe People & Creators
  delta;
- requirement IDs: [UC-028, UC-029, RBAC-019, RBAC-020, RBAC-021, RBAC-022,
  RBAC-023, RBAC-024, RBAC-025, RBAC-026, RBAC-027, RBAC-028, TEST-INV-076,
  TEST-INV-077, TEST-INV-078, TEST-INV-079, TEST-INV-080, TEST-INV-081,
  TEST-INV-082, TEST-INV-083, TEST-INV-084, TEST-INV-085, TEST-INV-086,
  TEST-INV-087, TEST-INV-088, V1-AC-037, V1-AC-038, V1-AC-039, V1-AC-040,
  V1-AC-041, V1-AC-042, V1-AC-043];
- included: C25, Company navigation, six new route frames, four declared
  existing-route updates, and named prototype flow 10;
- exclusions: browser/runtime accessibility, authorization enforcement,
  persistence, activity projections, calculation, exports, performance,
  deployment, and release proof.

## Guard history and controlled terminal rebase

The original W10 run correctly stopped before acceptance when its historical
pre-write fingerprint
`f543c32c1197640bc7858061a99a39f30c27529888fae0e685fdb838cedfaafa`
differed from its first terminal observation
`dfb9e1098a7b5d928085e0b901b65081642788e0455ed5c4119f244dfdc22950`.
The earlier observation of revisions 191 to 192 remains a pre-write incident,
not a W10 modification. W08 overlap recovery subsequently established the
actual W10 start guard at revision 197.

The historical run did not retain a per-file pre-write manifest, so the prior
aggregate hash could not identify individual byte changes. The authorized
read-only reconciliation therefore verified the current 25 declared paths,
the accepted W08/recovery/W09 records, and the complete current W09
organization/access source set. All product/UI/architecture/route/localization
content is the accepted `0.9.3-draft` / `0.6.3-draft` scope: the six declared
route identities, requirement set, access boundaries, and localization keys
are unchanged. No new product meaning, route identity, or executable contract
was found.

With the user's explicit authorization, the terminal gate was rebased to the
stable current source snapshot. The exact ordered SHA-256 command over the
ticket's 25 `context_sources` paths returned
`f062de8a4c738ed18d6de0feb68e97ca819ecf4ca6edecac0178cc2afc194018`
twice. No Penpot mutation occurred after the original mismatch or during this
terminal rebase.

## Predecessors and live-file guards

| Guard | Result | Observation |
| --- | --- | --- |
| W08 discount delta | pass | Ticket `accepted`; terminal evidence `passed`. |
| W08 analytics baseline recovery | pass | Ticket `accepted`; terminal evidence `passed`. |
| W09 organization/access contract | pass | Ticket `accepted`; terminal evidence `passed`. |
| Canonical file | pass | `7cd71457-8d32-8044-8008-549f83bb4645`. |
| Final revision stability | pass | Sequential final reads remained at `213`. |
| File validation | pass | `currentFile.validate()` returned `[]`. |
| Controlled terminal fingerprint | pass | `f062de8a4c738ed18d6de0feb68e97ca819ecf4ca6edecac0178cc2afc194018` twice. |

## Penpot delta and structural reconciliation

| Surface kind | Expected | Actual | Verdict |
| --- | ---: | ---: | --- |
| Route frames | 116 | 116 | pass |
| Overlay/state frames | 25 | 25 | pass |
| System surfaces | 5 | 5 | pass |
| Duplicate, missing, or orphan stable IDs | 0 | 0 | pass |

Created W10 surfaces and components:

- C25 Organization, Ownership & People
  (`2311ae53-d9f0-80b6-8008-5b1ebed340f5`) with Org tree & table,
  Member & leader scope, Policy & grants, Ownership & creators, and
  Privacy-safe activity component boards;
- `UI-ORG-001` (`2311ae53-d9f0-80b6-8008-5b1ebfe3bd54`),
  `UI-ORG-002` (`2311ae53-d9f0-80b6-8008-5b1f353d1f4d`),
  `UI-PEOPLE-001` (`2311ae53-d9f0-80b6-8008-5b1f3955c8ec`),
  `UI-PEOPLE-002` (`2311ae53-d9f0-80b6-8008-5b1f3d3b0d26`),
  `UI-ADMIN-019` (`2311ae53-d9f0-80b6-8008-5b1f4184b75d`), and
  `UI-ADMIN-020` (`2311ae53-d9f0-80b6-8008-5b1f45bd5c31`);
- declared existing targets `UI-ADMIN-003`
  (`e451483d-aae3-807d-8008-54a9f7722b81`), `UI-ADMIN-018`
  (`3e34a4ec-283e-800b-8008-593347ebb7a7`), `UI-RPT-001`
  (`e451483d-aae3-807d-8008-54a9e6d259ad`), and `UI-DASH-001`
  (`e451483d-aae3-807d-8008-54a9d7749e38`).

Company navigation exposes Organization and People & Creators without merging
Administration into business browsing. Direct-child sibling geometry and
containment checks for every W10 target found no unintended overlap or
overflow.

Named flow 10 is present with start board `UI-ADMIN-019`:

`10 Organization setup → access & ownership → Department Hub → People → report/dashboard return`

Its working same-page prototype chain is `UI-ADMIN-019` → `UI-ADMIN-020` →
`UI-ORG-001` → `UI-ORG-002` → `UI-PEOPLE-001` → `UI-PEOPLE-002` →
Authorized report discovery bridge (`2311ae53-d9f0-80b6-8008-5b2827dcb31a`) →
Authorized dashboard discovery bridge (`2311ae53-d9f0-80b6-8008-5b282a850ab1`) →
`UI-ADMIN-019`. The bounded expired-grant branch links `UI-ADMIN-020` to
`UI-ADMIN-018`; the return path is present. The two bridge boards are
explicitly non-contract prototypes required by Penpot's page-local navigation;
no stable route, overlay, or system ID was created.

## Final visual QA

Fresh PNG exports at revision 213 were reviewed individually. For
`UI-PEOPLE-001` and `UI-ADMIN-003`, independent current exports of the sidebar
and W10 content panel were also reviewed against the root-frame geometry to
verify the complete composition.

| Target | Visual verdict |
| --- | --- |
| C25 Organization, Ownership & People | pass |
| UI-ORG-001 | pass |
| UI-ORG-002 | pass |
| UI-PEOPLE-001 | pass |
| UI-PEOPLE-002 | pass |
| UI-ADMIN-019 | pass |
| UI-ADMIN-020 | pass |
| UI-ADMIN-003 | pass |
| UI-ADMIN-018 | pass |
| UI-RPT-001 | pass |
| UI-DASH-001 | pass |
| Flow 10 authorized report bridge | pass |
| Flow 10 authorized dashboard bridge | pass |

No target showed clipping, covered content, unintended overlap, hidden-count
leak, leaderboard treatment, color-only state treatment, or misaligned
controls. The visual proof is Penpot-artifact evidence only.

## Commands and observations

| Command | Result | Observation |
| --- | --- | --- |
| `uv run python -m tools.custometry_quality.validate_route_registry` | pass | 116 routes, 25 overlays, 5 systems, 22 capabilities, 29 use-case bindings. |
| route JSON Schema | pass | `ui-route-contracts.json` validated. |
| surface JSON Schema | pass | `ui-surface-contracts.json` validated. |
| `uv run python -m tools.custometry_quality.validate_delivery_tickets` | pass | 20 tickets validated after the W10 terminal status update. |
| `git diff --check` | pass | No whitespace errors. |

## Verdict

`passed`. The user-authorized controlled terminal rebase replaces only the
unreconstructable historical aggregate-fingerprint gate. W10 retains its
actual start revision 197 and verified terminal revision 213; no product or
contract source was changed by this ticket.
