"""Explicit prior-year calendar/date mapping for the pinned UTC calendar provider."""

from datetime import date, timedelta
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.temporal import (
    ComparisonPeriod,
    TemporalDatePairV2,
    TemporalSettingsV2,
)
from packages.contracts.semantic import BusinessCalendarVersion
from packages.analytics_core.domain.calendar_buckets import boundary, month


def resolve_year(
    settings: TemporalSettingsV2,
    current: ComparisonPeriod,
    grain: str,
    calendar: BusinessCalendarVersion,
    basis: str,
) -> tuple[ComparisonPeriod | None, list[TemporalDatePairV2] | None, list[str]]:
    mode = settings.mode
    if mode in ("previous_year_calendar_aligned", "previous_year_fiscal_period"):
        required = "fiscal" if mode == "previous_year_fiscal_period" else "calendar"
        if basis != required or grain not in ("month", "quarter", "half_year", "year"):
            raise AnalyticsFailure("COMPARISON_CALENDAR_BASIS_UNSUPPORTED")
        first, last = (
            boundary(current.starts_on, grain, calendar, basis),
            boundary(current.ends_on, grain, calendar, basis),
        )
        if first["bucket_start"] != str(current.starts_on) or last["bucket_end_exclusive"] != str(
            current.ends_on + timedelta(days=1)
        ):
            raise AnalyticsFailure("COMPARISON_CALENDAR_RANGE_UNALIGNED")
        return (
            ComparisonPeriod(
                starts_on=month(current.starts_on, -12),
                ends_on=month(current.ends_on + timedelta(days=1), -12) - timedelta(days=1),
            ),
            None,
            [],
        )
    if mode == "previous_year_iso_week_aligned" and grain not in ("day", "week"):
        raise AnalyticsFailure("COMPARISON_ISO_GRAIN_UNSUPPORTED")
    mapping: list[TemporalDatePairV2] = []
    for i in range((current.ends_on - current.starts_on).days + 1):
        day = current.starts_on + timedelta(days=i)
        previous = None
        excluded = False
        reason = None
        if mode == "previous_year_iso_week_aligned":
            year, week, weekday = day.isocalendar()
            try:
                previous = date.fromisocalendar(year - 1, week, weekday)
            except ValueError:
                if week != 53:
                    raise
                if settings.iso_week_53_policy == "calendar_map":
                    raise AnalyticsFailure("COMPARISON_CALENDAR_MAP_UNAVAILABLE")
                excluded = settings.iso_week_53_policy == "exclude"
                reason = "ISO_WEEK_53_EXCLUDED" if excluded else "ISO_WEEK_53_UNMAPPED"
        else:
            try:
                previous = day.replace(year=day.year - 1)
            except ValueError:
                if day.month != 2 or day.day != 29:
                    raise
                if settings.leap_day_policy == "calendar_map":
                    raise AnalyticsFailure("COMPARISON_CALENDAR_MAP_UNAVAILABLE")
                if settings.leap_day_policy == "merge_with_feb_28":
                    previous = day.replace(year=day.year - 1, day=28)
                    reason = "LEAP_DAY_MERGED"
                else:
                    excluded = True
                    reason = "LEAP_DAY_EXCLUDED"
        mapping.append(
            TemporalDatePairV2(
                current_date=day, comparison_date=previous, excluded=excluded, reason=reason
            )
        )
    dates = [p.comparison_date for p in mapping if p.comparison_date is not None]
    comparison = ComparisonPeriod(starts_on=min(dates), ends_on=max(dates)) if dates else None
    codes = sorted({p.reason for p in mapping if p.reason})
    if not dates:
        codes.append("COMPARISON_NO_MAPPED_DATES")
    if comparison and any(
        d.month == 2 and d.day == 29 and d not in dates
        for d in (
            comparison.starts_on + timedelta(days=i)
            for i in range((comparison.ends_on - comparison.starts_on).days + 1)
        )
    ):
        codes.append("BASELINE_UNMAPPED_LEAP_DAY_EXCLUDED")
    return comparison, mapping, codes
