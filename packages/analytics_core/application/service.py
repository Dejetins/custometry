from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping
from datetime import date, datetime
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
from typing import Protocol
from uuid import UUID, uuid5

from packages.analytics_core.domain.model import (
    AnalyticsRequest,
    FilterPredicate,
    Period,
    decimal_value,
)
from packages.contracts.analytics import (
    AnalyticsFailure,
    SemanticProjectionPort,
    TabularArtifactPort,
)


RESULT_NAMESPACE = UUID("2ef8434d-0b48-50be-9b97-bf41a1a8aef1")


class ResultRepository(Protocol):
    def find_by_request_hash(
        self, *, workspace_id: UUID, request_hash: str
    ) -> dict[str, object] | None: ...
    def save(self, record: Mapping[str, object]) -> None: ...
    def get_visible(
        self, *, workspace_id: UUID, principal_id: UUID, result_id: UUID
    ) -> dict[str, object]: ...
    def list_visible(
        self, *, workspace_id: UUID, principal_id: UUID, offset: int, limit: int
    ) -> tuple[tuple[dict[str, object], ...], int]: ...


class ResultArtifactStore(Protocol):
    def commit_json(
        self, *, result_id: UUID, payload: Mapping[str, object]
    ) -> tuple[str, str, int]: ...


def _canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def _sha(value: object) -> str:
    return hashlib.sha256(_canonical(value).encode()).hexdigest()


def _row_date(row: Mapping[str, object]) -> date:
    value = row.get("receipt_datetime")
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return datetime.fromisoformat(str(value)).date()


def _matches(row: Mapping[str, object], predicate: FilterPredicate) -> bool:
    actual = row.get(predicate.field)
    if predicate.field == "net_amount":
        actual_decimal = decimal_value(actual)
        expected = predicate.value
        assert isinstance(expected, Decimal)
        return {
            "eq": actual_decimal == expected,
            "gte": actual_decimal >= expected,
            "lte": actual_decimal <= expected,
        }[predicate.operator]
    actual_text = str(actual)
    if predicate.operator == "eq":
        return actual_text == predicate.value
    expected_items = predicate.value
    assert isinstance(expected_items, tuple)
    return actual_text in expected_items


def _eligible(
    rows: tuple[dict[str, object], ...], filters: tuple[FilterPredicate, ...]
) -> tuple[dict[str, object], ...]:
    return tuple(row for row in rows if all(_matches(row, predicate) for predicate in filters))


def _in_period(
    rows: tuple[dict[str, object], ...], period: Period
) -> tuple[dict[str, object], ...]:
    return tuple(row for row in rows if period.starts_on <= _row_date(row) <= period.ends_on)


def _qualified_customer(source_system_id: UUID, row: Mapping[str, object]) -> str | None:
    value = row.get("customer_id")
    return None if value is None else f"{source_system_id}:{value}"


def _basic_metrics(
    rows: tuple[dict[str, object], ...], source_system_id: UUID
) -> dict[str, Decimal | None]:
    if not rows:
        return {
            key: None
            for key in (
                "net_revenue",
                "gross_revenue",
                "discount_amount",
                "receipt_count",
                "customer_count",
                "average_receipt",
                "revenue_per_customer",
            )
        }
    net = sum((decimal_value(row["net_amount"]) for row in rows), Decimal(0))
    gross = sum((decimal_value(row["gross_amount"]) for row in rows), Decimal(0))
    discount = sum((decimal_value(row["discount_amount"]) for row in rows), Decimal(0))
    receipt_count = Decimal(len({str(row["receipt_id"]) for row in rows}))
    customers = {
        value for row in rows if (value := _qualified_customer(source_system_id, row)) is not None
    }
    customer_count = Decimal(len(customers))
    return {
        "net_revenue": net,
        "gross_revenue": gross,
        "discount_amount": discount,
        "receipt_count": receipt_count,
        "customer_count": customer_count,
        "average_receipt": net / receipt_count,
        "revenue_per_customer": net / customer_count if customer_count else None,
    }


