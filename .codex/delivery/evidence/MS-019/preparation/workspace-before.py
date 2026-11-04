"""Strict metric-workspace/v2 wire shapes; calculation/activation belongs to S02/S03."""

from __future__ import annotations
from datetime import date, datetime
from typing import Annotated, Literal, Protocol, Any, cast
from uuid import UUID
from pydantic import (
    Field,
    model_validator,
    BeforeValidator,
    model_serializer,
    SerializerFunctionWrapHandler,
)
from packages.contracts.semantic import CalendarRef, Hash, Strict
from packages.contracts.semantic.store_filters import StoreFilterV1
from packages.contracts.analytics.retail_filter import ReceiptFilterInput
from packages.contracts.analytics.temporal import TemporalSettingsV2, ResolvedTemporalSpecV2

MetricId = Literal["net_revenue", "receipt_count", "average_receipt"]
Grain = Literal["day", "week", "month", "quarter", "half_year", "year"]
CalendarBasis = Literal["calendar", "fiscal"]
DecimalValue = Annotated[str, Field(pattern=r"^-?(?:0|[1-9][0-9]*)(?:\.[0-9]*[1-9])?$")]
StoreId = Annotated[str, Field(min_length=1, max_length=128, pattern=r"\S")]


def canonical_stores(value: object) -> object:
    if not isinstance(value, list):
        return value
    items = cast(list[object], value)
    if not all(isinstance(item, str) for item in items):
        return items
    return sorted({item for item in items if isinstance(item, str)})


Stores = Annotated[list[StoreId], Field(max_length=1000), BeforeValidator(canonical_stores)]


class MetricRef(Strict):
    metric_id: MetricId
    version_id: UUID
    content_hash: Hash


class NumberFormat(Strict):
    decimal_places: Annotated[int, Field(strict=True, ge=0, le=2)]


class Period(Strict):
    starts_on: date
    ends_on: date

    @model_validator(mode="after")
    def bounded(self) -> Period:
        if self.ends_on < self.starts_on or (self.ends_on - self.starts_on).days >= 366:
            raise ValueError("WORKSPACE_LIMIT_EXCEEDED:current_days")
        return self


class QueryContext(Period):
    store_ids: Stores | None


class EffectiveContext(Period):
    time_comparison: ResolvedTemporalSpecV2 | None = None
    scope_hash: Hash | None = None

    @model_serializer(mode="wrap")
    def preserve_old_context(self, handler: SerializerFunctionWrapHandler):
        value: dict[str, Any] = handler(self)
        if "time_comparison" not in self.model_fields_set:
            value.pop("time_comparison", None)
        if "scope_hash" not in self.model_fields_set:
            value.pop("scope_hash", None)
        return value

    store_ids: Stores
    grain: Grain
    calendar_ref: CalendarRef
    calendar_basis: CalendarBasis
    timezone: Annotated[str, Field(min_length=1, max_length=128)] = "UTC"
    week_start: Literal["monday"] = "monday"
    alignment: Literal["none", "previous_year_same_dates"]


class ArtifactRef(Strict):
    artifact_id: UUID
    content_hash: Hash


class ResultRef(Strict):
    result_id: UUID
    schema_version: Literal["metric-workspace/v2"]
    manifest: ArtifactRef


class Coverage(Strict):
    state: Literal["complete", "partial", "unavailable"]
    expected_days: Annotated[int, Field(strict=True, ge=0)]
    calendar_days: Annotated[int, Field(strict=True, ge=0)]
    declared_complete_days: Annotated[int, Field(strict=True, ge=0)]
    observed_days: Annotated[int, Field(strict=True, ge=0)]
    eligible_receipts: Annotated[int, Field(strict=True, ge=0)]
    reason_codes: list[str]


class MetricValues(Strict):
    net_revenue: DecimalValue | None
    receipt_count: DecimalValue | None
    average_receipt: DecimalValue | None


class WorkspaceBucket(Strict):
    bucket_id: str
    natural_starts_on: date
    natural_ends_on: date
    effective_starts_on: date
    effective_ends_on: date
    bucket_start: date
    bucket_end_exclusive: date
    effective_start: date
    effective_end_exclusive: date
    is_partial_bucket: bool
    calendar_ref: CalendarRef
    calendar_basis: CalendarBasis
    fiscal_year: int | None
    fiscal_quarter: int | None
    fiscal_half: int | None
    label: str
    clipped: bool
    values: MetricValues
    state: Literal["ready", "no_data", "incomplete"]
    coverage: Coverage


class ComparisonSide(Strict):
    card_id: UUID
    metric_ref: MetricRef
    result: ResultRef
    unit: Literal["EUR", "receipt", "EUR/receipt"]
    format: NumberFormat
    context: EffectiveContext
    baseline_dates: list[date] | None


