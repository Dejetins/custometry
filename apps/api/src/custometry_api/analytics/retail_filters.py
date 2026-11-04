"""Authenticated composition for published filter catalog and bounded previews."""
from uuid import UUID, uuid5

from fastapi import Request

from custometry_api.analytics.filter_access import PublishedRetailFilterAccess
from custometry_api.config import Settings
from custometry_api.database import connection_factory
from custometry_api.identity.http_auth import IdentityHTTPAdapter
from packages.analytics_core.infrastructure.columnar_filters import DuckDBFlatFilter
from packages.artifacts.infrastructure.sales import SalesArtifactStore
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.columnar_filters import FilterResourcePolicy
from packages.contracts.analytics.retail_filter import CatalogField, FilterCatalogResponse, FilterLabels
from packages.identity_access.application.resource_access import ResourceAccessService
from packages.identity_access.infrastructure.resource_access import PostgresResourceAccessRepository
from packages.semantic_model.infrastructure.postgres import PostgresSalesSemanticRepository

LABELS = {
    "source_system_id": ("Источник", "Source"), "store_id": ("Магазин", "Store"),
    "status": ("Статус чека", "Receipt status"), "currency": ("Валюта", "Currency"),
    "receipt_date": ("Дата чека", "Receipt date"),
}


def filter_resource_policy(settings: Settings) -> FilterResourcePolicy:
    bounds = dict(max_rows=settings.filter_max_rows, max_input_bytes=settings.filter_max_input_bytes,
                  memory_mb=settings.filter_memory_mb, timeout_ms=settings.filter_timeout_ms,
                  max_nodes=64, max_depth=12, max_values=1000, threads=1)
    return FilterResourcePolicy(version_id=uuid5(UUID("4388ed3e-f1b4-4c49-9499-80969cec76c5"),
                                                  str(sorted(bounds.items()))), **bounds)


def build_filters(settings: Settings, auth: IdentityHTTPAdapter, request: Request) -> DuckDBFlatFilter:
    connect = connection_factory(settings)
    policy = filter_resource_policy(settings)
    # No request memo: every delivery reauthenticates current session and policy.
    access = PublishedRetailFilterAccess(
        identity=ResourceAccessService(PostgresResourceAccessRepository(connect), lambda: auth.authenticate(request)),
        semantics=PostgresSalesSemanticRepository(connect),
        artifacts=SalesArtifactStore(connect, settings.analytics_artifact_root),
        resource_policy=policy, require_run=False)
    return DuckDBFlatFilter(artifact_root=settings.analytics_artifact_root, access=access)


def catalog(engine: DuckDBFlatFilter, workspace: UUID, actor: UUID, dataset: UUID,
            search: str) -> FilterCatalogResponse:
    grant = engine.access.authorize(workspace_id=workspace, actor_id=actor, dataset_version_id=dataset)
    fields: list[CatalogField] = []
    for field in grant.registry.fields:
        ru, en = LABELS[field.column]
        label = {"ru": ru, "en": en}
        description = {"ru": f"Опубликованное поле чека: {ru}", "en": f"Published receipt field: {en}"}
        haystack = " ".join([field.field_id, field.entity, field.data_type, *label.values(), *description.values()])
        if search.casefold() in haystack.casefold():
            fields.append(CatalogField(field=field, label=FilterLabels(**label), description=FilterLabels(**description)))
    if engine.access.authorize(workspace_id=workspace, actor_id=actor, dataset_version_id=dataset) != grant:
        raise AnalyticsFailure("FILTER_POLICY_CHANGED")
    return FilterCatalogResponse(registry_version_id=grant.registry.version_id, dataset_version_id=dataset,
                                fields=fields, mandatory_expression=grant.row_ceiling,
                                resource_policy_version_id=grant.resource_policy.version_id)
