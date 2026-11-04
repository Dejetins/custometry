"""Policy-aware v2 comparison over the provider's authorized metric projector."""

from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal, localcontext
import hashlib
import json
from typing import Any, Callable
from uuid import UUID, uuid5

from packages.contracts.analytics.temporal import ResolvedTemporalSpecV2
from packages.contracts.semantic import BusinessCalendarVersion
from packages.analytics_core.domain.calendar_buckets import boundary
from packages.analytics_core.domain.decimal_numbers import number

NAMESPACE = UUID("ea1ce196-4db5-4358-8af3-b58f52996478")
Project = Callable[[list[date]], tuple[dict[str, Any], dict[str, Any]]]
METRICS = ("net_revenue", "receipt_count", "average_receipt")


def _dates(start: date, end: date) -> list[date]:
    return [start + timedelta(days=i) for i in range((end - start).days + 1)]


def _delta(
    left: str | None,
    right: str | None,
    current: dict[str, Any],
    baseline: dict[str, Any],
    allow_partial: bool,
) -> dict[str, Any]:
    codes: list[str] = []
    if left is None:
        codes.append("CURRENT_UNAVAILABLE")
    if right is None:
        codes.append("BASELINE_UNAVAILABLE")
    incomplete = current["state"] != "complete" or baseline["state"] != "complete"
    if incomplete:
        codes.append("COVERAGE_INCOMPLETE")
    absolute = percent = None
    if left is not None and right is not None and (allow_partial or not incomplete):
        with localcontext() as context:
            context.prec = 38
            absolute = Decimal(left) - Decimal(right)
            if Decimal(right) == 0:
                codes.append("ZERO_BASELINE")
            else:
                percent = absolute / abs(Decimal(right)) * 100
    return dict(
        left_coverage=current,
        right_coverage=baseline,
        left=left,
        right=right,
        absolute_delta=number(absolute),
        relative_delta_percent=number(percent),
        reason_codes=codes,
    )


def project_temporal(
    spec: ResolvedTemporalSpecV2,
    *,
    project: Project,
    calendar: BusinessCalendarVersion,
    request_hash: str,
    policy_hash: str,
    dataset_id: UUID,
    metric_refs: list[dict[str, Any]],
    filter_hash: str,
    complete_days: dict[date, bool],
    selection_limitations: tuple[str, ...] = (),
) -> dict[str, Any] | None:
    if spec.settings.mode == "none" or (
        spec.comparison_period is None and spec.date_mapping is None
    ):
        return None
    left = _dates(spec.current_period.starts_on, spec.current_period.ends_on)
    right = (
        _dates(spec.comparison_period.starts_on, spec.comparison_period.ends_on)
        if spec.comparison_period
        else []
    )
    codes = [*spec.limitation_codes, *selection_limitations]
    mapped = (
        [p for p in spec.date_mapping if not p.excluded] if spec.date_mapping is not None else None
    )
    if mapped is not None:
        if spec.settings.incomplete_period_policy == "comparable_elapsed_days":
            count = 0
            for pair in mapped:
                if (
                    not complete_days.get(pair.current_date, False)
                    or pair.comparison_date is None
                    or not complete_days.get(pair.comparison_date, False)
                ):
                    break
                count += 1
            if count != len(mapped):
                codes.append("COMPARABLE_ELAPSED_DAYS_TRIMMED")
            mapped = mapped[:count]
        left = [p.current_date for p in mapped]
        right = sorted({p.comparison_date for p in mapped if p.comparison_date is not None})
    elif spec.settings.incomplete_period_policy == "comparable_elapsed_days":

        def prefix(days: list[date]) -> int:
            for i, day in enumerate(days):
                if not complete_days.get(day, False):
                    return i
            return len(days)

        count = min(prefix(left), prefix(right))
        if count != len(left) or count != len(right):
            codes.append("COMPARABLE_ELAPSED_DAYS_TRIMMED")
        left, right = left[:count], right[:count]
    allow_partial = spec.settings.incomplete_period_policy == "explicit_partial"

    def changes(ls: list[date], rs: list[date], missing: int = 0) -> dict[str, Any]:
        lv, lc = project(ls)
        rv, rc = project(rs)
        if missing:
            rc = {
                **rc,
                "expected_days": len(rs) + missing,
                "state": "partial" if rc["calendar_days"] else "unavailable",
                "reason_codes": [*rc["reason_codes"], "COMPARISON_MAPPING_INCOMPLETE"],
            }
        return {m: _delta(lv[m], rv[m], lc, rc, allow_partial) for m in METRICS}

    def groups(days: list[date]) -> list[tuple[str, list[date]]]:
        result: dict[str, list[date]] = defaultdict(list)
        for day in days:
            result[boundary(day, spec.grain, calendar, spec.calendar_basis)["bucket_id"]].append(
                day
            )
        return list(result.items())

    pairs: list[dict[str, Any]] = []
    if mapped is not None:
        by_bucket: dict[str, list[Any]] = defaultdict(list)
        for pair in mapped:
            group_day = pair.current_date
            if pair.reason == "LEAP_DAY_MERGED":
                group_day = group_day.replace(day=28)
            by_bucket[
                boundary(group_day, spec.grain, calendar, spec.calendar_basis)["bucket_id"]
            ].append(pair)
        for identifier, members in by_bucket.items():
            lds = [p.current_date for p in members]
            rds = sorted({p.comparison_date for p in members if p.comparison_date is not None})
            pairs.append(
                dict(
                    current_bucket_id=identifier,
                    comparison_bucket_id=None,
                    current_dates=[str(d) for d in lds],
                    comparison_dates=[str(d) for d in rds],
                    changes=changes(lds, rds, sum(p.comparison_date is None for p in members)),
                )
            )
        totals = changes(left, right, sum(p.comparison_date is None for p in mapped))
    else:
        left_groups, right_groups = groups(left), groups(right)
        if len(left_groups) != len(right_groups):
            codes.append("COMPARISON_BUCKET_COUNT_MISMATCH")
        for i in range(max(len(left_groups), len(right_groups))):
            lid, lds = left_groups[i] if i < len(left_groups) else (None, [])
            rid, rds = right_groups[i] if i < len(right_groups) else (None, [])
            pairs.append(
                dict(
                    current_bucket_id=lid,
                    comparison_bucket_id=rid,
                    current_dates=[str(d) for d in lds],
                    comparison_dates=[str(d) for d in rds],
                    changes=changes(lds, rds),
                )
            )
        totals = changes(left, right)
    codes.extend(c for change in totals.values() for c in change["reason_codes"])
    status = (
        "unavailable"
        if any(v["absolute_delta"] is None for v in totals.values())
        else "partial"
        if "COVERAGE_INCOMPLETE" in codes
        else "descriptive"
        if codes
        else "comparable"
    )
    result: dict[str, Any] = dict(
        schema_version="time-comparison-artifact/v2",
        artifact_id=str(uuid5(NAMESPACE, request_hash)),
        request_hash=request_hash,
        policy_hash=policy_hash,
        spec=spec.model_dump(mode="json"),
        semantic_dataset_version_id=str(dataset_id),
        metric_refs=metric_refs,
        normalized_filter_hash=filter_hash,
        evaluated_current_dates=[str(d) for d in left],
        evaluated_comparison_dates=[str(d) for d in right],
        buckets=pairs,
        changes=totals,
        comparability_status=status,
        limitation_codes=sorted(set(codes)),
    )
    result["content_hash"] = hashlib.sha256(
        json.dumps(
            result, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
        ).encode()
    ).hexdigest()
    return result
