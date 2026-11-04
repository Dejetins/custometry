"""Lossless decimal wire representation shared by current and temporal projections."""
from decimal import Decimal
from packages.contracts.analytics import AnalyticsFailure


def number(value: Decimal | None) -> str | None:
    if value is None:
        return None
    if not value.is_finite():
        raise AnalyticsFailure("NON_FINITE_VALUE")
    if value == 0:
        return "0"
    return (
        format(value, "f").rstrip("0").rstrip(".")
        if "." in format(value, "f")
        else format(value, "f")
    )
