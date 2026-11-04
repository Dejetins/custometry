"""Strict composer routes, with request-scoped Identity/Analytics/Artifacts ports."""
from threading import Event
from custometry_api.analytics.filter_cancellation import cancellable_filter
from typing import Any
from fastapi import Query
from packages.contracts.analytics.retail_filter import (FilterPreviewRequest, FilterPreviewResponse, FilterFacetRequest, FilterFacetResponse, FilterCatalogResponse)
from packages.analytics_core.infrastructure.retail_filter import PublishedReceiptFilter
from custometry_api.analytics.retail_filters import build_filters, catalog
from custometry_api.analytics.relational_filters import build_relational_filters, relational_catalog, relational_request
from packages.contracts.analytics.retail_relational import RelationalCatalogResponse, RelationalPreviewRequest, RelationalPreviewResponse, RelationalFacetRequest, RelationalFacetResponse
from custometry_api.analytics.aggregate_filters import build_aggregate_filters, aggregate_catalog
from packages.contracts.analytics.retail_aggregate import AggregateCatalogResponse, AggregatePreviewRequest, AggregatePreviewResponse, AggregateFacetRequest, receipt_aggregate_request
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.customer_events import CustomerEventCatalog, CustomerEventPreviewRequest, CustomerEventPreviewResponse, RootRestrictedSequenceGrant, customer_event_request
from custometry_api.analytics.customer_events import build_customer_events, customer_event_catalog, LIMITATIONS as CUSTOMER_EVENT_LIMITATIONS
from custometry_api.analytics.cohort_filters import build_cohort_filters, cohort_catalog
from packages.contracts.analytics.receipt_cohorts import CohortCatalogResponse, CohortPreviewRequest, CohortPreviewResponse, CohortFacetRequest, ReceiptCohortGrant, receipt_cohort_request
from packages.analytics_core.infrastructure.relational_filters import identity as filter_identity
from uuid import UUID
from fastapi import APIRouter, Request
from custometry_api.config import Settings
from custometry_api.identity.http_auth import IdentityHTTPAdapter
from custometry_api.reports.workspace_composition import build_workspace
from packages.contracts.presentation.composer import (
    ComposerApplyRequest, ComposerApplyResponse, ComposerSaveRequest,
    ComposerReportResponse, ComposerEditorResponse, ComposerPrepareResponse, ComposerCapabilities, ComposerPreflightResponse, ComposerValidationResponse, ComposerDefinitionV1, ComposerCompareRequest, CardComparisonV1,
)
from packages.contracts.presentation.workspace import NewWorkspaceRequest, ReportActor
from packages.presentation.application.composer import ComposerService
from packages.contracts.presentation import PresentationFailure
from packages.identity_access.domain.policy import Actor


