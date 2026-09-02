from __future__ import annotations

from dataclasses import replace
from datetime import UTC, date, datetime
from decimal import Decimal
import hashlib
import json
from typing import Any
from uuid import UUID, uuid4

import pytest

from packages.analytics_core.application.service import AnalyticsService
from packages.analytics_core.domain.model import (
    AnalyticsRequest,
    FilterPredicate,
    Period,
    TimeComparison,
)
from packages.contracts.analytics import (
    AnalyticsFailure,
    PublishedSemanticProjection,
    SemanticArtifactBinding,
)


WORKSPACE = UUID("10000000-0000-0000-0000-000000000001")
PRINCIPAL = UUID("20000000-0000-0000-0000-000000000001")
SEMANTIC = UUID("30000000-0000-0000-0000-000000000001")
SOURCE = UUID("40000000-0000-0000-0000-000000000001")
CALENDAR = UUID("60000000-0000-0000-0000-000000000001")
BINDING = SemanticArtifactBinding(
    entity="Receipt",
    artifact_id=UUID("50000000-0000-0000-0000-000000000001"),
    relative_uri="objects/receipt.parquet",
    content_hash="a" * 64,
    source_system_id=SOURCE,
)


def receipt(
    receipt_id: str,
    occurred: str,
    customer: str | None,
    net: str,
    gross: str,
    discount: str,
    *,
    channel: str = "store",
    status: str = "completed",
) -> dict[str, object]:
    return {
        "receipt_id": receipt_id,
        "receipt_datetime": datetime.fromisoformat(occurred).replace(tzinfo=UTC),
        "customer_id": customer,
        "store_id": "s1",
        "channel_id": channel,
        "currency": "EUR",
        "net_amount": Decimal(net),
        "gross_amount": Decimal(gross),
        "discount_amount": Decimal(discount),
        "status": status,
    }


ROWS = (
    receipt("r1", "2024-01-10T12:00:00", "a", "100", "120", "20"),
    receipt("r2", "2024-02-10T12:00:00", "b", "200", "200", "0", channel="web"),
    receipt("r0", "2023-01-10T12:00:00", "c", "50", "50", "0"),
    receipt("r3", "2025-01-10T12:00:00", "a", "150", "180", "30"),
    receipt("r4", "2025-02-10T12:00:00", "c", "300", "320", "20", channel="web"),
    receipt("r5", "2026-03-10T12:00:00", "b", "999", "999", "0", status="cancelled"),
)


class ProjectionPort:
    def get_published_projection(self, **_: object) -> PublishedSemanticProjection:
        return PublishedSemanticProjection(
            semantic_dataset_version_id=SEMANTIC,
            workspace_id=WORKSPACE,
            quality_decision="passed_with_waivers",
            capability_matrix={"customer": "available", "receipts": "available"},
            bindings=(BINDING,),
        )


class ArtifactPort:
    def read_rows(self, binding: SemanticArtifactBinding) -> tuple[dict[str, object], ...]:
        assert binding == BINDING
        return ROWS


class MemoryResults:
    def __init__(self) -> None:
        self.items: dict[str, dict[str, object]] = {}
        self.commits = 0

    def find_by_request_hash(self, *, request_hash: str, **_: object) -> dict[str, object] | None:
        return self.items.get(request_hash)

    def save(self, record: dict[str, object]) -> None:
        self.items[str(record["request_hash"])] = dict(record["response_payload"])

    def get_visible(self, **kwargs: object) -> dict[str, object]:
        result_id = str(kwargs["result_id"])
        for item in self.items.values():
            if item["result_id"] == result_id and kwargs["principal_id"] == PRINCIPAL:
                return item
        raise AnalyticsFailure("NOT_FOUND")

    def list_visible(self, **kwargs: object) -> tuple[tuple[dict[str, object], ...], int]:
        if kwargs["principal_id"] != PRINCIPAL:
            return (), 0
        items = tuple(self.items.values())
        return items, len(items)

    def commit_json(self, *, result_id: UUID, payload: object) -> tuple[str, str, int]:
        self.commits += 1
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode()
        return f"analytics-results/{result_id}.json", hashlib.sha256(raw).hexdigest(), len(raw)


@pytest.fixture
def service() -> tuple[AnalyticsService, MemoryResults]:
    memory = MemoryResults()
    return (
        AnalyticsService(
            projections=ProjectionPort(),
            artifacts=ArtifactPort(),
            results=memory,
            result_store=memory,
        ),
        memory,
    )


def comparison(mode: str = "previous_year_same_dates") -> TimeComparison:
    return TimeComparison(
        mode=mode,  # type: ignore[arg-type]
        current_period=Period(date(2025, 1, 1), date(2025, 12, 31)),
        comparison_period=(
            None if mode == "none" else Period(date(2024, 1, 1), date(2024, 12, 30))
        ),
        timezone="UTC",
        calendar_version_id=CALENDAR,
        incomplete_period_policy="explicit_partial",
        leap_day_policy="calendar_map",
        iso_week_53_policy="explicit_partial",
        definition_compatibility_policy="require_same_versions",
    )


