---
artifact_kind: delivery_evidence
delivery_contract: global/v1
delivery_schema_version: 1
spec_version: 0.9.3-draft
ticket_id: W08-PENPOT-ANALYTICS-BASELINE-RECOVERY
proof_boundary: canonical-penpot-analytics-baseline-recovery-after-revision-181
proof_skills: ["product-design:audit"]
verdict: passed
penpot_file_id: 7cd71457-8d32-8044-8008-549f83bb4645
penpot_start_revision: 185
penpot_end_revision: 191
repository_fingerprint: 99beedc35b6df55ca0e7d1391118e8477aa5638e630e17b55af2aa1fff2baa49
redaction: No credentials, customer data, Penpot document payloads, browser state, or environment dumps were retained.
executed_checks:
  - confirm canonical Penpot file ID and exact revision 185 before the first design write
  - confirm serial revision guards remain stable and compute the ordered context_sources SHA-256 fingerprint before the first design write
  - restore stable route frame UI-AN-002 from accepted W08 metadata and design structures
  - repair UI-AN-011 inside its existing Configuration and right-rail regions
  - individually export and visually review UI-AN-002 and UI-AN-011 after the final design write
  - confirm exactly 110 route frames, 25 overlay frames, and 5 system surfaces with no duplicate missing or orphan UI-ID
  - confirm Penpot currentFile.validate returns no errors
  - repeat the identical ordered context_sources fingerprint immediately before repository baseline-reference updates
  - uv run python -m tools.custometry_quality.validate_blueprints
  - uv run python -m tools.custometry_quality.validate_route_registry
  - uvx check-jsonschema --schemafile packages/contracts/routes/ui-route-contracts.schema.json packages/contracts/routes/ui-route-contracts.json
  - uvx check-jsonschema --schemafile packages/contracts/routes/ui-surface-contracts.schema.json packages/contracts/routes/ui-surface-contracts.json
  - uv run python -m tools.custometry_quality.validate_delivery_tickets
  - uv run python -m tools.custometry_quality.check_docs_links
  - uv run python -m tools.custometry_quality.generate_docs_index --check
  - source scripts/activate-toolchain.sh && uv run --locked python -m tools.check --scope local
  - git diff --check
observations:
  - Canonical Penpot file 7cd71457-8d32-8044-8008-549f83bb4645 moved from unexpected drift revision 185 to recovery terminal revision 191.
  - Historical W08 acceptance at revision 181 and its ticket/evidence remain unchanged.
  - Stable-ID reconciliation found exactly 110 routes, 25 overlays, and 5 system surfaces; duplicate, missing, and orphan lists were empty.
  - The repeated ordered repository fingerprint was 99beedc35b6df55ca0e7d1391118e8477aa5638e630e17b55af2aa1fff2baa49 before the separately authorized repository baseline-reference updates.
---

# W08-PENPOT-ANALYTICS-BASELINE-RECOVERY Evidence

> Compact evidence for one terminal recovery ticket. It records a new
> canonical baseline and does not rewrite historical W08 acceptance.

## Outcome and scope

- outcome: the canonical Penpot file again contains stable route frame
  `UI-AN-002`, and `UI-AN-011` presents its accepted W08 configuration,
  MetricGroup availability, cap, and table-preview content without a covering
  overlay;
- requirement IDs: [UC-027, METRIC-014, METRIC-015, DISCOUNT-017,
  DISCOUNT-018, V1-AC-021, V1-AC-034];
- included: only `UI-AN-002`, `UI-AN-011`, their nested design content, the
  separate recovery records, and current baseline references in the UI
  blueprint, UI surface contract, and ready W10 ticket;
- exclusions: W10 was not executed. Product scope, route identity, machine and
  human blueprints, architecture, executable contracts, permissions, and
  W05-W08 historical artifacts were not changed. This proves Penpot design
  implementation only and does not prove browser/runtime behavior,
  accessibility runtime, calculation correctness, export generation,
  authorization, deployment, or release readiness.

The recovered composition preserves Frost, W06 compact density, ordered
MetricGroup presentation, compact Result Trust semantics, and all existing
stable UI-ID strings. The product contract is unchanged.

## Recovered Penpot surfaces

