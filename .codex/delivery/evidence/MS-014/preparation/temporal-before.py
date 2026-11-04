"""Additive temporal settings and resolved period contract for the mounted workspace."""

from __future__ import annotations

from datetime import date, datetime
from typing import Annotated, Literal
from pydantic import Field, model_validator
from packages.contracts.semantic import CalendarRef, Strict


class ComparisonPeriod(Strict):
    starts_on: date
    ends_on: date

    @model_validator(mode="after")
    def bounded(self) -> ComparisonPeriod:
        if self.ends_on < self.starts_on or (self.ends_on - self.starts_on).days >= 366:
            raise ValueError("COMPARISON_PERIOD_LIMIT")
        return self


class TemporalSettingsV2(Strict):
    """Legacy alignment stays separate; settings are explicit and never imply last year."""

    schema_version: Literal["time-comparison-settings/v2"] = "time-comparison-settings/v2"
    mode: Literal["none", "previous_period", "custom_period"]
    comparison_period: ComparisonPeriod | None = None
    previous_period_basis: Literal["calendar_bucket_count", "local_date_duration"] | None = None
    incomplete_period_policy: Literal["exclude", "comparable_elapsed_days", "explicit_partial"]
    duration_normalization: Literal["none"] = "none"

    @model_validator(mode="after")
    def explicit_inputs(self) -> TemporalSettingsV2:
        if (self.mode == "custom_period") != (self.comparison_period is not None):
            raise ValueError("COMPARISON_CUSTOM_PERIOD_REQUIRED")
        if (self.mode == "previous_period") != (self.previous_period_basis is not None):
            raise ValueError("COMPARISON_PREVIOUS_BASIS_REQUIRED")
        return self


class ResolvedComparisonPeriod(ComparisonPeriod):
    starts_at: datetime
    ends_at_exclusive: datetime
    local_date_count: Annotated[int, Field(strict=True, ge=1, le=366)]
    elapsed_seconds: Annotated[int, Field(strict=True, ge=1)]


class ResolvedTemporalSpecV2(Strict):
    schema_version: Literal["resolved-time-comparison/v2"] = "resolved-time-comparison/v2"
    settings: TemporalSettingsV2
    current_period: ResolvedComparisonPeriod
    comparison_period: ResolvedComparisonPeriod | None
    calendar_ref: CalendarRef
    calendar_basis: Literal["calendar", "fiscal"]
    grain: Literal["day", "week", "month", "quarter", "half_year", "year"]
    timezone: Literal["UTC"]
    overlap_local_dates: Annotated[int, Field(strict=True, ge=0)]
    duration_difference_local_dates: int
    limitation_codes: list[str]