class ComparisonValues(Strict):
    left_coverage: Coverage
    right_coverage: Coverage
    left: DecimalValue | None
    right: DecimalValue | None
    absolute_delta: DecimalValue | None
    relative_delta_percent: DecimalValue | None
    reason_codes: list[str]


class ComparisonBucket(ComparisonValues):
    bucket_id: str


class CardComparisonV1(Strict):
    schema_version: Literal["card-comparison/v1"]
    mode: Literal["temporal", "pair"]
    left: ComparisonSide
    right: ComparisonSide
    comparability_status: Literal["comparable", "descriptive", "unavailable"]
    buckets: list[ComparisonBucket]
    totals: ComparisonValues
    coverage: Coverage
    manifest: ArtifactRef

    @model_validator(mode="after")
    def units_and_identity(self) -> CardComparisonV1:
        if self.mode == "pair" and self.left.card_id == self.right.card_id:
            raise ValueError("PAIR_REQUIRES_DISTINCT_CARDS")
        if self.left.unit != self.right.unit:
            values = [self.totals, *self.buckets]
            if any(
                v.absolute_delta is not None or v.relative_delta_percent is not None for v in values
            ):
                raise ValueError("CROSS_UNIT_DELTA_UNSUPPORTED")
        return self


class WorkspaceLineage(Strict):
    source_artifacts: list[ArtifactRef]
    metric_components: list[MetricRef]
    source_calendar_version_id: UUID
    data_as_of: datetime


class WorkspaceTrust(Strict):
    status: Literal["ready", "no_data", "comparison_unavailable"]
    reason_codes: list[str]


class DayAlignment(Strict):
    current_date: date
    baseline_date: date | None


class TemporalBucket(Strict):
    bucket_id: str
    baseline_dates: list[date]
    values: MetricValues
    coverage: Coverage
    changes: dict[MetricId, ComparisonValues]


class TemporalProjection(Strict):
    alignment: Literal["previous_year_same_dates"]
    mapping: list[DayAlignment]
    baseline_dates: list[date]
    excluded_baseline_dates: list[date]
    buckets: list[TemporalBucket]
    totals: MetricValues
    coverage: Coverage
    changes: dict[MetricId, ComparisonValues]
    reason_codes: list[str]


class WorkspaceDay(Strict):
    date: date
    values: MetricValues
    coverage: Coverage


class TemporalMetricChangesV2(Strict):
    net_revenue: ComparisonValues
    receipt_count: ComparisonValues
    average_receipt: ComparisonValues


class TemporalPairBucketV2(Strict):
    current_bucket_id: str | None
    comparison_bucket_id: str | None
    current_dates: list[date]
    comparison_dates: list[date]
    changes: TemporalMetricChangesV2


class TemporalArtifactV2(Strict):
    schema_version: Literal["time-comparison-artifact/v2"] = "time-comparison-artifact/v2"
    artifact_id: UUID
    content_hash: Hash
    request_hash: Hash
    policy_hash: Hash
    spec: ResolvedTemporalSpecV2
    semantic_dataset_version_id: UUID
    metric_refs: list[MetricRef]
    normalized_filter_hash: Hash
    evaluated_current_dates: list[date]
    evaluated_comparison_dates: list[date]
    buckets: list[TemporalPairBucketV2]
    changes: TemporalMetricChangesV2
    comparability_status: Literal["comparable", "partial", "descriptive", "unavailable"]
    limitation_codes: list[str]


class WorkspaceResultV2(Strict):
    temporal_v2: TemporalArtifactV2 | None = None

    @model_serializer(mode="wrap")
    def preserve_old_result(self, handler: SerializerFunctionWrapHandler):
        value: dict[str, Any] = handler(self)
        if "temporal_v2" not in self.model_fields_set:
            value.pop("temporal_v2", None)
        return value

    schema_version: Literal["metric-workspace/v2"]
    result_id: UUID
    request_hash: Hash
    policy_hash: Hash
    semantic_dataset_version_id: UUID
    publication_hash: Hash
    effective_context: EffectiveContext
    metric_refs: list[MetricRef]
    buckets: list[WorkspaceBucket]
    totals: MetricValues
    coverage: Coverage
    comparison: CardComparisonV1 | None
    temporal: TemporalProjection | None
    daily: list[WorkspaceDay]
    lineage: WorkspaceLineage
    trust: WorkspaceTrust
    manifest: ArtifactRef


