---
artifact_kind: ui_design_owner_review
program_id: CUSTOMETRY-UI-DESIGN-PROGRAM-V1
gate_id: G3
validation_profile: program_ready
review_revision: 4
accepted_baseline_revision: 3
accepted_baseline_validation_profile: structure_gate
accepted_baseline_owner_decision_ref: owner-decision://3ee4be0dfc6d1ef9a191165b0758645f66e58f39a4be6db72de8973985ae3053/.codex/delivery/ui-design-programs/custometry-v1/owner-decision-journal.json?value_sha256=3a98719d7d75e6aa187d8a7ce4c67f5136a9c82eb8352b44f9faf28bed5bdf13#/iterations/1/owner_decision
accepted_baseline_manifest_sha256: 22632c142a6c67ef73116bbb448b4da64f165bbb9b1da7d7edb301b1ede03871
manifest_sha256: 9ef53c33260421a8d1131c0b2caef0649ffb666de130bd4fb0990ed1081c8880
responsive_owner_decision_receipt: .codex/delivery/ui-design-programs/custometry-v1/g3-responsive-web-range-owner-decision.json
responsive_owner_decision_receipt_sha256: 5f4693b0f1ff330fff4ec8220ddccbb9e3a34bff451e5d533b298327b4e20036
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
  - .codex/delivery/ui-design-programs/custometry-v1/g3-responsive-web-range-owner-decision.json:5f4693b0f1ff330fff4ec8220ddccbb9e3a34bff451e5d533b298327b4e20036
  - .codex/delivery/ui-design-programs/custometry-v1/g1-source-reconciliation.json:d1bccb9a0ac4201180b6ffcdf7a5e1488ccdcb60bc9e658c471225ebbdb6ca31
browser_receipts: []
responsive_web_anchors:
  - web-min-768:768x900
  - web-standard-1440:1440x900
  - web-wide-1920:1920x1080
  - web-max-2560:2560x1440
mobile_scope: unauthorized
agent_self_acceptance: prohibited
---

# Owner review: G3 Foundations And Shell

## What is being reviewed

- Exact program identity: `CUSTOMETRY-UI-DESIGN-PROGRAM-V1`, revision `4`,
  status `review`, `validation_profile: program_ready`.
- Accepted baseline retained: revision `3`, `structure_gate`, with unchanged
  hash-pinned G2 owner-decision evidence and `accepted_revision: 3`.
- G3 scope: source-backed foundation, application-shell, typography, density,
  asset, layout, and responsive-Web decisions only.
- Product capabilities, routes, roles, permissions, states, copy, and business
  semantics remain referenced from their authoritative sources; revision 4
  does not restate them as a new independent product contract.
- No screen contract, frontend/design implementation, prompt pack, stage
  ledger, commit, or push is included.

## Foundation and application-shell decisions

These rows confirm source ownership and G3 boundaries. They do not create a
second token, component, route, or product-semantics registry.

| Area | Confirmed decision boundary | Provenance |
|---|---|---|
| Visual foundation | Calm, analytical, data-dense Web workbench; semantic four-theme target `abyss|graphite|frost|paper` | `custometry-ui-blueprint-ru.md` §§2.3, 6.1 and `custometry-technical-blueprint-ru.md#THEME-001`, hashes pinned above |
| Application shell | Preserve four exact shell identities `auth`, `global`, `installation`, and `workspace`; permission-aware navigation and shell regions remain source-owned | `packages/contracts/routes/ui-route-contracts.json#/routes/*/shell_profile`, G1 reconciliation `/extension_screens/0..3`, and UI blueprint §§4.1–4.2 |
| Typography | Self-hosted versioned `Inter Variable`, system fallbacks, exact type scale, en/ru coverage, 200% zoom requirement, and no table text below 12 px | `custometry-ui-blueprint-ru.md` §6.2 |
| Density | Source-owned compact reporting hierarchy, 4 px base spacing, declared gaps/control sizes, 12-column content grid, and first-viewport data priority | `custometry-ui-blueprint-ru.md` §5.2 and `custometry-technical-blueprint-ru.md#UI-DENSITY-001` |
| Assets | Pinned `lucide-react` as the v1 core icon family, accessible icon-label rules, text-only `Custometry` wordmark until an official SVG, and source-owned BrandProfile constraints | `custometry-ui-blueprint-ru.md` §6.3 |
| Layout constraints | No page-level horizontal scroll; dense tables, timelines, and canvases may use deliberate local scroll; logical properties and content-driven adaptation remain required | `custometry-ui-blueprint-ru.md` §5 and responsive policy §§Viewport Contract, Breakpoints And Components |

The G3 artifact confirms these decisions by reference. It does not claim that a
production font bundle, token package, component library, or browser shell has
already been implemented or loaded.

