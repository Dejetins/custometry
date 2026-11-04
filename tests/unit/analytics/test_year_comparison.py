"""Versioned prior-year policy math and frozen pre-stage compatibility."""

import importlib.util
import json
import sys
from pathlib import Path
from datetime import date, datetime
import pytest
from pydantic import ValidationError
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.temporal import TemporalSettingsV2, ComparisonPeriod
from packages.contracts.analytics.workspace import WorkspaceRunRequest, WorkspaceAccess
from packages.contracts.semantic import BusinessCalendarVersion
from packages.analytics_core.application.temporal_resolution import resolve_temporal
from packages.analytics_core.application.workspace_calculation import build_workspace
from tests.unit.analytics.test_workspace_calculation import fixture


def resolve(start, end, mode="previous_year_same_dates", grain="day", basis="calendar", **policies):
    calendar = fixture()[-1]
    settings = TemporalSettingsV2(
        mode=mode,
        leap_day_policy=policies.get("leap", "exclude")
        if mode in ("previous_year_same_dates", "previous_year_comparable_elapsed_days")
        else None,
        iso_week_53_policy=policies.get("iso", "exclude")
        if mode == "previous_year_iso_week_aligned"
        else None,
        incomplete_period_policy=policies.get("incomplete", "exclude"),
    )
    return resolve_temporal(
        settings,
        ComparisonPeriod(starts_on=start, ends_on=end),
        grain=grain,
        calendar=calendar,
        basis=basis,
    ), calendar


def test_leap_exclude_merge_and_calendar_map_are_explicit():
    spec, _ = resolve("2024-02-28", "2024-03-01")
    assert [p.excluded for p in spec.date_mapping] == [False, True, False]
    assert spec.date_mapping[1].comparison_date is None
    merged, _ = resolve("2024-02-28", "2024-03-01", leap="merge_with_feb_28")
    assert [str(p.comparison_date) for p in merged.date_mapping] == [
        "2023-02-28",
        "2023-02-28",
        "2023-03-01",
    ]
    assert "LEAP_DAY_MERGED" in merged.limitation_codes
    with pytest.raises(AnalyticsFailure, match="CALENDAR_MAP_UNAVAILABLE"):
        resolve("2024-02-29", "2024-02-29", leap="calendar_map")
    empty, _ = resolve("2024-02-29", "2024-02-29")
    assert (
        empty.comparison_period is None and "COMPARISON_NO_MAPPED_DATES" in empty.limitation_codes
    )


@pytest.mark.parametrize(
    "mode,basis,start,end,expected",
    [
        (
            "previous_year_calendar_aligned",
            "calendar",
            "2025-02-01",
            "2025-02-28",
            ("2024-02-01", "2024-02-29"),
        ),
        (
            "previous_year_fiscal_period",
            "fiscal",
            "2025-04-01",
            "2026-03-31",
            ("2024-04-01", "2025-03-31"),
        ),
    ],
)
def test_aligned_actual_ranges(mode, basis, start, end, expected):
    spec, _ = resolve(start, end, mode, "month" if "02-01" in start else "year", basis)
    assert (str(spec.comparison_period.starts_on), str(spec.comparison_period.ends_on)) == expected
    assert spec.date_mapping is None
    with pytest.raises(AnalyticsFailure, match="BASIS_UNSUPPORTED"):
        resolve(start, end, mode, "month", "calendar" if basis == "fiscal" else "fiscal")
    with pytest.raises(AnalyticsFailure, match="RANGE_UNALIGNED"):
        resolve("2025-02-02", "2025-02-28", "previous_year_calendar_aligned", "month")


def test_iso_year_boundary_and_missing_week53():
    spec, _ = resolve("2021-01-04", "2021-01-10", "previous_year_iso_week_aligned", "week")
    assert str(spec.comparison_period.starts_on) == "2019-12-30"
    for policy in ["exclude", "explicit_partial"]:
        spec, _ = resolve(
            "2020-12-28", "2021-01-03", "previous_year_iso_week_aligned", "week", iso=policy
        )
        assert len(spec.date_mapping) == 7 and all(
            p.comparison_date is None for p in spec.date_mapping
        )
        assert all(p.excluded == (policy == "exclude") for p in spec.date_mapping)
    with pytest.raises(AnalyticsFailure, match="CALENDAR_MAP_UNAVAILABLE"):
        resolve("2021-01-01", "2021-01-02", "previous_year_iso_week_aligned", iso="calendar_map")


def test_new_modes_require_explicit_policies_and_elapsed_policy():
    with pytest.raises(ValidationError, match="YEAR_POLICIES_REQUIRED"):
        TemporalSettingsV2(mode="previous_year_same_dates", incomplete_period_policy="exclude")
    with pytest.raises(ValidationError, match="ELAPSED_POLICY_REQUIRED"):
        resolve("2025-01-01", "2025-01-03", "previous_year_comparable_elapsed_days")


