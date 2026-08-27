"""PostgreSQL adapter for the Identity-owned contributor projection and policy."""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
import hashlib
import json
from typing import cast
from uuid import UUID

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from packages.contracts.people import (
    ContributorActivityBucket,
    ContributorCandidate,
    ContributorDomainEvent,
    PeopleFailure,
    PeopleViewVariant,
    ProjectionRebuildResult,
    ResourceType,
    ViewerContext,
)
from packages.identity_access.application.organization import (
    OrganizationFailure,
    OrganizationService,
)
from packages.identity_access.domain.policy import Actor


Connect = Callable[[], psycopg.Connection[object]]


def _canonical_event(event: ContributorDomainEvent) -> dict[str, object]:
    return {
        "event_id": str(event.event_id),
        "workspace_id": str(event.workspace_id),
        "principal_id": str(event.principal_id),
        "event_type": event.event_type,
        "occurred_at": event.occurred_at.astimezone(UTC).isoformat(),
        "resource_type": event.resource_type,
        "resource_id": None if event.resource_id is None else str(event.resource_id),
        "safe_resource_title": event.safe_resource_title,
        "display_name": event.display_name,
        "title": event.title,
        "title_visible": event.title_visible,
        "contribution_labels": list(event.contribution_labels),
        "expertise_domains": list(event.expertise_domains),
    }


