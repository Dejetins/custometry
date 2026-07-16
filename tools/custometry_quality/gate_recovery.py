from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Sequence

from .core import (
    CheckResult,
    add_common_arguments,
    json_object,
    json_string,
    load_json,
    main_guard,
    render_result,
    require_file,
)


def _timestamp(value: Any) -> datetime:
    if not isinstance(value, str):
        raise ValueError("timestamp must be an ISO-8601 string")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include timezone")
    return parsed.astimezone(UTC)


def check(root: Path, evidence: Path, *, max_age_hours: float = 168.0) -> CheckResult:
    result = CheckResult("gate_recovery")
    path = root / evidence
    if not require_file(path, result, "recovery-evidence-missing"):
        return result
    try:
        data = load_json(path)
        if data.get("schema_version") != 1:
            raise ValueError("recovery evidence requires schema_version=1")
        started, finished = _timestamp(data.get("started_at")), _timestamp(data.get("finished_at"))
        if finished < started:
            raise ValueError("finished_at precedes started_at")
        json_string(data.get("environment"), "environment")
        if data.get("restore_target_disposable") is not True:
            raise ValueError("restore_target_disposable must be true")
    except (ValueError, TypeError) as exc:
        result.add("recovery-evidence-invalid", str(exc), path)
        return result
    required_truth = (
        "backup_created",
        "restore_succeeded",
        "data_hash_match",
        "application_restart_succeeded",
    )
    for key in required_truth:
        if data.get(key) is not True:
            result.add("recovery-proof-failed", f"{key} is not true", path)
    try:
        manifest = json_object(data.get("backup_manifest"), "backup_manifest")
        digest = json_string(manifest.get("sha256"), "backup_manifest.sha256")
    except ValueError:
        digest = ""
    if len(digest) != 64:
        result.add("backup-manifest-invalid", "backup_manifest.sha256 is required", path)
    age = (datetime.now(UTC) - finished).total_seconds() / 3600
    if age < -1:
        result.add("recovery-evidence-future", "finished_at is in the future", path)
    elif age > max_age_hours:
        result.add("recovery-evidence-stale", f"evidence age {age:.1f}h exceeds {max_age_hours:.1f}h", path)
    result.details.update(
        environment=json_string(data.get("environment"), "environment"), age_hours=round(age, 2)
    )
    return result


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate fresh backup/restore recovery evidence")
    add_common_arguments(parser)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--max-age-hours", type=float, default=168.0)
    args = parser.parse_args(argv)
    return render_result(
        check(args.root.resolve(), args.evidence, max_age_hours=args.max_age_hours), args.json
    )


if __name__ == "__main__":
    main_guard(cli)
