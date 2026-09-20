"""Personal configured reports, exact base reading and atomic companion Saved Views."""

from __future__ import annotations
from datetime import UTC, datetime
from typing import Any, cast, Literal
from uuid import UUID, uuid4, uuid5
from packages.contracts.identity.access import ResourceAccessPort
from packages.contracts.analytics.workspace import (
    WorkspaceCardRequest,
    WorkspaceRunRequest,
    WorkspaceResultV2,
    QueryContext,
    CardResultBinding,
    ResultRef,
    NumberFormat,
)
from packages.contracts.presentation import (
    DraftResponse,
    PresentationFailure,
    SnapshotArtifacts,
    Page,
    Block,
)
from packages.contracts.presentation.workspace import (
    ConfiguredReportV2,
    CreatorApplyRequest,
    WorkspaceApplyRequest,
    WorkspaceApplyResponse,
    WorkspaceSaveRequest,
    SaveViewRequest,
    SavedViewV1,
    ReaderViewOverride,
    ViewQueryContext,
    ViewDisplay,
    SingleSelection,
    ChartSeriesRef,
    PairSelection,
    WorkspaceChartSpecV2,
    AnalyticalDocumentCompositionV2,
    WorkspaceSection,
    WorkspaceFilterBinding,
    WorkspaceReportResponse,
    WorkspaceEditorResponse,
    ReportCapabilities,
    VersionedReport,
    adapt_legacy_definition,
    creator_saved_view_id,
    selection_ids,
)
from packages.contracts.presentation.workspace_ports import WorkspaceResults
from packages.contracts.semantic import CalendarRef, BusinessCalendarProfile, WorkspaceCalendarPort
from packages.presentation.domain.reports import digest, versioned


def artifact(value: dict[str, Any]) -> dict[str, Any]:
    return {k: value[k] for k in ("artifact_id", "content_hash")}


def page_payload(composition: dict[str, Any]) -> dict[str, Any]:
    return {"schema_version": "workspace-page/v2", "composition": composition}