class PostgresContributorProjection:
    """Store only allowlisted redacted events and derived privacy-safe buckets."""

    def __init__(self, connect: Connect) -> None:
        self._connect = connect

    def append_redacted_events(self, events: tuple[ContributorDomainEvent, ...]) -> int:
        inserted = 0
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                for event in events:
                    cursor.execute(
                        """
                        SELECT status FROM identity_memberships
                        WHERE workspace_id = %s AND principal_id = %s
                        """,
                        (event.workspace_id, event.principal_id),
                    )
                    if cursor.fetchone() is None:
                        raise PeopleFailure("EVENT_SUBJECT_NOT_FOUND")
                    cursor.execute(
                        """
                        SELECT workspace_id, principal_id, event_type, occurred_at,
                               resource_type, resource_id, safe_resource_title,
                               display_name, title, title_visible,
                               contribution_labels, expertise_domains
                        FROM identity_contributor_projection_events
                        WHERE event_id = %s
                        """,
                        (event.event_id,),
                    )
                    existing = cursor.fetchone()
                    if existing is not None:
                        stored = ContributorDomainEvent(
                            event_id=event.event_id,
                            workspace_id=UUID(str(existing["workspace_id"])),
                            principal_id=UUID(str(existing["principal_id"])),
                            event_type=str(existing["event_type"]),  # type: ignore[arg-type]
                            occurred_at=existing["occurred_at"],
                            resource_type=existing["resource_type"],  # type: ignore[arg-type]
                            resource_id=(
                                None
                                if existing["resource_id"] is None
                                else UUID(str(existing["resource_id"]))
                            ),
                            safe_resource_title=existing["safe_resource_title"],
                            display_name=existing["display_name"],
                            title=existing["title"],
                            title_visible=bool(existing["title_visible"]),
                            contribution_labels=tuple(existing["contribution_labels"]),
                            expertise_domains=tuple(existing["expertise_domains"]),
                        )
                        if _canonical_event(stored) != _canonical_event(event):
                            raise PeopleFailure("EVENT_ID_CONFLICT")
                        continue
                    cursor.execute(
                        """
                        INSERT INTO identity_contributor_projection_events
                          (event_id, workspace_id, principal_id, event_type, occurred_at,
                           resource_type, resource_id, safe_resource_title, display_name,
                           title, title_visible, contribution_labels, expertise_domains)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            event.event_id,
                            event.workspace_id,
                            event.principal_id,
                            event.event_type,
                            event.occurred_at,
                            event.resource_type,
                            event.resource_id,
                            event.safe_resource_title,
                            event.display_name,
                            event.title,
                            event.title_visible,
                            Jsonb(list(event.contribution_labels)),
                            Jsonb(list(event.expertise_domains)),
                        ),
                    )
                    inserted += 1
        return inserted

    def rebuild(self, workspace_id: UUID, *, rebuilt_at: datetime) -> ProjectionRebuildResult:
        with self._connect() as connection, connection.transaction():
            with connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(
                    """
                    SELECT event_id, workspace_id, principal_id, event_type, occurred_at,
                           resource_type, resource_id, safe_resource_title, display_name,
                           title, title_visible, contribution_labels, expertise_domains
                    FROM identity_contributor_projection_events
                    WHERE workspace_id = %s
                    ORDER BY occurred_at, event_id
                    """,
                    (workspace_id,),
                )
                rows = list(cursor.fetchall())
                digest_payload = [
                    {
                        key: (
                            value.astimezone(UTC).isoformat()
                            if isinstance(value, datetime)
                            else str(value)
                            if isinstance(value, UUID)
                            else value
                        )
                        for key, value in row.items()
                    }
                    for row in rows
                ]
                projection_version = hashlib.sha256(
                    json.dumps(
                        digest_payload,
                        sort_keys=True,
                        separators=(",", ":"),
                        ensure_ascii=True,
                    ).encode("utf-8")
                ).hexdigest()

                cursor.execute(
                    "DELETE FROM identity_contributor_profiles WHERE workspace_id = %s",
                    (workspace_id,),
                )
                cursor.execute(
                    "DELETE FROM identity_contributor_activity_buckets WHERE workspace_id = %s",
                    (workspace_id,),
                )

                profiles: dict[UUID, dict[str, object]] = {}
                buckets: dict[tuple[UUID, str, UUID, object], dict[str, object]] = {}
                for row in rows:
                    principal_id = UUID(str(row["principal_id"]))
                    if row["event_type"] == "profile.published":
                        profiles[principal_id] = row
                        continue
                    resource_id = UUID(str(row["resource_id"]))
                    occurred_at = row["occurred_at"]
                    key = (
                        principal_id,
                        str(row["resource_type"]),
                        resource_id,
                        occurred_at.date(),
                    )
                    bucket = buckets.setdefault(
                        key,
                        {
                            "safe_resource_title": str(row["safe_resource_title"]),
                            "created_count": 0,
                            "published_count": 0,
                            "materially_updated_count": 0,
                            "maintained_count": 0,
                            "coauthored_count": 0,
                            "reviewed_count": 0,
                            "resolved_count": 0,
                            "last_activity_at": occurred_at,
                        },
                    )
                    counter = {
                        "resource.created": "created_count",
                        "resource.published": "published_count",
                        "resource.materially_updated": "materially_updated_count",
                        "resource.maintained": "maintained_count",
                        "collaboration.coauthored": "coauthored_count",
                        "collaboration.reviewed": "reviewed_count",
                        "collaboration.resolved": "resolved_count",
                    }[str(row["event_type"])]
                    bucket[counter] = cast(int, bucket[counter]) + 1
                    if occurred_at >= cast(datetime, bucket["last_activity_at"]):
                        bucket["last_activity_at"] = occurred_at
                        bucket["safe_resource_title"] = str(row["safe_resource_title"])

                for principal_id, row in profiles.items():
                    cursor.execute(
                        """
                        INSERT INTO identity_contributor_profiles
                          (workspace_id, principal_id, display_name, title, title_visible,
                           contribution_labels, expertise_domains, projection_version, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            workspace_id,
                            principal_id,
                            row["display_name"],
                            row["title"],
                            row["title_visible"],
                            Jsonb(list(cast(list[object], row["contribution_labels"]))),
                            Jsonb(list(cast(list[object], row["expertise_domains"]))),
                            projection_version,
                            row["occurred_at"],
                        ),
                    )
                for key, bucket in buckets.items():
                    principal_id, resource_type, resource_id, activity_date = key
                    cursor.execute(
                        """
                        INSERT INTO identity_contributor_activity_buckets
                          (workspace_id, principal_id, resource_type, resource_id,
                           activity_date, safe_resource_title, created_count,
                           published_count, materially_updated_count, maintained_count,
                           coauthored_count, reviewed_count, resolved_count,
                           last_activity_at, projection_version)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            workspace_id,
                            principal_id,
                            resource_type,
                            resource_id,
                            activity_date,
                            bucket["safe_resource_title"],
                            bucket["created_count"],
                            bucket["published_count"],
                            bucket["materially_updated_count"],
                            bucket["maintained_count"],
                            bucket["coauthored_count"],
                            bucket["reviewed_count"],
                            bucket["resolved_count"],
                            bucket["last_activity_at"],
                            projection_version,
                        ),
                    )
                cursor.execute(
                    """
                    INSERT INTO identity_contributor_projection_state
                      (workspace_id, projection_version, event_count, rebuilt_at)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (workspace_id) DO UPDATE SET
                      projection_version = EXCLUDED.projection_version,
                      event_count = EXCLUDED.event_count,
                      rebuilt_at = EXCLUDED.rebuilt_at
                    """,
                    (workspace_id, projection_version, len(rows), rebuilt_at),
                )
        return ProjectionRebuildResult(
            workspace_id=workspace_id,
            event_count=len(rows),
            bucket_count=len(buckets),
            projection_version=projection_version,
            rebuilt_at=rebuilt_at,
        )

    def list_candidates(self, workspace_id: UUID) -> tuple[ContributorCandidate, ...]:
        with self._connect() as connection, connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT p.principal_id, p.display_name, p.title, p.title_visible,
                       p.contribution_labels, p.expertise_domains,
                       p.projection_version, p.updated_at,
                       a.org_unit_id, v.display_name AS org_unit_name
                FROM identity_contributor_profiles AS p
                JOIN identity_memberships AS m
                  ON m.workspace_id = p.workspace_id
                 AND m.principal_id = p.principal_id
                 AND m.status = 'active'
                JOIN organization_primary_assignments AS a
                  ON a.workspace_id = p.workspace_id
                 AND a.principal_id = p.principal_id
                 AND a.effective_from <= CURRENT_TIMESTAMP
                 AND (a.effective_to IS NULL OR a.effective_to > CURRENT_TIMESTAMP)
                 AND a.needs_department_assignment = FALSE
                JOIN organization_units AS u ON u.id = a.org_unit_id
                JOIN organization_unit_versions AS v
                  ON v.org_unit_id = u.id AND v.version = u.current_version
                 AND v.status = 'active'
                WHERE p.workspace_id = %s
                ORDER BY lower(p.display_name), p.principal_id
                """,
                (workspace_id,),
            )
            return tuple(
                ContributorCandidate(
                    principal_id=UUID(str(row["principal_id"])),
                    display_name=str(row["display_name"]),
                    title=(
                        str(row["title"])
                        if bool(row["title_visible"]) and row["title"] is not None
                        else None
                    ),
                    contribution_labels=tuple(row["contribution_labels"]),
                    expertise_domains=tuple(row["expertise_domains"]),
                    org_unit_id=UUID(str(row["org_unit_id"])),
                    org_unit_name=str(row["org_unit_name"]),
                    projection_version=str(row["projection_version"]),
                    updated_at=row["updated_at"],
                )
                for row in cursor.fetchall()
            )

    def activity_buckets(
        self, workspace_id: UUID, principal_id: UUID
    ) -> tuple[ContributorActivityBucket, ...]:
        with self._connect() as connection, connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT principal_id, resource_type, resource_id, safe_resource_title,
                       activity_date, created_count, published_count,
                       materially_updated_count, maintained_count, coauthored_count,
                       reviewed_count, resolved_count, last_activity_at
                FROM identity_contributor_activity_buckets
                WHERE workspace_id = %s AND principal_id = %s
                ORDER BY activity_date DESC, resource_type, resource_id
                """,
                (workspace_id, principal_id),
            )
            return tuple(
                ContributorActivityBucket(
                    principal_id=UUID(str(row["principal_id"])),
                    resource_type=str(row["resource_type"]),  # type: ignore[arg-type]
                    resource_id=UUID(str(row["resource_id"])),
                    safe_resource_title=str(row["safe_resource_title"]),
                    activity_date=row["activity_date"],
                    created_count=int(row["created_count"]),
                    published_count=int(row["published_count"]),
                    materially_updated_count=int(row["materially_updated_count"]),
                    maintained_count=int(row["maintained_count"]),
                    coauthored_count=int(row["coauthored_count"]),
                    reviewed_count=int(row["reviewed_count"]),
                    resolved_count=int(row["resolved_count"]),
                    last_activity_at=row["last_activity_at"],
                )
                for row in cursor.fetchall()
            )


class PostgresContributorAuthorization:
    """Resolve self/leader/grantee scope and current resource visibility."""

    def __init__(self, connect: Connect, organization: OrganizationService) -> None:
        self._connect = connect
        self._organization = organization

    def view_variant(
        self, viewer: ViewerContext, target_principal_id: UUID, *, at: datetime
    ) -> PeopleViewVariant:
        with self._connect() as connection, connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT a.org_unit_id
                FROM identity_memberships AS m
                JOIN organization_primary_assignments AS a
                  ON a.workspace_id = m.workspace_id AND a.principal_id = m.principal_id
                 AND a.effective_from <= %s
                 AND (a.effective_to IS NULL OR a.effective_to > %s)
                 AND a.needs_department_assignment = FALSE
                WHERE m.workspace_id = %s AND m.principal_id = %s AND m.status = 'active'
                ORDER BY a.effective_from DESC LIMIT 1
                """,
                (at, at, viewer.workspace_id, target_principal_id),
            )
            target = cursor.fetchone()
            if target is None:
                raise PeopleFailure("NOT_FOUND")
            target_org_unit_id = UUID(str(target["org_unit_id"]))
            cursor.execute(
                """
                SELECT a.org_unit_id
                FROM identity_memberships AS m
                JOIN organization_primary_assignments AS a
                  ON a.workspace_id = m.workspace_id AND a.principal_id = m.principal_id
                 AND a.effective_from <= %s
                 AND (a.effective_to IS NULL OR a.effective_to > %s)
                 AND a.needs_department_assignment = FALSE
                WHERE m.workspace_id = %s AND m.principal_id = %s AND m.status = 'active'
                ORDER BY a.effective_from DESC LIMIT 1
                """,
                (at, at, viewer.workspace_id, viewer.principal_id),
            )
            viewer_row = cursor.fetchone()
            if viewer_row is None:
                raise PeopleFailure("FORBIDDEN")
            viewer_org_unit_id = UUID(str(viewer_row["org_unit_id"]))
            if viewer.principal_id == target_principal_id:
                return "self"
            if "organization.activity.read" not in viewer.permissions:
                return "public"

            cursor.execute(
                """
                WITH RECURSIVE target_ancestors(id) AS (
                  SELECT %s::uuid
                  UNION ALL
                  SELECT v.parent_org_unit_id
                  FROM target_ancestors AS a
                  JOIN organization_units AS u ON u.id = a.id
                  JOIN organization_unit_versions AS v
                    ON v.org_unit_id = u.id AND v.version = u.current_version
                  WHERE v.parent_org_unit_id IS NOT NULL
                )
                SELECT EXISTS (
                  SELECT 1
                  FROM organization_leadership_assignments AS l
                  WHERE l.workspace_id = %s AND l.principal_id = %s
                    AND l.effective_from <= %s
                    AND (l.effective_to IS NULL OR l.effective_to > %s)
                    AND l.permissions ? 'organization.activity.read'
                    AND (
                      l.scope_mode = 'workspace'
                      OR (l.scope_mode = 'unit' AND l.org_unit_id = %s)
                      OR (l.scope_mode = 'subtree' AND l.org_unit_id IN (
                        SELECT id FROM target_ancestors
                      ))
                    )
                ) AS allowed
                """,
                (
                    target_org_unit_id,
                    viewer.workspace_id,
                    viewer.principal_id,
                    at,
                    at,
                    target_org_unit_id,
                ),
            )
            leadership = cursor.fetchone()
            assert leadership is not None
            if bool(leadership["allowed"]):
                return "leader"

            cursor.execute(
                """
                SELECT EXISTS (
                  SELECT 1 FROM organization_cross_department_grants AS g
                  WHERE g.workspace_id = %s
                    AND g.target_org_unit_id = %s
                    AND g.resource_type IS NULL AND g.resource_id IS NULL
                    AND g.actions ? 'organization.activity.read'
                    AND g.effective_from <= %s
                    AND (g.expires_at IS NULL OR g.expires_at > %s)
                    AND g.revoked_at IS NULL
                    AND (
                      (g.subject_type = 'principal' AND g.subject_id = %s)
                      OR (g.subject_type = 'org_unit' AND g.subject_id = %s)
                    )
                ) AS allowed
                """,
                (
                    viewer.workspace_id,
                    target_org_unit_id,
                    at,
                    at,
                    viewer.principal_id,
                    viewer_org_unit_id,
                ),
            )
            grant = cursor.fetchone()
            assert grant is not None
            return "grantee" if bool(grant["allowed"]) else "public"

    def resource_visible(
        self,
        viewer: ViewerContext,
        *,
        target_org_unit_id: UUID,
        resource_type: ResourceType,
        resource_id: UUID,
    ) -> bool:
        actor = Actor(
            principal_id=viewer.principal_id,
            workspace_id=viewer.workspace_id,
            email="redacted@invalid.test",
            permissions=viewer.permissions,
        )
        try:
            return self._organization.decide_access(
                actor,
                target_org_unit_id=target_org_unit_id,
                action="view_snapshot",
                resource_type=resource_type,
                resource_id=resource_id,
            ).allowed
        except OrganizationFailure:
            return False


__all__ = ["PostgresContributorAuthorization", "PostgresContributorProjection"]
