"""Fail-closed supply preparation for the existing internal candidate producer.

No command publishes, signs, installs tools or changes credentials. Native jobs
supply real observations; assembly checks them before a separate authorized signer.
"""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import io
import json
import platform
import re
import stat
import subprocess
import tarfile
import zipfile
from datetime import datetime, timezone
from email.parser import BytesParser
from pathlib import Path
from typing import Any, cast

from . import delivery_bundle as bundle
from . import gate_licenses, gate_sbom

ROOT = bundle.ROOT
POLICY = json.loads((ROOT / "deploy/compose/delivery-verification-policy.json").read_bytes())
DIGEST = re.compile(r"sha256:[0-9a-f]{64}")
PLATFORMS = {"amd64", "arm64"}
DIST_INFO = "app/.venv/lib/python3.12/site-packages/custometry_api-0.1.0.dev0.dist-info/"
UV_CACHE = DIST_INFO + "uv_cache.json"
WHEEL_RECORD = DIST_INFO + "RECORD"


def require(value: bool, code: str = "DELIVERY_SUPPLY_INVALID") -> None:
    bundle.require(value, code)


def run(*args: str) -> bytes:
    return subprocess.run(args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout


def evidence_bytes(value: Any) -> bytes:
    """Evidence may contain Unicode, multiline notices and CVSS floats; manifests may not."""
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
    ).encode("ascii")


def load(path: Path) -> Any:
    require(path.is_file() and not path.is_symlink() and path.stat().st_size <= 67108864)

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            require(key not in result)
            result[key] = value
        return result

    value = json.loads(path.read_bytes(), object_pairs_hook=pairs)

    def depth(item: Any, level: int = 0) -> None:
        require(level <= 32, "DELIVERY_LIMIT")
        if isinstance(item, dict):
            for child in cast(dict[str, Any], item).values():
                depth(child, level + 1)
        elif isinstance(item, list):
            for child in cast(list[Any], item):
                depth(child, level + 1)

    depth(value)
    evidence_bytes(value)  # Reject NaN/Infinity without applying manifest-only text rules.
    return value


def save(path: Path, value: Any) -> None:
    raw = evidence_bytes(value)
    require(len(raw) <= 67108864, "DELIVERY_LIMIT")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(raw)


def sha(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None)
    return parsed


def vulnerability_result(
    report: dict[str, Any],
    database: dict[str, Any],
    subject: str,
    now: datetime,
    *,
    expected_config: str | None = None,
) -> dict[str, Any]:
    """Require native Trivy source identity, explicit scanner/version and fresh DB."""
    require(DIGEST.fullmatch(subject) is not None)
    require(database.get("Version") == POLICY["tools"][3]["version"].lstrip("v"))
    db = database.get("VulnerabilityDB", {})
    require(db.get("Version") == 2)
    for value in (db.get("UpdatedAt", ""), report.get("CreatedAt", "")):
        age = (now - timestamp(value)).total_seconds()
        require(0 <= age <= 24 * 3600, "DELIVERY_SCAN_STALE")
    require(timestamp(db.get("NextUpdate", "")) > now, "DELIVERY_SCAN_STALE")
    require(report.get("SchemaVersion") == 2)
    require(report.get("ArtifactType") == "container_image")
    metadata = report.get("Metadata", {})
    registry_refs = cast(list[str], metadata.get("RepoDigests") or [])
    registry_bound = any(ref.endswith("@" + subject) for ref in registry_refs)
    archive_bound = (
        expected_config is not None
        and DIGEST.fullmatch(expected_config) is not None
        and metadata.get("ImageID") == expected_config
    )
    require(registry_bound or archive_bound, "DELIVERY_SUBJECT_MISMATCH")
    raw_results = report.get("Results")
    require(isinstance(raw_results, list) and raw_results != [])
    results = cast(list[dict[str, Any]], raw_results)
    findings = [v for result in results for v in result.get("Vulnerabilities", [])]
    unknown = [
        v for v in findings if v.get("Severity") not in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
    ]
    critical = [v for v in findings if v.get("Severity") == "CRITICAL"]
    return {
        "subject": subject,
        "critical": len(critical),
        "unknown_severity": len(unknown),
        "findings": len(findings),
        "status": "pass" if not (critical or unknown) else "fail",
        "database": db,
        "scanner": database["Version"],
    }


def bind_sbom(
    document: dict[str, Any],
    source: dict[str, Any],
    subject: str,
    *,
    expected_config: str | None = None,
) -> dict[str, Any]:
    """Bind only a scanner-reported matching container child; never relabel a BOM."""
    require(document.get("bomFormat") == "CycloneDX")
    metadata = document.get("metadata", {})
    component = metadata.get("component", {})
    require(component.get("type") == "container")
    require(source.get("type") == "image")
    reported = source.get("metadata", {}).get("repoDigests", [])
    registry_bound = any(isinstance(ref, str) and ref.endswith("@" + subject) for ref in reported)
    archive_bound = (
        expected_config is not None
        and DIGEST.fullmatch(expected_config) is not None
        and source.get("metadata", {}).get("imageID") == expected_config
    )
    require(registry_bound or archive_bound, "DELIVERY_SUBJECT_MISMATCH")
    existing = metadata.setdefault("properties", [])
    require(not any(p.get("name") == gate_sbom.SUBJECT_PROPERTY for p in existing))
    existing.append({"name": gate_sbom.SUBJECT_PROPERTY, "value": subject})
    return document


