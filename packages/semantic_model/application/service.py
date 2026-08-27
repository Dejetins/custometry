from __future__ import annotations

import hashlib
import json
from uuid import UUID, uuid5

from packages.contracts.data_pipeline import DataPipelineFailure
from packages.semantic_model.domain.model import SemanticDatasetPublication, SemanticEntityBinding


ENTITY_KEYS: dict[str, tuple[str, ...]] = {
    "Customer": ("customer_id",),
    "Product": ("product_id",),
    "Receipt": ("receipt_id",),
    "ReceiptItem": ("receipt_item_id",),
}

FIELD_ROLES: dict[str, dict[str, str]] = {
    "Customer": {"customer_id": "customer_identifier", "created_at": "customer_created_at"},
    "Product": {"product_id": "product_identifier", "category": "product_category"},
    "Receipt": {
        "receipt_id": "receipt_identifier",
        "customer_id": "customer_reference",
        "receipt_datetime": "receipt_occurred_at",
        "net_amount": "receipt_net_amount",
        "updated_at": "source_updated_at",
    },
    "ReceiptItem": {
        "receipt_item_id": "receipt_item_identifier",
        "receipt_id": "receipt_reference",
        "product_id": "product_reference",
        "quantity": "quantity",
        "net_amount": "item_net_amount",
    },
}


def build_retail_publication(
    *,
    semantic_dataset_id: UUID,
    workspace_id: UUID,
    batch_id: UUID,
    quality_report_id: UUID,
    quality_decision: str,
    artifact_ids: dict[str, UUID],
    artifact_hashes: dict[str, str],
    row_counts: dict[str, int],
    violation_counts: dict[str, int],
) -> SemanticDatasetPublication:
    if quality_decision not in {"passed", "passed_with_waivers"}:
        raise DataPipelineFailure("SEMANTIC_PUBLICATION_DQ_BLOCKED")
    expected = set(ENTITY_KEYS)
    if set(artifact_ids) != expected or set(artifact_hashes) != expected:
        raise DataPipelineFailure("SEMANTIC_PUBLICATION_INPUT_INCOMPLETE")
    normalized = {
        "semantic_dataset_id": str(semantic_dataset_id),
        "workspace_id": str(workspace_id),
        "batch_id": str(batch_id),
        "quality_report_id": str(quality_report_id),
        "quality_decision": quality_decision,
        "artifact_hashes": {key: artifact_hashes[key] for key in sorted(artifact_hashes)},
        "schema_version": 1,
    }
    request_hash = hashlib.sha256(
        json.dumps(normalized, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    version_id = uuid5(semantic_dataset_id, request_hash)
    bindings = tuple(
        SemanticEntityBinding(
            entity=entity,
            artifact_id=artifact_ids[entity],
            primary_key=ENTITY_KEYS[entity],
            field_roles=FIELD_ROLES[entity],
        )
        for entity in ("Customer", "Receipt", "ReceiptItem", "Product")
    )
    product_reference_misses = violation_counts.get("receipt_item.product.reference", 0)
    capability_matrix = {
        "customer": "available",
        "receipts": "available",
        "basket": "degraded" if product_reference_misses else "available",
        "products": "degraded" if product_reference_misses else "available",
    }
    return SemanticDatasetPublication(
        semantic_dataset_version_id=version_id,
        semantic_dataset_id=semantic_dataset_id,
        workspace_id=workspace_id,
        version=1,
        status="published",
        quality_report_id=quality_report_id,
        bindings=bindings,
        capability_matrix=capability_matrix,
        impact_summary={
            "entities": [item.entity for item in bindings],
            "rows": {key: row_counts[key] for key in sorted(row_counts)},
            "quality_decision": quality_decision,
            "product_reference_misses": product_reference_misses,
        },
        request_hash=request_hash,
    )
