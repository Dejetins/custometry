"""Versioned correlated filter foundation; trusted grants are never HTTP input."""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Annotated, Any, Literal, Protocol
from uuid import UUID
from pydantic import ConfigDict, Field, model_validator
from packages.contracts.semantic import Strict, Hash
from packages.contracts.semantic.filter_fields import Name, Operator
from packages.contracts.semantic.relationships import FilterRelationshipVersion
from packages.contracts.analytics.columnar_filters import (
    FilterResourcePolicy,
    FilterValue,
    FlatInputGrant,
)


class ScopedNode(Strict):
    model_config = ConfigDict(extra="forbid", frozen=True, json_schema_mode_override="validation")
    node_id: UUID
    scope_id: UUID


class ScopedPredicate(ScopedNode):
    kind: Literal["predicate"] = "predicate"
    field_id: Name
    field_version_id: UUID
    operator: Operator
    values: tuple[FilterValue, ...] = Field(default=(), max_length=1000)


class ScopedBoolean(ScopedNode):
    kind: Literal["and", "or"]
    children: tuple[ScopedExpression, ...] = Field(min_length=1, max_length=1000)


class ScopedNot(ScopedNode):
    kind: Literal["not"] = "not"
    child: ScopedExpression


class CorrelatedExists(ScopedNode):
    kind: Literal["exists", "not_exists"]
    parent_scope_id: UUID
    child_scope_id: UUID
    child_entity: Name
    relationship_id: Name
    relationship_version_id: UUID
    predicate: ScopedExpression


ScopedExpression = Annotated[
    ScopedPredicate | ScopedBoolean | ScopedNot | CorrelatedExists, Field(discriminator="kind")
]
ScopedBoolean.model_rebuild()
ScopedNot.model_rebuild()
CorrelatedExists.model_rebuild()


class RelationalFilterRequest(Strict):
    schema_version: Literal["relational-filter-execution/v2"] = "relational-filter-execution/v2"
    workspace_id: UUID
    dataset_version_id: UUID
    root_entity: Name
    root_scope_id: UUID
    registry_versions: dict[Name, UUID]
    expression: ScopedExpression
    compatibility_registry_version_id: UUID | None = None


class RelationalResourcePolicy(FilterResourcePolicy):
    max_entities: Annotated[int, Field(strict=True, ge=1, le=8)]
    max_correlations: Annotated[int, Field(strict=True, ge=1, le=64)]
    max_fan_out: Annotated[int, Field(strict=True, ge=1)]
    max_estimated_work: Annotated[int, Field(strict=True, ge=1)]
    estimation_version: Literal["sum-input-rows-times-correlations/v1"] = (
        "sum-input-rows-times-correlations/v1"
    )


@dataclass(frozen=True, slots=True)
class RelationshipInput:
    relationship: FilterRelationshipVersion
    # Must apply to the currently authorized child universe, not transport alone.
    complete: bool
    completeness_hash: str


@dataclass(frozen=True, slots=True)
class RelationalInputGrant:
    entities: tuple[FlatInputGrant, ...]
    relationships: tuple[RelationshipInput, ...]
    resource_policy: RelationalResourcePolicy
    compatibility_registry_versions: tuple[UUID, ...] = ()


class RelationalFilterAccess(Protocol):
    def authorize(
        self, *, workspace_id: UUID, actor_id: UUID, dataset_version_id: UUID
    ) -> RelationalInputGrant: ...


class RelationalFilterResult(Strict):
    schema_version: Literal["relational-filter-result/v2"] = "relational-filter-result/v2"
    request_hash: Hash
    matched_ids: tuple[str, ...]
    not_matched_count: Annotated[int, Field(strict=True, ge=0)]
    unknown_count: Annotated[int, Field(strict=True, ge=0)]
    authorized_count: Annotated[int, Field(strict=True, ge=0)]
    preview_kind: Literal["exact"] = "exact"
    limitation_codes: tuple[str, ...]

    @model_validator(mode="after")
    def counts(self) -> RelationalFilterResult:
        if (
            len(set(self.matched_ids)) != len(self.matched_ids)
            or len(self.matched_ids) + self.not_matched_count + self.unknown_count
            != self.authorized_count
        ):
            raise ValueError("FILTER_RESULT_COUNTS")
        return self


def canonical_scoped_expression(node: ScopedExpression) -> dict[str, Any]:
    value = node.model_dump(mode="json")
    if isinstance(node, ScopedBoolean):
        value["children"] = sorted(
            (canonical_scoped_expression(c) for c in node.children),
            key=lambda c: json.dumps(c, sort_keys=True),
        )
    elif isinstance(node, ScopedNot):
        value["child"] = canonical_scoped_expression(node.child)
    elif isinstance(node, CorrelatedExists):
        value["predicate"] = canonical_scoped_expression(node.predicate)
    return value
