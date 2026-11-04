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
from packages.contracts.semantic import BusinessCalendarVersion, ZonedCalendarProfileV2
from packages.contracts.semantic.store_filters import semantic_expression
from packages.analytics_core.application.store_scopes import resolve_store_filters
from packages.analytics_core.domain.calendar_buckets import boundary, month as month
from packages.analytics_core.domain.decimal_numbers import number
from packages.analytics_core.application.temporal_resolution import resolve_temporal
from packages.contracts.analytics.temporal import ComparisonPeriod, ResolvedTemporalSpecV2
from packages.analytics_core.application.temporal_projection import project_temporal
from packages.analytics_core.domain.calendar_time import (
    calendar_zone,
    period_bounds,
    day_bounds,
    utc_source_dates,
)

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


def dates(start: date, end: date) -> list[date]:
    return [start + timedelta(days=i) for i in range((end - start).days + 1)]


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
    if request.scope is not None:
        effective = set(
            resolve_store_filters(
                request.scope.filters,
                allowed=frozenset(allowed),
                dataset_id=request.semantic_dataset_version_id,
                mandatory=[request.common.store_ids, request.local_store_ids],
            )
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
        "timezone": calendar.profile.timezone,
        "week_start": "monday",
        "alignment": request.alignment,
    }
    if isinstance(calendar.profile, ZonedCalendarProfileV2):
        zone = calendar_zone(calendar.profile)
        period_bounds(request.common.starts_on, request.common.ends_on, zone)
        if request.alignment != "none":
            for day in dates(request.common.starts_on, request.common.ends_on):
                try:
                    prior = day.replace(year=day.year - 1)
                except ValueError:
                    continue
                day_bounds(prior, zone)
    if request.time_comparison is not None:
        if request.alignment != "none":
            raise AnalyticsFailure("COMPARISON_CONTRACT_CONFLICT")
        context["time_comparison"] = resolve_temporal(
            request.time_comparison,
            ComparisonPeriod(starts_on=request.common.starts_on, ends_on=request.common.ends_on),
            grain=request.grain,
            calendar=calendar,
            basis=request.calendar_basis,
        ).model_dump(mode="json")
    if request.scope is not None:
        context["scope_hash"] = digest(
            {
                "schema_version": request.scope.schema_version,
                "dependency_hash": request.scope.dependency_hash,
                "filters": sorted(
                    [
                        {
                            **f.model_dump(mode="json"),
                            "expression": semantic_expression(f.expression),
                        }
                        for f in request.scope.filters
                    ],
                    key=lambda f: json.dumps(f, sort_keys=True),
                ),
                "effective_store_ids": sorted(effective),
            }
        )
    if request.receipt_filter is not None:
        fingerprint = source.get("receipt_filter_hash")
        if not isinstance(fingerprint, str) or len(fingerprint) != 64:
            raise AnalyticsFailure("FILTER_PROVIDER_UNAVAILABLE")
        context["scope_hash"] = digest(
            {"store_scope": context.get("scope_hash"), "receipt_filter_hash": fingerprint}
        )
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
    zone = calendar_zone(calendar.profile)
    if isinstance(calendar.profile, ZonedCalendarProfileV2):
        needed = set(dates(request.common.starts_on, request.common.ends_on))
        if request.time_comparison is not None:
            spec = ResolvedTemporalSpecV2.model_validate(context["time_comparison"])
            if spec.comparison_period is not None:
                needed.update(
                    dates(spec.comparison_period.starts_on, spec.comparison_period.ends_on)
                )
        elif request.alignment != "none":
            for day in tuple(needed):
                try:
                    needed.add(day.replace(year=day.year - 1))
                except ValueError:
                    pass
        source_days = calendar_days
        calendar_days = {}
        for day in needed:
            intersecting = utc_source_dates(day, zone)
            if all(d in source_days for d in intersecting):
                calendar_days[day] = all(source_days[d] for d in intersecting)
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
            by_day[occurred.astimezone(zone).date()].append({"amount": amount})

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
    selection = source.get("receipt_selection")
    selection_codes = list(selection["limitation_codes"]) if selection else []
    if selection and selection["unknown_count"]:
        selection_codes.append("RECEIPT_MEMBERSHIP_UNKNOWN")
    reasons += selection_codes
    if isinstance(calendar.profile, ZonedCalendarProfileV2):
        reasons.append("COVERAGE_INTERSECTING_UTC_SOURCE_DAYS")
        if request.receipt_filter is not None:
            reasons.append("REGISTERED_RECEIPT_DATE_FILTER_UTC")
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
        disclosures = codes + (["BASELINE_UNMAPPED_LEAP_DAY_EXCLUDED"] if excluded else []) + selection_codes
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
    temporal_v2 = None
    if request.time_comparison is not None:
        temporal_v2 = project_temporal(
            ResolvedTemporalSpecV2.model_validate(context["time_comparison"]),
            project=project,
            calendar=calendar,
            request_hash=request_hash,
            policy_hash=access.policy_hash,
            dataset_id=request.semantic_dataset_version_id,
            metric_refs=refs,
            filter_hash=digest(
                {
                    "store_ids": context["store_ids"],
                    "scope_hash": context.get("scope_hash"),
                    "receipt_filter_hash": source.get("receipt_filter_hash"),
                }
            ),
            complete_days=calendar_days,
            selection_limitations=tuple(selection_codes),
        )
        if temporal_v2 is not None:
            reasons += temporal_v2["limitation_codes"]
    return {
        **({"receipt_selection": selection} if selection is not None else {}),
        **({"temporal_v2": temporal_v2} if request.time_comparison is not None else {}),
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
            "data_as_of": (
                source.get("receipt_data_as_of") or as_of or datetime(1970, 1, 1, tzinfo=UTC)
            ).isoformat(),
        },
        "trust": {
            "status": "no_data"
            if totals["receipt_count"] is None
            else "comparison_unavailable"
            if (temporal and any(v["absolute_delta"] is None for v in temporal["changes"].values()))
            or (temporal_v2 and temporal_v2["comparability_status"] == "unavailable")
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
