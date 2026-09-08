"""Verify narrowly scoped, evidence-backed component reviews without a global waiver.

This checks bindings and evidence completeness, not legal approval. The executor
must substantively review primary license texts, distribution and linking facts.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any, cast


def _digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def declaration_digest(component: dict[str, Any]) -> str:
    values = {key: component[key] for key in ("licenses", "licenseConcluded") if key in component}
    return hashlib.sha256(json.dumps(values, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def validate_reviews(
    path: Path, sbom: Path, policy: Path, subjects: set[str], components: list[dict[str, Any]]
) -> dict[tuple[str, str, str], set[str]]:
    """Missing/mismatched/duplicate/unfulfilled evidence always fails closed."""
    if path.is_symlink() or path.stat().st_size > 1048576:
        raise ValueError("invalid component review file")
    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in values:
            if key in result:
                raise ValueError("duplicate review key")
            result[key] = value
        return result

    record = json.loads(path.read_text(), object_pairs_hook=pairs)
    if set(record) != {"schema_version", "policy_sha256", "sbom_sha256", "subjects", "components"}:
        raise ValueError("invalid component review fields")
    if (record["schema_version"] != 1 or not subjects
            or set(record["subjects"]) != subjects
            or record["policy_sha256"] != _digest(policy)
            or record["sbom_sha256"] != _digest(sbom)):
        raise ValueError("component review context mismatch")
    by_key = {(str(c.get("name", "")), str(c.get("version", "")), str(c.get("purl", ""))): c for c in components}
    result: dict[tuple[str, str, str], set[str]] = {}

    def file_evidence(item: dict[str, Any]) -> None:
        if set(item) != {"path", "sha256", "size_bytes"}:
            raise ValueError("invalid review evidence fields")
        name = PurePosixPath(item["path"])
        if name.is_absolute() or ".." in name.parts or not name.parts:
            raise ValueError("unsafe review evidence path")
        target = path.parent
        for part in name.parts:
            target /= part
            if target.is_symlink():
                raise ValueError("linked review evidence forbidden")
        if (not target.is_file() or target.stat().st_size != item["size_bytes"]
                or item["size_bytes"] <= 0 or _digest(target) != item["sha256"]):
            raise ValueError("review evidence missing or altered")

    for value in record["components"]:
        item = cast(dict[str, Any], value)
        if set(item) != {"name", "version", "purl", "declaration_sha256", "review", "obligations"}:
            raise ValueError("invalid reviewed component fields")
        key = (item["name"], item["version"], item["purl"])
        if not all(key) or key in result or key not in by_key:
            raise ValueError("reviewed component identity missing or ambiguous")
        if sum((c.get("name"), c.get("version"), c.get("purl")) == key for c in components) != 1:
            raise ValueError("ambiguous reviewed SBOM component")
        if item["declaration_sha256"] != declaration_digest(by_key[key]):
            raise ValueError("reviewed license declaration changed")
        file_evidence(item["review"])
        kinds: set[str] = set()
        for obligation in item["obligations"]:
            if (set(obligation) != {"kind", "status", "evidence"}
                    or obligation["kind"] not in {"notice", "corresponding-source", "relinking", "modification-record"}
                    or obligation["status"] != "verified" or not obligation["evidence"]):
                raise ValueError("unfulfilled or unknown review obligation")
            kinds.add(obligation["kind"])
            for evidence in obligation["evidence"]:
                file_evidence(evidence)
        if "notice" not in kinds:
            raise ValueError("review notice evidence missing")
        result[key] = kinds
    return result
