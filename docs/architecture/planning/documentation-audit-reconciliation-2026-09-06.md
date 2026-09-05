---
doc_id: DOC-AUDIT-RECONCILIATION-2026-09-06
title: Documentation audit reconciliation
doc_version: 1
product_spec_version: 0.10.0-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: [DOC-RULE-008]
status: active
proof_boundary:
  label: documentation-reconciliation-evidence
  exclusions: [runtime-readiness, release-readiness]
---

# Documentation audit reconciliation

## Authority and scope

On 2026-09-06 the user accepted the comparative review of the PRO and ULTRA
documentation audits and requested all necessary corrections. This record carries
that selection, the later publication clarification, and their resulting evidence; execution status belongs only
to `W31-RECONCILE-DOCUMENTATION-AUDITS`.

Both archives contain the same 21 original documents; their 20 substantive
project documents match the pre-edit working checkout. PRO records 22 findings,
97 applied operations and 16 proposals; ULTRA records 32 findings, 102 applied
operations and 18 proposals. Findings overlap. The initial local-baseline review accepted 85 bounded
operations, required rewriting/splitting 51, and rejected importing 63; these
are not independent defects or a runnable patch list. The publication disposition
below incorporates the subsequent explicit decision to preserve accepted `main`
authority; the initial operation counts are historical review classification.

Input archive SHA-256:

- PRO: `b5390ce65715577fb72bd30f493985e6db5d80051e0707f630b27c3cc8dc2ba6`.
- ULTRA: `0bfe5391366f1be2f10c219c89c7d9c6153a08d7ba6b3790402c1063f0b60351`.

## Accepted correction boundary

Correct YAML, route counts, v1 acceptance coverage, accepted frontend technology,
retired workflow prerequisites, ownership/public ports, temporal and grain
semantics, certification/provenance, mode-dependent comparison labels, role/grant
semantics, finite cross-department expiry, cancellation/artifact consistency,
Notifications egress, offline/cleanup scope, motion and historical/current claims.
Repair current human-mirror RBAC and deny-aware dashboard summaries. Complete
the registry for already-required artifact formats and method metadata placement.

Before publication, the remote `main` base was verified as
`d5ecbd33c1fd582058ec3514e2084820c8a3f1c2`. The local audit checkout was based on
`80cd0976c434b6db62d3e415bc638cbe4a9468c2` and did not contain the later published
UI authority and implementation. The user explicitly selected preservation of
already accepted `main` decisions. Therefore the final target pilot remains
authority for its demonstrated composition, navigation, analytical interactions,
and visual language; ADR-0007 and the active Web implementation source contract
retain their published technology, rollout and endpoint/risk-based proof rules.
The prior visual-language-only limitation and mandatory four-anchor proof
reinterpretation are not published. The G-program remains retired, and the
existing Web frontier and ticket status sources remain. Archive missing-source
caveats do not replace the sources actually available at the publication base.

The full audited documents also include 100 previously accepted local product
requirement IDs absent from that remote base: both machine and human grow from
1141 to 1241 IDs without losing upstream IDs. Their authoring/source-adaptation
contracts, comparative research, revision-bound coverage evidence and paired
surface requirement bindings are included as the necessary source closure.
This publication is the corrected document set, not only patch hunks relative
to the uncommitted local audit baseline. Existing application code, API/schema
payloads, migrations, executable route identities, permissions and pilot bytes
are preserved.

PVM, shared-consumer cancellation, endpoint revocation and TLS/Edge need concrete
bounded contract proposals. They do not authorize invented policy values or a
claim that dependent implementation is complete. Forecasting remains on hold;
the first external release remains unselected.

## Final finding disposition

The tables cover all 54 audit records, including overlaps. `corrected` is a
documentation result, not implementation acceptance. The four proposal rows
remain unaccepted behavioral choices and do not claim full normative closure.
Source-level compatibility work is explicitly separate from document correction.

### PRO

