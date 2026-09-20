"""Immutable v2 JSON admission using existing artifact manifests and dependencies."""

from __future__ import annotations
import hashlib
import json
import os
from typing import Any
from uuid import uuid4
from psycopg.types.json import Jsonb
from packages.artifacts.infrastructure.sales import SalesArtifactStore
from packages.artifacts.infrastructure.postgres import PostgresArtifactRepository
from packages.contracts.analytics import AnalyticsFailure


class WorkspaceArtifactStore(SalesArtifactStore):
    def commit_workspace(
        self, *, workspace_id: Any, payload: dict[str, Any], bindings: list[dict[str, Any]]
    ) -> dict[str, Any]:
        version = payload["schema_version"]
        if version not in {"metric-workspace/v2", "card-comparison/v1"}:
            raise AnalyticsFailure("UNSUPPORTED_RESULT_VERSION")
        raw = json.dumps(
            payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
        ).encode()
        content_hash = hashlib.sha256(raw).hexdigest()
        artifact_id = payload.get("result_id") or str(uuid4())
        # Comparison identity is content-addressed; no card IDs enter metric result identity.
        if version == "card-comparison/v1":
            from uuid import UUID, uuid5

            artifact_id = str(uuid5(UUID("7aab35da-cb8b-49ba-97c0-94f93dc9a852"), content_hash))
        relative = f"objects/{artifact_id}.json"
        temporary = self._local.root / ".staging" / f"{uuid4()}.json.tmp"
        try:
            final = self._local.resolve(relative)
            temporary.write_bytes(raw)
            with temporary.open("rb") as handle:
                os.fsync(handle.fileno())
            try:
                os.link(temporary, final)
            except FileExistsError:
                if final.read_bytes() != raw:
                    raise AnalyticsFailure("RESULT_ARTIFACT_IDENTITY_CONFLICT")
            fd = os.open(final.parent, os.O_RDONLY)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)
            with self._connect() as c, c.transaction(), c.cursor() as cursor:
                parents = [self._manifest(cursor, workspace_id, b["artifact_id"]) for b in bindings]
                if any(
                    p["content_hash"] != b["content_hash"]
                    for p, b in zip(parents, bindings, strict=True)
                ):
                    raise AnalyticsFailure("ARTIFACT_BINDING_MISMATCH")
                for parent in parents:
                    self._bytes(parent)
                cursor.execute(
                    """INSERT INTO artifact_manifests
                    (id,workspace_id,producer_batch_id,artifact_type,entity,relative_uri,content_hash,row_count,byte_size,schema_json,pii_class,state)
                    VALUES (%s,%s,NULL,'sales_report_json',%s,%s,%s,%s,%s,%s,'internal','committed') ON CONFLICT(id) DO NOTHING""",
                    (
                        artifact_id,
                        workspace_id,
                        "MetricWorkspace" if version == "metric-workspace/v2" else "CardComparison",
                        relative,
                        content_hash,
                        len(payload["buckets"]),
                        len(raw),
                        Jsonb({"version": version}),
                    ),
                )
                manifest = self._manifest(cursor, workspace_id, artifact_id)
                if manifest["content_hash"] != content_hash or manifest["relative_uri"] != relative:
                    raise AnalyticsFailure("RESULT_ARTIFACT_IDENTITY_CONFLICT")
                for parent in parents:
                    PostgresArtifactRepository.add_dependency(
                        cursor, parent_id=parent["artifact_id"], child_id=artifact_id
                    )
            return {"artifact_id": artifact_id, "content_hash": content_hash}
        except OSError as exc:
            raise AnalyticsFailure("RESULT_STORAGE_UNAVAILABLE") from exc
        finally:
            temporary.unlink(missing_ok=True)

    def verify_workspace(self, *, workspace_id: Any, payload: dict[str, Any]) -> None:
        reference = payload["manifest"]
        with self._connect() as c, c.cursor() as cursor:
            manifest = self._manifest(cursor, workspace_id, reference["artifact_id"])
            if manifest["content_hash"] != reference["content_hash"] or (
                "result_id" in payload and payload["result_id"] != reference["artifact_id"]
            ):
                raise AnalyticsFailure("RESULT_ARTIFACT_IDENTITY_CONFLICT")
            if json.loads(self._bytes(manifest)) != {
                k: v for k, v in payload.items() if k != "manifest"
            }:
                raise AnalyticsFailure("RESULT_ARTIFACT_IDENTITY_CONFLICT")
