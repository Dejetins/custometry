"""Pure pinned-rule conversion; local dates and elapsed instants stay distinct."""

import base64
from datetime import UTC, date, datetime, timedelta, tzinfo
from io import BytesIO
from zoneinfo import ZoneInfo
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.semantic import CalendarProfile, ZonedCalendarProfileV2


def calendar_zone(profile: CalendarProfile) -> tzinfo:
    if isinstance(profile, ZonedCalendarProfileV2):
        return ZoneInfo.from_file(
            BytesIO(base64.b64decode(profile.tzif_base64)), key=profile.timezone
        )
    return UTC


def midnight(day: date, zone: tzinfo) -> datetime:
    wall = datetime.combine(day, datetime.min.time())
    candidates: list[datetime] = []
    for fold in (0, 1):
        instant = wall.replace(tzinfo=zone, fold=fold).astimezone(UTC)
        if instant.astimezone(zone).replace(tzinfo=None) == wall:
            candidates.append(instant)
    if not candidates:
        raise AnalyticsFailure("LOCAL_DATE_BOUNDARY_UNAVAILABLE")
    return min(candidates)


def day_bounds(day: date, zone: tzinfo) -> tuple[datetime, datetime]:
    left, right = midnight(day, zone), midnight(day + timedelta(days=1), zone)
    if right <= left:
        raise AnalyticsFailure("LOCAL_DATE_BOUNDARY_UNAVAILABLE")
    return left, right


def period_bounds(start: date, end: date, zone: tzinfo) -> tuple[datetime, datetime]:
    # Validate every interior boundary, including historically skipped dates.
    for offset in range((end - start).days + 1):
        day_bounds(start + timedelta(days=offset), zone)
    return midnight(start, zone), midnight(end + timedelta(days=1), zone)


def utc_source_dates(day: date, zone: tzinfo) -> list[date]:
    left, right = day_bounds(day, zone)
    end = (right - timedelta(microseconds=1)).date()
    return [left.date() + timedelta(days=i) for i in range((end - left.date()).days + 1)]
