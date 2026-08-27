from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from uuid import UUID, uuid4

import pyarrow.parquet as pq

from packages.contracts.analytics import AnalyticsFailure, SemanticArtifactBinding


class LocalAnalyticsArtifactStore:
    """Read governed inputs and atomically commit immutable result manifests."""

    def __init__(self, root: Path) -> None:
        if not root.is_absolute():
            raise AnalyticsFailure("ARTIFACT_ROOT_NOT_ABSOLUTE")
        self.root = root.resolve()

    def _resolve(self, relative_uri: str) -> Path:
        candidate = self.root / relative_uri
        resolved = candidate.resolve()
        try:
            resolved.relative_to(self.root)
        except ValueError as exc:
            raise AnalyticsFailure("ARTIFACT_PATH_ESCAPE") from exc
        if candidate.is_symlink():
            raise AnalyticsFailure("ARTIFACT_SYMLINK_FORBIDDEN")
        return resolved

    @staticmethod
    def _hash(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def read_rows(self, binding: SemanticArtifactBinding) -> tuple[dict[str, object], ...]:
        path = self._resolve(binding.relative_uri)
        if not path.is_file() or self._hash(path) != binding.content_hash:
            raise AnalyticsFailure("SOURCE_ARTIFACT_INTEGRITY_FAILED")
        return tuple(pq.read_table(path).to_pylist())

    def commit_json(self, *, result_id: UUID, payload: object) -> tuple[str, str, int]:
        results = self.root / "analytics-results"
        staging = self.root / ".analytics-staging"
        results.mkdir(parents=True, exist_ok=True)
        staging.mkdir(parents=True, exist_ok=True)
        raw = json.dumps(
            payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode()
        content_hash = hashlib.sha256(raw).hexdigest()
        final = self._resolve(f"analytics-results/{result_id}.json")
        temporary = staging / f"{uuid4()}.json.tmp"
        temporary.write_bytes(raw)
        with temporary.open("rb") as handle:
            os.fsync(handle.fileno())
        try:
            if final.exists():
                if self._hash(final) != content_hash:
                    raise AnalyticsFailure("RESULT_ARTIFACT_IDENTITY_CONFLICT")
                temporary.unlink()
            else:
                os.replace(temporary, final)
                directory_fd = os.open(results, os.O_RDONLY)
                try:
                    os.fsync(directory_fd)
                finally:
                    os.close(directory_fd)
        finally:
            temporary.unlink(missing_ok=True)
        return f"analytics-results/{result_id}.json", content_hash, len(raw)
