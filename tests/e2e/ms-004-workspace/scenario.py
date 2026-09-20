"""S04 isolated real source intake, sessions and native workspace browser fixture."""

from __future__ import annotations
import json
import os
from pathlib import Path
from uuid import UUID, uuid4
from datetime import date
from typing import Any, TypedDict, cast
import psycopg
from custometry_api.config import Settings
from custometry_api.main import create_app
from packages.identity_access.application.service import IdentityService
from packages.identity_access.infrastructure.postgres import PostgresIdentityRepository
from packages.identity_access.application.organization import OrganizationService
from packages.identity_access.infrastructure.organization_postgres import (
    PostgresOrganizationRepository,
)
from packages.contracts.analytics.sales_report import SalesReportRequest
from packages.contracts.presentation import SaveRequest
from packages.presentation.application.reports import ReportService
from packages.presentation.infrastructure.postgres import PostgresReportRepository
from packages.artifacts.infrastructure.document_snapshots import DocumentSnapshotArtifacts
from packages.artifacts.infrastructure.local import LocalArtifactStore
from apps.worker_data.vertical_slice import DataPipelineRunner
from custometry_api.analytics.router import build_analytics_services
from tests.integration.data_pipeline.conftest import DataPipelineRuntime
from tests.integration.data_pipeline.test_retail_report import request_for
from plugins.connector_postgresql.adapter import PostgreSQLConnector, PostgreSQLTarget

ROOT = Path(__file__).resolve().parents[3]


class ActorArguments(TypedDict):
    workspace_id: UUID
    principal_id: UUID
    permissions: frozenset[str]


