from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Literal
from uuid import UUID
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from packages.contracts.analytics import AnalyticsFailure


ResultType = Literal["sales", "customer", "rfm"]
ComparisonMode = Literal[
    "none",
    "previous_year_same_dates",
    "previous_year_calendar_aligned",
    "previous_year_iso_week_aligned",
    "previous_year_fiscal_period",
    "previous_year_comparable_elapsed_days",
]


@dataclass(frozen=True, slots=True)
class Period:
    starts_on: date
    ends_on: date

    def validate(self) -> None:
        if self.ends_on < self.starts_on:
            raise AnalyticsFailure("INVALID_PERIOD")
        if (self.ends_on - self.starts_on).days > 370:
            raise AnalyticsFailure("PERIOD_TOO_LARGE")


@dataclass(frozen=True, slots=True)
class TimeComparison:
    mode: ComparisonMode
    current_period: Period
    comparison_period: Period | None
    timezone: str
    calendar_version_id: UUID
    incomplete_period_policy: Literal["exclude", "comparable_elapsed_days", "explicit_partial"]
    leap_day_policy: Literal["calendar_map", "exclude", "merge_with_feb_28"]
    iso_week_53_policy: Literal["calendar_map", "exclude", "explicit_partial"]
    definition_compatibility_policy: Literal["require_same_versions", "allow_explicit_rebase"]

    def validate(self) -> None:
        self.current_period.validate()
        try:
            ZoneInfo(self.timezone)
        except ZoneInfoNotFoundError as exc:
            raise AnalyticsFailure("INVALID_TIMEZONE") from exc
        if self.mode == "none":
            if self.comparison_period is not None:
                raise AnalyticsFailure("COMPARISON_PERIOD_FOR_MODE_NONE")
            return
        if self.comparison_period is None:
            raise AnalyticsFailure("COMPARISON_PERIOD_REQUIRED")
        self.comparison_period.validate()
        if self.comparison_period.ends_on >= self.current_period.starts_on:
            raise AnalyticsFailure("COMPARISON_PERIOD_OVERLAP")
        if self.mode == "previous_year_same_dates":
            current_days = (self.current_period.ends_on - self.current_period.starts_on).days
            comparison_days = (
                self.comparison_period.ends_on - self.comparison_period.starts_on
            ).days
            if current_days != comparison_days and self.leap_day_policy == "calendar_map":
                raise AnalyticsFailure("CALENDAR_ALIGNMENT_MISMATCH")
        if (
            self.mode == "previous_year_comparable_elapsed_days"
            and self.incomplete_period_policy != "comparable_elapsed_days"
        ):
            raise AnalyticsFailure("INCOMPLETE_PERIOD_POLICY_MISMATCH")


@dataclass(frozen=True, slots=True)
class FilterPredicate:
    field: Literal["store_id", "channel_id", "currency", "status", "net_amount"]
    operator: Literal["eq", "in", "gte", "lte"]
    value: str | Decimal | tuple[str, ...]

    def validate(self) -> None:
        categorical = self.field in {"store_id", "channel_id", "currency", "status"}
        if categorical:
            if self.operator not in {"eq", "in"}:
                raise AnalyticsFailure("FILTER_OPERATOR_TYPE_MISMATCH")
            if self.operator == "eq" and not isinstance(self.value, str):
                raise AnalyticsFailure("FILTER_VALUE_TYPE_MISMATCH")
            if self.operator == "in" and (
                not isinstance(self.value, tuple)
                or not self.value
                or not all(isinstance(item, str) for item in self.value)
            ):
                raise AnalyticsFailure("FILTER_VALUE_TYPE_MISMATCH")
        elif self.operator not in {"eq", "gte", "lte"} or not isinstance(self.value, Decimal):
            raise AnalyticsFailure("FILTER_VALUE_TYPE_MISMATCH")


@dataclass(frozen=True, slots=True)
class AnalyticsRequest:
    result_type: ResultType
    semantic_dataset_version_id: UUID
    comparison: TimeComparison
    filters: tuple[FilterPredicate, ...] = ()
    rfm_score_bins: int = 5
    rfm_frequency_measure: Literal["receipt_count", "purchase_day_count"] = "receipt_count"
    rfm_segment_rule_set_version: str = "rfm-retail-v1"

    def validate(self) -> None:
        self.comparison.validate()
        if not 2 <= self.rfm_score_bins <= 10:
            raise AnalyticsFailure("INVALID_RFM_SCORE_BINS")
        if self.rfm_segment_rule_set_version != "rfm-retail-v1":
            raise AnalyticsFailure("UNKNOWN_RFM_RULE_SET")
        seen: set[str] = set()
        for predicate in self.filters:
            predicate.validate()
            if predicate.field in seen:
                raise AnalyticsFailure("DUPLICATE_FILTER_FIELD")
            seen.add(predicate.field)


def decimal_value(value: object) -> Decimal:
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))
