"""Analytical-authoring/v1 contracts; existing v1/v2 remain unchanged.

These DTOs validate structure, not actor authorization or provider readiness.
Analytical input fingerprints are NOT policy-aware result/cache identities.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict, deque
from datetime import datetime
from typing import Annotated, Literal, Any, cast
from uuid import UUID, uuid4

from pydantic import Field, field_validator, model_validator, model_serializer, SerializerFunctionWrapHandler

from packages.contracts.analytics.workspace import (
    MetricRef, WorkspaceRunRequest, WorkspaceScopePreflight, CardComparisonV1, WorkspaceResultV2, CardResultBinding, ArtifactRef,
)
from packages.contracts.presentation.workspace import ReportActor
from packages.contracts.presentation import Reference
from packages.contracts.semantic import Strict
from packages.contracts.presentation.scopes import ComposerScopes, ScopeOrigin

from packages.contracts.presentation.visual import BlockVisual, ChartKind

Order = Annotated[int, Field(strict=True, ge=0)]
Text = Annotated[str, Field(min_length=1, max_length=200, pattern=r"\S")]


class ComposerOrigin(Strict):
    report_id: UUID
    version_id: UUID
    snapshot_id: UUID


class ComposerNodeOrigin(Strict):
    node_id: UUID
    snapshot_id: UUID | None = None


class ComposerNodeState(Strict):
    hidden: bool = Field(default=False, strict=True)
    locked: bool = Field(default=False, strict=True)
    copied_from: ComposerNodeOrigin | None = None

    @model_serializer(mode="wrap")
    def preserve_omitted_metadata(self, handler: SerializerFunctionWrapHandler):
        # Added defaults must not change old immutable snapshot payloads or replay hashes.
        value: dict[str, Any] = handler(self)
        for field in ("hidden", "locked", "copied_from"):
            if field not in self.model_fields_set:
                value.pop(field, None)
        return value


class ComposerChapter(ComposerNodeState):
    chapter_id: UUID
    order: Order
    title: Text


class ComposerPage(ComposerNodeState):
    page_id: UUID
    chapter_id: UUID | None = None
    order: Order
    title: Text
    layout: Literal["flow", "dashboard_grid", "narrative"] = "flow"


class ComposerSection(ComposerNodeState):
    section_id: UUID
    page_id: UUID
    parent_section_id: UUID | None = None
    order: Order
    title: Text


class GridPlacement(Strict):
    """Column coordinates are checked against the document grid version."""

    column: Annotated[int, Field(strict=True, ge=0, lt=24)] = 0
    span: Annotated[int, Field(strict=True, ge=1, le=24)] = 12
    row: Order = 0
    row_span: Annotated[int, Field(strict=True, ge=1)] = 1

    @model_validator(mode="after")
    def contained(self) -> GridPlacement:
        if self.column + self.span > 24:
            raise ValueError("COMPOSER_GRID_OVERFLOW")
        return self


class RetailAnalysisInput(Strict):
    """Typed reference to the existing bounded Analytics provider, not a new evaluator."""

    definition_id: UUID
    provider: Literal["metric-workspace/v2"] = "metric-workspace/v2"
    query: WorkspaceRunRequest

    @model_validator(mode="after")
    def distinct_metrics(self) -> RetailAnalysisInput:
        if self.query.scope is not None:
            raise ValueError("COMPOSER_DERIVED_SCOPE_NOT_AUTHORABLE")
        metrics = [m.metric_id for m in self.query.metric_refs]
        if len(metrics) != len(set(metrics)):
            raise ValueError("COMPOSER_DUPLICATE_METRIC")
        return self


class DataBinding(Strict):
    definition_id: UUID
    metric_ref: MetricRef


class BlockPresentation(Strict):
    chart_type: ChartKind = "line"
    description: str = Field(default="", max_length=4000)
    show_title: bool = True
    visual: BlockVisual | None = None

    @model_serializer(mode="wrap")
    def preserve_old_presentation(self, handler: SerializerFunctionWrapHandler):
        value = handler(self)
        for field in ("chart_type", "description", "show_title", "visual"):
            if field not in self.model_fields_set:
                value.pop(field, None)
        return value

    density: Literal["compact", "comfortable", "spacious"] = "comfortable"
    title: str = Field(max_length=200)
    legend: bool = Field(default=True, strict=True)


class StoreControl(Strict):
    semantic_dataset_version_id: UUID
    target_block_ids: list[UUID]
    store_ids: list[str] | None = None

    @model_validator(mode="after")
    def unique_targets(self) -> StoreControl:
        if len(set(self.target_block_ids)) != len(self.target_block_ids):
            raise ValueError("COMPOSER_DUPLICATE_FILTER_TARGET")
        if self.store_ids is not None and len(set(self.store_ids)) != len(self.store_ids):
            raise ValueError("COMPOSER_DUPLICATE_STORE")
        return self


class ComposerBlock(ComposerNodeState):
    block_id: UUID
    section_id: UUID
    order: Order
    block_type: Literal["chart", "table", "metric", "text", "filter"]
    source: DataBinding | None = None
    text: str = Field(default="", max_length=20000)
    text_style: Literal["plain", "callout"] = "plain"
    control: StoreControl | None = None

    @model_validator(mode="after")
    def content_kind(self) -> ComposerBlock:
        if (self.block_type in ("chart", "table", "metric")) != (self.source is not None):
            raise ValueError("COMPOSER_INVALID_BLOCK_SOURCE")
        if (self.block_type == "filter") != (self.control is not None):
            raise ValueError("COMPOSER_INVALID_CONTROL")
        if self.block_type != "text" and (self.text or self.text_style != "plain"):
            raise ValueError("COMPOSER_INVALID_TEXT")
        return self

    @model_serializer(mode="wrap")
    def preserve_old_block(self, handler: SerializerFunctionWrapHandler):
        value = handler(self)
        for field in ("source", "text", "text_style", "control", "hidden", "locked", "copied_from"):
            if field not in self.model_fields_set:
                value.pop(field, None)
        return value

    presentation: BlockPresentation
    placement: GridPlacement | None = None


class ComposerPairSelection(Strict):
    left_block_id: UUID
    right_block_id: UUID

    @model_validator(mode="after")
    def distinct(self) -> ComposerPairSelection:
        if self.left_block_id == self.right_block_id:
            raise ValueError("PAIR_REQUIRES_DISTINCT_CARDS")
        return self


class ComposerDefinitionV1(Strict):
    grid_columns: Literal[12, 24] = 12
    pair: ComposerPairSelection | None = None
    scopes: ComposerScopes | None = None

    @field_validator("scopes", mode="before")
    @classmethod
    def legacy_scope_default(cls, value: Any) -> Any:
        if isinstance(value, dict) and "schema_version" not in value:
            return {**cast(dict[str, Any], value), "schema_version": "composer-scopes/v1"}
        return cast(Any, value)

    @model_serializer(mode="wrap")
    def preserve_old_scope(self, handler: SerializerFunctionWrapHandler):
        value: dict[str, Any] = handler(self)
        for field in ("scopes", "pair", "grid_columns"):
            if field not in self.model_fields_set:
                value.pop(field, None)
        return value

    schema_version: Literal["analytical-authoring/v1"] = "analytical-authoring/v1"
    document_id: UUID
    creator_principal_id: UUID
    profile: Literal["dashboard", "workbook_report", "narrative_research"]
    title: Text
    origin: ComposerOrigin | None = None
    brand_profile: Reference
    company_pack: Reference
    default_page_id: UUID
    chapters: list[ComposerChapter] = Field(default_factory=lambda: list[ComposerChapter]())
    pages: list[ComposerPage] = Field(min_length=1)
    sections: list[ComposerSection]
    blocks: list[ComposerBlock]
    definitions: list[RetailAnalysisInput]

    @model_validator(mode="after")
    def coherent_graph(self) -> ComposerDefinitionV1:
        ids = (
            [self.document_id]
            + [c.chapter_id for c in self.chapters]
            + [p.page_id for p in self.pages]
            + [s.section_id for s in self.sections]
            + [b.block_id for b in self.blocks]
            + [d.definition_id for d in self.definitions]
        )
        if len(ids) != len(set(ids)):
            raise ValueError("COMPOSER_DUPLICATE_ID")
        chapters = {c.chapter_id: c for c in self.chapters}
        pages = {p.page_id: p for p in self.pages}
        sections = {s.section_id: s for s in self.sections}
        definitions = {d.definition_id: d for d in self.definitions}
        if self.default_page_id not in pages:
            raise ValueError("COMPOSER_UNKNOWN_DEFAULT_PAGE")
        default = pages[self.default_page_id]
        chapter = chapters.get(default.chapter_id) if default.chapter_id else None
        if default.hidden or (chapter is not None and chapter.hidden):
            raise ValueError("COMPOSER_HIDDEN_DEFAULT_PAGE")
        for node, identity in (
            [(n, n.chapter_id) for n in self.chapters]
            + [(n, n.page_id) for n in self.pages]
            + [(n, n.section_id) for n in self.sections]
            + [(n, n.block_id) for n in self.blocks]
        ):
            if node.copied_from is not None and node.copied_from.node_id == identity:
                raise ValueError("COMPOSER_SELF_COPY_ORIGIN")
        orders: set[tuple[str, UUID | None, int]] = set()

        def order(kind: str, parent: UUID | None, value: int) -> None:
            key = (kind, parent, value)
            if key in orders:
                raise ValueError("COMPOSER_DUPLICATE_ORDER")
            orders.add(key)

        for chapter in self.chapters:
            order("chapter", None, chapter.order)
        for page in self.pages:
            if page.chapter_id is not None and page.chapter_id not in chapters:
                raise ValueError("COMPOSER_UNKNOWN_CHAPTER")
            order("page", page.chapter_id, page.order)

        # Topological validation avoids recursive traversal of untrusted nesting.
        children: dict[UUID, list[UUID]] = defaultdict(list)
        roots: deque[UUID] = deque()
        for section in self.sections:
            if section.page_id not in pages:
                raise ValueError("COMPOSER_UNKNOWN_PAGE")
            parent = section.parent_section_id
            if parent is None:
                roots.append(section.section_id)
            elif parent not in sections or sections[parent].page_id != section.page_id:
                raise ValueError("COMPOSER_INVALID_SECTION_PARENT")
            else:
                children[parent].append(section.section_id)
            order("section", parent or section.page_id, section.order)
        visited = 0
        while roots:
            current = roots.popleft()
            visited += 1
            roots.extend(children[current])
        if visited != len(sections):
            raise ValueError("COMPOSER_SECTION_CYCLE")

        used: set[UUID] = set()
        placements: dict[UUID, list[GridPlacement]] = defaultdict(list)
        for block in self.blocks:
            if block.section_id not in sections:
                raise ValueError("COMPOSER_UNKNOWN_SECTION")
            order("block", block.section_id, block.order)
            if block.source is not None:
                source = definitions.get(block.source.definition_id)
                if source is None or block.source.metric_ref not in source.query.metric_refs:
                    raise ValueError("COMPOSER_INVALID_SOURCE_BINDING")
                used.add(source.definition_id)
            if block.control is not None:
                for target_id in block.control.target_block_ids:
                    target = next((b for b in self.blocks if b.block_id == target_id), None)
                    if target is None or target.source is None:
                        raise ValueError("COMPOSER_INVALID_FILTER_TARGET")
                    source = definitions.get(target.source.definition_id)
                    if source is None or source.query.semantic_dataset_version_id != block.control.semantic_dataset_version_id:
                        raise ValueError("COMPOSER_FILTER_DATASET_MISMATCH")
            page = pages[sections[block.section_id].page_id]
            if (page.layout == "dashboard_grid") != (block.placement is not None):
                raise ValueError("COMPOSER_LAYOUT_PLACEMENT_MISMATCH")
            placement = block.placement
            if placement is not None:
                if placement.column + placement.span > self.grid_columns:
                    raise ValueError("COMPOSER_GRID_OVERFLOW")
                for other in placements[block.section_id]:
                    if (
                        placement.column < other.column + other.span
                        and other.column < placement.column + placement.span
                        and placement.row < other.row + other.row_span
                        and other.row < placement.row + placement.row_span
                    ):
                        raise ValueError("COMPOSER_GRID_OVERLAP")
                placements[block.section_id].append(placement)
        if used != set(definitions):
            raise ValueError("COMPOSER_UNUSED_DEFINITION")
        if self.pair is not None and not {self.pair.left_block_id, self.pair.right_block_id} <= {b.block_id for b in self.blocks if b.source is not None}:
            raise ValueError("COMPOSER_UNKNOWN_PAIR_BLOCK")
        return self


def input_fingerprint(value: RetailAnalysisInput) -> str:
    """Grouping hint only: Analytics must still resolve inputs, policy and cache key."""
    payload = value.query.model_dump(mode="json")
    payload["metric_refs"] = sorted(payload["metric_refs"], key=lambda m: m["metric_id"])
    encoded = json.dumps(
        {"provider": value.provider, "query": payload},
        sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False,
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def duplicate_block(
    definition: ComposerDefinitionV1,
    block_id: UUID,
    *,
    section_id: UUID,
    order: int,
    placement: GridPlacement | None = None,
) -> ComposerDefinitionV1:
    """Copy editable inputs with fresh IDs; compatible provider results can still reuse."""
    original = next((b for b in definition.blocks if b.block_id == block_id), None)
    if original is None:
        raise ValueError("COMPOSER_UNKNOWN_BLOCK")
    source = next((d for d in definition.definitions if original.source is not None and d.definition_id == original.source.definition_id), None)
    new_source = source.model_dump(mode="json") if source else None
    if new_source is not None:
        new_source["definition_id"] = str(uuid4())
    new_block = original.model_dump(mode="json")
    new_block.update(
        block_id=str(uuid4()), section_id=str(section_id), order=order,
        copied_from={"node_id": str(block_id), "snapshot_id": None},
        placement=placement.model_dump(mode="json") if placement else None,
    )
    if new_source is not None:
        new_block["source"] = {**new_block["source"], "definition_id": new_source["definition_id"]}
    raw = definition.model_dump(mode="json")
    raw["blocks"].append(new_block)
    if new_source is not None:
        raw["definitions"].append(new_source)
    if definition.scopes is not None:
        for collection in ("filters", "receipt_filters"):
            filters = raw["scopes"].get(collection, [])
            for binding in getattr(definition.scopes, collection, []):
                local = binding.target.kind == "block" and binding.target.id == block_id
                linked = block_id in binding.linked_target_block_ids
                if not local and not linked:
                    continue
                copied = binding.model_dump(mode="json")
                copied.update(binding_id=str(uuid4()), target={"kind": "block", "id": new_block["block_id"]}, linked_target_block_ids=[])
                if not local:
                    copied.update(combine_mode="intersect", replaces=[])
                copied["order"] = 1 + max((f["order"] for key in ("filters", "receipt_filters") for f in raw["scopes"].get(key, []) if f["target"]["id"] == new_block["block_id"]), default=-1)
                filters.append(copied)
        for binding in definition.scopes.contexts:
            if binding.target.kind == "block" and binding.target.id == block_id:
                copied = binding.model_dump(mode="json")
                copied.update(binding_id=str(uuid4()), target={"kind": "block", "id": new_block["block_id"]})
                raw["scopes"]["contexts"].append(copied)
    return ComposerDefinitionV1.model_validate(raw)


class ComposerResultRef(Strict):
    block_id: UUID
    result_id: UUID


class ComposerComparisonState(Strict):
    comparison: CardComparisonV1 | None = None

    @model_serializer(mode="wrap")
    def preserve_old_comparison(self, handler: SerializerFunctionWrapHandler):
        value: dict[str, Any] = handler(self)
        if "comparison" not in self.model_fields_set:
            value.pop("comparison", None)
        return value


class ComposerCompareRequest(Strict):
    contract_version: Literal["analytical-authoring/v1"]
    definition: ComposerDefinitionV1
    results: list[ComposerResultRef]

    @model_validator(mode="after")
    def selected(self) -> ComposerCompareRequest:
        if self.definition.pair is None:
            raise ValueError("COMPOSER_PAIR_REQUIRED")
        ids = [r.block_id for r in self.results]
        if len(ids) != len(set(ids)):
            raise ValueError("COMPOSER_DUPLICATE_RESULT")
        return self


class ComposerSaveRequest(ComposerComparisonState):
    contract_version: Literal["analytical-authoring/v1"]
    definition: ComposerDefinitionV1
    expected_revision: Annotated[int, Field(strict=True, ge=0)]
    idempotency_key: UUID
    results: list[ComposerResultRef] = Field(default_factory=lambda: list[ComposerResultRef]())


class ComposerCapabilities(Strict):
    schema_version: Literal["composer-capabilities/v1"] = "composer-capabilities/v1"
    definition_edit: bool = Field(default=False, strict=True)
    block_apply: bool = Field(default=False, strict=True)
    profiles: list[Literal["dashboard", "workbook_report", "narrative_research"]] = ["dashboard", "workbook_report", "narrative_research"]
    providers: list[Literal["metric-workspace/v2"]] = ["metric-workspace/v2"]
    blocks: list[Literal["chart", "table", "metric", "text", "filter"]] = ["chart", "table", "metric", "text", "filter"]
    channels: list[Literal["interactive"]] = ["interactive"]


class ComposerApplyRequest(Strict):
    contract_version: Literal["analytical-authoring/v1"]
    definition: ComposerDefinitionV1
    block_id: UUID


class ComposerValidationResponse(Strict):
    valid: Literal[True] = True


class ComposerPreflightResponse(Strict):
    block_id: UUID
    effective_query: WorkspaceRunRequest
    origins: list[ScopeOrigin]
    provider: WorkspaceScopePreflight


class ComposerApplyResponse(Strict):
    contract_version: Literal["composer-block-result/v1"] = "composer-block-result/v1"
    block_id: UUID
    input_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    binding: CardResultBinding
    result: WorkspaceResultV2


class ComposerReportResponse(ComposerComparisonState):
    contract_version: Literal["composed-report/v1"] = "composed-report/v1"
    report_id: UUID
    revision: Annotated[int, Field(strict=True, ge=1)]
    version_id: UUID
    snapshot_id: UUID
    author_principal_id: UUID
    saved_at: datetime
    definition: ComposerDefinitionV1
    results: list[ComposerResultRef]
    manifest: ArtifactRef

    @model_validator(mode="after")
    def bound(self) -> ComposerReportResponse:
        if (self.report_id != self.definition.document_id
                or self.author_principal_id != self.definition.creator_principal_id):
            raise ValueError("INVALID_DEFINITION_BINDING")
        ids = [r.block_id for r in self.results]
        if len(set(ids)) != len(ids) or not set(ids) <= {b.block_id for b in self.definition.blocks}:
            raise ValueError("RESULT_BINDING_MISMATCH")
        return self


class ComposerEditorResponse(Strict):
    report: ComposerReportResponse
    actor: ReportActor
    capabilities: ComposerCapabilities = Field(default_factory=ComposerCapabilities)


class ComposerPrepareResponse(Strict):
    definition: ComposerDefinitionV1
    actor: ReportActor
    capabilities: ComposerCapabilities = Field(default_factory=ComposerCapabilities)
