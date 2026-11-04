"""Additive flat columnar execution boundary; old filter serializers stay unchanged."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Annotated, Any, Literal, Protocol
from uuid import UUID

from pydantic import ConfigDict, Field, model_validator

from packages.contracts.analytics import SemanticArtifactBinding
from packages.contracts.semantic import Hash, Strict
from packages.contracts.semantic.filter_fields import DataType, FlatFilterRegistry, Name, Operator


class FilterValue(Strict):
    data_type: DataType
    # Decimal/date use lossless text; no floating point conversion.
    value: (
        Annotated[str, Field(strict=True, max_length=4096)]
        | Annotated[int, Field(strict=True)]
        | Annotated[bool, Field(strict=True)]
    )


class FlatPredicate(Strict):
    kind: Literal["predicate"] = "predicate"
    field_id: Name
    field_version_id: UUID
    operator: Operator
    values: tuple[FilterValue, ...] = Field(default=(), max_length=1000)


class FlatBoolean(Strict):
    model_config = ConfigDict(extra="forbid", frozen=True, json_schema_mode_override="validation")
    kind: Literal["and", "or"]
    children: tuple[FlatExpression, ...] = Field(min_length=1, max_length=1000)


class FlatNot(Strict):
    model_config = ConfigDict(extra="forbid", json_schema_mode_override="validation")
    kind: Literal["not"] = "not"
    child: FlatExpression


FlatExpression = Annotated[FlatPredicate | FlatBoolean | FlatNot, Field(discriminator="kind")]
FlatBoolean.model_rebuild()
FlatNot.model_rebuild()


class FlatFilterRequest(Strict):
    schema_version: Literal["flat-filter-execution/v1"] = "flat-filter-execution/v1"
    workspace_id: UUID
    dataset_version_id: UUID
    registry_version_id: UUID
    expression: FlatExpression


class FilterResourcePolicy(Strict):
    """Explicit trusted limits, not browser input or implicit product defaults."""

    version_id: UUID
    max_rows: Annotated[int, Field(strict=True, ge=1)]
    max_input_bytes: Annotated[int, Field(strict=True, ge=1)]
    max_nodes: Annotated[int, Field(strict=True, ge=1, le=1000)]
    max_depth: Annotated[int, Field(strict=True, ge=1, le=64)]
    max_values: Annotated[int, Field(strict=True, ge=1)]
    memory_mb: Annotated[int, Field(strict=True, ge=16)]
    threads: Annotated[int, Field(strict=True, ge=1, le=64)]
    timeout_ms: Annotated[int, Field(strict=True, ge=1)]


@dataclass(frozen=True, slots=True)
class FlatInputGrant:
    """Trusted current provider output. Never deserialize this from an HTTP caller.

    Registry includes only fields allowed for this actor; ceiling is mandatory,
    evaluated independently of user Boolean logic. Metadata is provider-owned.
    """

    workspace_id: UUID
    actor_id: UUID
    policy_revision: str
    binding: SemanticArtifactBinding | MaterializedFilterBinding
    registry: FlatFilterRegistry
    resource_policy: FilterResourcePolicy
    row_ceiling: FlatExpression
    row_id_column: str


class FlatFilterAccess(Protocol):
    def authorize(
        self, *, workspace_id: UUID, actor_id: UUID, dataset_version_id: UUID
    ) -> FlatInputGrant: ...


class FlatFilterResult(Strict):
    schema_version: Literal["flat-filter-result/v1"] = "flat-filter-result/v1"
    request_hash: Hash
    matched_ids: tuple[str, ...]
    not_matched_count: Annotated[int, Field(strict=True, ge=0)]
    unknown_count: Annotated[int, Field(strict=True, ge=0)]
    authorized_count: Annotated[int, Field(strict=True, ge=0)]
    preview_kind: Literal["exact"] = "exact"

    @model_validator(mode="after")
    def coverage(self) -> FlatFilterResult:
        if (
            len(self.matched_ids) + self.not_matched_count + self.unknown_count
            != self.authorized_count
        ):
            raise ValueError("FILTER_COVERAGE_MISMATCH")
        return self


@dataclass(frozen=True, slots=True)
class MaterializedFilterBinding:
    """Artifact-owner admitted reference, before engine verification of exact bytes."""

    workspace_id: UUID
    entity: str
    artifact_id: UUID
    relative_uri: str
    content_hash: str


class FilterArtifactAdmission(Protocol):
    def admit_filter_input(
        self, *, workspace_id: UUID, artifact_id: UUID, entity: str, content_hash: str
    ) -> MaterializedFilterBinding: ...


@dataclass(frozen=True, slots=True)
class PublishedRetailFilter:
    registry: FlatFilterRegistry
    artifact_id: UUID
    content_hash: str
    source_namespace: str
    row_id_column: str


class RetailFilterSemanticPort(Protocol):
    def retail_filter_projection(
        self, *, workspace_id: UUID, dataset_version_id: UUID
    ) -> PublishedRetailFilter: ...


def canonical_flat_expression(node: FlatExpression) -> dict[str, Any]:
    """Stable Boolean meaning, shared across execution and scope identity boundaries."""
    if node.kind == "predicate":
        return node.model_dump(mode="json")
    if node.kind == "not":
        return {"kind": "not", "child": canonical_flat_expression(node.child)}
    return {
        "kind": node.kind,
        "children": sorted(
            (canonical_flat_expression(child) for child in node.children),
            key=lambda child: json.dumps(child, sort_keys=True),
        ),
    }


def flat_expression_fields(node: FlatExpression) -> frozenset[str]:
    if node.kind == "predicate":
        return frozenset([node.field_id])
    if node.kind == "not":
        return flat_expression_fields(node.child)
    return frozenset[str]().union(*(flat_expression_fields(child) for child in node.children))