| Finding | Disposition | Concrete outcome |
|---|---|---|
| F-001 | corrected | Nine exact scalar-quoting repairs; all machine fences parse. |
| F-002 | corrected | Published ADR-0007 platform, pins, ownership, rollout and active proof policy preserved; unshown details remain ticket-scoped. |
| F-003 | resolved against current main | Retired program stays retired; accepted target-pilot composition/interactions and published rollout/proof rules preserved. |
| F-004 | archive limitation resolved | Current human mirror used; local semantic RBAC/dashboard drift repaired. No missing-mirror caveat imported. |
| F-005 | corrected | M11 includes V1-AC-001 through V1-AC-067; N0/N3/N4 and TEST-INV-113 through 122 allocation explicit. |
| F-006 | corrected | Current 117/25/5/22 counts; historical W10 116/25/5 retained. |
| F-007 | corrected | Foundation tree/impact/scaffold evidence explicitly historical; current layout conventions and sources retained. |
| F-008 | corrected | Accepted logical owner summaries and target modules synchronized; no physical context migration claimed. |
| F-009 | corrected | Public owner ports/DTOs/projections replace private cross-context repository wording. |
| F-010 | corrected | Table-first/pivot-first reports need no mandatory chart or KPI strip. |
| F-011 | corrected | Display labels derive from applied modes/axes; no-comparison suppresses label; v1 legacy compact_label wire shape preserved. |
| F-012 | corrected; implementation proof deferred | Required nine-token format registry completed with MIME mapping and reader-first compatibility contract. |
| F-013 | corrected | DATA-RULE-010 and TEST-INV-011 distinguish historical temporal joins from disclosed current-only bindings. |
| F-014 | corrected | UNIT-ECON-012 uses common certification axis, separate origin/quality; no automatic proxy reclassification or promotion. |
| F-015 | clarified | Existing combined-authority issuer and grant ceiling retained; no new delegation privilege. |
| F-016 | corrected | Data Guide actor requires explicit data_guide.publish; no automatic default grant. |
| F-017 | target corrected; migration deferred | Finite expiry follows RESOLVED-040/V1-AC-040; existing nullable API/persistence incompatibility is explicit. |
| F-018 | corrected | Operating model separates normative sources from implementation evidence under current AGENTS precedence. |
| F-019 | corrected where material | Architecture existence no longer proves consistency; revision-bound history and actual observations preserved. |
| F-020 | archive limitation resolved | Actual current manifests/catalogs used and validated; archive absence caveats rejected. |
| F-021 | proposal prepared; policy unaccepted | TLS-only Edge credential exception and external-termination alternative concretely specified; current SEC rules not silently superseded. |
| F-022 | corrected | Canonical route-family count changed from three to four. |

### ULTRA

