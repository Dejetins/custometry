from __future__ import annotations

import base64
from io import BytesIO
import json

from fastapi.testclient import TestClient
from openpyxl import Workbook

from tests.integration.source_intake.conftest import bearer, login


def create_connection(client: TestClient, access: str) -> dict[str, object]:
    response = client.post(
        "/connections",
        headers=bearer(access),
        json={
            "connector_id": "postgresql",
            "profile_ref": "retail_demo",
            "secret_ref": "retail_demo_reader",
            "display_name": "Retail demo",
        },
    )
    assert response.status_code == 200, response.text
    return response.json()


def template_payload() -> dict[str, object]:
    return {
        "name": "Retail receipt import",
        "accepted_media_types": [
            "text/csv",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ],
        "allowed_sheet_names": ["data"],
        "required_sheet_names": ["data"],
        "columns": [
            {
                "source_header": "receipt_id",
                "field_role": "receipt_id",
                "data_type": "integer",
                "required": True,
            },
            {
                "source_header": "net_amount",
                "field_role": "net_amount",
                "data_type": "decimal",
                "required": True,
            },
        ],
        "row_limit": 10,
        "file_size_limit": 100_000,
        "decimal_separator": ".",
        "date_format": "%Y-%m-%d",
        "error_policy": "reject_rows_with_report",
    }


def xlsx_formula() -> bytes:
    workbook = Workbook()
    sheet = workbook.active
    assert sheet is not None
    sheet.title = "data"
    sheet.append(["receipt_id", "net_amount"])
    sheet.append([1, "=2+2"])
    buffer = BytesIO()
    workbook.save(buffer)
    workbook.close()
    return buffer.getvalue()


def test_real_postgresql_discovery_preview_and_bounded_session(
    client: TestClient, bootstrap_owner: dict[str, str]
) -> None:
    _, access = login(
        client,
        email="owner@example.test",
        password="Owner-password-123!",
        workspace_id=bootstrap_owner["workspace_id"],
    )
    connection = create_connection(client, access)
    connection_id = str(connection["connection_id"])

    assert "secret_ref" not in connection
    assert "profile_ref" not in connection
    tested = client.post(f"/connections/{connection_id}/test", headers=bearer(access))
    assert tested.status_code == 200, tested.text
    assert tested.json()["status"] == "ready"
    assert tested.json()["capabilities"]["read_only_enforced"] is True
    assert "17" in tested.json()["capabilities"]["supported_source_versions"]

    catalog = client.get(f"/connections/{connection_id}/catalog", headers=bearer(access))
    assert catalog.status_code == 200, catalog.text
    names = {(item["schema_name"], item["object_name"]) for item in catalog.json()["objects"]}
    assert {("retail", "customers"), ("retail", "receipts"), ("retail", "receipt_items")} <= names

    preview = client.post(
        f"/connections/{connection_id}/preview",
        headers=bearer(access),
        json={
            "schema_name": "retail",
            "object_name": "customers",
            "columns": ["customer_id", "email", "loyalty_card"],
            "limit": 3,
        },
    )
    assert preview.status_code == 200, preview.text
    assert len(preview.json()["rows"]) == 3
    assert all(row["email"] in {"***", None} for row in preview.json()["rows"])
    assert all(row["loyalty_card"] in {"***", None} for row in preview.json()["rows"])

    started = client.post(f"/connections/{connection_id}/sessions", headers=bearer(access))
    assert started.status_code == 200, started.text
    session = started.json()
    assert session["state"] == "active"
    extracted = client.post(
        f"/connections/{connection_id}/extract",
        headers=bearer(access),
        json={
            "session_id": session["session_id"],
            "schema_name": "retail",
            "object_name": "receipts",
            "columns": ["receipt_id", "net_amount", "status"],
            "limit": 5_000,
        },
    )
    assert extracted.status_code == 200, extracted.text
    assert extracted.json()["row_count"] == 5_000
    assert len(extracted.json()["content_hash"]) == 64
    closed = client.post(
        f"/connections/{connection_id}/sessions/close",
        headers=bearer(access),
        json={"session_id": session["session_id"], "outcome": "committed"},
    )
    assert closed.status_code == 200, closed.text
    assert closed.json()["state"] == "committed"
    reused = client.post(
        f"/connections/{connection_id}/extract",
        headers=bearer(access),
        json={
            "session_id": session["session_id"],
            "schema_name": "retail",
            "object_name": "receipts",
            "columns": ["receipt_id"],
            "limit": 1,
        },
    )
    assert reused.status_code == 400
    assert reused.json() == {"code": "EXTRACTION_SESSION_INVALID"}


