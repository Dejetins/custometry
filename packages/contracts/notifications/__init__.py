"""Public, locale-neutral contracts for the in-app Notifications context."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Protocol, TypeAlias
from uuid import UUID


NOTIFICATIONS_API_VERSION = "1.0.0"
NotificationSeverity = Literal["info", "warning", "critical"]
NotificationCategory = Literal[
    "run", "data_quality", "data_freshness", "forecast", "schedule", "system", "security", "admin"
]
SafeScalar: TypeAlias = str | int | bool


class NotificationFailure(RuntimeError):
    """Stable redacted failure at the Notifications boundary."""

    def __init__(self, code: str, *, current_revision: int | None = None) -> None:
        super().__init__(code)
        self.code = code
        self.current_revision = current_revision


@dataclass(frozen=True, slots=True)
class NotificationActor:
    principal_id: UUID
    permissions: frozenset[str]
    policy_version: str
    active_workspace_ids: tuple[UUID, ...]


@dataclass(frozen=True, slots=True)
class DeepLinkDescriptor:
    route_id: str
    parameters: tuple[tuple[str, str], ...]


@dataclass(frozen=True, slots=True)
class NotificationEvent:
    """Versioned owner event accepted by the Notifications projection port."""

    event_id: UUID
    source_owner: str
    source_type: str
    source_version: int
    workspace_id: UUID
    resource_type: str
    resource_id: str
    severity: NotificationSeverity
    category: NotificationCategory
    occurred_at: datetime
    message_code: str
    message_parameters: tuple[tuple[str, SafeScalar], ...]
    group_key: str
    deep_link: DeepLinkDescriptor | None
    trace_id: str | None
    resolved: bool = False


@dataclass(frozen=True, slots=True)
class RecipientCandidate:
    principal_id: UUID
    policy_version: str
    preference_reference: str | None = None


@dataclass(frozen=True, slots=True)
class AuditIntent:
    action: Literal["notification.acknowledged", "notification.dismissed"]
    workspace_id: UUID
    actor_id: UUID
    notification_id: UUID
    reason_code: str
    request_id: str
    occurred_at: datetime


class NotificationRecipientResolverPort(Protocol):
    """Identity-owned policy projection; implementations must not expose private tables."""

    def eligible_recipients(self, event: NotificationEvent) -> tuple[RecipientCandidate, ...]: ...


class NotificationAccessPort(Protocol):
    """Current Identity policy decision used before list/action disclosure."""

    def require(self, actor: NotificationActor, action: str) -> None: ...

    def can_access(
        self,
        actor: NotificationActor,
        *,
        workspace_id: UUID,
        resource_type: str,
        resource_id: str,
    ) -> bool: ...

    def can_disclose_deep_link(
        self,
        actor: NotificationActor,
        *,
        workspace_id: UUID,
        resource_type: str,
        resource_id: str,
        deep_link: DeepLinkDescriptor,
    ) -> bool: ...


class NotificationAuditPort(Protocol):
    """Audit-owned append port receiving only the redacted intent contract."""

    def append(self, intent: AuditIntent) -> None: ...


__all__ = [
    "AuditIntent",
    "DeepLinkDescriptor",
    "NOTIFICATIONS_API_VERSION",
    "NotificationAccessPort",
    "NotificationActor",
    "NotificationAuditPort",
    "NotificationCategory",
    "NotificationEvent",
    "NotificationFailure",
    "NotificationRecipientResolverPort",
    "NotificationSeverity",
    "RecipientCandidate",
    "SafeScalar",
]
