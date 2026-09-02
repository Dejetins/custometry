# pyright: reportUnknownArgumentType=false, reportUnknownMemberType=false, reportUnknownVariableType=false
from __future__ import annotations

from datetime import UTC, datetime, timedelta
import json
from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from custometry_api.config import Settings
from packages.contracts.people import ContributorDomainEvent
from packages.identity_access.application.contributor_activity import ContributorActivityProjector
from packages.identity_access.infrastructure.contributor_postgres import (
    PostgresContributorProjection,
)
from tests.integration.organization_access.conftest import bearer, connect, login


def _create_unit(
    client: TestClient,
    headers: dict[str, str],
    *,
    key: str,
    kind: str,
    display_name: str,
    parent_org_unit_id: str | None,
) -> dict[str, object]:
    response = client.post(
        "/organization/units",
        headers=headers,
        json={
            "key": key,
            "kind": kind,
            "display_name": display_name,
            "parent_org_unit_id": parent_org_unit_id,
        },
    )
    assert response.status_code == 200, response.text
    return response.json()


def _invite(
    client: TestClient,
    *,
    csrf_token: str,
    owner_access: str,
    workspace_id: str,
    email: str,
    role: str,
) -> str:
    invitation = client.post(
        "/identity/invitations",
        headers={
            "Authorization": f"Bearer {owner_access}",
            "Origin": "http://testserver",
            "X-CSRF-Token": csrf_token,
        },
        json={"workspace_id": workspace_id, "email": email, "roles": [role]},
    )
    assert invitation.status_code == 200, invitation.text
    accepted = client.post(
        "/identity/invitations/accept",
        json={"token": invitation.json()["token"], "password": "Member-password-123!"},
    )
    assert accepted.status_code == 200, accepted.text
    return str(accepted.json()["principal_id"])


def _assign(
    client: TestClient, headers: dict[str, str], *, principal_id: str, org_unit_id: str
) -> None:
    response = client.post(
        "/organization/primary-assignments",
        headers=headers,
        json={"principal_id": principal_id, "org_unit_id": org_unit_id},
    )
    assert response.status_code == 200, response.text


def _publish_policy(client: TestClient, headers: dict[str, str], org_unit_id: str) -> None:
    draft = client.post(
        "/organization/department-policies/drafts",
        headers=headers,
        json={
            "org_unit_id": org_unit_id,
            "allowed_actions": ["view_snapshot", "search"],
            "row_scope_refs": [],
            "column_policy_refs": [],
            "pii_allowed": False,
            "include_descendants": True,
        },
    )
    assert draft.status_code == 200, draft.text
    published = client.post(
        f"/organization/department-policies/{draft.json()['policy_id']}/publish",
        headers=headers,
        json={"expected_version": draft.json()["version"]},
    )
    assert published.status_code == 200, published.text


def _bind_resource(
    client: TestClient,
    headers: dict[str, str],
    *,
    resource_id: UUID,
    creator_principal_id: str,
    owner_id: str,
    requires_pii: bool,
) -> None:
    response = client.post(
        "/organization/resource-ownership",
        headers=headers,
        json={
            "resource_type": "report",
            "resource_id": str(resource_id),
            "creator_principal_id": creator_principal_id,
            "owner_type": "org_unit",
            "owner_id": owner_id,
            "allowed_actions": ["view_snapshot", "search"],
            "required_row_scope_refs": [],
            "required_column_policy_refs": [],
            "requires_pii": requires_pii,
        },
    )
    assert response.status_code == 200, response.text


def _grant(
    client: TestClient,
    headers: dict[str, str],
    *,
    principal_id: str,
    target_org_unit_id: str,
    actions: list[str],
    resource_id: UUID | None = None,
) -> None:
    response = client.post(
        "/organization/cross-department-grants",
        headers=headers,
        json={
            "subject_type": "principal",
            "subject_id": principal_id,
            "target_org_unit_id": target_org_unit_id,
            "resource_type": "report" if resource_id is not None else None,
            "resource_id": str(resource_id) if resource_id is not None else None,
            "actions": actions,
            "reason": "W17 bounded projection proof",
        },
    )
    assert response.status_code == 200, response.text


