"""Published count meaning, including grain, window and value policies."""

from datetime import UTC, datetime
from typing import Literal
from uuid import UUID
from pydantic import Field, model_validator
from packages.contracts.semantic import Strict
from packages.contracts.semantic.filter_fields import Name


class AggregateFieldRef(Strict):
    field_id: Name
    version_id: UUID


class FilterCountVersion(Strict):
    schema_version: Literal["filter-count/v1"] = "filter-count/v1"
    count_id: Name
    version_id: UUID
    relationship_version_id: UUID
    child_entity: Name
    kind: Literal["count", "count_distinct"]
    grain_fields: tuple[AggregateFieldRef, ...] = Field(min_length=1, max_length=4)
    unit: Name
    null_policy: Literal["unknown", "exclude"]
    empty_policy: Literal["zero_if_complete"] = "zero_if_complete"
    returns_policy: Literal["all_observed_rows/v1"] = "all_observed_rows/v1"
    time_entity: Literal["parent", "child"]
    time_field: AggregateFieldRef
    time_basis: Literal["utc_date/v1"] = "utc_date/v1"

    @model_validator(mode="after")
    def grain(self):
        if len({f.field_id for f in self.grain_fields}) != len(self.grain_fields):
            raise ValueError("FILTER_AGGREGATE_GRAIN")
        return self


def utc_time(value: datetime) -> bool:
    return value.tzinfo is not None and value.utcoffset() == UTC.utcoffset(value)


def utc_midnight(value: datetime) -> bool:
    return (
        value.tzinfo is not None
        and value.utcoffset() == UTC.utcoffset(value)
        and (value.hour, value.minute, value.second, value.microsecond) == (0, 0, 0, 0)
    )


class AggregateObservation(Strict):
    """Trusted coverage at the current authorized relationship, not client evidence."""

    starts_at: datetime
    ends_at: datetime
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
            raise ValueError("FILTER_AGGREGATE_OBSERVATION")
        return self
