"""Exact six-entity retail report projection and current-only relationships."""

import hashlib
import json
from datetime import UTC, date, datetime
from uuid import UUID, uuid5

from packages.contracts.data_pipeline import DataPipelineFailure
from packages.semantic_model.domain.model import SemanticDatasetPublication, SemanticEntityBinding

PROFILE = "retail-report/v1"
NAMESPACE = "northwind-retail"
RELATIONSHIP_POLICY = "retail-report-current-only/v1"
KEYS = {
    "Customer": ("customer_version_id",),
    "Product": ("product_version_id",),
    "Store": ("store_version_id",),
    "Calendar": ("source_system_id", "calendar_date"),
    "Receipt": ("source_system_id", "receipt_id"),
    "ReceiptItem": ("source_system_id", "receipt_id", "line_id"),
}


def canonicalize(
    rows: dict[str, tuple[dict[str, object], ...]], *, batch_id: UUID, observed_at: datetime
) -> dict[str, tuple[dict[str, object], ...]]:
    output: dict[str, tuple[dict[str, object], ...]] = {}
    for entity, source_rows in rows.items():
        mapped: list[dict[str, object]] = []
        for source in source_rows:
            row = dict(source)
            if row.get("source_namespace", NAMESPACE) != NAMESPACE:
                raise DataPipelineFailure("RETAIL_REPORT_NAMESPACE_MISMATCH")
            row["source_system_id"] = NAMESPACE
            for key, value in tuple(row.items()):
                if key.endswith("_id") and value is not None:
                    row[key] = str(value)
                if isinstance(value, datetime):
                    if value.tzinfo is None:
                        raise DataPipelineFailure("RETAIL_REPORT_NAIVE_TIMESTAMP")
                    row[key] = value.astimezone(UTC)
            if entity in {"Customer", "Product", "Store"}:
                natural = entity.lower() + "_id"
                row[entity.lower() + "_version_id"] = str(
                    uuid5(batch_id, entity + ":" + str(row[natural]))
                )
                row["relationship_policy"] = RELATIONSHIP_POLICY
                if "valid_from" not in source:
                    row["valid_from"] = observed_at
                    row["valid_to"] = None
                    row["validity_basis"] = "platform_observed"
                else:
                    row["validity_basis"] = "source_supplied_current_only"
            if entity == "ReceiptItem":
                row["line_id"] = row["receipt_item_id"]
            if entity == "Receipt":
                occurred = row["receipt_datetime"]
                if not isinstance(occurred, datetime):
                    raise DataPipelineFailure("RETAIL_REPORT_INVALID_DATE")
                row["receipt_date"] = occurred.date()
            mapped.append(row)
        output[entity] = tuple(mapped)
    for entity, key in KEYS.items():
        values = [tuple(row.get(k) for k in key) for row in output[entity]]
        if any(None in v for v in values) or len(set(values)) != len(values):
            raise DataPipelineFailure("RETAIL_REPORT_CANONICAL_KEY_INVALID")
    for child, field, parent, parent_field, nullable in (
        ("Receipt", "customer_id", "Customer", "customer_id", True),
        ("Receipt", "store_id", "Store", "store_id", False),
        ("Receipt", "receipt_date", "Calendar", "calendar_date", False),
        ("ReceiptItem", "receipt_id", "Receipt", "receipt_id", False),
        ("ReceiptItem", "product_id", "Product", "product_id", False),
    ):
        parent_keys = {(r["source_system_id"], r[parent_field]) for r in output[parent]}
        if any(
            (r["source_system_id"], r[field]) not in parent_keys
            and not (nullable and r[field] is None)
            for r in output[child]
        ):
            raise DataPipelineFailure("RETAIL_REPORT_CANONICAL_REFERENCE_INVALID")
    return output


def build_publication(
    *,
    semantic_dataset_id: UUID,
    workspace_id: UUID,
    batch_id: UUID,
    quality_report_id: UUID,
    artifact_ids: dict[str, UUID],
    artifact_hashes: dict[str, str],
    rows: dict[str, tuple[dict[str, object], ...]],
    accounting: dict[str, object],
    raw_artifacts: dict[str, str],
    quarantine_artifact: str,
) -> SemanticDatasetPublication:
    relationships: list[dict[str, object]] = []
    for parent, child, pk, fk, nullable in (
        ("Customer", "Receipt", "customer_id", "customer_id", True),
        ("Receipt", "ReceiptItem", "receipt_id", "receipt_id", False),
        ("Product", "ReceiptItem", "product_id", "product_id", False),
        ("Store", "Receipt", "store_id", "store_id", False),
        ("Calendar", "Receipt", "calendar_date", "receipt_date", False),
    ):
        relationships.append(
            {
                "parent": parent,
                "child": child,
                "cardinality": "one_to_many",
                "parent_key": ["source_system_id", pk],
                "child_key": ["source_system_id", fk],
                "nullable": nullable,
                "policy": RELATIONSHIP_POLICY,
            }
        )
    dates = [r["receipt_date"] for r in rows["Receipt"]]
    if not dates or any(not isinstance(d, date) for d in dates):
        raise DataPipelineFailure("RETAIL_REPORT_INVALID_DATE")
    receipt_dates = [d for d in dates if isinstance(d, date)]
    summary: dict[str, object] = {
        "profile": PROFILE,
        "mapping_version": PROFILE,
        "schema_version": PROFILE,
        "namespace": NAMESPACE,
        "relationship_policy": RELATIONSHIP_POLICY,
        "relationships": relationships,
        "quality_accounting": accounting,
        "dimension_history": "current_only",
        "event_time_classification": "unavailable",
        "raw_artifacts": raw_artifacts,
        "quarantine_artifact": quarantine_artifact,
        "artifact_hashes": artifact_hashes,
        "calendar": [
            {k: v.isoformat() if isinstance(v, (date, datetime)) else v for k, v in r.items()}
            for r in rows["Calendar"]
        ],
        "stores": [
            {k: v.isoformat() if isinstance(v, (date, datetime)) else v for k, v in r.items()}
            for r in rows["Store"]
        ],
        "receipt_date_min": min(receipt_dates).isoformat(),
        "receipt_date_max": max(receipt_dates).isoformat(),
        "currencies": sorted({str(r["currency"]).strip() for r in rows["Receipt"]}),
        "rows": {e: len(r) for e, r in rows.items()},
    }
    request_hash = hashlib.sha256(
        json.dumps(
            {
                "workspace": str(workspace_id),
                "batch": str(batch_id),
                "dataset": str(semantic_dataset_id),
                "quality": str(quality_report_id),
                "summary": summary,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
    return SemanticDatasetPublication(
        uuid5(semantic_dataset_id, request_hash),
        semantic_dataset_id,
        workspace_id,
        1,
        "published",
        quality_report_id,
        tuple(
            SemanticEntityBinding(
                e,
                artifact_ids[e],
                KEYS[e],
                {
                    "source_system_id": "source_namespace",
                    **(
                        {"receipt_item_id": "source_line_identifier", "line_id": "line_identifier"}
                        if e == "ReceiptItem"
                        else {}
                    ),
                },
            )
            for e in KEYS
        ),
        {
            "customer": "available",
            "receipts": "available",
            "basket": "degraded",
            "products": "degraded",
            "stores": "available",
            "calendar": "available",
            "product_receipt_revenue_slicing": "unavailable",
        },
        summary,
        request_hash,
    )