def request(result_type: str = "sales", **kwargs: Any) -> AnalyticsRequest:
    return AnalyticsRequest(
        result_type=result_type,  # type: ignore[arg-type]
        semantic_dataset_version_id=SEMANTIC,
        comparison=kwargs.pop("comparison", comparison()),
        **kwargs,
    )


def run(service: AnalyticsService, payload: AnalyticsRequest) -> dict[str, object]:
    return service.run(
        workspace_id=WORKSPACE,
        principal_id=PRINCIPAL,
        permissions=frozenset({"analysis.run", "analysis.read"}),
        request=payload,
    )


def metrics(payload: dict[str, object]) -> dict[str, dict[str, object]]:
    return {
        metric["metric_id"]: metric
        for group in payload["metric_groups"]  # type: ignore[union-attr]
        for metric in group["metrics"]
    }


def test_sales_golden_values_comparison_and_order(
    service: tuple[AnalyticsService, MemoryResults],
) -> None:
    analytics, _ = service
    result = run(analytics, request())
    values = metrics(result)
    assert [group["group_id"] for group in result["metric_groups"]] == ["finance", "commerce"]  # type: ignore[index]
    assert values["net_revenue"]["current_value"] == "450"
    assert values["net_revenue"]["comparison_value"] == "300"
    assert values["net_revenue"]["absolute_change"] == "150"
    assert values["net_revenue"]["percent_change"] == "50.0"
    assert values["receipt_count"]["current_value"] == "2"
    assert values["customer_count"]["current_value"] == "2"
    assert result["comparability_status"] == "comparable"
    assert result["lineage"]["fact_scope"] == "receipt_header"  # type: ignore[index]


def test_typed_filter_and_customer_lifecycle(
    service: tuple[AnalyticsService, MemoryResults],
) -> None:
    analytics, _ = service
    filtered = run(
        analytics,
        request(filters=(FilterPredicate("channel_id", "eq", "web"),)),
    )
    assert metrics(filtered)["net_revenue"]["current_value"] == "300"
    customer = run(analytics, request("customer"))
    values = metrics(customer)
    assert values["active_customers"]["current_value"] == "2"
    assert values["new_customers"]["current_value"] == "0"
    assert values["retained_customers"]["current_value"] == "1"
    assert values["reactivated_customers"]["current_value"] == "1"
    assert values["churned_customers"]["current_value"] == "1"


def test_rfm_scores_are_deterministic_bounded_and_redacted(
    service: tuple[AnalyticsService, MemoryResults],
) -> None:
    analytics, _ = service
    first = run(analytics, request("rfm"))
    second = run(analytics, request("rfm"))
    assert first["result_id"] == second["result_id"]
    assert first["rfm_profiles"] == second["rfm_profiles"]
    for profile in first["rfm_profiles"]:  # type: ignore[union-attr]
        assert len(profile["customer_key"]) == 64
        assert 1 <= profile["r_score"] <= 5
        assert 1 <= profile["f_score"] <= 5
        assert 1 <= profile["m_score"] <= 5
        assert "customer_id" not in profile


def test_repeated_request_is_single_identity_and_hidden_counts_do_not_leak(
    service: tuple[AnalyticsService, MemoryResults],
) -> None:
    analytics, memory = service
    result = run(analytics, request())
    replay = run(analytics, request())
    assert replay == result
    assert memory.commits == 1
    visible, visible_count = analytics.list(
        workspace_id=WORKSPACE,
        principal_id=PRINCIPAL,
        permissions=frozenset({"analysis.read"}),
        offset=0,
        limit=50,
    )
    hidden, hidden_count = analytics.list(
        workspace_id=WORKSPACE,
        principal_id=uuid4(),
        permissions=frozenset({"analysis.read"}),
        offset=0,
        limit=50,
    )
    assert len(visible) == visible_count == 1
    assert hidden == () and hidden_count == 0
    with pytest.raises(AnalyticsFailure, match="NOT_FOUND"):
        analytics.get(
            workspace_id=WORKSPACE,
            principal_id=uuid4(),
            permissions=frozenset({"analysis.read"}),
            result_id=UUID(str(result["result_id"])),
        )


@pytest.mark.parametrize(
    ("predicate", "code"),
    [
        (FilterPredicate("channel_id", "gte", "web"), "FILTER_OPERATOR_TYPE_MISMATCH"),
        (FilterPredicate("net_amount", "in", ("1",)), "FILTER_VALUE_TYPE_MISMATCH"),
    ],
)
def test_invalid_typed_filters_fail_closed(predicate: FilterPredicate, code: str) -> None:
    with pytest.raises(AnalyticsFailure, match=code):
        predicate.validate()


def test_comparison_requires_explicit_period_and_policy() -> None:
    missing = replace(comparison(), comparison_period=None)
    with pytest.raises(AnalyticsFailure, match="COMPARISON_PERIOD_REQUIRED"):
        missing.validate()
    wrong_policy = replace(
        comparison("previous_year_comparable_elapsed_days"),
        incomplete_period_policy="exclude",
    )
    with pytest.raises(AnalyticsFailure, match="INCOMPLETE_PERIOD_POLICY_MISMATCH"):
        wrong_policy.validate()
