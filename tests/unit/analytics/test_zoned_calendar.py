"""Pinned zone rules, real local-date aggregation, and conservative source coverage."""

from datetime import UTC, date, datetime, timedelta
import pytest
from pydantic import ValidationError
from packages.analytics_core.application.workspace_calculation import (
    build_workspace,
    digest,
    normalize,
)
from packages.analytics_core.application.temporal_resolution import resolve_temporal
from packages.analytics_core.domain.calendar_time import calendar_zone, day_bounds
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.temporal import ComparisonPeriod, TemporalSettingsV2
from packages.contracts.analytics.workspace import WorkspaceRunRequest
from packages.contracts.semantic import (
    BusinessCalendarProfile,
    ZonedCalendarInputV2,
    ZonedCalendarProfileV2,
    UpdateCalendarRequest,
    CalendarFailure,
)
from packages.semantic_model.infrastructure.timezone_rules import PackagedCalendarRules
from tests.unit.analytics.test_workspace_calculation import fixture


def zoned(zone="America/New_York"):
    request, source, inputs, access, calendar = fixture()
    profile = PackagedCalendarRules().resolve(ZonedCalendarInputV2(timezone=zone))
    calendar = calendar.model_copy(
        update={"profile": profile, "content_hash": digest(profile.model_dump(mode="json"))}
    )
    raw = request.model_dump(mode="json")
    raw.update(
        calendar_ref={
            "version_id": str(calendar.version_id),
            "content_hash": calendar.content_hash,
        },
        alignment="none",
        grain="day",
    )
    return raw, source, inputs, access, calendar


@pytest.mark.parametrize("day,hours", [("2025-03-09", 23), ("2025-11-02", 25), ("2025-03-08", 24)])
def test_actual_elapsed_instants_and_local_date_count(day, hours):
    calendar = zoned()[-1]
    spec = resolve_temporal(
        TemporalSettingsV2(
            mode="previous_period",
            previous_period_basis="local_date_duration",
            incomplete_period_policy="exclude",
        ),
        ComparisonPeriod(starts_on=day, ends_on=day),
        grain="day",
        calendar=calendar,
        basis="calendar",
    )
    assert spec.current_period.elapsed_seconds == hours * 3600
    assert spec.current_period.local_date_count == 1
    assert spec.timezone == "America/New_York"
    assert ("LOCAL_DAY_DURATION_VARIES" in spec.limitation_codes) == (hours != 24)


@pytest.mark.parametrize(
    "zone,day", [("Pacific/Apia", "2011-12-30"), ("America/Sao_Paulo", "2018-11-04")]
)
def test_missing_midnight_and_interior_skipped_day_reject_preflight(zone, day):
    raw, source, inputs, access, calendar = zoned(zone)
    target = date.fromisoformat(day)
    raw["common"] = {
        "starts_on": str(target - timedelta(days=1)),
        "ends_on": str(target + timedelta(days=1)),
        "store_ids": None,
    }
    with pytest.raises(AnalyticsFailure, match="LOCAL_DATE_BOUNDARY_UNAVAILABLE"):
        normalize(WorkspaceRunRequest.model_validate(raw), source, inputs, access, calendar)


def test_ambiguous_midnight_uses_earliest_valid_instant():
    zone = calendar_zone(zoned("America/Havana")[-1].profile)
    left, right = day_bounds(date(2025, 11, 2), zone)
    assert left == datetime(2025, 11, 2, 4, tzinfo=UTC)
    assert (right - left).total_seconds() == 25 * 3600


def test_real_aggregation_boundaries_and_missing_intersecting_source_day():
    raw, source, inputs, access, calendar = zoned()
    raw["common"] = {"starts_on": "2025-03-09", "ends_on": "2025-03-09", "store_ids": None}
    raw["time_comparison"] = {
        "mode": "previous_period",
        "previous_period_basis": "local_date_duration",
        "incomplete_period_policy": "exclude",
    }
    times = [
        "2025-03-09T04:59:59+00:00",
        "2025-03-09T05:00:00+00:00",
        "2025-03-10T03:59:59+00:00",
        "2025-03-10T04:00:00+00:00",
    ]
    inputs["Receipt"] = tuple(
        {
            "source_system_id": "dst",
            "receipt_id": str(i),
            "receipt_datetime": datetime.fromisoformat(t),
            "store_id": "1",
            "status": "completed",
            "currency": "EUR",
            "net_amount": str(10**i),
        }
        for i, t in enumerate(times)
    )
    inputs["Calendar"] = tuple(
        {"calendar_date": date(2025, 3, d), "is_period_complete": True} for d in (8, 9, 10)
    )
    request = WorkspaceRunRequest.model_validate(raw)
    result = build_workspace(request, source, inputs, access, calendar)
    assert result["totals"]["net_revenue"] == "110"
    assert result["temporal_v2"]["changes"]["net_revenue"]["right"] == "1"
    assert result["coverage"]["state"] == "complete"
    assert result["lineage"]["data_as_of"] == "2025-03-10T04:00:00+00:00"
    inputs["Calendar"] = inputs["Calendar"][:-1]
    missing = build_workspace(request, source, inputs, access, calendar)
    assert missing["totals"] == result["totals"]
    assert missing["coverage"]["state"] == "unavailable"
    assert missing["temporal_v2"]["changes"]["net_revenue"]["absolute_delta"] is None
    assert "COVERAGE_INTERSECTING_UTC_SOURCE_DAYS" in missing["trust"]["reason_codes"]


def test_rules_are_pinned_and_public_input_rejects_injection(monkeypatch):
    profile = zoned()[-1].profile
    stored = profile.model_dump(mode="json")
    monkeypatch.setattr(
        "packages.semantic_model.infrastructure.timezone_rules.files",
        lambda *_: (_ for _ in ()).throw(AssertionError("replay must not read package")),
    )
    restored = ZonedCalendarProfileV2.model_validate(stored)
    assert day_bounds(date(2025, 3, 9), calendar_zone(restored))[0] == datetime(
        2025, 3, 9, 5, tzinfo=UTC
    )
    with pytest.raises(ValidationError):
        UpdateCalendarRequest.model_validate(
            {
                "profile": stored,
                "expected_revision": 0,
                "idempotency_key": "00000000-0000-0000-0000-000000000001",
            }
        )
    with pytest.raises(ValidationError):
        ZonedCalendarProfileV2.model_validate({**stored, "tzif_sha256": "0" * 64})
    with pytest.raises(ValidationError):
        BusinessCalendarProfile.model_validate(stored)


@pytest.mark.parametrize(
    "zone", ["../etc/passwd", "/etc/passwd", "America//New_York", "Unknown/Nowhere"]
)
def test_invalid_zone_fails_bounded(zone):
    with pytest.raises(
        (ValidationError, CalendarFailure), match="CALENDAR_TIMEZONE_UNAVAILABLE|pattern"
    ):
        PackagedCalendarRules().resolve(ZonedCalendarInputV2(timezone=zone))


def test_actual_pre_stage_calendar_reader_preserves_v1_and_rejects_v2():
    import importlib.util
    import sys
    from pathlib import Path

    path = Path(".codex/delivery/evidence/MS-015/preparation/semantic-before.py")
    spec = importlib.util.spec_from_file_location("ms015_old_calendar", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    current = fixture()[-1].model_dump(mode="json")
    assert module.BusinessCalendarVersion.model_validate(current).model_dump(mode="json") == current
    with pytest.raises(ValidationError):
        module.BusinessCalendarVersion.model_validate(zoned()[-1].model_dump(mode="json"))
