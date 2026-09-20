"""Configured report and personal Saved View contracts; no mounted v2 consumers."""

from __future__ import annotations
from typing import Annotated, Literal, Protocol
from uuid import UUID, uuid4, uuid5
from pydantic import Field, RootModel, model_validator
from packages.contracts.semantic import CalendarRef, Hash, Strict
from packages.contracts.analytics.workspace import (
    ArtifactRef,
    CalendarBasis,
    CardComparisonV1,
    CardResultBinding,
    Grain,
    MetricRef,
    QueryContext,
    Stores,
)
from packages.contracts.presentation import (
    AnalyticalDocumentCompositionV1,
    DraftResponse,
    LineChartSpecV1,
    Reference,
    Page,
    Section,
    Block,
)

Name = Annotated[str, Field(min_length=1, max_length=200, pattern=r"\S")]


class LocalizedName(Strict):
    ru: Name
    en: Name


class Card(Strict):
    card_id: UUID
    metric_ref: MetricRef
    local_store_ids: Stores | None
    population_binding: None = None
    target_action_binding: None = None


class Workset(Strict):
    workset_id: UUID
    name: LocalizedName
    visibility: Literal["personal"]
    owner_principal_id: UUID
    cards: Annotated[list[Card], Field(max_length=50)]


class SingleSelection(Strict):
    mode: Literal["single"]
    card_id: UUID
    temporal: Literal["none", "previous_year_same_dates"]
    display: Literal["series", "delta_trend"]

    @model_validator(mode="after")
    def delta_requires_temporal(self) -> SingleSelection:
        if self.display == "delta_trend" and self.temporal == "none":
            raise ValueError("DELTA_REQUIRES_COMPARISON")
        return self


class PairSelection(Strict):
    mode: Literal["pair"]
    left_card_id: UUID
    right_card_id: UUID
    display: Literal["series"]

    @model_validator(mode="after")
    def different_cards(self) -> PairSelection:
        if self.left_card_id == self.right_card_id:
            raise ValueError("PAIR_REQUIRES_DISTINCT_CARDS")
        return self


AnalysisSelection = Annotated[SingleSelection | PairSelection, Field(discriminator="mode")]


def selection_ids(selection: AnalysisSelection | None) -> set[UUID]:
    if selection is None:
        return set()
    if isinstance(selection, SingleSelection):
        return {selection.card_id}
    return {selection.left_card_id, selection.right_card_id}


class BaseSnapshotRef(Strict):
    version_id: UUID
    snapshot_id: UUID
    manifest: ArtifactRef


class ConfiguredReportV2(Strict):
    schema_version: Literal["configured-report/v2"]
    report_id: UUID
    creator_principal_id: UUID
    title: Name
    semantic_dataset_version_id: UUID
    common_context: QueryContext
    grain: Grain
    calendar_ref: CalendarRef
    calendar_basis: CalendarBasis
    worksets: Annotated[list[Workset], Field(max_length=20)]
    default_workset_id: UUID | None
    selection: AnalysisSelection | None
    brand_profile: Reference
    company_pack: Reference
    base_snapshot_ref: BaseSnapshotRef

    @model_validator(mode="after")
    def coherence(self) -> ConfiguredReportV2:
        workset_ids = [w.workset_id for w in self.worksets]
        cards = [c for w in self.worksets for c in w.cards]
        card_ids = [c.card_id for c in cards]
        if len(set(workset_ids + card_ids)) != len(workset_ids + card_ids):
            raise ValueError("DUPLICATE_INSTANCE_ID")
        if len(cards) > 200:
            raise ValueError("WORKSPACE_LIMIT_EXCEEDED:total_cards")
        if any(w.owner_principal_id != self.creator_principal_id for w in self.worksets):
            raise ValueError("PERSONAL_WORKSET_OWNER_MISMATCH")
        if self.default_workset_id is None:
            if self.worksets or self.selection is not None:
                raise ValueError("DEFAULT_WORKSET_REQUIRED")
        elif self.default_workset_id not in workset_ids:
            raise ValueError("UNKNOWN_WORKSET")
        else:
            active = next(w for w in self.worksets if w.workset_id == self.default_workset_id)
            if not selection_ids(self.selection).issubset({c.card_id for c in active.cards}):
                raise ValueError("SELECTION_OUTSIDE_ACTIVE_WORKSET")
        all_stores = set(self.common_context.store_ids or [])
        for card in cards:
            all_stores.update(card.local_store_ids or [])
        if len(all_stores) > 1000:
            raise ValueError("WORKSPACE_LIMIT_EXCEEDED:store_ids")
        if len(self.model_dump_json().encode()) > 1024 * 1024:
            raise ValueError("WORKSPACE_LIMIT_EXCEEDED:configuration_bytes")
        return self


