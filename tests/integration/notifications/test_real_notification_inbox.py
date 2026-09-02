from __future__ import annotations

import time
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from custometry_api.config import Settings
from custometry_api.notifications.router import create_notifications_app
from packages.contracts.execution import ExecutionActor, ExecutionTerminalEventOutboxPort
from packages.contracts.notifications import (
    AuditIntent,
    DeepLinkDescriptor,
    NOTIFICATIONS_API_VERSION,
    NotificationActor,
    NotificationEvent,
    NotificationFailure,
    RecipientCandidate,
)
from packages.execution.infrastructure.control_postgres import PostgresExecutionControlStore
from packages.identity_access.domain.policy import Actor
from packages.notifications.application.service import (
    ExecutionTerminalNotificationProjector,
    NotificationInboxService,
)
from packages.notifications.infrastructure.postgres import PostgresNotificationStore
from tests.integration.notifications.conftest import (
    NotificationBoundaries,
    NotificationRuntime,
    migrate,
)


class TokenIdentity:
    def __init__(self, actors: dict[str, Actor]) -> None:
        self.actors = actors

    def authenticate(self, token: str) -> Actor:
        try:
            return self.actors[token]
        except KeyError as exc:
            raise RuntimeError("AUTHENTICATION_FAILED") from exc


class DynamicAccess:
    def __init__(self) -> None:
        self.resource_grants: set[tuple[UUID, UUID, str, str]] = set()
        self.link_grants: set[tuple[UUID, UUID, str, str]] = set()

    def require(self, actor: NotificationActor, action: str) -> None:
        if action not in actor.permissions:
            raise NotificationFailure("FORBIDDEN")

    @staticmethod
    def _key(
        actor: NotificationActor,
        workspace_id: UUID,
        resource_type: str,
        resource_id: str,
    ) -> tuple[UUID, UUID, str, str]:
        return actor.principal_id, workspace_id, resource_type, resource_id

    def can_access(
        self,
        actor: NotificationActor,
        *,
        workspace_id: UUID,
        resource_type: str,
        resource_id: str,
    ) -> bool:
        return self._key(actor, workspace_id, resource_type, resource_id) in self.resource_grants

    def can_disclose_deep_link(
        self,
        actor: NotificationActor,
        *,
        workspace_id: UUID,
        resource_type: str,
        resource_id: str,
        deep_link: DeepLinkDescriptor,
    ) -> bool:
        del deep_link
        return self._key(actor, workspace_id, resource_type, resource_id) in self.link_grants

    def grant(
        self,
        principal_id: UUID,
        workspace_id: UUID,
        resource_type: str,
        resource_id: str,
        *,
        deep_link: bool = True,
    ) -> None:
        key = principal_id, workspace_id, resource_type, resource_id
        self.resource_grants.add(key)
        if deep_link:
            self.link_grants.add(key)


class DynamicRecipients:
    def __init__(self) -> None:
        self.recipients: dict[UUID, tuple[UUID, ...]] = {}

    def eligible_recipients(self, event: NotificationEvent) -> tuple[RecipientCandidate, ...]:
        return tuple(
            RecipientCandidate(item, "identity-policy-v1", "preferences:run:v1")
            for item in self.recipients.get(event.event_id, ())
        )


class RecordingAudit:
    def __init__(self) -> None:
        self.intents: list[AuditIntent] = []

    def append(self, intent: AuditIntent) -> None:
        self.intents.append(intent)


def actors(runtime: NotificationRuntime) -> dict[str, Actor]:
    return {
        "reader": Actor(
            runtime.reader_id,
            runtime.workspace_id,
            "reader@example.invalid",
            frozenset({"notification.read", "run.read"}),
        ),
        "acknowledger": Actor(
            runtime.acknowledger_id,
            runtime.workspace_id,
            "ack@example.invalid",
            frozenset({"notification.read", "notification.acknowledge", "run.read"}),
        ),
        "no-permission": Actor(
            runtime.outsider_id,
            runtime.workspace_id,
            "outsider@example.invalid",
            frozenset({"run.read"}),
        ),
    }


def headers(token: str, *, request_id: str = "w37-request") -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "X-Request-ID": request_id,
        "X-Contract-Version": NOTIFICATIONS_API_VERSION,
    }


def boundary(runtime: NotificationRuntime):
    store = PostgresNotificationStore(runtime.connect)
    access = DynamicAccess()
    recipients = DynamicRecipients()
    audit = RecordingAudit()
    service = NotificationInboxService(
        store,
        access,
        recipients=recipients,
        audit=audit,
    )
    app = create_notifications_app(
        Settings(version="0.1.0-dev.0"),
        identity_service=TokenIdentity(actors(runtime)),  # type: ignore[arg-type]
        notification_service=service,
    )
    return TestClient(app), service, store, access, recipients, audit


