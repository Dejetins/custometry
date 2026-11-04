"""Authenticated aggregate catalog and report executor composition."""

from uuid import UUID
from fastapi import Request
from custometry_api.config import Settings
from custometry_api.database import connection_factory
from custometry_api.identity.http_auth import IdentityHTTPAdapter
from custometry_api.analytics.relational_filters import build_relational_filters, relational_catalog
from custometry_api.analytics.aggregate_access import PublishedRetailAggregateAccess
from packages.semantic_model.infrastructure.postgres import PostgresSalesSemanticRepository
from packages.analytics_core.infrastructure.relational_filters import DuckDBRelationalFilter
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.aggregate_filters import AggregateInputGrant
from packages.contracts.analytics.retail_aggregate import AggregateCatalogResponse, CatalogCount
from packages.contracts.analytics.retail_filter import FilterLabels


def build_aggregate_filters(
    settings: Settings, auth: IdentityHTTPAdapter, request: Request
) -> DuckDBRelationalFilter:
    base = build_relational_filters(settings, auth, request)
    access = PublishedRetailAggregateAccess(
        base.access, PostgresSalesSemanticRepository(connection_factory(settings))
    )
    return DuckDBRelationalFilter(artifact_root=settings.analytics_artifact_root, access=access)


def aggregate_catalog(
    engine: DuckDBRelationalFilter, workspace: UUID, actor: UUID, dataset: UUID, search: str
) -> AggregateCatalogResponse:
    grant = engine.access.authorize(
        workspace_id=workspace, actor_id=actor, dataset_version_id=dataset
    )
    if not isinstance(grant, AggregateInputGrant):
        raise AnalyticsFailure("FILTER_AGGREGATE_CAPABILITY")
    base = relational_catalog(engine, workspace, actor, dataset, search)
    counts: list[CatalogCount] = []
    for c in grant.counts:
        label = FilterLabels(
            ru="Число наблюдаемых позиций"
            if c.definition.kind == "count"
            else "Число разных наблюдаемых товаров",
            en="Observed item count"
            if c.definition.kind == "count"
            else "Distinct observed product count",
        )
        if search.casefold() in " ".join((c.definition.count_id, label.ru, label.en)).casefold():
            counts.append(
                CatalogCount(
                    definition=c.definition,
                    observation=c.observation,
                    evidence_hash=c.evidence_hash,
                    label=label,
                )
            )
    if (
        engine.access.authorize(workspace_id=workspace, actor_id=actor, dataset_version_id=dataset)
        != grant
    ):
        raise AnalyticsFailure("FILTER_POLICY_CHANGED")
    return AggregateCatalogResponse(
        **base.model_dump(exclude={"schema_version", "limitation_codes"}),
        counts=tuple(counts),
        limitation_codes=(
            *base.limitation_codes,
            *(("AGGREGATE_NO_CLOSED_UTC_DAY",) if not grant.counts else ()),
        ),
    )
