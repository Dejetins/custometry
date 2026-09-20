"""Receipt-header workspace math; no storage, HTTP, or current-default lookup."""

from __future__ import annotations

from collections import defaultdict
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal, InvalidOperation, localcontext
import hashlib
import json
from typing import Any
from uuid import UUID, uuid5

from packages.contracts.analytics import AnalyticsFailure
from packages.contracts.analytics.workspace import WorkspaceAccess, WorkspaceRunRequest
from packages.contracts.semantic import BusinessCalendarVersion

VERSION = "metric-workspace/v2"
CALCULATION = "receipt-fiscal/v2"
NAMESPACE = UUID("f313b67c-a176-4f0b-a217-2dcd411e7b65")
METRICS = ("net_revenue", "receipt_count", "average_receipt")


def digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
        ).encode()
    ).hexdigest()


def number(value: Decimal | None) -> str | None:
    if value is None:
        return None
    if not value.is_finite():
        raise AnalyticsFailure("NON_FINITE_VALUE")
    if value == 0:
        return "0"
    return (
        format(value, "f").rstrip("0").rstrip(".")
        if "." in format(value, "f")
        else format(value, "f")
    )


def dates(start: date, end: date) -> list[date]:
    return [start + timedelta(days=i) for i in range((end - start).days + 1)]


