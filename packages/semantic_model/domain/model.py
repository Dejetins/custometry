from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class SemanticEntityBinding:
    entity: str
    artifact_id: UUID
    primary_key: tuple[str, ...]
    field_roles: dict[str, str]


@dataclass(frozen=True, slots=True)
class SemanticDatasetPublication:
    semantic_dataset_version_id: UUID
    semantic_dataset_id: UUID
    workspace_id: UUID
    version: int
    status: str
    quality_report_id: UUID
    bindings: tuple[SemanticEntityBinding, ...]
    capability_matrix: dict[str, str]
    impact_summary: dict[str, object]
    request_hash: str
