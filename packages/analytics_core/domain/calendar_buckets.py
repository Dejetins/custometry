"""Pure pinned month-based calendar boundaries, shared without changing legacy meaning."""

from datetime import date, timedelta
from typing import Any
from packages.contracts.semantic import BusinessCalendarVersion


def month(start: date, offset: int) -> date:
    n = start.year * 12 + start.month - 1 + offset
    return date(n // 12, n % 12 + 1, 1)


def boundary(
    day: date, grain: str, calendar: BusinessCalendarVersion, basis: str
) -> dict[str, Any]:
    start_month = calendar.profile.fiscal_year_start_month if basis == "fiscal" else 1
    origin = date(day.year - (day.month < start_month), start_month, 1)
    offset = (day.year - origin.year) * 12 + day.month - origin.month
    quarter, half = offset // 3 + 1, offset // 6 + 1
    year = (
        origin.year
        if calendar.profile.year_label == "start_year"
        else (month(origin, 12) - timedelta(days=1)).year
    )
    if grain == "day":
        start, end, label = day, day + timedelta(days=1), str(day)
    elif grain == "week":
        start = day - timedelta(days=day.weekday())
        end = start + timedelta(days=7)
        iso = start.isocalendar()
        label = f"{iso.year}-W{iso.week:02d}"
    elif grain == "month":
        start = day.replace(day=1)
        end, label = month(start, 1), day.strftime("%Y-%m")
    else:
        width = {"quarter": 3, "half_year": 6, "year": 12}[grain]
        start = month(origin, offset // width * width)
        end = month(start, width)
        prefix = "FY" if basis == "fiscal" else ""
        label = f"{prefix}{year}" + (
            f" Q{quarter}" if grain == "quarter" else f" H{half}" if grain == "half_year" else ""
        )
    return {
        "bucket_id": f"{grain}:{start}",
        "bucket_start": str(start),
        "bucket_end_exclusive": str(end),
        "natural_starts_on": str(start),
        "natural_ends_on": str(end - timedelta(days=1)),
        "label": label,
        "fiscal_year": year if basis == "fiscal" else None,
        "fiscal_quarter": quarter if basis == "fiscal" else None,
        "fiscal_half": half if basis == "fiscal" else None,
    }