def filesystem_inventory(archive: Path) -> list[dict[str, Any]]:
    """Compare content/modes/links of the complete exported final filesystem.

    Docker's container-specific resolver/hostname/hosts are explicitly separate;
    Only mtime and tar order are excluded; owners and directory modes are compared.
    No archive member is extracted or executed.
    """
    result: list[dict[str, Any]] = []
    names: set[str] = set()
    with tarfile.open(archive, "r|") as source:
        for item in source:
            name = item.name.removeprefix("./").rstrip("/")
            if not name:
                continue
            require(not name.startswith("/") and ".." not in name.split("/"))
            require(name not in names)
            names.add(name)
            if name in {"etc/hosts", "etc/hostname", "etc/resolv.conf", ".dockerenv"}:
                continue
            require(item.isfile() or item.issym() or item.islnk() or item.isdir())
            record: dict[str, Any] = {
                "path": name,
                "mode": item.mode,
                "uid": item.uid,
                "gid": item.gid,
                "type": item.type.decode("ascii"),
                "link": item.linkname,
            }
            if item.isfile():
                stream = source.extractfile(item)
                require(stream is not None)
                assert stream is not None
                hasher = hashlib.sha256()
                metadata_parts: list[bytes] = []
                while block := stream.read(1048576):
                    hasher.update(block)
                    if name in {UV_CACHE, WHEEL_RECORD}:
                        require(item.size <= 1048576, "DELIVERY_LIMIT")
                        metadata_parts.append(block)
                record.update(size_bytes=item.size, sha256=hasher.hexdigest())
                if name in {UV_CACHE, WHEEL_RECORD}:
                    record["build_metadata"] = b"".join(metadata_parts).decode("utf-8")
            result.append(record)
    require(bool(result))
    return sorted(result, key=lambda row: row["path"])


def normalize_build_metadata(rows: list[dict[str, Any]]) -> dict[str, Any]:
    result = {row["path"]: dict(row) for row in rows}
    require(len(result) == len(rows) and bool(rows))
    if UV_CACHE not in result or WHEEL_RECORD not in result:
        return result
    cache, record = result[UV_CACHE], result[WHEEL_RECORD]
    raw = cache["build_metadata"].encode("utf-8")
    require(bundle.digest(raw) == cache["sha256"] and len(raw) == cache["size_bytes"])
    metadata = json.loads(raw)
    require(set(metadata) == {"timestamp", "commit", "tags", "env", "directories"})
    require(set(metadata["timestamp"]) == {"secs_since_epoch", "nanos_since_epoch"})
    require(all(type(value) is int for value in metadata["timestamp"].values()))
    require(set(metadata["directories"]) == {"src"} and type(metadata["directories"]["src"]) is int)
    metadata["timestamp"] = {"secs_since_epoch": 0, "nanos_since_epoch": 0}
    metadata["directories"]["src"] = 0  # uv 0.9.26 directory creation-time/inode cache key.
    normalized = evidence_bytes(metadata)
    raw_record = record["build_metadata"].encode("utf-8")
    require(
        bundle.digest(raw_record) == record["sha256"] and len(raw_record) == record["size_bytes"]
    )
    entries = list(csv.reader(io.StringIO(record["build_metadata"])))
    matching = [entry for entry in entries if entry[0] == UV_CACHE.split("site-packages/", 1)[1]]
    require(len(matching) == 1)
    entry = matching[0]
    require(
        entry[1:]
        == [
            "sha256=" + base64.urlsafe_b64encode(hashlib.sha256(raw).digest()).decode().rstrip("="),
            str(len(raw)),
        ]
    )
    entry[1:] = ["normalized-build-metadata", str(len(normalized))]
    for item, data in ((cache, normalized), (record, evidence_bytes(entries))):
        item.pop("build_metadata")
        item.update(sha256=bundle.digest(data), size_bytes=len(data))
    return result


def compare(first: list[dict[str, Any]], second: list[dict[str, Any]]) -> dict[str, Any]:
    left, right = normalize_build_metadata(first), normalize_build_metadata(second)
    changes = [
        name for name in sorted(left.keys() | right.keys()) if left.get(name) != right.get(name)
    ]
    raw_left, raw_right = {r["path"]: r for r in first}, {r["path"]: r for r in second}
    raw_changes = [
        name
        for name in sorted(raw_left.keys() | raw_right.keys())
        if raw_left.get(name) != raw_right.get(name)
    ]
    return {
        "status": "pass" if not changes else "fail",
        "changed_paths": changes,
        "raw_changed_paths": raw_changes,
        "allowed_build_metadata_differences": [
            p for p in raw_changes if p not in changes and p in {UV_CACHE, WHEEL_RECORD}
        ],
        "first_sha256": bundle.digest(evidence_bytes(first)),
        "second_sha256": bundle.digest(evidence_bytes(second)),
        "metadata_excluded": ["tar-order", "mtime"],
        "container_generated_excluded": [
            ".dockerenv",
            "etc/hosts",
            "etc/hostname",
            "etc/resolv.conf",
        ],
    }


