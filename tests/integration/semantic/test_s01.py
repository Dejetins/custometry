"""Real control-PostgreSQL and real Identity/session API proof, isolated per test."""

from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import os
from pathlib import Path
import subprocess
from uuid import UUID, uuid4
import psycopg
from psycopg import sql
from psycopg.types.json import Jsonb
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from custometry_api.config import Settings
from custometry_api.main import create_app
from custometry_api.semantic.router import build_calendar_service
from packages.contracts.semantic import CalendarRef
from packages.semantic_model.application.calendar import initial_calendar_id
from packages.identity_access.domain.policy import Actor

ROOT = Path(__file__).resolve().parents[3]


@dataclass
class Database:
    settings: Settings

    def connect(self):
        s = self.settings
        return psycopg.connect(
            host=s.database_host,
            port=s.database_port,
            dbname=s.database_name,
            user=s.database_user,
            password=s.read_database_password(),
        )

    def migrate(self, target: str, *, down: bool = False) -> subprocess.CompletedProcess[str]:
        s = self.settings
        env = {
            **os.environ,
            "CUSTOMETRY_DATABASE_HOST": s.database_host,
            "CUSTOMETRY_DATABASE_PORT": str(s.database_port),
            "CUSTOMETRY_DATABASE_NAME": s.database_name,
            "CUSTOMETRY_DATABASE_USER": s.database_user,
            "CUSTOMETRY_DATABASE_PASSWORD_FILE": str(s.database_password_file),
        }
        return subprocess.run(
            [
                "uv",
                "run",
                "--locked",
                "--package",
                "custometry-api",
                "alembic",
                "-c",
                "migrations/alembic.ini",
                "downgrade" if down else "upgrade",
                target,
            ],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
        )


@pytest.fixture
def database(tmp_path: Path):
    if "MS004_PASSWORD_FILE" not in os.environ:
        pytest.skip(
            "Run through tests/integration/semantic/run_s01.py; real isolated PostgreSQL is required"
        )
    name = "ms004_" + uuid4().hex
    secret = tmp_path / "bootstrap"
    secret.write_text("ms004-synthetic-bootstrap")
    secret.chmod(0o600)
    settings = Settings(
        environment="test",
        database_host="127.0.0.1",
        database_port=int(os.environ["MS004_DATABASE_PORT"]),
        database_name=name,
        database_user="postgres",
        database_password_file=Path(os.environ["MS004_PASSWORD_FILE"]),
        bootstrap_token_file=secret,
        cors_allowed_origins=["http://testserver"],
        identity_cookie_secure=False,
        identity_rate_limit_requests=1000,
    )
    with psycopg.connect(
        host=settings.database_host,
        port=settings.database_port,
        dbname="postgres",
        user="postgres",
        password=settings.read_database_password(),
        autocommit=True,
    ) as admin:
        admin.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(name)))
        db = Database(settings)
        try:
            result = db.migrate("0011_presentation_drafts")
            assert result.returncode == 0, result.stderr
            yield db
        finally:
            admin.execute(sql.SQL("DROP DATABASE {} WITH (FORCE)").format(sql.Identifier(name)))


def seed_legacy(db: Database):
    from tests.contract.presentation.test_workspace import legacy_fixture

    payload = legacy_fixture()
    workspace = UUID(payload["composition"]["workspace_id"])
    owner, report, version, snapshot = [
        UUID(payload[key])
        for key in ("author_principal_id", "report_id", "version_id", "snapshot_id")
    ]
    with db.connect() as c:
        c.execute(
            "INSERT INTO identity_principals(id,email,password_hash,installation_admin,active) VALUES (%s,%s,'fixture',false,true)",
            (owner, f"{owner}@example.test"),
        )
        c.execute(
            "INSERT INTO identity_workspaces(id,key,name,active) VALUES (%s,%s,'Legacy',true)",
            (workspace, "legacy-" + workspace.hex),
        )
        c.execute(
            "INSERT INTO presentation_documents(id,workspace_id,owner_principal_id) VALUES (%s,%s,%s)",
            (report, workspace, owner),
        )
        c.execute(
            "INSERT INTO presentation_versions(id,document_id,revision,snapshot_id,idempotency_key,request_hash,payload) VALUES (%s,%s,1,%s,%s,%s,%s)",
            (version, report, snapshot, uuid4(), "a" * 64, Jsonb(payload)),
        )
        c.execute(
            "UPDATE presentation_documents SET revision=1,latest_version_id=%s WHERE id=%s",
            (version, report),
        )
    return workspace, owner, report, version, payload


