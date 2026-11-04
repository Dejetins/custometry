"""Receipt-root HTTP composition with genuine customer-event history membership."""

from uuid import UUID
from fastapi import Request
from custometry_api.config import Settings
from custometry_api.database import connection_factory
from custometry_api.identity.http_auth import IdentityHTTPAdapter
from custometry_api.analytics.customer_events import build_customer_events, customer_event_catalog
from custometry_api.analytics.cohort_access import PublishedReceiptCohortAccess
from custometry_api.analytics.customer_event_access import PublishedCustomerEventAccess
from packages.semantic_model.infrastructure.postgres import PostgresSalesSemanticRepository
from packages.analytics_core.infrastructure.relational_filters import DuckDBRelationalFilter
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.receipt_cohorts import ReceiptCohortGrant, CohortCatalogResponse


def build_cohort_filters(
    settings: Settings, auth: IdentityHTTPAdapter, request: Request, *, require_run: bool
) -> DuckDBRelationalFilter:
    base = build_customer_events(settings, auth, request, require_run=require_run)
    assert isinstance(base.access, PublishedCustomerEventAccess)
    access = PublishedReceiptCohortAccess(
        base.access, PostgresSalesSemanticRepository(connection_factory(settings))
    )
    return DuckDBRelationalFilter(artifact_root=settings.analytics_artifact_root, access=access)


def cohort_catalog(
    settings: Settings,
    auth: IdentityHTTPAdapter,
    request: Request,
    workspace: UUID,
    actor: UUID,
    dataset: UUID,
    search: str,
) -> CohortCatalogResponse:
    base = build_customer_events(settings, auth, request, require_run=False)
    source = customer_event_catalog(base, workspace, actor, dataset, search)
    engine = build_cohort_filters(settings, auth, request, require_run=False)
    grant = engine.access.authorize(
        workspace_id=workspace, actor_id=actor, dataset_version_id=dataset
    )
    if (
        not isinstance(grant, ReceiptCohortGrant)
        or source.registry_versions
        != {e.registry.entity: e.registry.version_id for e in grant.entities}
        or source.mandatory_expressions
        != {e.registry.entity: e.row_ceiling for e in grant.entities}
        or source.universe != grant.root_restrictions[0]
    ):
        raise AnalyticsFailure("FILTER_POLICY_CHANGED")
    return CohortCatalogResponse(
        **source.model_dump(exclude={"schema_version", "root_entity"}),
        facet_field_ids={
            entity: tuple(field for owner, field in grant.facet_fields if owner == entity)
            for entity in ("Receipt", "ReceiptItem")
        },
        receipt_registry_versions=dict(grant.receipt_registry_versions),
        legacy_registry_version_id=grant.compatibility_registry_versions[0],
    )