def inspect_index(repository: str, digest: str, architecture: str) -> dict[str, Any]:
    require(repository in POLICY["origin"]["image_repositories"])
    require(DIGEST.fullmatch(digest) is not None and architecture in PLATFORMS)
    raw = run("docker", "buildx", "imagetools", "inspect", repository + "@" + digest, "--raw")
    require("sha256:" + bundle.digest(raw) == digest, "DELIVERY_SUBJECT_MISMATCH")
    index = json.loads(raw)
    children = [
        m
        for m in index["manifests"]
        if m.get("platform", {}).get("os") == "linux"
        and m["platform"].get("architecture") == architecture
    ]
    require(len(children) == 1)
    child = children[0]["digest"]
    raw = run("docker", "buildx", "imagetools", "inspect", repository + "@" + child, "--raw")
    require("sha256:" + bundle.digest(raw) == child, "DELIVERY_SUBJECT_MISMATCH")
    manifest = json.loads(raw)
    return {
        "os": "linux",
        "architecture": architecture,
        "digest": child,
        "compressed_bytes": sum(layer["size"] for layer in manifest["layers"]),
        "config_digest": manifest["config"]["digest"],
    }


def check_local_subject(inspected: dict[str, Any], child: dict[str, Any], reference: str) -> None:
    """Docker classic stores report config IDs; containerd stores may report child IDs."""
    references = {reference}
    if reference.startswith("docker.io/library/postgres@"):
        references.add(reference.removeprefix("docker.io/library/"))
    require(
        bool(references.intersection(inspected.get("RepoDigests", []))), "DELIVERY_SUBJECT_MISMATCH"
    )
    require(
        inspected.get("Id") in {child["config_digest"], child["digest"]},
        "DELIVERY_SUBJECT_MISMATCH",
    )
    require(
        inspected.get("Architecture") == child["architecture"] and inspected.get("Os") == "linux"
    )
    descriptor = inspected.get("Descriptor")
    if descriptor:
        require(descriptor.get("digest") == child["digest"], "DELIVERY_SUBJECT_MISMATCH")


def export_inventory(image: str, directory: Path, label: str) -> list[dict[str, Any]]:
    container = run("docker", "create", "--pull=never", image).decode().strip()
    require(re.fullmatch(r"[a-f0-9]{64}", container) is not None)
    archive = directory / (label + ".tar")
    try:
        run("docker", "export", "-o", str(archive), container)
        inventory = filesystem_inventory(archive)
        save(directory / (label + "-filesystem.json"), inventory)
        return inventory
    finally:
        run("docker", "rm", "-v", container)
        archive.unlink(missing_ok=True)


def notice_sbom(text: str, subject: str) -> tuple[dict[str, Any], list[str]]:
    """Conservative shipped Web notice inventory; no invented license declarations."""
    components: list[dict[str, Any]] = []
    missing: list[str] = []
    for match in re.finditer(r"^([^\n]+)@([^\n@]+)\nDeclared license: ([^\n]+)\n", text, re.M):
        name, version, raw_license = match.groups()
        license_value = json.loads(raw_license)
        components.append(
            {
                "type": "library",
                "name": name,
                "version": version,
                "licenses": [{"license": {"name": str(license_value)}}],
            }
        )
        if text[match.end() :].startswith("No root license text found; review required."):
            missing.append(name + "@" + version)
    require(bool(components), "DELIVERY_WEB_INVENTORY_MISSING")
    return {
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "version": 1,
        "metadata": {
            "properties": [
                {"name": gate_sbom.SUBJECT_PROPERTY, "value": subject},
                {
                    "name": "custometry:coverage",
                    "value": "conservative shipped Web notices, includes build dependencies",
                },
            ]
        },
        "components": components,
    }, missing


def web_notices(image: str, subject: str, directory: Path) -> bool:
    container = run("docker", "create", "--pull=never", image).decode().strip()
    require(re.fullmatch(r"[a-f0-9]{64}", container) is not None)
    path = directory / "THIRD-PARTY.txt"
    try:
        run("docker", "cp", container + ":/usr/share/nginx/html/notices/THIRD-PARTY.txt", str(path))
    finally:
        run("docker", "rm", "-v", container)
    document, missing = notice_sbom(path.read_text(), subject)
    save(directory / "web-notices-sbom.json", document)
    result = gate_licenses.check(
        directory, Path("web-notices-sbom.json"), ROOT / "deploy/license-policy.json"
    )
    save(
        directory / "web-notices-gate.json",
        {
            "subject": subject,
            "notice_sha256": sha(path),
            "missing_root_text": missing,
            "licenses": result.to_dict(),
        },
    )
    # Retain evidence even when policy findings prevent signing. The notice inventory
    # supplements final-image cataloging; known missing runtime notices never pass.
    return result.ok and not missing


