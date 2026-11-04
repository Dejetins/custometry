"""Explicit bounded sequence capability; existing filter readers remain strict."""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Annotated, Literal
from uuid import UUID
from pydantic import Field, model_validator
from packages.contracts.semantic import Strict
from packages.contracts.semantic.filter_fields import Name
from packages.contracts.semantic.filter_aggregates import AggregateFieldRef, utc_time
from packages.contracts.semantic.filter_events import FilterEventVersion, EventObservation
from packages.contracts.analytics.relational_filters import ScopedNode, ScopedPredicate
from packages.contracts.analytics.aggregate_filters import (
    AggregateExpression,
    AggregateCompare,
    AggregateInputGrant,
)

Microseconds = Annotated[int, Field(strict=True, ge=0, le=315360000000000)]
Offset = Annotated[int, Field(strict=True, ge=-315360000000000, le=0)]


class FixedSequenceWindow(Strict):
    kind: Literal["fixed"] = "fixed"
    starts_at: datetime
    ends_at: datetime
    timezone: Literal["UTC"] = "UTC"
    observation_as_of: datetime
    knowledge_as_of: datetime

    @model_validator(mode="after")
    def interval(self):
        if (
            not all(
                utc_time(v)
                for v in (
                    self.starts_at,
                    self.ends_at,
                    self.observation_as_of,
                    self.knowledge_as_of,
                )
            )
            or not self.starts_at < self.ends_at <= self.observation_as_of <= self.knowledge_as_of
        ):
            raise ValueError("FILTER_SEQUENCE_WINDOW")
        return self


class RelativeSequenceWindow(Strict):
    kind: Literal["relative"] = "relative"
    policy: Literal["publication_observation_as_of_elapsed_utc/v1"] = (
        "publication_observation_as_of_elapsed_utc/v1"
    )
    anchor: datetime
    start_offset_us: Offset
    end_offset_us: Offset
    starts_at: datetime
    ends_at: datetime
    timezone: Literal["UTC"] = "UTC"
    observation_as_of: datetime
    knowledge_as_of: datetime

    @model_validator(mode="after")
    def resolved(self):
        FixedSequenceWindow.model_validate(
            self.model_dump(
                exclude={"kind", "policy", "anchor", "start_offset_us", "end_offset_us"}
            )
        )
        if (
            not utc_time(self.anchor)
            or self.anchor != self.observation_as_of
            or self.start_offset_us >= self.end_offset_us
        ):
            raise ValueError("FILTER_SEQUENCE_RELATIVE_WINDOW")
        try:
            if (self.starts_at, self.ends_at) != (
                self.anchor + timedelta(microseconds=self.start_offset_us),
                self.anchor + timedelta(microseconds=self.end_offset_us),
            ):
                raise ValueError("FILTER_SEQUENCE_RELATIVE_WINDOW")
        except OverflowError:
            raise ValueError("FILTER_SEQUENCE_RELATIVE_WINDOW") from None
        return self


class SequenceGap(Strict):
    minimum_us: Microseconds = 0
    maximum_us: Microseconds

    @model_validator(mode="after")
    def ordered(self):
        if self.minimum_us > self.maximum_us:
            raise ValueError("FILTER_SEQUENCE_GAP")
        return self


class PositiveStep(Strict):
    kind: Literal["positive"] = "positive"
    step_id: UUID
    child_scope_id: UUID
    event: FilterEventVersion
    predicate: AggregateExpression
    gap: SequenceGap | None = None


class NegativeStep(Strict):
    kind: Literal["negative"] = "negative"
    step_id: UUID
    child_scope_id: UUID
    event: FilterEventVersion
    predicate: AggregateExpression
    after_step_id: UUID
    starts_after_us: Microseconds = 0
    ends_after_us: Microseconds

    @model_validator(mode="after")
    def interval(self):
        if self.starts_after_us >= self.ends_after_us:
            raise ValueError("FILTER_SEQUENCE_NEGATIVE_INTERVAL")
        return self


class SequencePropertyBinding(Strict):
    left_step_id: UUID
    left_field: AggregateFieldRef
    right_step_id: UUID
    right_field: AggregateFieldRef
    null_policy: Literal["unknown"] = "unknown"


class BehavioralSequence(ScopedNode):
    kind: Literal["sequence"] = "sequence"
    parent_scope_id: UUID
    relationship_id: Name
    relationship_version_id: UUID
    child_entity: Name
    window: Annotated[FixedSequenceWindow | RelativeSequenceWindow, Field(discriminator="kind")]
    steps: tuple[Annotated[PositiveStep | NegativeStep, Field(discriminator="kind")], ...] = Field(
        min_length=1, max_length=8
    )
    bindings: tuple[SequencePropertyBinding, ...] = Field(default=(), max_length=16)
    tie_policy: Literal["strict_event_time/v1"] = "strict_event_time/v1"

    @model_validator(mode="after")
    def ordered(self):
        ids: set[UUID] = set()
        positive: set[UUID] = set()
        previous = None
        for step in self.steps:
            if step.step_id in ids:
                raise ValueError("FILTER_SEQUENCE_STEP_ID")
            ids.add(step.step_id)
            if isinstance(step, PositiveStep):
                if (previous is None) != (step.gap is None):
                    raise ValueError("FILTER_SEQUENCE_ANCHOR")
                previous = step.step_id
                positive.add(step.step_id)
            elif previous is None or step.after_step_id != previous:
                raise ValueError("FILTER_SEQUENCE_ANCHOR")
        for binding in self.bindings:
            if (
                binding.left_step_id == binding.right_step_id
                or not {binding.left_step_id, binding.right_step_id} <= positive
            ):
                raise ValueError("FILTER_SEQUENCE_PROPERTY_BINDING")
        return self


class SequenceBoolean(ScopedNode):
    kind: Literal["and", "or"]
    children: tuple[SequenceExpression, ...] = Field(min_length=1, max_length=1000)


class SequenceNot(ScopedNode):
    kind: Literal["not"] = "not"
    child: SequenceExpression


class SequenceExists(ScopedNode):
    kind: Literal["exists", "not_exists"]
    parent_scope_id: UUID
    child_scope_id: UUID
    child_entity: Name
    relationship_id: Name
    relationship_version_id: UUID
    predicate: SequenceExpression


SequenceExpression = Annotated[
    ScopedPredicate
    | AggregateCompare
    | BehavioralSequence
    | SequenceBoolean
    | SequenceNot
    | SequenceExists,
    Field(discriminator="kind"),
]
for model in (SequenceBoolean, SequenceNot, SequenceExists):
    model.model_rebuild()


class SequenceFilterRequest(Strict):
    schema_version: Literal["sequence-filter-execution/v1"] = "sequence-filter-execution/v1"
    workspace_id: UUID
    dataset_version_id: UUID
    root_entity: Name
    root_scope_id: UUID
    registry_versions: dict[Name, UUID]
    expression: SequenceExpression
    compatibility_registry_version_id: UUID | None = None


@dataclass(frozen=True, slots=True)
class EventInput:
    definition: FilterEventVersion
    observation: EventObservation
    complete: bool
    evidence_hash: str


@dataclass(frozen=True, slots=True)
class SequenceInputGrant(AggregateInputGrant):
    events: tuple[EventInput, ...] = ()


def canonical_sequence_expression(node: Strict):
    import json
    from typing import Any, cast

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
