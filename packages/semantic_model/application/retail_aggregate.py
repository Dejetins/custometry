"""Count definitions over genuinely published observed retail items; never certified history."""

from datetime import UTC, date, datetime, time, timedelta
from typing import Any
from uuid import UUID, uuid5
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.aggregate_filters import CountInput
from packages.contracts.analytics.retail_aggregate import PublishedRetailAggregates
from packages.contracts.semantic.filter_aggregates import (
    AggregateFieldRef,
    AggregateObservation,
    FilterCountVersion,
)
from packages.semantic_model.application.retail_relational import (
    retail_relational_projection,
    digest,
)


def retail_aggregate_projection(
    dataset: UUID, source: dict[str, Any], published_at: datetime
) -> PublishedRetailAggregates:
    relations = retail_relational_projection(dataset, source)
    if published_at.tzinfo is None:
        raise AnalyticsFailure("FILTER_AGGREGATE_PUBLICATION_TIME")
    cutoff = published_at.astimezone(UTC)
    try:
        first = date.fromisoformat(source["summary"]["receipt_date_min"])
        last = date.fromisoformat(source["summary"]["receipt_date_max"])
        if first > last or last > cutoff.date():
            raise ValueError("Invalid observed dates")
        start = datetime.combine(first, time(), UTC)
        # Date windows include only closed UTC days. The current observed day is
        # not a future date and must not disable earlier supported windows.
        end = min(
            datetime.combine(last + timedelta(days=1), time(), UTC),
            datetime.combine(cutoff.date(), time(), UTC),
        )
        if start == end:
            return PublishedRetailAggregates(relations, ())
        observation = AggregateObservation(
            starts_at=start, ends_at=end, observation_as_of=cutoff, knowledge_as_of=cutoff
        )
    except (ValueError, TypeError, KeyError, OverflowError):
        raise AnalyticsFailure("FILTER_AGGREGATE_OBSERVATION_UNAVAILABLE") from None
    fields = {f.field_id: f for e in relations.entities for f in e.registry.fields}

    def ref(name: str):
        field = fields[name]
        return AggregateFieldRef(field_id=name, version_id=field.version_id)

    relationship = relations.relationships[0].relationship
    counts: list[CountInput] = []
    for kind, grain, unit in (
        ("count", "line_id", "ReceiptItem.rows"),
        ("count_distinct", "product_id", "ReceiptItem.products"),
    ):
        count_id = f"retail.observed.{kind}.{grain}"
        meaning = dict(
            count_id=count_id,
            relationship_version_id=relationship.version_id,
            child_entity="ReceiptItem",
            kind=kind,
            grain_fields=[ref(f"ReceiptItem.{grain}").model_dump(mode="json")],
            unit=unit,
            null_policy="unknown",
            time_entity="parent",
            time_field=ref("Receipt.receipt_date").model_dump(mode="json"),
            empty_policy="zero_if_complete",
            returns_policy="all_observed_rows/v1",
            time_basis="utc_date/v1",
        )
        definition = FilterCountVersion.model_validate(
            {
                **meaning,
                "version_id": uuid5(
                    dataset,
                    digest({**meaning, "relationship_version_id": str(relationship.version_id)}),
                ),
            }
        )
        evidence = digest(
            dict(
                contract="retail-observed-aggregate/v1",
                publication=source["publication_hash"],
                observation=observation.model_dump(mode="json"),
                relationship_completeness=relations.relationships[0].completeness_hash,
                definition=definition.model_dump(mode="json"),
            )
        )
        counts.append(CountInput(definition, observation, evidence))
    return PublishedRetailAggregates(relations, tuple(counts))