def test_additive_backfill_legacy_bytes_creator_guard_and_safe_downgrade(database: Database):
    db = database
    workspace, owner, report, version, _ = seed_legacy(db)
    with db.connect() as c:
        before = c.execute(
            "SELECT payload::text FROM presentation_versions WHERE id=%s", (version,)
        ).fetchall()[0][0]
    result = db.migrate("head")
    assert result.returncode == 0, result.stderr
    from packages.contracts.presentation.workspace import VersionedReport

    with db.connect() as c:
        stored = c.execute(
            "SELECT payload FROM presentation_versions WHERE id=%s", (version,)
        ).fetchall()[0][0]
        assert VersionedReport.model_validate(stored).root.contract_version == "draft-report/v1"

    with db.connect() as c:
        row = c.execute(
            "SELECT creator_principal_id FROM presentation_documents WHERE id=%s", (report,)
        ).fetchone()
        assert row is not None and row[0] == owner
        assert c.execute(
            "SELECT payload::text,contract_version FROM presentation_versions WHERE id=%s",
            (version,),
        ).fetchone() == (before, "draft-report/v1")
        initial = c.execute(
            "SELECT version_id,revision FROM semantic_workspace_calendar_defaults WHERE workspace_id=%s",
            (workspace,),
        ).fetchone()
        assert initial == (initial_calendar_id(workspace), 0)
    service = build_calendar_service(db.settings)
    service.provision(workspace)
    actor = Actor(owner, workspace, "fixture", frozenset({"workspace.read"}))
    default = service.get_default(workspace, actor)
    assert default.calendar.profile.fiscal_year_start_month == 1
    assert default.calendar.created_by is None
    assert (
        service.get_version(
            CalendarRef(
                version_id=default.calendar.version_id, content_hash=default.calendar.content_hash
            ),
            actor,
        )
        == default.calendar
    )
    with pytest.raises(psycopg.errors.RaiseException, match="CREATOR_IMMUTABLE"):
        with db.connect() as c:
            c.execute(
                "UPDATE presentation_documents SET creator_principal_id=%s WHERE id=%s",
                (uuid4(), report),
            )
    with pytest.raises(psycopg.errors.RaiseException, match="VERSION_IMMUTABLE"):
        with db.connect() as c:
            c.execute("UPDATE semantic_business_calendar_versions SET content_hash=%s", ("b" * 64,))
    with pytest.raises(psycopg.errors.RaiseException, match="VERSION_IMMUTABLE"):
        with db.connect() as c:
            c.execute("DELETE FROM semantic_business_calendar_versions")
    # Existing v1 inserts still work after migration, without a new creator parameter.
    with db.connect() as c:
        inserted = c.execute(
            "INSERT INTO presentation_documents(id,workspace_id,owner_principal_id) VALUES (%s,%s,%s) RETURNING creator_principal_id",
            (uuid4(), workspace, owner),
        ).fetchone()
        assert inserted is not None and inserted[0] == owner
    assert db.migrate("0011_presentation_drafts", down=True).returncode == 0
    with db.connect() as c:
        assert (
            c.execute(
                "SELECT payload::text FROM presentation_versions WHERE id=%s", (version,)
            ).fetchall()[0][0]
            == before
        )
    assert db.migrate("head").returncode == 0
    with db.connect() as c:
        assert c.execute(
            "SELECT version_id FROM semantic_workspace_calendar_defaults WHERE workspace_id=%s",
            (workspace,),
        ).fetchall()[0][0] == initial_calendar_id(workspace)