def normalize_python_licenses(
    document: dict[str, Any], raw: dict[str, Any], image: str, directory: Path
) -> list[dict[str, Any]]:
    """Fill missing declarations from exact installed metadata and actual notice files."""
    inventory = {row["path"]: row for row in load(directory / "selected-filesystem.json")}
    python_packages = {
        (p["name"], p["version"]): p for p in raw["artifacts"] if p["type"] == "python"
    }
    observations: list[dict[str, Any]] = []
    container = run("docker", "create", "--pull=never", image).decode().strip()
    require(re.fullmatch(r"[a-f0-9]{64}", container) is not None)
    try:
        for component in document["components"]:
            package = python_packages.get((component.get("name"), component.get("version")))
            if package is None or component.get("licenses"):
                continue
            locations = [p["path"] for p in package["locations"] if p["path"].endswith(".dist-info/METADATA")]
            require(len(locations) == 1)
            location = locations[0].lstrip("/")
            bundle.safe_path(location)
            expected = inventory[location]
            require(0 < expected["size_bytes"] <= 1048576, "DELIVERY_LIMIT")
            temporary = directory / "installed-metadata"
            try:
                run("docker", "cp", container + ":/" + location, str(temporary))
                data = temporary.read_bytes()
                require(bundle.digest(data) == expected["sha256"], "DELIVERY_SUBJECT_MISMATCH")
            finally:
                temporary.unlink(missing_ok=True)
            metadata = BytesParser().parsebytes(data)
            require(metadata["Name"] == package["name"] and metadata["Version"] == package["version"])
            declaration = metadata.get("License-Expression")
            if declaration is None:
                classifiers = metadata.get_all("Classifier", [])
                # Only the exact standardized MIT classifier is mapped here. No fuzzy
                # copyright-text matching or conversion of an unlisted license occurs.
                licenses = [v for v in classifiers if v.startswith("License ::")]
                if licenses == ["License :: OSI Approved :: MIT License"]:
                    declaration = "MIT"
            if declaration is None:
                continue
            root = package["metadata"]["sitePackagesRootPath"].strip("/")
            notice_files: list[dict[str, Any]] = []
            for item in package["metadata"]["files"]:
                name = root + "/" + item["path"]
                if ".dist-info/" in name and re.search(r"/(?:LICENSE|COPYING|NOTICE)(?:[./]|$)", name, re.I):
                    bundle.safe_path(name)
                    actual = inventory.get(name)
                    if actual is not None and actual.get("size_bytes", 0) > 0:
                        notice_files.append(actual)
            if not notice_files:
                continue
            component["licenses"] = [{"expression": str(declaration)}]
            observations.append({
                "name": package["name"], "version": package["version"],
                "expression": str(declaration), "metadata": expected,
                "notice_files": notice_files,
            })
    finally:
        run("docker", "rm", "-v", container)
    return observations


def scan(image: str, subject: str, directory: Path) -> dict[str, Any]:
    """Invoke pinned installed tools against the exact pulled registry child."""
    require(image.endswith("@" + subject))
    require(json.loads(run("syft", "version", "-o", "json"))["version"] == "1.51.1")
    raw = json.loads(run("syft", "docker:" + image, "-o", "syft-json"))
    save(directory / "sbom-raw.json", raw)
    converted = json.loads(
        run("syft", "convert", str(directory / "sbom-raw.json"), "-o", "cyclonedx-json")
    )
    bound = bind_sbom(converted, raw["source"], subject)
    save(directory / "sbom-original.json", bound)
    normalized = normalize_python_licenses(bound, raw, image, directory)
    save(directory / "license-metadata.json", {"subject": subject, "normalizations": normalized})
    save(directory / "sbom.json", bound)
    sbom_result = gate_sbom.check(
        directory, Path("sbom.json"), expected_subjects=[subject], require_subjects=True
    )
    licenses = gate_licenses.check(
        directory, Path("sbom.json"), ROOT / "deploy/license-policy.json"
    )
    cache = directory / "trivy-cache"
    run(
        "trivy",
        "--cache-dir",
        str(cache),
        "image",
        "--image-src",
        "docker",
        "--scanners",
        "vuln",
        "--format",
        "json",
        "--ignorefile",
        "/dev/null",
        "--ignore-unfixed=false",
        "--skip-db-update=false",
        "--severity",
        "UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL",
        "--output",
        str(directory / "trivy.json"),
        image,
    )
    database = json.loads(run("trivy", "--cache-dir", str(cache), "version", "--format", "json"))
    save(
        directory / "trivy-db.json",
        {
            "database_sha256": sha(cache / "db/trivy.db"),
            "metadata_sha256": sha(cache / "db/metadata.json"),
        },
    )
    save(directory / "trivy-version.json", database)
    vulnerabilities = vulnerability_result(
        load(directory / "trivy.json"), database, subject, datetime.now(timezone.utc)
    )
    notices_ok = web_notices(image, subject, directory) if "custometry-web@" in image else True
    results = {
        "web_notice_coverage": notices_ok,
        "sbom": sbom_result.to_dict(),
        "licenses": licenses.to_dict(),
        "vulnerabilities": vulnerabilities,
    }
    save(directory / "gates.json", results)
    require(
        sbom_result.ok and licenses.ok and vulnerabilities["status"] == "pass" and notices_ok,
        "DELIVERY_SUPPLY_GATES_FAILED",
    )
    return results


