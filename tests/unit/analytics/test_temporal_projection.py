"""Actual receipt projection, Decimal deltas, partial policy and legacy parity."""

import hashlib
import importlib.util
import json
import sys
from copy import deepcopy
from pathlib import Path

import pytest
from pydantic import ValidationError
from packages.contracts.analytics.temporal import TemporalSettingsV2
from packages.contracts.analytics.workspace import WorkspaceRunRequest, TemporalArtifactV2
from packages.analytics_core.application.workspace_calculation import build_workspace
from tests.unit.analytics.test_workspace_calculation import fixture


def configured(policy="exclude"):
    request, source, inputs, access, calendar = fixture()
    raw = request.model_dump(mode="json")
    raw["alignment"] = "none"
    raw["time_comparison"] = {
        "mode": "custom_period",
        "incomplete_period_policy": policy,
        "comparison_period": {"starts_on": "2024-01-01", "ends_on": "2024-01-03"},
    }
    return WorkspaceRunRequest.model_validate(raw), source, inputs, access, calendar


def test_actual_values_zero_denominator_and_immutable_artifact_hash():
    args = configured()
    result = build_workspace(*args)
    artifact = result["temporal_v2"]
    assert (
        result["temporal"] is None and artifact["changes"]["net_revenue"]["absolute_delta"] == "120"
    )
    assert artifact["changes"]["net_revenue"]["relative_delta_percent"] is None
    assert artifact["changes"]["net_revenue"]["reason_codes"] == ["ZERO_BASELINE"]
    assert artifact["changes"]["receipt_count"]["relative_delta_percent"] == "200"
    payload = {k: v for k, v in artifact.items() if k != "content_hash"}
    assert (
        artifact["content_hash"]
        == hashlib.sha256(
            json.dumps(
                payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
            ).encode()
        ).hexdigest()
    )
    assert TemporalArtifactV2.model_validate(artifact).spec.settings.mode == "custom_period"
    assert artifact["spec"]["current_period"]["ends_at_exclusive"] == "2025-01-04T00:00:00Z"
    different = args[0].model_copy(
        update={
            "time_comparison": TemporalSettingsV2(
                mode="previous_period",
                incomplete_period_policy="exclude",
                previous_period_basis="local_date_duration",
            )
        }
    )
    assert build_workspace(different, *args[1:])["request_hash"] != result["request_hash"]


@pytest.mark.parametrize(
    "policy,absolute,count,status",
    [
        ("exclude", None, 3, "unavailable"),
        ("explicit_partial", "120", 3, "partial"),
        ("comparable_elapsed_days", "100", 1, "descriptive"),
    ],
)
def test_incomplete_policy_never_silently_uses_full_period(policy, absolute, count, status):
    request, source, inputs, access, calendar = configured(policy)
    inputs = deepcopy(inputs)
    inputs["Calendar"] = tuple(
        {**r, "is_period_complete": False} if str(r["calendar_date"]) == "2025-01-02" else r
        for r in inputs["Calendar"]
    )
    result = build_workspace(request, source, inputs, access, calendar)["temporal_v2"]
    assert result["changes"]["net_revenue"]["absolute_delta"] == absolute
    assert len(result["evaluated_current_dates"]) == count
    assert result["comparability_status"] == status
    if policy == "comparable_elapsed_days":
        assert "COMPARABLE_ELAPSED_DAYS_TRIMMED" in result["limitation_codes"]
    else:
        assert "COVERAGE_INCOMPLETE" in result["limitation_codes"]


def load(name, filename):
    spec = importlib.util.spec_from_file_location(
        name, Path(".codex/delivery/evidence/MS-013/preparation") / filename
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_actual_pre_ms013_reader_and_calculation_are_identical_for_legacy_and_reject_new():
    old = load("ms013_old_reader", "workspace-before.py")
    calculation = load("ms013_old_calculation", "workspace-calculation-before.py")
    request, source, inputs, access, calendar = fixture()
    raw = request.model_dump_json()
    previous = old.WorkspaceRunRequest.model_validate_json(raw)
    assert previous.model_dump_json() == raw
    assert calculation.build_workspace(
        previous, source, inputs, access, calendar
    ) == build_workspace(request, source, inputs, access, calendar)
    new = configured()[0]
    encoded = new.model_dump_json()
    with pytest.raises(ValidationError, match="extra_forbidden"):
        old.WorkspaceRunRequest.model_validate_json(encoded)
    assert WorkspaceRunRequest.model_validate_json(encoded).model_dump_json() == encoded
    with pytest.raises(ValidationError, match="COMPARISON_CONTRACT_CONFLICT"):
        WorkspaceRunRequest.model_validate(
            {**new.model_dump(mode="json"), "alignment": "previous_year_same_dates"}
        )


def test_current_store_ceiling_and_mandatory_metric_rules_apply_to_both_periods():
    request, source, inputs, access, calendar = configured()
    for store, status, currency in [
        ("2", "completed", "EUR"),
        ("1", "cancelled", "EUR"),
        ("1", "completed", "USD"),
    ]:
        inputs["Receipt"] += tuple(
            {
                **row,
                "store_id": store,
                "status": status,
                "currency": currency,
                "net_amount": "999999",
                "receipt_id": str(row["receipt_id"]) + store + status + currency,
            }
            for row in inputs["Receipt"][:2]
        )
    access = access.model_copy(update={"allowed_store_ids": ["1"]})
    result = build_workspace(request, source, inputs, access, calendar)
    change = result["temporal_v2"]["changes"]["net_revenue"]
    assert (change["left"], change["right"], change["absolute_delta"]) == ("120", "0", "120")
    empty = access.model_copy(update={"allowed_store_ids": []})
    denied = build_workspace(request, source, inputs, empty, calendar)["temporal_v2"]
    assert denied["changes"]["net_revenue"]["left"] is None
    assert denied["changes"]["net_revenue"]["right"] is None
    assert denied["comparability_status"] == "unavailable"
    assert denied["content_hash"] != result["temporal_v2"]["content_hash"]
