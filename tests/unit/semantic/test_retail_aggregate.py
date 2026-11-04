"""Published count policy binds real observed metadata without inventing completeness."""

from datetime import UTC, datetime
from uuid import uuid4
import pytest
from packages.contracts.analytics import AnalyticsFailure
from packages.semantic_model.application.retail_aggregate import retail_aggregate_projection
from tests.unit.semantic.test_retail_relational import source


def published():
    value = source()
    value["summary"].update(receipt_date_min="2025-01-01", receipt_date_max="2025-01-03")
    return value


def test_exact_count_definitions_and_observation_cutoffs():
    value, dataset = published(), uuid4()
    cutoff = datetime(2026, 10, 7, 15, 24, 39, 123456, tzinfo=UTC)
    first = retail_aggregate_projection(dataset, value, cutoff)
    assert first == retail_aggregate_projection(dataset, value, cutoff)
    assert first.relations.relationships[0].complete is False
    assert [c.definition.kind for c in first.counts] == ["count", "count_distinct"]
    assert [c.definition.grain_fields[0].field_id for c in first.counts] == [
        "ReceiptItem.line_id",
        "ReceiptItem.product_id",
    ]
    assert all(c.definition.time_field.field_id == "Receipt.receipt_date" for c in first.counts)
    assert first.counts[0].observation.knowledge_as_of == cutoff
    changed = retail_aggregate_projection(dataset, value, cutoff.replace(microsecond=123457))
    assert changed.counts[0].definition == first.counts[0].definition
    assert changed.counts[0].evidence_hash != first.counts[0].evidence_hash
    value["summary"]["quality_accounting"]["business_history_completeness"] = "complete"
    assert (
        retail_aggregate_projection(dataset, value, cutoff).relations.relationships[0].complete
        is False
    )


@pytest.mark.parametrize("mutation", ["missing", "invalid", "reversed", "future", "naive"])
def test_missing_or_impossible_snapshot_metadata_is_blocked(mutation):
    value = published()
    cutoff = datetime(2026, 10, 7, tzinfo=UTC)
    if mutation == "missing":
        value["summary"].pop("receipt_date_min")
    elif mutation == "invalid":
        value["summary"]["receipt_date_min"] = "not-a-date"
    elif mutation == "reversed":
        value["summary"]["receipt_date_min"] = "2025-02-01"
    elif mutation == "future":
        value["summary"]["receipt_date_max"] = "2027-01-01"
    else:
        cutoff = cutoff.replace(tzinfo=None)
    with pytest.raises(AnalyticsFailure, match="FILTER_AGGREGATE_"):
        retail_aggregate_projection(uuid4(), value, cutoff)


def test_publication_day_keeps_earlier_closed_days_and_exact_cutoff():
    value = published()
    value["summary"].update(receipt_date_min="2026-10-01", receipt_date_max="2026-10-07")
    cutoff = datetime(2026, 10, 7, 15, 24, 39, 123456, tzinfo=UTC)
    result = retail_aggregate_projection(uuid4(), value, cutoff)
    assert len(result.counts) == 2
    for count in result.counts:
        assert count.observation.ends_at == datetime(2026, 10, 7, tzinfo=UTC)
        assert count.observation.starts_at == datetime(2026, 10, 1, tzinfo=UTC)
        assert count.observation.observation_as_of == count.observation.knowledge_as_of == cutoff
    assert result.relations.relationships[0].complete is False


def test_only_publication_day_has_no_closed_window_without_fake_coverage():
    value = published()
    value["summary"].update(receipt_date_min="2026-10-07", receipt_date_max="2026-10-07")
    result = retail_aggregate_projection(uuid4(), value, datetime(2026, 10, 7, 15, tzinfo=UTC))
    assert result.counts == ()
    assert result.relations.relationships[0].complete is False
