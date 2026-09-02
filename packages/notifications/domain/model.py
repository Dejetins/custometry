"""Domain records and safe query values for the in-app inbox."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from packages.contracts.notifications import (
    DeepLinkDescriptor,
    NotificationCategory,
    NotificationSeverity,
    SafeScalar,
)


@dataclass(frozen=True, slots=True)
class NotificationItem:
    notification_id: UUID
    workspace_id: UUID
    recipient_id: UUID
    recipient_policy_version: str
    preference_reference: str | None
    latest_event_id: UUID
    source_owner: str
    source_type: str
    resource_type: str
    resource_id: str
    severity: NotificationSeverity
    category: NotificationCategory
    occurred_at: datetime
    message_code: str
    message_parameters: tuple[tuple[str, SafeScalar], ...]
    group_key: str
    source_event_count: int
    deep_link: DeepLinkDescriptor | None
    trace_id: str | None
    resolved: bool
    read_at: datetime | None
    dismissed_at: datetime | None
    acknowledged_at: datetime | None
    revision: int
    freshness: str


@dataclass(frozen=True, slots=True)
class VisibleNotification:
    item: NotificationItem
    deep_link_status: str


@dataclass(frozen=True, slots=True)
class NotificationQuery:
    severities: tuple[str, ...] = ()
    categories: tuple[str, ...] = ()
    read: bool | None = None
    dismissed: bool | None = None
    acknowledged: bool | None = None
    resolved: bool | None = None
    workspace_id: UUID | None = None
    occurred_from: datetime | None = None
    occurred_to: datetime | None = None
    offset: int = 0
    limit: int = 50


@dataclass(frozen=True, slots=True)
class ProjectionOutcome:
    duplicate: bool
    projected_recipients: int
    notification_ids: tuple[UUID, ...]


__all__ = [
    "NotificationItem",
    "NotificationQuery",
    "ProjectionOutcome",
    "VisibleNotification",
]