def native(args: argparse.Namespace) -> None:
    architecture = args.architecture
    require(platform.system() == "Linux")
    require(
        platform.machine() == {"amd64": "x86_64", "arm64": "aarch64"}[architecture],
        "DELIVERY_NATIVE_REQUIRED",
    )
    engine = json.loads(run("docker", "info", "--format", "{{json .}}"))
    require(engine["Architecture"] == {"amd64": "x86_64", "arm64": "aarch64"}[architecture])
    require(run("git", "rev-parse", "HEAD").decode().strip() == args.commit)
    require(re.fullmatch(r"[a-f0-9]{40}", args.commit) is not None)
    require(
        not run("git", "status", "--porcelain", "--untracked-files=all", "--", *bundle.SOURCE_PATHS)
    )
    output = args.output.resolve()
    require(not output.exists())
    output.mkdir(parents=True, mode=0o700)
    settings = load(ROOT / "deploy/compose/delivery-supply-tools.json")
    source = output / "source.tar"
    bundle.capture(args.commit, source)
    # Fresh directory from a trusted Git archive; no worktree or source mounts.
    snapshot = output / "source"
    snapshot.mkdir()
    with tarfile.open(source) as archive:
        archive.extractall(snapshot, filter="data")
    version = "0.1.0-dev.0+sha." + args.commit[:12]
    observations: dict[str, Any] = {}
    for role, index in (
        ("api", args.api_digest),
        ("web", args.web_digest),
        ("postgres", bundle.POSTGRES_DIGEST),
    ):
        repository = (
            "docker.io/library/postgres"
            if role == "postgres"
            else "ghcr.io/dejetins/custometry-" + role
        )
        platform_record = inspect_index(repository, index, architecture)
        image = repository + "@" + platform_record["digest"]
        run("docker", "pull", "--platform", "linux/" + architecture, image)
        inspected = json.loads(run("docker", "image", "inspect", image))[0]
        check_local_subject(inspected, platform_record, image)
        platform_record.pop("config_digest")
        platform_record["unpacked_bytes"] = inspected["Size"]
        directory = output / role
        directory.mkdir()
        selected = export_inventory(image, directory, "selected")
        if role != "postgres":
            require(inspected["Config"]["Labels"]["org.opencontainers.image.version"] == version)
            bundle.observe_image_files(image, role, directory / "embedded.json")
            for attempt in (1, 2):
                builder = f"ms001-{role}-{architecture}-{attempt}"
                local = f"custometry-ms001-rebuild-{role}:{architecture}-{attempt}"
                command = [
                    "docker",
                    "buildx",
                    "build",
                    "--builder",
                    builder,
                    "--no-cache",
                    "--load",
                    "--platform",
                    "linux/" + architecture,
                    "--provenance=false",
                    "--sbom=false",
                    "--build-arg",
                    "CUSTOMETRY_VERSION=" + version,
                    "-t",
                    local,
                    "-f",
                    str(snapshot / f"apps/{role}/Dockerfile"),
                    str(snapshot),
                ]
                run(
                    "docker",
                    "buildx",
                    "create",
                    "--name",
                    builder,
                    "--driver",
                    "docker-container",
                    "--driver-opt",
                    "image=" + settings["buildkit"],
                )
                try:
                    run(*command)
                    actual = export_inventory(local, directory, f"rebuild-{attempt}")
                    comparison = compare(selected, actual)
                    save(directory / f"comparison-{attempt}.json", comparison)
                    save(
                        directory / f"build-{attempt}.json",
                        {
                            "command": command,
                            "source_commit": args.commit,
                            "source_archive_sha256": sha(source),
                            "image": json.loads(run("docker", "image", "inspect", local))[0]["Id"],
                        },
                    )
                    require(comparison["status"] == "pass", "DELIVERY_REBUILD_DRIFT")
                finally:
                    run("docker", "buildx", "rm", builder)
        scan(image, platform_record["digest"], directory)
        observations[role] = {
            "repository": repository,
            "index_digest": index,
            "platform": platform_record,
        }
    save(
        output / "platform.json",
        {
            "source_commit": args.commit,
            "architecture": architecture,
            "engine_version": engine["ServerVersion"],
            "compose_version": run("docker", "compose", "version", "--short").decode().strip(),
            "images": observations,
            "source_archive_sha256": sha(source),
        },
    )


