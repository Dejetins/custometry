"""Policy-filtered People & Creators composition over public Identity ports."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import TypedDict
from uuid import UUID

from packages.contracts.people import (
    ContributorActivityBucket,
    ContributorAuthorizationPort,
    ContributorCandidate,
    ContributorProjectionQueryPort,
    PeopleFailure,
    PeopleViewVariant,
    ViewerContext,
)


class _ResourceView(TypedDict):
    resource_type: str
    resource_id: UUID
    title: str
    last_activity_at: datetime


def _visible_buckets(
    candidate: ContributorCandidate,
    buckets: tuple[ContributorActivityBucket, ...],
    viewer: ViewerContext,
    authorization: ContributorAuthorizationPort,
) -> tuple[ContributorActivityBucket, ...]:
    return tuple(
        bucket
        for bucket in buckets
        if authorization.resource_visible(
            viewer,
            target_org_unit_id=candidate.org_unit_id,
            resource_type=bucket.resource_type,
            resource_id=bucket.resource_id,
        )
    )


def _window_summary(
    buckets: tuple[ContributorActivityBucket, ...], *, days: int, at: datetime
) -> dict[str, object]:
    starts_on = at.date() - timedelta(days=days - 1)
    selected = tuple(bucket for bucket in buckets if bucket.activity_date >= starts_on)
    return {
        "window_days": days,
        "created_count": sum(bucket.created_count for bucket in selected),
        "published_count": sum(bucket.published_count for bucket in selected),
        "materially_updated_count": sum(
            bucket.materially_updated_count for bucket in selected
        ),
        "maintained_count": sum(bucket.maintained_count for bucket in selected),
        "coauthored_count": sum(bucket.coauthored_count for bucket in selected),
        "reviewed_count": sum(bucket.reviewed_count for bucket in selected),
        "resolved_count": sum(bucket.resolved_count for bucket in selected),
        "last_activity_at": (
            max(bucket.last_activity_at for bucket in selected) if selected else None
        ),
    }


class PeopleService:
    """Compose results only after current scope and resource policy filtering."""

    def __init__(
        self,
        *,
        projection: ContributorProjectionQueryPort,
        authorization: ContributorAuthorizationPort,
    ) -> None:
        self._projection = projection
        self._authorization = authorization

    @staticmethod
    def _require_directory(viewer: ViewerContext) -> None:
        if "organization.read" not in viewer.permissions:
            raise PeopleFailure("FORBIDDEN")

    def _compose(
        self,
        viewer: ViewerContext,
        candidate: ContributorCandidate,
        *,
        at: datetime,
    ) -> dict[str, object] | None:
        variant = self._authorization.view_variant(
            viewer, candidate.principal_id, at=at
        )
        buckets = _visible_buckets(
            candidate,
            self._projection.activity_buckets(
                viewer.workspace_id, candidate.principal_id
            ),
            viewer,
            self._authorization,
        )
        extended = variant in {"self", "leader", "grantee"}
        if not extended and not buckets:
            return None
        resources: dict[tuple[str, UUID], _ResourceView] = {}
        for bucket in buckets:
            key = (bucket.resource_type, bucket.resource_id)
            current = resources.get(key)
            if current is None or bucket.last_activity_at > current["last_activity_at"]:
                resources[key] = {
                    "resource_type": bucket.resource_type,
                    "resource_id": bucket.resource_id,
                    "title": bucket.safe_resource_title,
                    "last_activity_at": bucket.last_activity_at,
                }
        ordered_resources = sorted(
            resources.values(),
            key=lambda item: (
                -item["last_activity_at"].timestamp(),
                str(item["resource_type"]),
                str(item["resource_id"]),
            ),
        )
        activity = (
            {
                "windows": [
                    _window_summary(buckets, days=30, at=at),
                    _window_summary(buckets, days=90, at=at),
                ]
            }
            if extended
            else None
        )
        return {
            "principal_id": candidate.principal_id,
            "display_name": candidate.display_name,
            "title": candidate.title,
            "primary_org_unit": {
                "org_unit_id": candidate.org_unit_id,
                "display_name": candidate.org_unit_name,
            },
            "contribution_labels": list(candidate.contribution_labels),
            "expertise_domains": list(candidate.expertise_domains),
            "view_variant": variant,
            "visible_resources": ordered_resources,
            "visible_resource_count": len(ordered_resources),
            "activity": activity,
            "projection_version": candidate.projection_version,
            "projection_updated_at": candidate.updated_at,
        }

    def list_people(
        self,
        viewer: ViewerContext,
        *,
        search: str | None,
        offset: int,
        limit: int,
        at: datetime | None = None,
    ) -> tuple[tuple[dict[str, object], ...], int]:
        self._require_directory(viewer)
        if offset < 0 or limit < 1 or limit > 100:
            raise PeopleFailure("INVALID_INPUT")
        normalized_search = " ".join((search or "").split()).casefold()
        if len(normalized_search) > 120:
            raise PeopleFailure("INVALID_INPUT")
        observed_at = (at or datetime.now(UTC)).astimezone(UTC)
        visible: list[dict[str, object]] = []
        for candidate in self._projection.list_candidates(viewer.workspace_id):
            composed = self._compose(viewer, candidate, at=observed_at)
            if composed is None:
                continue
            if normalized_search and normalized_search not in candidate.display_name.casefold():
                continue
            visible.append(composed)
        return tuple(visible[offset : offset + limit]), len(visible)

    def get_person(
        self,
        viewer: ViewerContext,
        *,
        principal_id: UUID,
        at: datetime | None = None,
    ) -> dict[str, object]:
        self._require_directory(viewer)
        observed_at = (at or datetime.now(UTC)).astimezone(UTC)
        candidate = next(
            (
                item
                for item in self._projection.list_candidates(viewer.workspace_id)
                if item.principal_id == principal_id
            ),
            None,
        )
        if candidate is None:
            raise PeopleFailure("NOT_FOUND")
        result = self._compose(viewer, candidate, at=observed_at)
        if result is None:
            raise PeopleFailure("NOT_FOUND")
        return result


__all__ = ["PeopleService", "PeopleViewVariant"]