def notification_event(
    *,
    workspace_id: UUID,
    resource_id: str,
    occurred_at: datetime,
    message_code: str,
    event_id: UUID | None = None,
    group_key: str | None = None,
    severity: str = "critical",
    resolved: bool = False,
) -> NotificationEvent:
    return NotificationEvent(
        event_id=event_id or uuid4(),
        source_owner="execution_control",
        source_type="run.terminal.v1",
        source_version=1,
        workspace_id=workspace_id,
        resource_type="run",
        resource_id=resource_id,
        severity=severity,  # type: ignore[arg-type]
        category="run",
        occurred_at=occurred_at,
        message_code=message_code,
        message_parameters=(("state_code", message_code),),
        group_key=group_key or f"run:{resource_id}",
        deep_link=DeepLinkDescriptor("UI-OPS-002", (("run_id", resource_id),)),
        trace_id=f"trace-{resource_id}",
        resolved=resolved,
    )


def test_real_w38_failure_stuck_and_recovery_converge_when_repeated_out_of_order(
    notification_runtime: NotificationRuntime,
) -> None:
    client, service, _, access, recipients, _ = boundary(notification_runtime)
    execution = PostgresExecutionControlStore(notification_runtime.connect)
    event_port: ExecutionTerminalEventOutboxPort = execution
    projector = ExecutionTerminalNotificationProjector(service)
    execution_actor = ExecutionActor(
        notification_runtime.reader_id,
        notification_runtime.workspace_id,
        frozenset({"run.read", "run.retry"}),
        "identity-policy-v1",
    )

    stuck = execution.create_run(
        workspace_id=notification_runtime.workspace_id,
        owner_principal_id=notification_runtime.reader_id,
        execution_kind="ingestion",
        safe_title="W38 safe stuck run",
        request_id="w38-create-stuck",
        policy_version="identity-policy-v1",
    )
    _, stuck_attempts = execution.get_run(execution_actor, "workspace", stuck.run_id)
    stuck_claim = execution.claim_attempt(
        stuck_attempts[0].attempt_id,
        worker_id="w38-public-worker",
        lease_seconds=0,
        request_id="w38-claim-stuck",
    )
    assert execution.reconcile(
        observed_at=datetime.now(UTC) + timedelta(seconds=1),
        request_id="w38-reconcile-stuck",
    ) == ("EXPIRED_LEASE_FENCED_AND_RETRIED",)

    failed = execution.create_run(
        workspace_id=notification_runtime.workspace_id,
        owner_principal_id=notification_runtime.reader_id,
        execution_kind="analytics",
        safe_title="W38 safe failing run",
        safe_trace_id="trace-w38-terminal",
        request_id="w38-create-failure",
        policy_version="identity-policy-v1",
    )
    _, attempts = execution.get_run(execution_actor, "workspace", failed.run_id)
    claimed = execution.claim_attempt(
        attempts[0].attempt_id,
        worker_id="w38-public-worker",
        lease_seconds=30,
        request_id="w38-claim-failure",
    )
    failed = execution.publish_attempt_state(
        claimed.attempt_id,
        fencing_token=claimed.fencing_token,
        state="FAILED",
        worker_id="w38-public-worker",
        reason="SAFE_FAILURE",
        request_id="w38-publish-failure",
    )
    recovered = execution.retry(
        execution_actor,
        "workspace",
        run_id=failed.run_id,
        expected_revision=3,
        mode="failed_nodes",
        reason="retry after bounded remediation",
        request_id="w38-create-recovery",
        idempotency_key="w38-retry-key",
        payload_hash="a" * 64,
    )
    _, recovery_attempts = execution.get_run(execution_actor, "workspace", recovered.run_id)
    recovered_claim = execution.claim_attempt(
        recovery_attempts[0].attempt_id,
        worker_id="w38-public-worker",
        lease_seconds=30,
        request_id="w38-claim-recovery",
    )
    recovered = execution.publish_attempt_state(
        recovered_claim.attempt_id,
        fencing_token=recovered_claim.fencing_token,
        state="SUCCEEDED",
        worker_id="w38-public-worker",
        reason="RECOVERY_SUCCEEDED",
        request_id="w38-publish-recovery",
    )
    assert failed.state == "FAILED" and recovered.state == "SUCCEEDED"

    claimed_events = event_port.claim_terminal_events(limit=10)
    by_type = {item.event_type: item for item in claimed_events}
    assert set(by_type) == {
        "execution.run.failed",
        "execution.run.stuck",
        "execution.run.recovered",
    }
    failure_event = by_type["execution.run.failed"]
    stuck_event = by_type["execution.run.stuck"]
    recovery_event = by_type["execution.run.recovered"]
    assert stuck_event.attempt_id == stuck_claim.attempt_id
    assert failure_event.group_key == recovery_event.group_key
    assert failure_event.retry_of_run_id is None
    assert recovery_event.retry_of_run_id == failed.run_id

    for item in claimed_events:
        recipients.recipients[item.event_id] = (notification_runtime.reader_id,)
        access.grant(
            notification_runtime.reader_id,
            item.workspace_id,
            item.resource_type,
            str(item.resource_id),
        )

    assert projector.project(recovery_event).duplicate is False
    assert projector.project(failure_event).duplicate is False
    assert projector.project(stuck_event).duplicate is False
    event_port.release_terminal_event(recovery_event.event_id, "PROJECTION_ACK_RETRY")
    event_port.mark_terminal_event_published(failure_event.event_id)
    event_port.mark_terminal_event_published(stuck_event.event_id)
    time.sleep(1.05)
    repeated = event_port.claim_terminal_events(limit=10)
    assert len(repeated) == 1 and repeated[0].event_id == recovery_event.event_id
    assert projector.project(repeated[0]).duplicate is True
    event_port.mark_terminal_event_published(repeated[0].event_id)

    english = client.get("/items", headers={**headers("reader"), "Accept-Language": "en"})
    russian = client.get("/items", headers={**headers("reader"), "Accept-Language": "ru"})
    assert english.status_code == 200
    assert english.json() == russian.json()
    assert english.json()["visible_count"] == 2
    item = next(
        candidate
        for candidate in english.json()["items"]
        if candidate["message_code"] == "RUN_RECOVERED"
    )
    assert item["message_code"] == "RUN_RECOVERED"
    assert item["message_parameters"] == {
        "reason_code": "RETRY_SUCCEEDED",
        "status_code": "RECOVERED",
    }
    assert item["source_event_count"] == 2
    assert item["resolved"] is True
    assert item["deep_link"]["route_id"] == "UI-OPS-002"
    assert item["source_type"] == "execution.run.recovered"
    with notification_runtime.connect() as connection, connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT recipient_policy_version, preference_reference
            FROM notification_inbox_items WHERE id = %s
            """,
            (item["notification_id"],),
        )
        assert cursor.fetchone() == ("identity-policy-v1", "preferences:run:v1")


def test_authenticated_visibility_count_deep_link_and_revocation_fail_closed(
    notification_runtime: NotificationRuntime,
) -> None:
    client, service, _, access, recipients, _ = boundary(notification_runtime)
    now = datetime.now(UTC)
    visible = notification_event(
        workspace_id=notification_runtime.workspace_id,
        resource_id=str(uuid4()),
        occurred_at=now,
        message_code="RUN_FAILED",
    )
    hidden = notification_event(
        workspace_id=notification_runtime.workspace_id,
        resource_id=str(uuid4()),
        occurred_at=now - timedelta(seconds=1),
        message_code="RUN_STUCK",
    )
    cross_workspace = notification_event(
        workspace_id=notification_runtime.second_workspace_id,
        resource_id=str(uuid4()),
        occurred_at=now - timedelta(seconds=2),
        message_code="RUN_FAILED",
    )
    for item in (visible, hidden, cross_workspace):
        recipients.recipients[item.event_id] = (notification_runtime.reader_id,)
        service.project_event(item)
    access.grant(
        notification_runtime.reader_id,
        visible.workspace_id,
        visible.resource_type,
        visible.resource_id,
    )
    access.grant(
        notification_runtime.reader_id,
        cross_workspace.workspace_id,
        cross_workspace.resource_type,
        cross_workspace.resource_id,
    )

    listing = client.get("/items", headers=headers("reader"))
    count = client.get("/unread-count", headers=headers("reader"))
    assert listing.status_code == 200
    assert listing.json()["visible_count"] == 2
    assert count.json() == {"unread_count": 2, "capped": False}
    assert hidden.resource_id not in str(listing.json())
    notification_id = listing.json()["items"][0]["notification_id"]

    access.link_grants.clear()
    stale_link = client.get(f"/items/{notification_id}", headers=headers("reader"))
    assert stale_link.status_code == 200
    assert stale_link.json()["deep_link"] == {
        "status": "unavailable",
        "route_id": None,
        "parameters": None,
    }

    access.resource_grants.clear()
    revoked_list = client.get("/items", headers=headers("reader"))
    revoked_count = client.get("/unread-count", headers=headers("reader"))
    revoked_detail = client.get(f"/items/{notification_id}", headers=headers("reader"))
    assert revoked_list.json() == {"items": [], "visible_count": 0}
    assert revoked_count.json() == {"unread_count": 0, "capped": False}
    assert revoked_detail.status_code == 404
    assert revoked_detail.json() == {"code": "NOT_FOUND"}

    after_revoke = notification_event(
        workspace_id=notification_runtime.workspace_id,
        resource_id=str(uuid4()),
        occurred_at=now + timedelta(seconds=1),
        message_code="RUN_FAILED",
    )
    assert service.project_event(after_revoke).projected_recipients == 0
    assert client.get("/items", headers=headers("reader")).json()["visible_count"] == 0

    assert client.get("/items", headers=headers("no-permission")).status_code == 403
    assert client.get("/items", headers={"X-Request-ID": "missing-auth"}).status_code == 400
    assert client.get("/items", headers=headers("unknown")).status_code == 401


def test_acknowledge_read_dismiss_are_durable_idempotent_and_redacted(
    notification_runtime: NotificationRuntime,
) -> None:
    client, service, _, access, recipients, audit = boundary(notification_runtime)
    event = notification_event(
        workspace_id=notification_runtime.workspace_id,
        resource_id=str(uuid4()),
        occurred_at=datetime.now(UTC),
        message_code="RUN_FAILED",
    )
    recipients.recipients[event.event_id] = (notification_runtime.acknowledger_id,)
    outcome = service.project_event(event)
    notification_id = outcome.notification_ids[0]
    access.grant(
        notification_runtime.acknowledger_id,
        event.workspace_id,
        event.resource_type,
        event.resource_id,
    )

    mutation_headers = headers("acknowledger", request_id="ack-request")
    mutation_headers["Idempotency-Key"] = "ack-key"
    acknowledged = client.post(
        f"/items/{notification_id}/acknowledge",
        headers=mutation_headers,
        json={"expected_revision": 1, "reason_code": "OPERATOR_CONFIRMED"},
    )
    assert acknowledged.status_code == 200, acknowledged.text
    assert acknowledged.json()["acknowledged"] is True
    assert acknowledged.json()["read"] is False
    assert acknowledged.json()["revision"] == 2

    read_headers = headers("acknowledger", request_id="read-request")
    read_headers["Idempotency-Key"] = "read-key"
    read = client.post(
        f"/items/{notification_id}/read",
        headers=read_headers,
        json={"expected_revision": 2},
    )
    assert read.json()["read"] is True and read.json()["revision"] == 3

    replay = client.post(
        f"/items/{notification_id}/acknowledge",
        headers=mutation_headers,
        json={"expected_revision": 1, "reason_code": "OPERATOR_CONFIRMED"},
    )
    assert replay.status_code == 200
    assert replay.json()["revision"] == 3
    conflict = client.post(
        f"/items/{notification_id}/acknowledge",
        headers=mutation_headers,
        json={"expected_revision": 1, "reason_code": "DIFFERENT_REASON"},
    )
    assert conflict.status_code == 409
    assert conflict.json() == {"code": "IDEMPOTENCY_CONFLICT"}

    dismiss_headers = headers("acknowledger", request_id="dismiss-request")
    dismiss_headers["Idempotency-Key"] = "dismiss-key"
    dismissed = client.post(
        f"/items/{notification_id}/dismiss",
        headers=dismiss_headers,
        json={"expected_revision": 3, "reason_code": "NO_LONGER_ACTIONABLE"},
    )
    assert dismissed.json()["dismissed"] is True
    assert dismissed.json()["revision"] == 4
    assert [item.action for item in audit.intents] == [
        "notification.acknowledged",
        "notification.dismissed",
    ]

    with notification_runtime.connect() as connection, connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT action, actor_id, notification_id, reason_code, request_id
            FROM notification_audit_outbox WHERE notification_id = %s ORDER BY occurred_at
            """,
            (notification_id,),
        )
        rows = cursor.fetchall()
    assert rows == [
        (
            "notification.acknowledged",
            notification_runtime.acknowledger_id,
            notification_id,
            "OPERATOR_CONFIRMED",
            "ack-request",
        ),
        (
            "notification.dismissed",
            notification_runtime.acknowledger_id,
            notification_id,
            "NO_LONGER_ACTIONABLE",
            "dismiss-request",
        ),
    ]


def test_z_real_postgresql_migration_repeat_downgrade_and_reupgrade(
    notification_boundaries: NotificationBoundaries,
) -> None:
    def migrate_to(revision: str) -> None:
        migrate(
            host=notification_boundaries.database_host,
            port=notification_boundaries.database_port,
            database="custometry",
            user="custometry",
            password_file=notification_boundaries.database_password_file,
            revision=revision,
        )

    migrate_to("head")
    migrate_to("-0008_execution_control")
    with notification_boundaries.connect() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT to_regclass('public.notification_inbox_items')")
        assert cursor.fetchone() == (None,)
        cursor.execute("SELECT to_regclass('public.execution_runs')")
        assert cursor.fetchone() == ("execution_runs",)
    migrate_to("head")
    with notification_boundaries.connect() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT version_num FROM alembic_version")
        assert cursor.fetchone() == ("0009_notifications",)
