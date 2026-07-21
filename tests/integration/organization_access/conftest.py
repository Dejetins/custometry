from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path

import psycopg
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from custometry_api.config import Settings
from custometry_api.main import create_app


@pytest.fixture(scope="session")
def organization_settings(tmp_path_factory: pytest.TempPathFactory) -> Settings:
    password_file_value = os.environ.get("CUSTOMETRY_TEST_DATABASE_PASSWORD_FILE")
    if password_file_value is None:
        pytest.skip("real PostgreSQL organization boundary was not configured")
    bootstrap_file = tmp_path_factory.mktemp("organization-secrets") / "bootstrap-token"
    bootstrap_file.write_text("w13-local-bootstrap-token\n", encoding="utf-8")
    return Settings(
        environment="test",
        database_host=os.environ.get("CUSTOMETRY_TEST_DATABASE_HOST", "127.0.0.1"),
        database_port=int(os.environ.get("CUSTOMETRY_TEST_DATABASE_PORT", "55432")),
        database_name=os.environ.get("CUSTOMETRY_TEST_DATABASE_NAME", "custometry"),
        database_user=os.environ.get("CUSTOMETRY_TEST_DATABASE_USER", "custometry"),
        database_password_file=Path(password_file_value),
        bootstrap_token_file=bootstrap_file,
        cors_allowed_origins=["http://testserver"],
        identity_cookie_secure=False,
        identity_rate_limit_requests=1000,
    )


def connect(settings: Settings) -> psycopg.Connection[object]:
    return psycopg.connect(
        host=settings.database_host,
        port=settings.database_port,
        dbname=settings.database_name,
        user=settings.database_user,
        password=settings.read_database_password(),
        connect_timeout=settings.database_connect_timeout_seconds,
    )


@pytest.fixture(autouse=True)
def clean_organization_database(organization_settings: Settings) -> None:
    with connect(organization_settings) as connection, connection.cursor() as cursor:
        cursor.execute(
            """
            TRUNCATE TABLE
                identity_audit_events,
                identity_password_resets,
                identity_api_tokens,
                identity_invitations,
                identity_refresh_history,
                identity_sessions,
                identity_bootstrap_state,
                identity_role_assignments,
                identity_memberships,
                identity_workspaces,
                identity_principals
            CASCADE
            """
        )


@pytest.fixture
def organization_app(organization_settings: Settings) -> FastAPI:
    return create_app(settings=organization_settings)


@pytest.fixture
def client(organization_app: FastAPI) -> Iterator[TestClient]:
    with TestClient(organization_app, base_url="http://testserver") as test_client:
        yield test_client


@pytest.fixture
def bootstrap_owner(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/identity/bootstrap",
        headers={"X-Bootstrap-Token": "w13-local-bootstrap-token"},
        json={
            "email": "owner@example.test",
            "password": "Owner-password-123!",
            "workspace_key": "primary-workspace",
            "workspace_name": "Primary Workspace",
        },
    )
    assert response.status_code == 200, response.text
    return {key: str(value) for key, value in response.json().items()}


def login(
    client: TestClient,
    *,
    email: str,
    password: str,
    workspace_id: str,
) -> tuple[dict[str, str], str]:
    response = client.post(
        "/identity/login",
        json={
            "email": email,
            "password": password,
            "workspace_id": workspace_id,
            "device_label": "organization-pytest",
        },
    )
    assert response.status_code == 200, response.text
    return response.json(), response.cookies["custometry_access"]


def bearer(access_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {access_token}"}
