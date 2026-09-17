"""Artifact-owner port for immutable Presentation root/page JSON manifests."""

from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Callable
from uuid import UUID, uuid4
from psycopg.types.json import Jsonb
from packages.artifacts.infrastructure.local import LocalArtifactStore
from packages.artifacts.infrastructure.postgres import PostgresArtifactRepository
from packages.contracts.presentation import PresentationFailure


class DocumentSnapshotArtifacts:
    def __init__(self, connect: Callable[[], Any], root: Path):
        self._connect = connect
        self._root = root

    def _read(self, workspace: UUID, reference: dict[str, Any]) -> bytes:
        with self._connect() as c:
            row = c.execute(
                """SELECT relative_uri,content_hash,byte_size FROM artifact_manifests
                WHERE id=%s AND workspace_id=%s AND state='committed'""",
                (reference["artifact_id"], workspace),
            ).fetchone()
        if row is None:
            raise PresentationFailure("ARTIFACT_MISSING")
        if row[1] != reference["content_hash"]:
            raise PresentationFailure("ARTIFACT_CORRUPT")
        try:
            raw = LocalArtifactStore(self._root).resolve(row[0]).read_bytes()
        except FileNotFoundError as exc:
            raise PresentationFailure("ARTIFACT_MISSING") from exc
        except OSError as exc:
            raise PresentationFailure("STORAGE_UNAVAILABLE") from exc
        if len(raw) != row[2] or hashlib.sha256(raw).hexdigest() != row[1]:
            raise PresentationFailure("ARTIFACT_CORRUPT")
        return raw

    def commit(
        self,
        *,
        workspace_id: UUID,
        artifact_id: UUID,
        payload: dict[str, Any],
        parents: list[dict[str, Any]],
    ) -> dict[str, Any]:
        for parent in parents:
            self._read(workspace_id, parent)
        raw = json.dumps(
            payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
        ).encode()
        digest = hashlib.sha256(raw).hexdigest()
        relative = f"objects/{artifact_id}.json"
        temporary = None
        try:
            local = LocalArtifactStore(self._root)
            final = local.resolve(relative)
            temporary = local.root / ".staging" / f"{uuid4()}.json.tmp"
            temporary.write_bytes(raw)
            with temporary.open("rb") as f:
                os.fsync(f.fileno())
            try:
                os.link(temporary, final)
            except FileExistsError:
                if final.read_bytes() != raw:
                    raise PresentationFailure("ARTIFACT_CONFLICT")
            fd = os.open(final.parent, os.O_RDONLY)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)
            with self._connect() as c, c.transaction(), c.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO artifact_manifests
                    (id,workspace_id,producer_batch_id,artifact_type,entity,relative_uri,
                     content_hash,row_count,byte_size,schema_json,pii_class,state)
                    VALUES (%s,%s,NULL,'document_snapshot_json','AnalyticalDocument',%s,%s,1,%s,%s,'internal','committed')
                    ON CONFLICT(id) DO NOTHING""",
                    (
                        artifact_id,
                        workspace_id,
                        relative,
                        digest,
                        len(raw),
                        Jsonb({"version": 1, "columns": list(payload)}),
                    ),
                )
                for parent in parents:
                    PostgresArtifactRepository.add_dependency(
                        cursor, parent_id=parent["artifact_id"], child_id=artifact_id
                    )
        except OSError as exc:
            raise PresentationFailure("STORAGE_UNAVAILABLE") from exc
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
        reference = {"artifact_id": str(artifact_id), "content_hash": digest, "byte_size": len(raw)}
        self.verify(workspace_id=workspace_id, reference=reference, payload=payload)
        return reference

    def verify(
        self, *, workspace_id: UUID, reference: dict[str, Any], payload: dict[str, Any]
    ) -> None:
        if json.loads(self._read(workspace_id, reference)) != payload:
            raise PresentationFailure("ARTIFACT_CORRUPT")
