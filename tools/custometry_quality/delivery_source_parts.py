"""Prepare source parts and reconcile immutable Actions uploads before signing.

These commands do not approve licenses or upload artifacts. The producer must
complete its source/obligation gates before invoking the pinned upload action.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import stat
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, cast

from . import delivery_bundle as bundle
from . import delivery_companions as companions
from . import delivery_set as delivery


def records(value: Any) -> list[dict[str, Any]]:
    bundle.require(type(value) is list and all(type(row) is dict for row in value), "DELIVERY_SOURCE_PLAN_INVALID")
    return cast(list[dict[str, Any]], value)


def validate_plan(plan: dict[str, Any]) -> None:
    bundle.require(set(plan) == {"schema_version", "parts"} and type(plan["schema_version"]) is int
                   and plan["schema_version"] == 1, "DELIVERY_SOURCE_PLAN_INVALID")
    limits = companions.policy()["companions"]
    parts = records(plan["parts"])
    bundle.require(0 < len(parts) <= limits["count"])
    paths: list[str] = []
    total = 0
    for index, part in enumerate(parts, 1):
        bundle.require(set(part) == {"part", "files", "expanded_bytes"}
                       and type(part["part"]) is int and part["part"] == index)
        files = records(part["files"])
        bundle.require(0 < len(files) <= limits["entries"])
        expanded = 0
        for file in files:
            bundle.require(set(file) == {"path", "sha256", "size_bytes"})
            bundle.require(isinstance(file["path"], str) and isinstance(file["sha256"], str)
                           and re.fullmatch(r"[a-f0-9]{64}", file["sha256"]) is not None)
            bundle.require(type(file["size_bytes"]) is int and 0 < file["size_bytes"] <= limits["file_bytes"], "DELIVERY_LIMIT")
            paths.append(bundle.safe_path(file["path"]))
            expanded += file["size_bytes"]
        bundle.require(type(part["expanded_bytes"]) is int and part["expanded_bytes"] == expanded
                       and expanded <= limits["expanded_bytes"], "DELIVERY_LIMIT")
        # Reserve more than the maximum ZIP header/central-directory overhead
        # for the bounded path and entry count. Provider compression is stored.
        bundle.require(expanded + len(part["files"]) * 1024 + 1024 <= limits["archive_bytes"], "DELIVERY_LIMIT")
        total += expanded
    companions.validate_paths(paths)
    bundle.require(len(paths) <= limits["entries"] and total <= limits["total_expanded_bytes"], "DELIVERY_LIMIT")


def prepare(source: Path, output: Path) -> None:
    bundle.require(source.is_dir() and source.resolve() == source.absolute())
    bundle.require(output.parent.is_dir() and output.parent.resolve() == output.parent.absolute())
    bundle.require(not output.exists() and not output.is_symlink(), "DELIVERY_VERSION_CONFLICT")
    limits = companions.policy()["companions"]
    files: list[tuple[dict[str, Any], Path]] = []
    total = 0
    for path in sorted(source.rglob("*")):
        mode = path.lstat().st_mode
        bundle.require(not stat.S_ISLNK(mode))
        if stat.S_ISDIR(mode):
            continue
        bundle.require(stat.S_ISREG(mode))
        size = path.stat().st_size
        bundle.require(0 < size <= limits["file_bytes"], "DELIVERY_LIMIT")
        total += size
        bundle.require(len(files) < limits["entries"] and total <= limits["total_expanded_bytes"], "DELIVERY_LIMIT")
        files.append(({"path": bundle.safe_path(path.relative_to(source).as_posix()),
                       "sha256": companions.sha(path), "size_bytes": size}, path))
    companions.validate_paths([row["path"] for row, _ in files])
    parts: list[dict[str, Any]] = []
    for row, _ in files:
        if not parts or (parts[-1]["expanded_bytes"] + row["size_bytes"]
                         + (len(parts[-1]["files"]) + 1) * 1024 + 1024 > limits["archive_bytes"]):
            parts.append({"part": len(parts) + 1, "files": [], "expanded_bytes": 0})
        parts[-1]["files"].append(row)
        parts[-1]["expanded_bytes"] += row["size_bytes"]
    plan = {"schema_version": 1, "parts": parts}
    validate_plan(plan)
    with tempfile.TemporaryDirectory(prefix=".source-parts-", dir=output.parent) as temporary:
        tree = Path(temporary) / "parts"
        tree.mkdir(mode=0o700)
        by_name = {row["path"]: path for row, path in files}
        for part in parts:
            folder = tree / f"{part['part']:02d}"
            folder.mkdir(mode=0o700)
            for row in part["files"]:
                target = folder / row["path"]
                parent = folder
                for component in Path(row["path"]).parts[:-1]:
                    parent /= component
                    parent.mkdir(mode=0o700, exist_ok=True)
                digest = hashlib.sha256()
                count = 0
                with by_name[row["path"]].open("rb") as original, target.open("xb") as copy:
                    target.chmod(0o600)
                    while block := original.read(1048576):
                        count += len(block)
                        bundle.require(count <= row["size_bytes"], "DELIVERY_SOURCE_CHANGED")
                        digest.update(block)
                        copy.write(block)
                bundle.require(count == row["size_bytes"] and digest.hexdigest() == row["sha256"], "DELIVERY_SOURCE_CHANGED")
        plan_path = tree / "parts.json"
        plan_path.write_bytes(bundle.canonical(plan))
        plan_path.chmod(0o600)
        delivery.promote_new(tree, output)


def listed_parts(provider: delivery.GitHub, version: str, run_id: int) -> tuple[list[dict[str, Any]], bool]:
    prefix = f"custometry-delivery-sources-{version}-{run_id}-"
    matches: list[dict[str, Any]] = []
    main_names: list[str] = []
    for page in range(1, 101):
        observed = provider.metadata(f"actions/artifacts?per_page=100&page={page}")
        values = records(observed.get("artifacts"))
        bundle.require(len(values) <= 100, "DELIVERY_PROVIDER_INVALID")
        matches.extend(value for value in values if str(value.get("name", "")).startswith(prefix))
        main_names.extend(str(value["name"]) for value in values if
                          str(value.get("name", "")).startswith(f"custometry-delivery-{version}-{run_id}-")
                          or value.get("name") == f"custometry-delivery-{version}")
        bundle.require(len(matches) <= 16, "DELIVERY_VERSION_CONFLICT")
        bundle.require(len(main_names) <= 1, "DELIVERY_VERSION_CONFLICT")
        if len(values) < 100:
            return matches, bool(main_names)
    raise bundle.BundleError("DELIVERY_PROVIDER_LIMIT")


def reconcile(plan: dict[str, Any], version: str, run_id: int, attempt: int,
              commit: str, output: Path, *, require_complete: bool = False) -> None:
    validate_plan(plan)
    bundle.require(run_id > 0 and attempt > 0 and version == f"0.1.0-ms001.{run_id}"
                   and re.fullmatch(r"[a-f0-9]{40}", commit) is not None)
    # A producer context is sufficient here; no unsigned root is accepted by
    # the consumer. The complete descriptor is later covered by the signature.
    context = {"producer": {"run_id": run_id, "run_attempt": attempt}, "source": {"commit": commit}}
    provider = delivery.GitHub()
    delivery.verify_run(context, provider.metadata(f"actions/runs/{run_id}"))
    values, main_exists = listed_parts(provider, version, run_id)
    selected: dict[int, dict[str, Any]] = {}
    prefix = f"custometry-delivery-sources-{version}-{run_id}-"
    for value in values:
        match = re.fullmatch(re.escape(prefix) + r"([1-9][0-9]*)-([0-9]{2})", value["name"])
        bundle.require(match is not None and int(match[1]) <= attempt, "DELIVERY_VERSION_CONFLICT")
        assert match is not None
        part_index = int(match[2])
        bundle.require(0 < part_index <= len(plan["parts"]) and part_index not in selected, "DELIVERY_VERSION_CONFLICT")
        selected[part_index] = value
    decisions: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="source-reconcile-") as temporary:
        root = Path(temporary).resolve()
        for plan_part in plan["parts"]:
            index = plan_part["part"]
            name = f"{prefix}{attempt}-{index:02d}"
            value = selected.get(index)
            if value is None:
                bundle.require(not require_complete and not main_exists, "DELIVERY_SOURCE_PART_MISSING")
                decisions.append({"part": index, "exists": False, "artifact_name": name})
                continue
            bundle.require(type(value.get("id")) is int and value["id"] > 0
                           and isinstance(value.get("digest"), str)
                           and re.fullmatch(r"sha256:[a-f0-9]{64}", value["digest"]) is not None
                           and type(value.get("size_in_bytes")) is int
                           and 0 < value["size_in_bytes"] <= companions.policy()["companions"]["archive_bytes"],
                           "DELIVERY_PROVIDER_INVALID")
            part: dict[str, Any] = {**plan_part, "artifact_id": value["id"], "artifact_name": value["name"],
                    "provider_sha256": value["digest"][7:], "archive_bytes": value["size_in_bytes"],
                    "expires_at": value.get("expires_at")}
            # Re-read each selected artifact's exact authenticated identity.
            metadata = provider.metadata(f"actions/artifacts/{part['artifact_id']}")
            companions.verify_provider(part, metadata, context, now=datetime.now(timezone.utc))
            archive = root / f"{index:02d}.zip"
            provider.download(part["artifact_id"], archive, part["archive_bytes"])
            companions.verify_zip(archive, part, root / f"{index:02d}")
            archive.unlink()
            shutil.rmtree(root / f"{index:02d}")
            decisions.append({"part": index, "exists": True, "artifact_name": value["name"], "descriptor": part})
    bundle.require(not output.exists() and not output.is_symlink(), "DELIVERY_VERSION_CONFLICT")
    with output.open("xb") as stream:
        output.chmod(0o600)
        stream.write(bundle.canonical({"schema_version": 1, "parts": decisions}))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)
    prepare_parser = subcommands.add_parser("prepare")
    prepare_parser.add_argument("--sources", type=Path, required=True)
    prepare_parser.add_argument("--output", type=Path, required=True)
    reconcile_parser = subcommands.add_parser("reconcile")
    reconcile_parser.add_argument("--plan", type=Path, required=True)
    reconcile_parser.add_argument("--delivery-version", required=True)
    reconcile_parser.add_argument("--run-id", type=int, required=True)
    reconcile_parser.add_argument("--run-attempt", type=int, required=True)
    reconcile_parser.add_argument("--commit", required=True)
    reconcile_parser.add_argument("--output", type=Path, required=True)
    reconcile_parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            prepare(args.sources, args.output)
        else:
            with args.plan.open("rb") as stream:
                plan = bundle.STRUCTURE.parse_json(stream.read(1048577))
            reconcile(plan, args.delivery_version, args.run_id, args.run_attempt, args.commit,
                      args.output, require_complete=args.require_complete)
    except (ValueError, OSError, KeyError, TypeError):
        print("DELIVERY_SOURCE_PARTS_REJECTED")
        return 1
    print("DELIVERY_SOURCE_PARTS_CHECKED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
