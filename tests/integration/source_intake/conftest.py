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
def source_intake_settings(tmp_path_factory: pytest.TempPathFactory) -> Settings:
    control_password = os.environ.get("CUSTOMETRY_TEST_DATABASE_PASSWORD_FILE")
    source_password = os.environ.get("CUSTOMETRY_TEST_SOURCE_PASSWORD_FILE")
    if control_password is None or source_password is None:
        pytest.skip("real PostgreSQL control and retail source boundaries were not configured")
    bootstrap_file = tmp_path_factory.mktemp("source-intake-secrets") / "bootstrap-token"
    bootstrap_file.write_text("w14-local-bootstrap-token\n", encoding="utf-8")
    return Settings(
        environment="test",
        database_host=os.environ.get("CUSTOMETRY_TEST_DATABASE_HOST", "127.0.0.1"),
        database_port=int(os.environ.get("CUSTOMETRY_TEST_DATABASE_PORT", "55432")),
        database_name=os.environ.get("CUSTOMETRY_TEST_DATABASE_NAME", "custometry"),
        database_user=os.environ.get("CUSTOMETRY_TEST_DATABASE_USER", "custometry"),
        database_password_file=Path(control_password),
        bootstrap_token_file=bootstrap_file,
        cors_allowed_origins=["http://testserver"],
        identity_cookie_secure=False,
        identity_rate_limit_requests=1000,
        source_postgresql_host=os.environ.get("CUSTOMETRY_TEST_SOURCE_HOST", "127.0.0.1"),
        source_postgresql_port=int(os.environ.get("CUSTOMETRY_TEST_SOURCE_PORT", "55433")),
        source_postgresql_database=os.environ.get(
            "CUSTOMETRY_TEST_SOURCE_DATABASE", "northwind_retail"
        ),
        source_postgresql_user=os.environ.get("CUSTOMETRY_TEST_SOURCE_USER", "demo_reader"),
        source_postgresql_password_file=Path(source_password),
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
def clean_source_intake_database(source_intake_settings: Settings) -> None:
    with connect(source_intake_settings) as connection, connection.cursor() as cursor:
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
def source_intake_app(source_intake_settings: Settings) -> FastAPI:
    return create_app(settings=source_intake_settings)


@pytest.fixture
def client(source_intake_app: FastAPI) -> Iterator[TestClient]:
    with TestClient(source_intake_app, base_url="http://testserver") as test_client:
        yield test_client


@pytest.fixture
def bootstrap_owner(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/identity/bootstrap",
        headers={"X-Bootstrap-Token": "w14-local-bootstrap-token"},
        json={
            "email": "owner@example.test",
            "password": "Owner-password-123!",
            "workspace_key": "source-workspace",
            "workspace_name": "Source Workspace",
        },
    )
    assert response.status_code == 200, response.text
    return {key: str(value) for key, value in response.json().items()}


def login(
    client: TestClient, *, email: str, password: str, workspace_id: str
) -> tuple[dict[str, str], str]:
    response = client.post(
        "/identity/login",
        json={
            "email": email,
            "password": password,
            "workspace_id": workspace_id,
            "device_label": "source-intake-pytest",
        },
    )
    assert response.status_code == 200, response.text
    return response.json(), response.cookies["custometry_access"]


def bearer(access_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {access_token}"}
