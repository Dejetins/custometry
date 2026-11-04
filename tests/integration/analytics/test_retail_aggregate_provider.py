"""Genuine disposable publication, current policy, HTTP auth and independent SQL."""

from __future__ import annotations
import importlib.util
import json
import os
from pathlib import Path
from uuid import UUID, uuid4
import psycopg
import pytest
from fastapi.testclient import TestClient
from custometry_api.analytics.relational_access import PublishedRetailRelationalAccess
from custometry_api.analytics.relational_filters import relational_resource_policy
from custometry_api.config import Settings
from custometry_api.reports.router import create_reports_app
from packages.analytics_core.infrastructure.relational_filters import DuckDBRelationalFilter
from packages.artifacts.infrastructure.sales import SalesArtifactStore
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.retail_relational import RelationalFacetQuery
from packages.contracts.analytics.relational_filters import (
    ScopedPredicate,
)
from packages.identity_access.application.organization import OrganizationService
from packages.identity_access.application.resource_access import ResourceAccessService
from packages.identity_access.application.service import IdentityFailure, IdentityService
from packages.identity_access.infrastructure.organization_postgres import (
    PostgresOrganizationRepository,
)
from packages.identity_access.infrastructure.postgres import PostgresIdentityRepository
from packages.identity_access.infrastructure.resource_access import PostgresResourceAccessRepository
from packages.semantic_model.infrastructure.postgres import PostgresSalesSemanticRepository

ROOT = Path(__file__).resolve().parents[3]


