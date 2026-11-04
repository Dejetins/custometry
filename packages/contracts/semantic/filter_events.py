"""Published event meaning and exact UTC observation coverage."""

from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import model_validator
from packages.contracts.semantic import Strict
from packages.contracts.semantic.filter_fields import Name
from packages.contracts.semantic.filter_aggregates import utc_time


class EventTimeFieldVersion(Strict):
    field_id: Name
    version_id: UUID
    entity: Name
    column: Name
    known_column: Name | None = None
    storage_type: Literal["timestamp_us_utc/v1"] = "timestamp_us_utc/v1"
    null_policy: Literal["unknown"] = "unknown"


class FilterEventVersion(Strict):
    schema_version: Literal["filter-event/v1"] = "filter-event/v1"
    event_id: Name
    version_id: UUID
    entity: Name
    relationship_version_id: UUID
    time_field: EventTimeFieldVersion
    row_meaning: Literal["one_published_row_one_event/v1"] = "one_published_row_one_event/v1"

    @model_validator(mode="after")
    def entity_binding(self):
        if self.entity != self.time_field.entity:
            raise ValueError("FILTER_EVENT_ENTITY")
        return self


class EventObservation(Strict):
    starts_at: datetime
    ends_at: datetime
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
            raise ValueError("FILTER_EVENT_OBSERVATION")
        return self