def test_saved_view_same_report_workspace_and_downgrade_guard(database: Database):
    db = database
    workspace, owner, report, version, _ = seed_legacy(db)
    other_workspace, _, _, other_version, _ = seed_legacy(db)
    assert db.migrate("head").returncode == 0
    with pytest.raises(psycopg.errors.ForeignKeyViolation):
        with db.connect() as c:
            c.execute(
                "INSERT INTO presentation_saved_views(id,workspace_id,owner_principal_id,document_id) VALUES (%s,%s,%s,%s)",
                (uuid4(), other_workspace, owner, report),
            )
    view = uuid4()
    with db.connect() as c:
        c.execute(
            "INSERT INTO presentation_saved_views(id,workspace_id,owner_principal_id,document_id) VALUES (%s,%s,%s,%s)",
            (view, workspace, owner, report),
        )
    with pytest.raises(psycopg.errors.ForeignKeyViolation):
        with db.connect() as c:
            c.execute(
                "INSERT INTO presentation_saved_view_versions(id,saved_view_id,document_id,revision,document_version_id,idempotency_key,request_hash,payload) VALUES (%s,%s,%s,1,%s,%s,%s,'{}')",
                (uuid4(), view, report, other_version, uuid4(), "a" * 64),
            )
    with db.connect() as c:
        view_version = uuid4()
        c.execute(
            "INSERT INTO presentation_saved_view_versions(id,saved_view_id,document_id,revision,document_version_id,idempotency_key,request_hash,payload) VALUES (%s,%s,%s,1,%s,%s,%s,'{}')",
            (view_version, view, report, version, uuid4(), "a" * 64),
        )
        c.execute(
            "UPDATE presentation_saved_views SET revision=1,latest_version_id=%s WHERE id=%s",
            (view_version, view),
        )
    refused = db.migrate("0011_presentation_drafts", down=True)
    assert refused.returncode != 0 and "FORWARD_REPAIR" in refused.stderr
    with db.connect() as c:
        assert (
            c.execute("SELECT version_num FROM alembic_version").fetchall()[0][0]
            == "0012_metric_workspace"
        )


def app_client(db: Database) -> TestClient:
    app = FastAPI()
    app.mount("/api", create_app(settings=db.settings))
    return TestClient(app, base_url="http://testserver/api/")


def bootstrap_login(client: TestClient):
    created = client.post(
        "/identity/bootstrap",
        headers={"X-Bootstrap-Token": "ms004-synthetic-bootstrap"},
        json={
            "email": "owner@example.test",
            "password": "Owner-password-123!",
            "workspace_key": "ms004",
            "workspace_name": "MS004",
        },
    )
    assert created.status_code == 200, created.text
    identity = created.json()
    response = client.post(
        "/identity/login",
        json={
            "email": "owner@example.test",
            "password": "Owner-password-123!",
            "workspace_id": identity["workspace_id"],
            "device_label": "s01",
        },
    )
    assert response.status_code == 200, response.text
    return identity, {"Origin": "http://testserver", "X-CSRF-Token": response.json()["csrf_token"]}


def update(month: int, revision: int):
    return {
        "profile": {"fiscal_year_start_month": month},
        "expected_revision": revision,
        "idempotency_key": str(uuid4()),
    }


