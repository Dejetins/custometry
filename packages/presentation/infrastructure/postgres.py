"""Owned document CAS, idempotency and immutable version transactions."""

from __future__ import annotations
from typing import Any, Callable
from uuid import UUID
from psycopg.types.json import Jsonb
from packages.contracts.presentation import PresentationFailure, SaveRequest
from packages.presentation.domain.reports import digest


class PostgresReportRepository:
    def __init__(self, connect: Callable[[], Any], *, checkpoint: Callable[[], None] | None = None):
        self._connect = connect
        self._checkpoint = checkpoint or (lambda: None)

    def put_reference(
        self, workspace_id: UUID, owner: UUID, value: dict[str, Any]
    ) -> dict[str, Any]:
        reference = value["reference"]
        with self._connect() as c:
            c.execute(
                """INSERT INTO presentation_references
                (id,workspace_id,owner_principal_id,kind,content_hash,payload)
                VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""",
                (
                    reference["id"],
                    workspace_id,
                    owner,
                    value["kind"],
                    reference["content_hash"],
                    Jsonb(value["payload"]),
                ),
            )
        return self.get_reference(workspace_id, owner, reference, value["kind"])

    def get_reference(
        self, workspace_id: UUID, owner: UUID, reference: dict[str, Any], kind: str
    ) -> dict[str, Any]:
        with self._connect() as c:
            row = c.execute(
                """SELECT payload,content_hash FROM presentation_references
                WHERE workspace_id=%s AND owner_principal_id=%s AND id=%s AND kind=%s""",
                (workspace_id, owner, reference["id"], kind),
            ).fetchone()
        if row is None or row[1] != reference["content_hash"] or digest(row[0]) != row[1]:
            raise PresentationFailure("INVALID_REFERENCE")
        return {"kind": kind, "reference": reference, "payload": row[0]}

    def latest(
        self, workspace_id: UUID, owner: UUID, report_id: UUID, snapshot_id: UUID | None = None
    ) -> dict[str, Any]:
        with self._connect() as c:
            row = c.execute(
                """SELECT v.payload FROM presentation_documents d
                JOIN presentation_versions v ON v.document_id=d.id
                WHERE d.id=%s AND d.workspace_id=%s AND d.owner_principal_id=%s
                  AND ((%s::uuid IS NULL AND v.id=d.latest_version_id) OR v.snapshot_id=%s)""",
                (report_id, workspace_id, owner, snapshot_id, snapshot_id),
            ).fetchone()
        if row is None:
            raise PresentationFailure("NOT_FOUND")
        return row[0]

    def candidates(self, workspace_id: UUID, owner: UUID) -> list[UUID]:
        with self._connect() as c:
            return [
                r[0]
                for r in c.execute(
                    """SELECT id FROM presentation_documents
                WHERE workspace_id=%s AND owner_principal_id=%s AND latest_version_id IS NOT NULL
                ORDER BY id""",
                    (workspace_id, owner),
                ).fetchall()
            ]

    def save(
        self,
        workspace_id: UUID,
        owner: UUID,
        report_id: UUID,
        request_hash: str,
        request: SaveRequest,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        with self._connect() as c, c.transaction():
            if request.expected_revision == 0:
                c.execute(
                    """INSERT INTO presentation_documents(id,workspace_id,owner_principal_id)
                    VALUES (%s,%s,%s) ON CONFLICT DO NOTHING""",
                    (report_id, workspace_id, owner),
                )
            row = c.execute(
                """SELECT revision FROM presentation_documents
                WHERE id=%s AND workspace_id=%s AND owner_principal_id=%s FOR UPDATE""",
                (report_id, workspace_id, owner),
            ).fetchone()
            if row is None:
                raise PresentationFailure("NOT_FOUND")
            previous = c.execute(
                """SELECT request_hash,payload FROM presentation_versions
                WHERE document_id=%s AND idempotency_key=%s""",
                (report_id, request.idempotency_key),
            ).fetchone()
            if previous is not None:
                if previous[0] != request_hash:
                    raise PresentationFailure("IDEMPOTENCY_CONFLICT")
                return previous[1]
            if row[0] != request.expected_revision:
                raise PresentationFailure("REVISION_CONFLICT")
            c.execute(
                """INSERT INTO presentation_versions
                (id,document_id,revision,snapshot_id,idempotency_key,request_hash,payload)
                VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                (
                    payload["version_id"],
                    report_id,
                    payload["revision"],
                    payload["snapshot_id"],
                    request.idempotency_key,
                    request_hash,
                    Jsonb(payload),
                ),
            )
            self._checkpoint()
            updated = c.execute(
                """UPDATE presentation_documents SET revision=%s,latest_version_id=%s
                WHERE id=%s AND revision=%s""",
                (payload["revision"], payload["version_id"], report_id, request.expected_revision),
            )
            if updated.rowcount != 1:
                raise PresentationFailure("REVISION_CONFLICT")
        return payload