| Finding | Disposition | Concrete outcome |
|---|---|---|
| ROOT-F001 | corrected | Nine exact scalar-quoting repairs; all machine fences parse. |
| ROOT-F002 | corrected local defects / archive limitation resolved | Current mirror RBAC-012/013/014/015 and DASHBOARD-011 summaries synchronized; all 1241 IDs retained. |
| F-DATA-001 | corrected | DATA-RULE-010 and TEST-INV-011 distinguish historical temporal joins from disclosed current-only bindings. |
| F-DATA-002 | corrected | UNIT-ECON-012 uses common certification axis, separate origin/quality; no automatic proxy reclassification or promotion. |
| F-DATA-003 | corrected | Receipt aggregates retain compatible dimensions/grain; item metrics do not duplicate header totals. |
| F-DATA-004 | corrected | External source-input row follows accepted SQL/CSV/XLSX envelope; internal Parquet artifacts remain supported. |
| AN-001 | corrected | Display labels derive from applied modes/axes; no-comparison suppresses label; v1 legacy compact_label wire shape preserved. |
| AN-002 | corrected | Product analytics is part of Analytics; Digital Journey & Marketing Measurement remains a separate context. |
| AN-003 | corrected | Segment definition methods separated from stratified DistributionArtifact and explicit saved-segment lifecycle. |
| AN-004 | proposal prepared; attribution unaccepted | Exact PVM formulas, root portfolio, drilldown allocation, coverage policies and rational numeric example provided. |
| SE-001 | corrected | Accepted logical owner summaries and target modules synchronized; no physical context migration claimed. |
| SE-002 | corrected | Dashboard/report ACL management uses the corresponding administrative permission; MAY preserved. |
| SE-003 | corrected | No post-fencing publication; committed cancelled-attempt outputs retain orphan/retention handling and declared successful partial branches. |
| SE-004 | corrected | CSV summary follows existing SEC-004 MUST with reversible escaping. |
| SE-005 | clarified | Existing combined-authority issuer and grant ceiling retained; no new delegation privilege. |
| SE-006 | proposal prepared; last-interest policy unaccepted | Durable participation vs operator cancellation, race ordering, fencing and reconnect specified; last-interest alternatives explicit. |
| AUD-OPS-002 | corrected | Operating model separates normative sources from implementation evidence under current AGENTS precedence. |
| AUD-OPS-003 | corrected | Notifications-owned v1 email/HTTPS-webhook egress appears in machine/runtime/system design; public MVP remains in-app-only. |
| AUD-OPS-004 | archive caveats rejected; history clarified | No generic missing-source paragraph imported into live contracts; actual Foundation history and proof limits scoped. |
| AUD-OPS-005 | corrected | Local offline reading separated from first acquisition/install/bootstrap. |
| AUD-OPS-006 | corrected | Repository cleanup allowlist distinguished from target installation-owned lifecycle; deletion authority unchanged. |
| PLAN-F001 | corrected | M11 includes V1-AC-001 through V1-AC-067; N0/N3/N4 and TEST-INV-113 through 122 allocation explicit. |
| PLAN-F002 | corrected | Discovery supplies research/optional proposals; accepted blueprint and authoring contract own adopted requirements. |
| PLAN-F003 | corrected | Historical development audit and research have narrow current-use notes, preserving recorded observations and hold. |
| UI-F01 | corrected | Current 117/25/5/22 counts; historical W10 116/25/5 retained. |
| UI-F02 | corrected | Published ADR-0007 platform, pins, ownership, rollout and active proof policy preserved; unshown details remain ticket-scoped. |
| UI-F03 | resolved against current main | Retired program stays retired; accepted target-pilot composition/interactions and published rollout/proof rules preserved. |
| UI-F04 | corrected | Normative motion tokens/durations retained; measured journey budgets and implementation proof distinguished. |
| UI-F05 | corrected | Section 4.5 moved under section 4 without changing its anchor or IDs. |
| UI-F06 | current main confirmed by user | Published target-pilot and active endpoint/risk-based proof authority retained; earlier local reversal excluded. |
| F-DATA-006 | corrected; consumer proof deferred | availability_class/method_family moved from PromotionVersion to AnalysisMethodVersion; narrow source search and future schema migration limits recorded. |
| SE-007 | proposal prepared; security semantics unaccepted | Security revoke/normal rotation, durable dispatch-admission cutoff, queued/retry and unknown outcomes concretely specified. |

## Contract compatibility

The applied source change is documentation plus surface requirement-binding,
capability-label and rationale metadata. No application code, API handler,
executable API/schema payload, database migration, route identity/permission,
renderer, runtime configuration or secret changed. The metadata update is a
`compatible-change`: existing IDs and executable surface behavior are retained. Target-contract consistency and future
implementation compatibility are distinct:

| Boundary | Classification / evidence | Required later action |
|---|---|---|
| v1 Focus `compact_label` | `compatible-change`: existing `vs_LY`/null serialization retained; displayed labels derive from effective comparison specs, including no-comparison and stale-hint guard | Any future expanded enum/localization-key serialization needs versioned reader/writer migration |
| Generic artifact vocabulary | Old five-token spelling/meaning preserved; `breaking-change` for an old closed-enum reader receiving svg/png/xlsx/markdown; actual consumer matrix `unknown` | Reader-first schema qualification under the [artifact format contract](../../contracts/artifact-format-contract.md) before new writer activation |
| CrossDepartmentGrant target expiry | `breaking-change` relative to the existing nullable-expiry API/application/persistence interaction if enforced; this task changes only its documented target | Inventory and handle existing no-expiry grants, API/DB consumers and rollback before enforcing finite expiry; no arbitrary TTL |
| Promotion/AnalysisMethod fields | Corrected target schema placement; compatibility `unknown` for external/persisted consumers, no match in bounded apps/packages/tests symbol search | Verify actual consumers and version/migrate any existing incorrect representation; no silent reinterpretation |
| Other settled target clarifications | Restore existing accepted requirements, owner boundaries and normative modality; implementation support remains outside this task | Provider/consumer tests at the actual implementing boundary; no behavior proof from ID parity |
| Four new behavioral contracts | `proposed`, with per-interaction compatibility and adoption seams in the [contract proposals](./audit-contract-decisions-2026-09-06.md) | Accept only the bounded economic/resource/security decisions, then synchronize their named normative clauses before implementation |

