---
artifact_kind: ui_design_owner_review
program_id: CUSTOMETRY-UI-DESIGN-PROGRAM-V1
gate_id: G2
validation_profile: structure_gate
review_revision: 3
accepted_baseline_revision: 2
accepted_baseline_owner_decision_ref: owner-decision://6a0a7c9ba6635fe6d02a47236a1cca8fd695ab6532f1b767ff9ac0eb28f43a13/.codex/delivery/ui-design-programs/custometry-v1/owner-decision-journal.json?value_sha256=8a8d9a0636437725318364093057c3b02b7a453f17036e819b071cb2539d6065#/iterations/0/owner_decision
manifest_sha256: cdd1f788caceed5b8a7bf42b8733222d5c182661e798d4674fcbc5c3ec555c14
source_hashes:
  - custometry-technical-blueprint-ru.md:eb453f8ab3a316de434d5a272422ebf320475498272b0167c17e32bd3b5a4ee1
  - custometry-technical-blueprint-human-ru.md:6e84cf0de2adc45b0bba335e2a0af9c1ef2df95055ebb466ed9cff0de0880918
  - custometry-ui-blueprint-ru.md:bca5441981a3956bb4a4433faa1beb24c6d007ad7b002cbfe3f80b39d45146b5
  - packages/contracts/routes/ui-routes.json:65d7042b09b812d610281dd0ae43af275410bd57941179eb0e8d74d04556cb55
  - packages/contracts/routes/ui-route-contracts.json:f499e23ff8821261dda92b2a1d3d0c5e294008abe239f9e723e72ac73ab6e9d2
  - packages/contracts/routes/ui-surface-contracts.json:a12ac7170c859ad5dce563cbc212a58631d5c94c905830c980cde0a3f436d9f7
  - apps/web/src/App.tsx:3adc6f97f3db0275dbcda542db29b42e224beb57af0edd26a0ff35d7808f9542
  - apps/web/src/sales-overview-prototype/SalesOverviewPrototype.tsx:89b1359d5d6684eda0e6021adb408b91b179417965662202ca9c5e02a379f785
  - apps/web/src/sales-overview-prototype/sales-overview-prototype.css:435a4ca8989c370f8647ce5bb484f33b89acbb6516c865c7c7768dc5cf115a1e
  - docs/architecture/ui/custometry-linear-ui-migration-registry-v1.json:b3c228a4d83ca89f52a15a490e0f3aeaab4412058d01e8e48b74d673c0e70679
  - .codex/delivery/graphs/custometry-linear-workspace-ui-transition-v1.json:18e5e7e1cca968f89e9da29470d1f6077f34c0210df0409f553bb0352a01c178
  - .codex/delivery/evidence/W10-PENPOT-093-ORGANIZATION-PEOPLE-DELTA-IMPLEMENTATION.md:7fd8ffd7b11cd1c1bab1f26bae7f2864923cac1f65d39d87a73c417c4a5a7f30
  - .codex/delivery/evidence/W20-LINEAR-FRONTEND-ARCHITECTURE-SPIKE.md:c9d8e2003bb2136145bfbd4bf388aefe73ad93ad05460e9a1a3f66836e861dab
  - .codex/delivery/evidence/W27-UI-AN-003-HTML-CONTRACT-COMPLETION.md:39e5e7dd35211ffc38f3633783b7819990d53c77a97f0beabebb640db012652b
  - .codex/delivery/evidence/assets/W28-UI-AN-003-FIGMA-SYNCHRONIZATION/browser-reference-receipt.json:30ccec372fafb80542ad2e61ad32ef899828286fcfa8e8c8cdbf51a0b1703d21
  - packages/contracts/ui-design/ui-an-003.manifest.v1.json:edbf95b330f55fcac90c052ff61767b3fa69216fc216ab52d175877afba5c148
  - .codex/delivery/ui-design-programs/custometry-v1/g1-source-reconciliation.json:d1bccb9a0ac4201180b6ffcdf7a5e1488ccdcb60bc9e658c471225ebbdb6ca31
browser_receipts: []
responsive_web_anchors: []
mobile_scope: unauthorized
agent_self_acceptance: prohibited
---

# Owner review: G2 Journeys And Families

## What is being reviewed

- Exact program identity: `CUSTOMETRY-UI-DESIGN-PROGRAM-V1`, revision `3`, status `review`.
- Exact manifest validation profile: `structure_gate`.
- Accepted baseline retained: revision `2`, `atlas_gate`, with the unchanged hash-pinned G1 owner-decision reference and `accepted_revision: 2`.
- Atlas scope retained: 156 entries total; 151 `in_scope`, 2 `internal`, and 3 `excluded` historical entries.
- G2 scope: seven source-backed journey graphs, exact family and representative classification, coverage profiles, and design-wave assignments.
- Responsive-web anchors: intentionally unresolved; the responsive range remains `{min_width: null, max_width: null}` and `anchor_viewports` remains empty.
- Mobile-specific design: not authorized.

## Journey graph inventory

All 90 transitions resolve to exact transition identities under
`.codex/delivery/ui-design-programs/custometry-v1/g1-source-reconciliation.json`.
Empty alternate or external collections below are explicit source-backed zeroes,
not omitted fields.

