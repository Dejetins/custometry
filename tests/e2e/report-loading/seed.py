"""Build fifty distinct synthetic principals and ready reports through owner services."""

from pathlib import Path
import json
import os
from datetime import date
from uuid import UUID, uuid4
import httpx

import psycopg
from custometry_api.config import Settings
from custometry_api.identity.router import create_identity_service
from custometry_api.analytics.router import build_analytics_services
from packages.identity_access.application.organization import OrganizationService
from packages.identity_access.infrastructure.organization_postgres import (
    PostgresOrganizationRepository,
)
from packages.contracts.analytics.sales_report import SalesReportRequest
from packages.contracts.presentation import SaveRequest
from packages.presentation.application.reports import ReportService
from packages.presentation.infrastructure.postgres import PostgresReportRepository
from packages.artifacts.infrastructure.document_snapshots import DocumentSnapshotArtifacts

ROOT = Path(__file__).resolve().parents[3]
os.environ.update(json.loads((ROOT / ".runtime/w39/connection.json").read_text()))

settings = Settings(
    analytics_artifact_root=Path(os.environ["CUSTOMETRY_DATABASE_PASSWORD_FILE"]).parent
    / "artifacts"
)


def connect():
    return psycopg.connect(
        host=settings.database_host,
        port=settings.database_port,
        dbname=settings.database_name,
        user=settings.database_user,
        password=settings.read_database_password(),
    )


identity = create_identity_service(settings)
demo = json.loads((ROOT / ".runtime/w39/demo.json").read_text())
workspace = UUID(demo["workspace"])
admin = identity.authenticate(
    identity.login(
        email="author@example.test",
        password="synthetic-author-password",
        workspace_id=workspace,
        device_label="W39 fixture setup",
    ).access_token
)
org = OrganizationService(PostgresOrganizationRepository(connect))
dept = next(UUID(str(u["org_unit_id"])) for u in org.list_units(admin) if u["key"] == "sales")
dataset = UUID(
    json.loads((ROOT / ".runtime/w39/corpus.json").read_text())["semantic_dataset_version_id"]
)
_, analytics = build_analytics_services(settings)
legacy = ReportService(
    PostgresReportRepository(connect),
    analytics,
    DocumentSnapshotArtifacts(connect, settings.analytics_artifact_root),
    json.loads((ROOT / "packages/presentation/infrastructure/system-brand.v1.json").read_text()),
)
fixtures = []
for i in range(50):
    email = f"w39-{i:02}@example.test"
    password = "synthetic-w39-password"
    from packages.identity_access.infrastructure.postgres import PostgresIdentityRepository

    existing = PostgresIdentityRepository(connect).credential_for_login(email, workspace)
    if existing:
        principal = existing.principal_id
    else:
        invite = identity.invite(
            admin, workspace_id=workspace, email=email, roles=["analyst"], expires_in_hours=24
        )
        principal = identity.accept_invitation(token=invite.token, password=password)
    if not existing:
        org.assign_primary(admin, principal_id=principal, org_unit_id=dept)
    if not existing:
        org.create_grant(
            admin,
            subject_type="principal",
            subject_id=principal,
            target_org_unit_id=dept,
            resource_type="analysis",
            resource_id=dataset,
            actions=("view_snapshot", "run", "edit"),
            reason="W39 synthetic load fixture",
            effective_from=None,
            expires_at=None,
        )
    token = identity.login(
        email=email, password=password, workspace_id=workspace, device_label="W39 fixture setup"
    )
    actor = identity.authenticate(token.access_token)
    args = dict(workspace_id=workspace, principal_id=principal, permissions=actor.permissions)
    result = analytics.run_sales_report(
        **args,
        request=SalesReportRequest(
            dataset,
            starts_on=date(2025, 1, 1),
            ends_on=date(2025, 12, 31),
            comparison="previous_year_same_dates",
        ),
    )
    refs = legacy.prepare(**args, result_id=UUID(result["result_id"]))
    saved = legacy.save(
        **args,
        request=SaveRequest(
            contract_version="draft-report/v1",
            result_id=result["result_id"],
            title=f"W39 Synthetic {i:02}",
            expected_revision=0,
            idempotency_key=uuid4(),
            **{n: refs[n]["reference"] for n in ("chart_spec", "brand_profile", "company_pack")},
        ),
    )
    report = saved["report_id"]
    org.bind_resource(
        admin,
        resource_type="report",
        resource_id=UUID(report),
        creator_principal_id=principal,
        owner_type="principal",
        owner_id=principal,
        allowed_actions=("view_snapshot", "run", "edit"),
        required_row_scope_refs=(),
        required_column_policy_refs=(),
        requires_pii=False,
        effective_from=None,
    )
    with httpx.Client(
        base_url="http://127.0.0.1:58139",
        headers={"Authorization": "Bearer " + token.access_token},
        timeout=240,
    ) as c:
        opened = c.get("/reports/v2/" + report)
        opened.raise_for_status()
        entry = opened.json()
        d = entry["definition"]
        cards = d["worksets"][0]["cards"]
        sets = []
        for n in range(3):
            sets.append(
                {
                    **d["worksets"][0],
                    "workset_id": str(uuid4()),
                    "name": {"ru": f"Набор {n + 1}", "en": f"Workset {n + 1}"},
                    "cards": [{**cards[k % 3], "card_id": str(uuid4())} for k in range(6)],
                }
            )
        d.update(
            worksets=sets,
            default_workset_id=sets[0]["workset_id"],
            selection={
                "mode": "single",
                "card_id": sets[0]["cards"][0]["card_id"],
                "temporal": "previous_year_same_dates",
                "display": "series",
            },
        )
        a = c.post(
            f"/reports/v2/{report}/apply",
            json={
                "contract_version": "configured-report/v2",
                "mode": "creator",
                "base_revision": entry["report"]["revision"],
                "definition": d,
            },
        )
        a.raise_for_status()
        applied = a.json()
        v = c.post(
            f"/reports/v2/{report}/versions",
            json={
                "contract_version": "configured-report/v2",
                "definition": d,
                "expected_revision": entry["report"]["revision"],
                "expected_saved_view_revision": entry["saved_view_revision"],
                "idempotency_key": str(uuid4()),
                "configuration_hash": applied["configuration_hash"],
                "result_ids": [b["result"]["result_id"] for b in applied["bindings_by_card"]],
                "chart_specs": applied["chart_specs"],
            },
        )
        v.raise_for_status()
    fixtures.append(
        {"workspace": str(workspace), "principal": str(principal), "email": email, "report": report}
    )
    (ROOT / ".runtime/w39/load-fixtures.json").write_text(json.dumps(fixtures, indent=2))
    print(f"Seeded {i + 1}/50", flush=True)
