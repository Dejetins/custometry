"""Bounded sales report request and owner integration ports."""

from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Any, Protocol
from uuid import UUID

from packages.contracts.analytics import AnalyticsFailure


@dataclass(frozen=True)
class SalesReportRequest:
    semantic_dataset_version_id: UUID
    starts_on: date = date(2025, 1, 1)
    ends_on: date = date(2025, 11, 30)
    store_id: str | None = None
    comparison: str = "none"

    def validate(self) -> None:
        if self.ends_on < self.starts_on or (self.ends_on - self.starts_on).days >= 366:
            raise AnalyticsFailure("INVALID_BOUNDED_PERIOD")
        if self.comparison not in {"none", "previous_year_same_dates"}:
            raise AnalyticsFailure("UNSUPPORTED_COMPARISON")
        if self.store_id is not None and (not self.store_id or len(self.store_id) > 128):
            raise AnalyticsFailure("INVALID_STORE")


class SalesSemanticPort(Protocol):
    def sales_projection(self, *, workspace_id: UUID, version_id: UUID) -> dict[str, Any]: ...


class SalesResultPort(Protocol):
    def find_sales(
        self, *, workspace_id: UUID, principal_id: UUID, request_hash: str
    ) -> dict[str, Any] | None: ...
    def get_sales(
        self, *, workspace_id: UUID, principal_id: UUID, result_id: UUID
    ) -> dict[str, Any]: ...
    def save_sales(
        self, payload: dict[str, Any], *, workspace_id: UUID, principal_id: UUID
    ) -> dict[str, Any]: ...


class SalesArtifactPort(Protocol):
    def read_sales_inputs(
        self, *, workspace_id: UUID, bindings: list[dict[str, Any]], supporting_artifacts: list[str]
    ) -> dict[str, tuple[dict[str, Any], ...]]: ...
    def commit_sales(self, *, workspace_id: UUID, payload: dict[str, Any]) -> dict[str, Any]: ...
    def verify_sales(self, *, workspace_id: UUID, payload: dict[str, Any]) -> None: ...
