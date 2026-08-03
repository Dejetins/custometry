---
artifact_kind: ui_visual_proposal
proposal_id: CUSTOMETRY-G3-RESPONSIVE-WEB-ENDPOINTS-R1
status: proposal_for_owner_review
program_revision_ref: CUSTOMETRY-UI-DESIGN-PROGRAM-V1@3
target_screen_ids: []
candidate_artifacts: []
candidate_sha256: []
mobile_scope: unauthorized
provenance_eligibility: none_until_owner_acceptance
blocker_gate: G3
blocked_validation_profile: program_ready
---

# G3 responsive-Web endpoint proposal for owner review

## Resolved constraints

- Accepted baseline: `CUSTOMETRY-UI-DESIGN-PROGRAM-V1`, revision `3`,
  `validation_profile: structure_gate`, with owner-decision journal SHA-256
  `3ee4be0dfc6d1ef9a191165b0758645f66e58f39a4be6db72de8973985ae3053`
  and accepted value SHA-256
  `3a98719d7d75e6aa187d8a7ce4c67f5136a9c82eb8352b44f9faf28bed5bdf13`.
- Source parity: all 17 source paths declared by revision 3 match their pinned
  SHA-256 values.
- Product identities and shell profiles: the exact `auth`, `global`,
  `installation`, and `workspace` identities come from
  `packages/contracts/routes/ui-route-contracts.json#/routes/*/shell_profile`
  at SHA-256
  `f499e23ff8821261dda92b2a1d3d0c5e294008abe239f9e723e72ac73ab6e9d2`
  and are normalized at
  `.codex/delivery/ui-design-programs/custometry-v1/g1-source-reconciliation.json#/extension_screens/0..3`
  at SHA-256
  `d1bccb9a0ac4201180b6ffcdf7a5e1488ccdcb60bc9e658c471225ebbdb6ca31`.
- Existing source-backed foundations: shell composition and navigation are in
  `custometry-ui-blueprint-ru.md` sections 4.1 and 4.2; layout and density are
  in sections 5.1 and 5.2; theme, typography, assets, elevation, and motion are
  in sections 6.1 through 6.5. The source SHA-256 is
  `bca5441981a3956bb4a4433faa1beb24c6d007ad7b002cbfe3f80b39d45146b5`.
- Pilot boundary: W27 at SHA-256
  `39e5e7dd35211ffc38f3633783b7819990d53c77a97f0beabebb640db012652b`
  proves `UI-AN-003` and its observed workspace-shell states at `1440 x 900`
  and `1024 x 768`. It does not prove product-wide responsive-Web endpoints,
  the other shell profiles, or all 62 coverage profiles.
- Coverage state: all 62 profiles defer exactly `viewport_anchor_ids`; no
  other coverage field is unresolved.
- Mobile-specific design remains unauthorized. No mobile anchor, navigation,
  screen identity, or composition is proposed.
- Explicit non-goals: G4 through G6, screen contracts, frontend/design
  implementation, prompt pack, stage ledger, commit, and push.

## Blocking source finding

The allowed source contracts do not define both exact terminal endpoints of a
finite responsive-Web width range:

- `custometry-ui-blueprint-ru.md#51-master-viewport` declares behavior bands
  `<768`, `768-1023`, `1024-1279`, `1280-1439`, and `>=1440`. The first and
  last bands are open-ended, so they do not establish an exact minimum or
  maximum supported Web width.
- The same section states that `1440 x 900` is a visual-review master canvas,
  not a fixed runtime viewport. It therefore cannot supply the maximum
  endpoint.
- W27 and the UI-AN-003 manifest contain observed `1440 x 900` and
  `1024 x 768` pilot viewports. Those measurements are scoped to one accepted
  pilot and cannot supply product-wide endpoint provenance.
- The prototype CSS breakpoints at `1199`, `899`, and `720` are content
  adaptation thresholds for the pilot implementation, not supported-range
  endpoints.
- No allowed source supplies exact endpoint heights for the required minimum
  and maximum responsive-Web anchors.

Consequently, revision 4 cannot truthfully declare
`validation_profile: program_ready`, populate the 62 `viewport_anchor_ids`, or
remove their unresolved token until an exact owner decision is hash-pinned.
The accepted revision 3 manifest remains unchanged.

## Candidate set

No numeric candidate is proposed because choosing one would invent the missing
contract. The owner decision must provide either an already-authoritative
contract pointer or exact values for all fields below.

| Candidate | Exact artifact | SHA-256 | Deliberate differences | Unresolved decisions |
|---|---|---|---|---|
| `OWNER-SPECIFIED-RESPONSIVE-WEB-ENDPOINTS` | A new owner decision recorded separately in `owner-decision-journal.json` | Pending owner decision | Promotes only the exact finite Web range and its two endpoint anchors; preserves `mobile_scope: unauthorized` | `min_width`, `max_width`, minimum `anchor_id`/`height`, maximum `anchor_id`/`height`, and below/above-range policy |

The decision payload must name the exact program and G3 boundary and provide a
shape equivalent to:

```json
{
  "program_id": "CUSTOMETRY-UI-DESIGN-PROGRAM-V1",
  "gate_id": "G3",
  "supported_web_width_range": {
    "min_width": "<exact positive integer CSS px>",
    "max_width": "<exact integer CSS px greater than min_width>"
  },
  "anchor_viewports": [
    {
      "anchor_id": "<exact minimum responsive-Web anchor ID>",
      "width": "<same exact min_width>",
      "height": "<exact positive integer CSS px>",
      "class": "responsive_web"
    },
    {
      "anchor_id": "<exact maximum responsive-Web anchor ID>",
      "width": "<same exact max_width>",
      "height": "<exact positive integer CSS px>",
      "class": "responsive_web"
    }
  ],
  "below_range_policy": "<exact Web behavior below min_width>",
  "above_range_policy": "<exact Web behavior above max_width>",
  "mobile_scope": "unauthorized"
}
```

## Promotion rule

This proposal is non-normative and cannot be cited as `accepted_visual`,
`owner_decision`, a token source, a component contract, or implementation
authority. Only an explicit owner decision naming the exact range, both exact
anchor identities and dimensions, and `mobile_scope: unauthorized` may promote
those values. Record that decision separately; never rewrite this proposal
into an acceptance receipt.
