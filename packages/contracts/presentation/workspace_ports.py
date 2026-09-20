"""Narrow Presentation integration ports for configured reports."""

from typing import Any, Protocol
from uuid import UUID
from packages.contracts.analytics.workspace import (
    WorkspaceAccess,
    WorkspaceCardRequest,
    WorkspaceApplyResult,
    WorkspaceRunRequest,
    WorkspaceResultV2,
    CardResultBinding,
    CardComparisonV1,
)


class WorkspaceResults(Protocol):
    def authorize_base(
        self, workspace: UUID, actor: UUID, owner: UUID, result: dict[str, Any]
    ) -> None: ...
    def resolve(
        self, workspace: UUID, actor: UUID, dataset: UUID, run: bool = False
    ) -> WorkspaceAccess: ...
    def apply(
        self, workspace: UUID, actor: UUID, cards: list[WorkspaceCardRequest]
    ) -> WorkspaceApplyResult: ...
    def verify(
        self, workspace: UUID, actor: UUID, query: WorkspaceRunRequest, result: UUID
    ) -> WorkspaceResultV2: ...
    def compare(
        self,
        workspace: UUID,
        actor: UUID,
        dataset: UUID,
        left: CardResultBinding,
        right: CardResultBinding | None,
    ) -> CardComparisonV1: ...
    def verify_comparison(
        self, workspace: UUID, actor: UUID, dataset: UUID, value: CardComparisonV1
    ) -> None: ...
    def legacy(
        self, workspace: UUID, actor: UUID, owner: UUID, result: dict[str, Any]
    ) -> WorkspaceAccess: ...
