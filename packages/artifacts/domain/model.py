from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class ArtifactWriteRequest:
    artifact_id: UUID
    workspace_id: UUID
    batch_id: UUID
    entity: str
    artifact_type: str = "landing_parquet"
    pii_class: str = "internal"
    schema_version: int = 1


@dataclass(frozen=True, slots=True)
class ArtifactManifest:
    artifact_id: UUID
    workspace_id: UUID
    batch_id: UUID
    entity: str
    artifact_type: str
    relative_uri: str
    content_hash: str
    row_count: int
    byte_size: int
    columns: tuple[str, ...]
    pii_class: str
    schema_version: int

    def as_dict(self) -> dict[str, object]:
        return {
            "artifact_id": str(self.artifact_id),
            "workspace_id": str(self.workspace_id),
            "batch_id": str(self.batch_id),
            "entity": self.entity,
            "artifact_type": self.artifact_type,
            "relative_uri": self.relative_uri,
            "content_hash": self.content_hash,
            "row_count": self.row_count,
            "byte_size": self.byte_size,
            "columns": list(self.columns),
            "pii_class": self.pii_class,
            "schema_version": self.schema_version,
        }
