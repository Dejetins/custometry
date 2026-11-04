"""Authenticated catalog/executor composition for observed customer receipt events."""

from uuid import UUID, uuid5
from fastapi import Request
from custometry_api.config import Settings
from custometry_api.database import connection_factory
from custometry_api.identity.http_auth import IdentityHTTPAdapter
from custometry_api.analytics.relational_filters import relational_resource_policy, ITEM_LABELS
from custometry_api.analytics.retail_filters import LABELS
from custometry_api.analytics.customer_event_access import PublishedCustomerEventAccess
from packages.identity_access.application.resource_access import ResourceAccessService
from packages.identity_access.infrastructure.resource_access import PostgresResourceAccessRepository
from packages.semantic_model.infrastructure.postgres import PostgresSalesSemanticRepository
from packages.artifacts.infrastructure.sales import SalesArtifactStore
from packages.analytics_core.infrastructure.relational_filters import DuckDBRelationalFilter
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.relational_filters import RelationalResourcePolicy
from packages.contracts.analytics.customer_events import (
    RootRestrictedSequenceGrant,
    CustomerEventCatalog,
    CustomerEventRelationship,
    CatalogEvent,
)
from packages.contracts.analytics.retail_filter import CatalogField, FilterLabels
from packages.contracts.analytics.retail_aggregate import CatalogCount

LIMITATIONS = (
    "OBSERVED_CUSTOMER_UNIVERSE",
    "CURRENT_DIMENSION_HISTORY_ONLY",
    "EVENT_HISTORY_UNCERTIFIED",
    "RELATIONSHIP_HISTORY_INCOMPLETE",
)


def customer_event_resource_policy(settings: Settings) -> RelationalResourcePolicy:
    policy = relational_resource_policy(settings)
    return policy.model_copy(
        update={"max_entities": 3, "version_id": uuid5(policy.version_id, "customer-events/v1:3")}
    )


def build_customer_events(
    settings: Settings, auth: IdentityHTTPAdapter, request: Request, *, require_run: bool
) -> DuckDBRelationalFilter:
    connect = connection_factory(settings)

    def current_actor():
        if hasattr(request.state, "identity_actor"):
            delattr(request.state, "identity_actor")
        return auth.authenticate(request)

    access = PublishedCustomerEventAccess(
        identity=ResourceAccessService(PostgresResourceAccessRepository(connect), current_actor),
        semantics=PostgresSalesSemanticRepository(connect),
        artifacts=SalesArtifactStore(connect, settings.analytics_artifact_root),
        resource_policy=customer_event_resource_policy(settings),
        require_run=require_run,
    )
    return DuckDBRelationalFilter(artifact_root=settings.analytics_artifact_root, access=access)


def customer_event_catalog(
    engine: DuckDBRelationalFilter, workspace: UUID, actor: UUID, dataset: UUID, search: str
) -> CustomerEventCatalog:
    grant = engine.access.authorize(
        workspace_id=workspace, actor_id=actor, dataset_version_id=dataset
    )
    if not isinstance(grant, RootRestrictedSequenceGrant) or len(grant.root_restrictions) != 1:
        raise AnalyticsFailure("FILTER_CUSTOMER_EVENT_BINDING")
    labels = (
        LABELS
        | ITEM_LABELS
        | {
            "customer_id": ("Идентификатор клиента", "Customer ID"),
            "customer_version_id": ("Версия клиента", "Customer version ID"),
        }
    )
    fields: list[CatalogField] = []
    for entity in grant.entities:
        for f in entity.registry.fields:
            ru, en = labels[f.column]
            description = FilterLabels(
                ru=f"Опубликованное поле {f.entity}: {ru}", en=f"Published {f.entity} field: {en}"
            )
            if (
                search.casefold()
                in " ".join(
                    (f.field_id, f.entity, f.data_type, ru, en, description.ru, description.en)
                ).casefold()
            ):
                fields.append(
                    CatalogField(field=f, label=FilterLabels(ru=ru, en=en), description=description)
                )
    events = tuple(
        CatalogEvent(
            definition=e.definition,
            observation=e.observation,
            complete=e.complete,
            evidence_hash=e.evidence_hash,
            label=FilterLabels(ru="Наблюдаемый чек", en="Observed receipt"),
            description=FilterLabels(
                ru="Опубликованный чек по записанному времени UTC. Текущие свойства; полнота истории не подтверждена.",
                en="Published receipt at recorded UTC time. Current properties; history is not certified.",
            ),
        )
        for e in grant.events
        if search.casefold()
        in " ".join((e.definition.event_id, "Наблюдаемый чек Observed receipt")).casefold()
    )
    counts = tuple(
        CatalogCount(
            definition=c.definition,
            observation=c.observation,
            evidence_hash=c.evidence_hash,
            label=FilterLabels(
                ru="Число наблюдаемых позиций"
                if c.definition.kind == "count"
                else "Число разных наблюдаемых товаров",
                en="Observed item count"
                if c.definition.kind == "count"
                else "Distinct observed product count",
            ),
        )
        for c in grant.counts
        if search.casefold()
        in " ".join(
            (
                c.definition.count_id,
                "Число наблюдаемых позиций товаров Observed item count Distinct product count",
            )
        ).casefold()
    )
    if (
        engine.access.authorize(workspace_id=workspace, actor_id=actor, dataset_version_id=dataset)
        != grant
    ):
        raise AnalyticsFailure("FILTER_POLICY_CHANGED")
    return CustomerEventCatalog(
        dataset_version_id=dataset,
        registry_versions={e.registry.entity: e.registry.version_id for e in grant.entities},
        fields=fields,
        relationships=[
            CustomerEventRelationship(
                relationship=r.relationship,
                label=FilterLabels(
                    ru="Чеки клиента"
                    if r.relationship.parent_entity == "Customer"
                    else "Позиции чека",
                    en="Customer receipts"
                    if r.relationship.parent_entity == "Customer"
                    else "Receipt items",
                ),
                complete=r.complete,
                completeness_hash=r.completeness_hash,
            )
            for r in grant.relationships
        ],
        events=events,
        counts=counts,
        mandatory_expressions={e.registry.entity: e.row_ceiling for e in grant.entities},
        universe=grant.root_restrictions[0],
        resource_policy_version_id=grant.resource_policy.version_id,
        limitation_codes=LIMITATIONS,
    )
