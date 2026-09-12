"""Versioned bounded report projection; all business values originate on the server."""

from datetime import date
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from packages.contracts.analytics.sales_report import SalesReportRequest


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SalesRunRequest(Strict):
    semantic_dataset_version_id: UUID
    starts_on: date = date(2025, 1, 1)
    ends_on: date = date(2025, 11, 30)
    store_id: str | None = Field(default=None, min_length=1, max_length=128)
    comparison: Literal["none", "previous_year_same_dates"] = "none"

    def domain(self) -> SalesReportRequest:
        return SalesReportRequest(**self.model_dump())


class Totals(Strict):
    net_revenue: str | None
    receipt_count: str | None
    average_receipt: str | None


class Daily(Totals):
    date: date
    state: Literal[
        "missing_calendar",
        "incomplete",
        "observed",
        "no_eligible_receipts",
        "comparison_unavailable",
    ]


class Coverage(Strict):
    period_days: int
    calendar_days: int
    declared_complete_days: int
    observed_receipt_days: int
    status: Literal["complete", "partial", "missing"]


class Comparison(Strict):
    period: dict[str, str]
    totals: Totals
    coverage: Coverage
    daily: list[Daily]


class SalesResponse(Strict):
    schema_version: Literal["sales-report/v1"]
    result_id: UUID
    semantic_dataset_version_id: UUID
    request_hash: str
    policy_hash: str
    parameters: dict[str, object]
    metrics: list[dict[str, object]]
    totals: Totals
    daily: list[Daily]
    coverage: Coverage
    comparison: Comparison | None
    comparability_status: Literal["comparable", "not_comparable"]
    changes: dict[str, object]
    mart: dict[str, object]
    lineage: dict[str, object]
    trust: dict[str, object]
    manifest: dict[str, object]
