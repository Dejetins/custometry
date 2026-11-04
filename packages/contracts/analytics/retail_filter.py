"""Persisted published-receipt filtering and bounded browser projections."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Annotated, Any, Literal, Protocol, TYPE_CHECKING
from uuid import UUID

from pydantic import Field, ConfigDict, model_validator

if TYPE_CHECKING:
    from packages.contracts.analytics.receipt_selection import ReceiptSelection

from packages.contracts.analytics.columnar_filters import FlatExpression, FilterResourcePolicy
from packages.contracts.semantic import Hash, Strict
from packages.contracts.semantic.filter_fields import FilterFieldVersion


class ReceiptFilterInput(Strict):
    model_config = ConfigDict(extra="forbid", json_schema_mode_override="validation")
    schema_version: Literal["receipt-filter/v1"] = "receipt-filter/v1"
    registry_version_id: UUID
    expression: FlatExpression


class FilterPreviewRequest(Strict):
    dataset_version_id: UUID
    filter: ReceiptFilterInput


class FilterFacetQuery(Strict):
    field_id: Annotated[str, Field(min_length=1, max_length=128)]
    search: Annotated[str, Field(max_length=100)] = ""
    limit: Annotated[int, Field(strict=True, ge=1, le=50)] = 20
    offset: Annotated[int, Field(strict=True, ge=0, le=1000)] = 0


class FilterFacetRequest(FilterPreviewRequest):
    facet: FilterFacetQuery


class FilterFacetValue(Strict):
    value: str | None
    count: Annotated[int, Field(strict=True, ge=0)]


class FilterFacetResponse(Strict):
    values: list[FilterFacetValue]
    has_more: bool
    request_hash: Hash


class FilterPreviewResponse(Strict):
    request_hash: Hash
    matched_count: int
    not_matched_count: int
    unknown_count: int
    authorized_count: int
    preview_kind: Literal["exact"] = "exact"


class FilterLabels(Strict):
    ru: str
    en: str


class CatalogField(Strict):
    field: FilterFieldVersion
    label: FilterLabels
    description: FilterLabels


class FilterCatalogResponse(Strict):
    registry_version_id: UUID
    dataset_version_id: UUID
    entity: Literal["Receipt"] = "Receipt"
    fields: list[CatalogField]
    mandatory_expression: FlatExpression
    resource_policy_version_id: UUID


@dataclass(frozen=True)
class ReceiptFilterProjection:
    inputs: dict[str, Any]
    data_as_of: datetime | None
    selection: ReceiptSelectionEvidence | None = None


class ReceiptSelectionEvidence(Strict):
    schema_version: Literal["receipt-selection-evidence/v2"] = "receipt-selection-evidence/v2"
    count_scope: Literal["authorized_dataset"] = "authorized_dataset"
    request_hash: Hash
    matched_count: Annotated[int, Field(strict=True, ge=0)]
    not_matched_count: Annotated[int, Field(strict=True, ge=0)]
    unknown_count: Annotated[int, Field(strict=True, ge=0)]
    authorized_count: Annotated[int, Field(strict=True, ge=0)]
    limitation_codes: tuple[str, ...]

    @model_validator(mode="after")
    def counts(self) -> ReceiptSelectionEvidence:
        if (
            self.matched_count + self.not_matched_count + self.unknown_count
            != self.authorized_count
        ):
            raise ValueError("FILTER_RESULT_COUNTS")
        return self


class BoundedSalesInputPort(Protocol):
    def read_bounded_sales_inputs(
        self,
        *,
        workspace_id: UUID,
        bindings: list[dict[str, Any]],
        supporting_artifacts: list[str],
        policy: FilterResourcePolicy,
        metadata_only: bool,
    ) -> dict[str, Any]: ...


class ReceiptFilterPort(Protocol):
    def inputs(
        self,
        workspace: UUID,
        actor: UUID,
        dataset: UUID,
        value: ReceiptSelection,
        source: dict[str, Any],
        *,
        metadata_only: bool = False,
    ) -> dict[str, Any]: ...
    def fingerprint(
        self, workspace: UUID, actor: UUID, dataset: UUID, value: ReceiptSelection
    ) -> str: ...
    def project(
        self,
        workspace: UUID,
        actor: UUID,
        dataset: UUID,
        value: ReceiptSelection,
        inputs: dict[str, Any],
    ) -> ReceiptFilterProjection: ...
