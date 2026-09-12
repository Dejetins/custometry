"""Bounded retail-report/v1 admission: keys and references never use waivers."""

from dataclasses import dataclass
from datetime import UTC, date, datetime
from decimal import Decimal
from uuid import UUID, uuid5

from packages.contracts.data_pipeline import DataPipelineFailure
from packages.data_quality.domain.model import QualityReport, QualityViolation

POLICY = "retail-report-orphan-product/v1"
KEYS = {
    "Customer": "customer_id",
    "Product": "product_id",
    "Receipt": "receipt_id",
    "ReceiptItem": "receipt_item_id",
    "Store": "store_id",
    "Calendar": "calendar_date",
}


@dataclass(frozen=True)
class RetailReportAdmission:
    rows: dict[str, tuple[dict[str, object], ...]]
    quarantine: tuple[dict[str, object], ...]
    report: QualityReport
    accounting: dict[str, object]


def admit(
    *,
    rows: dict[str, tuple[dict[str, object], ...]],
    workspace_id: UUID,
    batch_id: UUID,
    observed_at: datetime,
) -> RetailReportAdmission:
    violations: list[QualityViolation] = []
    keys: dict[str, set[object]] = {}
    for entity, key in KEYS.items():
        values = [r.get(key) for r in rows[entity]]
        keys[entity] = set(values)
        count = sum(v is None for v in values) + len(values) - len(set(values))
        if count:
            violations.append(QualityViolation(entity + ".key.invalid", count, (), False))
    for entity, field, parent, nullable in (
        ("Receipt", "customer_id", "Customer", True),
        ("Receipt", "store_id", "Store", False),
        ("ReceiptItem", "receipt_id", "Receipt", False),
    ):
        count = sum(
            r.get(field) not in keys[parent] and not (nullable and r.get(field) is None)
            for r in rows[entity]
        )
        if count:
            violations.append(
                QualityViolation(entity + "." + field + ".reference", count, (), False)
            )
    receipts = {r["receipt_id"]: r for r in rows["Receipt"]}
    invalid_dates = 0
    for receipt in rows["Receipt"]:
        occurred = receipt.get("receipt_datetime")
        if (
            not isinstance(occurred, datetime)
            or occurred.tzinfo is None
            or occurred.astimezone(UTC).date() not in keys["Calendar"]
        ):
            invalid_dates += 1
    invalid_dates += sum(
        not isinstance(r.get("calendar_date"), date)
        or not isinstance(r.get("is_period_complete"), bool)
        for r in rows["Calendar"]
    )
    if invalid_dates:
        violations.append(QualityViolation("receipt.calendar.reference", invalid_dates, (), False))
    # The selected policy covers only the known sentinel, not arbitrary new or null orphans.
    quarantine = tuple(
        r
        for r in rows["ReceiptItem"]
        if r.get("product_id") == 999999 and 999999 not in keys["Product"]
    )
    unexpected = sum(
        r.get("product_id") not in keys["Product"] and r not in quarantine
        for r in rows["ReceiptItem"]
    )
    if unexpected or len(quarantine) != 5:
        violations.append(
            QualityViolation(
                "receipt_item.product.unexpected", unexpected or abs(len(quarantine) - 5), (), False
            )
        )
    eligible = dict(rows)
    eligible["ReceiptItem"] = tuple(r for r in rows["ReceiptItem"] if r not in quarantine)
    impact: dict[str, Decimal] = {}
    for row in quarantine:
        receipt = receipts.get(row["receipt_id"])
        occurred = receipt.get("receipt_datetime") if receipt else None
        if receipt is not None and isinstance(occurred, datetime) and occurred.tzinfo is not None:
            key = (
                str(receipt["currency"]).strip() + ":" + occurred.astimezone(UTC).date().isoformat()
            )
            amount = row.get("net_amount")
            if not isinstance(amount, Decimal):
                raise DataPipelineFailure("RETAIL_REPORT_INVALID_AMOUNT")
            impact[key] = impact.get(key, Decimal(0)) + amount
    denominator = len(rows["ReceiptItem"])
    accounting: dict[str, object] = {
        "policy": POLICY,
        "gate": "block" if violations else "allow_degraded",
        "raw_counts": {e: len(r) for e, r in rows.items()},
        "eligible_counts": {e: len(r) for e, r in eligible.items()},
        "quarantined_count": len(quarantine),
        "denominator": denominator,
        "product_relationship_eligible_count": len(eligible["ReceiptItem"]),
        "quarantined_item_net_by_currency_date": {k: str(v) for k, v in sorted(impact.items())},
        "business_impact": "unknown",
        "business_history_completeness": "unknown",
        "transport_completeness": "complete",
        "classification_coverage": "degraded",
        "collapsed_duplicates": 0,
        "policy_excluded": 0,
        "expanded_rows": 0,
        "receipt_headers_retained": len(rows["Receipt"]),
        "anonymous_receipts": sum(r.get("customer_id") is None for r in rows["Receipt"]),
    }
    violations.append(
        QualityViolation("receipt_item.product.reference", len(quarantine), (), False, accounting)
    )
    report = QualityReport(
        uuid5(batch_id, POLICY),
        workspace_id,
        batch_id,
        "failed" if accounting["gate"] == "block" else "passed",
        tuple(violations),
        (),
        observed_at,
    )
    return RetailReportAdmission(eligible, quarantine, report, accounting)