def verify(record_path: Path, signature: Path, trust_root: Path, expected_commit: str) -> None:
    record = bundle.STRUCTURE.parse_json(record_path.read_bytes())
    bundle.validate_record(record)
    require(record_path.read_bytes() == bundle.canonical(record))
    require(record["source"]["commit"] == expected_commit, "DELIVERY_SOURCE_MISMATCH")
    settings = load(ROOT / "deploy/compose/delivery-supply-tools.json")
    require(sha(trust_root) == settings["trusted_root"]["sha256"], "DELIVERY_TRUST_MISMATCH")
    signer = POLICY["signer"]
    run(
        "cosign",
        "verify-blob",
        "--bundle",
        str(signature),
        "--trusted-root",
        str(trust_root),
        "--certificate-identity",
        signer["identity"],
        "--certificate-oidc-issuer",
        signer["issuer"],
        "--certificate-github-workflow-repository",
        POLICY["origin"]["repository"],
        "--certificate-github-workflow-ref",
        POLICY["origin"]["ref"],
        "--certificate-github-workflow-sha",
        expected_commit,
        str(record_path),
    )
    bundle.check_payload(record, bundle.candidate_payload(record, record_path.parent))


def assemble_supply(inputs: Path, output: Path, commit: str, run_id: int, run_attempt: int) -> None:
    """Aggregate native observations; use exact evidence bytes and preserve subjects."""
    require(re.fullmatch(r"[a-f0-9]{40}", commit) is not None and run_id > 0 and run_attempt > 0)
    records = {arch: load(inputs / arch / "platform.json") for arch in sorted(PLATFORMS)}
    require(
        all(
            r["architecture"] == arch and r["source_commit"] == commit
            for arch, r in records.items()
        )
    )
    require(len({r["source_archive_sha256"] for r in records.values()}) == 1)
    payload: dict[str, bytes] = {}
    evidence: list[dict[str, Any]] = []
    images: dict[str, Any] = {}
    for role in ("api", "web", "postgres"):
        refs = [r["images"][role] for r in records.values()]
        require(len({r["index_digest"] for r in refs}) == 1)
        require(len({r["repository"] for r in refs}) == 1)
        embedded = []
        for arch, record in records.items():
            directory = inputs / arch / role
            subject = record["images"][role]["platform"]["digest"]
            sbom_result = gate_sbom.check(
                directory, Path("sbom.json"), expected_subjects=[subject], require_subjects=True
            )
            license_result = gate_licenses.check(
                directory, Path("sbom.json"), ROOT / "deploy/license-policy.json"
            )
            vuln_result = vulnerability_result(
                load(directory / "trivy.json"),
                load(directory / "trivy-version.json"),
                subject,
                datetime.now(timezone.utc),
            )
            require(
                sbom_result.ok and license_result.ok and vuln_result["status"] == "pass",
                "DELIVERY_SUPPLY_GATES_FAILED",
            )
            files = {
                "sbom.json": "sbom",
                "gates.json": "licenses",
                "trivy.json": "vulnerabilities",
                "trivy-version.json": "vulnerabilities",
                "trivy-db.json": "vulnerabilities",
                "sbom-raw.json": "sbom",
                "sbom-original.json": "sbom",
                "license-metadata.json": "licenses",
            }
            if role == "web":
                notice_path = directory / "THIRD-PARTY.txt"
                bom, missing = notice_sbom(notice_path.read_text(), subject)
                require(
                    bom == load(directory / "web-notices-sbom.json") and not missing,
                    "DELIVERY_WEB_INVENTORY_MISSING",
                )
                require(
                    gate_licenses.check(
                        directory,
                        Path("web-notices-sbom.json"),
                        ROOT / "deploy/license-policy.json",
                    ).ok,
                    "DELIVERY_SUPPLY_GATES_FAILED",
                )
                payload[f"notices/{arch}-THIRD-PARTY.txt"] = notice_path.read_bytes()
                files["web-notices-sbom.json"] = "sbom"
                files["web-notices-gate.json"] = "licenses"
            if role != "postgres":
                current = load(directory / "embedded.json")
                if not embedded:
                    embedded = current
                else:
                    # Common v1 embedded inventory must have consistent cross-platform bytes.
                    shared = {r["path"]: r for r in embedded}
                    embedded = [row for row in current if shared.get(row["path"]) == row]
                for attempt in (1, 2):
                    rebuilt = load(directory / f"rebuild-{attempt}-filesystem.json")
                    comparison = compare(load(directory / "selected-filesystem.json"), rebuilt)
                    require(comparison["status"] == "pass", "DELIVERY_REBUILD_DRIFT")
                    build = load(directory / f"build-{attempt}.json")
                    require(
                        build["source_commit"] == commit
                        and build["source_archive_sha256"] == record["source_archive_sha256"]
                    )
                    files[f"comparison-{attempt}.json"] = "rebuild-comparison"
                    files[f"build-{attempt}.json"] = "provenance"
                files["embedded.json"] = "provenance"
            for name, kind in files.items():
                target = f"evidence/{arch}-{role}-{name}"
                raw = (directory / name).read_bytes()
                payload[target] = raw
                evidence.append(
                    {
                        "kind": kind,
                        "subject": subject,
                        "file": bundle.file_record(target, raw, "evidence"),
                    }
                )
        images[role] = {
            "repository": refs[0]["repository"],
            "index_digest": refs[0]["index_digest"],
            "platforms": [r["platform"] for r in refs],
            "embedded_files": embedded,
        }
    inventory = load(ROOT / "deploy/compose/delivery-image-inventory.json")
    head = inventory["migration_chain"][-1]["revision"]
    version = "0.1.0-dev.0+sha." + commit[:12]
    delivery_version = f"0.1.0-ms001.{run_id}"
    build_inputs = [
        {"path": name, "sha256": sha(ROOT / name)}
        for name in (
            "uv.lock",
            "pnpm-lock.yaml",
            "apps/api/Dockerfile",
            "apps/web/Dockerfile",
            "deploy/compose/delivery-supply-tools.json",
            "deploy/compose/delivery-verification-policy.json",
            "tools/custometry_quality/delivery_supply.py",
            ".github/workflows/publish-candidates.yml",
        )
    ]
    metadata = {
        "schema_version": "custometry-delivery/v1",
        "delivery_version": delivery_version,
        "application_version": version,
        "channel": "internal-candidate",
        "source": {"repository": "https://github.com/Dejetins/custometry", "commit": commit},
        "producer": {
            "workflow": POLICY["origin"]["workflow"],
            "ref": "refs/heads/main",
            "run_id": run_id,
            "run_attempt": run_attempt,
        },
        "profiles": ["core", "migration", "demo"],
        "images": images,
        "capabilities": [
            {
                "id": "foundation-artifact",
                "status": "enabled",
                "services": ["api", "web", "edge", "control-db"],
                "reason": "Bounded artifact supply; runtime and installed journeys require later proof.",
            },
            {
                "id": "optional-demo-resources",
                "status": "enabled",
                "services": ["demo-source-db"],
                "reason": "Explicit optional database resources; no end-to-end analytics readiness claim.",
            },
        ],
        "compatibility": {
            "reader_major": 1,
            "configuration_schema": "custometry-compose/v1",
            "docker_api_min": "1.43",
            "compose_min": "2.24.4",
            "postgres_version": "17.11",
            "supported_platforms": ["linux/amd64", "linux/arm64"],
            "tested_engines": [
                {
                    "engine_version": r["engine_version"],
                    "compose_version": r["compose_version"],
                    "host_os": "linux",
                    "host_arch": arch,
                }
                for arch, r in records.items()
            ],
        },
        "migrations": {
            "head": head,
            "revisions": inventory["migration_chain"],
            "support_files": inventory["migration_support"],
            "starting_state": "fresh-owned-database",
            "read_head": head,
            "write_head": head,
            "command": ["alembic", "-c", "/app/migrations/alembic.ini", "upgrade", "head"],
            "downtime": "before-application-start",
            "rollback": "not-qualified",
            "artifact_format_compatibility": "not-qualified",
        },
        "build_inputs": build_inputs,
        "evidence": evidence,
        "resources_budget": {
            "ram_bytes": 6442450944,
            "owned_disk_bytes": 26843545600,
            "api_unpacked_max_bytes": 367001600,
            "web_unpacked_max_bytes": 104857600,
        },
        "retrieval": {
            "provider": "github-actions-artifact",
            "repository": "Dejetins/custometry",
            "artifact_name": bundle.artifact_name(delivery_version, run_id, run_attempt),
            "retention_days": 90,
        },
        "signature": {
            "format": "sigstore-bundle",
            "path": "delivery-manifest.sigstore.json",
            "subject": "canonical-manifest-bytes",
        },
    }
    for name in bundle.DEMO_FILES:
        payload["demo/init/" + name] = (ROOT / "deploy/demo-source/init" / name).read_bytes()
    require(not output.exists())
    source = output.with_name(output.name + "-payload")
    bundle.write_new(source, payload)
    bundle.assemble(metadata, source, output)


