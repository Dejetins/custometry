"""Published provider proof on owned disposable control/source PostgreSQL only."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
from uuid import UUID, uuid4

import psycopg
import pytest

from custometry_api.analytics.filter_access import PublishedRetailFilterAccess
from custometry_api.config import Settings
from packages.analytics_core.infrastructure.columnar_filters import DuckDBFlatFilter
from packages.artifacts.infrastructure.sales import SalesArtifactStore
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.columnar_filters import (
    FilterResourcePolicy,
    FilterValue,
    FlatFilterRequest,
    FlatPredicate,
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


def test_published_retail_provider_current_policy_and_manifest(tmp_path, monkeypatch):
    if os.environ.get("MS010_OWNED_DATABASE") != "1":
        pytest.skip("requires run_retail_filters owned disposable database")
    # Reuse real intake/identity setup; no production row or permission fixture stub.
    corpus_path = tmp_path / "corpus.json"
    monkeypatch.setenv("MS004_S04_CORPUS_OUT", str(corpus_path))
    spec = importlib.util.spec_from_file_location(
        "retail_filter_scenario", ROOT / "tests/e2e/ms-004-workspace/scenario.py"
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
    token = identity.login(
        workspace_id=workspace,
        email="author@example.test",
        password="synthetic-author-password",
        device_label="MS010 disposable provider",
    )
    actor = identity.authenticate(token.access_token)
    identity_access = ResourceAccessService(
        PostgresResourceAccessRepository(connect), lambda: identity.authenticate(token.access_token)
    )
    semantics = PostgresSalesSemanticRepository(connect)
    artifacts = SalesArtifactStore(connect, artifact_root)
    limits = FilterResourcePolicy(
        version_id=uuid4(),
        max_rows=1_000_000,
        max_input_bytes=64 * 1024 * 1024,
        max_nodes=64,
        max_depth=12,
        max_values=1000,
        memory_mb=128,
        threads=1,
        timeout_ms=10000,
    )
    access = PublishedRetailFilterAccess(
        identity=identity_access, semantics=semantics, artifacts=artifacts, resource_policy=limits
    )
    engine = DuckDBFlatFilter(artifact_root=artifact_root, access=access)
    grant = access.authorize(
        workspace_id=workspace, actor_id=actor.principal_id, dataset_version_id=dataset
    )
    assert [f.field_id for f in grant.registry.fields] == [
        "Receipt.source_system_id",
        "Receipt.store_id",
        "Receipt.status",
        "Receipt.currency",
        "Receipt.receipt_date",
    ]
    assert (
        access.authorize(
            workspace_id=workspace, actor_id=actor.principal_id, dataset_version_id=dataset
        ).registry
        == grant.registry
    )
    status = next(f for f in grant.registry.fields if f.field_id == "Receipt.status")
    request = FlatFilterRequest(
        workspace_id=workspace,
        dataset_version_id=dataset,
        registry_version_id=grant.registry.version_id,
        expression=FlatPredicate(
            field_id=status.field_id,
            field_version_id=status.version_id,
            operator="eq",
            values=(FilterValue(data_type="string", value="completed"),),
        ),
    )
    result = engine.execute(request, actor_id=actor.principal_id)
    with psycopg.connect(
        host=os.environ["CUSTOMETRY_TEST_SOURCE_HOST"],
        port=os.environ["CUSTOMETRY_TEST_SOURCE_PORT"],
        dbname=os.environ["CUSTOMETRY_TEST_SOURCE_DATABASE"],
        user=os.environ["CUSTOMETRY_TEST_SOURCE_USER"],
        password=Path(os.environ["CUSTOMETRY_TEST_SOURCE_PASSWORD_FILE"]).read_text().strip(),
    ) as source:
        source.execute("SET TRANSACTION READ ONLY")
        expected = source.execute(
            "SELECT receipt_id::text FROM retail.receipts WHERE status='completed' ORDER BY receipt_id::text"
        ).fetchall()
        store_one = source.execute(
            "SELECT receipt_id::text FROM retail.receipts WHERE status='completed' AND store_id=1 ORDER BY receipt_id::text"
        ).fetchall()
    assert result.matched_ids == tuple(row[0] for row in expected)
    assert result.unknown_count == 0
    organization = OrganizationService(PostgresOrganizationRepository(connect))

    def bind(stores):
        # Required object scopes must be explicitly covered by department policy.
        # Read fixture identity; perform all policy changes through the public service.
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
    scoped = engine.execute(request, actor_id=actor.principal_id)
    assert scoped.matched_ids == tuple(row[0] for row in store_one)
    assert scoped.request_hash != result.request_hash
    bind(("store:absent",))
    assert engine.execute(request, actor_id=actor.principal_id).authorized_count == 0
    with pytest.raises(AnalyticsFailure, match="FORBIDDEN"):
        engine.execute(
            request.model_copy(update={"workspace_id": uuid4()}), actor_id=actor.principal_id
        )
    with pytest.raises(AnalyticsFailure, match="ARTIFACT_NOT_VISIBLE"):
        artifacts.admit_filter_input(
            workspace_id=uuid4(),
            artifact_id=grant.binding.artifact_id,
            entity="Receipt",
            content_hash=grant.binding.content_hash,
        )
    with pytest.raises(AnalyticsFailure, match="ARTIFACT_BINDING_MISMATCH"):
        artifacts.admit_filter_input(
            workspace_id=workspace,
            artifact_id=grant.binding.artifact_id,
            entity="Receipt",
            content_hash="0" * 64,
        )
    with pytest.raises(AnalyticsFailure, match="ARTIFACT_BINDING_MISMATCH"):
        artifacts.admit_filter_input(
            workspace_id=workspace,
            artifact_id=grant.binding.artifact_id,
            entity="Customer",
            content_hash=grant.binding.content_hash,
        )
    staged_id = uuid4()
    with connect() as pending:
        pending.execute(
            """INSERT INTO artifact_manifests
            (id,workspace_id,producer_batch_id,artifact_type,entity,relative_uri,content_hash,
             row_count,byte_size,schema_json,pii_class,state)
            SELECT %s,workspace_id,NULL,artifact_type,entity,%s,content_hash,row_count,byte_size,
                   schema_json,pii_class,state FROM artifact_manifests WHERE id=%s""",
            (staged_id, f"objects/{staged_id}.parquet", grant.binding.artifact_id),
        )
        with pytest.raises(AnalyticsFailure, match="ARTIFACT_NOT_VISIBLE"):
            artifacts.admit_filter_input(
                workspace_id=workspace,
                artifact_id=staged_id,
                entity="Receipt",
                content_hash=grant.binding.content_hash,
            )
        pending.rollback()
    original_read = engine._read

    def change_after_admission(*args, **kwargs):
        table = original_read(*args, **kwargs)
        bind(("store:1",))
        return table

    monkeypatch.setattr(engine, "_read", change_after_admission)
    with pytest.raises(AnalyticsFailure, match="FILTER_POLICY_CHANGED"):
        engine.execute(request, actor_id=actor.principal_id)
    monkeypatch.setattr(engine, "_read", original_read)

    def revoke_after_admission(*args, **kwargs):
        table = original_read(*args, **kwargs)
        identity.revoke_session(actor, token.session_id)
        return table

    monkeypatch.setattr(engine, "_read", revoke_after_admission)
    with pytest.raises(IdentityFailure):
        engine.execute(request, actor_id=actor.principal_id)
    monkeypatch.setattr(engine, "_read", original_read)
    with pytest.raises(IdentityFailure):
        engine.execute(request, actor_id=actor.principal_id)
