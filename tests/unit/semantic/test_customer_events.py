"""Published event meaning, nullable customer mapping and exact snapshot cutoffs."""

from datetime import datetime, UTC
from uuid import uuid4
import pytest
from packages.contracts.analytics import AnalyticsFailure
from packages.semantic_model.application.customer_events import customer_events_projection
from tests.unit.semantic.test_retail_aggregate import published


def source():
    value = published()
    value["summary"]["dimension_history"] = "current_only"
    value["summary"]["event_time_classification"] = "unavailable"
    value["summary"]["relationships"].append(
        dict(
            parent="Customer",
            child="Receipt",
            cardinality="one_to_many",
            parent_key=["source_system_id", "customer_id"],
            child_key=["source_system_id", "customer_id"],
            nullable=True,
            policy="retail-report-current-only/v1",
        )
    )
    value["bindings"].append(
        dict(
            entity="Customer",
            primary_key=["customer_version_id"],
            artifact_id=str(uuid4()),
            content_hash="d" * 64,
        )
    )
    return value


def test_native_event_versions_meaning_and_no_invented_history():
    value = source()
    dataset = uuid4()
    cutoff = datetime(2026, 10, 7, 12, 34, 56, 123456, tzinfo=UTC)
    result = customer_events_projection(dataset, value, cutoff)
    assert result == customer_events_projection(dataset, value, cutoff)
    assert tuple(e.registry.entity for e in result.entities) == (
        "Customer",
        "Receipt",
        "ReceiptItem",
    )
    assert result.events[0].observation.observation_as_of == cutoff
    assert result.events[0].definition.time_field.storage_type == "timestamp_us_utc/v1"
    assert result.relationships[0].relationship.nullable_child_fields == ("Receipt.customer_id",)
    assert all(not r.complete for r in result.relationships) and not result.events[0].complete
    assert {f.column for f in result.entities[0].registry.fields} == {
        "source_system_id",
        "customer_id",
        "customer_version_id",
    }
    value["summary"]["quality_accounting"]["business_history_completeness"] = "complete"
    changed = customer_events_projection(dataset, value, cutoff)
    assert (
        not changed.events[0].complete
        and changed.events[0].evidence_hash != result.events[0].evidence_hash
    )


def test_current_publication_day_has_native_event_window():
    value = source()
    value["summary"].update(receipt_date_min="2026-10-07", receipt_date_max="2026-10-07")
    cutoff = datetime(2026, 10, 7, 12, 34, 56, 123456, tzinfo=UTC)
    result = customer_events_projection(uuid4(), value, cutoff)
    assert result.counts == ()
    assert result.events[0].observation.ends_at == cutoff
    assert result.events[0].observation.starts_at == datetime(2026, 10, 7, tzinfo=UTC)


@pytest.mark.parametrize("mutation", ["nullable", "missing", "history", "key", "duplicate"])
def test_invalid_current_customer_mapping_is_blocked(mutation):
    value = source()
    if mutation == "nullable":
        value["summary"]["relationships"][-1]["nullable"] = False
    elif mutation == "missing":
        value["summary"]["relationships"].pop()
    elif mutation == "history":
        value["summary"]["dimension_history"] = "inferred"
    elif mutation == "key":
        value["bindings"][-1]["primary_key"] = ["customer_id"]
    else:
        value["bindings"].append(value["bindings"][-1])
    with pytest.raises(AnalyticsFailure, match="FILTER_CUSTOMER_EVENT_BINDING"):
        customer_events_projection(uuid4(), value, datetime(2026, 10, 7, tzinfo=UTC))
