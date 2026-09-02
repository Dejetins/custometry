"""Privacy-safe contributor event validation and projection orchestration."""

from __future__ import annotations

import re
from datetime import UTC, datetime
from uuid import UUID

from packages.contracts.people import (
    ContributorDomainEvent,
    ContributorProjectionStorePort,
    ProjectionRebuildResult,
)


_EVENT_TYPES = frozenset(
    {
        "profile.published",
        "resource.created",
        "resource.published",
        "resource.materially_updated",
        "resource.maintained",
        "collaboration.coauthored",
        "collaboration.reviewed",
        "collaboration.resolved",
    }
)
_RESOURCE_TYPES = frozenset({"dashboard", "report", "research"})
_SAFE_LABEL = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")


class ContributorProjectionFailure(ValueError):
    """Reject unsafe or structurally invalid event intake before persistence."""


def _safe_text(value: str, *, maximum: int, label: str) -> str:
    normalized = " ".join(value.split())
    if not normalized or len(normalized) > maximum:
        raise ContributorProjectionFailure(f"invalid {label}")
    if "@" in normalized or "\x00" in normalized:
        raise ContributorProjectionFailure(f"unsafe {label}")
    return normalized


def _safe_labels(values: tuple[str, ...], *, label: str) -> tuple[str, ...]:
    normalized = tuple(sorted(set(value.strip().casefold() for value in values)))
    if len(normalized) > 16 or any(not _SAFE_LABEL.fullmatch(value) for value in normalized):
        raise ContributorProjectionFailure(f"invalid {label}")
    return normalized


def validate_redacted_event(event: ContributorDomainEvent) -> ContributorDomainEvent:
    """Return a normalized event whose shape cannot contain arbitrary/raw payloads."""

    if event.event_type not in _EVENT_TYPES:
        raise ContributorProjectionFailure("event type is not allowlisted")
    if event.occurred_at.tzinfo is None or event.occurred_at.utcoffset() is None:
        raise ContributorProjectionFailure("occurred_at must be timezone-aware")

    occurred_at = event.occurred_at.astimezone(UTC)
    if event.event_type == "profile.published":
        if any(
            value is not None
            for value in (event.resource_type, event.resource_id, event.safe_resource_title)
        ):
            raise ContributorProjectionFailure("profile event cannot contain a resource")
        if event.display_name is None:
            raise ContributorProjectionFailure("profile event requires display_name")
        title = (
            None if event.title is None else _safe_text(event.title, maximum=120, label="title")
        )
        return ContributorDomainEvent(
            event_id=event.event_id,
            workspace_id=event.workspace_id,
            principal_id=event.principal_id,
            event_type=event.event_type,
            occurred_at=occurred_at,
            display_name=_safe_text(event.display_name, maximum=160, label="display_name"),
            title=title,
            title_visible=bool(title and event.title_visible),
            contribution_labels=_safe_labels(
                event.contribution_labels, label="contribution_labels"
            ),
            expertise_domains=_safe_labels(event.expertise_domains, label="expertise_domains"),
        )

    if (
        event.resource_type not in _RESOURCE_TYPES
        or event.resource_id is None
        or event.safe_resource_title is None
    ):
        raise ContributorProjectionFailure("activity event requires an allowlisted resource")
    if any(
        value is not None for value in (event.display_name, event.title)
    ) or event.contribution_labels or event.expertise_domains or event.title_visible:
        raise ContributorProjectionFailure("activity event contains profile fields")
    return ContributorDomainEvent(
        event_id=event.event_id,
        workspace_id=event.workspace_id,
        principal_id=event.principal_id,
        event_type=event.event_type,
        occurred_at=occurred_at,
        resource_type=event.resource_type,
        resource_id=event.resource_id,
        safe_resource_title=_safe_text(
            event.safe_resource_title, maximum=200, label="safe_resource_title"
        ),
    )


class ContributorActivityProjector:
    """Owner application service for idempotent redacted projection updates."""

    def __init__(self, store: ContributorProjectionStorePort) -> None:
        self._store = store

    def project(
        self,
        events: tuple[ContributorDomainEvent, ...],
        *,
        rebuilt_at: datetime | None = None,
    ) -> ProjectionRebuildResult:
        if not events:
            raise ContributorProjectionFailure("at least one event is required")
        normalized = tuple(validate_redacted_event(event) for event in events)
        workspace_ids = {event.workspace_id for event in normalized}
        if len(workspace_ids) != 1:
            raise ContributorProjectionFailure("one projection batch cannot cross workspaces")
        self._store.append_redacted_events(normalized)
        workspace_id = next(iter(workspace_ids))
        return self._store.rebuild(
            workspace_id,
            rebuilt_at=(rebuilt_at or datetime.now(UTC)).astimezone(UTC),
        )

    def rebuild(
        self, workspace_id: UUID, *, rebuilt_at: datetime | None = None
    ) -> ProjectionRebuildResult:
        return self._store.rebuild(
            workspace_id,
            rebuilt_at=(rebuilt_at or datetime.now(UTC)).astimezone(UTC),
        )


__all__ = [
    "ContributorActivityProjector",
    "ContributorProjectionFailure",
    "validate_redacted_event",
]