class CardResultBinding(Strict):
    card_id: UUID
    metric_ref: MetricRef
    result: ResultRef
    effective_context_hash: Hash
    configuration_hash: Hash
    bucket_projection: MetricId
    unit: Literal["EUR", "receipt", "EUR/receipt"]
    format: NumberFormat
    readiness: Literal["ready", "no_data", "comparison_unavailable"]

    @model_validator(mode="after")
    def consistent_metric(self) -> CardResultBinding:
        units = {"net_revenue": "EUR", "receipt_count": "receipt", "average_receipt": "EUR/receipt"}
        if (
            self.bucket_projection != self.metric_ref.metric_id
            or self.unit != units[self.metric_ref.metric_id]
        ):
            raise ValueError("METRIC_PROJECTION_MISMATCH")
        return self


class WorkspaceScopeInput(Strict):
    schema_version: Literal["workspace-scope/v1"] = "workspace-scope/v1"
    dependency_hash: Hash
    filters: list[StoreFilterV1]


class WorkspaceRunRequest(Strict):
    time_comparison: TemporalSettingsV2 | None = None
    receipt_filter: ReceiptFilterInput | None = None
    scope: WorkspaceScopeInput | None = None

    @model_serializer(mode="wrap")
    def preserve_old_request(self, handler: SerializerFunctionWrapHandler):
        value: dict[str, Any] = handler(self)
        if "time_comparison" not in self.model_fields_set:
            value.pop("time_comparison", None)
        if "scope" not in self.model_fields_set:
            value.pop("scope", None)
        if "receipt_filter" not in self.model_fields_set:
            value.pop("receipt_filter", None)
        return value

    semantic_dataset_version_id: UUID
    common: QueryContext
    local_store_ids: Stores | None
    grain: Grain
    calendar_ref: CalendarRef
    calendar_basis: CalendarBasis
    alignment: Literal["none", "previous_year_same_dates"]
    metric_refs: Annotated[list[MetricRef], Field(min_length=1, max_length=3)]

    @model_validator(mode="after")
    def one_comparison_contract(self) -> WorkspaceRunRequest:
        if self.time_comparison is not None and self.alignment != "none":
            raise ValueError("COMPARISON_CONTRACT_CONFLICT")
        return self


class WorkspaceScopePreflight(Strict):
    schema_version: Literal["workspace-scope-preflight/v1"] = "workspace-scope-preflight/v1"
    request_hash: Hash
    effective_context: EffectiveContext
    provider: Literal["metric-workspace/v2"] = "metric-workspace/v2"
    dimensions: list[Literal["date", "store_id"]] = ["date", "store_id"]
    filter_operators: list[Literal["store_in", "and", "or", "not"]] = [
        "store_in",
        "and",
        "or",
        "not",
    ]
    comparison_modes: list[
        Literal[
            "none",
            "previous_year_same_dates",
            "previous_period",
            "custom_period",
            "previous_year_calendar_aligned",
            "previous_year_iso_week_aligned",
            "previous_year_fiscal_period",
            "previous_year_comparable_elapsed_days",
            "pair",
        ]
    ] = [
        "none",
        "previous_year_same_dates",
        "previous_period",
        "custom_period",
        "previous_year_calendar_aligned",
        "previous_year_iso_week_aligned",
        "previous_year_fiscal_period",
        "previous_year_comparable_elapsed_days",
        "pair",
    ]
    estimate_state: Literal["unavailable"] = "unavailable"
    reuse: Literal["reuse", "new_compute"]
    locked_metric_rules: list[dict[str, str]]
    unsupported: list[str] = [
        "general_filter_registry",
        "channels",
        "relationships",
        "populations",
        "relative_windows",
    ]


class WorkspaceAccess(Strict):
    """Trusted server projection. Never populated from an HTTP request body."""

    workspace_id: UUID
    principal_id: UUID
    semantic_dataset_version_id: UUID
    policy_hash: Hash
    allowed_store_ids: Stores
    permissions: frozenset[str]


class WorkspaceAccessPort(Protocol):
    def resolve(
        self,
        *,
        workspace_id: UUID,
        principal_id: UUID,
        dataset_id: UUID,
        action: Literal["read", "run"],
    ) -> WorkspaceAccess: ...


class WorkspaceArtifactPort(Protocol):
    def read_sales_inputs(
        self, *, workspace_id: UUID, bindings: list[dict[str, Any]], supporting_artifacts: list[str]
    ) -> dict[str, tuple[dict[str, Any], ...]]: ...
    def commit_workspace(
        self, *, workspace_id: UUID, payload: dict[str, Any], bindings: list[dict[str, Any]]
    ) -> dict[str, Any]: ...
    def verify_workspace(self, *, workspace_id: UUID, payload: dict[str, Any]) -> None: ...


class WorkspaceCardRequest(Strict):
    card_id: UUID
    configuration_hash: Hash
    metric_ref: MetricRef
    query: WorkspaceRunRequest


class WorkspaceApplyResult(Strict):
    schema_version: Literal["workspace-apply/v2"] = "workspace-apply/v2"
    results: list[WorkspaceResultV2]
    bindings: list[CardResultBinding]