def composer_router(settings: Settings, auth: IdentityHTTPAdapter, brand: dict[str, Any]) -> APIRouter:
    router = APIRouter(prefix="/composer/v1")

    def services(request: Request):
        actor = auth.authenticate(request)
        workspace, _ = build_workspace(settings, auth, request)
        return actor, ComposerService(workspace)

    def projection(actor: Actor) -> ReportActor:
        return ReportActor(workspace_id=actor.workspace_id, principal_id=actor.principal_id,
                           permissions=sorted(actor.permissions))

    @router.get("/filters/{dataset_id}/catalog", response_model=FilterCatalogResponse)
    def filter_catalog(dataset_id: UUID, request: Request, search: str = Query(default="", max_length=100)):
        a = auth.authenticate(request)
        return catalog(build_filters(settings, auth, request), a.workspace_id, a.principal_id, dataset_id, search)

    @router.get("/filters/v2/{dataset_id}/catalog", response_model=RelationalCatalogResponse)
    def correlated_catalog(dataset_id: UUID, request: Request, search: str = Query(default="", max_length=100)):
        a = auth.authenticate(request)
        return relational_catalog(build_relational_filters(settings, auth, request), a.workspace_id, a.principal_id, dataset_id, search)

    @router.post("/filters/v2/preview", response_model=RelationalPreviewResponse)
    async def correlated_preview(body: RelationalPreviewRequest, request: Request):
        a = auth.authenticate(request)
        engine = build_relational_filters(settings, auth, request)
        query = relational_request(a.workspace_id, body.dataset_version_id, body.filter)
        def execute(cancel: Event):
            result = engine.execute(query, actor_id=a.principal_id, cancel=cancel)
            return RelationalPreviewResponse(request_hash=result.request_hash,
                matched_count=len(result.matched_ids), not_matched_count=result.not_matched_count,
                unknown_count=result.unknown_count, authorized_count=result.authorized_count,
                limitation_codes=result.limitation_codes)
        return await cancellable_filter(request, execute)

    @router.post("/filters/v2/facets", response_model=RelationalFacetResponse)
    async def correlated_facets(body: RelationalFacetRequest, request: Request):
        a = auth.authenticate(request)
        engine = build_relational_filters(settings, auth, request)
        query = relational_request(a.workspace_id, body.dataset_version_id, body.filter)
        return await cancellable_filter(request, lambda cancel: engine.facets(query,body.facet,actor_id=a.principal_id,cancel=cancel))

    @router.get("/filters/v3/{dataset_id}/catalog", response_model=AggregateCatalogResponse)
    def count_catalog(dataset_id: UUID, request: Request, search: str = Query(default="", max_length=100)):
        a = auth.authenticate(request)
        return aggregate_catalog(build_aggregate_filters(settings, auth, request), a.workspace_id, a.principal_id, dataset_id, search)

    @router.post("/filters/v3/preview", response_model=AggregatePreviewResponse)
    async def count_preview(body: AggregatePreviewRequest, request: Request):
        a = auth.authenticate(request)
        engine = build_aggregate_filters(settings, auth, request)
        query = receipt_aggregate_request(a.workspace_id, body.dataset_version_id, body.filter)
        def execute(cancel: Event):
            result = engine.execute(query, actor_id=a.principal_id, cancel=cancel)
            return AggregatePreviewResponse(request_hash=result.request_hash,
                matched_count=len(result.matched_ids), not_matched_count=result.not_matched_count,
                unknown_count=result.unknown_count, authorized_count=result.authorized_count,
                limitation_codes=result.limitation_codes)
        return await cancellable_filter(request, execute)

    @router.post("/filters/v3/facets", response_model=RelationalFacetResponse)
    async def count_facets(body: AggregateFacetRequest, request: Request):
        a = auth.authenticate(request)
        engine = build_aggregate_filters(settings, auth, request)
        query = receipt_aggregate_request(a.workspace_id, body.dataset_version_id, body.filter)
        return await cancellable_filter(request, lambda cancel: engine.facets(query,body.facet,actor_id=a.principal_id,cancel=cancel))

    @router.get("/filters/v4/{dataset_id}/catalog", response_model=CohortCatalogResponse)
    def receipt_cohort_catalog(dataset_id: UUID, request: Request, search: str = Query(default="", max_length=100)):
        a = auth.authenticate(request)
        return cohort_catalog(settings, auth, request, a.workspace_id, a.principal_id, dataset_id, search)

    @router.post("/filters/v4/preview", response_model=CohortPreviewResponse)
    async def cohort_preview(body: CohortPreviewRequest, request: Request):
        a = auth.authenticate(request)
        engine = build_cohort_filters(settings, auth, request, require_run=True)
        query = receipt_cohort_request(a.workspace_id, body.dataset_version_id, body.filter)
        def execute(cancel: Event):
            grant = engine.access.authorize(workspace_id=a.workspace_id, actor_id=a.principal_id, dataset_version_id=body.dataset_version_id)
            if not isinstance(grant, ReceiptCohortGrant) or len(grant.root_restrictions) != 1:
                raise AnalyticsFailure("FILTER_COHORT_BINDING")
            result = engine.execute(query, actor_id=a.principal_id, cancel=cancel)
            if result.request_hash != filter_identity(query, a.principal_id, grant):
                raise AnalyticsFailure("FILTER_POLICY_CHANGED")
            return CohortPreviewResponse(request_hash=result.request_hash, matched_count=len(result.matched_ids), not_matched_count=result.not_matched_count, unknown_count=result.unknown_count, authorized_count=result.authorized_count, limitation_codes=tuple(sorted(set(result.limitation_codes)|set(CUSTOMER_EVENT_LIMITATIONS))), universe=grant.root_restrictions[0])
        return await cancellable_filter(request, execute)

    @router.post("/filters/v4/facets", response_model=RelationalFacetResponse)
    async def cohort_facets(body: CohortFacetRequest, request: Request):
        a = auth.authenticate(request)
        engine = build_cohort_filters(settings, auth, request, require_run=True)
        query = receipt_cohort_request(a.workspace_id, body.dataset_version_id, body.filter)
        return await cancellable_filter(request, lambda cancel: engine.facets(query, body.facet, actor_id=a.principal_id, cancel=cancel))

    @router.get("/filters/customer-events/v1/{dataset_id}/catalog", response_model=CustomerEventCatalog)
    def event_catalog(dataset_id: UUID, request: Request, search: str = Query(default="", max_length=100)):
        a = auth.authenticate(request)
        return customer_event_catalog(build_customer_events(settings,auth,request,require_run=False),a.workspace_id,a.principal_id,dataset_id,search)

    @router.post("/filters/customer-events/v1/preview", response_model=CustomerEventPreviewResponse)
    async def event_preview(body: CustomerEventPreviewRequest, request: Request):
        a=auth.authenticate(request)
        engine=build_customer_events(settings,auth,request,require_run=True)
        query=customer_event_request(a.workspace_id,body.dataset_version_id,body.filter)
        def execute(cancel: Event):
            grant=engine.access.authorize(workspace_id=a.workspace_id,actor_id=a.principal_id,dataset_version_id=body.dataset_version_id)
            if not isinstance(grant,RootRestrictedSequenceGrant) or len(grant.root_restrictions)!=1:
                raise AnalyticsFailure("FILTER_CUSTOMER_EVENT_BINDING")
            result=engine.execute(query,actor_id=a.principal_id,cancel=cancel)
            if result.request_hash!=filter_identity(query,a.principal_id,grant):
                raise AnalyticsFailure("FILTER_POLICY_CHANGED")
            return CustomerEventPreviewResponse(request_hash=result.request_hash,matched_count=len(result.matched_ids),not_matched_count=result.not_matched_count,unknown_count=result.unknown_count,authorized_count=result.authorized_count,limitation_codes=tuple(sorted(set(result.limitation_codes)|set(CUSTOMER_EVENT_LIMITATIONS))),universe=grant.root_restrictions[0])
        return await cancellable_filter(request,execute)

    async def filter_work(body: FilterPreviewRequest, request: Request):
        a = auth.authenticate(request)
        engine = build_filters(settings, auth, request)
        query = PublishedReceiptFilter.request(a.workspace_id, body.dataset_version_id, body.filter)
        def execute(cancel: Event):
            if isinstance(body, FilterFacetRequest):
                return engine.facets(query, body.facet, actor_id=a.principal_id, cancel=cancel)
            result = engine.execute(query, actor_id=a.principal_id, cancel=cancel)
            return FilterPreviewResponse(request_hash=result.request_hash,
                matched_count=len(result.matched_ids), not_matched_count=result.not_matched_count,
                unknown_count=result.unknown_count, authorized_count=result.authorized_count)
        return await cancellable_filter(request, execute)

    @router.post("/filters/preview", response_model=FilterPreviewResponse)
    async def filter_preview(body: FilterPreviewRequest, request: Request):
        return await filter_work(body, request)

    @router.post("/filters/facets", response_model=FilterFacetResponse)
    async def filter_facets(body: FilterFacetRequest, request: Request):
        return await filter_work(body, request)

    @router.post("/prepare", response_model=ComposerPrepareResponse)
    def prepare(body: NewWorkspaceRequest, request: Request):
        a, service = services(request)
        definition = service.prepare(a.workspace_id, a.principal_id, body, brand)
        can_apply = True
        try:
            service.authorize(a.workspace_id, a.principal_id, definition, run=True)
        except PresentationFailure:
            can_apply = False
        return ComposerPrepareResponse(definition=definition, actor=projection(a),
                                       capabilities=ComposerCapabilities(definition_edit=True, block_apply=can_apply))

    @router.post("/compare", response_model=CardComparisonV1)
    def compare(body: ComposerCompareRequest, request: Request):
        a, service = services(request)
        return service.compare(a.workspace_id, a.principal_id, body)

    @router.post("/validate", response_model=ComposerValidationResponse)
    def validate(body: ComposerDefinitionV1, request: Request):
        a, service = services(request)
        return service.validate_definition(a.workspace_id, a.principal_id, body)

    @router.get("/{report_id}/snapshots/{snapshot_id}/blocks/{block_id}/preflight", response_model=ComposerPreflightResponse)
    def saved_preflight(report_id: UUID, snapshot_id: UUID, block_id: UUID, request: Request):
        a, service = services(request)
        return service.saved_preflight(a.workspace_id, a.principal_id, report_id, snapshot_id, block_id)

    @router.post("/preflight", response_model=ComposerPreflightResponse)
    def preflight(body: ComposerApplyRequest, request: Request):
        a, service = services(request)
        return service.preflight(a.workspace_id, a.principal_id, body)

    @router.post("/apply", response_model=ComposerApplyResponse)
    def apply(body: ComposerApplyRequest, request: Request):
        a, service = services(request)
        return service.apply(a.workspace_id, a.principal_id, body)

    @router.post("/versions", response_model=ComposerReportResponse)
    def save(body: ComposerSaveRequest, request: Request):
        a, service = services(request)
        return service.save(a.workspace_id, a.principal_id, body)

    @router.get("/{report_id}", response_model=ComposerEditorResponse)
    def get(report_id: UUID, request: Request):
        a, service = services(request)
        saved = service.get(a.workspace_id, a.principal_id, report_id)
        caps = service.workspace.capabilities(a.workspace_id, a.principal_id, report_id)
        return ComposerEditorResponse(report=saved, actor=projection(a), capabilities=ComposerCapabilities(
            definition_edit=caps.definition_edit, block_apply=caps.definition_edit and caps.view_apply))

    @router.get("/{report_id}/snapshots/{snapshot_id}", response_model=ComposerEditorResponse)
    def snapshot(report_id: UUID, snapshot_id: UUID, request: Request):
        a, service = services(request)
        return ComposerEditorResponse(report=service.get(a.workspace_id, a.principal_id, report_id, snapshot_id),
                                      actor=projection(a), capabilities=ComposerCapabilities())

    @router.get("/{report_id}/snapshots/{snapshot_id}/blocks/{block_id}/result", response_model=ComposerApplyResponse)
    def result(report_id: UUID, snapshot_id: UUID, block_id: UUID, request: Request):
        a, service = services(request)
        return service.result(a.workspace_id, a.principal_id, report_id, snapshot_id, block_id)

    _ = receipt_cohort_catalog, cohort_preview, cohort_facets, event_catalog, event_preview, count_catalog, count_preview, count_facets, correlated_catalog, correlated_preview, correlated_facets, filter_catalog, filter_preview, filter_facets, prepare, compare, validate, saved_preflight, preflight, apply, save, get, snapshot, result
    return router