def _customer_metrics(
    all_rows: tuple[dict[str, object], ...],
    current: tuple[dict[str, object], ...],
    comparison: tuple[dict[str, object], ...],
    source_system_id: UUID,
    current_period: Period,
    comparison_period: Period | None,
) -> dict[str, Decimal | None]:
    if not current and not comparison:
        return {
            key: None
            for key in (
                "active_customers",
                "new_customers",
                "retained_customers",
                "reactivated_customers",
                "churned_customers",
            )
        }
    current_ids = {_qualified_customer(source_system_id, row) for row in current} - {None}
    comparison_ids = {_qualified_customer(source_system_id, row) for row in comparison} - {None}
    first_dates: dict[str, date] = {}
    for row in all_rows:
        customer = _qualified_customer(source_system_id, row)
        if customer is not None:
            first_dates[customer] = min(first_dates.get(customer, _row_date(row)), _row_date(row))
    historical_before_comparison = {
        _qualified_customer(source_system_id, row)
        for row in all_rows
        if comparison_period is not None and _row_date(row) < comparison_period.starts_on
    } - {None}
    return {
        "active_customers": Decimal(len(current_ids)),
        "new_customers": Decimal(
            sum(
                current_period.starts_on <= first_dates[item] <= current_period.ends_on
                for item in current_ids
            )
        ),
        "retained_customers": Decimal(len(current_ids & comparison_ids)),
        "reactivated_customers": Decimal(
            len((current_ids - comparison_ids) & historical_before_comparison)
        ),
        "churned_customers": Decimal(len(comparison_ids - current_ids)),
    }


