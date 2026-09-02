from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from packages.data_quality.domain.model import (
    QualityReport,
    QualityRuleVersion,
    QualityViolation,
    QualityWaiver,
)


def default_retail_rules() -> tuple[QualityRuleVersion, ...]:
    return (
        QualityRuleVersion("customer.key.not_null", 1, "customers", "not_null", ("customer_id",)),
        QualityRuleVersion("customer.key.unique", 1, "customers", "unique", ("customer_id",)),
        QualityRuleVersion("product.key.not_null", 1, "products", "not_null", ("product_id",)),
        QualityRuleVersion("product.key.unique", 1, "products", "unique", ("product_id",)),
        QualityRuleVersion("receipt.key.not_null", 1, "receipts", "not_null", ("receipt_id",)),
        QualityRuleVersion("receipt.key.unique", 1, "receipts", "unique", ("receipt_id",)),
        QualityRuleVersion(
            "receipt.datetime.valid", 1, "receipts", "valid_datetime", ("receipt_datetime",)
        ),
        QualityRuleVersion(
            "receipt.customer.reference",
            1,
            "receipts",
            "reference",
            ("customer_id",),
            reference_entity="customers",
            reference_field="customer_id",
            ignore_null=True,
        ),
        QualityRuleVersion(
            "receipt_item.receipt.reference",
            1,
            "receipt_items",
            "reference",
            ("receipt_id",),
            reference_entity="receipts",
            reference_field="receipt_id",
        ),
        QualityRuleVersion(
            "receipt_item.product.reference",
            1,
            "receipt_items",
            "reference",
            ("product_id",),
            reference_entity="products",
            reference_field="product_id",
            waivable=True,
            ignore_null=True,
        ),
    )


def _row_key(row: dict[str, object]) -> str:
    for field in ("receipt_item_id", "receipt_id", "customer_id", "product_id"):
        if row.get(field) is not None:
            return f"{field}:{row[field]}"
    return "row:redacted"


def _invalid_rows(
    rule: QualityRuleVersion, rows_by_entity: dict[str, tuple[dict[str, object], ...]]
) -> tuple[dict[str, object], ...]:
    rows = rows_by_entity.get(rule.entity, ())
    field = rule.fields[0]
    if rule.kind == "not_null":
        return tuple(row for row in rows if row.get(field) is None)
    if rule.kind == "unique":
        seen: set[tuple[object, ...]] = set()
        invalid: list[dict[str, object]] = []
        for row in rows:
            key = tuple(row.get(item) for item in rule.fields)
            if key in seen:
                invalid.append(row)
            else:
                seen.add(key)
        return tuple(invalid)
    if rule.kind == "valid_datetime":
        return tuple(row for row in rows if not isinstance(row.get(field), datetime))
    if rule.kind == "reference":
        assert rule.reference_entity is not None and rule.reference_field is not None
        reference_values = {
            row.get(rule.reference_field) for row in rows_by_entity.get(rule.reference_entity, ())
        }
        return tuple(
            row
            for row in rows
            if not (rule.ignore_null and row.get(field) is None)
            and row.get(field) not in reference_values
        )
    raise AssertionError(rule.kind)


def evaluate_quality(
    *,
    workspace_id: UUID,
    batch_id: UUID,
    rows_by_entity: dict[str, tuple[dict[str, object], ...]],
    rules: tuple[QualityRuleVersion, ...],
    waivers: tuple[QualityWaiver, ...],
    now: datetime,
) -> QualityReport:
    violations: list[QualityViolation] = []
    applied: list[UUID] = []
    blocking = False
    for rule in rules:
        invalid = _invalid_rows(rule, rows_by_entity)
        if not invalid:
            continue
        waiver = next((item for item in waivers if item.applies(rule, now=now)), None)
        waived = waiver is not None
        if waiver is not None:
            applied.append(waiver.waiver_id)
        elif rule.required:
            blocking = True
        violations.append(
            QualityViolation(
                rule_id=rule.rule_id,
                count=len(invalid),
                sample_keys=tuple(_row_key(row) for row in invalid[:5]),
                waived=waived,
            )
        )
    decision = "failed" if blocking else ("passed_with_waivers" if applied else "passed")
    return QualityReport(
        report_id=uuid4(),
        workspace_id=workspace_id,
        batch_id=batch_id,
        decision=decision,
        violations=tuple(violations),
        applied_waiver_ids=tuple(applied),
        evaluated_at=now,
    )
