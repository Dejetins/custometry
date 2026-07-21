from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from uuid import UUID, uuid4

from fastapi import FastAPI
from fastapi.testclient import TestClient

from custometry_api.config import Settings
from packages.identity_access.application.service import IdentityFailure, IdentityService
from packages.identity_access.infrastructure.postgres import PostgresIdentityRepository
from tests.integration.identity_access.conftest import browser_headers, connect, login


def test_bootstrap_is_single_winner_under_concurrency(identity_settings: Settings) -> None:
    service = IdentityService(
        PostgresIdentityRepository(lambda: connect(identity_settings)),
        bootstrap_secret="w12-local-bootstrap-token",
    )

    def attempt(index: int) -> str:
        try:
            service.bootstrap(
                presented_secret="w12-local-bootstrap-token",
                email=f"owner-{index}@example.test",
                password="Owner-password-123!",
                workspace_key=f"workspace-{index}",
                workspace_name=f"Workspace {index}",
            )
        except IdentityFailure as exc:
            return exc.code
        return "created"

    with ThreadPoolExecutor(max_workers=2) as executor:
        outcomes = sorted(executor.map(attempt, (1, 2)))

    assert outcomes == ["BOOTSTRAP_UNAVAILABLE", "created"]


def test_local_auth_workspace_invitation_session_and_token_flow(
    identity_app: FastAPI,
    client: TestClient,
    bootstrap_owner: dict[str, str],
    identity_settings: Settings,
) -> None:
    workspace_id = bootstrap_owner["workspace_id"]
    owner_login = login(
        client,
        email="owner@example.test",
        password="Owner-password-123!",
        workspace_id=workspace_id,
    )
    assert owner_login.status_code == 200, owner_login.text
    owner_csrf = owner_login.json()["csrf_token"]
    owner_access = owner_login.cookies["custometry_access"]
    owner_refresh = owner_login.cookies["custometry_refresh"]

    me = client.get("/identity/me")
    assert me.status_code == 200
    assert me.json()["workspace_id"] == workspace_id
    assert me.json()["installation_admin"] is True
    assert "workspace.members.manage" in me.json()["permissions"]

    second_workspace = client.post(
        "/identity/workspaces",
        headers=browser_headers(owner_csrf),
        json={"key": "second-workspace", "name": "Second Workspace"},
    )
    assert second_workspace.status_code == 200, second_workspace.text
    second_workspace_id = second_workspace.json()["workspace_id"]

    cross_workspace = client.get(f"/identity/workspaces/{second_workspace_id}/members")
    assert cross_workspace.status_code == 404
    assert cross_workspace.json() == {"code": "NOT_FOUND"}

    invitation = client.post(
        "/identity/invitations",
        headers=browser_headers(owner_csrf),
        json={
            "workspace_id": workspace_id,
            "email": "analyst@example.test",
            "roles": ["analyst"],
            "expires_in_hours": 24,
        },
    )
    assert invitation.status_code == 200, invitation.text
    assert invitation.headers["cache-control"] == "no-store"
    invitation_token = invitation.json()["token"]

    accepted = client.post(
        "/identity/invitations/accept",
        json={"token": invitation_token, "password": "Analyst-password-123!"},
    )
    assert accepted.status_code == 200, accepted.text
    analyst_id = accepted.json()["principal_id"]

    analyst_client = TestClient(identity_app, base_url="http://testserver")
    analyst_login = login(
        analyst_client,
        email="analyst@example.test",
        password="Analyst-password-123!",
        workspace_id=workspace_id,
    )
    assert analyst_login.status_code == 200, analyst_login.text
    analyst_csrf = analyst_login.json()["csrf_token"]
    denied_invite = analyst_client.post(
        "/identity/invitations",
        headers=browser_headers(analyst_csrf),
        json={
            "workspace_id": workspace_id,
            "email": "viewer@example.test",
            "roles": ["viewer"],
        },
    )
    assert denied_invite.status_code == 403
    assert denied_invite.json() == {"code": "FORBIDDEN"}

    analyst_sessions = client.get(f"/identity/sessions?principal_id={analyst_id}")
    assert analyst_sessions.status_code == 200
    assert len(analyst_sessions.json()["sessions"]) == 1
    revoke_analyst_session = client.delete(
        f"/identity/sessions/{analyst_sessions.json()['sessions'][0]['id']}",
        headers=browser_headers(owner_csrf),
    )
    assert revoke_analyst_session.status_code == 204

    revocable_invitation = client.post(
        "/identity/invitations",
        headers=browser_headers(owner_csrf),
        json={
            "workspace_id": workspace_id,
            "email": "viewer@example.test",
            "roles": ["viewer"],
        },
    )
    assert revocable_invitation.status_code == 200
    revoked_invitation_token = revocable_invitation.json()["token"]
    revoked = client.delete(
        f"/identity/invitations/{revocable_invitation.json()['invitation_id']}",
        headers=browser_headers(owner_csrf),
    )
    assert revoked.status_code == 204
    rejected_acceptance = client.post(
        "/identity/invitations/accept",
        json={"token": revoked_invitation_token, "password": "Viewer-password-123!"},
    )
    assert rejected_acceptance.status_code == 401
    assert rejected_acceptance.json() == {"code": "INVITATION_INVALID"}

    api_token = client.post(
        "/identity/api-tokens",
        headers=browser_headers(owner_csrf),
        json={"name": "read-only", "scopes": ["workspace.read"], "expires_in_hours": 2},
    )
    assert api_token.status_code == 200, api_token.text
    assert api_token.headers["cache-control"] == "no-store"
    raw_api_token = api_token.json()["token"]
    api_me = client.get("/identity/me", headers={"Authorization": f"Bearer {raw_api_token}"})
    assert api_me.status_code == 200
    assert api_me.json()["token_kind"] == "api_token"
    assert api_me.json()["permissions"] == ["workspace.read"]

    sessions = client.get("/identity/sessions")
    assert sessions.status_code == 200
    assert len(sessions.json()["sessions"]) == 1

    refreshed = client.post(
        "/identity/refresh",
        headers=browser_headers(owner_csrf),
    )
    assert refreshed.status_code == 200, refreshed.text
    new_access = refreshed.cookies["custometry_access"]
    new_csrf = refreshed.json()["csrf_token"]

    replay_client = TestClient(identity_app, base_url="http://testserver")
    replay_client.cookies.set("custometry_refresh", owner_refresh, path="/identity")
    replay = replay_client.post(
        "/identity/refresh",
        headers=browser_headers(owner_csrf),
    )
    assert replay.status_code == 401
    assert replay.json() == {"code": "REFRESH_REUSE_DETECTED"}
    revoked_family = replay_client.get(
        "/identity/me", headers={"Authorization": f"Bearer {new_access}"}
    )
    assert revoked_family.status_code == 401

    owner_relogin = login(
        client,
        email="owner@example.test",
        password="Owner-password-123!",
        workspace_id=workspace_id,
    )
    assert owner_relogin.status_code == 200
    logout_csrf = owner_relogin.json()["csrf_token"]
    logout_access = owner_relogin.cookies["custometry_access"]
    logout_response = client.post("/identity/logout", headers=browser_headers(logout_csrf))
    assert logout_response.status_code == 204
    assert (
        client.get("/identity/me", headers={"Authorization": f"Bearer {logout_access}"}).status_code
        == 401
    )

    with connect(identity_settings) as connection, connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT p.password_hash, i.token_hash, t.token_hash,
                   array_agg(s.access_token_hash), array_agg(s.refresh_token_hash)
            FROM identity_principals AS p
            CROSS JOIN identity_invitations AS i
            CROSS JOIN identity_api_tokens AS t
            CROSS JOIN identity_sessions AS s
            WHERE p.id = %s
            GROUP BY p.password_hash, i.token_hash, t.token_hash
            """,
            (UUID(analyst_id),),
        )
        persisted = repr(cursor.fetchone())
    for secret in (
        "Analyst-password-123!",
        invitation_token,
        revoked_invitation_token,
        raw_api_token,
        owner_access,
        owner_refresh,
        new_access,
        new_csrf,
    ):
        assert secret not in persisted


def test_password_reset_and_change_revoke_sessions(
    identity_app: FastAPI,
    client: TestClient,
    bootstrap_owner: dict[str, str],
) -> None:
    workspace_id = bootstrap_owner["workspace_id"]
    owner_login = login(
        client,
        email="owner@example.test",
        password="Owner-password-123!",
        workspace_id=workspace_id,
    )
    owner_csrf = owner_login.json()["csrf_token"]
    members = client.get(f"/identity/workspaces/{workspace_id}/members")
    owner_id = members.json()["members"][0]["id"]

    out_of_scope_reset = client.post(
        "/identity/password/resets",
        headers=browser_headers(owner_csrf),
        json={"principal_id": str(uuid4()), "expires_in_minutes": 30},
    )
    assert out_of_scope_reset.status_code == 404
    assert out_of_scope_reset.json() == {"code": "NOT_FOUND"}

    reset = client.post(
        "/identity/password/resets",
        headers=browser_headers(owner_csrf),
        json={"principal_id": owner_id, "expires_in_minutes": 30},
    )
    assert reset.status_code == 200, reset.text
    assert reset.headers["cache-control"] == "no-store"
    consumed = client.post(
        "/identity/password/resets/consume",
        json={"token": reset.json()["token"], "new_password": "Reset-password-123!"},
    )
    assert consumed.status_code == 200
    assert (
        login(
            client,
            email="owner@example.test",
            password="Owner-password-123!",
            workspace_id=workspace_id,
        ).status_code
        == 401
    )
    relogin = login(
        client,
        email="owner@example.test",
        password="Reset-password-123!",
        workspace_id=workspace_id,
    )
    assert relogin.status_code == 200
    access = relogin.cookies["custometry_access"]
    changed = client.post(
        "/identity/password/change",
        headers=browser_headers(relogin.json()["csrf_token"]),
        json={
            "current_password": "Reset-password-123!",
            "new_password": "Changed-password-123!",
        },
    )
    assert changed.status_code == 204, changed.text
    assert (
        client.get("/identity/me", headers={"Authorization": f"Bearer {access}"}).status_code == 401
    )
    assert (
        login(
            client,
            email="owner@example.test",
            password="Changed-password-123!",
            workspace_id=workspace_id,
        ).status_code
        == 200
    )
