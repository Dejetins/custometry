from datetime import UTC, datetime, timedelta
from uuid import uuid4

from packages.data_quality import QualityWaiver, default_retail_rules, evaluate_quality


NOW = datetime(2026, 8, 27, tzinfo=UTC)


def rows() -> dict[str, tuple[dict[str, object], ...]]:
    return {
        "customers": ({"customer_id": 1},),
        "products": ({"product_id": 10},),
        "receipts": ({"receipt_id": 100, "customer_id": 1, "receipt_datetime": NOW},),
        "receipt_items": ({"receipt_item_id": 1001, "receipt_id": 100, "product_id": 10},),
    }


def waiver(*, rule_id: str, status: str = "active", expired: bool = False) -> QualityWaiver:
    return QualityWaiver(
        waiver_id=uuid4(),
        workspace_id=uuid4(),
        rule_id=rule_id,
        status=status,  # type: ignore[arg-type]
        expires_at=NOW + (-timedelta(seconds=1) if expired else timedelta(days=1)),
        approved_by=uuid4(),
        reason_code="KNOWN_SOURCE_EXCEPTION",
    )


def evaluate(
    source_rows: dict[str, tuple[dict[str, object], ...]], waivers: tuple[QualityWaiver, ...] = ()
):
    return evaluate_quality(
        workspace_id=uuid4(),
        batch_id=uuid4(),
        rows_by_entity=source_rows,
        rules=default_retail_rules(),
        waivers=waivers,
        now=NOW,
    )


def test_required_rules_pass_clean_retail_rows() -> None:
    report = evaluate(rows())
    assert report.decision == "passed"
    assert report.allows_publication is True
    assert report.violations == ()


def test_required_rule_failure_blocks_publication() -> None:
    broken = rows()
    broken["receipt_items"] = ({"receipt_item_id": 1001, "receipt_id": 100, "product_id": 999},)
    report = evaluate(broken)
    assert report.decision == "failed"
    assert report.allows_publication is False
    assert report.violations[0].rule_id == "receipt_item.product.reference"
    assert report.violations[0].sample_keys == ("receipt_item_id:1001",)


def test_active_waiver_allows_only_waivable_rule() -> None:
    broken = rows()
    broken["receipt_items"] = ({"receipt_item_id": 1001, "receipt_id": 100, "product_id": 999},)
    active = waiver(rule_id="receipt_item.product.reference")
    report = evaluate(broken, (active,))
    assert report.decision == "passed_with_waivers"
    assert report.applied_waiver_ids == (active.waiver_id,)


def test_expired_revoked_and_non_waivable_rules_remain_blocked() -> None:
    product_broken = rows()
    product_broken["receipt_items"] = (
        {"receipt_item_id": 1001, "receipt_id": 100, "product_id": 999},
    )
    assert (
        evaluate(
            product_broken, (waiver(rule_id="receipt_item.product.reference", expired=True),)
        ).decision
        == "failed"
    )
    assert (
        evaluate(
            product_broken,
            (waiver(rule_id="receipt_item.product.reference", status="revoked"),),
        ).decision
        == "failed"
    )

    receipt_broken = rows()
    receipt_broken["receipt_items"] = (
        {"receipt_item_id": 1001, "receipt_id": 999, "product_id": 10},
    )
    assert (
        evaluate(receipt_broken, (waiver(rule_id="receipt_item.receipt.reference"),)).decision
        == "failed"
    )