def parse_configuration(raw: bytes) -> ConfiguredReportV2:
    if len(raw) > 1024 * 1024:
        raise ValueError("WORKSPACE_LIMIT_EXCEEDED:configuration_bytes")
    return ConfiguredReportV2.model_validate_json(raw)


def copy_card(card: Card) -> Card:
    return card.model_copy(update={"card_id": uuid4()})


def copy_workset(
    workset: Workset, selection: AnalysisSelection | None = None
) -> tuple[Workset, AnalysisSelection | None]:
    mapping = {card.card_id: uuid4() for card in workset.cards}
    cards = [card.model_copy(update={"card_id": mapping[card.card_id]}) for card in workset.cards]
    result = workset.model_copy(update={"workset_id": uuid4(), "cards": cards})
    if not selection_ids(selection).issubset(mapping):
        raise ValueError("SELECTION_OUTSIDE_COPIED_WORKSET")
    if isinstance(selection, SingleSelection):
        selection = selection.model_copy(update={"card_id": mapping[selection.card_id]})
    elif isinstance(selection, PairSelection):
        selection = selection.model_copy(
            update={
                "left_card_id": mapping[selection.left_card_id],
                "right_card_id": mapping[selection.right_card_id],
            }
        )
    return result, selection


def legacy_instance_ids(report_id: UUID) -> tuple[UUID, dict[str, UUID]]:
    return uuid5(report_id, "legacy/workset"), {
        m: uuid5(report_id, f"legacy/card/{m}")
        for m in ("net_revenue", "receipt_count", "average_receipt")
    }


def creator_saved_view_id(report_id: UUID, creator_id: UUID) -> UUID:
    return uuid5(report_id, f"personal/{creator_id}")


class ViewQueryContext(QueryContext):
    grain: Grain


class ViewDisplay(Strict):
    active_workset_id: UUID | None
    selection: AnalysisSelection | None
    card_order: list[UUID]
    hidden_card_ids: list[UUID]
    representation: Literal["chart", "table"]
    density: Literal["comfortable", "compact"]

    @model_validator(mode="after")
    def unique_order(self) -> ViewDisplay:
        if len(self.card_order) != len(set(self.card_order)) or len(self.hidden_card_ids) != len(
            set(self.hidden_card_ids)
        ):
            raise ValueError("DUPLICATE_INSTANCE_ID")
        return self


class ReaderViewOverride(Strict):
    query_context: ViewQueryContext
    display: ViewDisplay


class SavedViewV1(Strict):
    schema_version: Literal["saved-view/v1"]
    saved_view_id: UUID
    version_id: UUID
    revision: Annotated[int, Field(strict=True, gt=0)]
    workspace_id: UUID
    owner_principal_id: UUID
    report_id: UUID
    document_version_id: UUID
    document_content_hash: Hash
    calendar_ref: CalendarRef
    calendar_basis: CalendarBasis
    page_ids: list[UUID]
    result_scope: list[CardResultBinding]
    query_context: ViewQueryContext
    display: ViewDisplay


class ChartSeriesRef(Strict):
    card_id: UUID
    artifact: ArtifactRef
    field: Literal[
        "net_revenue",
        "receipt_count",
        "average_receipt",
        "left",
        "right",
        "absolute_delta",
        "relative_delta_percent",
    ]
    axis: Literal["left", "right"]
    unit: Literal["EUR", "receipt", "EUR/receipt", "percent"]


