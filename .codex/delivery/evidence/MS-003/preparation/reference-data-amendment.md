# MS-003 reference-data amendment — 2026-09-12

## Authority and scope

The owner requires Customer and Product reference data in MS-003. WS-002 and
MS-003 are revised to `0.2.0`; all six prompt bindings and the canonical draft
journal are synchronized. ReceiptItem provides the required product-to-receipt
relationship. The source contract now covers six actual PostgreSQL tables,
qualified keys, dimension versions, relationships and quality accounting.

MAP-001 and the six L1 directions receive editorial reference revisions `2.0.2`.
Their capability boundaries and proposed checkpoint order are unchanged. Existing
WS-001 and completed MS-001/MS-002 artifacts retain their historical bindings and
bytes. No blueprint, product code, runtime configuration or source seed is changed.
No product stage, container, installation, commit or push is performed.

The owner's Customer/Product inclusion is recorded as MS-003/DEC-04. It does not
constitute acceptance of all other proposed MS-003 decisions. The plan remains
`in_review`, the journal remains `draft`, and every stage is pending/disallowed
with no claim, execution attempt or transition receipt.

## Source and compatibility evidence

Static inspection of the existing demo profile, DDL, seed and golden manifest
establishes the proposed counts: 1,000 customers, 120 products, 5,000 receipts,
15,000 items, 20 stores and 1,830 calendar rows. This amendment does not claim
live source or ingestion evidence. The existing seed deliberately assigns five
item rows to missing product `999999`; that is a declared test scenario.

DATA-RULE-001/002/005/008..011, METRIC-008 and DQ-INPUT-001/003..007 support the
explicit source contract. All raw items are retained; the proposed versioned
policy quarantines the five orphan item rows and publishes the eligible item
subset, with counts, provenance and limitations. It preserves every receipt
header and the receipt-grain calculations. Customer/Product/Store relationships
use disclosed current-only snapshot semantics; full history is not claimed.

This is an additive profile through existing owner ports, not a change to the
default full-retail profile or a blanket DQ waiver. It adds no library, service,
directory CRUD screen or customer/product analytical feature. Current runtime
contract impact is `none`; future profile/publication changes and real proof
are explicitly allocated to S01/S02. S03 preserves quality/version references,
and S04 displays the limitation from the saved result.

## Validation and independent review

Saved plan binding: `0.2.0`, SHA-256
`fe3ee41122e111e956346dec278aa77b859d933c01bacfe5901b9a1fb4c4f870`.

| Check | Observed result |
|---|---|
| `uv run --locked python -m tools.custometry_quality.generate_docs_index` | Pass; 68 contributor documents |
| `uv run --locked python -m tools.custometry_quality.validate_prompt_packs` | Pass; three journals; no stage execution |
| `uv run --locked python -m tools.custometry_quality.prompt_pack_validation --root . --ledger .codex/delivery/ledgers/MS-003.md --check draft` | Pass; saved authoring structure and file bindings |
| `uv run --locked python -m tools.custometry_quality.check_docs_links` | Pass; 84 documents and 665 local links |
| `uv run --locked python -m tools.check --scope local` | Pass; authoring source checks |
| `git diff --check` | Pass |
| Bounded source/navigation/triad comparison | Exact current parent and source bindings, 16 current child navigation references at 0.2.0, six matching prompt/journal contracts and plan hashes; seed expression confirms five expected orphan links |
| Preservation against fresh amendment baseline | 317 protected files byte-identical: 316 completed MS-001/MS-002 files plus WS-001; all draft lifecycle values retained |

The first navigation comparison found stale child version labels in map/direction
prose. These were corrected and the comparison repeated successfully. Existing
tooling implementation/tests were unchanged by this amendment; their prior test
results remain in the original preparation evidence, not new execution claims.

Cold-head review: **completed**.
Mode: **independent subagent**, exactly one read-only review of this amendment
using the installed architecture-review cold-head plan/prompt-pack checklist.
Verdict: **Release**, for the non-runnable owner-review candidate.
Findings resolved / unresolved: **0 / 0**; no material findings.
Local follow-up check: **completed**; source, navigation, triad and preservation
checks above passed. No second independent review was required or performed.

The review confirmed the six-table producer scope, qualified cardinality,
current-only dimension semantics, explicit orphan handling, receipt-grain oracle
and S01→S02→S03→S04 quality-reference handoff. Product/basket analysis and directory
management screens remain outside this first report.

`draft_valid`: **true**. `entry_ready`: **false**. No runtime data, migration,
calculation, browser or packaged behavior was proved by this authoring task.
Implementation of the new profile-specific policy remains assigned to S01.
The next action is owner review of the remaining concrete 0.2.0 decisions before
the existing initial-activation workflow; Customer/Product inclusion is already
settled and does not require another question.

The earlier [preparation report](report.md) records validation and review of
`0.1.0`; its results are not presented as review of this source-scope amendment.
