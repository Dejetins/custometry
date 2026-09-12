from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class RetailObjectSpec:
    semantic_entity: str
    source_object: str
    columns: tuple[str, ...]
    primary_key: str
    pii_class: str


@dataclass(frozen=True, slots=True)
class ExtractionBatchRequest:
    batch_id: UUID
    workspace_id: UUID
    connection_id: UUID
    source_system_id: UUID
    semantic_dataset_id: UUID
    idempotency_key: str
    profile: str = "retail/v1"
    source_fingerprint: str | None = None


@dataclass(frozen=True, slots=True)
class ExtractionBatchState:
    batch_id: UUID
    state: str
    lower_watermark: datetime | None
    candidate_upper_watermark: datetime | None
    consistency_mode: str


RETAIL_OBJECTS: tuple[RetailObjectSpec, ...] = (
    RetailObjectSpec(
        "Customer",
        "customers",
        (
            "customer_id",
            "source_namespace",
            "first_name",
            "last_name",
            "email",
            "loyalty_card",
            "city",
            "created_at",
            "valid_from",
            "valid_to",
        ),
        "customer_id",
        "sensitive",
    ),
    RetailObjectSpec(
        "Receipt",
        "receipts",
        (
            "receipt_id",
            "receipt_number",
            "receipt_datetime",
            "customer_id",
            "store_id",
            "channel_id",
            "currency",
            "gross_amount",
            "discount_amount",
            "net_amount",
            "status",
            "updated_at",
        ),
        "receipt_id",
        "personal",
    ),
    RetailObjectSpec(
        "ReceiptItem",
        "receipt_items",
        (
            "receipt_item_id",
            "receipt_id",
            "product_id",
            "quantity",
            "unit_price",
            "discount_amount",
            "net_amount",
        ),
        "receipt_item_id",
        "internal",
    ),
    RetailObjectSpec(
        "Product",
        "products",
        (
            "product_id",
            "sku",
            "product_name",
            "brand",
            "category",
            "subcategory",
            "currency",
            "list_price",
            "valid_from",
            "valid_to",
        ),
        "product_id",
        "internal",
    ),
)


RETAIL_REPORT_OBJECTS = RETAIL_OBJECTS + (
    RetailObjectSpec(
        "Store",
        "stores",
        ("store_id", "store_code", "store_name", "region", "opened_on"),
        "store_id",
        "internal",
    ),
    RetailObjectSpec(
        "Calendar",
        "calendar",
        ("calendar_date", "iso_year", "iso_week", "month_start", "is_period_complete"),
        "calendar_date",
        "internal",
    ),
)
