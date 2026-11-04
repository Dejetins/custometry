"""Explicit filterable subset of the published retail-report/v1 profile."""

from __future__ import annotations

import hashlib
import json
from typing import Any
from uuid import UUID, uuid5

from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.columnar_filters import PublishedRetailFilter
from packages.contracts.semantic.filter_fields import FilterFieldVersion, FlatFilterRegistry


def retail_filter_projection(dataset: UUID, source: dict[str, Any]) -> PublishedRetailFilter:
    summary = source["summary"]
    if (
        summary.get("profile") != "retail-report/v1"
        or summary.get("namespace") != "northwind-retail"
        or source.get("capabilities", {}).get("receipts") != "available"
    ):
        raise AnalyticsFailure("FILTER_PROFILE_UNAVAILABLE")
    bindings = [b for b in source["bindings"] if b["entity"] == "Receipt"]
    if len(bindings) != 1 or bindings[0]["primary_key"] != ["source_system_id", "receipt_id"]:
        raise AnalyticsFailure("FILTER_PROFILE_BINDING")
    fields: list[FilterFieldVersion] = []
    for name in ("source_system_id", "store_id", "status", "currency", "receipt_date"):
        field = FilterFieldVersion(
            field_id=f"Receipt.{name}",
            version_id=uuid5(dataset, f"retail-filter/v1:{name}"),
            entity="Receipt",
            column=name,
            data_type="date" if name == "receipt_date" else "string",
            operators=("eq", "ne", "lt", "le", "gt", "ge", "in", "is_null", "is_not_null")
            if name == "receipt_date"
            else ("eq", "ne", "in", "is_null", "is_not_null"),
            null_policy="not_matched",
        )
        fields.append(field)
    revision = hashlib.sha256(
        json.dumps(
            {
                "publication": source["publication_hash"],
                "fields": [f.model_dump(mode="json") for f in fields],
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
    registry = FlatFilterRegistry(
        version_id=uuid5(dataset, revision),
        dataset_version_id=dataset,
        entity="Receipt",
        fields=tuple(fields),
    )
    return PublishedRetailFilter(
        registry=registry,
        artifact_id=UUID(bindings[0]["artifact_id"]),
        content_hash=bindings[0]["content_hash"],
        source_namespace=summary["namespace"],
        row_id_column="receipt_id",
    )
