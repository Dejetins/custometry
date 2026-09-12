"""Opt-in real HTTP proof against the explicitly prepared, owned Hybrid runtime."""

from __future__ import annotations

import json
import os
from pathlib import Path

import httpx
import pytest

from tools.custometry_quality import development_runtime as runtime


def test_prepared_analyst_http_prefix_session_and_revocation() -> None:
    if os.environ.get("CUSTOMETRY_TEST_PREPARED_HTTP") != "1":
        pytest.skip("explicit owned prepared Hybrid HTTP target required")
    root = Path.cwd()
    policy = runtime.load_policy(root)
    paths = runtime.runtime_paths(root, policy)
    state = json.loads((paths.secrets_dir / "retail-report.json").read_text())
    origin = policy.host_processes["web"].url
    with (
        httpx.Client(base_url=origin, trust_env=False) as client,
        httpx.Client(base_url=origin, trust_env=False) as admin,
    ):
        login = client.post(
            "/api/identity/login",
            json={
                "email": state["analyst_email"],
                "password": state["analyst_password"],
                "workspace_id": state["workspace_id"],
            },
        )
        assert login.status_code == 200
        cookies = {c.name: c for c in client.cookies.jar}
        assert cookies["custometry_access"].path == "/"
        assert cookies["custometry_refresh"].path == "/api/identity"
        assert cookies["custometry_csrf"].path == "/"
        assert cookies["custometry_access"].has_nonstandard_attr("HttpOnly")
        assert cookies["custometry_refresh"].has_nonstandard_attr("HttpOnly")
        assert not cookies["custometry_csrf"].has_nonstandard_attr("HttpOnly")
        assert all(c._rest.get("SameSite") == "strict" for c in cookies.values())
        cleanup = login.headers.get_list("set-cookie")
        assert sum("Path=/identity" in c and "Max-Age=0" in c for c in cleanup) == 3
        me = client.get("/api/identity/me")
        assert me.status_code == 200
        assert me.json()["principal_id"] == state["analyst_id"]
        assert me.json()["installation_admin"] is False
        assert "analysis.run" in me.json()["permissions"]
        assert "connection.manage" not in me.json()["permissions"]
        assert client.get("/api/analytics/results").status_code == 200
        csrf = login.json()["csrf_token"]
        for headers in (
            {},
            {"Origin": origin},
            {"Origin": "https://outsider.invalid", "X-CSRF-Token": csrf},
        ):
            response = client.post("/api/analytics/results", headers=headers, json={})
            assert response.status_code == 403
            assert response.json()["code"] == "CSRF_FAILED"
        assert (
            client.get("/api/identity/me", headers={"Authorization": "Basic invalid"}).status_code
            == 401
        )
        token = cookies["custometry_access"].value
        assert (
            client.get("/api/identity/me", headers={"Authorization": "Bearer " + token}).status_code
            == 200
        )
        denied = client.post(
            "/api/identity/workspaces",
            headers={"Origin": origin, "X-CSRF-Token": csrf},
            json={"key": "denied-ms003", "name": "Denied"},
        )
        assert denied.status_code == 403
        refreshed = client.post(
            "/api/identity/refresh", headers={"Origin": origin, "X-CSRF-Token": csrf}
        )
        assert refreshed.status_code == 200
        csrf = refreshed.json()["csrf_token"]
        owner = admin.post(
            "/api/identity/login",
            json={
                "email": state["admin_email"],
                "password": state["admin_password"],
                "workspace_id": state["workspace_id"],
            },
        )
        assert owner.status_code == 200
        headers = {"Origin": origin, "X-CSRF-Token": owner.json()["csrf_token"]}
        revoked = admin.delete(
            "/api/identity/sessions/" + refreshed.json()["session_id"], headers=headers
        )
        assert revoked.status_code == 204
        assert client.get("/api/analytics/results").status_code == 401
        assert admin.post("/api/identity/logout", headers=headers).status_code == 204
        assert admin.get("/api/identity/me").status_code == 401
        relogin = client.post(
            "/api/identity/login",
            json={
                "email": state["analyst_email"],
                "password": state["analyst_password"],
                "workspace_id": state["workspace_id"],
            },
        )
        assert relogin.status_code == 200
        out = client.post(
            "/api/identity/logout",
            headers={"Origin": origin, "X-CSRF-Token": relogin.json()["csrf_token"]},
        )
        assert out.status_code == 204
        assert not list(client.cookies.jar)
        assert client.get("/api/analytics/results").status_code == 401
