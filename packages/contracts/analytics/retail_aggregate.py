"""Explicit published receipt aggregate capability and report input version."""

from dataclasses import dataclass
from typing import Literal, Protocol
from uuid import UUID
from pydantic import ConfigDict
from packages.contracts.semantic import Strict, Hash
from packages.contracts.analytics.aggregate_filters import (
    AggregateExpression,
    AggregateFilterRequest,
    CountInput,
)
from packages.contracts.semantic.filter_aggregates import FilterCountVersion, AggregateObservation
from packages.contracts.analytics.retail_relational import (
    PublishedRetailRelations,
    RelationalFacetQuery,
    CatalogRelationship,
)
from packages.contracts.analytics.retail_filter import (
    FilterLabels,
    FilterPreviewResponse,
    CatalogField,
)
from packages.contracts.analytics.columnar_filters import FlatExpression


@dataclass(frozen=True, slots=True)
class PublishedRetailAggregates:
    relations: PublishedRetailRelations
    counts: tuple[CountInput, ...]


class RetailAggregatesSemanticPort(Protocol):
    def retail_aggregate_projection(
        self, *, workspace_id: UUID, dataset_version_id: UUID
    ) -> PublishedRetailAggregates: ...


class AggregateReceiptFilterInput(Strict):
    model_config = ConfigDict(extra="forbid", json_schema_mode_override="validation")
    schema_version: Literal["receipt-filter/v3"] = "receipt-filter/v3"
    root_scope_id: UUID
    registry_versions: dict[str, UUID]
    expression: AggregateExpression
    legacy_registry_version_id: UUID | None = None


def receipt_aggregate_request(
    workspace: UUID, dataset: UUID, value: AggregateReceiptFilterInput
) -> AggregateFilterRequest:
    return AggregateFilterRequest(
        workspace_id=workspace,
        dataset_version_id=dataset,
        root_entity="Receipt",
        root_scope_id=value.root_scope_id,
        registry_versions=value.registry_versions,
        expression=value.expression,
        compatibility_registry_version_id=value.legacy_registry_version_id,
    )


class AggregatePreviewRequest(Strict):
    dataset_version_id: UUID
    filter: AggregateReceiptFilterInput


class AggregatePreviewResponse(FilterPreviewResponse):
    schema_version: Literal["receipt-filter-preview/v3"] = "receipt-filter-preview/v3"
    limitation_codes: tuple[str, ...]


class AggregateFacetRequest(AggregatePreviewRequest):
    facet: RelationalFacetQuery


class CatalogCount(Strict):
    definition: FilterCountVersion
    observation: AggregateObservation
    evidence_hash: Hash
    label: FilterLabels


class AggregateCatalogResponse(Strict):
    schema_version: Literal["receipt-filter-catalog/v3"] = "receipt-filter-catalog/v3"
    dataset_version_id: UUID
    root_entity: Literal["Receipt"] = "Receipt"
    registry_versions: dict[str, UUID]
    legacy_registry_version_id: UUID
    fields: list[CatalogField]
    relationships: list[CatalogRelationship]
    mandatory_expressions: dict[str, FlatExpression]
    child_authorization: Literal["inherits_correlated_receipt_store_ceiling"] = (
        "inherits_correlated_receipt_store_ceiling"
    )
    resource_policy_version_id: UUID
    limitation_codes: tuple[str, ...]
    counts: tuple[CatalogCount, ...]