def test_real_calendar_api_csrf_roles_cas_replay_scope_revocation(database: Database):
    db = database
    assert db.migrate("head").returncode == 0
    with app_client(db) as client:
        assert client.get("/semantic/workspace-calendar/v1").status_code == 401
        identity, headers = bootstrap_login(client)
        initial = client.get("/semantic/workspace-calendar/v1")
        assert initial.status_code == 200 and initial.headers["cache-control"] == "no-store"
        initial = initial.json()
        assert (
            initial["revision"] == 0
            and initial["calendar"]["profile"]["fiscal_year_start_month"] == 1
        )
        body = update(4, 0)
        assert client.post("/semantic/workspace-calendar/v1/versions", json=body).status_code == 403
        assert (
            client.post(
                "/semantic/workspace-calendar/v1/versions", headers=headers, json=update(13, 0)
            ).status_code
            == 422
        )
        first = client.post("/semantic/workspace-calendar/v1/versions", headers=headers, json=body)
        assert first.status_code == 200, first.text
        first = first.json()
        assert (
            first["revision"] == 1
            and first["calendar"]["previous_version_id"] == initial["calendar"]["version_id"]
        )
        assert (
            client.post(
                "/semantic/workspace-calendar/v1/versions", headers=headers, json=body
            ).json()
            == first
        )
        assert (
            client.post(
                "/semantic/workspace-calendar/v1/versions",
                headers=headers,
                json={**body, "profile": {"fiscal_year_start_month": 10}},
            ).status_code
            == 409
        )
        assert (
            client.post(
                "/semantic/workspace-calendar/v1/versions", headers=headers, json=update(10, 0)
            ).status_code
            == 409
        )
        # Two independent sessions/connections compete on revision 1.
        cookies = dict(client.cookies)

        def write(month: int) -> int:
            with app_client(db) as concurrent:
                concurrent.cookies.update(cookies)
                return concurrent.post(
                    "/semantic/workspace-calendar/v1/versions",
                    headers=headers,
                    json=update(month, 1),
                ).status_code

        with ThreadPoolExecutor(max_workers=2) as pool:
            assert sorted(pool.map(write, [7, 10])) == [200, 409]
        assert (
            client.post(
                "/semantic/workspace-calendar/v1/versions", headers=headers, json=body
            ).json()
            == first
        )
        current = client.get("/semantic/workspace-calendar/v1").json()
        assert current["revision"] == 2
        pin = initial["calendar"]
        assert (
            client.get(
                f"/semantic/workspace-calendar/v1/versions/{pin['version_id']}?content_hash={pin['content_hash']}"
            ).json()
            == pin
        )
        other = client.post(
            "/identity/workspaces", headers=headers, json={"key": "second", "name": "Second"}
        )
        assert other.status_code == 200, other.text
        other_id = UUID(other.json()["workspace_id"])
        with db.connect() as c:
            other_version = c.execute(
                "SELECT version_id FROM semantic_workspace_calendar_defaults WHERE workspace_id=%s",
                (other_id,),
            ).fetchall()[0][0]
        assert (
            client.get(
                f"/semantic/workspace-calendar/v1/versions/{other_version}?content_hash={pin['content_hash']}"
            ).status_code
            == 404
        )
        with db.connect() as c:
            c.execute(
                "UPDATE identity_role_assignments SET role='workspace_admin' WHERE principal_id=%s AND workspace_id=%s",
                (UUID(identity["principal_id"]), UUID(identity["workspace_id"])),
            )
        october = client.post(
            "/semantic/workspace-calendar/v1/versions", headers=headers, json=update(10, 2)
        )
        assert (
            october.status_code == 200
            and october.json()["calendar"]["profile"]["fiscal_year_start_month"] == 10
        )
        with db.connect() as c:
            c.execute(
                "UPDATE identity_role_assignments SET role='analyst' WHERE principal_id=%s AND workspace_id=%s",
                (UUID(identity["principal_id"]), UUID(identity["workspace_id"])),
            )
        assert client.get("/semantic/workspace-calendar/v1").status_code == 200
        assert (
            client.post(
                "/semantic/workspace-calendar/v1/versions", headers=headers, json=body
            ).status_code
            == 403
        )
        with db.connect() as c:
            c.execute(
                "UPDATE identity_memberships SET status='suspended' WHERE principal_id=%s AND workspace_id=%s",
                (UUID(identity["principal_id"]), UUID(identity["workspace_id"])),
            )
        assert client.get("/semantic/workspace-calendar/v1").status_code == 401
        refused = db.migrate("0011_presentation_drafts", down=True)
        assert refused.returncode != 0 and "FORWARD_REPAIR" in refused.stderr


