"""Authenticated correlated catalog, preview and report-provider composition."""

from uuid import UUID, uuid5
from fastapi import Request
from custometry_api.analytics.relational_access import PublishedRetailRelationalAccess
from custometry_api.analytics.retail_filters import filter_resource_policy, LABELS
from custometry_api.config import Settings
from custometry_api.database import connection_factory
from custometry_api.identity.http_auth import IdentityHTTPAdapter
from packages.analytics_core.infrastructure.relational_filters import DuckDBRelationalFilter
from packages.artifacts.infrastructure.sales import SalesArtifactStore
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.relational_filters import (
    RelationalFilterRequest,
    RelationalResourcePolicy,
)
from packages.contracts.analytics.retail_filter import CatalogField, FilterLabels
from packages.contracts.analytics.retail_relational import (
    RelationalReceiptFilterInput,
    RelationalCatalogResponse,
    CatalogRelationship,
    receipt_relational_request,
)
from packages.identity_access.application.resource_access import ResourceAccessService
from packages.identity_access.infrastructure.resource_access import PostgresResourceAccessRepository
from packages.semantic_model.infrastructure.postgres import PostgresSalesSemanticRepository

ITEM_LABELS = {
    "receipt_id": ("Идентификатор чека", "Receipt ID"),
    "line_id": ("Идентификатор позиции", "Item ID"),
    "product_id": ("Идентификатор товара", "Product ID"),
    "quantity": ("Количество", "Quantity"),
    "unit_price": ("Цена за единицу", "Unit price"),
    "discount_amount": ("Скидка позиции", "Item discount"),
    "net_amount": ("Сумма позиции", "Item net amount"),
}


def relational_resource_policy(settings: Settings) -> RelationalResourcePolicy:
    base = filter_resource_policy(settings).model_dump()
    base.update(max_entities=2, max_correlations=16, max_fan_out=10000, max_estimated_work=17000000)
    base["version_id"] = uuid5(base["version_id"], "retail-correlated/v2:2:16:10000:17000000")
    return RelationalResourcePolicy(**base)


def build_relational_filters(
    settings: Settings, auth: IdentityHTTPAdapter, request: Request
) -> DuckDBRelationalFilter:
    connect = connection_factory(settings)

    def current_actor():
        # Catalog GET revalidation must not reuse the HTTP adapter's request cache.
        if hasattr(request.state, "identity_actor"):
            delattr(request.state, "identity_actor")
        return auth.authenticate(request)

    access = PublishedRetailRelationalAccess(
        identity=ResourceAccessService(PostgresResourceAccessRepository(connect), current_actor),
        semantics=PostgresSalesSemanticRepository(connect),
        artifacts=SalesArtifactStore(connect, settings.analytics_artifact_root),
        resource_policy=relational_resource_policy(settings),
        require_run=False,
    )
    return DuckDBRelationalFilter(artifact_root=settings.analytics_artifact_root, access=access)


def relational_request(
    workspace: UUID, dataset: UUID, value: RelationalReceiptFilterInput
) -> RelationalFilterRequest:
    return receipt_relational_request(workspace, dataset, value)


def relational_catalog(
    engine: DuckDBRelationalFilter, workspace: UUID, actor: UUID, dataset: UUID, search: str
) -> RelationalCatalogResponse:
    grant = engine.access.authorize(
        workspace_id=workspace, actor_id=actor, dataset_version_id=dataset
    )
    fields: list[CatalogField] = []
    for entity in grant.entities:
        for f in entity.registry.fields:
            ru, en = (LABELS | ITEM_LABELS)[f.column]
            description = FilterLabels(
                ru=f"Опубликованное поле {f.entity}: {ru}", en=f"Published {f.entity} field: {en}"
            )
            if (
                search.casefold()
                in " ".join(
                    [f.field_id, f.entity, f.data_type, ru, en, description.ru, description.en]
                ).casefold()
            ):
                fields.append(
                    CatalogField(field=f, label=FilterLabels(ru=ru, en=en), description=description)
                )
    if (
        engine.access.authorize(workspace_id=workspace, actor_id=actor, dataset_version_id=dataset)
        != grant
    ):
        raise AnalyticsFailure("FILTER_POLICY_CHANGED")
    return RelationalCatalogResponse(
        legacy_registry_version_id=grant.compatibility_registry_versions[0],
        dataset_version_id=dataset,
        registry_versions={e.registry.entity: e.registry.version_id for e in grant.entities},
        fields=fields,
        relationships=[
            CatalogRelationship(
                relationship=r.relationship,
                label=FilterLabels(ru="Позиции чека", en="Receipt items"),
                complete=r.complete,
                completeness_hash=r.completeness_hash,
            )
            for r in grant.relationships
        ],
        mandatory_expressions={e.registry.entity: e.row_ceiling for e in grant.entities},
        resource_policy_version_id=grant.resource_policy.version_id,
        limitation_codes=("RELATIONSHIP_HISTORY_INCOMPLETE",),
    )
