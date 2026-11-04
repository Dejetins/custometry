"""Explicit current published Receipt→ReceiptItem semantics; no history inference."""

from __future__ import annotations

import hashlib
import json
from typing import Any
from uuid import UUID, uuid5
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.columnar_filters import PublishedRetailFilter
from packages.contracts.analytics.relational_filters import RelationshipInput
from packages.contracts.analytics.retail_relational import PublishedRetailRelations
from packages.contracts.semantic.filter_fields import FilterFieldVersion, FlatFilterRegistry
from packages.contracts.semantic.relationships import FilterRelationshipVersion
from packages.semantic_model.application.retail_filters import retail_filter_projection


def digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def retail_relational_projection(dataset: UUID, source: dict[str, Any]) -> PublishedRetailRelations:
    receipt = retail_filter_projection(dataset, source)
    summary = source["summary"]
    expected = dict(
        parent="Receipt",
        child="ReceiptItem",
        cardinality="one_to_many",
        parent_key=["source_system_id", "receipt_id"],
        child_key=["source_system_id", "receipt_id"],
        nullable=False,
        policy="retail-report-current-only/v1",
    )
    relations = [
        r
        for r in summary.get("relationships", [])
        if r.get("parent") == "Receipt" and r.get("child") == "ReceiptItem"
    ]
    bindings = [b for b in source["bindings"] if b["entity"] == "ReceiptItem"]
    if (
        relations != [expected]
        or summary.get("relationship_policy") != expected["policy"]
        or len(bindings) != 1
        or bindings[0]["primary_key"] != ["source_system_id", "receipt_id", "line_id"]
    ):
        raise AnalyticsFailure("FILTER_RELATIONSHIP_BINDING")
    publication = source["publication_hash"]

    def field(entity: str, name: str, dtype: str = "string", scale: int = 2):
        return FilterFieldVersion.model_validate(
            dict(
                field_id=f"{entity}.{name}",
                version_id=uuid5(dataset, f"retail-correlated/v2:{entity}.{name}"),
                entity=entity,
                column=name,
                data_type=dtype,
                decimal_precision=18,
                decimal_scale=scale,
                operators=("eq", "ne", "lt", "le", "gt", "ge", "in", "is_null", "is_not_null")
                if dtype == "decimal"
                else ("eq", "ne", "in", "is_null", "is_not_null"),
                null_policy="unknown",
            )
        )

    root_fields = (*receipt.registry.fields, field("Receipt", "receipt_id"))
    item_fields = tuple(
        field("ReceiptItem", name)
        for name in ("source_system_id", "receipt_id", "line_id", "product_id")
    ) + tuple(
        field("ReceiptItem", name, "decimal", 3 if name == "quantity" else 2)
        for name in ("quantity", "unit_price", "discount_amount", "net_amount")
    )

    def registry(entity: str, fields: tuple[FilterFieldVersion, ...]) -> FlatFilterRegistry:
        return FlatFilterRegistry(
            version_id=uuid5(
                dataset,
                digest(
                    dict(
                        publication=publication, fields=[f.model_dump(mode="json") for f in fields]
                    )
                ),
            ),
            dataset_version_id=dataset,
            entity=entity,
            fields=fields,
        )

    relationship = FilterRelationshipVersion(
        relationship_id="receipt.items",
        version_id=uuid5(dataset, digest(dict(publication=publication, relationship=expected))),
        parent_entity="Receipt",
        child_entity="ReceiptItem",
        parent_fields=("Receipt.source_system_id", "Receipt.receipt_id"),
        child_fields=("ReceiptItem.source_system_id", "ReceiptItem.receipt_id"),
        policy_version_id=uuid5(dataset, str(expected["policy"])),
    )
    # This publication has no certified business-history completeness. Even a future
    # transport or accounting flag cannot silently upgrade this provider contract.
    completeness = digest(
        dict(
            contract="retail-observed-only/v2",
            publication=publication,
            accounting=summary.get("quality_accounting"),
            relationship=relationship.model_dump(mode="json"),
        )
    )
    return PublishedRetailRelations(
        legacy_registry_version_id=receipt.registry.version_id,
        entities=(
            PublishedRetailFilter(
                registry=registry("Receipt", root_fields),
                artifact_id=receipt.artifact_id,
                content_hash=receipt.content_hash,
                source_namespace=receipt.source_namespace,
                row_id_column="receipt_id",
            ),
            PublishedRetailFilter(
                registry=registry("ReceiptItem", item_fields),
                artifact_id=UUID(bindings[0]["artifact_id"]),
                content_hash=bindings[0]["content_hash"],
                source_namespace=receipt.source_namespace,
                row_id_column="line_id",
            ),
        ),
        relationships=(RelationshipInput(relationship, False, completeness),),
    )