- `UI-AN-002 — Guided analysis setup`: restored stable route board
  `33a2a659-d0eb-80bd-8008-5b0f986e2a90` on page `24 Analytics`, 1440 by 900.
  The reconstruction used the accepted W08 board metadata and retained W08
  helper structures stored in the canonical file; it was not an approximate
  replacement. Analysis identity remains in Configuration, while capability
  preflight and continuation use the existing validation/right-rail regions.
- `UI-AN-011 — Custom Builder`: existing stable route board
  `e451483d-aae3-807d-8008-54a9bbc4981f` was retained. Builder pins remain in
  Configuration; availability, cap, and table preview remain in the existing
  right rail. No full-width methodology layer covers Configuration or Metric
  groups.

## Final visual QA verdicts

| Board/frame | Final visual verdict |
| --- | --- |
| UI-AN-002 | pass — fresh individual export after the final write is unclipped and overlap-free; shell, stepper, Configuration, capability preflight, continuation, badges, alignment, and compact density are readable. |
| UI-AN-011 | pass — fresh individual export after the final write is unclipped and overlap-free; Configuration remains primary, Metric groups stay visible, and cap/table preview rows and non-color-only statuses fit in the existing right rail. |

The two `READY` chips in the primary Configuration column were normalized to
the same 92 px width and `parentX: 628` left guide as `DIRECT` and `DERIVED`.
Their final individual export shows one consistent status-column alignment.

One Penpot export response transiently omitted right-edge layers from
`UI-AN-011`; the immediately repeated individual export rendered the complete
frame, while the structural inspection independently confirmed every affected
child inside its parent bounds. The accepted visual verdict uses the complete
fresh export and the matching structural evidence.

## Commands and observations

| Command or action | Result | Redacted observation / durable reference |
| --- | --- | --- |
| Initial Penpot guard | pass | File ID matched; serial reads remained exactly revision 185 before the first write. Penpot MCP was available. |
| Ordered fingerprint, before and after design work | pass | `99beedc35b6df55ca0e7d1391118e8477aa5638e630e17b55af2aa1fff2baa49` both times, repeated before the authorized repository baseline-reference updates. |
| Accurate `UI-AN-002` recovery | pass | Accepted W08 metadata identified the missing stable board and its 1440 by 900 analytics structure; retained W08 helpers supplied the existing Frost/W06/W08 design grammar. |
| `UI-AN-011` overlap repair | pass | W08 content is integrated into existing Configuration and right-rail regions; no covering layer remains. |
| Product Design visual audit | pass | Individual post-write exports of `UI-AN-002` and `UI-AN-011` passed clipping, overlap, alignment, hierarchy, and density review. |
| Stable-ID reconciliation | pass | Penpot contains 110 route, 25 overlay, and 5 system IDs; duplicate, missing, and orphan lists are empty. The six W10 backlog identities remain unimplemented. |
| Penpot file validation | pass | `currentFile.validate()` returned no errors at terminal revision 191. |
| Configuration status alignment | pass | Both `READY` chips use the same 92 px width and left guide as the other status chips. |
| Terminal revision guard | pass | Two serial reads remained revision 191 with the canonical file ID. |
| `uv run python -m tools.custometry_quality.validate_blueprints` | pass | Observed 941 requirement IDs and product spec `0.9.3-draft`. |
| `uv run python -m tools.custometry_quality.validate_route_registry` | pass | Observed 116 contract routes: 110 Penpot baseline and 6 Penpot backlog; 25 overlays and 5 system surfaces. |
| Both JSON Schema checks | pass | Route and surface contract documents validate against their repository schemas. |
| `uv run python -m tools.custometry_quality.check_docs_links` | pass | Checked 42 documents and 91 local links. |
| `uv run python -m tools.custometry_quality.generate_docs_index --check` | pass | Generated documentation index is current. |
| `uv run python -m tools.custometry_quality.validate_delivery_tickets` | pass | Terminal recovery ticket/evidence and the ready W10 frontier validate together. |
| `source scripts/activate-toolchain.sh && uv run --locked python -m tools.check --scope local` | pass | Grouped local repository gate passed; no broader runtime or release proof is inferred. |
| `git diff --check` | pass | No whitespace errors. |

## Verdict

`passed`. Revision `191` is the current canonical Penpot baseline after the
revision-185 post-acceptance recovery. W08 remains historically accepted at
revision `181`; its ticket and evidence were not rewritten. W10 remains
`ready`, now guarded by revision `191`, and was not executed. Residual risk is
limited to the declared design-only proof boundary.
