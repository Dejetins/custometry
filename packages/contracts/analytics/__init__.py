"""Public ports and stable failure envelope for governed analytics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
from uuid import UUID


ANALYTICS_API_VERSION = "1.0.0"


class AnalyticsFailure(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code

    def __str__(self) -> str:
        return self.code


@dataclass(frozen=True, slots=True)
class SemanticArtifactBinding:
    entity: str
    artifact_id: UUID
    relative_uri: str
    content_hash: str
    source_system_id: UUID


@dataclass(frozen=True, slots=True)
class PublishedSemanticProjection:
    semantic_dataset_version_id: UUID
    workspace_id: UUID
    quality_decision: str
    capability_matrix: dict[str, str]
    bindings: tuple[SemanticArtifactBinding, ...]


class SemanticProjectionPort(Protocol):
    def get_published_projection(
        self, *, workspace_id: UUID, semantic_dataset_version_id: UUID
    ) -> PublishedSemanticProjection: ...


class TabularArtifactPort(Protocol):
    def read_rows(self, binding: SemanticArtifactBinding) -> tuple[dict[str, object], ...]: ...


__all__ = [
    "ANALYTICS_API_VERSION",
    "AnalyticsFailure",
    "PublishedSemanticProjection",
    "SemanticArtifactBinding",
    "SemanticProjectionPort",
    "TabularArtifactPort",
]
