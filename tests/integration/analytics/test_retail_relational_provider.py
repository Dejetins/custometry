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
from packages.contracts.analytics.columnar_filters import FilterValue
from packages.contracts.analytics.retail_relational import RelationalFacetQuery
from packages.contracts.analytics.relational_filters import (
    RelationalFilterRequest,
    ScopedPredicate,
    ScopedBoolean,
    CorrelatedExists,
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


def test_published_correlated_membership_http_and_current_policy(tmp_path, monkeypatch):
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
    engine = DuckDBRelationalFilter(artifact_root=artifact_root, access=access)
    grant = access.authorize(
        workspace_id=workspace, actor_id=actor.principal_id, dataset_version_id=dataset
    )
    assert not grant.relationships[0].complete
    assert len(grant.relationships[0].completeness_hash) == 64
    scope, child = uuid4(), uuid4()
    fields = {f.field_id: f for e in grant.entities for f in e.registry.fields}

    def predicate(name, value, op):
        f = fields[f"ReceiptItem.{name}"]
        return ScopedPredicate(
            node_id=uuid4(),
            scope_id=child,
            field_id=f.field_id,
            field_version_id=f.version_id,
            operator=op,
            values=(FilterValue(data_type=f.data_type, value=value),),
        )

    relation = grant.relationships[0].relationship
    node = CorrelatedExists(
        node_id=uuid4(),
        scope_id=scope,
        parent_scope_id=scope,
        child_scope_id=child,
        child_entity="ReceiptItem",
        relationship_id=relation.relationship_id,
        relationship_version_id=relation.version_id,
        kind="exists",
        predicate=ScopedBoolean(
            node_id=uuid4(),
            scope_id=child,
            kind="and",
            children=(predicate("quantity", "2.000", "ge"), predicate("unit_price", "10.00", "gt")),
        ),
    )
    query = RelationalFilterRequest(
        workspace_id=workspace,
        dataset_version_id=dataset,
        root_entity="Receipt",
        root_scope_id=scope,
        registry_versions={e.registry.entity: e.registry.version_id for e in grant.entities},
        expression=node,
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
        # Quality publication excludes orphan products; inner join is independent
        # source SQL reproducing that eligibility, not executor-generated SQL.
        oracle = """SELECT r.receipt_id::text,r.store_id FROM retail.receipts r WHERE EXISTS
            (SELECT 1 FROM retail.receipt_items i JOIN retail.products p ON p.product_id=i.product_id
             WHERE i.receipt_id=r.receipt_id AND i.quantity>=2.000 AND i.unit_price>10.00)
            ORDER BY r.receipt_id::text"""
        expected = source.execute(oracle).fetchall()
        facet_oracle = source.execute(f"""WITH matched AS ({oracle})
            SELECT m.store_id,i.quantity::text,count(*) FROM matched m
            JOIN retail.receipt_items i ON i.receipt_id::text=m.receipt_id
            JOIN retail.products p ON p.product_id=i.product_id
            GROUP BY m.store_id,i.quantity ORDER BY i.quantity::text""").fetchall()
        totals = dict(
            source.execute(
                "SELECT store_id,count(*) FROM retail.receipts GROUP BY store_id"
            ).fetchall()
        )
    actual = execute()
    assert expected and actual.matched_ids == tuple(r[0] for r in expected)
    assert actual.authorized_count == sum(totals.values())
    assert actual.not_matched_count == 0
    assert actual.unknown_count == actual.authorized_count - len(expected) > 0
    assert actual.limitation_codes == ("RELATIONSHIP_HISTORY_INCOMPLETE",)
    facet = RelationalFacetQuery(entity="ReceiptItem", field_id="ReceiptItem.quantity", limit=50)
    expected_facets: dict[str, int] = {}
    for _, value, count in facet_oracle:
        expected_facets[value] = expected_facets.get(value, 0) + count
    actual_facets = engine.facets(query, facet, actor_id=actor.principal_id)
    assert {v.value: v.count for v in actual_facets.values} == expected_facets
    assert actual_facets.count_grain == "observed_items_in_matching_receipts"
    negative = execute(
        query.model_copy(update={"expression": node.model_copy(update={"kind": "not_exists"})})
    )
    assert negative.matched_ids == () and negative.not_matched_count == len(expected)
    assert negative.unknown_count == actual.unknown_count

    app = create_reports_app(settings, identity_service=identity)
    body = dict(
        dataset_version_id=str(dataset),
        filter=dict(
            schema_version="receipt-filter/v2",
            root_scope_id=str(scope),
            registry_versions={k: str(v) for k, v in query.registry_versions.items()},
            expression=node.model_dump(mode="json"),
        ),
    )
    path = "/composer/v1/filters/v2"
    with TestClient(app) as client:
        assert client.get(f"{path}/{dataset}/catalog").status_code == 401
        headers = {"Authorization": f"Bearer {token.access_token}"}
        catalog = client.get(f"{path}/{dataset}/catalog", headers=headers)
        assert catalog.status_code == 200, catalog.json().get("code")
        payload = catalog.json()
        assert payload["registry_versions"] == body["filter"]["registry_versions"]
        assert len(payload["fields"]) == 14 and payload["relationships"][0]["complete"] is False
        assert payload["child_authorization"] == "inherits_correlated_receipt_store_ceiling"
        assert (
            client.get(f"{path}/{dataset}/catalog?search=Количество", headers=headers).json()[
                "fields"
            ][0]["field"]["field_id"]
            == "ReceiptItem.quantity"
        )
        preview = client.post(f"{path}/preview", json=body, headers=headers)
        assert preview.status_code == 200, preview.json().get("code")
        p = preview.json()
        assert p["matched_count"] == len(expected) and p["unknown_count"] == actual.unknown_count
        assert set(p) == {
            "schema_version",
            "request_hash",
            "matched_count",
            "not_matched_count",
            "unknown_count",
            "authorized_count",
            "preview_kind",
            "limitation_codes",
        }
        assert preview.headers["cache-control"] == "no-store"
        assert (
            client.post("/composer/v1/filters/preview", json=body, headers=headers).status_code
            == 422
        )
        for extra in (
            {"workspace_id": str(uuid4())},
            {"root_entity": "ReceiptItem"},
            {"sql": "SELECT *"},
        ):
            assert (
                client.post(f"{path}/preview", json={**body, **extra}, headers=headers).status_code
                == 422
            )
        wrong = {
            **body,
            "filter": {**body["filter"], "registry_versions": {"Receipt": str(uuid4())}},
        }
        invalid = client.post(f"{path}/preview", json=wrong, headers=headers)
        assert invalid.status_code == 400 and invalid.json()["code"] == "FILTER_REGISTRY_BINDING"
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
    assert scoped.matched_ids == tuple(r[0] for r in expected if r[1] == 1)
    assert scoped.authorized_count == totals[1]
    assert {
        v.value: v.count for v in engine.facets(query, facet, actor_id=actor.principal_id).values
    } == {value: count for store, value, count in facet_oracle if store == 1}
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

    # A GET catalog is checked again after projection, bypassing per-request auth
    # memoization. Revoke the actual session at that delivery boundary.
    original_projection = PostgresSalesSemanticRepository.retail_relational_projection
    revoked = False

    def revoke_after_projection(self, **kwargs):
        nonlocal revoked
        result = original_projection(self, **kwargs)
        if not revoked:
            revoked = True
            identity.revoke_session(actor, token.session_id)
        return result

    monkeypatch.setattr(
        PostgresSalesSemanticRepository, "retail_relational_projection", revoke_after_projection
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
        PostgresSalesSemanticRepository, "retail_relational_projection", original_projection
    )
    with pytest.raises(IdentityFailure):
        execute()
