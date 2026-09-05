---
doc_id: CONTRACT-ARTIFACT-FORMAT-001
title: Artifact format registry and reader compatibility
doc_version: 1
product_spec_version: 0.10.0-draft
visibility: internal
ship: false
owner: artifact-lifecycle
requirement_ids: [DOC-RULE-006, REPORT-006, XLSX-001, DATA-GUIDE-008]
status: accepted
proof_boundary:
  label: documented-artifact-format-contract
  exclusions: [implemented-schema, runtime-reader-compatibility, release-readiness]
---

# Artifact format registry and reader compatibility

## Identity, authority, and ownership

The `artifact-format-registry/v1` vocabulary completes the format field of the
[machine blueprint](../../custometry-technical-blueprint-ru.md) section 4.1 for
outputs already required by ChartSpec, ReportSnapshot, XLSX and Data Guide.
The user accepted this minimal completion in the documentation-audit
reconciliation on 2026-09-06. It adds no product output channel or import source.

Artifact Lifecycle owns manifest validation and publication through
`ArtifactCommitPort`. Ingestion, Analytics and other producers own their payload
schemas. Presentation owns chart/report render contracts; Data Documentation
owns Data Guide content. Readers consume only authorized immutable references.
A file extension or media type never grants access or selects a schema by itself.

This is a target documentation contract. Publication-base source inspection at
`d5ecbd33c1fd582058ec3514e2084820c8a3f1c2` finds an existing batch/Parquet
`ArtifactManifest` in `packages/artifacts/domain/model.py`, local-file and
PostgreSQL adapters, and a consumer in `apps/worker_data/vertical_slice.py`.
That implemented record has `artifact_type: str` and `schema_version: int`; it
has no generic `format` enum and is not automatically the target representation
specified here. Preserve its existing readers and persisted records. A generic
format field needs an explicit compatible schema/adapter mapping and producer/
consumer evidence before activation. Source inspection does not prove runtime
support, migration safety or the absence of dynamic/external readers.

## Vocabulary and payload mapping

The existing `parquet`, `json`, `csv`, `cbm` and `html` tokens are preserved.
The required chart/report/guide outputs add `svg`, `png`, `xlsx` and `markdown`.
Tokens are lowercase, locale-neutral, and are not interchangeable aliases.

