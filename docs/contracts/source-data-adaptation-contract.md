---
doc_id: CONTRACT-SOURCE-DATA-ADAPTATION-001
title: Source data adaptation and imperfect snapshot refresh contract
doc_version: 1
product_spec_version: 0.10.0-draft
visibility: internal
ship: false
owner: architecture
requirement_ids: [IDENTITY-006, IDENTITY-007, IDENTITY-008, DATA-MAP-001, DATA-MAP-007, INGEST-008, INGEST-020, DQ-INPUT-001, DQ-INPUT-008, TEST-INV-113, TEST-INV-122, V1-AC-063, V1-AC-067]
status: accepted
acceptance_basis: owner-approved-source-data-requirements-2026-09-05
proof_boundary:
  label: target-requirements-and-acceptance-allocation
  exclusions: [implemented-api-schema, persistence-migration, source-readiness-proof, performance-proof, browser-proof, release-authority]
---

# Source data adaptation and imperfect snapshot refresh

## Authority and scope

The owner requested these requirements on 2026-09-05 after explaining the
expected first integration: daily source-mart rebuilds without row change
markers, rare old sales corrections, changing customer identifiers/contacts,
disappearing or reassigned orders, duplicates and incomplete data. These are
owner-reported input characteristics, not observed provider guarantees. Their
rarity is not an accepted quality threshold, and this case does not establish
coverage of every other provider.

The [machine blueprint](../../custometry-technical-blueprint-ru.md) owns the
requirements, with the [human mirror](../../custometry-technical-blueprint-human-ru.md)
and [UI blueprint](../../custometry-ui-blueprint-ru.md) synchronized. This document
allocates requirements, examples, ownership and proof. It selects no new
database, connector vendor, service or execution engine. The v1 source-format
envelope and Forecasting hold remain unchanged. Implementation tickets may
deliver bounded subsets; the first real-source integration needs the applicable
snapshot, readiness, remediation and mapping proof before acceptance.

## Requirement allocation

| Area | Normative requirements | Proof |
|---|---|---|
| Mutable source customer identity and order reassignment | IDENTITY-006 through IDENTITY-008 | TEST-INV-118; V1-AC-063 |
| Typed mapping, flag-based returns and derived dimensions | DATA-MAP-001 through DATA-MAP-007 | TEST-INV-119, TEST-INV-120; V1-AC-066 |
| Pull, push, completion and readiness | INGEST-008 through INGEST-014 | TEST-INV-116, TEST-INV-117; V1-AC-064 |
| Full rebuild comparison, absence and correction propagation | INGEST-015 through INGEST-020 | TEST-INV-113 through TEST-INV-115, TEST-INV-122; V1-AC-063, V1-AC-067 |
| Imperfect-input accounting and degraded capabilities | DQ-INPUT-001 through DQ-INPUT-008 | TEST-INV-114, TEST-INV-115, TEST-INV-121; V1-AC-065 |

This adoption adds 31 functional requirements, ten test invariants and five
v1 acceptance criteria. It builds on existing `allow_degraded`, immutable
identity/semantic versions, extraction sessions, DQ waivers and materialization
reuse rather than introducing parallel contracts for them.

## Ownership and logical configuration

| Existing owner | Responsibility and public boundary |
|---|---|
| Connection Catalog | Source bindings, connector capabilities and safe control-table discovery; credentials remain adapter-only |
| Data Documentation | Published file templates and governed push-file admission definitions |
| Ingestion | Versioned refresh/readiness policy, generation and coverage observations, staged batches, snapshot comparison evidence and successful checkpoint |
| Semantic Model | Shared mapping expressions, key/grain rules, deterministic customer crosswalks, return policy, derived channel hierarchy and capability dependencies |
| Data Quality | Duplicate/conflict diagnostics, quality rules/tolerances, remediation validation, coverage accounting and gate decisions |
| Execution Control | Existing scheduling, admission, retries, cancellation, coalescing and fencing for both ingestion directions |
| Artifact Lifecycle | Protected original/derived artifacts, manifests, atomic visibility and retention |
| Analytics | Corrected current projections, affected partitions/populations and immutable results through public semantic/DQ/artifact references |
| Presentation & Reports | Mapping/quality/version projections, source-to-result explanations and visible limitations; no local channel computation |
| Identity & Workspace | Actor/source authorization, workspace/row/field policy and protected diagnostics; does not own business-customer identity resolution |

