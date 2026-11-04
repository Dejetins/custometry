"""Observed published customer/receipt events, with explicit current-only meaning."""

from datetime import UTC, date, datetime, time, timedelta
from typing import Any
from uuid import UUID, uuid5
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.columnar_filters import PublishedRetailFilter
from packages.contracts.analytics.relational_filters import RelationshipInput
from packages.contracts.analytics.sequence_filters import EventInput
from packages.contracts.analytics.customer_events import (
    PublishedCustomerEvents,
    ObservedChildRootRestriction,
)
from packages.contracts.semantic.filter_events import (
    EventTimeFieldVersion,
    FilterEventVersion,
    EventObservation,
)
from packages.contracts.semantic.filter_fields import FilterFieldVersion, FlatFilterRegistry
from packages.contracts.semantic.nullable_relationships import NullableFilterRelationshipVersion
from packages.semantic_model.application.retail_aggregate import retail_aggregate_projection
from packages.semantic_model.application.retail_relational import digest


def customer_events_projection(
    dataset: UUID, source: dict[str, Any], published_at: datetime
) -> PublishedCustomerEvents:
    aggregates = retail_aggregate_projection(dataset, source, published_at)
    summary = source["summary"]
    publication = source["publication_hash"]
    expected = dict(
        parent="Customer",
        child="Receipt",
        cardinality="one_to_many",
        parent_key=["source_system_id", "customer_id"],
        child_key=["source_system_id", "customer_id"],
        nullable=True,
        policy="retail-report-current-only/v1",
    )
    mappings = [
        r
        for r in summary.get("relationships", [])
        if r.get("parent") == "Customer" and r.get("child") == "Receipt"
    ]
    customer = [b for b in source["bindings"] if b["entity"] == "Customer"]
    if (
        mappings != [expected]
        or len(customer) != 1
        or customer[0]["primary_key"] != ["customer_version_id"]
        or summary.get("dimension_history") != "current_only"
    ):
        raise AnalyticsFailure("FILTER_CUSTOMER_EVENT_BINDING")

    def field(entity: str, name: str):
        return FilterFieldVersion(
            field_id=f"{entity}.{name}",
            version_id=uuid5(dataset, f"customer-events/v1:{entity}.{name}"),
            entity=entity,
            column=name,
            data_type="string",
            operators=("eq", "ne", "in", "is_null", "is_not_null"),
            null_policy="unknown",
        )

    def registry(entity: str, fields: tuple[FilterFieldVersion, ...]):
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

    receipt, item = aggregates.relations.entities
    receipt = PublishedRetailFilter(
        registry=registry("Receipt", (*receipt.registry.fields, field("Receipt", "customer_id"))),
        artifact_id=receipt.artifact_id,
        content_hash=receipt.content_hash,
        source_namespace=receipt.source_namespace,
        row_id_column=receipt.row_id_column,
    )
    customer_projection = PublishedRetailFilter(
        registry=registry(
            "Customer",
            tuple(
                field("Customer", n)
                for n in ("source_system_id", "customer_id", "customer_version_id")
            ),
        ),
        artifact_id=UUID(customer[0]["artifact_id"]),
        content_hash=customer[0]["content_hash"],
        source_namespace=receipt.source_namespace,
        row_id_column="customer_version_id",
    )
    relation = NullableFilterRelationshipVersion(
        relationship_id="customer.receipts",
        version_id=uuid5(dataset, digest(dict(publication=publication, relationship=expected))),
        parent_entity="Customer",
        child_entity="Receipt",
        parent_fields=("Customer.source_system_id", "Customer.customer_id"),
        child_fields=("Receipt.source_system_id", "Receipt.customer_id"),
        nullable_child_fields=("Receipt.customer_id",),
        policy_version_id=uuid5(dataset, str(expected["policy"])),
    )
    evidence = digest(
        dict(
            contract="published-observed-customer-events/v1",
            publication=publication,
            relationship=relation.model_dump(mode="json"),
            dimension_history=summary["dimension_history"],
            event_time_classification=summary.get("event_time_classification"),
            accounting=summary.get("quality_accounting"),
        )
    )
    time_field = EventTimeFieldVersion(
        field_id="Receipt.receipt_datetime",
        version_id=uuid5(dataset, "retail-native-receipt-datetime-us-utc/v1"),
        entity="Receipt",
        column="receipt_datetime",
    )
    event = FilterEventVersion(
        event_id="retail.observed.receipt",
        version_id=uuid5(
            dataset,
            digest(
                dict(
                    publication=publication,
                    relationship=str(relation.version_id),
                    time_field=time_field.model_dump(mode="json"),
                    meaning="one_published_row_one_event/v1",
                )
            ),
        ),
        entity="Receipt",
        relationship_version_id=relation.version_id,
        time_field=time_field,
    )
    cutoff = published_at.astimezone(UTC)
    try:
        start = datetime.combine(date.fromisoformat(summary["receipt_date_min"]), time(), UTC)
        end = min(
            datetime.combine(
                date.fromisoformat(summary["receipt_date_max"]) + timedelta(days=1), time(), UTC
            ),
            cutoff,
        )
        observation = EventObservation(
            starts_at=start, ends_at=end, observation_as_of=cutoff, knowledge_as_of=cutoff
        )
    except (ValueError, KeyError, TypeError, OverflowError):
        raise AnalyticsFailure("FILTER_CUSTOMER_EVENT_OBSERVATION_UNAVAILABLE") from None
    universe = ObservedChildRootRestriction(
        version_id=uuid5(dataset, "published-customers-with-authorized-observed-receipts/v1"),
        root_entity="Customer",
        relationship_id=relation.relationship_id,
        relationship_version_id=relation.version_id,
    )
    return PublishedCustomerEvents(
        (customer_projection, receipt, item),
        (RelationshipInput(relation, False, evidence), *aggregates.relations.relationships),
        aggregates.counts,
        (
            EventInput(
                event,
                observation,
                False,
                digest(
                    dict(
                        evidence=evidence,
                        observation=observation.model_dump(mode="json"),
                        event=event.model_dump(mode="json"),
                    )
                ),
            ),
        ),
        universe,
    )
