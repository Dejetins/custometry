"""Local candidate packaging and closure checks; never release authorization.

All executable readers/templates come from this independently selected source,
not from a candidate payload. S03 supplies actual subjects/evidence and signs;
S04 owns authenticated retrieval and hostile archive/runtime verification.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import stat
import subprocess
import tempfile
import zipfile
from pathlib import Path
from types import ModuleType
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CONFIG = "compose.json"
ENV = ".release.env"
ENVELOPE = {"delivery-manifest.json", "delivery-manifest.sigstore.json"}
DEMO_FILES = (
    "010_create_reader.sh",
    "015_profile.sh",
    "020_schema.sql",
    "030_seed.sql",
    "040_grants.sql",
)
ROLES = {
    "api": "api",
    "migrate": "api",
    "web": "web",
    "edge": "web",
    "control-db": "postgres",
    "demo-source-db": "postgres",
}
SOURCE_PATHS = (
    ".dockerignore",
    ".node-version",
    ".uv-version",
    "scripts/activate-toolchain.sh",
    "pyproject.toml",
    "uv.lock",
    "README.md",
    "LICENSE",
    "mkdocs.yml",
    "package.json",
    "pnpm-lock.yaml",
    "pnpm-workspace.yaml",
    "compose.yaml",
    "apps/api",
    "apps/web",
    "packages",
    "plugins",
    "migrations",
    "docs-site",
    "deploy",
    "tools/custometry_quality/delivery_bundle.py",
    "tools/custometry_quality/delivery_supply.py",
    "tools/custometry_quality/delivery_companions.py",
    "tools/custometry_quality/delivery_set.py",
    "tools/custometry_quality/license_reviews.py",
    ".github/workflows/publish-candidates.yml",
)
PATH_PATTERN = re.compile(
    r"(?!.*(?:^|/)[.]{1,2}(?:/|$))[A-Za-z0-9_.][A-Za-z0-9_.-]*(?:/[A-Za-z0-9_.][A-Za-z0-9_.-]*)*"
)


class BundleError(ValueError):
    """Payload-free error safe for the CLI."""


def require(condition: bool, code: str = "DELIVERY_TAMPERED") -> None:
    if not condition:
        raise BundleError(code)


def reader(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, ROOT / "deploy/compose" / name)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


STRUCTURE = reader("validate-delivery-manifest.py")
LEGACY = reader("validate-release-manifest.py")


def canonical(value: Any) -> bytes:
    return STRUCTURE.canonical_bytes(value)


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def safe_path(name: str) -> str:
    require(len(name) <= 240 and PATH_PATTERN.fullmatch(name) is not None)
    return name


def unique(items: list[dict[str, Any]], key: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    folded: set[str] = set()
    for item in items:
        name = item[key]
        require(name.casefold() not in folded)
        folded.add(name.casefold())
        result[name] = item
    return result


def file_record(name: str, raw: bytes, role: str) -> dict[str, Any]:
    safe_path(name)
    require(len(raw) <= 67108864, "DELIVERY_LIMIT")
    return {"path": name, "sha256": digest(raw), "size_bytes": len(raw), "role": role}


def file_mode(name: str) -> int:
    if name == ENV:
        return 0o600
    if name in {"demo/init/010_create_reader.sh", "demo/init/015_profile.sh"}:
        return 0o755
    return 0o644


def projection(record: dict[str, Any]) -> bytes:
    values = {"CUSTOMETRY_VERSION": record["application_version"]}
    for role in ("api", "web"):
        image = record["images"][role]
        values[f"CUSTOMETRY_{role.upper()}_IMAGE"] = (
            image["repository"] + "@" + image["index_digest"]
        )
    raw = "".join(f"{key}={value}\n" for key, value in values.items()).encode("ascii")
    require(LEGACY.parse_manifest(raw) == values)
    return raw


def configuration(record: dict[str, Any]) -> dict[str, Any]:
    """Generate only the independently trusted finite candidate topology."""
    config: dict[str, Any] = json.loads(
        (ROOT / "deploy/compose/compose.candidate.json").read_bytes()
    )
    for name, service in config["services"].items():
        image = record["images"][ROLES[name]]
        service["image"] = image["repository"] + "@" + image["index_digest"]
        if name in ("api", "migrate"):
            service["environment"]["CUSTOMETRY_VERSION"] = record["application_version"]
    if "demo" not in record["profiles"]:
        del config["services"]["demo-source-db"]
        del config["volumes"]["demo_source_data"]
        del config["networks"]["demo_source"]
        for key in ("demo_source_admin_password", "demo_source_reader_password"):
            del config["secrets"][key]
    return config


def service_records(config: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "name": name,
            "image": ROLES[name],
            "profile": service.get("profiles", ["core"])[0],
            "depends_on": sorted(service.get("depends_on", {})),
        }
        for name, service in sorted(config["services"].items())
    ]


def resource_records(config: dict[str, Any]) -> list[dict[str, Any]]:
    """One explicit binding per service/resource, including external secret slots."""
    result: list[dict[str, Any]] = []
    for name, service in sorted(config["services"].items()):
        profile = service.get("profiles", ["core"])[0]
        bindings: list[tuple[str, str]] = []
        for kind, field in (
            ("secret-slot", "secrets"),
            ("network", "networks"),
            ("tmpfs", "tmpfs"),
        ):
            bindings.extend((kind, item) for item in service.get(field, []))
        for mount in service.get("volumes", []):
            source = mount.split(":")[0]
            if source == "./demo/init":
                bindings.extend(("bundle-file", "demo/init/" + f) for f in DEMO_FILES)
            else:
                bindings.append(("volume", source))
        for index, (kind, location) in enumerate(bindings):
            result.append(
                {
                    "id": f"{name}-{index}",
                    "kind": kind,
                    "location": location,
                    "services": [name],
                    "profile": profile,
                    "required": True,
                }
            )
    return result


def artifact_name(delivery_version: str, run_id: int, run_attempt: int) -> str:
    """S01 immutable provider identity; attempts never redefine delivery contents."""
    require(run_id > 0 and run_attempt > 0)
    return f"custometry-delivery-{delivery_version}-{run_id}-{run_attempt}"


def validate_record(record: dict[str, Any]) -> None:
    version = record.get("schema_version")
    require(version in {"custometry-delivery/v1", "custometry-delivery/v2"}, "DELIVERY_READER_UNSUPPORTED")
    name = "delivery-manifest.v2.schema.json" if version == "custometry-delivery/v2" else "delivery-manifest.schema.json"
    schema = STRUCTURE.parse_json(
        (ROOT / "deploy/compose" / name).read_bytes()
    )
    STRUCTURE.check_schema(schema, schema)
    STRUCTURE.validate(record, schema, schema)
    producer = record["producer"]
    require(record["retrieval"]["artifact_name"] == artifact_name(
        record["delivery_version"], producer["run_id"], producer["run_attempt"]
    ))
    config = configuration(record)
    require(sorted(record["profiles"]) in (["core", "migration"], ["core", "demo", "migration"]))
    require(sorted(record["services"], key=lambda s: s["name"]) == service_records(config))
    unique(record["services"], "name")
    services = set(config["services"])
    unique(record["capabilities"], "id")
    for capability in record["capabilities"]:
        require(set(capability["services"]) <= services)
    for role, image in record["images"].items():
        expected_repo = (
            "docker.io/library/postgres"
            if role == "postgres"
            else f"ghcr.io/dejetins/custometry-{role}"
        )
        require(image["repository"] == expected_repo)
        require({p["architecture"] for p in image["platforms"]} == {"amd64", "arm64"})
        for name in unique(image["embedded_files"], "path"):
            safe_path(name)
    expected_images = json.loads(
        (ROOT / "deploy/compose/delivery-image-inventory.json").read_bytes()
    )
    for role in ("api", "web"):
        embedded = unique(record["images"][role]["embedded_files"], "path")
        for item in expected_images[role]:
            actual = embedded.get(item["path"], {})
            require(all(actual.get(k) == item[k] for k in ("path", "sha256", "size_bytes")))
    web_files = unique(record["images"]["web"]["embedded_files"], "path")
    require(
        all(
            web_files.get(name, {}).get("size_bytes", 0) > 0
            for name in expected_images["web_generated_required"]
        )
    )
    # Pin upstream identity independently of the candidate record.
    require(record["images"]["postgres"]["index_digest"] == POSTGRES_DIGEST)
    files = unique(record["files"], "path")
    require(CONFIG in files and ENV in files and not (set(files) & ENVELOPE))
    for name in files:
        safe_path(name)
    unique(record["build_inputs"], "path")
    for item in record["build_inputs"]:
        safe_path(item["path"])
    resources = unique(record["resources"], "id")
    expected = resource_records(config)
    actual = [r for r in resources.values() if r["kind"] != "image-file"]
    require(sorted(actual, key=lambda r: r["id"]) == sorted(expected, key=lambda r: r["id"]))
    for resource in resources.values():
        require(set(resource["services"]) <= services)
        if resource["kind"] == "bundle-file":
            require(resource["location"] in files)
        if resource["kind"] == "image-file":
            for service in resource["services"]:
                embedded = unique(record["images"][ROLES[service]]["embedded_files"], "path")
                require(resource["location"] in embedded)
    migrations = record["migrations"]
    require(migrations["revisions"] == expected_images["migration_chain"])
    require(migrations["support_files"] == expected_images["migration_support"])
    revisions = unique(migrations["revisions"], "revision")
    previous = None
    embedded = unique(record["images"]["api"]["embedded_files"], "path")
    for revision in revisions.values():
        require(revision["down_revision"] == previous)
        previous = revision["revision"]
        require(embedded.get(revision["file"]["path"]) == revision["file"])
    require(previous == migrations["head"] == migrations["read_head"] == migrations["write_head"])
    for item in migrations["support_files"]:
        require(embedded.get(item["path"]) == item)
    for item in record["evidence"]:
        require(files.get(item["file"]["path"]) == item["file"])
        subjects = {i["index_digest"] for i in record["images"].values()}
        subjects.update(p["digest"] for i in record["images"].values() for p in i["platforms"])
        require(item["subject"] in subjects)
    required_payload = {CONFIG, ENV, "delivery-verification-policy.json"}
    required_payload.update(e["file"]["path"] for e in record["evidence"])
    if "demo" in record["profiles"]:
        required_payload.update("demo/init/" + name for name in DEMO_FILES)
    require(required_payload <= set(files))
    require(all(name in required_payload or name.startswith("notices/") for name in files))
    projection(record)


POSTGRES_DIGEST = "sha256:9ae4e8f8d0284836a505f0b2e825144e32e20499856e7dc5f7b99e19d10eedd6"


def payload_files(directory: Path) -> dict[str, bytes]:
    """Read only bounded regular local payloads; never follow a symlink."""
    require(directory.is_dir() and not directory.is_symlink())
    result: dict[str, bytes] = {}
    total = 0
    for path in sorted(directory.rglob("*")):
        mode = path.lstat().st_mode
        require(not stat.S_ISLNK(mode))
        if stat.S_ISDIR(mode):
            continue
        require(stat.S_ISREG(mode))
        name = safe_path(path.relative_to(directory).as_posix())
        with path.open("rb") as stream:
            raw = stream.read(67108865)
        total += len(raw)
        require(
            len(raw) <= 67108864 and total <= 536870912 and len(result) < 2048, "DELIVERY_LIMIT"
        )
        result[name] = raw
    require(len({n.casefold() for n in result}) == len(result))
    return result


def policy_path(record: dict[str, Any]) -> Path:
    version = record.get("schema_version")
    require(version in {"custometry-delivery/v1", "custometry-delivery/v2"}, "DELIVERY_READER_UNSUPPORTED")
    name = "delivery-verification-policy.v2.json" if version == "custometry-delivery/v2" else "delivery-verification-policy.json"
    return ROOT / "deploy/compose" / name


def check_payload(record: dict[str, Any], payload: dict[str, bytes]) -> None:
    validate_record(record)
    files = unique(record["files"], "path")
    require(set(payload) == set(files))
    for name, raw in payload.items():
        require(file_record(name, raw, files[name]["role"]) == files[name])
    require(payload[ENV] == projection(record))
    require(payload[CONFIG] == canonical(configuration(record)))
    require(
        payload.get("delivery-verification-policy.json")
        == policy_path(record).read_bytes()
    )


def candidate_payload(record: dict[str, Any], directory: Path) -> dict[str, bytes]:
    payload = payload_files(directory)
    if "delivery-manifest.json" in payload:
        require(payload.pop("delivery-manifest.json") == canonical(record))
    return payload


def write_new(directory: Path, payload: dict[str, bytes]) -> None:
    require(not directory.exists() and not directory.is_symlink())
    require(directory.parent.is_dir() and directory.parent.resolve() == directory.parent.absolute())
    directory.mkdir(mode=0o700)
    for name, raw in sorted(payload.items()):
        target = directory / safe_path(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as stream:
            stream.write(raw)
        target.chmod(file_mode(name))


def prepare(record: dict[str, Any], source: Path, output: Path) -> None:
    """Materialize supplied complete record inputs; never invent image evidence."""
    payload = payload_files(source)
    require(not (set(payload) & ENVELOPE))
    payload[CONFIG] = canonical(configuration(record))
    payload[ENV] = projection(record)
    payload["delivery-verification-policy.json"] = policy_path(record).read_bytes()
    check_payload(record, payload)
    write_new(output, payload)


def assemble(metadata: dict[str, Any], source: Path, output: Path) -> None:
    """Fill only derived fields; producer must supply actual image/build evidence.

    Metadata has all v1 fields except files/services/resources. Payload includes
    actual notices/evidence and (when enabled) the five demo files. No synthetic
    digest, scanner result, migration revision or tested engine is manufactured.
    """
    require(not ({"files", "services", "resources"} & set(metadata)))
    record = dict(metadata)
    payload = payload_files(source)
    require(not (set(payload) & ENVELOPE))
    config = configuration(record)
    record["services"] = service_records(config)
    record["resources"] = resource_records(config)
    payload[CONFIG] = canonical(config)
    payload[ENV] = projection(record)
    payload["delivery-verification-policy.json"] = policy_path(record).read_bytes()
    evidence_paths = {e["file"]["path"] for e in record["evidence"]}

    def role(name: str) -> str:
        if name == CONFIG:
            return "compose"
        if name == ENV:
            return "legacy-env"
        if name in evidence_paths:
            return "evidence"
        if name.startswith("notices/"):
            return "notices"
        if name.startswith("demo/init/"):
            return "resource"
        return "config"

    record["files"] = [file_record(n, b, role(n)) for n, b in sorted(payload.items())]
    files = unique(record["files"], "path")
    # Evidence file identities are input proof, not silently rewritten by assembly.
    for evidence in record["evidence"]:
        require(files.get(evidence["file"]["path"]) == evidence["file"])
    check_payload(record, payload)
    payload["delivery-manifest.json"] = canonical(record)
    write_new(output, payload)


def pack(record: dict[str, Any], payload: Path, signature: Path, output: Path) -> None:
    """Construct a deterministic ZIP after local closure; signature is not verified here."""
    content = candidate_payload(record, payload)
    check_payload(record, content)
    content["delivery-manifest.json"] = canonical(record)
    with signature.open("rb") as stream:
        content["delivery-manifest.sigstore.json"] = stream.read(1048577)
    require(0 < len(content["delivery-manifest.sigstore.json"]) <= 1048576, "DELIVERY_LIMIT")
    require(not output.exists() and not output.is_symlink())
    # Stored regular entries have deterministic bytes and cannot exceed ratio limits.
    with tempfile.TemporaryFile() as stream:
        with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_STORED) as archive:
            for name, raw in sorted(content.items()):
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = (stat.S_IFREG | file_mode(name)) << 16
                archive.writestr(info, raw)
        require(stream.tell() <= 134217728, "DELIVERY_LIMIT")
        stream.seek(0)
        with output.open("xb") as destination:
            while block := stream.read(1048576):
                destination.write(block)
        output.chmod(0o600)


def capture(commit: str, output: Path) -> None:
    """Archive a real commit only when its tracked source is the current clean tree."""
    require(re.fullmatch(r"[0-9a-f]{40}", commit) is not None, "DELIVERY_UNSUPPORTED")

    def git(*args: str) -> bytes:
        return subprocess.run(
            ["git", "-C", str(ROOT), *args],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout

    require(git("rev-parse", "HEAD").decode().strip() == commit, "DELIVERY_SOURCE_CAPTURE_REQUIRED")
    require(
        not git("status", "--porcelain", "--untracked-files=all", "--", *SOURCE_PATHS),
        "DELIVERY_SOURCE_CAPTURE_REQUIRED",
    )
    require(not output.exists() and not output.is_symlink())
    with output.open("xb") as stream:
        subprocess.run(
            ["git", "-C", str(ROOT), "archive", "--format=tar", commit, *SOURCE_PATHS],
            check=True,
            stdout=stream,
            stderr=subprocess.PIPE,
        )


def observe_image_files(image: str, role: str, output: Path) -> None:
    """Read a caller-authorized local image without running it or mounting source.

    The caller records image identity independently; this inventory is local
    observation, not a signature, platform qualification or registry claim.
    """
    require(role in {"api", "web"} and not output.exists())

    def docker(*args: str) -> bytes:
        return subprocess.run(
            ["docker", *args], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ).stdout

    container = docker("create", "--pull=never", image).decode().strip()
    require(re.fullmatch(r"[0-9a-f]{64}", container) is not None)
    try:
        with tempfile.TemporaryDirectory(prefix="ms001-image-files-") as scratch:
            root = Path(scratch)
            paths = ("app",) if role == "api" else ("usr/share/nginx/html", "etc/nginx")
            for name in paths:
                (root / name).parent.mkdir(parents=True, exist_ok=True)
                docker("cp", f"{container}:/{name}", str((root / name).parent))
            expected = json.loads(
                (ROOT / "deploy/compose/delivery-image-inventory.json").read_bytes()
            )
            names = {f["path"] for f in expected[role]}
            if role == "web":
                names.update(
                    p.relative_to(root).as_posix()
                    for p in (root / "usr/share/nginx/html").rglob("*")
                    if p.is_file()
                )
                names.update(expected["web_generated_required"])
            records: list[dict[str, Any]] = []
            for name in sorted(names):
                path = root / safe_path(name)
                require(path.is_file() and not path.is_symlink())
                raw = path.read_bytes()
                records.append(
                    file_record(
                        name, raw, "migration" if name.startswith("app/migrations/") else "asset"
                    )
                )
            actual = unique(records, "path")
            for item in expected[role]:
                require(
                    all(
                        actual[item["path"]][k] == item[k] for k in ("path", "sha256", "size_bytes")
                    )
                )
            if role == "web":
                require(
                    all(
                        actual[name]["size_bytes"] > 0
                        for name in expected["web_generated_required"]
                    )
                )
            with output.open("xb") as stream:
                stream.write(canonical(records))
    finally:
        docker("rm", "-v", container)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("check", "prepare", "pack", "assemble"):
        child = sub.add_parser(command)
        child.add_argument("--record", type=Path, required=True)
        child.add_argument("--payload", type=Path, required=True)
        if command != "check":
            child.add_argument("--output", type=Path, required=True)
        if command == "pack":
            child.add_argument("--signature", type=Path, required=True)
    child = sub.add_parser("capture")
    child.add_argument("--commit", required=True)
    child.add_argument("--output", type=Path, required=True)
    child = sub.add_parser("observe-image-files")
    child.add_argument("--image", required=True)
    child.add_argument("--role", choices=("api", "web"), required=True)
    child.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "capture":
            capture(args.commit, args.output)
        elif args.command == "observe-image-files":
            observe_image_files(args.image, args.role, args.output)
        else:
            if args.command == "assemble":
                with args.record.open("rb") as stream:
                    metadata = STRUCTURE.parse_json(stream.read(1048577))
                assemble(metadata, args.payload, args.output)
            else:
                record = STRUCTURE.read_contract(args.record, reader_major=2)
                if args.command == "check":
                    check_payload(record, candidate_payload(record, args.payload))
                elif args.command == "prepare":
                    prepare(record, args.payload, args.output)
                elif args.command == "pack":
                    pack(record, args.payload, args.signature, args.output)
    except (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError) as error:
        print(
            json.dumps(
                {
                    "result": "fail",
                    "code": str(error)
                    if isinstance(error, (BundleError, STRUCTURE.InvalidDelivery))
                    else "DELIVERY_INPUT_INVALID",
                    "next_action": "Correct candidate inputs; do not execute.",
                }
            )
        )
        return 2
    print(
        json.dumps(
            {
                "result": "pass",
                "code": "DELIVERY_CANDIDATE_PREPARED",
                "next_action": "Complete independent authenticity and runtime checks.",
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
