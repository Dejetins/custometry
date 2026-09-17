"""Presentation-owned draft contracts and owner integration ports."""

from __future__ import annotations

from typing import Any, Literal, Protocol
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

VERSION = "draft-report/v1"


class PresentationFailure(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Reference(Strict):
    id: UUID
    content_hash: str = Field(pattern=r"^[0-9a-f]{64}$")


class PrepareRequest(Strict):
    contract_version: Literal["draft-report/v1"]
    result_id: UUID


class SaveRequest(PrepareRequest):
    title: str = Field(min_length=1, max_length=200, pattern=r"\S")
    expected_revision: int = Field(ge=0)
    idempotency_key: UUID
    chart_spec: Reference
    brand_profile: Reference
    company_pack: Reference


class LineChartSpecV1(Strict):
    chart_spec_id: UUID
    workspace_id: UUID
    schema_version: Literal["1.0.0"]
    chart_type: Literal["line"]
    title_key: str
    title_override: None
    description_key: None
    source_binding: dict[str, Any]
    chart_data: dict[str, Any]
    dimensions: list[dict[str, Any]]
    measures: list[dict[str, Any]]
    axes: list[dict[str, Any]]
    series: list[dict[str, Any]]
    annotations: list[dict[str, Any]]
    range_timeline: None
    interaction: dict[str, Any]
    visual_semantics: dict[str, Any]
    accessibility: dict[str, Any]
    export_policy: dict[str, Any]
    access_policy: dict[str, Any]
    created_at: str


class SystemBrandProfileV1(Strict):
    schema_version: Literal["system-brand/v1"]
    brand_profile_version_id: UUID
    name: str
    token_version: str
    source: dict[str, str]
    font_family: Literal["Inter"]
    themes: list[Literal["abyss", "graphite", "frost", "paper"]]
    tokens: list[dict[str, Any]]
    remote_assets: list[str]


class SystemCompanyPackV1(Strict):
    schema_version: Literal["system-company-pack/v1"]
    company_pack_version_id: UUID
    name: str
    brand_profile: Reference
    metric_versions: list[dict[str, Any]]
    methodology_packs: list[dict[str, Any]]
    localization_catalogs: list[Literal["en", "ru"]]


class ChartSpecObject(Strict):
    reference: Reference
    kind: Literal["chart_spec"]
    payload: LineChartSpecV1


class BrandProfileObject(Strict):
    reference: Reference
    kind: Literal["brand_profile"]
    payload: SystemBrandProfileV1


class CompanyPackObject(Strict):
    reference: Reference
    kind: Literal["company_pack"]
    payload: SystemCompanyPackV1


class PreparedResponse(Strict):
    contract_version: Literal["draft-report/v1"]
    chart_spec: ChartSpecObject
    brand_profile: BrandProfileObject
    company_pack: CompanyPackObject


class Page(Strict):
    page_id: UUID
    chapter_id: None = None
    order: int
    title: dict[str, str]
    visibility: Literal["visible"]
    layout_mode: Literal["flow"]


class Section(Strict):
    section_id: UUID
    page_id: UUID
    parent_section_id: None = None
    order: int
    title: None = None


class Block(Strict):
    block_id: UUID
    section_id: UUID
    order: int
    block_type: Literal["metric_group", "chart", "table", "result_trust"]
    source_binding: dict[str, Any]
    content_binding: None = None
    presentation: dict[str, Any]


class AnalyticalDocumentCompositionV1(Strict):
    analytical_document_version_id: UUID
    analytical_document_id: UUID
    workspace_id: UUID
    profile: Literal["workbook_report"]
    composition_schema_version: Literal[1]
    source_owner_ref: dict[str, str]
    navigation_mode: Literal["tabs"]
    default_page_id: UUID
    chapters: list[dict[str, Any]]
    pages: list[Page]
    sections: list[Section]
    blocks: list[Block]
    brand_profile_version_id: UUID
    access_policy_id: UUID
    filter_scope_bindings: list[dict[str, Any]]


class DraftResponse(Strict):
    contract_version: Literal["draft-report/v1"]
    lifecycle: Literal["owned_draft_preview"]
    report_id: UUID
    revision: int
    title: str
    version_id: UUID
    snapshot_id: UUID
    author_principal_id: UUID
    saved_at: str
    composition: AnalyticalDocumentCompositionV1
    snapshot: dict[str, Any]
    page_snapshot: dict[str, Any]
    result: dict[str, Any]
    references: PreparedResponse
    manifest: dict[str, Any]


class ReportSummary(Strict):
    report_id: UUID
    revision: int
    title: str
    version_id: UUID
    snapshot_id: UUID
    saved_at: str
    lifecycle: Literal["owned_draft_preview"]


class ReportList(Strict):
    reports: list[ReportSummary]
    visible_count: int


class ResultReader(Protocol):
    def get_sales_report(
        self,
        *,
        workspace_id: UUID,
        principal_id: UUID,
        permissions: frozenset[str],
        result_id: UUID,
    ) -> dict[str, Any]: ...


class SnapshotArtifacts(Protocol):
    def commit(
        self,
        *,
        workspace_id: UUID,
        artifact_id: UUID,
        payload: dict[str, Any],
        parents: list[dict[str, Any]],
    ) -> dict[str, Any]: ...
    def verify(
        self, *, workspace_id: UUID, reference: dict[str, Any], payload: dict[str, Any]
    ) -> None: ...


class ReportRepository(Protocol):
    def put_reference(
        self, workspace_id: UUID, owner: UUID, value: dict[str, Any]
    ) -> dict[str, Any]: ...
    def get_reference(
        self, workspace_id: UUID, owner: UUID, reference: dict[str, Any], kind: str
    ) -> dict[str, Any]: ...
    def latest(
        self, workspace_id: UUID, owner: UUID, report_id: UUID, snapshot_id: UUID | None = None
    ) -> dict[str, Any]: ...
    def candidates(self, workspace_id: UUID, owner: UUID) -> list[UUID]: ...
    def save(
        self,
        workspace_id: UUID,
        owner: UUID,
        report_id: UUID,
        request_hash: str,
        request: SaveRequest,
        payload: dict[str, Any],
    ) -> dict[str, Any]: ...
