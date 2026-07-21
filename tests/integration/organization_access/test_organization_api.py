from __future__ import annotations

from datetime import UTC, datetime, timedelta
import os
from pathlib import Path
import subprocess
from typing import cast
from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from custometry_api.config import Settings
from tests.integration.organization_access.conftest import bearer, connect, login


def _create_unit(
    client: TestClient,
    headers: dict[str, str],
    *,
    key: str,
    kind: str,
    name: str,
    parent: str | None = None,
) -> dict[str, object]:
    response = client.post(
        "/organization/units",
        headers=headers,
        json={
            "key": key,
            "kind": kind,
            "display_name": name,
            "parent_org_unit_id": parent,
        },
    )
    assert response.status_code == 200, response.text
    return response.json()


def _invite(
    client: TestClient,
    owner_csrf: str,
    *,
    workspace_id: str,
    email: str,
    role: str,
    password: str,
) -> str:
    invitation = client.post(
        "/identity/invitations",
        headers={"Origin": "http://testserver", "X-CSRF-Token": owner_csrf},
        json={"workspace_id": workspace_id, "email": email, "roles": [role]},
    )
    assert invitation.status_code == 200, invitation.text
    accepted = client.post(
        "/identity/invitations/accept",
        json={"token": invitation.json()["token"], "password": password},
    )
    assert accepted.status_code == 200, accepted.text
    return str(accepted.json()["principal_id"])


def _publish_policy(
    client: TestClient,
    headers: dict[str, str],
    org_unit_id: str,
    *,
    include_descendants: bool = False,
    pii_allowed: bool = False,
) -> str:
    draft = client.post(
        "/organization/department-policies/drafts",
        headers=headers,
        json={
            "org_unit_id": org_unit_id,
            "allowed_actions": ["view_snapshot", "search", "run"],
            "row_scope_refs": ["region:all"],
            "column_policy_refs": ["sales:standard"],
            "pii_allowed": pii_allowed,
            "include_descendants": include_descendants,
        },
    )
    assert draft.status_code == 200, draft.text
    published = client.post(
        f"/organization/department-policies/{draft.json()['policy_id']}/publish",
        headers=headers,
        json={"expected_version": draft.json()["version"]},
    )
    assert published.status_code == 200, published.text
    return str(draft.json()["policy_id"])


def _decision(
    client: TestClient,
    headers: dict[str, str],
    *,
    target: str,
    resource_id: str,
    **overrides: object,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "target_org_unit_id": target,
        "action": "view_snapshot",
        "resource_type": "report",
        "resource_id": resource_id,
    }
    payload.update(overrides)
    response = client.post("/organization/access/decide", headers=headers, json=payload)
    assert response.status_code == 200, response.text
    return response.json()


def _bind_resource(
    client: TestClient,
    headers: dict[str, str],
    *,
    resource_id: str,
    creator_principal_id: str,
    owner_type: str,
    owner_id: str,
    resource_type: str = "report",
    allowed_actions: tuple[str, ...] = ("view_snapshot", "search"),
    requires_pii: bool = False,
) -> dict[str, object]:
    response = client.post(
        "/organization/resource-ownership",
        headers=headers,
        json={
            "resource_type": resource_type,
            "resource_id": resource_id,
            "creator_principal_id": creator_principal_id,
            "owner_type": owner_type,
            "owner_id": owner_id,
            "allowed_actions": list(allowed_actions),
            "required_row_scope_refs": ["region:all"],
            "required_column_policy_refs": ["sales:standard"],
            "requires_pii": requires_pii,
        },
    )
    assert response.status_code == 200, response.text
    return response.json()


