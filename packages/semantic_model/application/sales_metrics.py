"""Immutable definitions for the selected receipt-header sales report."""

from __future__ import annotations

import hashlib
import json
from uuid import UUID, uuid5

NAMESPACE = UUID("93f1806c-ea66-5758-a81b-9c68a691de63")
POLICY = "completed-eur-receipt/v1"


def definitions() -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    references: dict[str, str] = {}
    for key, kind, expression, en, ru, unit in (
        (
            "net_revenue",
            "additive_measure",
            "sum(net_amount)",
            "Net revenue",
            "Выручка нетто",
            "EUR",
        ),
        (
            "receipt_count",
            "event_count",
            "count_distinct(source_system_id,receipt_id)",
            "Receipts",
            "Чеки",
            "receipt",
        ),
        (
            "average_receipt",
            "derived_ratio",
            "net_revenue/receipt_count",
            "Average receipt",
            "Средний чек",
            "EUR/receipt",
        ),
    ):
        definition: dict[str, object] = {
            "metric_id": key,
            "schema_version": "sales-metric/v1",
            "metric_kind": kind,
            "expression": expression,
            "source_grain": ["source_system_id", "receipt_id"],
            "fact_scope": "receipt_header",
            "allowed_dimensions": ["date", "store_id"],
            "aggregation": "recompute_ratio" if kind == "derived_ratio" else "sum",
            "time_aggregation": "recompute_ratio" if kind == "derived_ratio" else "sum",
            "unit": unit,
            "format": {"decimal_places": 0 if key == "receipt_count" else 2},
            "labels": {"en": en, "ru": ru},
            "timezone": "UTC",
            "eligibility": {
                "status": "completed",
                "currency": "EUR",
                "locked": True,
                "policy_version": POLICY,
            },
            "return_policy": "exclude_non_completed_not_refund_adjusted",
            "null_policy": "reject_null_amount;empty_is_unavailable",
            "numerator_version_id": references.get("net_revenue")
            if kind == "derived_ratio"
            else None,
            "denominator_version_id": references.get("receipt_count")
            if kind == "derived_ratio"
            else None,
        }
        digest = hashlib.sha256(
            json.dumps(definition, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        version_id = str(uuid5(NAMESPACE, digest))
        references[key] = version_id
        result.append({**definition, "version_id": version_id, "content_hash": digest})
    return result
