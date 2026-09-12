from copy import deepcopy
from datetime import UTC, date, datetime
from decimal import Decimal
from uuid import uuid4

import pytest
from pydantic import ValidationError

from custometry_api.analytics.sales_models import SalesRunRequest
from packages.analytics_core.application.sales_report import build_report
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.sales_report import SalesReportRequest
from packages.semantic_model.application.sales_metrics import definitions


def fixture():
    inputs = {k: () for k in ("Customer", "Product", "ReceiptItem", "Receipt", "Calendar", "Store")}
    inputs["Calendar"] = tuple(
        {"calendar_date": date(y, 1, d), "is_period_complete": True}
        for y in (2024, 2025)
        for d in (1, 2, 3)
    )
    inputs["Store"] = ({"store_id": "1"},)
    inputs["Receipt"] = tuple(
        {
            "source_system_id": "test",
            "receipt_id": str(i),
            "receipt_datetime": datetime(2025, 1, d, tzinfo=UTC),
            "store_id": "1",
            "status": "completed",
            "currency": "EUR",
            "net_amount": amount,
            "customer_id": None,
        }
        for i, d, amount in ((1, 1, "100"), (2, 2, "10"), (3, 2, "10"))
    )
    source = {
        "metrics": definitions(),
        "bindings": [{"entity": k, "artifact_id": str(uuid4())} for k in inputs],
        "publication_hash": "a" * 64,
        "summary": {
            "artifact_hashes": {},
            "relationship_policy": "current-only",
            "quality_accounting": {"quarantined_count": 5},
            "raw_artifacts": {},
            "quarantine_artifact": "q",
        },
        "quality_report_id": str(uuid4()),
        "capabilities": {"basket": "degraded"},
    }
    request = SalesReportRequest(uuid4(), date(2025, 1, 1), date(2025, 1, 3))
    return request, source, inputs


def test_ratio_grain_empty_and_immutable_definitions():
    request, source, inputs = fixture()
    result = build_report(request, source, inputs, "policy")
    assert result["totals"] == {"net_revenue": "120", "receipt_count": "3", "average_receipt": "40"}
    assert (
        Decimal(result["totals"]["average_receipt"])
        != sum(Decimal(r["average_receipt"]) for r in result["daily"][:2]) / 2
    )
    assert result["daily"][2]["state"] == "no_eligible_receipts"
    assert result["daily"][2]["net_revenue"] is None
    assert len(result["lineage"]["bindings"]) == 6
    assert source["metrics"][2]["numerator_version_id"] == source["metrics"][0]["version_id"]
    assert definitions() == definitions()
    extra = deepcopy(inputs)
    extra["ReceiptItem"] = ({"receipt_id": "1"},) * 300
    assert build_report(request, source, extra, "policy")["totals"] == result["totals"]


@pytest.mark.parametrize("amount", [None, "NaN", "Infinity"])
def test_invalid_amount_is_never_zero(amount):
    request, source, inputs = fixture()
    inputs["Receipt"][0]["net_amount"] = amount
    with pytest.raises(AnalyticsFailure, match="RECEIPT_AMOUNT_INVALID"):
        build_report(request, source, inputs, "policy")


def test_currency_status_negative_and_duplicate():
    request, source, inputs = fixture()
    inputs["Receipt"][0]["currency"] = "SEK"
    inputs["Receipt"][1]["status"] = "cancelled"
    inputs["Receipt"][2]["net_amount"] = "-10"
    assert build_report(request, source, inputs, "policy")["totals"]["net_revenue"] == "-10"
    inputs["Receipt"] += (inputs["Receipt"][2],)
    with pytest.raises(AnalyticsFailure, match="RECEIPT_GRAIN_INVALID"):
        build_report(request, source, inputs, "policy")


def test_coverage_policy_identity_and_dates():
    request, source, inputs = fixture()
    result = build_report(request, source, inputs, "a")
    assert build_report(request, source, inputs, "b")["result_id"] != result["result_id"]
    compared = SalesReportRequest(
        request.semantic_dataset_version_id,
        request.starts_on,
        request.ends_on,
        comparison="previous_year_same_dates",
    )
    inputs["Calendar"][0]["is_period_complete"] = False
    partial = build_report(compared, source, inputs, "a")
    assert partial["comparability_status"] == "not_comparable"
    assert partial["comparison"]["totals"]["receipt_count"] is None
    leap = SalesReportRequest(
        request.semantic_dataset_version_id,
        date(2024, 2, 29),
        date(2024, 2, 29),
        comparison="previous_year_same_dates",
    )
    assert (
        "LEAP_DAY_SAME_DATE_UNAVAILABLE"
        in build_report(leap, source, inputs, "a")["trust"]["limitations"]
    )
    with pytest.raises(AnalyticsFailure, match="INVALID_BOUNDED_PERIOD"):
        SalesReportRequest(uuid4(), date(2024, 1, 1), date(2025, 1, 1)).validate()


@pytest.mark.parametrize(
    "dimension", ["product_id", "category", "brand", "customer_id", "currency", "status"]
)
def test_unsupported_controls_rejected(dimension):
    with pytest.raises(ValidationError):
        SalesRunRequest.model_validate(
            {"semantic_dataset_version_id": str(uuid4()), dimension: "x"}
        )


def test_storage_failure_is_stable(tmp_path):
    from packages.artifacts.infrastructure.sales import SalesArtifactStore

    request, source, inputs = fixture()
    payload = build_report(request, source, inputs, "policy")
    (tmp_path / ".staging").write_text("blocked directory")
    with pytest.raises(AnalyticsFailure, match="RESULT_STORAGE_UNAVAILABLE"):
        SalesArtifactStore(lambda: None, tmp_path).commit_sales(
            workspace_id=uuid4(), payload=payload
        )


def test_timezone_normalizes_to_utc():
    from datetime import timedelta, timezone

    request, source, inputs = fixture()
    inputs["Receipt"][0]["receipt_datetime"] = datetime(
        2025, 1, 2, 1, tzinfo=timezone(timedelta(hours=2))
    )
    result = build_report(request, source, inputs, "policy")
    assert result["daily"][0]["net_revenue"] == "100"
    assert result["daily"][1]["net_revenue"] == "20"