| Manifest token | Conventional extension | Served media type | Required output / interpretation |
|---|---|---|---|
| `parquet` | `.parquet` | `application/vnd.apache.parquet` | Existing columnar landing, mart, result and export artifacts |
| `json` | `.json` | `application/json` | Existing typed specs/results; UTF-8 JSON payload |
| `csv` | `.csv` | `text/csv; charset=utf-8` | Existing tabular export, with the accepted CSV escaping/security contract |
| `cbm` | `.cbm` | `application/octet-stream` | Existing opaque CatBoost model binary; this generic transport type does not claim a registered CBM-specific media type |
| `html` | `.html` | `text/html; charset=utf-8` | Existing permitted rendered document artifact; no executable-template or remote-asset permission is added |
| `svg` | `.svg` | `image/svg+xml` | ChartSpec/static-render vector artifact |
| `png` | `.png` | `image/png` | ChartSpec/static-render raster artifact |
| `xlsx` | `.xlsx` | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` | One universal ReportSnapshot workbook path; no macro-enabled workbook type |
| `markdown` | `.md` | `text/markdown; charset=utf-8` | Immutable Data Guide source content; safe rendering remains governed by the guide contract |

The Parquet, Markdown and XLSX media types follow their respective IANA
registrations: [Parquet](https://www.iana.org/assignments/media-types/application/vnd.apache.parquet),
[Markdown](https://www.iana.org/assignments/media-types/text/markdown), and
[XLSX](https://www.iana.org/assignments/media-types/application/vnd.openxmlformats-officedocument.spreadsheetml.sheet).
Markdown explicitly declares its character set. The schema/renderer contract,
not merely the media type, establishes which payload constructs are permitted.

`format` describes the physical representation. Existing `artifact_category`
continues to select broad lifecycle/access policy; `artifact_schema_id` and
`artifact_schema_version` select the actual versioned payload contract. Neither
the format token nor this registry replaces those fields. No MIME field or
extra registry-version field is added to the persistent manifest by this document.

A format declaration does not authorize arbitrary model execution, formula
execution, HTML/SVG scripting, remote fetching, or macro-enabled workbooks.
Existing format-specific security and resource constraints remain applicable.
Forecast-related formats do not resume the held Forecasting workstream.

## Commit, reading, and failure behavior

The original immutable publication sequence remains: prepare the payload in
staging, validate its declared schema/representation and scope, compute the
hash/size over the actual stored bytes, then publish through the fenced artifact
commit boundary. A failed or cancelled writer cannot expose an incomplete
manifest. Existing retention, lineage, authorization and orphan handling apply.

Readers check schema/version and supported representation before parsing.
An unknown token, incompatible payload schema, byte/hash mismatch, or mismatched
representation fails explicitly; it is never silently treated as JSON, HTML or
an empty successful result. The implementing API selects stable error codes in
its own accepted error contract; this registry does not invent a wire enum.
Retries do not repair unsupported-format or schema failures. A corrupt artifact
requires reconciliation of its immutable reference, not an in-place rewrite.
Diagnostic evidence records safe artifact/schema identifiers and a reason;
it does not copy payload contents, private paths, secrets or denied metadata.

The exporter derives the response media type from this registry after access
checks. It does not trust a client-supplied extension or media-type header.
Text payload validation does not normalize bytes after hashing. All channels
retain the same source snapshot/lineage and format-specific renderer version.

## Compatibility, enabling writers, and rollback

| Interaction | Before → target | Classification at this documented boundary | Required condition |
|---|---|---|---|
| Existing five tokens and their stored payloads | Same token spelling, schema fields, bytes and meaning | `compatible-change` | New readers retain all previously supported schemas; no re-encoding or rehash migration is implied |
| A reader restricted to the old five-token enum receives a new token | Formerly outside its accepted vocabulary → required output vocabulary | `breaking-change` for that closed-enum contract | Update and verify every affected reader before enabling its new writer |
| Actual deployed/external reader set and supported version overlap | Not established by the bounded source search | `unknown` | Inventory provider/consumer versions, storage references and rollback readers in the implementing ticket |
| This documentation change against running product behavior | No code/schema/migration/config file is changed | `none` | This is not evidence that runtime supports the complete registry |

Before enabling one of the four newly documented representations, the
implementing ticket binds the concrete manifest/payload schemas and exercises
reader compatibility. A schema validator with a closed format enum receives an
explicit versioned update. `artifact_schema_version` remains a payload-schema
version; it is not silently overloaded as a global reader-capability flag.

Readers are deployed and verified before the affected writer. Until compatible
readers are available, the corresponding output remains explicitly unavailable;
a required output is not replaced with another format or mislabeled as ready.
Existing immutable artifacts are not renamed, re-encoded or deleted by this
registry completion.

Rollback must retain readers able to handle every format already committed.
Disabling a writer stops new output but cannot make its stored artifacts
readable to an older reader. A downgrade that loses that capability requires
an explicit compatibility outcome before execution; it cannot hide or erase
published history to claim a successful rollback.

## Acceptance evidence for implementation

- Round-trip manifest and payload fixtures for all nine tokens, including old
  five-token fixtures, with exact bytes, hashes, schema identity and scope.
- Unknown token/schema/version, mismatched bytes/extension, denied scope, and
  format-specific unsafe-content cases fail without partial publication.
- Web/static chart, report workbook and Data Guide producers preserve their
  existing snapshot/renderer/lineage contracts through `ArtifactCommitPort`.
- Reader-first deployment and rollback-reader fixtures cover formats already
  persisted; old-reader incompatibility is visible, not skipped.
- Real artifact-store/commit and renderer/export boundaries are exercised when
  those implementations exist. The present document and static gates prove
  only the vocabulary and consistency of the documentation.
