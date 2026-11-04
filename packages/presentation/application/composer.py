"""Versioned personal composition; Save persists inputs without hidden calculation."""
from __future__ import annotations
from datetime import UTC, datetime
from uuid import UUID, uuid4, uuid5
from typing import Any

from packages.contracts.analytics.workspace import WorkspaceCardRequest, CardResultBinding, WorkspaceAccess, WorkspaceResultV2, WorkspaceScopeInput, CardComparisonV1
from packages.contracts.presentation import PresentationFailure
from packages.contracts.presentation.composer import (
    ComposerApplyRequest, ComposerApplyResponse, ComposerDefinitionV1,
    ComposerReportResponse, ComposerSaveRequest, ComposerPreflightResponse, ComposerValidationResponse, ComposerCompareRequest, RetailAnalysisInput, ComposerPage, ComposerSection, input_fingerprint,
)
from packages.contracts.presentation.workspace import NewWorkspaceRequest
from packages.presentation.application.workspace import WorkspaceReportService, artifact
from packages.presentation.domain.reports import digest
from packages.presentation.domain.scopes import resolve_scope, validate_scope_graph, preserve_scope_locks
from packages.contracts.presentation.scopes import ComposerScopesV1


class ComposerService:
    def __init__(self, workspace: WorkspaceReportService):
        self.workspace = workspace
        self.repository = workspace.repository

    def effective_source(self, definition: ComposerDefinitionV1, block_id: UUID) -> RetailAnalysisInput:
        block = next((b for b in definition.blocks if b.block_id == block_id), None)
        if block is None or block.source is None:
            raise PresentationFailure("COMPOSER_UNKNOWN_BLOCK")
        source = next(s for s in definition.definitions if s.definition_id == block.source.definition_id)
        if definition.scopes is None and not any(b.control for b in definition.blocks):
            return source
        try:
            resolved = resolve_scope(definition, definition.scopes or ComposerScopesV1(), block_id)
        except ValueError as exc:
            raise PresentationFailure(str(exc)) from exc
        query = resolved.query
        if resolved.dependency_hash is not None:
            query = query.model_copy(update={"scope": WorkspaceScopeInput(dependency_hash=resolved.dependency_hash, filters=resolved.filters)})
        # Derived provider inputs are never admitted as authorable source queries.
        return source.model_copy(update={"query": query})

    def preflight(self, tenant: UUID, actor: UUID, request: ComposerApplyRequest) -> ComposerPreflightResponse:
        definition = request.definition
        self.authorize(tenant, actor, definition)
        source = self.effective_source(definition, request.block_id)
        self.validate_sources(tenant, actor, definition, source.definition_id, block_id=request.block_id)
        provider = self.workspace.results.preflight(tenant, actor, source.query)
        self.authorize(tenant, actor, definition)
        resolved = resolve_scope(definition, definition.scopes or ComposerScopesV1(), request.block_id)
        return ComposerPreflightResponse(block_id=request.block_id, effective_query=source.query, origins=resolved.origins, provider=provider)

    def validate_definition(self, tenant: UUID, actor: UUID, definition: ComposerDefinitionV1) -> ComposerValidationResponse:
        self.authorize(tenant, actor, definition)
        self.validate_sources(tenant, actor, definition)
        self.authorize(tenant, actor, definition)
        return ComposerValidationResponse()

    def saved_preflight(self, tenant: UUID, actor: UUID, report: UUID, snapshot: UUID, block: UUID) -> ComposerPreflightResponse:
        definition = self.get(tenant, actor, report, snapshot).definition
        source = self.effective_source(definition, block)
        provider = self.workspace.results.preflight(tenant, actor, source.query)
        resolved = resolve_scope(definition, definition.scopes or ComposerScopesV1(), block)
        self.workspace.guard(tenant, actor, report)
        return ComposerPreflightResponse(block_id=block, effective_query=source.query, origins=resolved.origins, provider=provider)

    def authorize(self, tenant: UUID, actor: UUID, definition: ComposerDefinitionV1, *, run: bool = False) -> None:
        if definition.scopes is not None:
            try:
                validate_scope_graph(definition, definition.scopes)
            except ValueError as exc:
                raise PresentationFailure(str(exc)) from exc
        if definition.creator_principal_id != actor:
            raise PresentationFailure("FORBIDDEN")
        try:
            metadata = self.repository.metadata(tenant, definition.document_id)
        except PresentationFailure as exc:
            if exc.code != "NOT_FOUND":
                raise
        else:
            if metadata["creator"] != actor:
                raise PresentationFailure("FORBIDDEN")
            self.workspace.guard(tenant, actor, definition.document_id, write=True, run=run)
            payload = self.repository.read(tenant, definition.document_id)
            if payload.get("contract_version") != "composed-report/v1":
                raise PresentationFailure("REPORT_VERSION_UPGRADE_REQUIRED")
            self.workspace.artifacts.verify(workspace_id=tenant, reference=payload["manifest"],
                payload={k: v for k, v in payload.items() if k != "manifest"})
            baseline = ComposerReportResponse.model_validate(payload)
            try:
                preserve_scope_locks(baseline.definition, definition)
            except ValueError as exc:
                raise PresentationFailure(str(exc)) from exc
        required = {"report.read", "report.manage", "analysis.read"} | ({"analysis.run"} if run else set[str]())
        for action in ["view_snapshot", "edit"] + (["run"] if run else []):
            decision = self.workspace.access.resolve_resource(
                workspace_id=tenant, principal_id=actor, resource_type="report",
                resource_id=definition.document_id, action=action, legacy_creator=actor,
            )
            if not decision.allowed or not required <= decision.permissions:
                raise PresentationFailure("FORBIDDEN")
        if definition.origin is not None:
            raise PresentationFailure("COMPOSER_CAPABILITY_UNAVAILABLE")
        for name in ("brand_profile", "company_pack"):
            self.repository.get_reference(tenant, actor, getattr(definition, name).model_dump(mode="json"), name)

    def validate_sources(self, tenant: UUID, actor: UUID, definition: ComposerDefinitionV1, source_id: UUID | None = None, *, verify_provider: bool = True, block_id: UUID | None = None) -> None:
        """Validate capability and access, without computing an analytical result."""
        contexts: dict[UUID, tuple[WorkspaceAccess, dict[str, Any] | None]] = {}
        for value in definition.definitions:
            if source_id is not None and value.definition_id != source_id:
                continue
            query = value.query
            dataset = query.semantic_dataset_version_id
            if dataset not in contexts:
                contexts[dataset] = (
                    self.workspace.results.resolve(tenant, actor, dataset),
                    self.workspace.results.context(tenant, actor, dataset) if verify_provider else None,
                )
            access, context = contexts[dataset]
            if verify_provider:
                assert context is not None
                self.workspace.calendars.get_version(query.calendar_ref, access)
                registered = [{k: m[k] for k in ("metric_id", "version_id", "content_hash")} for m in context["metrics"]]
                if any(m.model_dump(mode="json") not in registered for m in query.metric_refs):
                    raise PresentationFailure("METRIC_BASIS_MISMATCH")
            allowed = set(access.allowed_store_ids)
            stores = allowed.copy()
            for requested in (query.common.store_ids, query.local_store_ids):
                if requested is not None:
                    if not set(requested) <= allowed:
                        raise PresentationFailure("FORBIDDEN")
                    stores.intersection_update(requested)
            decision = self.workspace.access.resolve_resource(
                workspace_id=tenant, principal_id=actor, resource_type="report",
                resource_id=definition.document_id, action="view_snapshot", legacy_creator=actor,
            )
            if not decision.allowed or (definition.scopes is None and not any(b.control for b in definition.blocks) and decision.store_ids is not None and not stores <= set(decision.store_ids)):
                raise PresentationFailure("FORBIDDEN")

        for control in (b.control for b in definition.blocks if b.control is not None):
            access = self.workspace.results.resolve(tenant, actor, control.semantic_dataset_version_id)
            if control.store_ids is not None and not set(control.store_ids) <= set(access.allowed_store_ids):
                raise PresentationFailure("FORBIDDEN")

        if any(b.control for b in definition.blocks) or definition.scopes is not None or any(s.query.receipt_filter is not None for s in definition.definitions):
            for block in definition.blocks:
                if block.source is None:
                    continue
                if block_id is not None and block.block_id != block_id:
                    continue
                if source_id is not None and block.source.definition_id != source_id:
                    continue
                source = self.effective_source(definition, block.block_id)
                checked = self.workspace.results.preflight(tenant, actor, source.query)
                decision = self.workspace.access.resolve_resource(workspace_id=tenant, principal_id=actor,
                    resource_type="report", resource_id=definition.document_id, action="view_snapshot", legacy_creator=actor)
                if not decision.allowed or (decision.store_ids is not None and not set(checked.effective_context.store_ids) <= set(decision.store_ids)):
                    raise PresentationFailure("FORBIDDEN")

    def prepare(self, tenant: UUID, actor: UUID, request: NewWorkspaceRequest, brand: dict[str, Any]) -> ComposerDefinitionV1:
        legacy = self.workspace.new_definition(tenant, actor, request.model_copy(update={"template": "blank"}), brand)
        page, section = uuid5(legacy.report_id, "composer/page"), uuid5(legacy.report_id, "composer/section")
        return ComposerDefinitionV1(
            document_id=legacy.report_id, creator_principal_id=actor, profile="workbook_report",
            title=legacy.title, brand_profile=legacy.brand_profile, company_pack=legacy.company_pack,
            default_page_id=page, pages=[ComposerPage(page_id=page, order=0, title=legacy.title, layout="dashboard_grid")],
            sections=[ComposerSection(section_id=section, page_id=page, order=0, title=legacy.title)],
            blocks=[], definitions=[], grid_columns=24,
        )

    def apply(self, tenant: UUID, actor: UUID, request: ComposerApplyRequest) -> ComposerApplyResponse:
        definition = request.definition
        self.authorize(tenant, actor, definition, run=True)
        block = next((b for b in definition.blocks if b.block_id == request.block_id), None)
        if block is None or block.source is None:
            raise PresentationFailure("COMPOSER_UNKNOWN_BLOCK")
        source = self.effective_source(definition, block.block_id)
        # Data checks must precede run; applying one block must not calculate others.
        self.validate_sources(tenant, actor, definition, source.definition_id, block_id=request.block_id)
        value = self.workspace.results.apply(tenant, actor, [WorkspaceCardRequest(
            card_id=block.block_id, metric_ref=block.source.metric_ref, query=source.query,
            configuration_hash=input_fingerprint(source),
        )])
        self.authorize(tenant, actor, definition, run=True)
        result = value.results[0]
        return ComposerApplyResponse(block_id=block.block_id, input_fingerprint=input_fingerprint(source),
                                     binding=value.bindings[0], result=result)

    def comparison_bindings(self, tenant: UUID, actor: UUID, request: ComposerCompareRequest) -> tuple[UUID, CardResultBinding, CardResultBinding]:
        pair = request.definition.pair
        if pair is None:
            raise PresentationFailure("COMPOSER_PAIR_REQUIRED")
        references = {r.block_id: r.result_id for r in request.results}
        bindings: list[CardResultBinding] = []
        datasets: set[UUID] = set()
        for identifier in (pair.left_block_id, pair.right_block_id):
            if identifier not in references:
                raise PresentationFailure("COMPOSER_PAIR_RESULT_REQUIRED")
            source = self.effective_source(request.definition, identifier)
            self.validate_sources(tenant, actor, request.definition, source.definition_id, block_id=identifier)
            block = next(b for b in request.definition.blocks if b.block_id == identifier)
            result = self.workspace.results.verify(tenant, actor, source.query, references[identifier])
            datasets.add(result.semantic_dataset_version_id)
            metric = block.source.metric_ref.metric_id
            bindings.append(CardResultBinding.model_validate(dict(card_id=identifier, metric_ref=block.source.metric_ref,
                result=dict(result_id=result.result_id, schema_version=result.schema_version, manifest=result.manifest),
                effective_context_hash=digest(result.effective_context.model_dump(mode="json")),
                configuration_hash=input_fingerprint(source), bucket_projection=metric,
                unit={"net_revenue":"EUR","receipt_count":"receipt","average_receipt":"EUR/receipt"}[metric],
                format=dict(decimal_places=0 if metric=="receipt_count" else 2), readiness=result.trust.status)))
        if len(datasets) != 1:
            raise PresentationFailure("COMPOSER_PAIR_DATASET_MISMATCH")
        return next(iter(datasets)), bindings[0], bindings[1]

    def compare(self, tenant: UUID, actor: UUID, request: ComposerCompareRequest) -> CardComparisonV1:
        self.authorize(tenant, actor, request.definition)
        dataset, left, right = self.comparison_bindings(tenant, actor, request)
        value = self.workspace.results.compare(tenant, actor, dataset, left, right)
        self.authorize(tenant, actor, request.definition)
        return value

    def verify_comparison(self, tenant: UUID, actor: UUID, definition: ComposerDefinitionV1,
                          results: list[Any], comparison: CardComparisonV1 | None) -> list[dict[str, Any]]:
        if comparison is None:
            return []
        if definition.pair is None:
            raise PresentationFailure("COMPOSER_PAIR_REQUIRED")
        request = ComposerCompareRequest(contract_version="analytical-authoring/v1", definition=definition, results=results)
        dataset, left, right = self.comparison_bindings(tenant, actor, request)
        if (comparison.mode != "pair" or comparison.left.card_id != left.card_id
            or comparison.right.card_id != right.card_id or comparison.left.metric_ref != left.metric_ref
            or comparison.right.metric_ref != right.metric_ref or comparison.left.result != left.result
            or comparison.right.result != right.result):
            raise PresentationFailure("RESULT_BINDING_MISMATCH")
        self.workspace.results.verify_comparison(tenant, actor, dataset, comparison)
        return [comparison.manifest.model_dump(mode="json")]

    def _verify_results(self, tenant: UUID, actor: UUID, request: ComposerSaveRequest) -> list[dict[str, Any]]:
        blocks = {b.block_id: b for b in request.definition.blocks}
        if len({r.block_id for r in request.results}) != len(request.results):
            raise PresentationFailure("RESULT_BINDING_MISMATCH")
        parents: list[dict[str, Any]] = []
        verified: dict[tuple[str, UUID], WorkspaceResultV2] = {}
        for reference in request.results:
            block = blocks.get(reference.block_id)
            if block is None or block.source is None:
                raise PresentationFailure("RESULT_BINDING_MISMATCH")
            source = self.effective_source(request.definition, block.block_id)
            key = (input_fingerprint(source), reference.result_id)
            if key not in verified:
                verified[key] = self.workspace.results.verify(tenant, actor, source.query, reference.result_id)
            result = verified[key]
            parents.append(result.manifest.model_dump(mode="json"))
        parents.extend(self.verify_comparison(tenant, actor, request.definition, request.results, request.comparison))
        return parents

    def save(self, tenant: UUID, actor: UUID, request: ComposerSaveRequest) -> ComposerReportResponse:
        definition = request.definition
        self.authorize(tenant, actor, definition)
        request_hash = digest(request.model_dump(mode="json", exclude={"idempotency_key"}))
        replay = self.repository.replay(tenant, definition.document_id, request.idempotency_key, request_hash)
        if replay is not None:
            return self._verify(tenant, actor, replay)
        self.validate_sources(tenant, actor, definition)
        parents = self._verify_results(tenant, actor, request)
        snapshot = uuid4()
        payload: dict[str, Any] = dict(
            contract_version="composed-report/v1", report_id=str(definition.document_id),
            revision=request.expected_revision + 1, version_id=str(uuid4()), snapshot_id=str(snapshot),
            author_principal_id=str(actor), saved_at=datetime.now(UTC).isoformat(),
            definition=definition.model_dump(mode="json"), results=[r.model_dump(mode="json") for r in request.results],
        )
        if "comparison" in request.model_fields_set:
            payload["comparison"] = request.comparison.model_dump(mode="json") if request.comparison is not None else None
        payload["manifest"] = artifact(self.workspace.artifacts.commit(
            workspace_id=tenant, artifact_id=snapshot, payload=payload, parents=parents,
        ))
        ComposerReportResponse.model_validate(payload)

        def recheck():
            self.authorize(tenant, actor, definition)
            self.validate_sources(tenant, actor, definition)
            self._verify_results(tenant, actor, request)

        saved = self.repository.save_composer(tenant, actor, request, request_hash, payload, recheck)
        recheck()
        return ComposerReportResponse.model_validate(saved)

    def _verify(self, tenant: UUID, actor: UUID, saved: dict[str, Any]) -> ComposerReportResponse:
        report = UUID(saved["report_id"])
        metadata, _ = self.workspace.guard(tenant, actor, report)
        if metadata["creator"] != actor:
            raise PresentationFailure("NOT_FOUND")
        if saved["contract_version"] != "composed-report/v1":
            raise PresentationFailure("REPORT_VERSION_UPGRADE_REQUIRED")
        value = ComposerReportResponse.model_validate(saved)
        self.validate_sources(tenant, actor, value.definition, verify_provider=False)
        self.workspace.artifacts.verify(workspace_id=tenant, reference=saved["manifest"],
                                        payload={k: v for k, v in saved.items() if k != "manifest"})
        self.verify_comparison(tenant, actor, value.definition, value.results, value.comparison)
        self.workspace.guard(tenant, actor, report)
        return value

    def get(self, tenant: UUID, actor: UUID, report: UUID, snapshot: UUID | None = None) -> ComposerReportResponse:
        self.workspace.guard(tenant, actor, report)
        return self._verify(tenant, actor, self.repository.read(tenant, report, snapshot))


    def result(self, tenant: UUID, actor: UUID, report: UUID, snapshot: UUID, block_id: UUID):
        saved = self.get(tenant, actor, report, snapshot)
        block = next((b for b in saved.definition.blocks if b.block_id == block_id), None)
        reference = next((r for r in saved.results if r.block_id == block_id), None)
        if block is None or reference is None:
            raise PresentationFailure("NOT_FOUND")
        source = self.effective_source(saved.definition, block_id)
        result = self.workspace.results.verify(tenant, actor, source.query, reference.result_id)
        self.workspace.guard(tenant, actor, report)
        metric = block.source.metric_ref.metric_id
        fingerprint = input_fingerprint(source)
        binding = CardResultBinding.model_validate(dict(
            card_id=block_id, metric_ref=block.source.metric_ref,
            result=dict(result_id=result.result_id, schema_version=result.schema_version, manifest=result.manifest),
            effective_context_hash=digest(result.effective_context.model_dump(mode="json")),
            configuration_hash=fingerprint, bucket_projection=metric,
            unit={"net_revenue": "EUR", "receipt_count": "receipt", "average_receipt": "EUR/receipt"}[metric],
            format=dict(decimal_places=0 if metric == "receipt_count" else 2), readiness=result.trust.status,
        ))
        return ComposerApplyResponse(block_id=block_id, input_fingerprint=fingerprint, binding=binding, result=result)
