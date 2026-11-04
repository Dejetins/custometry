"""Additive temporal settings and resolved period contract for the mounted workspace."""

from __future__ import annotations

from datetime import date, datetime
from typing import Annotated, Literal
from pydantic import Field, model_validator, model_serializer, SerializerFunctionWrapHandler
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
    """Explicit comparison settings; legacy alignment keeps its separate meaning."""

    schema_version: Literal["time-comparison-settings/v2"] = "time-comparison-settings/v2"
    mode: Literal[
        "none",
        "previous_period",
        "custom_period",
        "previous_year_same_dates",
        "previous_year_calendar_aligned",
        "previous_year_iso_week_aligned",
        "previous_year_fiscal_period",
        "previous_year_comparable_elapsed_days",
    ]
    leap_day_policy: Literal["calendar_map", "exclude", "merge_with_feb_28"] | None = None
    iso_week_53_policy: Literal["calendar_map", "exclude", "explicit_partial"] | None = None

    @model_serializer(mode="wrap")
    def preserve_previous_settings(self, handler: SerializerFunctionWrapHandler):
        value = handler(self)
        if not self.mode.startswith("previous_year_"):
            value.pop("leap_day_policy", None)
            value.pop("iso_week_53_policy", None)
        return value

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
        leap = self.mode in ("previous_year_same_dates", "previous_year_comparable_elapsed_days")
        iso = self.mode == "previous_year_iso_week_aligned"
        if leap != (self.leap_day_policy is not None) or iso != (
            self.iso_week_53_policy is not None
        ):
            raise ValueError("COMPARISON_YEAR_POLICIES_REQUIRED")
        if (
            self.mode == "previous_year_comparable_elapsed_days"
            and self.incomplete_period_policy != "comparable_elapsed_days"
        ):
            raise ValueError("COMPARISON_ELAPSED_POLICY_REQUIRED")
        return self


class ResolvedComparisonPeriod(ComparisonPeriod):
    starts_at: datetime
    ends_at_exclusive: datetime
    local_date_count: Annotated[int, Field(strict=True, ge=1, le=366)]
    elapsed_seconds: Annotated[int, Field(strict=True, ge=1)]


class TemporalDatePairV2(Strict):
    current_date: date
    comparison_date: date | None
    excluded: bool
    reason: str | None


class ResolvedTemporalSpecV2(Strict):
    date_mapping: list[TemporalDatePairV2] | None = None

    @model_serializer(mode="wrap")
    def preserve_previous_resolution(self, handler: SerializerFunctionWrapHandler):
        value = handler(self)
        if self.date_mapping is None:
            value.pop("date_mapping", None)
        return value

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