class WorkspaceReportService:
    def __init__(
        self,
        repository: Any,
        results: WorkspaceResults,
        access: ResourceAccessPort,
        artifacts: SnapshotArtifacts,
        calendars: WorkspaceCalendarPort,
    ):
        self.repository, self.results, self.access = repository, results, access
        self.artifacts, self.calendars = artifacts, calendars

    def guard(
        self, workspace: UUID, actor: UUID, report: UUID, *, write: bool = False, run: bool = False
    ) -> tuple[dict[str, Any], str]:
        metadata = self.repository.metadata(workspace, report)
        actions = ["view_snapshot"] + (["edit"] if write else []) + (["run"] if run else [])
        decisions = [
            self.access.resolve_resource(
                workspace_id=workspace,
                principal_id=actor,
                resource_type="report",
                resource_id=report,
                action=action,
                legacy_creator=metadata["creator"],
            )
            for action in actions
        ]
        required: set[str] = (
            {"report.read", "analysis.read"}
            | ({"report.manage"} if write else set[str]())
            | ({"analysis.run"} if run else set[str]())
        )
        if (write and metadata["creator"] != actor) or any(
            not d.allowed or not required <= d.permissions for d in decisions
        ):
            raise PresentationFailure("FORBIDDEN")
        return metadata, digest([d.policy_hash for d in decisions])

    def _scope(self, workspace: UUID, actor: UUID, report: UUID, stores: set[str]) -> None:
        decision = self.access.resolve_resource(
            workspace_id=workspace,
            principal_id=actor,
            resource_type="report",
            resource_id=report,
            action="view_snapshot",
            legacy_creator=self.repository.metadata(workspace, report)["creator"],
        )
        if not decision.allowed or (
            decision.store_ids is not None and not stores <= set(decision.store_ids)
        ):
            raise PresentationFailure("FORBIDDEN")

    def _legacy(self, workspace: UUID, actor: UUID, saved: dict[str, Any]) -> dict[str, Any]:
        parsed = DraftResponse.model_validate(saved)
        access = self.results.legacy(workspace, actor, parsed.author_principal_id, saved["result"])
        store = saved["result"]["parameters"]["store_id"]
        self._scope(
            workspace,
            actor,
            parsed.report_id,
            set(access.allowed_store_ids) if store is None else {store},
        )
        for name in ("chart_spec", "brand_profile", "company_pack"):
            r = saved["references"][name]
            if (
                self.repository.get_reference(
                    workspace, parsed.author_principal_id, r["reference"], name
                )
                != r
            ):
                raise PresentationFailure("INVALID_REFERENCE")
        self.artifacts.verify(
            workspace_id=workspace,
            reference=saved["manifest"],
            payload={k: v for k, v in saved.items() if k != "manifest"},
        )
        self.artifacts.verify(
            workspace_id=workspace,
            reference=saved["snapshot"]["page_snapshot_refs"][0]["manifest"],
            payload=saved["page_snapshot"],
        )
        return saved

    def _definition(
        self, workspace: UUID, actor: UUID, saved: dict[str, Any]
    ) -> ConfiguredReportV2:
        if saved["contract_version"] == "configured-report/v2":
            definition = ConfiguredReportV2.model_validate(saved["composition"]["definition"])
            base = self.repository.read(
                workspace, definition.report_id, definition.base_snapshot_ref.snapshot_id
            )
            if actor == UUID(base["author_principal_id"]):
                self.results.authorize_base(
                    workspace, actor, UUID(base["author_principal_id"]), base["result"]
                )
            return definition
        if actor == UUID(saved["author_principal_id"]):
            self.results.authorize_base(
                workspace, actor, UUID(saved["author_principal_id"]), saved["result"]
            )
        ref = CalendarRef(
            version_id=uuid5(workspace, "business-calendar/v1/initial-january"),
            content_hash=digest(BusinessCalendarProfile().model_dump(mode="json")),
        )
        # Provision only the original January version; current default is never substituted.
        access = self.results.resolve(
            workspace, actor, UUID(saved["result"]["semantic_dataset_version_id"])
        )
        self.calendars.get_default(workspace, access)
        self.calendars.get_version(ref, access)
        return adapt_legacy_definition(DraftResponse.model_validate(saved), ref)

    def visible(
        self,
        workspace: UUID,
        actor: UUID,
        report: UUID,
        snapshot: UUID | None = None,
        version: UUID | None = None,
    ) -> dict[str, Any]:
        meta, _ = self.guard(workspace, actor, report)
        saved = self.repository.read(workspace, report, snapshot, version)
        if saved["contract_version"] == "configured-report/v2" and meta["creator"] != actor:
            if snapshot is not None or version is not None:
                raise PresentationFailure("NOT_FOUND")
            base = saved["composition"]["definition"]["base_snapshot_ref"]
            saved = self.repository.read(workspace, report, UUID(base["snapshot_id"]))
            if (
                saved["version_id"] != base["version_id"]
                or artifact(saved["manifest"]) != base["manifest"]
            ):
                raise PresentationFailure("ARTIFACT_CORRUPT")
        self._verify(workspace, actor, saved)
        return saved

    def _verify(self, workspace: UUID, actor: UUID, saved: dict[str, Any]) -> None:
        report = UUID(saved["report_id"])
        self.guard(workspace, actor, report)
        if saved["contract_version"] == "draft-report/v1":
            self._legacy(workspace, actor, saved)
        else:
            value = WorkspaceReportResponse.model_validate(saved)
            definition = self._definition(workspace, actor, saved)
            if definition.creator_principal_id != actor:
                raise PresentationFailure("NOT_FOUND")
            self._materialize(
                workspace,
                actor,
                definition,
                [b.result.result_id for b in value.composition.bindings_by_card],
                expected_bindings=value.composition.bindings_by_card,
                make_charts=False,
            )
            for comparison in value.composition.comparisons:
                self.results.verify_comparison(
                    workspace, actor, definition.semantic_dataset_version_id, comparison
                )
            for ref in value.composition.chart_specs:
                self.repository.get_reference(
                    workspace, actor, ref.model_dump(mode="json"), "chart_spec"
                )
            if len(value.composition.chart_specs) != len(value.composition.chart_payloads):
                raise PresentationFailure("ARTIFACT_CORRUPT")
            for ref, chart in zip(
                value.composition.chart_specs, value.composition.chart_payloads, strict=True
            ):
                stored_chart = self.repository.get_reference(
                    workspace, actor, ref.model_dump(mode="json"), "chart_spec"
                )
                if stored_chart["payload"] != chart.model_dump(mode="json"):
                    raise PresentationFailure("ARTIFACT_CORRUPT")
            companion = self.repository.view(
                workspace, actor, creator_saved_view_id(report, actor), value.saved_view.id
            )
            if (
                digest(companion.model_dump(mode="json")) != value.saved_view.content_hash
                or companion.document_version_id != value.version_id
                or companion.result_scope != value.composition.bindings_by_card
            ):
                raise PresentationFailure("ARTIFACT_CORRUPT")
            base = self.repository.read(workspace, report, definition.base_snapshot_ref.snapshot_id)
            if base["version_id"] != str(definition.base_snapshot_ref.version_id) or artifact(
                base["manifest"]
            ) != definition.base_snapshot_ref.manifest.model_dump(mode="json"):
                raise PresentationFailure("ARTIFACT_CORRUPT")
            self._legacy(workspace, actor, base)
            self.artifacts.verify(
                workspace_id=workspace,
                reference=saved["manifest"],
                payload={k: v for k, v in saved.items() if k != "manifest"},
            )
            if len(value.page_manifests) != 1:
                raise PresentationFailure("ARTIFACT_CORRUPT")
            self.artifacts.verify(
                workspace_id=workspace,
                reference=saved["page_manifests"][0],
                payload=page_payload(saved["composition"]),
            )
        self.guard(workspace, actor, report)

    def get(
        self, workspace: UUID, actor: UUID, report: UUID, snapshot: UUID | None = None
    ) -> WorkspaceEditorResponse:
        saved = self.visible(workspace, actor, report, snapshot)
        definition = self._definition(workspace, actor, saved)
        creator = self.repository.metadata(workspace, report)["creator"] == actor
        caps = self.capabilities(workspace, actor, report)
        try:
            revision = self.repository.view(
                workspace, actor, creator_saved_view_id(report, actor)
            ).revision
        except PresentationFailure as e:
            if e.code != "NOT_FOUND":
                raise
            revision = 0
        return WorkspaceEditorResponse(
            report=VersionedReport.model_validate(saved),
            definition=definition if creator else None,
            base_definition=None if creator else definition,
            capabilities=caps,
            saved_view_revision=revision,
        )

    def capabilities(self, workspace: UUID, actor: UUID, report: UUID) -> ReportCapabilities:
        def permitted(write: bool = False, run: bool = False) -> bool:
            try:
                self.guard(workspace, actor, report, write=write, run=run)
            except PresentationFailure:
                return False
            return True

        return ReportCapabilities(
            definition_edit=permitted(write=True),
            view_apply=permitted(run=True),
            saved_view_save=permitted(),
            exact_preview=permitted(),
        )

    def _candidate(
        self,
        workspace: UUID,
        actor: UUID,
        report: UUID,
        definition: ConfiguredReportV2,
        *,
        check_instances: bool = True,
    ) -> dict[str, Any]:
        meta, _ = self.guard(workspace, actor, report, write=True)
        current = self.repository.read(workspace, report)
        old = self._definition(workspace, actor, current)
        if (
            definition.report_id != report
            or definition.creator_principal_id != meta["creator"]
            or definition.semantic_dataset_version_id != old.semantic_dataset_version_id
            or definition.base_snapshot_ref != old.base_snapshot_ref
            or definition.brand_profile != old.brand_profile
            or definition.company_pack != old.company_pack
        ):
            raise PresentationFailure("INVALID_DEFINITION_BINDING")
        ids = {w.workset_id for w in definition.worksets} | {
            c.card_id for w in definition.worksets for c in w.cards
        }
        if check_instances and ids & self.repository.retired_ids(workspace, report):
            raise PresentationFailure("RETIRED_INSTANCE_ID")
        return current

    @staticmethod
    def _view_definition(
        definition: ConfiguredReportV2, override: ReaderViewOverride
    ) -> ConfiguredReportV2:
        raw = definition.model_dump(mode="json")
        display = override.display
        worksets = {w.workset_id: w for w in definition.worksets}
        if display.active_workset_id is None:
            if worksets:
                raise PresentationFailure("INVALID_VIEW_SCOPE")
            allowed: set[UUID] = set()
        elif display.active_workset_id not in worksets:
            raise PresentationFailure("INVALID_VIEW_SCOPE")
        else:
            allowed = {c.card_id for c in worksets[display.active_workset_id].cards}
        if (
            not (
                set(display.card_order)
                | set(display.hidden_card_ids)
                | selection_ids(display.selection)
            )
            <= allowed
        ):
            raise PresentationFailure("INVALID_VIEW_SCOPE")
        raw["default_workset_id"] = (
            str(display.active_workset_id) if display.active_workset_id else None
        )
        raw["selection"] = display.selection.model_dump(mode="json") if display.selection else None
        q = override.query_context.model_dump(mode="json")
        raw["grain"] = q.pop("grain")
        raw["common_context"] = q
        return ConfiguredReportV2.model_validate(raw)

    def _cards(self, definition: ConfiguredReportV2) -> list[WorkspaceCardRequest]:
        cards = [c for w in definition.worksets for c in w.cards]
        refs = list({c.metric_ref.metric_id: c.metric_ref for c in cards}.values())
        alignment = (
            definition.selection.temporal
            if isinstance(definition.selection, SingleSelection)
            else "none"
        )
        config_hash = digest(definition.model_dump(mode="json"))
        return [
            WorkspaceCardRequest(
                card_id=c.card_id,
                configuration_hash=config_hash,
                metric_ref=c.metric_ref,
                query=WorkspaceRunRequest(
                    semantic_dataset_version_id=definition.semantic_dataset_version_id,
                    common=definition.common_context,
                    local_store_ids=c.local_store_ids,
                    grain=definition.grain,
                    calendar_ref=definition.calendar_ref,
                    calendar_basis=definition.calendar_basis,
                    alignment=alignment,
                    metric_refs=refs,
                ),
            )
            for c in cards
        ]

    def _materialize(
        self,
        workspace: UUID,
        actor: UUID,
        definition: ConfiguredReportV2,
        result_ids: list[UUID] | None = None,
        *,
        expected_bindings: list[CardResultBinding] | None = None,
        make_charts: bool = True,
    ) -> WorkspaceApplyResponse:
        a = self.results.resolve(
            workspace, actor, definition.semantic_dataset_version_id, result_ids is None
        )
        self.calendars.get_version(definition.calendar_ref, a)
        cards = self._cards(definition)
        report_access = self.access.resolve_resource(
            workspace_id=workspace,
            principal_id=actor,
            resource_type="report",
            resource_id=definition.report_id,
            action="view_snapshot",
            legacy_creator=definition.creator_principal_id,
        )
        if not report_access.allowed:
            raise PresentationFailure("FORBIDDEN")
        if report_access.store_ids is not None:
            allowed = set(report_access.store_ids)
            for card in cards:
                for explicit in (card.query.common.store_ids, card.query.local_store_ids):
                    if explicit is not None and not set(explicit) <= allowed:
                        raise PresentationFailure("FORBIDDEN")
                if card.query.common.store_ids is None:
                    card.query.common = QueryContext.model_validate(
                        {**card.query.common.model_dump(), "store_ids": sorted(allowed)}
                    )
        bindings: list[CardResultBinding]
        if result_ids is None:
            batch = self.results.apply(workspace, actor, cards)
            bindings, results = batch.bindings, {r.result_id: r for r in batch.results}
        else:
            if len(result_ids) != len(cards):
                raise PresentationFailure("INCOMPLETE_CARD_BINDINGS")
            bindings, results = [], {}
            verified_queries: dict[tuple[UUID, str], WorkspaceResultV2] = {}
            for card, rid in zip(cards, result_ids, strict=True):
                key = (rid, digest(card.query.model_dump(mode="json")))
                if key not in verified_queries:
                    verified_queries[key] = self.results.verify(workspace, actor, card.query, rid)
                result = verified_queries[key]
                results[rid] = result
                bindings.append(
                    CardResultBinding(
                        card_id=card.card_id,
                        metric_ref=card.metric_ref,
                        result=ResultRef(
                            result_id=rid,
                            schema_version=result.schema_version,
                            manifest=result.manifest,
                        ),
                        effective_context_hash=digest(
                            result.effective_context.model_dump(mode="json")
                        ),
                        configuration_hash=card.configuration_hash,
                        bucket_projection=card.metric_ref.metric_id,
                        unit=cast(
                            Literal["EUR", "receipt", "EUR/receipt"],
                            {
                                "net_revenue": "EUR",
                                "receipt_count": "receipt",
                                "average_receipt": "EUR/receipt",
                            }[card.metric_ref.metric_id],
                        ),
                        format=NumberFormat(
                            decimal_places=0 if card.metric_ref.metric_id == "receipt_count" else 2
                        ),
                        readiness=result.trust.status,
                    )
                )
        for result in results.values():
            self._scope(
                workspace, actor, definition.report_id, set(result.effective_context.store_ids)
            )
        if expected_bindings is not None and bindings != expected_bindings:
            raise PresentationFailure("RESULT_BINDING_MISMATCH")
        comparison, charts = None, []
        chart_payloads: list[WorkspaceChartSpecV2] = []
        selected = definition.selection
        by_card = {b.card_id: b for b in bindings}
        if selected and make_charts:
            left = by_card[
                selected.card_id if isinstance(selected, SingleSelection) else selected.left_card_id
            ]
            right = by_card[selected.right_card_id] if isinstance(selected, PairSelection) else None
            if (
                right is not None
                or isinstance(selected, SingleSelection)
                and selected.temporal != "none"
            ):
                comparison = self.results.compare(
                    workspace, actor, definition.semantic_dataset_version_id, left, right
                )
            ref = comparison.manifest if comparison else left.result.manifest
            series: list[dict[str, Any]] = []
            delta = isinstance(selected, SingleSelection) and selected.display == "delta_trend"
            for side, binding in [("left", left)] + ([("right", right)] if right else []):
                series.append(
                    dict(
                        card_id=binding.card_id,
                        artifact=ref,
                        field="relative_delta_percent"
                        if delta
                        else side
                        if comparison
                        else binding.bucket_projection,
                        axis="right"
                        if right and right.unit != left.unit and side == "right"
                        else "left",
                        unit="percent" if delta else binding.unit,
                    )
                )
            if comparison and right is None and not delta:
                series.append(
                    dict(
                        card_id=left.card_id,
                        artifact=ref,
                        field="right",
                        axis="left",
                        unit=left.unit,
                    )
                )
            chart_id = uuid5(
                definition.report_id,
                digest(
                    {
                        "selection": selected.model_dump(mode="json"),
                        "series": [
                            {
                                k: str(v)
                                if isinstance(v, UUID)
                                else v.model_dump(mode="json")
                                if hasattr(v, "model_dump")
                                else v
                                for k, v in s.items()
                            }
                            for s in series
                        ],
                    }
                ),
            )
            chart = WorkspaceChartSpecV2(
                schema_version="2.0.0",
                chart_spec_id=chart_id,
                workspace_id=workspace,
                chart_type="line",
                selection=selected,
                series=[ChartSeriesRef.model_validate(s) for s in series],
                comparison=comparison.manifest if comparison else None,
                accessibility_table=ref,
            )
            stored_chart = self.repository.put_reference(
                workspace, actor, versioned("chart_spec", chart.model_dump(mode="json"))
            )
            chart_payloads = [WorkspaceChartSpecV2.model_validate(stored_chart["payload"])]
            charts = [stored_chart["reference"]]
        end = self.results.resolve(
            workspace, actor, definition.semantic_dataset_version_id, result_ids is None
        )
        if end != a:
            raise PresentationFailure("FORBIDDEN")
        return WorkspaceApplyResponse(
            contract_version="configured-report/v2",
            configuration_hash=digest(definition.model_dump(mode="json")),
            definition=definition,
            view_context=None,
            bindings_by_card=bindings,
            comparison=comparison,
            chart_specs=charts,
            base_revision=1,
            access_fingerprint=a.policy_hash,
            chart_payloads=chart_payloads,
            status="no_data"
            if not bindings or all(b.readiness == "no_data" for b in bindings)
            else "ready",
        )

    def apply(
        self, workspace: UUID, actor: UUID, report: UUID, request: WorkspaceApplyRequest
    ) -> WorkspaceApplyResponse:
        body = request.root
        reuse = body.reuse_result_ids if isinstance(body, CreatorApplyRequest) else None
        self.guard(
            workspace, actor, report, write=isinstance(body, CreatorApplyRequest), run=reuse is None
        )
        if isinstance(body, CreatorApplyRequest):
            current = self._candidate(workspace, actor, report, body.definition)
            definition = body.definition
        else:
            current = self._view_source(workspace, actor, report)
            definition = self._view_definition(
                self._definition(workspace, actor, current), body.view_override
            )
        if current["revision"] != body.base_revision:
            raise PresentationFailure("REVISION_CONFLICT")
        result = self._materialize(workspace, actor, definition, reuse)
        self.guard(
            workspace, actor, report, write=isinstance(body, CreatorApplyRequest), run=reuse is None
        )
        return result.model_copy(
            update={
                "base_revision": body.base_revision,
                "definition": definition if isinstance(body, CreatorApplyRequest) else None,
                "view_context": None
                if isinstance(body, CreatorApplyRequest)
                else body.view_override,
            }
        )

    @staticmethod
    def _default_view(definition: ConfiguredReportV2) -> ReaderViewOverride:
        active = next(
            (w for w in definition.worksets if w.workset_id == definition.default_workset_id), None
        )
        return ReaderViewOverride(
            query_context=ViewQueryContext(
                **definition.common_context.model_dump(), grain=definition.grain
            ),
            display=ViewDisplay(
                active_workset_id=definition.default_workset_id,
                selection=definition.selection,
                card_order=[c.card_id for c in active.cards] if active else [],
                hidden_card_ids=[],
                representation="chart",
                density="comfortable",
            ),
        )

    @staticmethod
    def _saved_view(
        workspace: UUID,
        actor: UUID,
        definition: ConfiguredReportV2,
        document: UUID,
        document_hash: str,
        revision: int,
        view_id: UUID,
        override: ReaderViewOverride,
        bindings: list[CardResultBinding],
        page_id: UUID,
    ) -> SavedViewV1:
        return SavedViewV1(
            schema_version="saved-view/v1",
            saved_view_id=view_id,
            version_id=uuid4(),
            revision=revision,
            workspace_id=workspace,
            owner_principal_id=actor,
            report_id=definition.report_id,
            document_version_id=document,
            document_content_hash=document_hash,
            calendar_ref=definition.calendar_ref,
            calendar_basis=definition.calendar_basis,
            page_ids=[page_id],
            result_scope=bindings,
            query_context=override.query_context,
            display=override.display,
        )

    def save(
        self, workspace: UUID, actor: UUID, report: UUID, request: WorkspaceSaveRequest
    ) -> WorkspaceReportResponse:
        self._candidate(workspace, actor, report, request.definition, check_instances=False)
        h = digest(request.model_dump(mode="json", exclude={"idempotency_key"}))
        replay = self.repository.replay(workspace, report, request.idempotency_key, h)
        if replay is not None:
            self._verify(workspace, actor, replay)
            return WorkspaceReportResponse.model_validate(replay)
        self._candidate(workspace, actor, report, request.definition)
        definition = request.definition
        verified = self._materialize(workspace, actor, definition, request.result_ids)
        if (
            verified.configuration_hash != request.configuration_hash
            or verified.chart_specs != request.chart_specs
        ):
            raise PresentationFailure("RESULT_BINDING_MISMATCH")
        document, snapshot, page_snapshot = uuid4(), uuid4(), uuid4()
        page = uuid5(report, "workspace/page")
        bindings = {b.card_id: b for b in verified.bindings_by_card}
        sections = [
            WorkspaceSection(section_id=w.workset_id, page_id=page, order=i, title=w.name)
            for i, w in enumerate(definition.worksets)
        ]
        blocks = [
            Block(
                block_id=c.card_id,
                section_id=w.workset_id,
                order=i,
                block_type="metric_group",
                source_binding=bindings[c.card_id].model_dump(mode="json"),
                presentation={},
            )
            for w in definition.worksets
            for i, c in enumerate(w.cards)
        ]
        filters = [
            WorkspaceFilterBinding(
                scope="document",
                scope_resource_id=report,
                expression=definition.common_context,
                combine_mode="intersect",
                linked_target_block_ids=[c.card_id for w in definition.worksets for c in w.cards],
                precedence=["security", "system_locked", "source_metric", "document"],
                policy_hash=verified.access_fingerprint,
                owner_principal_id=actor,
            )
        ]
        comp = AnalyticalDocumentCompositionV2(
            composition_schema_version=2,
            analytical_document_version_id=document,
            analytical_document_id=report,
            workspace_id=workspace,
            profile="workbook_report",
            source_owner_ref={
                "context": "presentation",
                "resource_type": "draft_report",
                "resource_version_id": str(document),
            },
            navigation_mode="tabs",
            default_page_id=page,
            chapters=[],
            pages=[
                Page(
                    page_id=page,
                    chapter_id=None,
                    order=0,
                    title={"ru": definition.title, "en": definition.title},
                    visibility="visible",
                    layout_mode="flow",
                )
            ],
            sections=sections,
            blocks=blocks,
            brand_profile_version_id=definition.brand_profile.id,
            access_policy_id=uuid5(report, "personal-policy"),
            filter_scope_bindings=filters,
            definition=definition,
            chart_specs=verified.chart_specs,
            bindings_by_card=verified.bindings_by_card,
            comparisons=[verified.comparison] if verified.comparison else [],
            chart_payloads=verified.chart_payloads,
        )
        comp_payload = comp.model_dump(mode="json")
        view = self._saved_view(
            workspace,
            actor,
            definition,
            document,
            digest(comp_payload),
            request.expected_saved_view_revision + 1,
            creator_saved_view_id(report, actor),
            self._default_view(definition),
            verified.bindings_by_card,
            page,
        )
        parents = [b.result.manifest.model_dump(mode="json") for b in verified.bindings_by_card]
        parents.append(definition.base_snapshot_ref.manifest.model_dump(mode="json"))
        if verified.comparison:
            parents.append(verified.comparison.manifest.model_dump(mode="json"))
        page_ref = artifact(
            self.artifacts.commit(
                workspace_id=workspace,
                artifact_id=page_snapshot,
                payload=page_payload(comp_payload),
                parents=parents,
            )
        )
        payload = dict(
            contract_version="configured-report/v2",
            report_id=str(report),
            revision=request.expected_revision + 1,
            version_id=str(document),
            snapshot_id=str(snapshot),
            author_principal_id=str(actor),
            saved_at=datetime.now(UTC).isoformat(),
            composition=comp_payload,
            saved_view={
                "id": str(view.version_id),
                "content_hash": digest(view.model_dump(mode="json")),
            },
            page_manifests=[page_ref],
            capabilities=self.capabilities(workspace, actor, report).model_dump(mode="json"),
        )
        payload["manifest"] = artifact(
            self.artifacts.commit(
                workspace_id=workspace,
                artifact_id=snapshot,
                payload=payload,
                parents=[page_ref, *parents],
            )
        )
        WorkspaceReportResponse.model_validate(payload)

        def recheck() -> None:
            self.guard(workspace, actor, report, write=True)
            self._materialize(
                workspace,
                actor,
                definition,
                request.result_ids,
                expected_bindings=verified.bindings_by_card,
                make_charts=False,
            )
            self._legacy(
                workspace,
                actor,
                self.repository.read(workspace, report, definition.base_snapshot_ref.snapshot_id),
            )

        saved = self.repository.save_workspace(
            workspace, actor, report, request, h, payload, view, recheck
        )
        self._verify(workspace, actor, saved)
        return WorkspaceReportResponse.model_validate(saved)

    def _view_source(
        self, workspace: UUID, actor: UUID, report: UUID, version: UUID | None = None
    ) -> dict[str, Any]:
        """Authorized base definition for an explicit narrower query, never old numeric output."""
        meta, _ = self.guard(workspace, actor, report)
        saved = self.repository.read(workspace, report, version=version)
        if saved["contract_version"] == "configured-report/v2" and meta["creator"] != actor:
            if version is not None:
                raise PresentationFailure("NOT_FOUND")
            saved = self.repository.read(
                workspace,
                report,
                UUID(saved["composition"]["definition"]["base_snapshot_ref"]["snapshot_id"]),
            )
        self.artifacts.verify(
            workspace_id=workspace,
            reference=saved["manifest"],
            payload={k: v for k, v in saved.items() if k != "manifest"},
        )
        definition = self._definition(workspace, actor, saved)
        self.results.resolve(workspace, actor, definition.semantic_dataset_version_id)
        return saved

    def _verify_view(self, workspace: UUID, actor: UUID, value: SavedViewV1) -> None:
        saved = self._view_source(
            workspace, actor, value.report_id, version=value.document_version_id
        )
        if digest(saved["composition"]) != value.document_content_hash:
            raise PresentationFailure("ARTIFACT_CORRUPT")
        definition = self._view_definition(
            self._definition(workspace, actor, saved),
            ReaderViewOverride(query_context=value.query_context, display=value.display),
        )
        if (definition.calendar_ref, definition.calendar_basis) != (
            value.calendar_ref,
            value.calendar_basis,
        ):
            raise PresentationFailure("INVALID_VIEW_SCOPE")
        self._materialize(
            workspace,
            actor,
            definition,
            [b.result.result_id for b in value.result_scope],
            expected_bindings=value.result_scope,
            make_charts=False,
        )

    def views(self, workspace: UUID, actor: UUID, report: UUID) -> list[SavedViewV1]:
        self.guard(workspace, actor, report)
        values = self.repository.views(workspace, actor, report)
        if not values:
            self._view_source(workspace, actor, report)
        for value in values:
            self._verify_view(workspace, actor, value)
        return values

    def save_view(
        self,
        workspace: UUID,
        actor: UUID,
        report: UUID,
        request: SaveViewRequest,
        view_id: UUID | None = None,
    ) -> SavedViewV1:
        self.guard(workspace, actor, report)
        saved = self._view_source(workspace, actor, report, version=request.document_version_id)
        definition = self._view_definition(
            self._definition(workspace, actor, saved), request.view_override
        )
        # No new calculation: a query-changing Save view needs results from explicit Apply.
        verified = self._materialize(
            workspace, actor, definition, request.result_ids, make_charts=False
        )
        view_id = view_id or uuid5(report, f"view/{actor}/{request.idempotency_key}")
        if request.expected_revision > 0:
            existing = self.repository.view(workspace, actor, view_id)
            if existing.report_id != report:
                raise PresentationFailure("NOT_FOUND")
        elif (
            view_id
            == creator_saved_view_id(report, self.repository.metadata(workspace, report)["creator"])
            and actor != self.repository.metadata(workspace, report)["creator"]
        ):
            raise PresentationFailure("NOT_FOUND")
        value = self._saved_view(
            workspace,
            actor,
            definition,
            request.document_version_id,
            digest(saved["composition"]),
            request.expected_revision + 1,
            view_id,
            request.view_override,
            verified.bindings_by_card,
            UUID(saved["composition"]["default_page_id"]),
        )

        def recheck() -> None:
            self.guard(workspace, actor, report)
            self._verify_view(workspace, actor, value)

        actual = self.repository.save_view(
            value,
            request,
            digest(request.model_dump(mode="json", exclude={"idempotency_key"})),
            recheck,
        )
        self._verify_view(workspace, actor, actual)
        return actual