def create_scenario(tmp_path: Path):
    settings = Settings(analytics_artifact_root=tmp_path)

    def connect() -> psycopg.Connection[tuple[Any, ...]]:
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
    boot = identity.bootstrap(
        presented_secret="synthetic-bootstrap",
        email="author@example.test",
        password="synthetic-author-password",
        workspace_key="s04-owned",
        workspace_name="S04",
    )
    tokens = identity.login(
        email="author@example.test",
        password="synthetic-author-password",
        workspace_id=boot.workspace_id,
        device_label="S04",
    )
    actor = identity.authenticate(tokens.access_token)
    organization = OrganizationService(PostgresOrganizationRepository(connect))
    units = organization.list_units(actor)
    root = UUID(str(units[0]["org_unit_id"]))
    department = organization.create_unit(
        actor, key="sales", kind="department", parent_org_unit_id=root, display_name="Sales"
    )
    department_id = UUID(str(department["org_unit_id"]))
    organization.assign_primary(actor, principal_id=actor.principal_id, org_unit_id=department_id)
    draft = organization.create_policy_draft(
        actor,
        policy_id=None,
        org_unit_id=department_id,
        expected_version=None,
        allowed_actions=("view_snapshot", "run", "edit"),
        row_scope_refs=(),
        column_policy_refs=(),
        pii_allowed=False,
        include_descendants=True,
        effective_from=None,
    )
    organization.publish_policy(
        actor,
        policy_id=UUID(str(draft["policy_id"])),
        expected_version=int(cast(int, draft["version"])),
        effective_from=None,
    )
    source = PostgreSQLConnector(
        PostgreSQLTarget(
            host=os.environ["CUSTOMETRY_TEST_SOURCE_HOST"],
            port=int(os.environ["CUSTOMETRY_TEST_SOURCE_PORT"]),
            dbname=os.environ["CUSTOMETRY_TEST_SOURCE_DATABASE"],
            user=os.environ["CUSTOMETRY_TEST_SOURCE_USER"],
            password=Path(os.environ["CUSTOMETRY_TEST_SOURCE_PASSWORD_FILE"]).read_text().strip(),
        )
    )
    runtime = DataPipelineRuntime(connect, source, actor.workspace_id, actor.principal_id)
    intake = DataPipelineRunner(
        connector=source, connect=connect, artifact_store=LocalArtifactStore(tmp_path)
    ).run(request_for(runtime))
    dataset = intake.semantic_dataset_version_id
    assert dataset is not None

    def bind(
        kind: str, resource: UUID, owner: UUID = actor.principal_id, stores: tuple[str, ...] = ()
    ) -> dict[str, object]:
        return organization.bind_resource(
            actor,
            resource_type=kind,
            resource_id=resource,
            creator_principal_id=actor.principal_id,
            owner_type="principal",
            owner_id=owner,
            allowed_actions=("view_snapshot", "run", "edit"),
            required_row_scope_refs=stores,
            required_column_policy_refs=(),
            requires_pii=False,
            effective_from=None,
        )

    _, legacy_analytics = build_analytics_services(settings)
    result = legacy_analytics.run_sales_report(
        workspace_id=actor.workspace_id,
        principal_id=actor.principal_id,
        permissions=actor.permissions,
        request=SalesReportRequest(
            dataset,
            starts_on=date(2025, 1, 1),
            ends_on=date(2025, 1, 31),
            comparison="previous_year_same_dates",
        ),
    )
    with psycopg.connect(
        host=os.environ["CUSTOMETRY_TEST_SOURCE_HOST"],
        port=int(os.environ["CUSTOMETRY_TEST_SOURCE_PORT"]),
        dbname=os.environ["CUSTOMETRY_TEST_SOURCE_DATABASE"],
        user=os.environ["CUSTOMETRY_TEST_SOURCE_USER"],
        password=Path(os.environ["CUSTOMETRY_TEST_SOURCE_PASSWORD_FILE"]).read_text().strip(),
    ) as source_connection:
        receipt_coverage = source_connection.execute(
            "SELECT min(receipt_datetime)::date::text, max(receipt_datetime)::date::text, count(*) FROM retail.receipts"
        ).fetchone()
        calendar_coverage = source_connection.execute(
            "SELECT min(calendar_date)::text,max(calendar_date)::text,count(*),count(*) FILTER (WHERE is_period_complete) FROM retail.calendar"
        ).fetchone()
    corpus = {
        "schema_version": "ms004-s04-corpus/v1",
        "workspace_id": str(actor.workspace_id),
        "semantic_dataset_version_id": str(dataset),
        "receipt_coverage": receipt_coverage,
        "calendar_coverage": calendar_coverage,
        "source_bindings": result["lineage"]["bindings"],
        "source_hashes": result["lineage"]["source_hashes"],
        "metric_refs": [
            {k: m[k] for k in ("metric_id", "version_id", "content_hash")}
            for m in result["metrics"]
        ],
    }
    Path(os.environ.get("MS004_S04_CORPUS_OUT", "/tmp/ms004-s04-corpus.json")).write_text(
        json.dumps(corpus, indent=2)
    )
    legacy = ReportService(
        PostgresReportRepository(connect),
        legacy_analytics,
        DocumentSnapshotArtifacts(connect, tmp_path),
        json.loads(
            (ROOT / "packages/presentation/infrastructure/system-brand.v1.json").read_text()
        ),
    )
    args = cast(
        ActorArguments,
        dict(
            workspace_id=actor.workspace_id,
            principal_id=actor.principal_id,
            permissions=actor.permissions,
        ),
    )
    refs = legacy.prepare(**args, result_id=UUID(result["result_id"]))
    old_request = SaveRequest(
        contract_version="draft-report/v1",
        result_id=result["result_id"],
        title="Original",
        expected_revision=0,
        idempotency_key=uuid4(),
        **{n: refs[n]["reference"] for n in ("chart_spec", "brand_profile", "company_pack")},
    )
    bind("analysis", dataset)
    readers: dict[str, UUID] = {}
    for role in ("reader", "admin_reader"):
        invite = identity.invite(
            actor,
            workspace_id=actor.workspace_id,
            email=f"{role}@example.test",
            roles=["analyst"] + (["workspace_admin"] if role == "admin_reader" else []),
            expires_in_hours=1,
        )
        principal = identity.accept_invitation(
            token=invite.token, password="synthetic-reader-password"
        )
        organization.assign_primary(actor, principal_id=principal, org_unit_id=department_id)
        readers[role] = principal
    app = create_app(settings=settings)

    reader_grants: list[tuple[UUID, str, UUID]] = []

    @app.post("/fixture/reader-view-only/{report_id}")
    def reader_view_only(report_id: UUID) -> dict[str, bool]:
        for grant_id, kind, resource in reader_grants:
            if kind != "report" or resource != report_id:
                continue
            organization.revoke_grant(actor, grant_id=grant_id, expected_version=1)
            organization.create_grant(
                actor,
                subject_type="principal",
                subject_id=readers["reader"],
                target_org_unit_id=department_id,
                resource_type=kind,
                resource_id=resource,
                actions=("view_snapshot",),
                reason="S04 effective read-only browser",
                effective_from=None,
                expires_at=None,
            )
        reader_grants.clear()
        return {"view_only": bool(report_id)}

    @app.get("/fixture/scenario")
    def scenario() -> dict[str, str]:
        request = old_request.model_copy(update={"idempotency_key": uuid4()})
        saved = legacy.save(**args, request=request)
        report_id = UUID(str(saved["report_id"]))
        bind("report", report_id)
        for principal in readers.values():
            for kind, resource in (("report", report_id), ("analysis", dataset)):
                grant = organization.create_grant(
                    actor,
                    subject_type="principal",
                    subject_id=principal,
                    target_org_unit_id=department_id,
                    resource_type=kind,
                    resource_id=resource,
                    actions=("view_snapshot", "run", "edit"),
                    reason="S04 isolated browser",
                    effective_from=None,
                    expires_at=None,
                )
                if principal == readers["reader"]:
                    reader_grants.append((UUID(str(grant["grant_id"])), kind, resource))
        return {"workspace": str(actor.workspace_id), "report": str(saved["report_id"])}

    _ = scenario, reader_view_only
    return app