def _event(
    *,
    workspace_id: UUID,
    principal_id: UUID,
    occurred_at: datetime,
    event_type: str,
    resource_id: UUID,
    title: str,
) -> ContributorDomainEvent:
    return ContributorDomainEvent(
        event_id=uuid4(),
        workspace_id=workspace_id,
        principal_id=principal_id,
        event_type=event_type,  # type: ignore[arg-type]
        occurred_at=occurred_at,
        resource_type="report",
        resource_id=resource_id,
        safe_resource_title=title,
    )


def test_real_postgresql_rebuild_idempotency_and_authenticated_people_variants(
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
    root = client.get("/organization/units", headers=owner_headers).json()["units"][0]
    division = _create_unit(
        client,
        owner_headers,
        key="commercial",
        kind="division",
        display_name="Commercial",
        parent_org_unit_id=str(root["org_unit_id"]),
    )
    department_a = _create_unit(
        client,
        owner_headers,
        key="sales",
        kind="department",
        display_name="Sales",
        parent_org_unit_id=str(division["org_unit_id"]),
    )
    department_b = _create_unit(
        client,
        owner_headers,
        key="marketing",
        kind="department",
        display_name="Marketing",
        parent_org_unit_id=str(division["org_unit_id"]),
    )

    members = {
        "target": ("target@example.test", "analyst", department_a),
        "leader": ("leader@example.test", "analyst", department_b),
        "grantee": ("grantee@example.test", "viewer", department_b),
        "viewer": ("viewer@example.test", "viewer", department_a),
        "admin": ("admin@example.test", "workspace_admin", department_a),
    }
    principal_ids: dict[str, str] = {}
    headers: dict[str, dict[str, str]] = {}
    for key, (email, role, department) in members.items():
        principal_id = _invite(
            client,
            csrf_token=owner_session["csrf_token"],
            owner_access=owner_access,
            workspace_id=workspace_id,
            email=email,
            role=role,
        )
        principal_ids[key] = principal_id
        _assign(
            client,
            owner_headers,
            principal_id=principal_id,
            org_unit_id=str(department["org_unit_id"]),
        )
        _, access = login(
            client,
            email=email,
            password="Member-password-123!",
            workspace_id=workspace_id,
        )
        headers[key] = bearer(access)

    _publish_policy(client, owner_headers, str(department_a["org_unit_id"]))
    _publish_policy(client, owner_headers, str(department_b["org_unit_id"]))
    visible_report = uuid4()
    hidden_pii_report = uuid4()
    _bind_resource(
        client,
        owner_headers,
        resource_id=visible_report,
        creator_principal_id=principal_ids["target"],
        owner_id=str(department_a["org_unit_id"]),
        requires_pii=False,
    )
    _bind_resource(
        client,
        owner_headers,
        resource_id=hidden_pii_report,
        creator_principal_id=principal_ids["target"],
        owner_id=str(department_a["org_unit_id"]),
        requires_pii=True,
    )

    leadership = client.post(
        "/organization/leadership-assignments",
        headers=owner_headers,
        json={
            "principal_id": principal_ids["leader"],
            "org_unit_id": department_a["org_unit_id"],
            "scope_mode": "unit",
            "permissions": ["organization.activity.read", "report.read"],
            "reason": "Sales contributor visibility",
        },
    )
    assert leadership.status_code == 200, leadership.text
    _grant(
        client,
        owner_headers,
        principal_id=principal_ids["grantee"],
        target_org_unit_id=str(department_a["org_unit_id"]),
        actions=["organization.activity.read"],
    )
    _grant(
        client,
        owner_headers,
        principal_id=principal_ids["grantee"],
        target_org_unit_id=str(department_a["org_unit_id"]),
        actions=["view_snapshot"],
        resource_id=visible_report,
    )

    observed_at = datetime.now(UTC).replace(microsecond=0)
    profile = ContributorDomainEvent(
        event_id=uuid4(),
        workspace_id=UUID(workspace_id),
        principal_id=UUID(principal_ids["target"]),
        event_type="profile.published",
        occurred_at=observed_at - timedelta(days=5),
        display_name="Target Contributor",
        title="Senior Analyst",
        title_visible=True,
        contribution_labels=("maintainer", "reviewer"),
        expertise_domains=("sales",),
    )
    events = (
        profile,
        _event(
            workspace_id=UUID(workspace_id),
            principal_id=UUID(principal_ids["target"]),
            occurred_at=observed_at - timedelta(days=4),
            event_type="resource.published",
            resource_id=visible_report,
            title="Visible sales review",
        ),
        _event(
            workspace_id=UUID(workspace_id),
            principal_id=UUID(principal_ids["target"]),
            occurred_at=observed_at - timedelta(days=2),
            event_type="resource.materially_updated",
            resource_id=visible_report,
            title="Visible sales review",
        ),
        *tuple(
            _event(
                workspace_id=UUID(workspace_id),
                principal_id=UUID(principal_ids["target"]),
                occurred_at=observed_at - timedelta(days=1, seconds=index),
                event_type="resource.published",
                resource_id=hidden_pii_report,
                title="Hidden PII compensation report",
            )
            for index in range(5)
        ),
    )
    projection = PostgresContributorProjection(lambda: connect(organization_settings))
    projector = ContributorActivityProjector(projection)
    first = projector.project(events, rebuilt_at=observed_at)
    second = projector.project(events, rebuilt_at=observed_at + timedelta(seconds=1))
    third = projector.rebuild(
        UUID(workspace_id), rebuilt_at=observed_at + timedelta(seconds=2)
    )
    assert first.event_count == second.event_count == third.event_count == len(events)
    assert first.bucket_count == second.bucket_count == third.bucket_count == 3
    assert first.projection_version == second.projection_version == third.projection_version

    expected_variants = {
        "target": "self",
        "leader": "leader",
        "grantee": "grantee",
        "viewer": "public",
    }
    for actor, expected_variant in expected_variants.items():
        response = client.get(
            f"/people/contributors/{principal_ids['target']}", headers=headers[actor]
        )
        assert response.status_code == 200, (actor, response.text)
        payload = response.json()
        assert payload["view_variant"] == expected_variant
        assert payload["visible_resource_count"] == 1
        assert payload["visible_resources"][0]["title"] == "Visible sales review"
        if expected_variant == "public":
            assert payload["activity"] is None
        else:
            assert payload["activity"]["windows"][0]["published_count"] == 1
            assert payload["activity"]["windows"][0]["materially_updated_count"] == 1
        serialized = json.dumps(payload, sort_keys=True).casefold()
        assert "hidden pii compensation" not in serialized
        assert "example.test" not in serialized
        assert "raw_audit" not in serialized
        assert "ranking" not in serialized
        assert "productivity" not in serialized

    listing = client.get("/people/contributors", headers=headers["viewer"])
    assert listing.status_code == 200
    assert listing.json()["visible_count"] == 1
    assert len(listing.json()["people"]) == 1

    admin = client.get(
        f"/people/contributors/{principal_ids['target']}", headers=headers["admin"]
    )
    assert admin.status_code == 404
    assert admin.json() == {"code": "NOT_FOUND"}
    assert client.get("/people/contributors", headers=headers["admin"]).json() == {
        "people": [],
        "visible_count": 0,
    }
    assert client.get(
        f"/people/contributors/{uuid4()}", headers=headers["viewer"]
    ).status_code == 404

    with connect(organization_settings) as connection, connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
              (SELECT count(*) FROM identity_contributor_projection_events
               WHERE workspace_id = %s),
              (SELECT count(*) FROM identity_contributor_activity_buckets
               WHERE workspace_id = %s),
              (SELECT count(*) FROM identity_contributor_profiles
               WHERE workspace_id = %s)
            """,
            (workspace_id, workspace_id, workspace_id),
        )
        assert cursor.fetchone() == (len(events), 3, 1)
