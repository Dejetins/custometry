from __future__ import annotations

import hashlib
import os
from pathlib import Path
from uuid import uuid4

import pyarrow as pa
import pyarrow.parquet as pq

from packages.artifacts.domain.model import ArtifactManifest, ArtifactWriteRequest
from packages.contracts.data_pipeline import DataPipelineFailure


class LocalArtifactStore:
    """Atomic, content-verified local Parquet storage with generated paths only."""

    def __init__(self, root: Path) -> None:
        if not root.is_absolute():
            raise DataPipelineFailure("ARTIFACT_ROOT_NOT_ABSOLUTE")
        self.root = root.resolve()
        self._staging = self.root / ".staging"
        self._objects = self.root / "objects"
        self._staging.mkdir(parents=True, exist_ok=True)
        self._objects.mkdir(parents=True, exist_ok=True)

    def _safe(self, candidate: Path) -> Path:
        resolved_parent = candidate.parent.resolve()
        if resolved_parent not in {self._staging.resolve(), self._objects.resolve()}:
            raise DataPipelineFailure("ARTIFACT_PATH_ESCAPE")
        if candidate.exists() and candidate.is_symlink():
            raise DataPipelineFailure("ARTIFACT_SYMLINK_FORBIDDEN")
        return candidate

    @staticmethod
    def _hash(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def write_parquet(
        self, request: ArtifactWriteRequest, rows: tuple[dict[str, object], ...]
    ) -> ArtifactManifest:
        if not rows:
            raise DataPipelineFailure("EMPTY_LANDING_ARTIFACT")
        staging = self._safe(self._staging / f"{uuid4()}.parquet.tmp")
        final = self._safe(self._objects / f"{request.artifact_id}.parquet")
        try:
            table = pa.Table.from_pylist(list(rows))
            pq.write_table(
                table,
                staging,
                compression="zstd",
                version="2.6",
                write_statistics=True,
            )
            with staging.open("rb") as handle:
                os.fsync(handle.fileno())
            content_hash = self._hash(staging)
            if final.exists():
                if self._hash(final) != content_hash:
                    raise DataPipelineFailure("ARTIFACT_IDENTITY_CONFLICT")
                staging.unlink()
            else:
                os.replace(staging, final)
                directory_fd = os.open(self._objects, os.O_RDONLY)
                try:
                    os.fsync(directory_fd)
                finally:
                    os.close(directory_fd)
            return ArtifactManifest(
                artifact_id=request.artifact_id,
                workspace_id=request.workspace_id,
                batch_id=request.batch_id,
                entity=request.entity,
                artifact_type=request.artifact_type,
                relative_uri=f"objects/{request.artifact_id}.parquet",
                content_hash=content_hash,
                row_count=table.num_rows,
                byte_size=final.stat().st_size,
                columns=tuple(table.column_names),
                pii_class=request.pii_class,
                schema_version=request.schema_version,
            )
        except Exception:
            staging.unlink(missing_ok=True)
            raise

    def resolve(self, relative_uri: str) -> Path:
        candidate = self.root / relative_uri
        resolved = candidate.resolve()
        try:
            resolved.relative_to(self.root)
        except ValueError as exc:
            raise DataPipelineFailure("ARTIFACT_PATH_ESCAPE") from exc
        if candidate.is_symlink():
            raise DataPipelineFailure("ARTIFACT_SYMLINK_FORBIDDEN")
        return resolved

    def cleanup_staging(self) -> int:
        removed = 0
        for candidate in self._staging.glob("*.parquet.tmp"):
            self._safe(candidate).unlink(missing_ok=True)
            removed += 1
        return removed