def unwrap_transport(raw: bytes, provider_digest: str) -> bytes:
    """Remove one provider wrapper; do not extract or inspect the payload ZIP."""
    limit = POLICY["limits"]["archive_bytes"]
    require(len(raw) <= limit, "DELIVERY_LIMIT")
    require("sha256:" + bundle.digest(raw) == provider_digest, "DELIVERY_SUBJECT_MISMATCH")
    with zipfile.ZipFile(io.BytesIO(raw)) as container:
        require(container.namelist() == ["delivery.zip"], "DELIVERY_TRANSPORT_INVALID")
        info = container.getinfo("delivery.zip")
        mode = info.external_attr >> 16
        require(not info.is_dir() and stat.S_IFMT(mode) in {0, stat.S_IFREG})
        require(not info.flag_bits & 1)
        require(info.compress_type in {zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED})
        require(0 < info.file_size <= limit, "DELIVERY_LIMIT")
        require(
            info.file_size <= max(info.compress_size, 1) * POLICY["limits"]["compression_ratio"],
            "DELIVERY_LIMIT",
        )
        with container.open(info) as source:
            payload = source.read(limit + 1)
        require(len(payload) == info.file_size and len(payload) <= limit, "DELIVERY_LIMIT")
    return payload


def reconcile(archive: Path, run_id: int, run_attempt: int, output: Path) -> None:
    """Read-only provider reconciliation; never overwrite or delete any version."""
    require(run_id > 0 and archive.stat().st_size <= POLICY["limits"]["archive_bytes"])
    version = f"0.1.0-ms001.{run_id}"
    name = bundle.artifact_name(version, run_id, run_attempt)
    legacy_name = f"custometry-delivery-{version}"
    attempts = re.compile(re.escape(f"{legacy_name}-{run_id}-") + r"[1-9][0-9]*")
    pages = json.loads(
        run(
            "gh",
            "api",
            "--paginate",
            "--slurp",
            "repos/Dejetins/custometry/actions/artifacts?per_page=100",
        )
    )
    # Global enumeration prevents another attempt (or the legacy short name)
    # from reassigning an already published delivery version.
    artifacts = [
        a for page in pages for a in page["artifacts"]
        if a["name"] == legacy_name or attempts.fullmatch(a["name"])
    ]
    require(len(artifacts) <= 1, "DELIVERY_VERSION_CONFLICT")
    lines = ["exists=false", f"artifact_name={name}"]
    if artifacts:
        artifact = artifacts[0]
        require(
            not artifact["expired"] and artifact["workflow_run"]["id"] == run_id,
            "DELIVERY_UNAVAILABLE",
        )
        require(artifact["size_in_bytes"] <= POLICY["limits"]["archive_bytes"])
        raw = run(
            "gh", "api", f"repos/Dejetins/custometry/actions/artifacts/{int(artifact['id'])}/zip"
        )
        payload = unwrap_transport(raw, artifact["digest"])
        require(bundle.digest(payload) == sha(archive), "DELIVERY_VERSION_CONFLICT")
        lines = [
            "exists=true",
            f"artifact_name={artifact['name']}",
            f"artifact_id={int(artifact['id'])}",
            f"artifact_digest={artifact['digest']}",
        ]
    with output.open("a") as stream:
        stream.write("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    p = sub.add_parser("native")
    p.add_argument("--architecture", choices=sorted(PLATFORMS), required=True)
    p.add_argument("--commit", required=True)
    p.add_argument("--api-digest", required=True)
    p.add_argument("--web-digest", required=True)
    p.add_argument("--output", type=Path, required=True)
    p = sub.add_parser("inventory")
    p.add_argument("--archive", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p = sub.add_parser("compare")
    p.add_argument("--first", type=Path, required=True)
    p.add_argument("--second", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p = sub.add_parser("assemble")
    p.add_argument("--inputs", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--commit", required=True)
    p.add_argument("--run-id", type=int, required=True)
    p.add_argument("--run-attempt", type=int, required=True)
    p = sub.add_parser("reconcile")
    p.add_argument("--archive", type=Path, required=True)
    p.add_argument("--run-id", type=int, required=True)
    p.add_argument("--run-attempt", type=int, required=True)
    p.add_argument("--output", type=Path, required=True)
    p = sub.add_parser("unwrap")
    p.add_argument("--transport", type=Path, required=True)
    p.add_argument("--provider-digest", required=True)
    p.add_argument("--payload-sha256", required=True)
    p.add_argument("--output", type=Path, required=True)
    p = sub.add_parser("verify")
    for name in ("record", "signature", "trust-root"):
        p.add_argument("--" + name, type=Path, required=True)
    p.add_argument("--commit", required=True)
    args = parser.parse_args()
    try:
        if args.action == "unwrap":
            require(args.transport.stat().st_size <= POLICY["limits"]["archive_bytes"])
            payload = unwrap_transport(args.transport.read_bytes(), args.provider_digest)
            require(bundle.digest(payload) == args.payload_sha256, "DELIVERY_SUBJECT_MISMATCH")
            with args.output.open("xb") as stream:
                stream.write(payload)
            args.output.chmod(0o600)
        elif args.action == "native":
            native(args)
        elif args.action == "reconcile":
            reconcile(args.archive, args.run_id, args.run_attempt, args.output)
        elif args.action == "assemble":
            assemble_supply(args.inputs, args.output, args.commit, args.run_id, args.run_attempt)
        elif args.action == "inventory":
            save(args.output, filesystem_inventory(args.archive))
        elif args.action == "compare":
            result = compare(load(args.first), load(args.second))
            save(args.output, result)
            require(result["status"] == "pass", "DELIVERY_REBUILD_DRIFT")
        else:
            verify(args.record, args.signature, args.trust_root, args.commit)
        print("DELIVERY_SUPPLY_PREPARED")
        return 0
    except (
        ValueError,
        OSError,
        KeyError,
        TypeError,
        subprocess.SubprocessError,
        tarfile.TarError,
        zipfile.BadZipFile,
    ) as exc:
        print(str(exc) if isinstance(exc, bundle.BundleError) else "DELIVERY_SUPPLY_UNAVAILABLE")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
