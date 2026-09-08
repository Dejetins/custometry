"""Require license/source/relinking evidence from the complete verified v2 set."""
from __future__ import annotations

import hashlib
import stat
from pathlib import Path
from typing import Any

from . import delivery_bundle as bundle
from . import gate_licenses, gate_sbom


def verified_files(record: dict[str, Any], complete: Path) -> dict[str, Path]:
    """Resolve only signed descriptors, and recheck exact bytes before license use."""
    groups = [(complete / "main", record["files"])]
    groups.extend((complete / "companions" / f"{part['part']:02d}", part["files"]) for part in record["companions"])
    result: dict[str, Path] = {}
    for root, files in groups:
        for item in files:
            key = bundle.safe_path(item["path"])
            bundle.require(key not in result, "DELIVERY_LICENSE_CLOSURE_INVALID")
            target = root
            for component in Path(key).parts:
                target /= component
                bundle.require(not target.is_symlink(), "DELIVERY_LICENSE_CLOSURE_INVALID")
            bundle.require(target.is_file() and stat.S_ISREG(target.stat().st_mode)
                           and target.stat().st_size == item["size_bytes"], "DELIVERY_LICENSE_CLOSURE_INVALID")
            with target.open("rb") as stream:
                digest = hashlib.file_digest(stream, "sha256").hexdigest()
            bundle.require(digest == item["sha256"], "DELIVERY_LICENSE_CLOSURE_INVALID")
            result[key] = target
    return result


def verify(record: dict[str, Any], complete: Path) -> None:
    files = verified_files(record, complete)
    subjects = {platform["digest"] for image in record["images"].values() for platform in image["platforms"]}
    declarations = bundle.unique(record["license_closure"], "subject")
    bundle.require(len(subjects) == 6 and set(declarations) == subjects, "DELIVERY_LICENSE_CLOSURE_INVALID")
    policy = bundle.ROOT / "deploy/license-policy.json"
    for subject, declaration in declarations.items():
        bundle.require(declaration["sbom_path"] in files and declaration["reviews_path"] in files,
                       "DELIVERY_LICENSE_CLOSURE_INVALID")
        sbom = files[declaration["sbom_path"]]
        reviews = files[declaration["reviews_path"]]
        # An external source file cannot impersonate the main signed SBOM/review.
        bundle.require(sbom.is_relative_to(complete / "main") and reviews.is_relative_to(complete / "main"),
                       "DELIVERY_LICENSE_CLOSURE_INVALID")
        bundle.require(reviews.stat().st_size <= 1048576
                       and bundle.STRUCTURE.parse_json(reviews.read_bytes()).get("schema_version") == 2,
                       "DELIVERY_LICENSE_CLOSURE_INVALID")
        bundle.require(gate_sbom.check(complete, sbom, expected_subjects=[subject], require_subjects=True).ok,
                       "DELIVERY_LICENSE_CLOSURE_INVALID")
        bundle.require(gate_licenses.check(complete, sbom, policy, reviews=reviews,
                       expected_subjects=[subject], verified_evidence=files).ok, "DELIVERY_LICENSE_CLOSURE_INVALID")
