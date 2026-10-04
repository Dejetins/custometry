"""Semantic-owned atomic immutable versions and compare-and-swap default pointer."""

from collections.abc import Callable
from typing import Any
from uuid import UUID, uuid4
import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb
from packages.contracts.semantic import (
    BusinessCalendarProfile,
    BusinessCalendarVersion,
    CalendarFailure,
    UpdateCalendarRequest,
    WorkspaceCalendarDefault,
)


def _version(row: dict[str, Any]) -> BusinessCalendarVersion:
    return BusinessCalendarVersion(
        version_id=row["id"],
        workspace_id=row["workspace_id"],
        content_hash=row["content_hash"],
        profile=row["profile_json"],
        created_by=row["created_by"],
        created_at=row["created_at"],
        previous_version_id=row["previous_version_id"],
    )


class PostgresCalendarRepository:
    def __init__(self, connect: Callable[[], psycopg.Connection[Any]]) -> None:
        self.connect = connect

    def provision(
        self,
        workspace_id: UUID,
        version_id: UUID,
        profile: BusinessCalendarProfile,
        content_hash: str,
    ) -> None:
        with self.connect() as c, c.transaction():
            c.execute(
                """INSERT INTO semantic_business_calendar_versions
                (id, workspace_id, content_hash, profile_json, created_by, previous_version_id, idempotency_key, request_hash, default_revision)
                VALUES (%s,%s,%s,%s,NULL,NULL,NULL,NULL,0) ON CONFLICT (workspace_id,id) DO NOTHING""",
                (version_id, workspace_id, content_hash, Jsonb(profile.model_dump(mode="json"))),
            )
            c.execute(
                """INSERT INTO semantic_workspace_calendar_defaults (workspace_id,revision,version_id)
                VALUES (%s,0,%s) ON CONFLICT (workspace_id) DO NOTHING""",
                (workspace_id, version_id),
            )

    def get_default(self, workspace_id: UUID) -> WorkspaceCalendarDefault:
        with self.connect() as c, c.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """SELECT v.*, d.revision FROM semantic_workspace_calendar_defaults d
                JOIN semantic_business_calendar_versions v ON (v.workspace_id,v.id)=(d.workspace_id,d.version_id)
                WHERE d.workspace_id=%s""",
                (workspace_id,),
            )
            row = cur.fetchone()
            if row is None:
                raise CalendarFailure("NOT_FOUND")
            return WorkspaceCalendarDefault(
                workspace_id=workspace_id, revision=row["revision"], calendar=_version(row)
            )

    def get_version(self, workspace_id: UUID, version_id: UUID) -> BusinessCalendarVersion:
        with self.connect() as c, c.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "SELECT * FROM semantic_business_calendar_versions WHERE workspace_id=%s AND id=%s",
                (workspace_id, version_id),
            )
            row = cur.fetchone()
            if row is None:
                raise CalendarFailure("NOT_FOUND")
            return _version(row)

    def update_default(
        self,
        workspace_id: UUID,
        principal_id: UUID,
        request: UpdateCalendarRequest,
        content_hash: str,
        request_hash: str,
    ) -> WorkspaceCalendarDefault:
        with self.connect() as c, c.transaction(), c.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "SELECT * FROM semantic_workspace_calendar_defaults WHERE workspace_id=%s FOR UPDATE",
                (workspace_id,),
            )
            default = cur.fetchone()
            if default is None:
                raise CalendarFailure("NOT_FOUND")
            cur.execute(
                "SELECT * FROM semantic_business_calendar_versions WHERE workspace_id=%s AND idempotency_key=%s",
                (workspace_id, request.idempotency_key),
            )
            prior = cur.fetchone()
            if prior is not None:
                if prior["request_hash"] != request_hash:
                    raise CalendarFailure("CALENDAR_IDEMPOTENCY_CONFLICT")
                return WorkspaceCalendarDefault(
                    workspace_id=workspace_id,
                    revision=prior["default_revision"],
                    calendar=_version(prior),
                )
            if default["revision"] != request.expected_revision:
                raise CalendarFailure("CALENDAR_REVISION_CONFLICT")
            revision = default["revision"] + 1
            cur.execute(
                """INSERT INTO semantic_business_calendar_versions
                (id,workspace_id,content_hash,profile_json,created_by,previous_version_id,idempotency_key,request_hash,default_revision)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *""",
                (
                    uuid4(),
                    workspace_id,
                    content_hash,
                    Jsonb(request.profile.model_dump(mode="json")),
                    principal_id,
                    default["version_id"],
                    request.idempotency_key,
                    request_hash,
                    revision,
                ),
            )
            row = cur.fetchone()
            assert row is not None
            cur.execute(
                "UPDATE semantic_workspace_calendar_defaults SET revision=%s,version_id=%s WHERE workspace_id=%s",
                (revision, row["id"], workspace_id),
            )
            return WorkspaceCalendarDefault(
                workspace_id=workspace_id, revision=revision, calendar=_version(row)
            )