## Accepted and measured pilot boundary

- W27 is the only accepted current visual pilot and remains scoped to
  `UI-AN-003` plus the workspace-shell states it actually exercises.
- The pilot proves observed `1440 x 900` and `1024 x 768` behavior only. It does
  not prove the new `768`, `1920`, or `2560` anchors and does not prove the
  `auth`, `global`, or `installation` shell families.
- The pilot implementation hashes remain exact measured/accepted inputs, but
  they are not promoted into whole-product component reuse or global runtime
  readiness.

## Responsive-Web range and anchors

The owner decision receipt explicitly authorizes a finite mandatory validation
range of `768..2560` CSS px. Widths below `768` and above `2560` are outside the
mandatory validation range. Below-range behavior is not mobile authorization.

| Anchor ID | Width | Height | Class | Provenance value SHA-256 |
|---|---:|---:|---|---|
| `web-min-768` | 768 | 900 | `responsive_web` | `4cea0db7a44380c2c23fa6d7bd31463853bcba35f1509b2e7129cc730cf9f3bd` |
| `web-standard-1440` | 1440 | 900 | `responsive_web` | `33bb42a8ca1a27949510aee03228164b324d32a7b5dd2a912d7dab2a9cfdc85f` |
| `web-wide-1920` | 1920 | 1080 | `responsive_web` | `bbbdfc499f214a457c9177c57f420514a63c9b0f610a35a6ac59f4d037a76dc8` |
| `web-max-2560` | 2560 | 1440 | `responsive_web` | `a6f540b9321dba11cac5637d26319e237c39190f7139c7bf35dcf41822ef3178` |

- Range value SHA-256:
  `660e7441a18cae9dba4844c1436209d8ef2c21bc5c4655d34f32d6d6dc7047de`.
- Ordered coverage-anchor list SHA-256:
  `3b7d24eba21fd25f3394f10900a16a1f1d7f8a0bd4aba4157ea367a2c0733684`.
- Every material responsive value points to the exact receipt SHA-256 and the
  matching canonical value hash.

## Coverage and mobile inventory

- Coverage profiles: `62`.
- Profiles containing all four responsive-Web anchors: `62`.
- Profiles containing both exact endpoints: `62`.
- Remaining unresolved coverage fields: `0`.
- Mobile scope: `unauthorized`.
- Mobile anchors, mobile navigation, mobile screen identities, and
  mobile-specific composition: `0`.

## Automatic gates

| Gate | Evidence | Result |
|---|---|---|
| Source hash parity | All 18 `source_contracts` paths match their declared SHA-256 values | passed |
| Contract, provenance, and exact owner-value pins | `validate_ui_design_program.py --profile program_ready` | passed: 0 errors, 0 warnings |
| Coverage endpoint inclusion | 62 profiles contain `web-min-768` and `web-max-2560`, plus the two declared intermediate anchors | passed |
| Geometry and overflow | No new browser work authorized for G3 | not run; G4+ evidence boundary |
| Raster comparison | No screen contract created in G3 | not run; G4+ evidence boundary |
| Accessibility and keyboard | No browser screen acceptance performed in G3 | not run; G4+ evidence boundary |
| Console and network | No runtime work performed in G3 | not run; implementation/browser boundary |

## Known exclusions and residual risks

- Revision 4 is `review`, not accepted. The responsive-value decision is not a
  G3 program-gate acceptance.
- No newly declared anchor has browser/raster evidence at G3. Each G4 screen
  contract must later prove its exact declared anchor set.
- The Inter Variable production bundle, license metadata, semantic token
  package, and reusable component assets are source-backed requirements, not
  implemented or browser-loaded evidence in this stage.
- W27 cannot be generalized beyond `UI-AN-003` and its observed workspace-shell
  values. The other three shell profiles still require their own downstream
  screen contracts and evidence.
- The 17 multi-screen families remain reuse hypotheses until representative G4
  contracts and evidence prove them.
- No browser, raster, full accessibility, runtime, API, authorization,
  persistence, performance, release, or deployment readiness claim is made.

## Exact owner decision

The owner chooses one and names the unchanged identity:

- `accept CUSTOMETRY-UI-DESIGN-PROGRAM-V1 revision 4 validation_profile program_ready`
- `reject CUSTOMETRY-UI-DESIGN-PROGRAM-V1 revision 4 validation_profile program_ready: <reason>`
- `request changes to CUSTOMETRY-UI-DESIGN-PROGRAM-V1 revision 4 validation_profile program_ready: <bounded changes>`

No agent may fill or infer the owner decision. Revision 4 remains `review`
until an explicit owner decision is recorded without rewriting the accepted
revision-3 evidence.