def test_published_aggregate_provider_http_and_current_policy(tmp_path, monkeypatch):
    if os.environ.get("MS010_OWNED_DATABASE") != "1":
        pytest.skip("requires owned run_retail_filters disposable database")
    corpus_path = tmp_path / "corpus.json"
    monkeypatch.setenv("MS004_S04_CORPUS_OUT", str(corpus_path))
    spec = importlib.util.spec_from_file_location(
        "correlated_scenario", ROOT / "tests/e2e/ms-004-workspace/scenario.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    artifact_root = tmp_path / "artifacts"
    module.create_scenario(artifact_root)
    corpus = json.loads(corpus_path.read_text())
    workspace, dataset = UUID(corpus["workspace_id"]), UUID(corpus["semantic_dataset_version_id"])
    settings = Settings(analytics_artifact_root=artifact_root)

    def connect():
        return psycopg.connect(
            host=settings.database_host,
            port=settings.database_port,
            dbname=settings.database_name,
            user=settings.database_user,
            password=settings.read_database_password(),
        )

    identity = IdentityService(
        PostgresIdentityRepository(connect), bootstrap_secret="synthetic-bootstrap"
    )

    def login():
        return identity.login(
            workspace_id=workspace,
            email="author@example.test",
            password="synthetic-author-password",
            device_label="MS018 disposable provider",
        )

    token = login()
    actor = identity.authenticate(token.access_token)
    semantics = PostgresSalesSemanticRepository(connect)
    access = PublishedRetailRelationalAccess(
        identity=ResourceAccessService(
            PostgresResourceAccessRepository(connect),
            lambda: identity.authenticate(token.access_token),
        ),
        semantics=semantics,
        artifacts=SalesArtifactStore(connect, artifact_root),
        resource_policy=relational_resource_policy(settings),
    )
    from custometry_api.analytics.aggregate_access import PublishedRetailAggregateAccess
    from packages.contracts.analytics.aggregate_filters import (
        AggregateFilterRequest,
        ScopedCount,
        AggregateWindow,
        AggregateCompare,
        AggregateScalar,
    )
    from packages.contracts.analytics.retail_aggregate import AggregateReceiptFilterInput

    access = PublishedRetailAggregateAccess(access, semantics)
    engine = DuckDBRelationalFilter(artifact_root=artifact_root, access=access)
    grant = access.authorize(
        workspace_id=workspace, actor_id=actor.principal_id, dataset_version_id=dataset
    )
    scope, child = uuid4(), uuid4()
    definition = grant.counts[0].definition
    fields = {f.field_id: f for e in grant.entities for f in e.registry.fields}
    field = fields["ReceiptItem.line_id"]
    edge = grant.relationships[0].relationship
    left = ScopedCount(
        parent_scope_id=scope,
        child_scope_id=child,
        child_entity="ReceiptItem",
        relationship_id=edge.relationship_id,
        relationship_version_id=edge.version_id,
        definition=definition,
        window=AggregateWindow(**grant.counts[0].observation.model_dump(), timezone="UTC"),
        predicate=ScopedPredicate(
            node_id=uuid4(),
            scope_id=child,
            field_id=field.field_id,
            field_version_id=field.version_id,
            operator="is_not_null",
        ),
    )
    node = AggregateCompare(
        node_id=uuid4(),
        scope_id=scope,
        left=left,
        operator="ge",
        right=AggregateScalar(value="1", unit=definition.unit),
    )
    query = AggregateFilterRequest(
        workspace_id=workspace,
        dataset_version_id=dataset,
        root_entity="Receipt",
        root_scope_id=scope,
        registry_versions={e.registry.entity: e.registry.version_id for e in grant.entities},
        expression=node,
        compatibility_registry_version_id=grant.compatibility_registry_versions[0],
    )

    def execute(q=query):
        return engine.execute(q, actor_id=actor.principal_id)

    with psycopg.connect(
        host=os.environ["CUSTOMETRY_TEST_SOURCE_HOST"],
        port=os.environ["CUSTOMETRY_TEST_SOURCE_PORT"],
        dbname=os.environ["CUSTOMETRY_TEST_SOURCE_DATABASE"],
        user=os.environ["CUSTOMETRY_TEST_SOURCE_USER"],
        password=Path(os.environ["CUSTOMETRY_TEST_SOURCE_PASSWORD_FILE"]).read_text().strip(),
    ) as source:
        source.execute("SET TRANSACTION READ ONLY")
        totals = dict(
            source.execute(
                "SELECT store_id,count(*) FROM retail.receipts GROUP BY store_id"
            ).fetchall()
        )
        observed = source.execute(
            "SELECT count(*),count(DISTINCT i.product_id) FROM retail.receipt_items i JOIN retail.products p ON p.product_id=i.product_id"
        ).fetchone()
    assert observed[0] > 0 and observed[1] > 0
    actual = execute()
    assert (
        actual.authorized_count == sum(totals.values())
        and actual.unknown_count == actual.authorized_count
    )
    assert actual.matched_ids == () and actual.not_matched_count == 0
    assert "RELATIONSHIP_HISTORY_INCOMPLETE" in actual.limitation_codes
    assert "AGGREGATE_VALUE_UNAVAILABLE" in actual.limitation_codes
    assert (
        engine.facets(
            query,
            RelationalFacetQuery(entity="ReceiptItem", field_id="ReceiptItem.product_id"),
            actor_id=actor.principal_id,
        ).values
        == []
    )
    value = AggregateReceiptFilterInput(
        root_scope_id=scope,
        registry_versions=query.registry_versions,
        expression=node,
        legacy_registry_version_id=grant.compatibility_registry_versions[0],
    )
    body = dict(dataset_version_id=str(dataset), filter=value.model_dump(mode="json"))
    path = "/composer/v1/filters/v3"
    app = create_reports_app(settings, identity_service=identity)
    with TestClient(app) as client:
        assert client.get(f"{path}/{dataset}/catalog").status_code == 401
        headers = {"Authorization": f"Bearer {token.access_token}"}
        response = client.get(f"{path}/{dataset}/catalog", headers=headers)
        assert response.status_code == 200, response.json().get("code")
        catalog = response.json()
        assert len(catalog["counts"]) == 2 and catalog["relationships"][0]["complete"] is False
        assert catalog["counts"][0]["observation"] == grant.counts[0].observation.model_dump(
            mode="json"
        )
        assert (
            len(
                client.get(f"{path}/{dataset}/catalog?search=not-a-published-count", headers=headers).json()[
                    "counts"
                ]
            )
            == 0
        )
        assert (
            len(
                client.get(f"{path}/{dataset}/catalog?search=Distinct", headers=headers).json()[
                    "counts"
                ]
            )
            == 1
        )
        preview = client.post(f"{path}/preview", json=body, headers=headers)
        assert preview.status_code == 200, preview.json().get("code")
        assert (
            preview.json()["unknown_count"] == sum(totals.values())
            and preview.json()["matched_count"] == 0
        )
        assert preview.headers["cache-control"] == "no-store"
        assert "matched_ids" not in preview.json() and "artifact" not in preview.text
        assert (
            client.post("/composer/v1/filters/v2/preview", json=body, headers=headers).status_code
            == 422
        )
        assert (
            client.post(
                f"{path}/preview", json={**body, "workspace_id": str(uuid4())}, headers=headers
            ).status_code
            == 422
        )
        bad = json.loads(json.dumps(body))
        bad["filter"]["expression"]["left"]["definition"]["unit"] = "forged"
        denied = client.post(f"{path}/preview", json=bad, headers=headers)
        assert denied.status_code == 400 and denied.json()["code"] == "FILTER_AGGREGATE_BINDING"
        facet = client.post(
            f"{path}/facets",
            json={**body, "facet": {"entity": "ReceiptItem", "field_id": "ReceiptItem.product_id"}},
            headers=headers,
        )
        assert facet.status_code == 200 and facet.json()["values"] == []
        client.cookies.set("custometry_access", token.access_token)
        assert client.post(f"{path}/preview", json=body).status_code == 403
        assert (
            client.post(
                f"{path}/preview",
                json=body,
                headers={
                    "Origin": settings.cors_allowed_origins[0],
                    "X-CSRF-Token": token.csrf_token,
                },
            ).status_code
            == 200
        )
    organization = OrganizationService(PostgresOrganizationRepository(connect))

    def bind(stores):
        with connect() as connection:
            policy_id, department, version = connection.execute(
                "SELECT id,org_unit_id,current_version FROM organization_department_policies WHERE workspace_id=%s",
                (workspace,),
            ).fetchone()
        draft = organization.create_policy_draft(
            actor,
            policy_id=policy_id,
            org_unit_id=department,
            expected_version=version,
            allowed_actions=("view_snapshot", "run", "edit"),
            row_scope_refs=stores,
            column_policy_refs=(),
            pii_allowed=False,
            include_descendants=True,
            effective_from=None,
        )
        organization.publish_policy(
            actor, policy_id=policy_id, expected_version=int(draft["version"]), effective_from=None
        )
        organization.bind_resource(
            actor,
            resource_type="analysis",
            resource_id=dataset,
            creator_principal_id=actor.principal_id,
            owner_type="principal",
            owner_id=actor.principal_id,
            allowed_actions=("view_snapshot", "run", "edit"),
            required_row_scope_refs=stores,
            required_column_policy_refs=(),
            requires_pii=False,
            effective_from=None,
        )

    bind(("store:1",))
    scoped = execute()
    assert scoped.unknown_count == scoped.authorized_count == totals[1]
    assert scoped.request_hash != actual.request_hash
    bind(("store:absent",))
    assert execute().authorized_count == 0
    with pytest.raises(AnalyticsFailure, match="FORBIDDEN"):
        execute(query.model_copy(update={"workspace_id": uuid4()}))
    import packages.analytics_core.infrastructure.relational_filters as adapter

    original_read = adapter.read_admitted_input
    changed = False

    def change_after_read(*args, **kwargs):
        nonlocal changed
        result = original_read(*args, **kwargs)
        if not changed:
            changed = True
            bind(("store:1",))
        return result

    monkeypatch.setattr(adapter, "read_admitted_input", change_after_read)
    with pytest.raises(AnalyticsFailure, match="FILTER_POLICY_CHANGED"):
        execute()
    monkeypatch.setattr(adapter, "read_admitted_input", original_read)
    original_projection = PostgresSalesSemanticRepository.retail_aggregate_projection
    revoked = False

    def revoke_after_projection(self, **kwargs):
        nonlocal revoked
        result = original_projection(self, **kwargs)
        if not revoked:
            revoked = True
            identity.revoke_session(actor, token.session_id)
        return result

    monkeypatch.setattr(
        PostgresSalesSemanticRepository, "retail_aggregate_projection", revoke_after_projection
    )
    with TestClient(app) as client:
        assert (
            client.get(
                f"{path}/{dataset}/catalog",
                headers={"Authorization": f"Bearer {token.access_token}"},
            ).status_code
            == 401
        )
    monkeypatch.setattr(
        PostgresSalesSemanticRepository, "retail_aggregate_projection", original_projection
    )
    with pytest.raises(IdentityFailure):
        execute()