def test_calendar_scope_constraints_and_v2_report_downgrade_refusal(database: Database):
    db = database
    workspace, _, _, version, _ = seed_legacy(db)
    other_workspace, *_ = seed_legacy(db)
    assert db.migrate("head").returncode == 0
    with pytest.raises(psycopg.errors.ForeignKeyViolation):
        with db.connect() as c:
            c.execute(
                "UPDATE semantic_workspace_calendar_defaults SET version_id=%s WHERE workspace_id=%s",
                (initial_calendar_id(other_workspace), workspace),
            )
    with db.connect() as c:
        c.execute(
            "UPDATE presentation_versions SET contract_version='configured-report/v2' WHERE id=%s",
            (version,),
        )
    refused = db.migrate("0011_presentation_drafts", down=True)
    assert refused.returncode != 0 and "FORWARD_REPAIR" in refused.stderr


def test_report_and_analytics_v2_routes_remain_unmounted(database: Database):
    assert database.migrate("head").returncode == 0
    with app_client(database) as client:
        _, headers = bootstrap_login(client)
        assert (
            client.post("/analytics/metric-workspace/v2", headers=headers, json={}).status_code
            == 404
        )
        assert client.get(f"/reports/v2/{uuid4()}").status_code == 404
        assert (
            client.post(f"/reports/v2/{uuid4()}/apply", headers=headers, json={}).status_code == 404
        )


def test_calendar_failed_pointer_write_rolls_back_version(database: Database) -> None:
    db = database
    assert db.migrate("head").returncode == 0
    with app_client(db) as client:
        _, headers = bootstrap_login(client)
        before = client.get("/semantic/workspace-calendar/v1").json()
        body = update(4, 0)
        with db.connect() as c:
            c.execute("""CREATE FUNCTION test_fail_calendar() RETURNS trigger LANGUAGE plpgsql AS $$
                BEGIN RAISE EXCEPTION 'TASK_OWNED_WRITE_FAILURE'; END $$;
                CREATE TRIGGER task_fail BEFORE UPDATE ON semantic_workspace_calendar_defaults
                FOR EACH ROW EXECUTE FUNCTION test_fail_calendar();""")
        failed = client.post("/semantic/workspace-calendar/v1/versions", headers=headers, json=body)
        assert failed.status_code == 503 and failed.json() == {"code": "STORAGE_UNAVAILABLE"}
        assert client.get("/semantic/workspace-calendar/v1").json() == before
        with db.connect() as c:
            assert (
                c.execute("SELECT count(*) FROM semantic_business_calendar_versions").fetchall()[0][
                    0
                ]
                == 1
            )
            c.execute(
                "DROP TRIGGER task_fail ON semantic_workspace_calendar_defaults; DROP FUNCTION test_fail_calendar();"
            )
        assert (
            client.post(
                "/semantic/workspace-calendar/v1/versions", headers=headers, json=body
            ).status_code
            == 200
        )


