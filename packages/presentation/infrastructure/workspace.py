"""Presentation-only persistence: one transaction for report and companion view CAS."""

from __future__ import annotations
from typing import Any, Callable
from uuid import UUID
from psycopg.types.json import Jsonb
from packages.contracts.presentation import PresentationFailure
from packages.contracts.presentation.workspace import (
    SavedViewV1,
    WorkspaceSaveRequest,
    SaveViewRequest,
)
from packages.presentation.infrastructure.postgres import PostgresReportRepository


class PostgresWorkspaceRepository(PostgresReportRepository):
    def all_candidates(self, workspace: UUID) -> list[UUID]:
        with self._connect() as c:
            return [
                r[0]
                for r in c.execute(
                    "SELECT id FROM presentation_documents WHERE workspace_id=%s AND latest_version_id IS NOT NULL ORDER BY id",
                    (workspace,),
                ).fetchall()
            ]

    def metadata(self, workspace: UUID, report: UUID) -> dict[str, Any]:
        with self._connect() as c:
            r = c.execute(
                """SELECT creator_principal_id,revision,latest_version_id
                FROM presentation_documents WHERE workspace_id=%s AND id=%s""",
                (workspace, report),
            ).fetchone()
        if r is None:
            raise PresentationFailure("NOT_FOUND")
        return dict(creator=r[0], revision=r[1], version_id=r[2])

    def read(
        self,
        workspace: UUID,
        report: UUID,
        snapshot: UUID | None = None,
        version: UUID | None = None,
    ) -> dict[str, Any]:
        with self._connect() as c:
            r = c.execute(
                """SELECT v.payload FROM presentation_documents d
                JOIN presentation_versions v ON v.document_id=d.id
                WHERE d.workspace_id=%s AND d.id=%s AND
                ((%s::uuid IS NOT NULL AND v.snapshot_id=%s) OR
                 (%s::uuid IS NOT NULL AND v.id=%s) OR
                 (%s::uuid IS NULL AND %s::uuid IS NULL AND v.id=d.latest_version_id))""",
                (workspace, report, snapshot, snapshot, version, version, snapshot, version),
            ).fetchone()
        if r is None:
            raise PresentationFailure("NOT_FOUND")
        return r[0]

    def retired_ids(self, workspace: UUID, report: UUID) -> set[UUID]:
        with self._connect() as c:
            rows = c.execute(
                """SELECT v.payload FROM presentation_versions v JOIN presentation_documents d ON d.id=v.document_id
                WHERE d.workspace_id=%s AND d.id=%s ORDER BY v.revision""",
                (workspace, report),
            ).fetchall()
        previous: set[UUID] = set()
        retired: set[UUID] = set()
        for row in rows:
            value = row[0]
            if value["contract_version"] == "draft-report/v1":
                from packages.contracts.presentation.workspace import legacy_instance_ids

                workset, cards = legacy_instance_ids(report)
                ids = {workset, *cards.values()}
            else:
                sets = value["composition"]["definition"]["worksets"]
                ids = {UUID(w["workset_id"]) for w in sets} | {
                    UUID(c["card_id"]) for w in sets for c in w["cards"]
                }
            retired |= previous - ids
            previous = ids
        return retired

    def replay(
        self, workspace: UUID, report: UUID, key: UUID, request_hash: str
    ) -> dict[str, Any] | None:
        with self._connect() as c:
            r = c.execute(
                """SELECT v.request_hash,v.payload FROM presentation_versions v
                JOIN presentation_documents d ON d.id=v.document_id
                WHERE d.workspace_id=%s AND d.id=%s AND v.idempotency_key=%s""",
                (workspace, report, key),
            ).fetchone()
        if r is None:
            return None
        if r[0] != request_hash:
            raise PresentationFailure("IDEMPOTENCY_CONFLICT")
        return r[1]

    def view(
        self, workspace: UUID, owner: UUID, view_id: UUID, version: UUID | None = None
    ) -> SavedViewV1:
        with self._connect() as c:
            r = c.execute(
                """SELECT v.payload FROM presentation_saved_views s
                JOIN presentation_saved_view_versions v ON v.saved_view_id=s.id
                WHERE s.workspace_id=%s AND s.owner_principal_id=%s AND s.id=%s
                AND v.id=COALESCE(%s,s.latest_version_id)""",
                (workspace, owner, view_id, version),
            ).fetchone()
        if r is None:
            raise PresentationFailure("NOT_FOUND")
        return SavedViewV1.model_validate(r[0])

    def views(self, workspace: UUID, owner: UUID, report: UUID) -> list[SavedViewV1]:
        with self._connect() as c:
            rows = c.execute(
                """SELECT v.payload FROM presentation_saved_views s
                JOIN presentation_saved_view_versions v ON v.id=s.latest_version_id
                WHERE s.workspace_id=%s AND s.owner_principal_id=%s AND s.document_id=%s ORDER BY s.id""",
                (workspace, owner, report),
            ).fetchall()
        return [SavedViewV1.model_validate(r[0]) for r in rows]

    @staticmethod
    def _lock_view(c: Any, value: SavedViewV1) -> int:
        c.execute(
            """INSERT INTO presentation_saved_views(id,workspace_id,owner_principal_id,document_id)
            VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING""",
            (value.saved_view_id, value.workspace_id, value.owner_principal_id, value.report_id),
        )
        r = c.execute(
            """SELECT revision FROM presentation_saved_views WHERE id=%s AND workspace_id=%s
            AND owner_principal_id=%s AND document_id=%s FOR UPDATE""",
            (value.saved_view_id, value.workspace_id, value.owner_principal_id, value.report_id),
        ).fetchone()
        if r is None:
            raise PresentationFailure("NOT_FOUND")
        return int(r[0])

    @staticmethod
    def _insert_view(c: Any, value: SavedViewV1, key: UUID, request_hash: str) -> None:
        c.execute(
            """INSERT INTO presentation_saved_view_versions
            (id,saved_view_id,document_id,revision,document_version_id,idempotency_key,request_hash,payload)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
            (
                value.version_id,
                value.saved_view_id,
                value.report_id,
                value.revision,
                value.document_version_id,
                key,
                request_hash,
                Jsonb(value.model_dump(mode="json")),
            ),
        )
        c.execute(
            "UPDATE presentation_saved_views SET revision=%s,latest_version_id=%s WHERE id=%s",
            (value.revision, value.version_id, value.saved_view_id),
        )

    def save_workspace(
        self,
        workspace: UUID,
        owner: UUID,
        report: UUID,
        request: WorkspaceSaveRequest,
        request_hash: str,
        payload: dict[str, Any],
        view: SavedViewV1,
        recheck: Callable[[], None],
    ) -> dict[str, Any]:
        with self._connect() as c, c.transaction():
            row = c.execute(
                """SELECT revision,creator_principal_id FROM presentation_documents
                WHERE workspace_id=%s AND id=%s FOR UPDATE""",
                (workspace, report),
            ).fetchone()
            if row is None or row[1] != owner:
                raise PresentationFailure("FORBIDDEN")
            replay = c.execute(
                "SELECT request_hash,payload FROM presentation_versions WHERE document_id=%s AND idempotency_key=%s",
                (report, request.idempotency_key),
            ).fetchone()
            if replay:
                if replay[0] != request_hash:
                    raise PresentationFailure("IDEMPOTENCY_CONFLICT")
                recheck()
                return replay[1]
            if row[0] != request.expected_revision:
                raise PresentationFailure("REVISION_CONFLICT")
            if self._lock_view(c, view) != request.expected_saved_view_revision:
                raise PresentationFailure("SAVED_VIEW_REVISION_CONFLICT")
            c.execute(
                """INSERT INTO presentation_versions
                (id,document_id,revision,snapshot_id,idempotency_key,request_hash,payload,contract_version)
                VALUES (%s,%s,%s,%s,%s,%s,%s,'configured-report/v2')""",
                (
                    payload["version_id"],
                    report,
                    payload["revision"],
                    payload["snapshot_id"],
                    request.idempotency_key,
                    request_hash,
                    Jsonb(payload),
                ),
            )
            self._insert_view(c, view, request.idempotency_key, request_hash)
            self._checkpoint()
            recheck()
            c.execute(
                "UPDATE presentation_documents SET revision=%s,latest_version_id=%s WHERE id=%s",
                (payload["revision"], payload["version_id"], report),
            )
        return payload

    def save_view(
        self,
        value: SavedViewV1,
        request: SaveViewRequest,
        request_hash: str,
        recheck: Callable[[], None],
    ) -> SavedViewV1:
        with self._connect() as c, c.transaction():
            # Same lock order as definition Save avoids report/view inversion.
            c.execute(
                "SELECT id FROM presentation_documents WHERE workspace_id=%s AND id=%s FOR UPDATE",
                (value.workspace_id, value.report_id),
            )
            revision = self._lock_view(c, value)
            replay = c.execute(
                "SELECT request_hash,payload FROM presentation_saved_view_versions WHERE saved_view_id=%s AND idempotency_key=%s",
                (value.saved_view_id, request.idempotency_key),
            ).fetchone()
            if replay:
                if replay[0] != request_hash:
                    raise PresentationFailure("IDEMPOTENCY_CONFLICT")
                recheck()
                return SavedViewV1.model_validate(replay[1])
            if revision != request.expected_revision:
                raise PresentationFailure("SAVED_VIEW_REVISION_CONFLICT")
            self._insert_view(c, value, request.idempotency_key, request_hash)
            self._checkpoint()
            recheck()
        return value