def _rfm(
    rows: tuple[dict[str, object], ...],
    source_system_id: UUID,
    *,
    as_of: date,
    bins: int,
    frequency_measure: str,
) -> tuple[dict[str, Decimal | None], list[dict[str, object]]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        customer = _qualified_customer(source_system_id, row)
        if customer is not None and _row_date(row) <= as_of:
            grouped[customer].append(row)
    features: list[dict[str, object]] = []
    for customer, customer_rows in sorted(grouped.items()):
        purchase_dates = {_row_date(row) for row in customer_rows}
        features.append(
            {
                "customer": customer,
                "recency": Decimal((as_of - max(purchase_dates)).days),
                "frequency": Decimal(
                    len(customer_rows)
                    if frequency_measure == "receipt_count"
                    else len(purchase_dates)
                ),
                "monetary": sum(
                    (decimal_value(row["net_amount"]) for row in customer_rows), Decimal(0)
                ),
            }
        )
    if not features:
        return {
            "rfm_customers": None,
            "recency_days_avg": None,
            "frequency_avg": None,
            "monetary_avg": None,
        }, []
    for field, reverse in (("recency", True), ("frequency", False), ("monetary", False)):
        ordered = sorted(
            features, key=lambda item: (item[field], item["customer"]), reverse=reverse
        )
        for index, item in enumerate(ordered):
            item[f"{field}_score"] = min(bins, (index * bins // len(ordered)) + 1)
    profiles: list[dict[str, object]] = []
    for item in sorted(features, key=lambda value: str(value["customer"])):
        r = int(item["recency_score"])
        f = int(item["frequency_score"])
        m = int(item["monetary_score"])
        segment = (
            "champions"
            if min(r, f, m) >= bins - 1
            else "loyal"
            if f >= bins - 1
            else "at_risk"
            if r <= 2
            else "developing"
        )
        profiles.append(
            {
                "customer_key": hashlib.sha256(str(item["customer"]).encode()).hexdigest(),
                "recency_days": str(item["recency"]),
                "frequency": str(item["frequency"]),
                "monetary": str(item["monetary"]),
                "r_score": r,
                "f_score": f,
                "m_score": m,
                "segment": segment,
            }
        )
    count = Decimal(len(features))
    return {
        "rfm_customers": count,
        "recency_days_avg": sum((item["recency"] for item in features), Decimal(0)) / count,
        "frequency_avg": sum((item["frequency"] for item in features), Decimal(0)) / count,
        "monetary_avg": sum((item["monetary"] for item in features), Decimal(0)) / count,
    }, profiles


GROUPS: dict[str, tuple[tuple[str, tuple[str, ...]], ...]] = {
    "sales": (
        ("finance", ("net_revenue", "gross_revenue", "discount_amount")),
        (
            "commerce",
            ("receipt_count", "customer_count", "average_receipt", "revenue_per_customer"),
        ),
    ),
    "customer": (
        (
            "customer_base",
            (
                "active_customers",
                "new_customers",
                "retained_customers",
                "reactivated_customers",
                "churned_customers",
            ),
        ),
    ),
    "rfm": (("rfm", ("rfm_customers", "recency_days_avg", "frequency_avg", "monetary_avg")),),
}


def _compact(value: Decimal | None) -> str | None:
    if value is None:
        return None
    magnitude = abs(value)
    for divisor, suffix in (
        (Decimal("1000000000"), "B"),
        (Decimal("1000000"), "M"),
        (Decimal("1000"), "K"),
    ):
        if magnitude >= divisor:
            return f"{(value / divisor).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)}{suffix}"
    return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def _metric_groups(
    current: Mapping[str, Decimal | None],
    comparison: Mapping[str, Decimal | None],
    result_type: str,
    limitations: list[str],
) -> list[dict[str, object]]:
    groups: list[dict[str, object]] = []
    for group_index, (group_id, metric_ids) in enumerate(GROUPS[result_type], start=1):
        metrics: list[dict[str, object]] = []
        for metric_index, metric_id in enumerate(metric_ids, start=1):
            current_value = current.get(metric_id)
            comparison_value = comparison.get(metric_id)
            absolute = (
                current_value - comparison_value
                if current_value is not None and comparison_value is not None
                else None
            )
            percent = (
                absolute / abs(comparison_value) * 100
                if absolute is not None and comparison_value not in {None, Decimal(0)}
                else None
            )
            metric_limitations = list(limitations)
            if comparison_value == 0 and current_value is not None:
                metric_limitations.append("COMPARISON_ZERO_PERCENT_UNDEFINED")
            metrics.append(
                {
                    "metric_id": metric_id,
                    "metric_order": metric_index * 10,
                    "current_value": None if current_value is None else str(current_value),
                    "comparison_value": None if comparison_value is None else str(comparison_value),
                    "absolute_change": None if absolute is None else str(absolute),
                    "percent_change": None if percent is None else str(percent),
                    "compact_current": _compact(current_value),
                    "compact_comparison": _compact(comparison_value),
                    "limitation_codes": sorted(set(metric_limitations)),
                }
            )
        groups.append({"group_id": group_id, "group_order": group_index * 10, "metrics": metrics})
    return groups


class AnalyticsService:
    def __init__(
        self,
        *,
        projections: SemanticProjectionPort,
        artifacts: TabularArtifactPort,
        results: ResultRepository,
        result_store: ResultArtifactStore,
    ) -> None:
        self._projections = projections
        self._artifacts = artifacts
        self._results = results
        self._result_store = result_store

    def run(
        self,
        *,
        workspace_id: UUID,
        principal_id: UUID,
        permissions: frozenset[str],
        request: AnalyticsRequest,
    ) -> dict[str, object]:
        if "analysis.run" not in permissions:
            raise AnalyticsFailure("FORBIDDEN")
        request.validate()
        source = self._projections.get_published_projection(
            workspace_id=workspace_id,
            semantic_dataset_version_id=request.semantic_dataset_version_id,
        )
        if source.quality_decision not in {"passed", "passed_with_waivers"}:
            raise AnalyticsFailure("DATA_QUALITY_BLOCKED")
        receipt_binding = next((item for item in source.bindings if item.entity == "Receipt"), None)
        if receipt_binding is None:
            raise AnalyticsFailure("RECEIPT_ARTIFACT_REQUIRED")
        source_hashes = {item.entity: item.content_hash for item in source.bindings}
        policy_hash = _sha(
            {
                "workspace_id": workspace_id,
                "principal_id": principal_id,
                "permissions": sorted(permissions),
            }
        )
        normalized = {
            "workspace_id": workspace_id,
            "principal_id": principal_id,
            "result_type": request.result_type,
            "semantic_dataset_version_id": request.semantic_dataset_version_id,
            "comparison": request.comparison,
            "filters": request.filters,
            "rfm_score_bins": request.rfm_score_bins,
            "rfm_frequency_measure": request.rfm_frequency_measure,
            "rfm_segment_rule_set_version": request.rfm_segment_rule_set_version,
            "source_hashes": source_hashes,
            "policy_hash": policy_hash,
            "code_version": "analytics-v1",
        }
        request_hash = _sha(normalized)
        existing = self._results.find_by_request_hash(
            workspace_id=workspace_id, request_hash=request_hash
        )
        if existing is not None:
            return existing
        all_rows = _eligible(self._artifacts.read_rows(receipt_binding), request.filters)
        current_rows = _in_period(all_rows, request.comparison.current_period)
        comparison_rows = (
            ()
            if request.comparison.comparison_period is None
            else _in_period(all_rows, request.comparison.comparison_period)
        )
        profiles: list[dict[str, object]] = []
        if request.result_type == "sales":
            current_metrics = _basic_metrics(current_rows, receipt_binding.source_system_id)
            comparison_metrics = _basic_metrics(comparison_rows, receipt_binding.source_system_id)
        elif request.result_type == "customer":
            current_metrics = _customer_metrics(
                all_rows,
                current_rows,
                comparison_rows,
                receipt_binding.source_system_id,
                request.comparison.current_period,
                request.comparison.comparison_period,
            )
            comparison_metrics = _customer_metrics(
                all_rows,
                comparison_rows,
                (),
                receipt_binding.source_system_id,
                request.comparison.comparison_period or request.comparison.current_period,
                None,
            )
        else:
            current_metrics, profiles = _rfm(
                current_rows,
                receipt_binding.source_system_id,
                as_of=request.comparison.current_period.ends_on,
                bins=request.rfm_score_bins,
                frequency_measure=request.rfm_frequency_measure,
            )
            comparison_metrics, _ = _rfm(
                comparison_rows,
                receipt_binding.source_system_id,
                as_of=(
                    request.comparison.comparison_period or request.comparison.current_period
                ).ends_on,
                bins=request.rfm_score_bins,
                frequency_measure=request.rfm_frequency_measure,
            )
        limitations = [] if request.comparison.mode != "none" else ["COMPARISON_DISABLED"]
        current_dates = {_row_date(row) for row in current_rows}
        comparison_dates = {_row_date(row) for row in comparison_rows}
        comparability = (
            "not_comparable"
            if request.comparison.mode == "none"
            else "comparable"
            if len(current_dates) == len(comparison_dates)
            else "partial"
        )
        result_id = uuid5(RESULT_NAMESPACE, request_hash)
        payload: dict[str, object] = {
            "result_id": str(result_id),
            "result_type": request.result_type,
            "semantic_dataset_version_id": str(request.semantic_dataset_version_id),
            "request_hash": request_hash,
            "policy_hash": policy_hash,
            "applied_comparison_mode": request.comparison.mode,
            "resolved_current_period": {
                "starts_on": str(request.comparison.current_period.starts_on),
                "ends_on": str(request.comparison.current_period.ends_on),
            },
            "resolved_comparison_period": None
            if request.comparison.comparison_period is None
            else {
                "starts_on": str(request.comparison.comparison_period.starts_on),
                "ends_on": str(request.comparison.comparison_period.ends_on),
            },
            "timezone": request.comparison.timezone,
            "calendar_version_id": str(request.comparison.calendar_version_id),
            "comparison_policy_hash": _sha(request.comparison),
            "normalized_filter_expression_hash": _sha(request.filters),
            "metric_groups": _metric_groups(
                current_metrics, comparison_metrics, request.result_type, limitations
            ),
            "current_coverage": {
                "observed_days": len(current_dates),
                "period_days": (
                    request.comparison.current_period.ends_on
                    - request.comparison.current_period.starts_on
                ).days
                + 1,
            },
            "comparison_coverage": None
            if request.comparison.comparison_period is None
            else {
                "observed_days": len(comparison_dates),
                "period_days": (
                    request.comparison.comparison_period.ends_on
                    - request.comparison.comparison_period.starts_on
                ).days
                + 1,
            },
            "comparability_status": comparability,
            "limitation_codes": limitations,
            "quality": {
                "decision": source.quality_decision,
                "capabilities": source.capability_matrix,
            },
            "freshness": {
                "max_event_date": None
                if not all_rows
                else str(max(_row_date(row) for row in all_rows))
            },
            "lineage": {
                "source_artifact_ids": [str(item.artifact_id) for item in source.bindings],
                "source_content_hashes": source_hashes,
                "canonical_customer_key": "sha256(source_system_id:customer_id)",
                "fact_scope": "receipt_header",
            },
            "rfm_profiles": profiles,
        }
        relative_uri, content_hash, byte_size = self._result_store.commit_json(
            result_id=result_id, payload=payload
        )
        payload["manifest"] = {
            "relative_uri": relative_uri,
            "content_hash": content_hash,
            "byte_size": byte_size,
            "immutable": True,
        }
        self._results.save(
            {
                "id": result_id,
                "workspace_id": workspace_id,
                "owner_principal_id": principal_id,
                "semantic_dataset_version_id": request.semantic_dataset_version_id,
                "result_type": request.result_type,
                "request_hash": request_hash,
                "policy_hash": policy_hash,
                "response_payload": payload,
                "storage_uri": relative_uri,
                "content_hash": content_hash,
                "byte_size": byte_size,
            }
        )
        return payload

    def get(
        self,
        *,
        workspace_id: UUID,
        principal_id: UUID,
        permissions: frozenset[str],
        result_id: UUID,
    ) -> dict[str, object]:
        if "analysis.read" not in permissions:
            raise AnalyticsFailure("FORBIDDEN")
        return self._results.get_visible(
            workspace_id=workspace_id, principal_id=principal_id, result_id=result_id
        )

    def list(
        self,
        *,
        workspace_id: UUID,
        principal_id: UUID,
        permissions: frozenset[str],
        offset: int,
        limit: int,
    ) -> tuple[tuple[dict[str, object], ...], int]:
        if "analysis.read" not in permissions:
            raise AnalyticsFailure("FORBIDDEN")
        return self._results.list_visible(
            workspace_id=workspace_id, principal_id=principal_id, offset=offset, limit=limit
        )
