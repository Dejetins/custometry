"""Permission-first in-app inbox projection, queries, and state transitions."""

from __future__ import annotations

import re
from typing import Protocol
from uuid import UUID

from packages.contracts.execution import ExecutionTerminalEvent
from packages.contracts.notifications import (
    AuditIntent,
    DeepLinkDescriptor,
    NotificationAccessPort,
    NotificationActor,
    NotificationAuditPort,
    NotificationEvent,
    NotificationFailure,
    NotificationRecipientResolverPort,
    RecipientCandidate,
)
from packages.notifications.domain.model import (
    NotificationItem,
    NotificationQuery,
    ProjectionOutcome,
    VisibleNotification,
)


CODE = re.compile(r"^[A-Z][A-Z0-9_]{2,79}$")
IDENTITY = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$")
SAFE_ROUTES: dict[str, frozenset[str]] = {
    "UI-OPS-001": frozenset(),
    "UI-OPS-002": frozenset({"run_id"}),
    "UI-OPS-003": frozenset({"run_id", "node_id", "attempt_id"}),
}


class NotificationStorePort(Protocol):
    def project_event(
        self, event: NotificationEvent, recipients: tuple[RecipientCandidate, ...]
    ) -> ProjectionOutcome: ...

    def list_candidates(
        self, principal_id: UUID, query: NotificationQuery
    ) -> tuple[NotificationItem, ...]: ...

    def get_for_recipient(self, principal_id: UUID, notification_id: UUID) -> NotificationItem: ...

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
    ) -> tuple[NotificationItem, AuditIntent | None]: ...


class NullNotificationAudit:
    """Default sink; the durable store outbox remains the audit source of truth."""

    def append(self, intent: AuditIntent) -> None:
        del intent


class ExecutionTerminalNotificationProjector:
    """Translate the public Execution event without reading Execution-owned state."""

    _EXPECTED = {
        "execution.run.failed": ("FAILED", "RUN_FAILED"),
        "execution.run.stuck": ("STUCK", "RUN_STUCK"),
        "execution.run.recovered": ("RECOVERED", "RUN_RECOVERED"),
    }

    def __init__(self, inbox: "NotificationInboxService") -> None:
        self._inbox = inbox

    @classmethod
    def notification_event(cls, event: ExecutionTerminalEvent) -> NotificationEvent:
        expected = cls._EXPECTED.get(event.event_type)
        if (
            event.event_version != "1.0.0"
            or event.source_owner != "execution"
            or event.category != "execution"
            or event.resource_type != "run"
            or event.resource_id != event.run_id
            or expected != (event.status_code, event.message_code)
            or dict(event.route_parameters) != {"run_id": str(event.run_id)}
        ):
            raise NotificationFailure("INVALID_EVENT")
        return NotificationEvent(
            event_id=event.event_id,
            source_owner=event.source_owner,
            source_type=event.event_type,
            source_version=1,
            workspace_id=event.workspace_id,
            resource_type=event.resource_type,
            resource_id=str(event.resource_id),
            severity=event.severity,
            category="run",
            occurred_at=event.occurred_at,
            message_code=event.message_code,
            message_parameters=event.message_parameters,
            group_key=event.group_key,
            deep_link=DeepLinkDescriptor(event.route_id, event.route_parameters),
            trace_id=event.trace_id,
            resolved=event.status_code == "RECOVERED",
        )

    def project(self, event: ExecutionTerminalEvent) -> ProjectionOutcome:
        return self._inbox.project_event(self.notification_event(event))


