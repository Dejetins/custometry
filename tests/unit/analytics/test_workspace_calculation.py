"""Focused v2 invariants; real intake evidence lives in integration/analytics."""

from __future__ import annotations
from datetime import UTC, date, datetime
from copy import deepcopy
from typing import Any
from uuid import uuid4
import pytest
from packages.analytics_core.application.workspace_calculation import (
    boundary,
    build_workspace,
    digest,
)
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.workspace import WorkspaceRunRequest, WorkspaceAccess, MetricRef
from packages.contracts.semantic import BusinessCalendarProfile, BusinessCalendarVersion
from packages.semantic_model.application.sales_metrics import definitions


def fixture():
    workspace, principal, dataset = uuid4(), uuid4(), uuid4()
    profile = BusinessCalendarProfile(fiscal_year_start_month=4)
    calendar = BusinessCalendarVersion(
        version_id=uuid4(),
        workspace_id=workspace,
        content_hash=digest(profile.model_dump(mode="json")),
        profile=profile,
        created_by=principal,
        created_at=datetime(2026, 1, 1, tzinfo=UTC),
        previous_version_id=None,
    )
    metrics = definitions()
    refs = [
        MetricRef.model_validate({k: m[k] for k in ("metric_id", "version_id", "content_hash")})
        for m in metrics
    ]
    request = WorkspaceRunRequest.model_validate(
        {
            "semantic_dataset_version_id": dataset,
            "common": {"starts_on": "2025-01-01", "ends_on": "2025-01-03", "store_ids": None},
            "local_store_ids": None,
            "grain": "month",
            "calendar_ref": {
                "version_id": calendar.version_id,
                "content_hash": calendar.content_hash,
            },
            "calendar_basis": "fiscal",
            "alignment": "previous_year_same_dates",
            "metric_refs": refs,
        }
    )
    access = WorkspaceAccess(
        workspace_id=workspace,
        principal_id=principal,
        semantic_dataset_version_id=dataset,
        policy_hash="a" * 64,
        allowed_store_ids=["1", "2"],
        permissions=frozenset({"analysis.read", "analysis.run", "workspace.read"}),
    )
    inputs: dict[str, Any] = {
        k: () for k in ("Customer", "Product", "Receipt", "ReceiptItem", "Store", "Calendar")
    }
    inputs["Store"] = ({"store_id": "1"}, {"store_id": "2"})
    inputs["Calendar"] = tuple(
        {"calendar_date": date(y, 1, d), "is_period_complete": True}
        for y in (2024, 2025)
        for d in (1, 2, 3)
    )
    inputs["Receipt"] = tuple(
        {
            "source_system_id": "test",
            "receipt_id": str(i),
            "receipt_datetime": datetime(y, 1, d, tzinfo=UTC),
            "store_id": "1",
            "status": "completed",
            "currency": "EUR",
            "net_amount": amount,
        }
        for i, (y, d, amount) in enumerate(
            ((2024, 1, "0"), (2025, 1, "100"), (2025, 2, "10"), (2025, 2, "10"))
        )
    )
    source: dict[str, Any] = {
        "metrics": metrics,
        "publication_hash": "b" * 64,
        "bindings": [
            {"entity": k, "artifact_id": str(uuid4()), "content_hash": "c" * 64} for k in inputs
        ],
    }
    return request, source, inputs, access, calendar


def test_zero_empty_ratio_clipping_and_decimal_canonicalization():
    req, source, inputs, access, calendar = fixture()
    result = build_workspace(req, source, inputs, access, calendar)
    assert result["totals"] == {"net_revenue": "120", "receipt_count": "3", "average_receipt": "40"}
    b = result["buckets"][0]
    assert b["clipped"] and b["coverage"]["state"] == "complete"
    assert b["fiscal_year"] == 2025 and b["fiscal_quarter"] == 4 and b["fiscal_half"] == 2
    assert result["daily"][2]["values"]["net_revenue"] is None
    change = result["temporal"]["changes"]["net_revenue"]
    assert (
        change["absolute_delta"] == "120"
        and change["relative_delta_percent"] is None
        and change["reason_codes"] == ["ZERO_BASELINE"]
    )
    duplicated = deepcopy(inputs)
    duplicated["ReceiptItem"] = ({"receipt_id": "1"},) * 500
    assert build_workspace(req, source, duplicated, access, calendar) == result


@pytest.mark.parametrize(
    "field", ["principal_id", "policy_hash", "calendar", "publication", "source_hash"]
)
def test_identity_partitions(field: str):
    req, source, inputs, access, calendar = fixture()
    old = build_workspace(req, source, inputs, access, calendar)["result_id"]
    if field == "principal_id":
        access = access.model_copy(update={"principal_id": uuid4()})
    elif field == "policy_hash":
        access = access.model_copy(update={"policy_hash": "d" * 64})
    elif field == "calendar":
        calendar = calendar.model_copy(update={"version_id": uuid4()})
        req = req.model_copy(
            update={
                "calendar_ref": req.calendar_ref.model_copy(
                    update={"version_id": calendar.version_id}
                )
            }
        )
    elif field == "publication":
        source["publication_hash"] = "d" * 64
    else:
        source["bindings"][0]["content_hash"] = "d" * 64
    assert build_workspace(req, source, inputs, access, calendar)["result_id"] != old


@pytest.mark.parametrize("amount", ["NaN", "Infinity", None])
def test_bad_amount_cannot_become_zero(amount: str | None):
    req, source, inputs, access, calendar = fixture()
    inputs["Receipt"][0]["net_amount"] = amount
    with pytest.raises(AnalyticsFailure, match="RECEIPT_AMOUNT_INVALID"):
        build_workspace(req, source, inputs, access, calendar)


def test_denied_duplicate_unknown_and_registry_mismatch():
    req, source, inputs, access, calendar = fixture()
    bad = req.model_copy(
        update={"metric_refs": [req.metric_refs[0].model_copy(update={"content_hash": "f" * 64})]}
    )
    with pytest.raises(AnalyticsFailure, match="METRIC_BASIS_MISMATCH"):
        build_workspace(bad, source, inputs, access, calendar)
    inputs["Receipt"] += (inputs["Receipt"][0],)
    with pytest.raises(AnalyticsFailure, match="RECEIPT_GRAIN_INVALID"):
        build_workspace(req, source, inputs, access, calendar)


def test_iso_week_is_current_axis_not_prior_iso_week():
    _, _, _, _, calendar = fixture()
    result = boundary(date(2025, 1, 1), "week", calendar, "fiscal")
    assert result["bucket_start"] == "2024-12-30" and result["bucket_end_exclusive"] == "2025-01-06"
    assert result["label"] == "2025-W01"


@pytest.mark.parametrize("start", range(1, 13))
def test_month_based_year_has_exact_anniversary(start: int):
    _, _, _, _, calendar = fixture()
    profile = calendar.profile.model_copy(update={"fiscal_year_start_month": start})
    calendar = calendar.model_copy(update={"profile": profile})
    b = boundary(date(2024, start, 1), "year", calendar, "fiscal")
    assert b["bucket_start"] == str(date(2024, start, 1))
    assert b["bucket_end_exclusive"] == str(date(2025, start, 1))


def test_provider_order_does_not_change_canonical_result_bytes():
    req, source, inputs, access, calendar = fixture()
    old = build_workspace(req, source, inputs, access, calendar)
    source["bindings"].reverse()
    source["metrics"].reverse()
    assert build_workspace(req, source, inputs, access, calendar) == old
