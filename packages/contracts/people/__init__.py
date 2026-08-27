"""Public contracts for privacy-safe contributor projections and People reads."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal, Protocol
from uuid import UUID


PEOPLE_API_VERSION = "1.0.0"

ActivityEventType = Literal[
    "profile.published",
    "resource.created",
    "resource.published",
    "resource.materially_updated",
    "resource.maintained",
    "collaboration.coauthored",
    "collaboration.reviewed",
    "collaboration.resolved",
]
ResourceType = Literal["dashboard", "report", "research"]
PeopleViewVariant = Literal["public", "self", "leader", "grantee"]


class PeopleFailure(RuntimeError):
    """Stable failure envelope for the independently versioned People API."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True, slots=True)
class ViewerContext:
    principal_id: UUID
    workspace_id: UUID
    permissions: frozenset[str]


@dataclass(frozen=True, slots=True)
class ContributorDomainEvent:
    """Allowlisted and already-redacted event accepted by the projection owner."""

    event_id: UUID
    workspace_id: UUID
    principal_id: UUID
    event_type: ActivityEventType
    occurred_at: datetime
    resource_type: ResourceType | None = None
    resource_id: UUID | None = None
    safe_resource_title: str | None = None
    display_name: str | None = None
    title: str | None = None
    title_visible: bool = False
    contribution_labels: tuple[str, ...] = ()
    expertise_domains: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ProjectionRebuildResult:
    workspace_id: UUID
    event_count: int
    bucket_count: int
    projection_version: str
    rebuilt_at: datetime


@dataclass(frozen=True, slots=True)
class ContributorCandidate:
    principal_id: UUID
    display_name: str
    title: str | None
    contribution_labels: tuple[str, ...]
    expertise_domains: tuple[str, ...]
    org_unit_id: UUID
    org_unit_name: str
    projection_version: str
    updated_at: datetime


@dataclass(frozen=True, slots=True)
class ContributorActivityBucket:
    principal_id: UUID
    resource_type: ResourceType
    resource_id: UUID
    safe_resource_title: str
    activity_date: date
    created_count: int
    published_count: int
    materially_updated_count: int
    maintained_count: int
    coauthored_count: int
    reviewed_count: int
    resolved_count: int
    last_activity_at: datetime


class ContributorProjectionStorePort(Protocol):
    """Identity-owned redacted event and projection persistence boundary."""

    def append_redacted_events(self, events: tuple[ContributorDomainEvent, ...]) -> int: ...

    def rebuild(self, workspace_id: UUID, *, rebuilt_at: datetime) -> ProjectionRebuildResult: ...


class ContributorProjectionQueryPort(Protocol):
    """Public read projection consumed by Presentation without private-table access."""

    def list_candidates(self, workspace_id: UUID) -> tuple[ContributorCandidate, ...]: ...

    def activity_buckets(
        self, workspace_id: UUID, principal_id: UUID
    ) -> tuple[ContributorActivityBucket, ...]: ...


class ContributorAuthorizationPort(Protocol):
    """Identity-owned current-policy decisions used before protected projection reads."""

    def view_variant(
        self, viewer: ViewerContext, target_principal_id: UUID, *, at: datetime
    ) -> PeopleViewVariant: ...

    def resource_visible(
        self,
        viewer: ViewerContext,
        *,
        target_org_unit_id: UUID,
        resource_type: ResourceType,
        resource_id: UUID,
    ) -> bool: ...


__all__ = [
    "ActivityEventType",
    "ContributorActivityBucket",
    "ContributorAuthorizationPort",
    "ContributorCandidate",
    "ContributorDomainEvent",
    "ContributorProjectionQueryPort",
    "ContributorProjectionStorePort",
    "PEOPLE_API_VERSION",
    "PeopleFailure",
    "PeopleViewVariant",
    "ProjectionRebuildResult",
    "ResourceType",
    "ViewerContext",
]