def test_analytics_v2_metadata_blocks_lossy_downgrade(database: Database) -> None:
    db = database
    workspace, owner, _, _, _ = seed_legacy(db)
    assert db.migrate("head").returncode == 0
    connection, source, dataset, batch, quality, version = [uuid4() for _ in range(6)]
    # Valid control-plane fixture only; this is not source intake/calculation proof.
    with db.connect() as c:
        c.execute(
            """INSERT INTO source_connections(id,workspace_id,source_system_id,connector_id,profile_ref,secret_ref,display_name,status,created_by)
            VALUES (%s,%s,%s,'postgresql','fixture','fixture','S01 metadata','active',%s)""",
            (connection, workspace, source, owner),
        )
        c.execute(
            """INSERT INTO ingestion_batches(id,workspace_id,connection_id,source_system_id,semantic_dataset_id,idempotency_key,state,consistency_mode)
            VALUES (%s,%s,%s,%s,%s,'s01-metadata','committed','repeatable_read')""",
            (batch, workspace, connection, source, dataset),
        )
        c.execute(
            """INSERT INTO data_quality_reports(id,workspace_id,batch_id,decision,rule_versions,violations,applied_waiver_ids,evaluated_at)
            VALUES (%s,%s,%s,'passed','[]','[]','[]',now())""",
            (quality, workspace, batch),
        )
        c.execute(
            """INSERT INTO semantic_dataset_versions(id,semantic_dataset_id,workspace_id,version,status,quality_report_id,bindings,capability_matrix,impact_summary,request_hash)
            VALUES (%s,%s,%s,1,'published',%s,'[]','{}','{}',%s)""",
            (version, dataset, workspace, quality, "a" * 64),
        )
        c.execute(
            """INSERT INTO analytics_sales_reports(id,workspace_id,owner_principal_id,semantic_dataset_version_id,request_hash,policy_hash,response_payload,contract_version)
            VALUES (%s,%s,%s,%s,%s,%s,'{}','metric-workspace/v2')""",
            (uuid4(), workspace, owner, version, "b" * 64, "c" * 64),
        )
    refused = db.migrate("0011_presentation_drafts", down=True)
    assert refused.returncode != 0 and "FORWARD_REPAIR" in refused.stderr


def test_interrupted_workspace_provision_is_recovered_without_replacing_default(
    database: Database,
) -> None:
    from packages.contracts.semantic import UpdateCalendarRequest, BusinessCalendarProfile

    db = database
    assert db.migrate("head").returncode == 0
    workspace, owner, *_ = seed_legacy(db)  # simulates an old writer after the additive migration
    actor = Actor(owner, workspace, "fixture", frozenset({"workspace.read", "workspace.manage"}))
    service = build_calendar_service(db.settings)
    default = service.get_default(workspace, actor)
    assert default.calendar.version_id == initial_calendar_id(workspace)
    changed = service.update_default(
        UpdateCalendarRequest(
            profile=BusinessCalendarProfile(fiscal_year_start_month=4),
            expected_revision=0,
            idempotency_key=uuid4(),
        ),
        actor,
    )
    service.provision(workspace)
    assert service.get_default(workspace, actor) == changed


def test_custom_calendar_cannot_use_null_request_hash(database: Database) -> None:
    db = database
    workspace, owner, _, _, _ = seed_legacy(db)
    assert db.migrate("head").returncode == 0
    with pytest.raises(psycopg.errors.CheckViolation):
        with db.connect() as c:
            c.execute(
                """INSERT INTO semantic_business_calendar_versions
                (id,workspace_id,content_hash,profile_json,created_by,previous_version_id,idempotency_key,request_hash,default_revision)
                SELECT %s,workspace_id,content_hash,profile_json,%s,id,%s,NULL,1
                FROM semantic_business_calendar_versions WHERE workspace_id=%s AND default_revision=0""",
                (uuid4(), owner, uuid4(), workspace),
            )
    with db.connect() as c:
        assert (
            c.execute(
                "SELECT count(*) FROM semantic_business_calendar_versions WHERE workspace_id=%s",
                (workspace,),
            ).fetchall()[0][0]
            == 1
        )
        assert (
            c.execute(
                "SELECT revision FROM semantic_workspace_calendar_defaults WHERE workspace_id=%s",
                (workspace,),
            ).fetchall()[0][0]
            == 0
        )