The logical configuration is carried by existing versioned ingestion policy
and `SemanticDatasetVersion` boundaries. An implementing ticket defines exact
schemas and stable error codes before adding providers or consumers. Required
information includes source/object scope, key stability, history coverage,
trigger/readiness rules, completion semantics, absence policy, typed mappings,
conflict resolution, tolerance policy, expected dependencies and workload
budget. Settings are reusable company configuration, not per-report formulas.

## Readiness and refresh semantics

Acquisition direction, trigger, readiness evidence and refresh mode are separate
axes. A timer/manual request can initiate a readiness check. A source notification
can trigger a pull. A source push can transfer governed files in multiple parts.
All paths converge on the same admission, staging, validation and publication
semantics. Receipt of a notification or a file part never implies completion.

A read-only control table such as `log update` is configurable by field roles,
not literal names. The contract records whether its marker means start,
completion or successful publication. A table update timestamp is not a row
watermark. Related objects need compatible generation evidence. A table marker
that stays unchanged while the provider rebuilds data in place does not prove
a stable snapshot, even if it is checked before and after extraction.

Provider snapshot/atomic publication guarantees are preferred. Otherwise the
existing `best_effort_validated` mode records read bounds, readiness limitations
and required checks. Unsupported completeness claims cannot authorize inferred
deletions. Polling has bounded interval/backoff, deadline and source-load budget;
unavailable markers produce an actionable waiting/failure outcome or an
explicitly configured validated fallback, never fabricated readiness.

The successful checkpoint advances only after the existing durable landing
manifest and required validation transaction. A seen signal is separate from a
committed generation. Push includes authorized binding, declared scope, part
inventory, completion and integrity evidence. Replayed signals/batches coalesce;
older generations cannot replace the current projection. Reprocessing the same
inputs under a new mapping has a different execution identity.

## Daily full rebuilds and uncertain identity

Without reliable row change tracking, the declared authoritative history is
read and reconciled as complete snapshots. Comparing typed content under stable
keys detects old corrections independently of row/chunk order. Scanning only
recent sales cannot guarantee discovery of an arbitrarily old edit. Content or
partition reuse can save downstream work; it cannot prove unchanged unobserved
source data. Resource requirements cover full source I/O as well as compute.

Absence means withdrawal from the current source projection only within a
verified complete authoritative scope and its published policy. It is not a
business cancellation. Partial reads, an unfinished rebuild, changed filters or
permissions, quarantined records and failed joins cannot silently erase earlier
data. Legitimate empty snapshots require completion evidence. Withdrawn records
can reappear. Retained old values under a last-good policy remain visibly stale.

A stable order moving to a different customer is an observed reassignment, not
proof that the two customer profiles are the same person. A customer ID derived
from a mutable contact needs independent stable identity or an explicit
crosswalk. Without it, continuity remains unresolved. A full replacement may
still support compatible current-snapshot analytics; row-by-row history and
identity continuity are not fabricated. Observation time is retained separately
from unknown source-effective time. Corrections recompute both old and new
affected groups while preserving already published historical results.

## Imperfect inputs and typed business rules

Dirty raw data is admissible under policy; canonical outputs still obey their
key, grain, cardinality, security and integrity invariants. Exact duplicates of
an established business key can collapse with multiplicity/provenance. Conflicting
versions need valid precedence evidence or quarantine of the conflicting key
group. Equal-looking rows without a shared key may be legitimate separate facts.
No arbitrary row ordering determines which value wins.

Coverage distinguishes complete transport from complete business history, field
coverage, relationship coverage and classification coverage. A quality decision
uses affected capabilities/scope, counts, declared denominators and monetary
impact where measurable. Unknown financial impact is visible. A small error
ratio cannot waive a critical invariant. Valid sales totals can remain available
when customer attribution is degraded. Missing history cannot certify that a
customer has no purchases, including through negated segment predicates.

| Setting/example | Required interpretation |
|---|---|
| Localized yes/no strings (exact Russian example in DATA-MAP-002) | Explicit dictionary to true/false, configured trimming/case handling; null and unknown tokens remain distinct |
| Sale-versus-return flag | Configure its vocabulary/polarity and quantity/amount sign; a separate return document is not required; already-signed values are not inverted twice |
| `source_channel = SP`, normalized `is_lk = false` | Child channel for direct sales through a manager, parent SP |
| `source_channel = SP`, normalized `is_lk = true` | Child channel for the personal account, parent SP |
| SP with null/unknown `is_lk` | Unknown child classification with visible coverage; never default to the manager channel |
| Non-SP input or overlapping rules | Explicit fallback and overlap policy, not accidental first-row or last-rule behavior |

