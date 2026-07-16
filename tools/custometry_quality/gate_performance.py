from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from .core import (
    CheckResult,
    add_common_arguments,
    json_integer,
    json_list,
    json_number,
    json_object,
    json_string,
    load_json,
    main_guard,
    render_result,
    require_file,
)


def _timestamp(value: Any) -> datetime:
    if not isinstance(value, str):
        raise ValueError("measured_at must be ISO-8601")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("measured_at must include timezone")
    return parsed.astimezone(UTC)


def check(root: Path, evidence: Path, *, max_age_hours: float = 168.0) -> CheckResult:
    result = CheckResult("gate_performance")
    path = root / evidence
    if not require_file(path, result, "performance-evidence-missing"):
        return result
    try:
        data = load_json(path)
        if data.get("schema_version") != 1:
            raise ValueError("performance evidence requires schema_version=1")
        measured_at = _timestamp(data.get("measured_at"))
        for key in ("environment", "workload", "command", "baseline_identity", "candidate_identity"):
            json_string(data.get(key), key)
        metrics = json_list(data.get("metrics"), "metrics")
        if not metrics:
            raise ValueError("metrics must be a non-empty list")
    except (ValueError, TypeError) as exc:
        result.add("performance-evidence-invalid", str(exc), path)
        return result
    for index, value in enumerate(metrics):
        try:
            metric = json_object(value, f"metrics[{index}]")
            name = json_string(metric.get("name"), f"metrics[{index}].name")
            direction = json_string(metric.get("direction"), f"metrics[{index}].direction")
            baseline = json_number(metric.get("baseline"), f"metrics[{index}].baseline")
            candidate = json_number(metric.get("candidate"), f"metrics[{index}].candidate")
            threshold = json_number(
                metric.get("max_regression_percent"), f"metrics[{index}].max_regression_percent"
            )
            samples = json_integer(metric.get("samples"), f"metrics[{index}].samples")
            if direction not in {"lower", "higher"}:
                raise ValueError("name/direction invalid")
            if baseline <= 0 or candidate < 0 or threshold < 0 or samples < 3:
                raise ValueError("baseline > 0, candidate >= 0, threshold >= 0, samples >= 3 required")
        except (KeyError, TypeError, ValueError) as exc:
            result.add("performance-metric-invalid", f"metrics[{index}]: {exc}", path)
            continue
        regression = (
            ((candidate - baseline) / baseline) * 100
            if direction == "lower"
            else ((baseline - candidate) / baseline) * 100
        )
        if regression > threshold:
            result.add(
                "performance-regression",
                f"{name}: regression {regression:.2f}% exceeds {threshold:.2f}%",
                path,
            )
    age = (datetime.now(UTC) - measured_at).total_seconds() / 3600
    if age < -1:
        result.add("performance-evidence-future", "measured_at is in the future", path)
    elif age > max_age_hours:
        result.add("performance-evidence-stale", f"evidence age {age:.1f}h exceeds {max_age_hours:.1f}h", path)
    result.details.update(
        metrics=len(metrics),
        age_hours=round(age, 2),
        workload=json_string(data.get("workload"), "workload"),
    )
    return result


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate comparable performance evidence")
    add_common_arguments(parser)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--max-age-hours", type=float, default=168.0)
    args = parser.parse_args(argv)
    return render_result(
        check(args.root.resolve(), args.evidence, max_age_hours=args.max_age_hours), args.json
    )


if __name__ == "__main__":
    main_guard(cli)