| Journey | Entry | Intermediate | Alternate | Failure | Recovery | Terminal | External | Transitions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `JOURNEY-001` | 1 | 2 | 0 | 1 | 1 | 1 | 0 | 6 |
| `JOURNEY-002` | 1 | 12 | 2 | 1 | 1 | 1 | 0 | 18 |
| `JOURNEY-003` | 1 | 4 | 3 | 1 | 1 | 1 | 0 | 12 |
| `JOURNEY-004` | 1 | 3 | 4 | 1 | 1 | 1 | 0 | 13 |
| `JOURNEY-005` | 1 | 5 | 1 | 1 | 1 | 1 | 0 | 9 |
| `JOURNEY-006` | 1 | 5 | 2 | 1 | 2 | 1 | 0 | 13 |
| `JOURNEY-007` | 1 | 11 | 3 | 1 | 1 | 1 | 0 | 19 |

## Families, representatives, coverage, and waves

- Families: 61 total; 17 source-backed reuse hypotheses and 44 explicit `one_off` families.
- Representatives: 61; exactly one representative per family. `UI-AN-003` is the representative for its exact route-contract tuple because it is the only member with a declared measured baseline; other representatives use authoritative inventory order.
- Route family grouping uses only the exact tuple `family + surface_kind + state_profile + navigation_profile + query_profile`. It does not prove component reuse.
- Every registered overlay, route-backed transient, system layout, and persistent shell remains an explicit family when no accepted reuse evidence exists.
- Coverage profiles: 62. Every G2-owned state, role, locale, and theme dimension is source-backed or has an exact source-backed `not_applicable` reason.
- Locale coverage is `en|ru`; theme coverage is `abyss|graphite|frost|paper`.
- Every coverage profile declares `viewport_anchor_ids` with `mode: required`, `values: []`, `not_applicable_reason_ref: null`, normative G2 provenance, and `unresolved_fields: ["viewport_anchor_ids"]`.

| Wave | Gate | Screens | Families | Dependency |
|---|---|---:|---:|---|
| `WAVE-G3-SHELL` | `G3` | 4 | 4 | none |
| `WAVE-G4-REPRESENTATIVES` | `G4` | 57 | 57 | `WAVE-G3-SHELL` |
| `WAVE-G5-MVP` | `G5` | 52 | 12 | `WAVE-G4-REPRESENTATIVES` |
| `WAVE-G5-MVP-V1` | `G5` | 16 | 9 | `WAVE-G5-MVP` |
| `WAVE-G5-V1` | `G5` | 22 | 9 | `WAVE-G5-MVP-V1` |

These wave assignments define sequencing only. They do not execute or accept
G3, G4, or G5 and do not authorize frontend or design implementation.

## Automatic gates

| Gate | Evidence | Result |
|---|---|---|
| Source hash parity | All 17 `source_contracts` paths match their declared SHA-256 values | passed |
| Program contract and provenance | `validate_ui_design_program.py --profile structure_gate` | passed: 0 errors, 0 warnings |
| Journey reachability, exact transitions, failure recovery, and terminal checks | `structure_gate` semantic validation | passed |
| Family membership, representative parity, coverage assignments, and wave DAG | `structure_gate` semantic validation | passed |
| Geometry and overflow | No browser work authorized for G2 | not run; G4+ boundary |
| Raster comparison | No visual contract or accepted source revision is in G2 scope | not run; G4+ boundary |
| Accessibility and keyboard | No browser work authorized for G2 | not run; G4+ boundary |
| Console and network | No runtime work authorized for G2 | not run; implementation/browser boundary |

## Unresolved inventory and residual risks

- The only unresolved coverage field is `viewport_anchor_ids`: 62 occurrences, one per coverage profile. This is the required G2 deferral and must remain unresolved until G3 owner-authorized work.
- Responsive-web minimum, maximum, and anchor identities remain undefined. No responsive range or responsive-web anchor is implied by this review.
- Mobile scope remains `unauthorized`; no mobile screen, composition, viewport, or navigation model is authorized.
- The 17 multi-screen families remain reuse hypotheses until representative G4 contracts and evidence prove them. No component extraction or implementation is authorized by revision 3.
- The G1 owner-decision journal records accepted revision-2 manifest artifact SHA-256 `177ae8247f04eb7a1998041f30e49b0b79117a4b149b3d82a9a81c84b50ad817`, while the checked-in revision-2 manifest observed immediately before G2 had SHA-256 `fe639d3e7c17061333b0fedee9273bca752137b082ce05409428c3bda92e55a6`. The hash-pinned accepted identity receipt remains unchanged and valid for `{program_id, revision}`, but byte-for-byte replay of the accepted revision-2 manifest is not established by the current checkout.
- No browser, raster, accessibility, runtime, release, or implementation readiness claim is made.

## Exact owner decision

The owner chooses one and names the unchanged identity:

- `accept CUSTOMETRY-UI-DESIGN-PROGRAM-V1 revision 3 validation_profile structure_gate`
- `reject CUSTOMETRY-UI-DESIGN-PROGRAM-V1 revision 3 validation_profile structure_gate: <reason>`
- `request changes to CUSTOMETRY-UI-DESIGN-PROGRAM-V1 revision 3 validation_profile structure_gate: <bounded changes>`

No agent may fill or infer the owner decision. Revision 3 remains `review` until
an explicit owner decision is recorded in the owner-controlled decision journal.