def test_actual_frozen_ms013_inputs_results_and_reader():
    pre = Path(".codex/delivery/evidence/MS-014/preparation")
    frozen = json.loads((pre / "previous-mode-golden.json").read_text())
    access = WorkspaceAccess.model_validate(frozen["access"])
    calendar = BusinessCalendarVersion.model_validate(frozen["calendar"])
    inputs = frozen["inputs"]
    for row in inputs["Receipt"]:
        row["receipt_datetime"] = datetime.fromisoformat(row["receipt_datetime"])
    for row in inputs["Calendar"]:
        row["calendar_date"] = date.fromisoformat(row["calendar_date"])
    for case in frozen["cases"]:
        query = WorkspaceRunRequest.model_validate(case["query"])
        assert query.model_dump(mode="json") == case["query"]
        assert build_workspace(query, frozen["source"], inputs, access, calendar) == case["result"]
    spec = importlib.util.spec_from_file_location("ms014_old_settings", pre / "temporal-before.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    with pytest.raises(ValidationError):
        module.TemporalSettingsV2.model_validate(
            resolve("2025-01-01", "2025-01-02")[0].settings.model_dump(mode="json")
        )


def actual(
    start,
    end,
    values,
    *,
    mode="previous_year_same_dates",
    grain="day",
    incomplete="exclude",
    leap="exclude",
    iso="exclude",
    incomplete_date=None,
):
    from datetime import UTC, timedelta

    request, source, inputs, access, calendar = fixture()
    raw = request.model_dump(mode="json")
    raw.update(
        alignment="none",
        grain=grain,
        calendar_basis="calendar",
        common={"starts_on": start, "ends_on": end, "store_ids": None},
        time_comparison={
            "mode": mode,
            "incomplete_period_policy": incomplete,
            "leap_day_policy": leap
            if mode in ("previous_year_same_dates", "previous_year_comparable_elapsed_days")
            else None,
            "iso_week_53_policy": iso if mode == "previous_year_iso_week_aligned" else None,
        },
    )
    inputs["Receipt"] = tuple(
        {
            "source_system_id": "year-test",
            "receipt_id": str(i),
            "receipt_datetime": datetime.combine(date.fromisoformat(day), datetime.min.time(), UTC),
            "store_id": "1",
            "status": "completed",
            "currency": "EUR",
            "net_amount": str(value),
        }
        for i, (day, value) in enumerate(values.items())
    )
    earliest = min(date.fromisoformat(d) for d in values)
    latest = max(date.fromisoformat(d) for d in values)
    inputs["Calendar"] = tuple(
        {
            "calendar_date": earliest + timedelta(days=i),
            "is_period_complete": str(earliest + timedelta(days=i)) != incomplete_date,
        }
        for i in range((latest - earliest).days + 1)
    )
    return build_workspace(
        WorkspaceRunRequest.model_validate(raw), source, inputs, access, calendar
    )


def test_merge_deduplicates_baseline_in_buckets_and_totals_and_exclude_drops_current():
    data = {"2023-02-28": 5, "2024-02-28": 10, "2024-02-29": 20}
    result = actual("2024-02-28", "2024-02-29", data, leap="merge_with_feb_28")["temporal_v2"]
    assert result["changes"]["net_revenue"]["absolute_delta"] == "25"
    assert result["evaluated_comparison_dates"] == ["2023-02-28"]
    assert len(result["buckets"]) == 1
    assert result["buckets"][0]["current_dates"] == ["2024-02-28", "2024-02-29"]
    assert result["buckets"][0]["changes"]["net_revenue"]["right"] == "5"
    excluded = actual("2024-02-28", "2024-02-29", data)["temporal_v2"]
    assert excluded["changes"]["net_revenue"]["absolute_delta"] == "5"
    assert excluded["evaluated_current_dates"] == ["2024-02-28"]
    empty = actual("2024-02-29", "2024-02-29", data)["temporal_v2"]
    assert (
        empty["comparability_status"] == "unavailable"
        and empty["changes"]["net_revenue"]["right"] is None
    )


def test_iso_missing_pair_is_not_reported_as_complete_or_zero():
    data = {"2019-12-23": 5, "2020-12-21": 10, "2020-12-28": 20}
    result = actual(
        "2020-12-21",
        "2021-01-03",
        data,
        mode="previous_year_iso_week_aligned",
        grain="week",
        incomplete="explicit_partial",
        iso="explicit_partial",
    )["temporal_v2"]
    change = result["changes"]["net_revenue"]
    assert (
        change["right_coverage"]["expected_days"] == 14
        and change["right_coverage"]["calendar_days"] == 7
    )
    assert result["comparability_status"] == "partial"
    assert result["buckets"][1]["changes"]["net_revenue"]["right"] is None
    assert result["buckets"][1]["changes"]["net_revenue"]["absolute_delta"] is None


def test_elapsed_year_trims_to_actual_complete_mapped_prefix():
    data = {
        "2024-01-01": 5,
        "2024-01-02": 8,
        "2024-01-03": 9,
        "2025-01-01": 10,
        "2025-01-02": 20,
        "2025-01-03": 30,
    }
    result = actual(
        "2025-01-01",
        "2025-01-03",
        data,
        mode="previous_year_comparable_elapsed_days",
        incomplete="comparable_elapsed_days",
        incomplete_date="2025-01-02",
    )["temporal_v2"]
    assert result["evaluated_current_dates"] == ["2025-01-01"] and result[
        "evaluated_comparison_dates"
    ] == ["2024-01-01"]
    assert result["changes"]["net_revenue"]["absolute_delta"] == "5"
    assert "COMPARABLE_ELAPSED_DAYS_TRIMMED" in result["limitation_codes"]


def test_leap_merge_across_week_boundary_counts_comparison_once():
    data = {"2015-02-28": 5, "2016-02-28": 10, "2016-02-29": 20}
    result = actual("2016-02-28", "2016-02-29", data, grain="week", leap="merge_with_feb_28")[
        "temporal_v2"
    ]
    assert len(result["buckets"]) == 1
    assert result["buckets"][0]["current_dates"] == ["2016-02-28", "2016-02-29"]
    assert result["buckets"][0]["changes"]["net_revenue"]["right"] == "5"
    assert result["buckets"][0]["changes"]["net_revenue"]["absolute_delta"] == "25"