def month(start: date, offset: int) -> date:
    n = start.year * 12 + start.month - 1 + offset
    return date(n // 12, n % 12 + 1, 1)


def boundary(
    day: date, grain: str, calendar: BusinessCalendarVersion, basis: str
) -> dict[str, Any]:
    start_month = calendar.profile.fiscal_year_start_month if basis == "fiscal" else 1
    origin = date(day.year - (day.month < start_month), start_month, 1)
    offset = (day.year - origin.year) * 12 + day.month - origin.month
    quarter, half = offset // 3 + 1, offset // 6 + 1
    year = (
        origin.year
        if calendar.profile.year_label == "start_year"
        else (month(origin, 12) - timedelta(days=1)).year
    )
    if grain == "day":
        start, end, label = day, day + timedelta(days=1), str(day)
    elif grain == "week":
        start = day - timedelta(days=day.weekday())
        end = start + timedelta(days=7)
        iso = start.isocalendar()
        label = f"{iso.year}-W{iso.week:02d}"
    elif grain == "month":
        start = day.replace(day=1)
        end, label = month(start, 1), day.strftime("%Y-%m")
    else:
        width = {"quarter": 3, "half_year": 6, "year": 12}[grain]
        start = month(origin, offset // width * width)
        end = month(start, width)
        prefix = "FY" if basis == "fiscal" else ""
        label = f"{prefix}{year}" + (
            f" Q{quarter}" if grain == "quarter" else f" H{half}" if grain == "half_year" else ""
        )
    return {
        "bucket_id": f"{grain}:{start}",
        "bucket_start": str(start),
        "bucket_end_exclusive": str(end),
        "natural_starts_on": str(start),
        "natural_ends_on": str(end - timedelta(days=1)),
        "label": label,
        "fiscal_year": year if basis == "fiscal" else None,
        "fiscal_quarter": quarter if basis == "fiscal" else None,
        "fiscal_half": half if basis == "fiscal" else None,
    }


def normalize(
    request: WorkspaceRunRequest,
    source: dict[str, Any],
    inputs: dict[str, Any],
    access: WorkspaceAccess,
    calendar: BusinessCalendarVersion,
) -> tuple[dict[str, Any], str]:
    if set(inputs) != {"Customer", "Product", "Receipt", "ReceiptItem", "Store", "Calendar"}:
        raise AnalyticsFailure("SIX_ENTITY_BINDING_REQUIRED")
    if (
        access.semantic_dataset_version_id != request.semantic_dataset_version_id
        or calendar.workspace_id != access.workspace_id
    ):
        raise AnalyticsFailure("FORBIDDEN")
    if (
        calendar.version_id != request.calendar_ref.version_id
        or calendar.content_hash != request.calendar_ref.content_hash
        or digest(calendar.profile.model_dump(mode="json")) != calendar.content_hash
    ):
        raise AnalyticsFailure("CALENDAR_BINDING_MISMATCH")
    known = {str(r["store_id"]) for r in inputs["Store"]}
    allowed = set(access.allowed_store_ids)
    if not allowed <= known:
        raise AnalyticsFailure("STORE_NOT_AVAILABLE")
    for selected in (request.common.store_ids, request.local_store_ids):
        if selected is not None:
            if not set(selected) <= known:
                raise AnalyticsFailure("STORE_NOT_AVAILABLE")
            if not set(selected) <= allowed:
                raise AnalyticsFailure("FORBIDDEN")
    effective = allowed.intersection(
        request.common.store_ids if request.common.store_ids is not None else allowed,
        request.local_store_ids if request.local_store_ids is not None else allowed,
    )
    registry = {m["metric_id"]: m for m in source["metrics"]}
    if set(registry) != set(METRICS):
        raise AnalyticsFailure("METRIC_BASIS_MISMATCH")
    for ref in request.metric_refs:
        actual = registry[ref.metric_id]
        if (
            str(ref.version_id) != actual["version_id"]
            or ref.content_hash != actual["content_hash"]
        ):
            raise AnalyticsFailure("METRIC_BASIS_MISMATCH")
    context = {
        "starts_on": str(request.common.starts_on),
        "ends_on": str(request.common.ends_on),
        "store_ids": sorted(effective),
        "grain": request.grain,
        "calendar_ref": request.calendar_ref.model_dump(mode="json"),
        "calendar_basis": request.calendar_basis,
        "timezone": "UTC",
        "week_start": "monday",
        "alignment": request.alignment,
    }
    identity = {
        "schema_version": VERSION,
        "calculation_version": CALCULATION,
        "workspace_id": str(access.workspace_id),
        "principal_id": str(access.principal_id),
        "policy_hash": access.policy_hash,
        "allowed_store_ids": access.allowed_store_ids,
        "dataset": str(request.semantic_dataset_version_id),
        "publication_hash": source["publication_hash"],
        "source_bindings": sorted(source["bindings"], key=lambda b: b["entity"]),
        "metric_components": sorted(source["metrics"], key=lambda m: m["metric_id"]),
        "context": context,
        "calendar_policy": calendar.profile.model_dump(mode="json"),
    }
    return context, digest(identity)


def components(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return dict.fromkeys(METRICS)
    with localcontext() as ctx:
        ctx.prec = 38
        revenue = sum((r["amount"] for r in rows), Decimal(0))
        count = Decimal(len(rows))
        return dict(
            zip(METRICS, (number(revenue), number(count), number(revenue / count)), strict=True)
        )


def delta(
    left: Any,
    right: Any,
    current: dict[str, Any],
    baseline: dict[str, Any],
    reasons: list[str] | None = None,
) -> dict[str, Any]:
    codes = list(reasons or [])
    if left is None:
        codes.append("CURRENT_UNAVAILABLE")
    if right is None:
        codes.append("BASELINE_UNAVAILABLE")
    if current["state"] != "complete" or baseline["state"] != "complete":
        codes.append("COVERAGE_INCOMPLETE")
    absolute = percent = None
    if not codes and left is not None and right is not None:
        with localcontext() as ctx:
            ctx.prec = 38
            absolute = Decimal(left) - Decimal(right)
            if Decimal(right) == 0:
                codes.append("ZERO_BASELINE")
            else:
                percent = absolute / abs(Decimal(right)) * 100
    return {
        "left_coverage": current,
        "right_coverage": baseline,
        "left": left,
        "right": right,
        "absolute_delta": number(absolute),
        "relative_delta_percent": number(percent),
        "reason_codes": sorted(set(codes)),
    }


def build_workspace(
    request: WorkspaceRunRequest,
    source: dict[str, Any],
    inputs: dict[str, Any],
    access: WorkspaceAccess,
    calendar: BusinessCalendarVersion,
) -> dict[str, Any]:
    context, request_hash = normalize(request, source, inputs, access, calendar)
    calendar_days: dict[date, bool] = {}
    for row in inputs["Calendar"]:
        day = date.fromisoformat(str(row["calendar_date"]))
        if day in calendar_days or type(row["is_period_complete"]) is not bool:
            raise AnalyticsFailure("CALENDAR_INVALID")
        calendar_days[day] = row["is_period_complete"]
    by_day: dict[date, list[dict[str, Any]]] = defaultdict(list)
    seen: set[tuple[str, str]] = set()
    as_of: datetime | None = None
    for row in inputs["Receipt"]:
        key = (str(row.get("source_system_id")), str(row.get("receipt_id")))
        if None in (row.get("source_system_id"), row.get("receipt_id")) or key in seen:
            raise AnalyticsFailure("RECEIPT_GRAIN_INVALID")
        seen.add(key)
        occurred = row["receipt_datetime"]
        if not isinstance(occurred, datetime) or occurred.tzinfo is None:
            raise AnalyticsFailure("RECEIPT_TIME_INVALID")
        occurred = occurred.astimezone(UTC)
        as_of = max(as_of or occurred, occurred)
        if row["status"] != "completed" or row["currency"] != "EUR":
            continue
        try:
            amount = Decimal(str(row["net_amount"]))
            if not amount.is_finite():
                raise InvalidOperation
        except (InvalidOperation, ValueError, KeyError) as exc:
            raise AnalyticsFailure("RECEIPT_AMOUNT_INVALID") from exc
        if str(row["store_id"]) in context["store_ids"]:
            by_day[occurred.date()].append({"amount": amount})

    def project(
        selected: list[date], expected: int | None = None
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        rows = [r for d in selected for r in by_day[d]]
        total = len(selected) if expected is None else expected
        covered = sum(d in calendar_days for d in selected)
        complete = sum(calendar_days.get(d, False) for d in selected)
        reasons = [] if context["store_ids"] else ["EMPTY_EFFECTIVE_SCOPE"]
        if not rows:
            reasons.append("NO_ELIGIBLE_RECEIPTS")
        if covered != total:
            reasons.append("CALENDAR_MISSING")
        if complete != covered:
            reasons.append("CALENDAR_INCOMPLETE")
        coverage = {
            "state": "complete" if complete == total else "partial" if covered else "unavailable",
            "expected_days": total,
            "calendar_days": covered,
            "declared_complete_days": complete,
            "observed_days": sum(bool(by_day[d]) for d in selected),
            "eligible_receipts": len(rows),
            "reason_codes": reasons,
        }
        return components(rows), coverage

    selected = dates(request.common.starts_on, request.common.ends_on)
    grouped: dict[str, list[date]] = defaultdict(list)
    natural: dict[str, dict[str, Any]] = {}
    for d in selected:
        b = boundary(d, request.grain, calendar, request.calendar_basis)
        grouped[b["bucket_id"]].append(d)
        natural.setdefault(b["bucket_id"], b)
    buckets: list[dict[str, Any]] = []
    for key, ds in grouped.items():
        b = natural[key]
        values, coverage = project(ds)
        end = ds[-1] + timedelta(days=1)
        clipped = str(ds[0]) != b["bucket_start"] or str(end) != b["bucket_end_exclusive"]
        buckets.append(
            {
                **b,
                "effective_starts_on": str(ds[0]),
                "effective_ends_on": str(ds[-1]),
                "effective_start": str(ds[0]),
                "effective_end_exclusive": str(end),
                "clipped": clipped,
                "is_partial_bucket": clipped,
                "calendar_ref": context["calendar_ref"],
                "calendar_basis": request.calendar_basis,
                "values": values,
                "coverage": coverage,
                "state": "no_data"
                if values["receipt_count"] is None
                else "ready"
                if coverage["state"] == "complete"
                else "incomplete",
            }
        )
    totals, coverage = project(selected)
    temporal: dict[str, Any] | None = None
    reasons = list(coverage["reason_codes"])
    if request.alignment != "none":
        mapping: dict[date, date | None] = {}
        for d in selected:
            try:
                mapping[d] = d.replace(year=d.year - 1)
            except ValueError:
                mapping[d] = None
        baseline_dates = [d for d in mapping.values() if d is not None]
        excluded = []
        if baseline_dates:
            excluded = [
                d
                for d in dates(min(baseline_dates), max(baseline_dates))
                if d.month == 2 and d.day == 29 and d not in baseline_dates
            ]
        temporal_buckets: list[dict[str, Any]] = []
        for b in buckets:
            ds = grouped[b["bucket_id"]]
            bs = [prior for d in ds if (prior := mapping[d]) is not None]
            values, cov = project(bs, len(ds))
            codes = ["LEAP_DAY_SAME_DATE_UNAVAILABLE"] if len(bs) != len(ds) else []
            temporal_buckets.append(
                {
                    "bucket_id": b["bucket_id"],
                    "baseline_dates": [str(d) for d in bs],
                    "values": values,
                    "coverage": cov,
                    "changes": {
                        m: delta(b["values"][m], values[m], b["coverage"], cov, codes)
                        for m in METRICS
                    },
                }
            )
        bt, bc = project(baseline_dates, len(selected))
        codes = ["LEAP_DAY_SAME_DATE_UNAVAILABLE"] if None in mapping.values() else []
        disclosures = codes + (["BASELINE_UNMAPPED_LEAP_DAY_EXCLUDED"] if excluded else [])
        temporal = {
            "alignment": request.alignment,
            "mapping": [
                {"current_date": str(d), "baseline_date": str(b) if b else None}
                for d, b in mapping.items()
            ],
            "baseline_dates": [str(d) for d in baseline_dates],
            "excluded_baseline_dates": [str(d) for d in excluded],
            "buckets": temporal_buckets,
            "totals": bt,
            "coverage": bc,
            "changes": {m: delta(totals[m], bt[m], coverage, bc, codes) for m in METRICS},
            "reason_codes": disclosures,
        }
        reasons += disclosures
        reasons += [
            code for change in temporal["changes"].values() for code in change["reason_codes"]
        ]
    refs = [
        {k: m[k] for k in ("metric_id", "version_id", "content_hash")}
        for m in sorted(source["metrics"], key=lambda item: item["metric_id"])
    ]
    return {
        "schema_version": VERSION,
        "result_id": str(uuid5(NAMESPACE, request_hash)),
        "request_hash": request_hash,
        "policy_hash": access.policy_hash,
        "semantic_dataset_version_id": str(request.semantic_dataset_version_id),
        "publication_hash": source["publication_hash"],
        "effective_context": context,
        "metric_refs": refs,
        "buckets": buckets,
        "totals": totals,
        "coverage": coverage,
        "comparison": None,
        "temporal": temporal,
        "daily": [
            {"date": str(d), "values": project([d])[0], "coverage": project([d])[1]}
            for d in selected
        ],
        "lineage": {
            "source_artifacts": [
                {"artifact_id": b["artifact_id"], "content_hash": b["content_hash"]}
                for b in sorted(source["bindings"], key=lambda item: item["entity"])
            ],
            "metric_components": refs,
            "source_calendar_version_id": next(
                b["artifact_id"] for b in source["bindings"] if b["entity"] == "Calendar"
            ),
            "data_as_of": (as_of or datetime(1970, 1, 1, tzinfo=UTC)).isoformat(),
        },
        "trust": {
            "status": "no_data"
            if totals["receipt_count"] is None
            else "comparison_unavailable"
            if temporal and any(v["absolute_delta"] is None for v in temporal["changes"].values())
            else "ready",
            "reason_codes": sorted(
                set(
                    reasons
                    + [
                        "COMPLETED_EUR_ONLY",
                        "NOT_REFUND_ADJUSTED",
                        "CURRENT_ONLY_DIMENSIONS",
                        "PRODUCT_BASKET_COVERAGE_DEGRADED",
                        "EMPTY_VALUES_UNAVAILABLE",
                    ]
                )
            ),
        },
    }
