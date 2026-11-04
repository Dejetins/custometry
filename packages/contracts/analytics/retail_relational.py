"""Published receipt/item correlation: server projection and count-only HTTP DTOs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol
from uuid import UUID
from pydantic import ConfigDict
from packages.contracts.semantic import Hash, Strict
from packages.contracts.analytics.columnar_filters import PublishedRetailFilter, FlatExpression
from packages.contracts.analytics.relational_filters import (
    RelationshipInput,
    ScopedExpression,
    RelationalFilterRequest,
)
from packages.contracts.analytics.retail_filter import (
    CatalogField,
    FilterLabels,
    FilterPreviewResponse,
    FilterFacetQuery,
    FilterFacetResponse,
)
from packages.contracts.semantic.relationships import FilterRelationshipVersion


@dataclass(frozen=True, slots=True)
class PublishedRetailRelations:
    entities: tuple[PublishedRetailFilter, ...]
    relationships: tuple[RelationshipInput, ...]
    legacy_registry_version_id: UUID


class RetailRelationsSemanticPort(Protocol):
    def retail_relational_projection(
        self, *, workspace_id: UUID, dataset_version_id: UUID
    ) -> PublishedRetailRelations: ...


class RelationalReceiptFilterInput(Strict):
    model_config = ConfigDict(extra="forbid", json_schema_mode_override="validation")
    schema_version: Literal["receipt-filter/v2"] = "receipt-filter/v2"
    root_scope_id: UUID
    registry_versions: dict[str, UUID]
    expression: ScopedExpression
    legacy_registry_version_id: UUID | None = None


class RelationalPreviewRequest(Strict):
    dataset_version_id: UUID
    filter: RelationalReceiptFilterInput


def receipt_relational_request(
    workspace: UUID, dataset: UUID, value: RelationalReceiptFilterInput
) -> RelationalFilterRequest:
    return RelationalFilterRequest(
        workspace_id=workspace,
        dataset_version_id=dataset,
        root_entity="Receipt",
        root_scope_id=value.root_scope_id,
        registry_versions=value.registry_versions,
        expression=value.expression,
        compatibility_registry_version_id=value.legacy_registry_version_id,
    )


class RelationalPreviewResponse(FilterPreviewResponse):
    schema_version: Literal["receipt-filter-preview/v2"] = "receipt-filter-preview/v2"
    limitation_codes: tuple[str, ...]


class RelationalFacetQuery(FilterFacetQuery):
    entity: Literal["Receipt", "ReceiptItem"]


class RelationalFacetRequest(RelationalPreviewRequest):
    facet: RelationalFacetQuery


class RelationalFacetResponse(FilterFacetResponse):
    count_grain: Literal["matching_receipts", "observed_items_in_matching_receipts"]


class CatalogRelationship(Strict):
    relationship: FilterRelationshipVersion
    label: FilterLabels
    complete: bool
    completeness_hash: Hash


class RelationalCatalogResponse(Strict):
    schema_version: Literal["receipt-filter-catalog/v2"] = "receipt-filter-catalog/v2"
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
