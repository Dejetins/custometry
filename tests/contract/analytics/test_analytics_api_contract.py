import json
from pathlib import Path

from custometry_api.analytics.router import create_analytics_app
from custometry_api.config import Settings
from custometry_api.main import create_app
from packages.contracts.analytics import ANALYTICS_API_VERSION


def settings() -> Settings:
    return Settings(
        version="0.1.0-dev.0",
        analytics_artifact_root=Path("/tmp/custometry-contract-artifacts"),
    )


def test_analytics_openapi_is_independently_versioned_and_mounted() -> None:
    analytics = create_analytics_app(settings())
    schema = analytics.openapi()
    parent = create_app(settings=settings())
    root = Path(__file__).resolve().parents[3]
    committed = json.loads(
        (root / "packages/contracts/openapi/analytics.openapi.json").read_text(encoding="utf-8")
    )

    assert schema == committed
    assert schema["info"]["version"] == ANALYTICS_API_VERSION
    assert schema["paths"]["/results"]["post"]["operationId"] == ("run_governed_analytics")
    assert schema["paths"]["/results"]["get"]["operationId"] == ("list_governed_analytics_results")
    assert "/analytics/results" not in parent.openapi()["paths"]
    assert any(getattr(route, "path", None) == "/analytics" for route in parent.routes)


def test_request_contract_is_typed_and_response_is_policy_safe() -> None:
    schema = create_analytics_app(settings()).openapi()
    request = schema["components"]["schemas"]["AnalyticsRunRequest"]
    typed_filter = schema["components"]["schemas"]["TypedFilterRequest"]
    comparison = schema["components"]["schemas"]["TimeComparisonRequest"]
    listing = schema["components"]["schemas"]["AnalyticsResultListResponse"]

    assert request["additionalProperties"] is False
    assert set(typed_filter["properties"]["field"]["enum"]) == {
        "store_id",
        "channel_id",
        "currency",
        "status",
        "net_amount",
    }
    assert "comparison_period" in comparison["properties"]
    assert {"leap_day_policy", "iso_week_53_policy", "incomplete_period_policy"}.issubset(
        comparison["required"]
    )
    assert "visible_count" in listing["required"]
    assert "total_count" not in listing["properties"]
