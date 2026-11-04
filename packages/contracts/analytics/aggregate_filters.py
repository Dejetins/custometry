"""Explicit aggregate execution capability; existing receipt/relational readers stay strict."""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
import json
from typing import Annotated, Any, Literal, cast
from uuid import UUID
from pydantic import Field, model_validator
from packages.contracts.semantic import Strict
from packages.contracts.semantic.filter_fields import Name
from packages.contracts.semantic.filter_aggregates import (
    FilterCountVersion,
    AggregateObservation,
    utc_midnight,
    utc_time,
)
from packages.contracts.analytics.relational_filters import (
    ScopedNode,
    ScopedPredicate,
    RelationalInputGrant,
)


class AggregateWindow(Strict):
    starts_at: datetime
    ends_at: datetime
    timezone: Literal["UTC"] = "UTC"
    observation_as_of: datetime
    knowledge_as_of: datetime

    @model_validator(mode="after")
    def interval(self):
        values = (self.starts_at, self.ends_at, self.observation_as_of, self.knowledge_as_of)
        if (
            not all(utc_time(v) for v in values)
            or not all(utc_midnight(v) for v in values[:2])
            or not (self.starts_at < self.ends_at <= self.observation_as_of <= self.knowledge_as_of)
        ):
            raise ValueError("FILTER_AGGREGATE_WINDOW")
        return self


class ScopedCount(Strict):
    kind: Literal["scoped_count"] = "scoped_count"
    parent_scope_id: UUID
    child_scope_id: UUID
    child_entity: Name
    relationship_id: Name
    relationship_version_id: UUID
    definition: FilterCountVersion
    window: AggregateWindow
    predicate: AggregateExpression


class CountRatio(Strict):
    kind: Literal["count_ratio"] = "count_ratio"
    numerator: ScopedCount
    denominator: ScopedCount
    unit: Literal["ratio"] = "ratio"
    zero_denominator_policy: Literal["unknown"] = "unknown"


class AggregateScalar(Strict):
    kind: Literal["scalar"] = "scalar"
    # Canonical finite nonnegative decimal, bounded for exact cross-products.
    value: Annotated[str, Field(pattern=r"^(0|[1-9][0-9]{0,8})(\.[0-9]{1,6})?$")]
    unit: Name


class AggregateCompare(ScopedNode):
    kind: Literal["aggregate_compare"] = "aggregate_compare"
    left: Annotated[ScopedCount | CountRatio, Field(discriminator="kind")]
    operator: Literal["eq", "ne", "lt", "le", "gt", "ge"]
    right: Annotated[ScopedCount | CountRatio | AggregateScalar, Field(discriminator="kind")]


class AggregateBoolean(ScopedNode):
    kind: Literal["and", "or"]
    children: tuple[AggregateExpression, ...] = Field(min_length=1, max_length=1000)


class AggregateNot(ScopedNode):
    kind: Literal["not"] = "not"
    child: AggregateExpression


class AggregateExists(ScopedNode):
    kind: Literal["exists", "not_exists"]
    parent_scope_id: UUID
    child_scope_id: UUID
    child_entity: Name
    relationship_id: Name
    relationship_version_id: UUID
    predicate: AggregateExpression


AggregateExpression = Annotated[
    ScopedPredicate | AggregateCompare | AggregateBoolean | AggregateNot | AggregateExists,
    Field(discriminator="kind"),
]
for model in (
    ScopedCount,
    CountRatio,
    AggregateCompare,
    AggregateBoolean,
    AggregateNot,
    AggregateExists,
):
    model.model_rebuild()


class AggregateFilterRequest(Strict):
    schema_version: Literal["aggregate-filter-execution/v1"] = "aggregate-filter-execution/v1"
    workspace_id: UUID
    dataset_version_id: UUID
    root_entity: Name
    root_scope_id: UUID
    registry_versions: dict[Name, UUID]
    expression: AggregateExpression
    compatibility_registry_version_id: UUID | None = None


@dataclass(frozen=True, slots=True)
class CountInput:
    definition: FilterCountVersion
    observation: AggregateObservation
    evidence_hash: str


@dataclass(frozen=True, slots=True)
class AggregateInputGrant(RelationalInputGrant):
    counts: tuple[CountInput, ...] = ()


def canonical_aggregate_expression(node: AggregateExpression) -> dict[str, Any]:
    def normalize(raw: Any) -> Any:
        if isinstance(raw, list):
            return [normalize(v) for v in cast(list[Any], raw)]
        if not isinstance(raw, dict):
            return raw
        value = {key: normalize(v) for key, v in cast(dict[str, Any], raw).items()}
        if value.get("kind") in ("and", "or"):
            value["children"] = sorted(
                value["children"], key=lambda c: json.dumps(c, sort_keys=True)
            )
        return value

    return normalize(node.model_dump(mode="json"))
