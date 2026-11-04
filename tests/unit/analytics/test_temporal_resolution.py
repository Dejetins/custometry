from datetime import date
import pytest
from pydantic import ValidationError
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.temporal import ComparisonPeriod, TemporalSettingsV2
from packages.analytics_core.application.temporal_resolution import resolve_temporal
from tests.unit.analytics.test_workspace_calculation import fixture


def resolve(
    start,
    end,
    *,
    grain="day",
    basis="calendar",
    previous="local_date_duration",
    custom=None,
    mode="previous_period",
):
    calendar = fixture()[-1]
    settings = TemporalSettingsV2(
        mode=mode,
        incomplete_period_policy="exclude",
        previous_period_basis=previous if mode == "previous_period" else None,
        comparison_period=ComparisonPeriod(starts_on=custom[0], ends_on=custom[1])
        if custom
        else None,
    )
    return resolve_temporal(
        settings,
        ComparisonPeriod(starts_on=start, ends_on=end),
        grain=grain,
        calendar=calendar,
        basis=basis,
    )


@pytest.mark.parametrize(
    "start,end,grain,expected",
    [
        ("2025-03-01", "2025-03-31", "month", ("2025-02-01", "2025-02-28")),
        ("2024-03-01", "2024-03-31", "month", ("2024-02-01", "2024-02-29")),
        ("2025-01-01", "2025-06-30", "quarter", ("2024-07-01", "2024-12-31")),
        ("2025-01-01", "2025-12-31", "year", ("2024-01-01", "2024-12-31")),
        ("2025-01-06", "2025-01-19", "week", ("2024-12-23", "2025-01-05")),
    ],
)
def test_previous_calendar_buckets(start, end, grain, expected):
    value = resolve(start, end, grain=grain, previous="calendar_bucket_count")
    assert (
        str(value.comparison_period.starts_on),
        str(value.comparison_period.ends_on),
    ) == expected
    assert (
        value.timezone == "UTC" and value.current_period.starts_at.utcoffset().total_seconds() == 0
    )
    assert value.current_period.elapsed_seconds == value.current_period.local_date_count * 86400
    assert value.overlap_local_dates == 0


def test_custom_duration_overlap_and_no_implicit_normalization():
    result = resolve(
        "2025-01-01", "2025-01-10", mode="custom_period", custom=("2025-01-05", "2025-01-08")
    )
    assert result.overlap_local_dates == 4 and result.duration_difference_local_dates == 6
    assert result.settings.duration_normalization == "none"
    assert set(result.limitation_codes) == {
        "COMPARISON_PERIODS_OVERLAP",
        "COMPARISON_DIFFERENT_DURATION",
    }
    duration = resolve("2025-03-03", "2025-03-08")
    assert (duration.comparison_period.starts_on, duration.comparison_period.ends_on) == (
        date(2025, 2, 25),
        date(2025, 3, 2),
    )
    assert duration.duration_difference_local_dates == 0


def test_partial_bucket_is_rejected_before_any_run_but_custom_date_duration_is_explicit():
    with pytest.raises(AnalyticsFailure, match="CALENDAR_RANGE_UNALIGNED"):
        resolve("2025-03-02", "2025-03-31", grain="month", previous="calendar_bucket_count")
    assert (
        resolve("2025-03-02", "2025-03-31", grain="month").comparison_period.local_date_count == 30
    )


def test_none_and_invalid_mode_inputs_and_period_bounds():
    assert resolve("2025-01-01", "2025-01-10", mode="none").comparison_period is None
    for raw in [
        dict(mode="custom_period"),
        dict(mode="previous_period"),
        dict(mode="none", previous_period_basis="local_date_duration"),
        dict(mode="none", comparison_period={"starts_on": "2025-01-01", "ends_on": "2025-01-02"}),
    ]:
        with pytest.raises(ValidationError):
            TemporalSettingsV2(incomplete_period_policy="exclude", **raw)
    with pytest.raises(ValidationError, match="PERIOD_LIMIT"):
        ComparisonPeriod(starts_on="2024-01-01", ends_on="2025-01-01")
    with pytest.raises(AnalyticsFailure, match="PERIOD_LIMIT"):
        resolve("0001-01-01", "0001-01-02")


def test_pinned_fiscal_year_and_half_year_boundaries():
    year = resolve(
        "2025-04-01", "2026-03-31", grain="year", basis="fiscal", previous="calendar_bucket_count"
    )
    assert (str(year.comparison_period.starts_on), str(year.comparison_period.ends_on)) == (
        "2024-04-01",
        "2025-03-31",
    )
    half = resolve(
        "2025-10-01",
        "2026-03-31",
        grain="half_year",
        basis="fiscal",
        previous="calendar_bucket_count",
    )
    assert (str(half.comparison_period.starts_on), str(half.comparison_period.ends_on)) == (
        "2025-04-01",
        "2025-09-30",
    )
