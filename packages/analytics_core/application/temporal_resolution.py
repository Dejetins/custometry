"""Resolve bounded explicit periods; no data reads or implicit clock/default lookup."""

from datetime import UTC, date, timedelta, tzinfo
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.temporal import (
    ComparisonPeriod,
    ResolvedComparisonPeriod,
    ResolvedTemporalSpecV2,
    TemporalSettingsV2,
)
from packages.contracts.semantic import BusinessCalendarVersion
from packages.analytics_core.domain.calendar_buckets import boundary, month
from packages.analytics_core.application.year_alignment import resolve_year
from packages.analytics_core.domain.calendar_time import calendar_zone, period_bounds


def resolved_period(start: date, end: date, zone: tzinfo = UTC) -> ResolvedComparisonPeriod:
    begin, finish = period_bounds(start, end, zone)
    return ResolvedComparisonPeriod(
        starts_on=start,
        ends_on=end,
        starts_at=begin,
        ends_at_exclusive=finish,
        local_date_count=(end - start).days + 1,
        elapsed_seconds=int((finish - begin).total_seconds()),
    )


def resolve_temporal(
    settings: TemporalSettingsV2,
    current: ComparisonPeriod,
    *,
    grain: str,
    calendar: BusinessCalendarVersion,
    basis: str,
) -> ResolvedTemporalSpecV2:
    zone = calendar_zone(calendar.profile)
    comparison = settings.comparison_period
    mapping = None
    mapping_codes: list[str] = []
    try:
        if settings.mode.startswith("previous_year_"):
            comparison, mapping, mapping_codes = resolve_year(
                settings, current, grain, calendar, basis
            )
        if settings.mode == "previous_period":
            end = current.starts_on - timedelta(days=1)
            if settings.previous_period_basis == "local_date_duration":
                start = current.starts_on - timedelta(
                    days=(current.ends_on - current.starts_on).days + 1
                )
            else:
                first = boundary(current.starts_on, grain, calendar, basis)
                last = boundary(current.ends_on, grain, calendar, basis)
                if first["bucket_start"] != str(current.starts_on) or last[
                    "bucket_end_exclusive"
                ] != str(current.ends_on + timedelta(days=1)):
                    raise AnalyticsFailure("COMPARISON_CALENDAR_RANGE_UNALIGNED")
                if grain in ("day", "week"):
                    start = current.starts_on - timedelta(
                        days=(current.ends_on - current.starts_on).days + 1
                    )
                else:
                    exclusive = current.ends_on + timedelta(days=1)
                    months = (
                        (exclusive.year - current.starts_on.year) * 12
                        + exclusive.month
                        - current.starts_on.month
                    )
                    start = month(current.starts_on, -months)
            comparison = ComparisonPeriod(starts_on=start, ends_on=end)
        left = resolved_period(current.starts_on, current.ends_on, zone)
        right = (
            resolved_period(comparison.starts_on, comparison.ends_on, zone) if comparison else None
        )
    except (ValueError, OverflowError) as exc:
        raise AnalyticsFailure("COMPARISON_PERIOD_LIMIT") from exc
    overlap = (
        max(0, (min(left.ends_on, right.ends_on) - max(left.starts_on, right.starts_on)).days + 1)
        if right
        else 0
    )
    difference = left.local_date_count - right.local_date_count if right else 0
    codes = (
        mapping_codes
        + (["COMPARISON_PERIODS_OVERLAP"] if overlap else [])
        + (["COMPARISON_DIFFERENT_DURATION"] if difference else [])
    )
    if any(
        p is not None and p.elapsed_seconds != p.local_date_count * 86400 for p in (left, right)
    ):
        codes.append("LOCAL_DAY_DURATION_VARIES")
    return ResolvedTemporalSpecV2.model_validate(
        dict(
            **({"date_mapping": mapping} if mapping is not None else {}),
            settings=settings,
            current_period=left,
            comparison_period=right,
            calendar_ref={"version_id": calendar.version_id, "content_hash": calendar.content_hash},
            calendar_basis=basis,
            grain=grain,
            timezone=calendar.profile.timezone,
            overlap_local_dates=overlap,
            duration_difference_local_dates=difference,
            limitation_codes=codes,
        )
    )
