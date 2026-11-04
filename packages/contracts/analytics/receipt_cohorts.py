"""Explicit receipt-root membership in an authorized observed customer cohort."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Annotated, Literal
from uuid import UUID
from pydantic import ConfigDict, Field
from packages.contracts.semantic import Strict
from packages.contracts.semantic.filter_fields import Name
from packages.contracts.analytics.relational_filters import ScopedNode, ScopedPredicate
from packages.contracts.analytics.aggregate_filters import AggregateCompare
from packages.contracts.analytics.sequence_filters import SequenceExpression, SequenceInputGrant
from packages.contracts.analytics.customer_events import (
    ObservedChildRootRestriction,
    CustomerEventRelationship,
    CatalogEvent,
)
from packages.contracts.analytics.retail_relational import RelationalFacetQuery
from packages.contracts.analytics.retail_filter import FilterPreviewResponse, CatalogField
from packages.contracts.analytics.retail_aggregate import CatalogCount
from packages.contracts.analytics.columnar_filters import FlatExpression


class CustomerEventMembership(ScopedNode):
    kind: Literal["customer_event_membership"] = "customer_event_membership"
    customer_scope_id: UUID
    relationship_id: Name
    relationship_version_id: UUID
    predicate: SequenceExpression


class CohortBoolean(ScopedNode):
    kind: Literal["and", "or"]
    children: tuple[CohortExpression, ...] = Field(min_length=1, max_length=1000)


class CohortNot(ScopedNode):
    kind: Literal["not"] = "not"
    child: CohortExpression


class CohortExists(ScopedNode):
    kind: Literal["exists", "not_exists"]
    parent_scope_id: UUID
    child_scope_id: UUID
    child_entity: Name
    relationship_id: Name
    relationship_version_id: UUID
    predicate: CohortExpression


CohortExpression = Annotated[
    ScopedPredicate
    | AggregateCompare
    | CustomerEventMembership
    | CohortBoolean
    | CohortNot
    | CohortExists,
    Field(discriminator="kind"),
]
for model in (CohortBoolean, CohortNot, CohortExists):
    model.model_rebuild()


class CohortFilterRequest(Strict):
    schema_version: Literal["cohort-filter-execution/v1"] = "cohort-filter-execution/v1"
    workspace_id: UUID
    dataset_version_id: UUID
    root_entity: Literal["Receipt"] = "Receipt"
    root_scope_id: UUID
    registry_versions: dict[Name, UUID]
    receipt_registry_versions: dict[Name, UUID]
    promoted_registry_sets: tuple[dict[Name, UUID], ...] = Field(default=(), max_length=32)
    expression: CohortExpression
    compatibility_registry_version_id: UUID | None = None


@dataclass(frozen=True, slots=True)
class ReceiptCohortGrant(SequenceInputGrant):
    root_restrictions: tuple[ObservedChildRootRestriction, ...] = ()
    receipt_registry_versions: tuple[tuple[str, UUID], ...] = ()
    facet_fields: tuple[tuple[str, str], ...] = ()


class CohortReceiptFilterInput(Strict):
    model_config = ConfigDict(extra="forbid", json_schema_mode_override="validation")
    schema_version: Literal["receipt-filter/v4"] = "receipt-filter/v4"
    root_scope_id: UUID
    registry_versions: dict[str, UUID]
    receipt_registry_versions: dict[str, UUID]
    promoted_registry_sets: tuple[dict[str, UUID], ...] = Field(default=(), max_length=32)
    expression: CohortExpression
    legacy_registry_version_id: UUID | None = None


def receipt_cohort_request(
    workspace: UUID, dataset: UUID, value: CohortReceiptFilterInput
) -> CohortFilterRequest:
    return CohortFilterRequest(
        workspace_id=workspace,
        dataset_version_id=dataset,
        **value.model_dump(exclude={"schema_version", "legacy_registry_version_id"}),
        compatibility_registry_version_id=value.legacy_registry_version_id,
    )


class CohortPreviewRequest(Strict):
    dataset_version_id: UUID
    filter: CohortReceiptFilterInput


class CohortPreviewResponse(FilterPreviewResponse):
    schema_version: Literal["receipt-filter-preview/v4"] = "receipt-filter-preview/v4"
    limitation_codes: tuple[str, ...]
    count_grain: Literal["receipts"] = "receipts"
    universe: ObservedChildRootRestriction


class CohortFacetRequest(CohortPreviewRequest):
    facet: RelationalFacetQuery


class CohortCatalogResponse(Strict):
    schema_version: Literal["receipt-filter-catalog/v4"] = "receipt-filter-catalog/v4"
    root_entity: Literal["Receipt"] = "Receipt"
    dataset_version_id: UUID
    registry_versions: dict[str, UUID]
    receipt_registry_versions: dict[str, UUID]
    legacy_registry_version_id: UUID
    fields: list[CatalogField]
    facet_field_ids: dict[str, tuple[str, ...]]
    relationships: list[CustomerEventRelationship]
    events: tuple[CatalogEvent, ...]
    counts: tuple[CatalogCount, ...]
    mandatory_expressions: dict[str, FlatExpression]
    universe: ObservedChildRootRestriction
    resource_policy_version_id: UUID
    limitation_codes: tuple[str, ...]