class WorkspaceChartSpecV2(Strict):
    schema_version: Literal["2.0.0"]
    chart_spec_id: UUID
    workspace_id: UUID
    chart_type: Literal["line"]
    selection: AnalysisSelection
    series: Annotated[list[ChartSeriesRef], Field(min_length=1, max_length=2)]
    comparison: ArtifactRef | None
    accessibility_table: ArtifactRef


class ChartSpec(
    RootModel[
        Annotated[LineChartSpecV1 | WorkspaceChartSpecV2, Field(discriminator="schema_version")]
    ]
):
    pass


class WorkspaceFilterBinding(Strict):
    scope: Literal["document", "workset", "card"]
    scope_resource_id: UUID
    expression: QueryContext
    combine_mode: Literal["intersect"]
    linked_target_block_ids: list[UUID]
    precedence: list[Literal["security", "system_locked", "source_metric", "document", "card"]]
    policy_hash: Hash
    owner_principal_id: UUID


class AnalyticalDocumentCompositionV2(Strict):
    composition_schema_version: Literal[2]
    analytical_document_version_id: UUID
    analytical_document_id: UUID
    workspace_id: UUID
    profile: Literal["workbook_report"]
    source_owner_ref: dict[str, str]
    navigation_mode: Literal["tabs"]
    default_page_id: UUID
    chapters: list[dict[str, str]]
    pages: list[Page]
    sections: list[Section]
    blocks: list[Block]
    brand_profile_version_id: UUID
    access_policy_id: UUID
    filter_scope_bindings: list[WorkspaceFilterBinding]
    definition: ConfiguredReportV2
    chart_specs: list[Reference]
    bindings_by_card: list[CardResultBinding]

    @model_validator(mode="after")
    def complete_bindings(self) -> AnalyticalDocumentCompositionV2:
        cards = {c.card_id: c for w in self.definition.worksets for c in w.cards}
        ids = [b.card_id for b in self.bindings_by_card]
        if set(ids) != set(cards) or len(ids) != len(set(ids)):
            raise ValueError("INCOMPLETE_CARD_BINDINGS")
        if self.analytical_document_id != self.definition.report_id:
            raise ValueError("REPORT_ID_MISMATCH")
        for binding in self.bindings_by_card:
            if binding.metric_ref != cards[binding.card_id].metric_ref:
                raise ValueError("METRIC_BINDING_MISMATCH")
        return self


class AnalyticalDocumentComposition(
    RootModel[
        Annotated[
            AnalyticalDocumentCompositionV1 | AnalyticalDocumentCompositionV2,
            Field(discriminator="composition_schema_version"),
        ]
    ]
):
    pass


class CreatorApplyRequest(Strict):
    contract_version: Literal["configured-report/v2"]
    mode: Literal["creator"]
    base_revision: Annotated[int, Field(strict=True, ge=1)]
    definition: ConfiguredReportV2


class ReaderApplyRequest(Strict):
    contract_version: Literal["configured-report/v2"]
    mode: Literal["reader"]
    base_revision: Annotated[int, Field(strict=True, ge=1)]
    view_override: ReaderViewOverride


class WorkspaceApplyRequest(
    RootModel[Annotated[CreatorApplyRequest | ReaderApplyRequest, Field(discriminator="mode")]]
):
    pass


class WorkspaceApplyResponse(Strict):
    contract_version: Literal["configured-report/v2"]
    configuration_hash: Hash
    definition: ConfiguredReportV2 | None
    view_context: ReaderViewOverride | None
    bindings_by_card: list[CardResultBinding]
    comparison: CardComparisonV1 | None
    chart_specs: list[Reference]
    base_revision: Annotated[int, Field(strict=True, ge=1)]
    access_fingerprint: Hash
    status: Literal["ready", "no_data", "comparison_unavailable"]


class WorkspaceSaveRequest(Strict):
    contract_version: Literal["configured-report/v2"]
    definition: ConfiguredReportV2
    expected_revision: Annotated[int, Field(strict=True, ge=1)]
    expected_saved_view_revision: Annotated[int, Field(strict=True, ge=0)]
    idempotency_key: UUID
    configuration_hash: Hash
    result_ids: list[UUID]
    chart_specs: list[Reference]