def test_identifier_injection_and_future_connector_are_rejected_without_source_damage(
    client: TestClient, bootstrap_owner: dict[str, str]
) -> None:
    _, access = login(
        client,
        email="owner@example.test",
        password="Owner-password-123!",
        workspace_id=bootstrap_owner["workspace_id"],
    )
    connection_id = str(create_connection(client, access)["connection_id"])
    attempted = client.post(
        f"/connections/{connection_id}/preview",
        headers=bearer(access),
        json={
            "schema_name": "retail",
            "object_name": "receipts; DROP TABLE retail.receipts",
            "columns": ["receipt_id"],
            "limit": 1,
        },
    )
    assert attempted.status_code == 400
    assert attempted.json() == {"code": "SOURCE_QUERY_REJECTED"}
    rediscovered = client.get(f"/connections/{connection_id}/catalog", headers=bearer(access))
    assert any(item["object_name"] == "receipts" for item in rediscovered.json()["objects"])

    future = client.post(
        "/connections",
        headers=bearer(access),
        json={
            "connector_id": "yandex_metrica",
            "profile_ref": "future_profile",
            "secret_ref": "future_secret",
            "display_name": "Not active",
        },
    )
    assert future.status_code == 422


def test_published_template_validation_rejects_hostile_csv_xlsx_and_reports_rows(
    client: TestClient, bootstrap_owner: dict[str, str]
) -> None:
    _, access = login(
        client,
        email="owner@example.test",
        password="Owner-password-123!",
        workspace_id=bootstrap_owner["workspace_id"],
    )
    created = client.post("/imports/templates", headers=bearer(access), json=template_payload())
    assert created.status_code == 200, created.text
    template_id = created.json()["template_id"]
    csv_content = b"receipt_id,net_amount\n1,10.25\n2,not-a-number\n"
    unpublished = client.post(
        f"/imports/templates/{template_id}/validate",
        headers=bearer(access),
        json={
            "media_type": "text/csv",
            "content_base64": base64.b64encode(csv_content).decode(),
        },
    )
    assert unpublished.status_code == 400
    assert unpublished.json() == {"code": "TEMPLATE_NOT_PUBLISHED"}

    published = client.post(
        f"/imports/templates/{template_id}/publish",
        headers=bearer(access),
        json={"expected_revision": 1},
    )
    assert published.status_code == 200, published.text
    assert published.json()["status"] == "published"
    assert published.json()["revision"] == 2
    validated = client.post(
        f"/imports/templates/{template_id}/validate",
        headers=bearer(access),
        json={
            "media_type": "text/csv",
            "content_base64": base64.b64encode(csv_content).decode(),
        },
    )
    assert validated.status_code == 200, validated.text
    result = validated.json()
    assert result["accepted_row_count"] == 1
    assert result["rejected_rows"] == [{"row_number": 3, "code": "TYPE_OR_REQUIRED_VALUE_INVALID"}]
    assert "not-a-number" not in json.dumps(result)

    formula_csv = b"receipt_id,net_amount\n1,=2+2\n"
    hostile_csv = client.post(
        f"/imports/templates/{template_id}/validate",
        headers=bearer(access),
        json={
            "media_type": "text/csv",
            "content_base64": base64.b64encode(formula_csv).decode(),
        },
    )
    assert hostile_csv.status_code == 400
    assert hostile_csv.json() == {"code": "FILE_FORMULA_REJECTED"}
    hostile_xlsx = client.post(
        f"/imports/templates/{template_id}/validate",
        headers=bearer(access),
        json={
            "media_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "content_base64": base64.b64encode(xlsx_formula()).decode(),
        },
    )
    assert hostile_xlsx.status_code == 400
    assert hostile_xlsx.json() == {"code": "FILE_FORMULA_REJECTED"}


def test_template_permissions_and_workspace_visibility_fail_closed(
    client: TestClient, bootstrap_owner: dict[str, str]
) -> None:
    _, owner_access = login(
        client,
        email="owner@example.test",
        password="Owner-password-123!",
        workspace_id=bootstrap_owner["workspace_id"],
    )
    connection = create_connection(client, owner_access)
    invitation = client.post(
        "/identity/invitations",
        headers=bearer(owner_access),
        json={
            "workspace_id": bootstrap_owner["workspace_id"],
            "email": "analyst@example.test",
            "roles": ["analyst"],
            "expires_in_hours": 24,
        },
    )
    assert invitation.status_code == 200, invitation.text
    accepted = client.post(
        "/identity/invitations/accept",
        json={
            "token": invitation.json()["token"],
            "password": "Analyst-password-123!",
        },
    )
    assert accepted.status_code == 200, accepted.text
    _, analyst_access = login(
        client,
        email="analyst@example.test",
        password="Analyst-password-123!",
        workspace_id=bootstrap_owner["workspace_id"],
    )
    forbidden_template = client.post(
        "/imports/templates", headers=bearer(analyst_access), json=template_payload()
    )
    assert forbidden_template.status_code == 403
    assert forbidden_template.json() == {"code": "FORBIDDEN"}

    second = client.post(
        "/identity/workspaces",
        headers=bearer(owner_access),
        json={"key": "other-workspace", "name": "Other Workspace"},
    )
    assert second.status_code == 200, second.text
    _, second_access = login(
        client,
        email="owner@example.test",
        password="Owner-password-123!",
        workspace_id=second.json()["workspace_id"],
    )
    hidden = client.get(
        f"/connections/{connection['connection_id']}/catalog", headers=bearer(second_access)
    )
    assert hidden.status_code == 404
    assert hidden.json() == {"code": "NOT_FOUND"}