class NotificationInboxService:
    def __init__(
        self,
        store: NotificationStorePort,
        access: NotificationAccessPort,
        *,
        recipients: NotificationRecipientResolverPort | None = None,
        audit: NotificationAuditPort | None = None,
    ) -> None:
        self._store = store
        self._access = access
        self._recipients = recipients
        self._audit = audit or NullNotificationAudit()

    @staticmethod
    def _bounded_identity(value: str, code: str, maximum: int = 128) -> str:
        normalized = value.strip()
        if not normalized or len(normalized) > maximum:
            raise NotificationFailure(code)
        return normalized

    @classmethod
    def _validate_deep_link(cls, value: DeepLinkDescriptor | None) -> None:
        if value is None:
            return
        expected = SAFE_ROUTES.get(value.route_id)
        parameters = dict(value.parameters)
        if (
            expected is None
            or frozenset(parameters) != expected
            or len(parameters) != len(value.parameters)
        ):
            raise NotificationFailure("UNSAFE_DEEP_LINK")
        if any(
            not IDENTITY.fullmatch(key) or not IDENTITY.fullmatch(item)
            for key, item in parameters.items()
        ):
            raise NotificationFailure("UNSAFE_DEEP_LINK")

    @classmethod
    def _validate_event(cls, event: NotificationEvent) -> None:
        if event.source_version < 1 or event.occurred_at.tzinfo is None:
            raise NotificationFailure("INVALID_EVENT")
        identities = (
            event.source_owner,
            event.source_type,
            event.resource_type,
            event.resource_id,
            event.group_key,
        )
        if any(not IDENTITY.fullmatch(item) for item in identities):
            raise NotificationFailure("INVALID_EVENT")
        if not CODE.fullmatch(event.message_code):
            raise NotificationFailure("INVALID_EVENT")
        parameters = dict(event.message_parameters)
        if len(parameters) != len(event.message_parameters) or len(parameters) > 16:
            raise NotificationFailure("INVALID_EVENT")
        for key, value in parameters.items():
            if not IDENTITY.fullmatch(key):
                raise NotificationFailure("INVALID_EVENT")
            if isinstance(value, str) and (not value or len(value) > 160):
                raise NotificationFailure("INVALID_EVENT")
        if event.trace_id is not None and not IDENTITY.fullmatch(event.trace_id):
            raise NotificationFailure("INVALID_EVENT")
        cls._validate_deep_link(event.deep_link)

    def project_event(self, event: NotificationEvent) -> ProjectionOutcome:
        self._validate_event(event)
        if self._recipients is None:
            raise NotificationFailure("RECIPIENT_RESOLUTION_UNAVAILABLE")
        candidates = self._recipients.eligible_recipients(event)
        unique = tuple({item.principal_id: item for item in candidates}.values())
        return self._store.project_event(event, unique)

    def _visible(self, actor: NotificationActor, item: NotificationItem) -> VisibleNotification:
        if item.recipient_id != actor.principal_id or not self._access.can_access(
            actor,
            workspace_id=item.workspace_id,
            resource_type=item.resource_type,
            resource_id=item.resource_id,
        ):
            raise NotificationFailure("NOT_FOUND")
        status = "unavailable"
        if item.deep_link is not None and self._access.can_disclose_deep_link(
            actor,
            workspace_id=item.workspace_id,
            resource_type=item.resource_type,
            resource_id=item.resource_id,
            deep_link=item.deep_link,
        ):
            status = "available"
        return VisibleNotification(item=item, deep_link_status=status)

    def list_items(
        self, actor: NotificationActor, query: NotificationQuery
    ) -> tuple[tuple[VisibleNotification, ...], int]:
        self._access.require(actor, "notification.read")
        if query.offset < 0 or not 1 <= query.limit <= 100:
            raise NotificationFailure("INVALID_INPUT")
        candidates = self._store.list_candidates(actor.principal_id, query)
        visible: list[VisibleNotification] = []
        for item in candidates:
            try:
                visible.append(self._visible(actor, item))
            except NotificationFailure as exc:
                if exc.code != "NOT_FOUND":
                    raise
        total = len(visible)
        return tuple(visible[query.offset : query.offset + query.limit]), total

    def unread_count(self, actor: NotificationActor) -> int:
        _, count = self.list_items(
            actor,
            NotificationQuery(read=False, dismissed=False, resolved=False, limit=100),
        )
        return min(count, 999)

    def get_item(self, actor: NotificationActor, notification_id: UUID) -> VisibleNotification:
        self._access.require(actor, "notification.read")
        return self._visible(
            actor, self._store.get_for_recipient(actor.principal_id, notification_id)
        )

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
    ) -> VisibleNotification:
        permission = "notification.acknowledge" if action == "acknowledge" else "notification.read"
        self._access.require(actor, permission)
        current = self._visible(
            actor, self._store.get_for_recipient(actor.principal_id, notification_id)
        ).item
        if action == "acknowledge" and current.severity != "critical":
            raise NotificationFailure("ACKNOWLEDGEMENT_NOT_ALLOWED")
        normalized_reason = None
        if action in {"acknowledge", "dismiss"}:
            normalized_reason = self._bounded_identity(
                reason_code or "", "AUDIT_REASON_REQUIRED", maximum=80
            )
            if not CODE.fullmatch(normalized_reason):
                raise NotificationFailure("AUDIT_REASON_REQUIRED")
        item, intent = self._store.mutate(
            actor,
            notification_id=notification_id,
            action=action,
            expected_revision=expected_revision,
            reason_code=normalized_reason,
            request_id=self._bounded_identity(request_id, "REQUEST_ID_REQUIRED"),
            idempotency_key=self._bounded_identity(idempotency_key, "IDEMPOTENCY_KEY_REQUIRED"),
            payload_hash=self._bounded_identity(payload_hash, "INVALID_PAYLOAD_HASH", maximum=64),
        )
        if intent is not None:
            self._audit.append(intent)
        return self._visible(actor, item)


__all__ = [
    "ExecutionTerminalNotificationProjector",
    "NotificationInboxService",
    "NotificationStorePort",
    "NullNotificationAudit",
]
