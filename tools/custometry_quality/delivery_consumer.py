"""Bounded internal-bundle consumer smoke; never builds or promotes a release."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import secrets
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from typing import Any
import urllib.request
import uuid
import zipfile


class ConsumerError(ValueError):
    """Safe failure code without payload or credentials."""


def require(value: object, code: str) -> None:
    if not value:
        raise ConsumerError(code)


def sha(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def unpack(source: Path, destination: Path, limit: int = 536870912) -> None:
    """Validate all entries before writing; atomically expose a complete new directory."""
    require(not destination.exists() and not destination.is_symlink(), "DESTINATION_EXISTS")
    with zipfile.ZipFile(source) as archive:
        entries = archive.infolist()
        require(0 < len(entries) <= 4096, "ARCHIVE_LIMIT")
        names = [entry.filename for entry in entries]
        require(len({name.casefold() for name in names}) == len(names), "DUPLICATE_PATH")
        require(sum(entry.file_size for entry in entries) <= limit, "ARCHIVE_LIMIT")
        for entry in entries:
            path = PurePosixPath(entry.filename)
            require(
                not path.is_absolute()
                and all(p not in ("", ".", "..") for p in entry.filename.split("/"))
                and "\\" not in entry.filename,
                "UNSAFE_PATH",
            )
            require(stat.S_ISREG(entry.external_attr >> 16), "NON_REGULAR_ENTRY")
        with tempfile.TemporaryDirectory(dir=destination.parent) as temporary:
            root = Path(temporary) / "complete"
            root.mkdir(mode=0o700)
            for entry in entries:
                target = root / entry.filename
                target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
                with archive.open(entry) as incoming, target.open("xb") as outgoing:
                    shutil.copyfileobj(incoming, outgoing, 1048576)
                target.chmod(0o600)
            root.rename(destination)


def checked_copy(source: Path, destination: Path, trusted: dict[str, Any]) -> int:
    destination.mkdir(mode=0o700)
    total = 0
    for item in trusted["files"]:
        name = item["path"]
        if name == "bundle/delivery-manifest.json":
            continue  # Compared after ZIP extraction, before reader execution.
        path = source / name
        require(
            path.is_file()
            and not path.is_symlink()
            and path.resolve().is_relative_to(source.resolve()),
            "SOURCE_PATH",
        )
        require(
            path.stat().st_size == item["size_bytes"] and sha(path) == item["sha256"],
            "TRUSTED_HASH_MISMATCH",
        )
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        shutil.copyfile(path, target)
        target.chmod(0o600)
        require(sha(target) == item["sha256"], "COPY_HASH_MISMATCH")
        total += target.stat().st_size
    return total


def prepare_demo_mount(bundle: Path) -> None:
    """Make verified demo files readable to PostgreSQL; retain private host parents."""
    root = bundle / "demo/init"
    root.chmod(0o755)
    for name in (
        "010_create_reader.sh",
        "015_profile.sh",
        "020_schema.sql",
        "030_seed.sql",
        "040_grants.sql",
    ):
        (root / name).chmod(0o755 if name.endswith(".sh") else 0o644)


def consume(source: Path, work: Path, trust: Path, architecture: str, keep: bool) -> dict[str, Any]:
    require(not work.exists(), "WORK_EXISTS")
    require(shutil.disk_usage(work.parent).free >= 2 * 1024**3, "INSUFFICIENT_DISK")
    work.mkdir(mode=0o700)
    result: dict[str, Any] = {
        "status": "running",
        "architecture": architecture,
        "timings_seconds": {},
    }
    output = work / "result.json"
    project = "ms001s04-" + uuid.uuid4().hex[:10]
    result["project"] = project
    environment = dict(os.environ)
    environment.pop("COMPOSE_FILE", None)
    environment.pop("COMPOSE_PROFILES", None)
    compose: list[str] = []

    def run(args: list[str], timeout: int = 180) -> str:
        process = subprocess.run(
            args,
            cwd=work,
            env=environment,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        if process.returncode != 0:
            result["failed_command"] = (
                args[len(compose) :] if compose and args[: len(compose)] == compose else args[:4]
            )
            # Only fixed diagnostic labels enter durable evidence, never raw logs.
            indicators = (
                "permission denied",
                "invalid reference format",
                "no such image",
                "unhealthy",
                "exited",
                "additional property",
                "invalid",
                "not found",
                "denied",
            )
            result["failure_indicators"] = [
                value for value in indicators if value in process.stderr.lower()
            ]
            if compose:
                logs = subprocess.run(
                    compose + ["logs", "--no-color", "--tail", "30"],
                    cwd=work,
                    env=environment,
                    text=True,
                    capture_output=True,
                    timeout=20,
                    check=False,
                )
                result["container_log_indicators"] = [
                    value for value in indicators if value in logs.stdout.lower()
                ]
        require(process.returncode == 0, "COMMAND_FAILED:" + ":".join(args[:3]))
        return process.stdout.strip()

    def timed(label: str, args: list[str]) -> str:
        start = time.monotonic()
        value = run(args)
        result["timings_seconds"][label] = round(time.monotonic() - start, 3)
        return value

    try:
        start = time.monotonic()
        trusted = json.loads(trust.read_text())
        acquired = work / "acquired"
        result["retrieved_bytes"] = checked_copy(source, acquired, trusted)
        result["timings_seconds"]["retrieval"] = round(time.monotonic() - start, 3)
        unpack(acquired / "delivery.zip", acquired / "bundle")
        manifest = acquired / "bundle/delivery-manifest.json"
        expected = next(
            item for item in trusted["files"] if item["path"] == "bundle/delivery-manifest.json"
        )
        require(sha(manifest) == expected["sha256"], "MANIFEST_TRUST")
        spec = importlib.util.spec_from_file_location(
            "trusted_delivery_reader",
            acquired / "toolkit/tools/custometry_quality/delivery_bundle.py",
        )
        assert spec and spec.loader
        reader = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(reader)
        record = reader.read_record(manifest, "internal-development")
        require(
            record["source"]["commit"] == "bc347d7e74c57640b42462c24cc2ed60d76ef055",
            "SOURCE_IDENTITY",
        )
        start = time.monotonic()
        reader.check_payload(record, reader.candidate_payload(record, acquired / "bundle"))
        reader.check_image_archives(record, acquired / "images")
        prepare_demo_mount(acquired / "bundle")
        result["timings_seconds"]["verification"] = round(time.monotonic() - start, 3)
        result.update(
            manifest_sha256=sha(manifest),
            source_commit=record["source"]["commit"],
            profile=record["channel"],
        )
        engine = json.loads(run(["docker", "info", "--format", "{{json .}}"]))
        result["engine"] = {
            key: engine.get(key)
            for key in ("ServerVersion", "Architecture", "OSType", "MemTotal", "NCPU")
        }
        require(
            engine["Architecture"]
            in ({"arm64", "aarch64"} if architecture == "arm64" else {"amd64", "x86_64"}),
            "NON_NATIVE_ENGINE",
        )
        observed_images: list[dict[str, Any]] = []
        result["images"] = observed_images
        for item in record["retrieval"]["archives"]:
            if item["architecture"] != architecture:
                continue
            timed(
                "import_" + item["role"],
                ["docker", "load", "--input", str(acquired / "images" / item["path"])],
            )
            info = json.loads(run(["docker", "image", "inspect", item["docker_id"]]))[0]
            require(info["Architecture"] == architecture, "IMPORTED_PLATFORM")
            observed_images.append({**item, "observed_id": info["Id"]})
        secret_dir = work / "secrets"
        secret_dir.mkdir(mode=0o700)
        for name in (
            "control_db_password",
            "demo_source_admin_password",
            "demo_source_reader_password",
        ):
            path = secret_dir / name
            path.write_text(secrets.token_urlsafe(32))
            path.chmod(0o444)
        environment.update(
            COMPOSE_PROJECT_NAME=project,
            CUSTOMETRY_SECRETS_DIR=str(secret_dir),
            CUSTOMETRY_BIND_HOST="127.0.0.1",
            CUSTOMETRY_HTTP_PORT="0",
        )
        # Explicit platform env wins over inherited image selections.
        for line in (acquired / f"bundle/.internal-{architecture}.env").read_text().splitlines():
            key, value = line.split("=", 1)
            environment[key] = value
        compose = [
            "docker",
            "compose",
            "--project-name",
            project,
            "--env-file",
            str(acquired / f"bundle/.internal-{architecture}.env"),
            "-f",
            str(acquired / "bundle/compose.json"),
            "--profile",
            "demo",
            "--profile",
            "migration",
        ]
        config = json.loads(run(compose + ["config", "--format", "json"]))
        require(
            sum(int(s["mem_limit"]) for s in config["services"].values()) <= 6 * 1024**3,
            "MEMORY_LIMIT",
        )
        require(
            all(
                "build" not in s and s["pull_policy"] == "never"
                for s in config["services"].values()
            ),
            "BUILD_OR_PULL",
        )
        timed(
            "database_start",
            compose
            + [
                "up",
                "-d",
                "--no-build",
                "--wait",
                "--wait-timeout",
                "120",
                "control-db",
                "demo-source-db",
            ],
        )
        timed("migration_fresh", compose + ["run", "--rm", "--no-deps", "migrate"])
        current = run(
            compose
            + [
                "run",
                "--rm",
                "--no-deps",
                "migrate",
                "alembic",
                "-c",
                "/app/migrations/alembic.ini",
                "current",
            ]
        )
        require("0009_notifications" in current, "MIGRATION_HEAD")
        timed("migration_repeat", compose + ["run", "--rm", "--no-deps", "migrate"])
        result["migration_head"] = "0009_notifications"
        timed(
            "application_start",
            compose
            + ["up", "-d", "--no-build", "--wait", "--wait-timeout", "120", "api", "web", "edge"],
        )
        run(
            compose
            + [
                "exec",
                "-T",
                "api",
                "python",
                "-c",
                'import custometry_api.main, pyarrow, pyarrow.parquet, sqlalchemy, psycopg, alembic; print("imports-ok")',
            ]
        )
        result["imports"] = "pass"
        port = run(compose + ["port", "edge", "8080"])
        require(re.fullmatch(r"127\.0\.0\.1:\d+", port), "PORT_BINDING")
        url = "http://" + port
        result["url"] = url
        paths = ["/", "/health/live", "/api/health/ready", "/docs/"]
        http: dict[str, Any] = {}
        for path in paths:
            with urllib.request.urlopen(url + path, timeout=10) as response:
                body = response.read()
                http[path] = {"status": response.status, "bytes": len(body)}
                if path == "/":
                    assets = re.findall(r'(?:src|href)="(/assets/[^\"]+)"', body.decode())
                    require(assets, "MISSING_ASSETS")
                    for asset in assets:
                        with urllib.request.urlopen(url + asset, timeout=10) as asset_response:
                            http[asset] = {
                                "status": asset_response.status,
                                "bytes": len(asset_response.read()),
                            }
        result["http"] = http
        ids = run(compose + ["ps", "-q"]).splitlines()
        result["stats"] = [
            json.loads(line)
            for line in run(
                ["docker", "stats", "--no-stream", "--format", "{{json .}}", *ids]
            ).splitlines()
        ]
        result["containers"] = [
            {k: item.get(k) for k in ("Name", "State", "Health", "Service")}
            for item in [
                json.loads(line) for line in run(compose + ["ps", "--format", "json"]).splitlines()
            ]
        ]
        result["status"] = "pass"
    except Exception as error:
        result["status"] = "failed"
        result["error"] = str(error) if isinstance(error, ConsumerError) else type(error).__name__
        raise
    finally:
        if compose and (not keep or result["status"] != "pass"):
            try:
                run(compose + ["down", "--volumes", "--remove-orphans"])
                result["cleanup"] = "owned-compose-resources-removed"
            except Exception:
                result["cleanup"] = "failed"
        else:
            result["cleanup"] = "retained-for-browser" if compose else "runtime-not-started"
        output.write_text(json.dumps(result, indent=2) + "\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--trust", type=Path, required=True)
    parser.add_argument("--architecture", choices=["arm64", "amd64"], required=True)
    parser.add_argument("--keep-for-browser", action="store_true")
    args = parser.parse_args()
    try:
        result = consume(
            args.source.resolve(),
            args.work.absolute(),
            args.trust.resolve(),
            args.architecture,
            args.keep_for_browser,
        )
    except Exception:
        print("Consumer failed; inspect the redacted result.json.", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "status": result["status"],
                "result": str(args.work / "result.json"),
                "url": result["url"],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
