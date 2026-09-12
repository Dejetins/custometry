"""Receipt-grain MART-SALES-PERIOD and daily projection for AnalyticsService."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal, InvalidOperation
from typing import Any
from uuid import UUID, uuid5

from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.sales_report import SalesReportRequest

VERSION = "sales-report/v1"
CODE_VERSION = "receipt-daily/v1"
NAMESPACE = UUID("e98e9543-3919-508d-82df-c7fcfcab62ac")


def digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    ).hexdigest()


def policy_hash(workspace_id: UUID, principal_id: UUID, permissions: frozenset[str]) -> str:
    return digest(
        {
            "workspace": str(workspace_id),
            "principal": str(principal_id),
            "permissions": sorted(permissions),
        }
    )


def days(start: date, end: date) -> list[date]:
    return [start + timedelta(days=i) for i in range((end - start).days + 1)]


def aggregate(rows: list[dict[str, Any]]) -> dict[str, str | None]:
    if not rows:
        return {"net_revenue": None, "receipt_count": None, "average_receipt": None}
    net = sum((Decimal(str(r["net_amount"])) for r in rows), Decimal(0))
    count = Decimal(len({(r["source_system_id"], r["receipt_id"]) for r in rows}))
    return {
        "net_revenue": str(net),
        "receipt_count": str(count),
        "average_receipt": str(net / count),
    }


def build_report(
    request: SalesReportRequest,
    source: dict[str, Any],
    inputs: dict[str, tuple[dict[str, Any], ...]],
    policy: str,
) -> dict[str, Any]:
    request.validate()
    expected = {"Receipt", "ReceiptItem", "Customer", "Product", "Calendar", "Store"}
    if set(inputs) != expected:
        raise AnalyticsFailure("SIX_ENTITY_BINDING_REQUIRED")
    stores = {str(row["store_id"]) for row in inputs["Store"]}
    if request.store_id is not None and request.store_id not in stores:
        raise AnalyticsFailure("STORE_NOT_AVAILABLE")
    calendar: dict[date, bool] = {}
    for row in inputs["Calendar"]:
        day = date.fromisoformat(str(row["calendar_date"]))
        if day in calendar or not isinstance(row["is_period_complete"], bool):
            raise AnalyticsFailure("CALENDAR_INVALID")
        calendar[day] = row["is_period_complete"]
    all_rows: list[dict[str, Any]] = []
    keys: set[tuple[str, str]] = set()
    for row in inputs["Receipt"]:
        key = (str(row.get("source_system_id")), str(row.get("receipt_id")))
        if None in (row.get("source_system_id"), row.get("receipt_id")) or key in keys:
            raise AnalyticsFailure("RECEIPT_GRAIN_INVALID")
        keys.add(key)
        occurred = row["receipt_datetime"]
        if not isinstance(occurred, datetime) or occurred.tzinfo is None:
            raise AnalyticsFailure("RECEIPT_TIME_INVALID")
        day = occurred.astimezone(UTC).date()
        if day not in calendar:
            raise AnalyticsFailure("CALENDAR_BINDING_INCOMPLETE")
        if row["currency"] != "EUR" or row["status"] != "completed":
            continue
        try:
            amount = Decimal(str(row["net_amount"]))
            if not amount.is_finite():
                raise InvalidOperation
        except (InvalidOperation, ValueError, KeyError) as exc:
            raise AnalyticsFailure("RECEIPT_AMOUNT_INVALID") from exc
        if request.store_id is None or str(row["store_id"]) == request.store_id:
            all_rows.append({**row, "day": day})

    def period(start: date, end: date) -> dict[str, Any]:
        selected_days = days(start, end)
        rows = [r for r in all_rows if start <= r["day"] <= end]
        covered = sum(d in calendar for d in selected_days)
        complete = sum(calendar.get(d, False) for d in selected_days)
        # Calendar completeness is the imported declaration, not inferred from sales.
        coverage = {
            "period_days": len(selected_days),
            "calendar_days": covered,
            "declared_complete_days": complete,
            "observed_receipt_days": len({r["day"] for r in rows}),
            "status": "complete"
            if complete == len(selected_days)
            else "partial"
            if covered
            else "missing",
        }
        daily: list[dict[str, Any]] = []
        for day in selected_days:
            day_rows = [r for r in rows if r["day"] == day]
            state = (
                "missing_calendar"
                if day not in calendar
                else "incomplete"
                if not calendar[day]
                else "observed"
                if day_rows
                else "no_eligible_receipts"
            )
            daily.append({"date": str(day), **aggregate(day_rows), "state": state})
        return {
            "period": {"starts_on": str(start), "ends_on": str(end)},
            "totals": aggregate(rows),
            "coverage": coverage,
            "daily": daily,
        }

    current = period(request.starts_on, request.ends_on)
    previous: dict[str, Any] | None = None
    reason = "COMPARISON_DISABLED"
    if request.comparison != "none":
        try:
            start = request.starts_on.replace(year=request.starts_on.year - 1)
            end = request.ends_on.replace(year=request.ends_on.year - 1)
        except ValueError:
            reason = "LEAP_DAY_SAME_DATE_UNAVAILABLE"
        else:
            previous = period(start, end)
            reason = (
                "COMPARISON_COVERAGE_INCOMPLETE"
                if any(p["coverage"]["status"] != "complete" for p in (current, previous))
                else ""
            )
    comparable = previous is not None and not reason
    if previous is not None and not comparable:
        previous["totals"] = {k: None for k in current["totals"]}
        previous["daily"] = [
            {**r, **previous["totals"], "state": "comparison_unavailable"}
            for r in previous["daily"]
        ]
    normalized = {
        "dataset": str(request.semantic_dataset_version_id),
        "publication_hash": source["publication_hash"],
        "period": current["period"],
        "store_id": request.store_id,
        "comparison": request.comparison,
        "policy_hash": policy,
        "metrics": source["metrics"],
        "source_hashes": source["summary"]["artifact_hashes"],
        "code_version": CODE_VERSION,
        "schema_version": VERSION,
        "timezone": "UTC",
    }
    request_hash = digest(normalized)
    limitations = [
        "COMPLETED_EUR_ONLY",
        "NOT_REFUND_ADJUSTED",
        "CURRENT_ONLY_DIMENSIONS",
        "PRODUCT_BASKET_COVERAGE_DEGRADED",
        "EMPTY_VALUES_UNAVAILABLE",
    ]
    if reason:
        limitations.append(reason)
    if current["coverage"]["status"] != "complete":
        limitations.append("CURRENT_COVERAGE_INCOMPLETE")
    changes: dict[str, Any] = {}
    for key, value in current["totals"].items():
        prior = None if previous is None else previous["totals"][key]
        delta = None if value is None or prior is None else Decimal(value) - Decimal(str(prior))
        changes[key] = {
            "absolute": None if delta is None else str(delta),
            "percent": None
            if delta is None or Decimal(str(prior)) == 0
            else str(delta / abs(Decimal(str(prior))) * 100),
            "reason": "UNAVAILABLE_OR_ZERO_DENOMINATOR"
            if delta is None or Decimal(str(prior)) == 0
            else None,
        }
    return {
        "schema_version": VERSION,
        "result_id": str(uuid5(NAMESPACE, request_hash)),
        "semantic_dataset_version_id": str(request.semantic_dataset_version_id),
        "request_hash": request_hash,
        "policy_hash": policy,
        "parameters": {
            "period": current["period"],
            "store_id": request.store_id,
            "comparison": request.comparison,
            "timezone": "UTC",
            "eligibility": source["metrics"][0]["eligibility"],
        },
        "metrics": source["metrics"],
        "totals": current["totals"],
        "daily": current["daily"],
        "coverage": current["coverage"],
        "comparison": previous,
        "comparability_status": "comparable" if comparable else "not_comparable",
        "changes": changes,
        "mart": {
            "id": "MART-SALES-PERIOD",
            "version": CODE_VERSION,
            "source_grain": ["source_system_id", "receipt_id"],
            "output_grain": ["date"],
            "row_count": len(current["daily"]),
            "pii_class": "internal",
            "chart_data": "daily",
            "table_data": "daily",
        },
        "lineage": {
            "bindings": source["bindings"],
            "source_hashes": source["summary"]["artifact_hashes"],
            "publication_hash": source["publication_hash"],
            "calendar_version_id": next(
                b["artifact_id"] for b in source["bindings"] if b["entity"] == "Calendar"
            ),
            "code_version": CODE_VERSION,
            "fact_scope": "receipt_header",
            "relationship_policy": source["summary"]["relationship_policy"],
        },
        "trust": {
            "quality_report_id": source["quality_report_id"],
            "quality_accounting": source["summary"]["quality_accounting"],
            "capabilities": source["capabilities"],
            "limitations": limitations,
            "raw_artifacts": source["summary"]["raw_artifacts"],
            "quarantine_artifact": source["summary"]["quarantine_artifact"],
        },
    }