SP remains a valid parent classification when its child is unknown. Parent
rollups count each purchase once, including the disclosed unclassified share;
the hierarchy is one dimension, not a customer segment or two copies of a sale.
Raw values, normalized flags, derived values and rule versions remain traceable.

## UI allocation and failure handling

The mapping example is configuration intent, not a required interview-style
questionnaire. `UI-DATA-008` provides a compact field mapping table, dictionary
and condition editors, bounded before/after examples and equivalent accessible
commands for optional dragging. `UI-DATA-009/010/012` provide relationships,
policies, identity limitations and version impact. Connections and existing
schedule/run surfaces expose acquisition mode, readiness dependencies, last
seen versus last committed generation, waiting/retry reason and last success.

`UI-DQ-001` through `UI-DQ-005`, dataset readiness, import diagnostics and Result
Trust expose retained/collapsed/quarantined/excluded counts, coverage by relevant
scope, unknown financial impact and affected capabilities. Mandatory invalid
canonical keys remain blocked; raw rows may be quarantined into a validated
subset. This does not widen non-waivable rules. Quarantine, waiting and last-good
serving have distinct semantics; no new serialized status enum is selected here.

## Compatibility and implementation prerequisites

Baseline: current pre-edit `0.10.0-draft` requirements in this shared checkout;
candidate: this owner-approved documentation revision.

| Surface | Classification | Conditions and remaining evidence |
|---|---|---|
| Existing valid full/incremental mappings and strict DQ behavior | compatible-change | Additional governed modes and transformations preserve their declared meanings; no silent default tolerance, rekey or boolean reinterpretation |
| Planned versioned ingestion/semantic/quality envelopes and source push admission | unknown | Concrete provider/consumer schemas, capability/version negotiation and retained configuration readers must be selected in implementing tickets |
| Planned checkpoint, generation, absence and cache identity persistence | unknown | Tickets need migration/reprocessing/rollback rules, queued-event coexistence and failure proof before writes |
| Current runtime API, code and database schema | none | This adoption changes documentation and requirement/surface indexes only; no runtime schema or application files are changed |

Existing configurations retain their interpretation. New rules create versions;
unsupported readers reject new variants explicitly. Exact wire compatibility
and rollback cannot be claimed from these requirements. The source's actual
marker semantics, key stability, authoritative history, absence policy,
tolerances and workload limits need authorized source evidence and workspace
policy before real integration; their values are not inferred from this account.

## Acceptance and documentation continuity

Implementing tickets use the synthetic fixture obligations in TEST-INV-113
through TEST-INV-122: successive snapshots, rare old changes, duplicate/conflict
groups, reassignment/rekey, incomplete/empty snapshots, mixed generations,
replay/crash, normalized flags, returns and derived channel parity. Tests compare
expected business outputs and source-row accounting, not only mapping syntax.

Source integration needs actual read/ready/commit/recovery evidence and a
measured workload budget. The first-source corpus is synthetic and contains
no employer payloads, credentials or personal identifiers. No such provider,
runtime, browser or benchmark evidence is claimed by this document.

Maintain the machine/human/UI blueprints, system/context ownership, the existing
development roadmap, surface coverage, analytical authoring trust dependencies
and generated requirement/contributor indexes together. Documentation proof is
`validate_blueprints`, requirement/docs index checks, `check_docs_links` and
`validate_route_registry`; the grouped local profile remains source-level proof.

### Documentation adoption evidence — 2026-09-05

`uv run --locked python -m tools.custometry_quality.generate_requirement_index`
and `generate_docs_index` passed after updating the canonical sources. The
machine/human representations contain the same 1,241 requirement IDs; all 46
new IDs have exactly one definition in each representation. UI capability
coverage was synchronized with the surface manifest, preserving existing routes.
`uv run --locked python -m tools.check --scope local` passed after sourcing
`scripts/activate-toolchain.sh`. This proves documentation/source consistency;
the listed refresh fixtures and source/browser/performance acceptance remain
implementation obligations, not tests executed by this adoption.
