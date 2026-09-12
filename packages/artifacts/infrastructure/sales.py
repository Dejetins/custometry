"""Artifact Lifecycle adapter for the bounded immutable sales result."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any, cast
from uuid import UUID, uuid4

import pyarrow.parquet as pq  # pyright: ignore[reportMissingTypeStubs]

from psycopg.types.json import Jsonb
from packages.artifacts.infrastructure.local import LocalArtifactStore
from packages.artifacts.infrastructure.postgres import PostgresArtifactRepository
from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.data_pipeline import DataPipelineFailure


class SalesArtifactStore:
    def __init__(self, connect: Any, root: Path) -> None:
        self._connect = connect
        self._root = root

    @property
    def _local(self) -> LocalArtifactStore:
        return LocalArtifactStore(self._root)

    def _manifest(self, cursor: Any, workspace_id: UUID, artifact_id: str) -> dict[str, Any]:
        cursor.execute(
            """SELECT id, producer_batch_id, relative_uri, content_hash, byte_size, entity
               FROM artifact_manifests WHERE id=%s AND workspace_id=%s AND state='committed'""",
            (artifact_id, workspace_id),
        )
        row = cursor.fetchone()
        if row is None:
            raise AnalyticsFailure("ARTIFACT_NOT_VISIBLE")
        return dict(
            zip(
                ("artifact_id", "batch_id", "relative_uri", "content_hash", "byte_size", "entity"),
                row,
                strict=True,
            )
        )

    def _bytes(self, manifest: dict[str, Any]) -> bytes:
        try:
            path = self._local.resolve(manifest["relative_uri"])
            raw = path.read_bytes()
            if (
                len(raw) != manifest["byte_size"]
                or hashlib.sha256(raw).hexdigest() != manifest["content_hash"]
            ):
                raise AnalyticsFailure("ARTIFACT_INTEGRITY_FAILED")
            return raw
        except DataPipelineFailure as exc:
            raise AnalyticsFailure(exc.code) from exc
        except OSError as exc:
            raise AnalyticsFailure("ARTIFACT_UNAVAILABLE") from exc

    def read_sales_inputs(
        self, *, workspace_id: UUID, bindings: list[dict[str, Any]], supporting_artifacts: list[str]
    ) -> dict[str, tuple[dict[str, Any], ...]]:
        result: dict[str, tuple[dict[str, Any], ...]] = {}
        with self._connect() as connection, connection.cursor() as cursor:
            for artifact_id in supporting_artifacts:
                self._bytes(self._manifest(cursor, workspace_id, artifact_id))
            for binding in bindings:
                manifest = self._manifest(cursor, workspace_id, binding["artifact_id"])
                if (
                    manifest["entity"] != binding["entity"]
                    or manifest["content_hash"] != binding["content_hash"]
                ):
                    raise AnalyticsFailure("ARTIFACT_BINDING_MISMATCH")
                raw = self._bytes(manifest)
                import pyarrow as pa  # pyright: ignore[reportMissingTypeStubs]

                try:
                    result[binding["entity"]] = tuple(
                        cast(Any, pq).read_table(cast(Any, pa).BufferReader(raw)).to_pylist()
                    )
                except (ValueError, OSError) as exc:
                    raise AnalyticsFailure("ARTIFACT_FORMAT_INVALID") from exc
        return result

    def commit_sales(self, *, workspace_id: UUID, payload: dict[str, Any]) -> dict[str, Any]:
        raw = json.dumps(
            payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode()
        digest = hashlib.sha256(raw).hexdigest()
        result_id = UUID(payload["result_id"])
        relative = f"objects/{result_id}.json"
        temporary: Path | None = None
        try:
            final = self._local.resolve(relative)
            temporary = self._local.root / ".staging" / f"{uuid4()}.json.tmp"
            temporary.write_bytes(raw)
            with temporary.open("rb") as handle:
                os.fsync(handle.fileno())
            try:
                os.link(temporary, final)
            except FileExistsError:
                if final.read_bytes() != raw:
                    raise AnalyticsFailure("RESULT_ARTIFACT_IDENTITY_CONFLICT")
            directory_fd = os.open(final.parent, os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
            with (
                self._connect() as connection,
                connection.transaction(),
                connection.cursor() as cursor,
            ):
                parents = [
                    self._manifest(cursor, workspace_id, b["artifact_id"])
                    for b in payload["lineage"]["bindings"]
                ]
                cursor.execute(
                    """INSERT INTO artifact_manifests(id,workspace_id,producer_batch_id,artifact_type,entity,relative_uri,content_hash,row_count,byte_size,schema_json,pii_class,state)
                       VALUES (%s,%s,NULL,'sales_report_json','SalesDaily',%s,%s,%s,%s,%s,'internal','committed')
                       ON CONFLICT(id) DO NOTHING""",
                    (
                        result_id,
                        workspace_id,
                        relative,
                        digest,
                        len(payload["daily"]),
                        len(raw),
                        Jsonb(
                            {
                                "version": 1,
                                "columns": [
                                    "date",
                                    "net_revenue",
                                    "receipt_count",
                                    "average_receipt",
                                ],
                            }
                        ),
                    ),
                )
                committed = self._manifest(cursor, workspace_id, str(result_id))
                if committed["content_hash"] != digest or committed["relative_uri"] != relative:
                    raise AnalyticsFailure("RESULT_ARTIFACT_IDENTITY_CONFLICT")
                for parent in parents:
                    PostgresArtifactRepository.add_dependency(
                        cursor, parent_id=parent["artifact_id"], child_id=result_id
                    )
            return {
                "artifact_id": str(result_id),
                "relative_uri": relative,
                "content_hash": digest,
                "byte_size": len(raw),
                "immutable": True,
                "schema_version": "sales-report/v1",
            }
        except OSError as exc:
            raise AnalyticsFailure("RESULT_STORAGE_UNAVAILABLE") from exc
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)

    def verify_sales(self, *, workspace_id: UUID, payload: dict[str, Any]) -> None:
        with self._connect() as connection, connection.cursor() as cursor:
            manifest = self._manifest(cursor, workspace_id, payload["result_id"])
            reference = payload["manifest"]
            if (
                any(
                    manifest[key] != reference[key]
                    for key in ("content_hash", "relative_uri", "byte_size")
                )
                or reference["artifact_id"] != payload["result_id"]
                or reference["immutable"] is not True
                or reference["schema_version"] != "sales-report/v1"
            ):
                raise AnalyticsFailure("RESULT_ARTIFACT_IDENTITY_CONFLICT")
            expected = {k: v for k, v in payload.items() if k != "manifest"}
            if json.loads(self._bytes(manifest)) != expected:
                raise AnalyticsFailure("RESULT_ARTIFACT_IDENTITY_CONFLICT")
