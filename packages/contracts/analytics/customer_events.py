"""Published observed-customer event capability; no receipt-root schema widening."""

from dataclasses import dataclass
from typing import Literal, Protocol
from uuid import UUID
from pydantic import ConfigDict
from packages.contracts.semantic import Strict, Hash
from packages.contracts.semantic.filter_fields import Name
from packages.contracts.semantic.filter_events import FilterEventVersion, EventObservation
from packages.contracts.semantic.relationships import FilterRelationshipVersion
from packages.contracts.semantic.nullable_relationships import NullableFilterRelationshipVersion
from packages.contracts.analytics.columnar_filters import PublishedRetailFilter, FlatExpression
from packages.contracts.analytics.relational_filters import RelationshipInput
from packages.contracts.analytics.aggregate_filters import CountInput
from packages.contracts.analytics.sequence_filters import (
    SequenceInputGrant,
    EventInput,
    SequenceExpression,
    SequenceFilterRequest,
)
from packages.contracts.analytics.retail_filter import (
    CatalogField,
    FilterLabels,
    FilterPreviewResponse,
)
from packages.contracts.analytics.retail_aggregate import CatalogCount


class ObservedChildRootRestriction(Strict):
    policy: Literal["published_customers_with_authorized_observed_receipts/v1"] = (
        "published_customers_with_authorized_observed_receipts/v1"
    )
    version_id: UUID
    root_entity: Name
    relationship_id: Name
    relationship_version_id: UUID


@dataclass(frozen=True, slots=True)
class RootRestrictedSequenceGrant(SequenceInputGrant):
    root_restrictions: tuple[ObservedChildRootRestriction, ...] = ()


@dataclass(frozen=True, slots=True)
class PublishedCustomerEvents:
    entities: tuple[PublishedRetailFilter, ...]
    relationships: tuple[RelationshipInput, ...]
    counts: tuple[CountInput, ...]
    events: tuple[EventInput, ...]
    universe: ObservedChildRootRestriction


class CustomerEventsSemanticPort(Protocol):
    def customer_events_projection(
        self, *, workspace_id: UUID, dataset_version_id: UUID
    ) -> PublishedCustomerEvents: ...


class CustomerEventFilterInput(Strict):
    model_config = ConfigDict(extra="forbid", json_schema_mode_override="validation")
    schema_version: Literal["customer-event-filter/v1"] = "customer-event-filter/v1"
    root_scope_id: UUID
    registry_versions: dict[str, UUID]
    expression: SequenceExpression


class CustomerEventPreviewRequest(Strict):
    dataset_version_id: UUID
    filter: CustomerEventFilterInput


def customer_event_request(
    workspace: UUID, dataset: UUID, value: CustomerEventFilterInput
) -> SequenceFilterRequest:
    return SequenceFilterRequest(
        workspace_id=workspace,
        dataset_version_id=dataset,
        root_entity="Customer",
        root_scope_id=value.root_scope_id,
        registry_versions=value.registry_versions,
        expression=value.expression,
    )


class CustomerEventPreviewResponse(FilterPreviewResponse):
    schema_version: Literal["customer-event-preview/v1"] = "customer-event-preview/v1"
    limitation_codes: tuple[str, ...]
    universe: ObservedChildRootRestriction


class CatalogEvent(Strict):
    definition: FilterEventVersion
    observation: EventObservation
    complete: bool
    evidence_hash: Hash
    label: FilterLabels
    description: FilterLabels


class CustomerEventRelationship(Strict):
    relationship: NullableFilterRelationshipVersion | FilterRelationshipVersion
    label: FilterLabels
    complete: bool
    completeness_hash: Hash


class CustomerEventCatalog(Strict):
    schema_version: Literal["customer-event-catalog/v1"] = "customer-event-catalog/v1"
    dataset_version_id: UUID
    root_entity: Literal["Customer"] = "Customer"
    registry_versions: dict[str, UUID]
    fields: list[CatalogField]
    relationships: list[CustomerEventRelationship]
    events: tuple[CatalogEvent, ...]
    counts: tuple[CatalogCount, ...]
    mandatory_expressions: dict[str, FlatExpression]
    universe: ObservedChildRootRestriction
    resource_policy_version_id: UUID
    limitation_codes: tuple[str, ...]