class SaveViewRequest(Strict):
    contract_version: Literal["saved-view/v1"]
    document_version_id: UUID
    expected_revision: Annotated[int, Field(strict=True, ge=0)]
    idempotency_key: UUID
    view_override: ReaderViewOverride
    result_ids: list[UUID]


class ReportCapabilities(Strict):
    definition_edit: bool
    view_apply: bool
    saved_view_save: bool
    exact_preview: bool


class WorkspaceReportResponse(Strict):
    contract_version: Literal["configured-report/v2"]
    report_id: UUID
    revision: Annotated[int, Field(strict=True, ge=1)]
    version_id: UUID
    snapshot_id: UUID
    author_principal_id: UUID
    saved_at: str
    composition: AnalyticalDocumentCompositionV2
    saved_view: Reference
    manifest: ArtifactRef
    page_manifests: list[ArtifactRef]
    capabilities: ReportCapabilities


class VersionedReport(
    RootModel[
        Annotated[DraftResponse | WorkspaceReportResponse, Field(discriminator="contract_version")]
    ]
):
    pass


class WorkspaceAccess(Strict):
    workspace_id: UUID
    principal_id: UUID
    policy_fingerprint: Hash
    allowed_store_ids: Stores


class WorkspaceCalculator(Protocol):
    def apply(
        self, request: WorkspaceApplyRequest, access: WorkspaceAccess
    ) -> WorkspaceApplyResponse: ...


class WorkspaceResultReader(Protocol):
    def verify(self, binding: CardResultBinding, access: WorkspaceAccess) -> None: ...


class SavedViewRepository(Protocol):
    def get(self, workspace_id: UUID, owner: UUID, saved_view_id: UUID) -> SavedViewV1: ...
    def save(
        self,
        workspace_id: UUID,
        owner: UUID,
        report_id: UUID,
        saved_view_id: UUID,
        request: SaveViewRequest,
        value: SavedViewV1,
    ) -> SavedViewV1: ...


def adapt_legacy_definition(
    saved: DraftResponse, initial_calendar: CalendarRef
) -> ConfiguredReportV2:
    """Project editor configuration only; original strict v1 result/snapshot stays v1.

    Caller resolves the immutable January calendar and current access. No compute,
    persistence or fabricated v2 result occurs here. First edit still needs v2 Apply.
    """
    workset_id, ids = legacy_instance_ids(saved.report_id)
    metrics = [
        MetricRef.model_validate({k: m[k] for k in ("metric_id", "version_id", "content_hash")})
        for m in saved.result["metrics"]
    ]
    if {m.metric_id for m in metrics} != set(ids) or len(metrics) != 3:
        raise ValueError("INCOMPLETE_LEGACY_METRICS")
    parameters = saved.result["parameters"]
    store = parameters["store_id"]
    return ConfiguredReportV2(
        schema_version="configured-report/v2",
        report_id=saved.report_id,
        creator_principal_id=saved.author_principal_id,
        title=saved.title,
        semantic_dataset_version_id=saved.result["semantic_dataset_version_id"],
        common_context=QueryContext(
            starts_on=parameters["period"]["starts_on"],
            ends_on=parameters["period"]["ends_on"],
            store_ids=None if store is None else [store],
        ),
        grain="day",
        calendar_ref=initial_calendar,
        calendar_basis="calendar",
        worksets=[
            Workset(
                workset_id=workset_id,
                name=LocalizedName(ru="Показатели", en="Metrics"),
                visibility="personal",
                owner_principal_id=saved.author_principal_id,
                cards=[
                    Card(card_id=ids[m.metric_id], metric_ref=m, local_store_ids=None)
                    for m in metrics
                ],
            )
        ],
        default_workset_id=workset_id,
        selection=SingleSelection(
            mode="single",
            card_id=ids["net_revenue"],
            temporal="previous_year_same_dates" if saved.result.get("comparison") else "none",
            display="series",
        ),
        brand_profile=saved.references.brand_profile.reference,
        company_pack=saved.references.company_pack.reference,
        base_snapshot_ref=BaseSnapshotRef(
            version_id=saved.version_id,
            snapshot_id=saved.snapshot_id,
            manifest=ArtifactRef.model_validate(
                {k: saved.manifest[k] for k in ("artifact_id", "content_hash")}
            ),
        ),
    )
