from datetime import UTC, datetime
from uuid import UUID, uuid4

import pytest

from packages.contracts.notifications import (
    AuditIntent,
    DeepLinkDescriptor,
    NotificationActor,
    NotificationEvent,
    NotificationFailure,
    RecipientCandidate,
)
from packages.notifications.application.service import NotificationInboxService
from packages.notifications.domain.model import (
    NotificationItem,
    NotificationQuery,
    ProjectionOutcome,
)


class RecordingStore:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def project_event(
        self, event: NotificationEvent, recipients: tuple[RecipientCandidate, ...]
    ) -> ProjectionOutcome:
        del event, recipients
        self.calls.append("project")
        raise AssertionError("not needed")

    def list_candidates(
        self, principal_id: UUID, query: NotificationQuery
    ) -> tuple[NotificationItem, ...]:
        del principal_id, query
        self.calls.append("list")
        return ()

    def get_for_recipient(self, principal_id: UUID, notification_id: UUID) -> NotificationItem:
        del principal_id, notification_id
        self.calls.append("get")
        raise AssertionError("not needed")

    def mutate(
        self,
        actor: NotificationActor,
        *,
        notification_id: UUID,
        action: str,
        expected_revision: int,
        reason_code: str | None,
        request_id: str,
        idempotency_key: str,
        payload_hash: str,
    ) -> tuple[NotificationItem, AuditIntent | None]:
        del (
            actor,
            notification_id,
            action,
            expected_revision,
            reason_code,
            request_id,
            idempotency_key,
            payload_hash,
        )
        self.calls.append("mutate")
        raise AssertionError("not needed")


class Access:
    def require(self, actor: NotificationActor, action: str) -> None:
        if action not in actor.permissions:
            raise NotificationFailure("FORBIDDEN")

    def can_access(
        self,
        actor: NotificationActor,
        *,
        workspace_id: UUID,
        resource_type: str,
        resource_id: str,
    ) -> bool:
        del actor, workspace_id, resource_type, resource_id
        return True

    def can_disclose_deep_link(
        self,
        actor: NotificationActor,
        *,
        workspace_id: UUID,
        resource_type: str,
        resource_id: str,
        deep_link: DeepLinkDescriptor,
    ) -> bool:
        del actor, workspace_id, resource_type, resource_id, deep_link
        return True


class Recipients:
    def eligible_recipients(self, event: NotificationEvent) -> tuple[RecipientCandidate, ...]:
        del event
        return (RecipientCandidate(UUID(int=3), "policy-v1"),)


def actor(*permissions: str) -> NotificationActor:
    return NotificationActor(uuid4(), frozenset(permissions), "policy-v1", (uuid4(),))


def event(*, code: str = "RUN_FAILED", link: DeepLinkDescriptor | None = None) -> NotificationEvent:
    return NotificationEvent(
        event_id=uuid4(),
        source_owner="execution_control",
        source_type="run.failed",
        source_version=1,
        workspace_id=uuid4(),
        resource_type="run",
        resource_id=str(uuid4()),
        severity="critical",
        category="run",
        occurred_at=datetime.now(UTC),
        message_code=code,
        message_parameters=(("failure_code", "SAFE_FAILURE"),),
        group_key=f"run:{uuid4()}",
        deep_link=link,
        trace_id="trace-safe",
    )


def test_list_permission_is_denied_before_store_fetch_or_count() -> None:
    store = RecordingStore()
    service = NotificationInboxService(store, Access())

    with pytest.raises(NotificationFailure, match="FORBIDDEN"):
        service.list_items(actor(), NotificationQuery())
    with pytest.raises(NotificationFailure, match="FORBIDDEN"):
        service.unread_count(actor())

    assert store.calls == []


@pytest.mark.parametrize(
    "unsafe",
    [
        DeepLinkDescriptor("https://evil.example", ()),
        DeepLinkDescriptor("UI-OPS-002", (("run_id", "safe"), ("returnTo", "evil"))),
        DeepLinkDescriptor("UI-OPS-002", (("run_id", "../secret"),)),
    ],
)
def test_projection_rejects_unsafe_deep_links_before_recipient_resolution(
    unsafe: DeepLinkDescriptor,
) -> None:
    store = RecordingStore()
    service = NotificationInboxService(store, Access(), recipients=Recipients())

    with pytest.raises(NotificationFailure, match="UNSAFE_DEEP_LINK"):
        service.project_event(event(link=unsafe))

    assert store.calls == []


def test_projection_rejects_rendered_or_non_code_content() -> None:
    store = RecordingStore()
    service = NotificationInboxService(store, Access(), recipients=Recipients())

    with pytest.raises(NotificationFailure, match="INVALID_EVENT"):
        service.project_event(event(code="Run failed: secret customer name"))

    assert store.calls == []
