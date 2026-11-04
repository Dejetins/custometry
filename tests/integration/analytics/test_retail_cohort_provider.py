"""Genuine disposable publication, current policy, HTTP auth and independent SQL."""

from __future__ import annotations
import importlib.util
import json
import os
from pathlib import Path
from typing import Any, cast
from uuid import UUID, uuid4
import psycopg
import pytest
from fastapi.testclient import TestClient
from custometry_api.analytics.customer_event_access import PublishedCustomerEventAccess
from custometry_api.analytics.customer_events import customer_event_resource_policy
from custometry_api.analytics.cohort_access import PublishedReceiptCohortAccess
from packages.contracts.analytics.receipt_cohorts import (
    CohortFilterRequest,
    CohortReceiptFilterInput,
    CustomerEventMembership,
)
from custometry_api.config import Settings
from custometry_api.reports.router import create_reports_app
from packages.analytics_core.infrastructure.relational_filters import DuckDBRelationalFilter
from packages.artifacts.infrastructure.sales import SalesArtifactStore
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.semantic.nullable_relationships import NullableFilterRelationshipVersion
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

def _count(row: tuple[Any, ...] | None) -> int:
    assert row is not None
    return cast(int, row[0])


ROOT = Path(__file__).resolve().parents[3]


def test_published_receipt_cohort_http_and_current_policy(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    if os.environ.get("MS010_OWNED_DATABASE") != "1":
        pytest.skip("requires owned run_retail_filters disposable database")
    corpus_path = tmp_path / "corpus.json"
    monkeypatch.setenv("MS004_S04_CORPUS_OUT", str(corpus_path))
    spec = importlib.util.spec_from_file_location(
        "correlated_scenario", ROOT / "tests/e2e/ms-004-workspace/scenario.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    artifact_root = tmp_path / "artifacts"
    module.create_scenario(artifact_root)
    corpus = json.loads(corpus_path.read_text())
    workspace, dataset = UUID(corpus["workspace_id"]), UUID(corpus["semantic_dataset_version_id"])
    settings = Settings(analytics_artifact_root=artifact_root)

    def connect() -> psycopg.Connection[Any]:
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
            device_label="MS024 disposable provider",
        )

    token = login()
    actor = identity.authenticate(token.access_token)
    semantics = PostgresSalesSemanticRepository(connect)
    access = PublishedCustomerEventAccess(
        identity=ResourceAccessService(
            PostgresResourceAccessRepository(connect),
            lambda: identity.authenticate(token.access_token),
        ),
        semantics=semantics,
        artifacts=SalesArtifactStore(connect, artifact_root),
        resource_policy=customer_event_resource_policy(settings),
    )
    access = PublishedReceiptCohortAccess(access, semantics)
    engine = DuckDBRelationalFilter(artifact_root=artifact_root, access=access)
    grant = access.authorize(
        workspace_id=workspace, actor_id=actor.principal_id, dataset_version_id=dataset
    )
    from packages.contracts.analytics.sequence_filters import (
        BehavioralSequence,
        PositiveStep,
        NegativeStep,
        SequenceGap,
        FixedSequenceWindow,
    )
    from packages.contracts.analytics.columnar_filters import FilterValue

    scope = uuid4()
    edge = grant.relationships[0].relationship
    event = grant.events[0]
    status = next(
        f for e in grant.entities for f in e.registry.fields if f.field_id == "Receipt.status"
    )

    def step(gap: SequenceGap | None = None, value: str = "completed") -> PositiveStep:
        child = uuid4()
        return PositiveStep(
            step_id=uuid4(),
            child_scope_id=child,
            event=event.definition,
            predicate=ScopedPredicate(
                node_id=uuid4(),
                scope_id=child,
                field_id=status.field_id,
                field_version_id=status.version_id,
                operator="eq",
                values=(FilterValue(data_type="string", value=value),),
            ),
            gap=gap,
        )

    first = step()
    second = step(SequenceGap(maximum_us=31536000000000))
    node = BehavioralSequence(
        node_id=uuid4(),
        scope_id=scope,
        parent_scope_id=scope,
        relationship_id=edge.relationship_id,
        relationship_version_id=edge.version_id,
        child_entity="Receipt",
        window=FixedSequenceWindow(**event.observation.model_dump()),
        steps=(first, second),
    )
    receipt_scope = uuid4()
    membership = CustomerEventMembership(
        node_id=uuid4(),
        scope_id=receipt_scope,
        customer_scope_id=scope,
        relationship_id=edge.relationship_id,
        relationship_version_id=edge.version_id,
        predicate=node,
    )
    query = CohortFilterRequest(
        workspace_id=workspace,
        dataset_version_id=dataset,
        root_entity="Receipt",
        root_scope_id=receipt_scope,
        receipt_registry_versions=dict(grant.receipt_registry_versions),
        registry_versions={e.registry.entity: e.registry.version_id for e in grant.entities},
        expression=membership,
    )

    def execute(q: CohortFilterRequest = query):
        return engine.execute(q, actor_id=actor.principal_id)

    with psycopg.connect(
        host=os.environ["CUSTOMETRY_TEST_SOURCE_HOST"],
        port=os.environ["CUSTOMETRY_TEST_SOURCE_PORT"],
        dbname=os.environ["CUSTOMETRY_TEST_SOURCE_DATABASE"],
        user=os.environ["CUSTOMETRY_TEST_SOURCE_USER"],
        password=Path(os.environ["CUSTOMETRY_TEST_SOURCE_PASSWORD_FILE"]).read_text().strip(),
    ) as source:
        source.execute("SET TRANSACTION READ ONLY")
        universe = _count(source.execute("SELECT count(*) FROM retail.receipts").fetchone())
        scoped_universe = _count(source.execute(
            "SELECT count(*) FROM retail.receipts WHERE store_id=1"
        ).fetchone())
        matched = _count(source.execute(
            "SELECT count(*) FROM retail.receipts r WHERE EXISTS (SELECT 1 FROM retail.receipts a JOIN retail.receipts b ON a.customer_id=b.customer_id AND b.receipt_datetime>a.receipt_datetime AND b.receipt_datetime-a.receipt_datetime<=interval '365 days' WHERE a.customer_id=r.customer_id AND a.status='completed' AND b.status='completed')"
        ).fetchone())
        scoped_matched = _count(source.execute(
            "SELECT count(*) FROM retail.receipts r WHERE r.store_id=1 AND EXISTS (SELECT 1 FROM retail.receipts a JOIN retail.receipts b ON a.customer_id=b.customer_id AND b.receipt_datetime>a.receipt_datetime AND b.receipt_datetime-a.receipt_datetime<=interval '365 days' WHERE a.customer_id=r.customer_id AND a.status='completed' AND b.status='completed' AND a.store_id=1 AND b.store_id=1)"
        ).fetchone())
        # Publication excludes orphan product references; source SQL independently
        # applies the same documented eligibility before counting admitted items.
        matched_items = _count(source.execute(
            "SELECT count(*) FROM retail.receipt_items i JOIN retail.products p ON p.product_id=i.product_id JOIN retail.receipts r ON i.receipt_id=r.receipt_id WHERE EXISTS (SELECT 1 FROM retail.receipts a JOIN retail.receipts b ON a.customer_id=b.customer_id AND b.receipt_datetime>a.receipt_datetime AND b.receipt_datetime-a.receipt_datetime<=interval '365 days' WHERE a.customer_id=r.customer_id AND a.status='completed' AND b.status='completed')"
        ).fetchone())
    actual = execute()
    assert actual.authorized_count == universe and len(actual.matched_ids) == matched > 0
    assert actual.unknown_count == universe - matched and actual.not_matched_count == 0
    assert event.complete is False and all(not r.complete for r in grant.relationships)
    assert isinstance(edge, NullableFilterRelationshipVersion)
    assert edge.nullable_child_fields == ("Receipt.customer_id",)
    missing = step(value="not-an-observed-status")
    negative = NegativeStep(
        step_id=missing.step_id,
        child_scope_id=missing.child_scope_id,
        event=missing.event,
        predicate=missing.predicate,
        after_step_id=first.step_id,
        ends_after_us=86400000000,
    )
    absent = execute(
        query.model_copy(
            update={
                "expression": membership.model_copy(
                    update={"predicate": node.model_copy(update={"steps": (first, negative)})}
                )
            }
        )
    )
    assert absent.matched_ids == () and absent.unknown_count == universe
    value = CohortReceiptFilterInput(
        root_scope_id=receipt_scope,
        registry_versions=query.registry_versions,
        receipt_registry_versions=query.receipt_registry_versions,
        expression=membership,
    )
    body = dict(dataset_version_id=str(dataset), filter=value.model_dump(mode="json"))
    path = "/composer/v1/filters/v4"
    app = create_reports_app(settings, identity_service=identity)
    headers = {"Authorization": f"Bearer {token.access_token}"}
    with TestClient(app) as client:
        assert client.get(f"{path}/{dataset}/catalog").status_code == 401
        response = client.get(f"{path}/{dataset}/catalog", headers=headers)
        assert response.status_code == 200, response.json().get("code")
        catalog = response.json()
        assert catalog["root_entity"] == "Receipt" and len(catalog["events"]) == 1
        assert catalog["relationships"][0]["relationship"]["nullable_child_fields"] == [
            "Receipt.customer_id"
        ]
        assert catalog["universe"] == grant.root_restrictions[0].model_dump(mode="json")
        assert catalog["events"][0]["observation"] == event.observation.model_dump(mode="json")
        assert not any(
            f["field"]["column"] in {"email", "phone", "name", "birth_date"}
            for f in catalog["fields"]
        )
        assert (
            client.get(f"{path}/{dataset}/catalog?search=not-published", headers=headers).json()[
                "events"
            ]
            == []
        )
        preview = client.post(f"{path}/preview", json=body, headers=headers)
        assert preview.status_code == 200, preview.json().get("code")
        assert (
            preview.json()["matched_count"] == matched
            and preview.json()["authorized_count"] == universe
        )
        assert preview.headers["cache-control"] == "no-store"
        assert "matched_ids" not in preview.json() and "artifact" not in preview.text
        assert (
            client.post(
                f"{path}/preview", json={**body, "workspace_id": str(uuid4())}, headers=headers
            ).status_code
            == 422
        )
        assert (
            client.post("/composer/v1/filters/v3/preview", json=body, headers=headers).status_code
            == 422
        )
        bad = json.loads(json.dumps(body))
        bad["filter"]["expression"]["predicate"]["steps"][0]["event"]["time_field"]["column"] = (
            "forged"
        )
        denial = client.post(f"{path}/preview", json=bad, headers=headers)
        assert denial.status_code == 400 and denial.json()["code"] == "FILTER_EVENT_BINDING"
        assert catalog["receipt_registry_versions"] == {
            k: str(v) for k, v in grant.receipt_registry_versions
        }
        facets = client.post(
            f"{path}/facets",
            json={
                **body,
                "facet": {
                    "entity": "Receipt",
                    "field_id": "Receipt.status",
                    "search": "",
                    "limit": 50,
                    "offset": 0,
                },
            },
            headers=headers,
        )
        assert facets.status_code == 200, facets.json().get("code")
        assert sum(v["count"] for v in facets.json()["values"]) == matched
        assert facets.json()["count_grain"] == "matching_receipts"
        item_facets = client.post(
            f"{path}/facets",
            json={
                **body,
                "facet": {
                    "entity": "ReceiptItem",
                    "field_id": "ReceiptItem.product_id",
                    "search": "",
                    "limit": 50,
                    "offset": 0,
                },
            },
            headers=headers,
        )
        assert item_facets.status_code == 200, item_facets.json().get("code")
        # Page all bounded distinct products, without returning customer memberships.
        total_items = sum(v["count"] for v in item_facets.json()["values"])
        offset = 50
        while item_facets.json()["has_more"]:
            item_facets = client.post(
                f"{path}/facets",
                json={
                    **body,
                    "facet": {
                        "entity": "ReceiptItem",
                        "field_id": "ReceiptItem.product_id",
                        "search": "",
                        "limit": 50,
                        "offset": offset,
                    },
                },
                headers=headers,
            )
            assert item_facets.status_code == 200, item_facets.json().get("code")
            total_items += sum(v["count"] for v in item_facets.json()["values"])
            offset += 50
            assert offset <= 1000
        assert total_items == matched_items
        assert item_facets.json()["count_grain"] == "observed_items_in_matching_receipts"
        denied_identity = client.post(
            f"{path}/facets",
            json={
                **body,
                "facet": {"entity": "Receipt", "field_id": "Receipt.customer_id", "limit": 10},
            },
            headers=headers,
        )
        assert (
            denied_identity.status_code == 400
            and denied_identity.json()["code"] == "FILTER_FIELD_FORBIDDEN"
        )
        assert "Receipt.customer_id" not in catalog["facet_field_ids"]["Receipt"]
        denied_facet = client.post(
            f"{path}/facets",
            json={
                **body,
                "facet": {
                    "entity": "Customer",
                    "field_id": "Customer.customer_id",
                    "search": "",
                    "limit": 10,
                    "offset": 0,
                },
            },
            headers=headers,
        )
        assert denied_facet.status_code == 422
        bad_bridge = json.loads(json.dumps(body))
        bad_bridge["filter"]["promoted_registry_sets"] = [{"Receipt": str(uuid4())}]
        denied_bridge = client.post(f"{path}/preview", json=bad_bridge, headers=headers)
        assert (
            denied_bridge.status_code == 400
            and denied_bridge.json()["code"] == "FILTER_COHORT_REGISTRY_BRIDGE"
        )
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

    def bind(stores: tuple[str, ...], actions: tuple[str, ...] = ("view_snapshot", "run", "edit")) -> None:
        with connect() as connection:
            row = connection.execute(
                "SELECT id,org_unit_id,current_version FROM organization_department_policies WHERE workspace_id=%s",
                (workspace,),
            ).fetchone()
        assert row is not None
        policy_id, department, version = cast(tuple[UUID, UUID, int], row)
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
            actor, policy_id=policy_id, expected_version=int(cast(int, draft["version"])), effective_from=None
        )
        organization.bind_resource(
            actor,
            resource_type="analysis",
            resource_id=dataset,
            creator_principal_id=actor.principal_id,
            owner_type="principal",
            owner_id=actor.principal_id,
            allowed_actions=actions,
            required_row_scope_refs=stores,
            required_column_policy_refs=(),
            requires_pii=False,
            effective_from=None,
        )

    bind(("store:1",))
    scoped = execute()
    assert scoped.authorized_count == scoped_universe and len(scoped.matched_ids) == scoped_matched
    assert scoped.request_hash != actual.request_hash
    bind(("store:absent",))
    assert execute().authorized_count == 0
    with pytest.raises(AnalyticsFailure, match="FORBIDDEN"):
        execute(query.model_copy(update={"workspace_id": uuid4()}))
    import packages.analytics_core.infrastructure.relational_filters as adapter

    original_read = adapter.read_admitted_input
    changed = False

    def change_after_read(*args: Any, **kwargs: Any) -> Any:
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
    bind(("store:1",), ("view_snapshot",))
    with TestClient(app) as client:
        assert client.get(f"{path}/{dataset}/catalog", headers=headers).status_code == 200
        assert client.post(f"{path}/preview", json=body, headers=headers).status_code == 403
    bind(("store:1",))
    original_bridge = PostgresSalesSemanticRepository.retail_aggregate_projection
    late_revoked = False

    def revoke_after_bridge(self: PostgresSalesSemanticRepository, **kwargs: Any) -> Any:
        nonlocal late_revoked
        result = original_bridge(self, **kwargs)
        if not late_revoked:
            late_revoked = True
            identity.revoke_session(actor, token.session_id)
        return result

    monkeypatch.setattr(
        PostgresSalesSemanticRepository, "retail_aggregate_projection", revoke_after_bridge
    )
    with TestClient(app) as client:
        assert client.get(f"{path}/{dataset}/catalog", headers=headers).status_code == 401
    assert late_revoked
    monkeypatch.setattr(
        PostgresSalesSemanticRepository, "retail_aggregate_projection", original_bridge
    )
    token = login()
    headers = {"Authorization": f"Bearer {token.access_token}"}
    original_projection = PostgresSalesSemanticRepository.customer_events_projection
    revoked = False

    def revoke_after_projection(self: PostgresSalesSemanticRepository, **kwargs: Any) -> Any:
        nonlocal revoked
        result = original_projection(self, **kwargs)
        if not revoked:
            revoked = True
            identity.revoke_session(actor, token.session_id)
        return result

    monkeypatch.setattr(
        PostgresSalesSemanticRepository, "customer_events_projection", revoke_after_projection
    )
    with TestClient(app) as client:
        assert client.get(f"{path}/{dataset}/catalog", headers=headers).status_code == 401
    monkeypatch.setattr(
        PostgresSalesSemanticRepository, "customer_events_projection", original_projection
    )
    with pytest.raises(IdentityFailure):
        execute()