def test_real_postgres_organization_access_lifecycle(
    client: TestClient,
    bootstrap_owner: dict[str, str],
    organization_settings: Settings,
) -> None:
    workspace_id = bootstrap_owner["workspace_id"]
    owner_session, owner_access = login(
        client,
        email="owner@example.test",
        password="Owner-password-123!",
        workspace_id=workspace_id,
    )
    owner_headers = bearer(owner_access)
    owner_id = bootstrap_owner["principal_id"]

    root_units = client.get("/organization/units", headers=owner_headers)
    assert root_units.status_code == 200, root_units.text
    company = root_units.json()["units"][0]
    assert company["kind"] == "company"
    division = _create_unit(
        client,
        owner_headers,
        key="commerce",
        kind="division",
        name="Commerce",
        parent=str(company["org_unit_id"]),
    )
    department_a = _create_unit(
        client,
        owner_headers,
        key="sales",
        kind="department",
        name="Sales",
        parent=str(division["org_unit_id"]),
    )
    team_a = _create_unit(
        client,
        owner_headers,
        key="sales-ops",
        kind="team",
        name="Sales Operations",
        parent=str(department_a["org_unit_id"]),
    )
    department_b = _create_unit(
        client,
        owner_headers,
        key="marketing",
        kind="department",
        name="Marketing",
        parent=str(division["org_unit_id"]),
    )
    department_c = _create_unit(
        client,
        owner_headers,
        key="finance",
        kind="department",
        name="Finance",
        parent=str(division["org_unit_id"]),
    )

    versioned = client.post(
        f"/organization/units/{department_a['org_unit_id']}/versions",
        headers=owner_headers,
        json={
            "expected_version": 1,
            "parent_org_unit_id": division["org_unit_id"],
            "display_name": "Commercial Sales",
        },
    )
    assert versioned.status_code == 200
    assert versioned.json()["version"] == 2
    future_version = client.post(
        f"/organization/units/{department_a['org_unit_id']}/versions",
        headers=owner_headers,
        json={
            "expected_version": 2,
            "parent_org_unit_id": division["org_unit_id"],
            "display_name": "Premature Future Sales",
            "effective_from": (datetime.now(UTC) + timedelta(days=1)).isoformat(),
        },
    )
    assert future_version.status_code == 400
    stale = client.post(
        f"/organization/units/{department_a['org_unit_id']}/versions",
        headers=owner_headers,
        json={
            "expected_version": 1,
            "parent_org_unit_id": division["org_unit_id"],
            "display_name": "Stale Name",
        },
    )
    assert stale.status_code == 409
    cycle_or_invalid_parent = client.post(
        f"/organization/units/{division['org_unit_id']}/versions",
        headers=owner_headers,
        json={
            "expected_version": 1,
            "parent_org_unit_id": department_a["org_unit_id"],
            "display_name": "Commerce",
        },
    )
    assert cycle_or_invalid_parent.status_code in {400, 409}

    assign_owner = client.post(
        "/organization/primary-assignments",
        headers=owner_headers,
        json={"principal_id": owner_id, "org_unit_id": department_a["org_unit_id"]},
    )
    assert assign_owner.status_code == 200, assign_owner.text
    overlapping = client.post(
        "/organization/primary-assignments",
        headers=owner_headers,
        json={"principal_id": owner_id, "org_unit_id": department_b["org_unit_id"]},
    )
    assert overlapping.status_code == 409

    analyst_id = _invite(
        client,
        owner_session["csrf_token"],
        workspace_id=workspace_id,
        email="analyst@example.test",
        role="analyst",
        password="Analyst-password-123!",
    )
    admin_id = _invite(
        client,
        owner_session["csrf_token"],
        workspace_id=workspace_id,
        email="admin@example.test",
        role="workspace_admin",
        password="Admin-password-123!",
    )
    viewer_id = _invite(
        client,
        owner_session["csrf_token"],
        workspace_id=workspace_id,
        email="viewer@example.test",
        role="viewer",
        password="Viewer-password-123!",
    )
    for principal_id, unit in (
        (analyst_id, department_b),
        (admin_id, department_a),
        (viewer_id, department_b),
    ):
        response = client.post(
            "/organization/primary-assignments",
            headers=owner_headers,
            json={"principal_id": principal_id, "org_unit_id": unit["org_unit_id"]},
        )
        assert response.status_code == 200, response.text

    department_a_policy = _publish_policy(
        client,
        owner_headers,
        str(department_a["org_unit_id"]),
        include_descendants=True,
        pii_allowed=True,
    )
    _publish_policy(client, owner_headers, str(department_b["org_unit_id"]))
    _publish_policy(client, owner_headers, str(department_c["org_unit_id"]))
    policy_v2 = client.post(
        "/organization/department-policies/drafts",
        headers=owner_headers,
        json={
            "policy_id": department_a_policy,
            "org_unit_id": department_a["org_unit_id"],
            "expected_version": 1,
            "allowed_actions": ["view_snapshot", "search", "run"],
            "row_scope_refs": ["region:all"],
            "column_policy_refs": ["sales:standard"],
            "pii_allowed": True,
            "include_descendants": True,
        },
    )
    assert policy_v2.status_code == 200, policy_v2.text
    publish_v2 = client.post(
        f"/organization/department-policies/{department_a_policy}/publish",
        headers=owner_headers,
        json={"expected_version": 2},
    )
    assert publish_v2.status_code == 200, publish_v2.text
    assert publish_v2.json()["version"] == 2

    _, analyst_access = login(
        client,
        email="analyst@example.test",
        password="Analyst-password-123!",
        workspace_id=workspace_id,
    )
    _, admin_access = login(
        client,
        email="admin@example.test",
        password="Admin-password-123!",
        workspace_id=workspace_id,
    )
    _, viewer_access = login(
        client,
        email="viewer@example.test",
        password="Viewer-password-123!",
        workspace_id=workspace_id,
    )
    analyst_headers = bearer(analyst_access)
    admin_headers = bearer(admin_access)
    viewer_headers = bearer(viewer_access)
    report_a = str(uuid4())
    _bind_resource(
        client,
        owner_headers,
        resource_id=report_a,
        creator_principal_id=owner_id,
        owner_type="org_unit",
        owner_id=str(department_a["org_unit_id"]),
        allowed_actions=("view_snapshot", "search", "run"),
    )

    admin_decision = _decision(
        client,
        admin_headers,
        target=str(department_a["org_unit_id"]),
        resource_id=report_a,
    )
    assert admin_decision["allowed"] is False
    admin_denied_by = admin_decision["denied_by"]
    assert isinstance(admin_denied_by, list)
    assert "functional_permission" in admin_denied_by

    unit_leadership = client.post(
        "/organization/leadership-assignments",
        headers=owner_headers,
        json={
            "principal_id": analyst_id,
            "org_unit_id": department_a["org_unit_id"],
            "scope_mode": "unit",
            "permissions": ["report.read"],
            "reason": "Sales leadership",
        },
    )
    assert unit_leadership.status_code == 200, unit_leadership.text
    escalation = client.post(
        "/organization/leadership-assignments",
        headers=owner_headers,
        json={
            "principal_id": viewer_id,
            "org_unit_id": department_a["org_unit_id"],
            "scope_mode": "unit",
            "permissions": ["analysis.run"],
            "reason": "Must remain inside the viewer functional ceiling",
        },
    )
    assert escalation.status_code == 400
    issuer_escalation = client.post(
        "/organization/leadership-assignments",
        headers=admin_headers,
        json={
            "principal_id": analyst_id,
            "org_unit_id": department_a["org_unit_id"],
            "scope_mode": "unit",
            "permissions": ["report.read"],
            "reason": "Issuer cannot delegate a permission outside its own ceiling",
        },
    )
    assert issuer_escalation.status_code == 400
    assert _decision(
        client,
        analyst_headers,
        target=str(department_a["org_unit_id"]),
        resource_id=report_a,
    )["allowed"] is True
    assert _decision(
        client,
        analyst_headers,
        target=str(team_a["org_unit_id"]),
        resource_id=report_a,
    )["allowed"] is False

    subtree = client.post(
        "/organization/leadership-assignments",
        headers=owner_headers,
        json={
            "principal_id": analyst_id,
            "org_unit_id": department_a["org_unit_id"],
            "scope_mode": "subtree",
            "permissions": ["report.read"],
            "reason": "Sales subtree leadership",
        },
    )
    assert subtree.status_code == 200
    assert _decision(
        client,
        analyst_headers,
        target=str(team_a["org_unit_id"]),
        resource_id=report_a,
    )["allowed"] is True
    workspace_leadership = client.post(
        "/organization/leadership-assignments",
        headers=owner_headers,
        json={
            "principal_id": analyst_id,
            "org_unit_id": company["org_unit_id"],
            "scope_mode": "workspace",
            "permissions": ["report.read"],
            "reason": "Workspace-wide reporting leadership",
        },
    )
    assert workspace_leadership.status_code == 200
    report_c = str(uuid4())
    _bind_resource(
        client,
        owner_headers,
        resource_id=report_c,
        creator_principal_id=owner_id,
        owner_type="org_unit",
        owner_id=str(department_c["org_unit_id"]),
    )
    assert _decision(
        client,
        analyst_headers,
        target=str(department_c["org_unit_id"]),
        resource_id=report_c,
    )["allowed"] is True

    before_grant = _decision(
        client,
        viewer_headers,
        target=str(department_a["org_unit_id"]),
        resource_id=report_a,
    )
    assert before_grant["allowed"] is False
    grant = client.post(
        "/organization/cross-department-grants",
        headers=owner_headers,
        json={
            "subject_type": "principal",
            "subject_id": viewer_id,
            "target_org_unit_id": department_a["org_unit_id"],
            "resource_type": "report",
            "resource_id": report_a,
            "actions": ["view_snapshot", "run"],
            "reason": "Quarterly collaboration",
        },
    )
    assert grant.status_code == 200, grant.text
    assert _decision(
        client,
        viewer_headers,
        target=str(department_a["org_unit_id"]),
        resource_id=report_a,
    )["allowed"] is True
    snapshot_does_not_grant_run = _decision(
        client,
        viewer_headers,
        target=str(department_a["org_unit_id"]),
        resource_id=report_a,
        action="run",
    )
    assert snapshot_does_not_grant_run["allowed"] is False
    run_denied_by = snapshot_does_not_grant_run["denied_by"]
    assert isinstance(run_denied_by, list)
    assert run_denied_by == ["functional_permission"]
    tampered = client.post(
        "/organization/access/decide",
        headers=viewer_headers,
        json={
            "target_org_unit_id": department_a["org_unit_id"],
            "functional_permission": "report.read",
            "action": "view_snapshot",
            "resource_type": "report",
            "resource_id": str(uuid4()),
            "object_policy": True,
        },
    )
    assert tampered.status_code == 422
    pii_report = str(uuid4())
    _bind_resource(
        client,
        owner_headers,
        resource_id=pii_report,
        creator_principal_id=owner_id,
        owner_type="org_unit",
        owner_id=str(department_a["org_unit_id"]),
        requires_pii=True,
    )
    pii_denied = _decision(
        client,
        viewer_headers,
        target=str(department_a["org_unit_id"]),
        resource_id=pii_report,
    )
    assert pii_denied["allowed"] is False
    pii_denied_by = pii_denied["denied_by"]
    assert isinstance(pii_denied_by, list)
    assert "pii_policy" in pii_denied_by
    revoked = client.post(
        f"/organization/cross-department-grants/{grant.json()['grant_id']}/revoke",
        headers=owner_headers,
        json={"expected_version": 1},
    )
    assert revoked.status_code == 200
    assert _decision(
        client,
        viewer_headers,
        target=str(department_a["org_unit_id"]),
        resource_id=report_a,
    )["allowed"] is False

    now = datetime.now(UTC)
    expired = client.post(
        "/organization/cross-department-grants",
        headers=owner_headers,
        json={
            "subject_type": "principal",
            "subject_id": viewer_id,
            "target_org_unit_id": department_a["org_unit_id"],
            "actions": ["view_snapshot"],
            "reason": "Expired collaboration",
            "effective_from": (now - timedelta(days=2)).isoformat(),
            "expires_at": (now - timedelta(days=1)).isoformat(),
        },
    )
    assert expired.status_code == 200
    assert _decision(
        client,
        viewer_headers,
        target=str(department_a["org_unit_id"]),
        resource_id=report_a,
    )["allowed"] is False

    visible_resource = str(uuid4())
    hidden_resource = str(uuid4())
    visibility_resource_type = "report"
    for resource_id, creator_id, resource_owner_id in (
        (visible_resource, viewer_id, str(department_b["org_unit_id"])),
        (hidden_resource, owner_id, str(department_a["org_unit_id"])),
    ):
        _bind_resource(
            client,
            owner_headers,
            resource_id=resource_id,
            creator_principal_id=creator_id,
            owner_type="org_unit",
            owner_id=resource_owner_id,
            resource_type=visibility_resource_type,
        )
    visible = client.post(
        "/organization/resource-visibility/search",
        headers=viewer_headers,
        json={
            "action": "view_snapshot",
            "resource_type": visibility_resource_type,
            "offset": 0,
            "limit": 1,
        },
    )
    assert visible.status_code == 200, visible.text
    assert visible.json()["visible_count"] == 1
    assert [item["resource_id"] for item in visible.json()["resources"]] == [visible_resource]

    principal_draft = str(uuid4())
    bind_draft = _bind_resource(
        client,
        owner_headers,
        resource_id=principal_draft,
        creator_principal_id=viewer_id,
        owner_type="principal",
        owner_id=viewer_id,
    )
    assert bind_draft["owner_type"] == "principal"
    assert _decision(
        client,
        viewer_headers,
        target=str(department_b["org_unit_id"]),
        resource_id=principal_draft,
    )["allowed"] is True
    same_department_colleague = _decision(
        client,
        analyst_headers,
        target=str(department_b["org_unit_id"]),
        resource_id=principal_draft,
    )
    assert same_department_colleague["allowed"] is False
    colleague_denied_by = same_department_colleague["denied_by"]
    assert isinstance(colleague_denied_by, list)
    assert "object_version_policy" in colleague_denied_by
    department_report = str(uuid4())
    bind_published = _bind_resource(
        client,
        owner_headers,
        resource_id=department_report,
        creator_principal_id=viewer_id,
        owner_type="org_unit",
        owner_id=str(department_b["org_unit_id"]),
    )
    assert bind_published["owner_type"] == "org_unit"
    changed_creator = client.post(
        "/organization/resource-ownership",
        headers=owner_headers,
        json={
            "resource_type": "report",
            "resource_id": department_report,
            "creator_principal_id": admin_id,
            "owner_type": "org_unit",
            "owner_id": department_b["org_unit_id"],
            "allowed_actions": ["view_snapshot"],
        },
    )
    assert changed_creator.status_code == 400

    transfer_sensitive_report = str(uuid4())
    _bind_resource(
        client,
        owner_headers,
        resource_id=transfer_sensitive_report,
        creator_principal_id=owner_id,
        owner_type="org_unit",
        owner_id=str(department_a["org_unit_id"]),
    )
    unit_grant = client.post(
        "/organization/cross-department-grants",
        headers=owner_headers,
        json={
            "subject_type": "org_unit",
            "subject_id": department_b["org_unit_id"],
            "target_org_unit_id": department_a["org_unit_id"],
            "resource_type": "report",
            "resource_id": transfer_sensitive_report,
            "actions": ["view_snapshot"],
            "reason": "Department collaboration before transfer",
        },
    )
    assert unit_grant.status_code == 200, unit_grant.text
    assert _decision(
        client,
        viewer_headers,
        target=str(department_a["org_unit_id"]),
        resource_id=transfer_sensitive_report,
    )["allowed"] is True

    transfer = client.post(
        f"/organization/members/{viewer_id}/transfer",
        headers=owner_headers,
        json={"org_unit_id": department_c["org_unit_id"]},
    )
    assert transfer.status_code == 200, transfer.text
    assert transfer.json()["handover_tasks"] == 1
    assert _decision(
        client,
        viewer_headers,
        target=str(department_a["org_unit_id"]),
        resource_id=transfer_sensitive_report,
    )["allowed"] is False
    future_deactivation = client.post(
        f"/organization/members/{viewer_id}/deactivate",
        headers=owner_headers,
        json={
            "status": "departed",
            "effective_at": (datetime.now(UTC) + timedelta(days=1)).isoformat(),
        },
    )
    assert future_deactivation.status_code == 400
    assert client.get("/organization/units", headers=viewer_headers).status_code == 200
    deactivated = client.post(
        f"/organization/members/{viewer_id}/deactivate",
        headers=owner_headers,
        json={"status": "departed"},
    )
    assert deactivated.status_code == 200, deactivated.text
    departed_access = client.get("/organization/units", headers=viewer_headers)
    assert departed_access.status_code == 401

    with connect(organization_settings) as connection, connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT creator_principal_id, owner_type, owner_id, effective_to
            FROM organization_resource_ownership_bindings
            WHERE workspace_id = %s AND resource_type = 'report' AND resource_id = %s
            ORDER BY version DESC LIMIT 1
            """,
            (UUID(workspace_id), UUID(department_report)),
        )
        durable_owner = cursor.fetchone()
    if durable_owner is None:
        raise AssertionError("department-owned resource binding was not retained")
    durable_owner_row = cast(tuple[object, object, object, object], durable_owner)
    assert str(durable_owner_row[0]) == viewer_id
    assert durable_owner_row[1] == "org_unit"
    assert str(durable_owner_row[2]) == str(department_b["org_unit_id"])
    assert durable_owner_row[3] is None

    close_without_successor = client.post(
        f"/organization/units/{department_b['org_unit_id']}/lifecycle",
        headers=owner_headers,
        json={"expected_version": 1, "status": "merged"},
    )
    assert close_without_successor.status_code == 409
    closed = client.post(
        f"/organization/units/{department_b['org_unit_id']}/lifecycle",
        headers=owner_headers,
        json={
            "expected_version": 1,
            "status": "merged",
            "successor_org_unit_id": department_c["org_unit_id"],
        },
    )
    assert closed.status_code == 200, closed.text
    assert closed.json()["status"] == "merged"
    assert closed.json()["successor_org_unit_id"] == department_c["org_unit_id"]

    second_workspace = client.post(
        "/identity/workspaces",
        headers=owner_headers,
        json={"key": "second-workspace", "name": "Second Workspace"},
    )
    assert second_workspace.status_code == 200
    _, second_access = login(
        client,
        email="owner@example.test",
        password="Owner-password-123!",
        workspace_id=second_workspace.json()["workspace_id"],
    )
    second_units = client.get("/organization/units", headers=bearer(second_access))
    assert second_units.status_code == 200
    second_company = second_units.json()["units"][0]
    cross_workspace_parent = client.post(
        "/organization/units",
        headers=owner_headers,
        json={
            "key": "invalid-cross-workspace",
            "kind": "department",
            "display_name": "Invalid",
            "parent_org_unit_id": second_company["org_unit_id"],
        },
    )
    assert cross_workspace_parent.status_code == 404
    second_resource = str(uuid4())
    _bind_resource(
        client,
        bearer(second_access),
        resource_id=second_resource,
        creator_principal_id=owner_id,
        owner_type="org_unit",
        owner_id=str(second_company["org_unit_id"]),
    )
    cross_workspace_access = client.post(
        "/organization/access/decide",
        headers=owner_headers,
        json={
            "target_org_unit_id": second_company["org_unit_id"],
            "action": "view_snapshot",
            "resource_type": "report",
            "resource_id": second_resource,
        },
    )
    assert cross_workspace_access.status_code == 404

    with connect(organization_settings) as connection, connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT principal_id, count(*)
            FROM organization_primary_assignments
            WHERE workspace_id = %s AND effective_to IS NULL
            GROUP BY principal_id
            """,
            (UUID(workspace_id),),
        )
        assignment_counts = cast(list[tuple[object, object]], cursor.fetchall())
        assert all(int(str(count)) == 1 for _, count in assignment_counts)

    root = Path(__file__).resolve().parents[3]
    migration_env = os.environ.copy()
    migration_env.update(
        {
            "CUSTOMETRY_DATABASE_HOST": organization_settings.database_host,
            "CUSTOMETRY_DATABASE_PORT": str(organization_settings.database_port),
            "CUSTOMETRY_DATABASE_NAME": organization_settings.database_name,
            "CUSTOMETRY_DATABASE_USER": organization_settings.database_user,
            "CUSTOMETRY_DATABASE_PASSWORD_FILE": str(
                organization_settings.database_password_file
            ),
        }
    )
    for revision in ("0002_identity_auth", "head"):
        action = "upgrade" if revision == "head" else "downgrade"
        completed = subprocess.run(
            [
                "uv",
                "run",
                "alembic",
                "-c",
                "migrations/alembic.ini",
                action,
                revision,
            ],
            cwd=root,
            env=migration_env,
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0, completed.stderr
    with connect(organization_settings) as connection, connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT m.workspace_id, m.principal_id, count(a.id)
            FROM identity_memberships AS m
            LEFT JOIN organization_primary_assignments AS a
              ON a.workspace_id = m.workspace_id
             AND a.principal_id = m.principal_id
             AND a.effective_to IS NULL
            WHERE m.status = 'active'
            GROUP BY m.workspace_id, m.principal_id
            HAVING count(a.id) <> 1
            """
        )
        assert cursor.fetchall() == []