Publication-base source inspection confirms existing batch/Parquet ArtifactManifest
readers/writers and persisted records, run-scoped Execution cancellation, and
in-app Notifications. The [artifact contract](../../contracts/artifact-format-contract.md)
and [proposals](./audit-contract-decisions-2026-09-06.md) describe those implemented
seams and the remaining extensions. No placeholder-only claim is made about
Execution, Notifications or Artifact Lifecycle. Exact `compact_label` and
Promotion/AnalysisMethod schema symbols were not found in the bounded source
search; comparison consumers do exist in `analytics_core` and Web.

The finite-expiry drift is evidenced by
`packages/identity_access/application/organization.py` accepting `expires_at: datetime | None`,
its non-null-only validation, the API router optional field and persistence read/write path.
The existing grant-ceiling path is evidenced by
`packages/identity_access/domain/policy.py` and `application/service.py`;
`workspace_owner` combines admin and analyst grants. These are source observations,
not a live authorization or database test.

## Validation and observed evidence

- All 1241 audited machine/human stable IDs and `spec_version: 0.10.0-draft` were preserved; all 1141 publication-base IDs remain.
  Both `updated_at` fields became 2026-09-06; semantic corrections were reviewed
  by ID, beyond what the representation validator proves.
- All 223 machine YAML fences parse with duplicate-key rejection; the wider
  checked documentation corpus has 224 YAML/JSON fences with zero parse errors.
- Route validation passed: 117 routes/contracts, 25 overlays, five system
  surfaces, 22 capabilities and 29 use-case bindings. Pilot metadata/IDs,
  target-pilot authority and the published ADR/source-contract proof policy were preserved.
- The proposed PVM example was verified with exact rational arithmetic:
  volume 30 + mix -6 + price 30 + assortment 11 + residual 1 = observed delta 66;
  atomic and parent totals reconcile. This is proposal algebra, not product code.
- Independent QA found and corrected one remaining adjacent contradiction: the
  Result Trust trigger is present on every result view; only its opened panel
  is on demand, consistent with the existing machine requirement.
- Both generated documentation/requirement indexes were regenerated with the
  existing repository toolchain and checked by the local profile.

The original local-baseline correction passed the pinned locked/offline
`tools.check --scope local` profile. That evidence does not establish publication
readiness of the newer remote base. The isolated publication branch uses the
current `main` code and its pinned toolchain; exact final source/static results,
independent review and revision limits are recorded in
[W31 evidence](../../../.codex/delivery/evidence/W31-RECONCILE-DOCUMENTATION-AUDITS.md).
GitHub's required `Foundation gate` is a separate observed publication boundary.
Static checks do not certify application, API/database, browser/accessibility,
security enforcement, recovery, performance, hosted CI, release or deployment.

## Remaining bounded work

The [four completed proposals](./audit-contract-decisions-2026-09-06.md) specify
PVM attribution/root-preserving drilldown; consumer/global cancellation and
last-interest resource policy; endpoint security-revoke dispatch semantics;
and TLS-only Edge custody versus external termination. They are ready for the
specific policy selections, not silently accepted production contracts.

Source readiness/tolerance/freshness/customer-identity values, workload/SLO,
privacy retention/suppression, and unresolved font/theme/asset registry values
remain scoped inputs to their affected implementation/qualification. No numbers
or new default permissions were invented. Forecasting remains on hold and the
first external release stays unselected. The next execution must use the current
user request or a ready ticket for its actual boundary; this report creates no
standing program or automatic implementation authority.
