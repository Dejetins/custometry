"""Persistent internal installer. S01 stops at migrations; HTTPS readiness is unavailable."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import fcntl
import importlib.util
import ipaddress
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import socket
import stat
import subprocess
import sys
import tempfile
import time
from typing import Any, Generator

# Also runs from the independent flat toolkit under Python -I.
_spec = importlib.util.spec_from_file_location(
    "installation_consumer", Path(__file__).with_name("delivery_consumer.py")
)
assert _spec and _spec.loader
consumer = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(consumer)
require = consumer.require
sha = consumer.sha
SCHEMA = "custometry-installation/v1"
HEAD = "0009_notifications"
GIB = 1024**3
PRIVATE = ("config", "secrets", "tls", "acquisition", "logs")
STATES = {"prepared", "acquired", "migrated", "ready", "failed", "stopped"}


def atomic(path: Path, value: Any) -> None:
    require(not path.is_symlink(), "UNSAFE_PATH")
    fd, name = tempfile.mkstemp(prefix=".write-", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(value, stream, sort_keys=True, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def safe_path(path: Path) -> None:
    require(path.is_absolute() and path == path.resolve(), "UNSAFE_PATH")
    for part in (path, *path.parents):
        require(not part.is_symlink(), "UNSAFE_PATH")


def private(path: Path, mode: int = 0o700) -> None:
    safe_path(path)
    info = path.stat()
    require(info.st_uid == os.getuid() and stat.S_IMODE(info.st_mode) == mode, "PATH_OWNERSHIP")


@contextmanager
def locked(root: Path, create: bool = False) -> Generator[None]:
    safe_path(root)
    if not root.exists():
        require(create and root.parent.is_dir(), "ROOT_MISSING")
        root.mkdir(mode=0o700)
    private(root)
    state = root / "installation.json"
    if not state.exists():
        require(create and not list(root.iterdir()), "FOREIGN_ROOT")
    lock = root / ".installation.lock"
    fd = os.open(lock, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    try:
        private(lock, 0o600)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise consumer.ConsumerError("INSTALLATION_LOCKED") from None
        yield
    finally:
        os.close(fd)


def command(args: list[str], *, timeout: int = 5) -> str:
    # Discard inherited Compose/image selections and remote-engine overrides.
    environment = {
        k: v
        for k, v in os.environ.items()
        if not k.startswith(
            (
                "COMPOSE_",
                "CUSTOMETRY_",
                "DOCKER_HOST",
                "DOCKER_CONTEXT",
                "DOCKER_TLS",
                "DOCKER_CERT",
            )
        )
    }
    try:
        result = subprocess.run(
            args,
            env=environment,
            cwd="/",
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        raise consumer.ConsumerError("COMMAND_TIMEOUT") from None
    except OSError:
        raise consumer.ConsumerError("COMMAND_UNAVAILABLE") from None
    require(result.returncode == 0, "COMMAND_FAILED")
    return result.stdout.strip()


def engine(context: str | None = None) -> dict[str, Any]:
    selected = command(["docker", "context", "show"])
    require(context is None or selected == context, "ENGINE_CONTEXT_MISMATCH")
    context = context or selected
    endpoint = json.loads(command(["docker", "context", "inspect", context]))[0]
    host = endpoint["Endpoints"]["docker"]["Host"]
    require(host.startswith("unix://"), "REMOTE_ENGINE_UNSUPPORTED")
    info = json.loads(command(["docker", "--context", context, "info", "--format", "{{json .}}"]))
    require(info["OSType"] == "linux", "ENGINE_OS_UNSUPPORTED")
    arch = {"aarch64": "arm64", "arm64": "arm64", "x86_64": "amd64", "amd64": "amd64"}.get(
        info["Architecture"]
    )
    require(arch is not None, "ENGINE_PLATFORM_UNSUPPORTED")
    require(
        ["driver-type", "io.containerd.snapshotter.v1"] in info["DriverStatus"],
        "CONTAINERD_STORE_REQUIRED",
    )
    compose = command(["docker", "--context", context, "compose", "version", "--short"])
    require(re.match(r"v?[2-9]\.", compose), "COMPOSE_VERSION_UNSUPPORTED")
    require(info["MemTotal"] >= 6 * GIB and info["NCPU"] >= 1, "ENGINE_RESOURCES")
    return {
        "context": context,
        "id": info["ID"],
        "endpoint": host,
        "architecture": arch,
        "version": info["ServerVersion"],
        "compose_version": compose,
        "memory_bytes": info["MemTotal"],
        "cpu_cap": min(4, info["NCPU"]),
    }


def same_engine(saved: dict[str, Any], observed: dict[str, Any]) -> None:
    require(
        all(saved[k] == observed[k] for k in ("context", "id", "endpoint", "architecture")),
        "ENGINE_IDENTITY_MISMATCH",
    )


def read_state(root: Path) -> dict[str, Any]:
    private(root / "installation.json", 0o600)
    data = json.loads((root / "installation.json").read_bytes())
    require(data.get("schema_version") == SCHEMA, "STATE_SCHEMA_UNSUPPORTED")
    require(re.fullmatch(r"custometry-[a-f0-9]{24}", data.get("id", "")), "STATE_IDENTITY")
    require(data.get("root") == str(root) and data.get("state") in STATES, "STATE_IDENTITY")
    for name in PRIVATE:
        if (root / name).exists():
            private(root / name)
        else:
            require(data["last_completed_step"] == "prepared", "OWNED_PATH_MISSING")
    safe_path(root / "artifacts")
    return data


def checkpoint(root: Path, state: dict[str, Any], step: str) -> None:
    if step == "acquired" and state["last_completed_step"] == "migrated":
        step = "migrated"
    state.update(state=step, last_completed_step=step, failure_code=None)
    atomic(root / "installation.json", state)


def initial(
    root: Path, args: argparse.Namespace, observed: dict[str, Any], *, persist: bool = True
) -> dict[str, Any]:
    source, trust = args.source.absolute(), args.trust.absolute()
    safe_path(source)
    safe_path(trust)
    require(source.is_dir() and trust.is_file(), "SUPPLY_MISSING")
    trusted = json.loads(trust.read_bytes())
    consumer.validate_inventory(trusted)
    size = sum(x["size_bytes"] for x in trusted["files"])
    # Supply + expansion + retained input plus the bounded persistent data reservation.
    require(size * 3 <= 25 * GIB, "SUPPLY_BUDGET")
    require(
        shutil.disk_usage(root if root.exists() else root.parent).free >= 25 * GIB + size * 3,
        "INSUFFICIENT_DISK",
    )
    address = ipaddress.IPv4Address(args.bind)
    require(
        str(address) == "127.0.0.1"
        or (
            args.lan
            and address.is_private
            and not address.is_unspecified
            and not address.is_link_local
            and not address.is_multicast
        ),
        "ACCESS_MODE",
    )
    require(args.port == 0 or 1024 <= args.port <= 65535, "PORT_INVALID")
    if args.port:
        with socket.socket() as sock:
            try:
                sock.bind((str(address), args.port))
            except OSError:
                raise consumer.ConsumerError("PORT_UNAVAILABLE") from None
    data: dict[str, Any] = {
        "schema_version": SCHEMA,
        "id": "custometry-" + secrets.token_hex(12),
        "root": str(root),
        "engine": observed,
        "state": "prepared",
        "last_completed_step": "prepared",
        "failure_code": None,
        "source": str(source),
        "trust": trusted,
        "demo": args.demo,
        "bind": str(address),
        "port": args.port,
        "origin": f"https://{address}:{args.port}" if args.port else None,
        "tls_input": {
            k: str(getattr(args, k).absolute()) if getattr(args, k) else None
            for k in ("certificate", "private_key", "trust_root")
        },
        "resources": {
            "data_ceiling_bytes": 25 * GIB,
            "memory_ceiling_bytes": 6 * GIB,
            "acquisition_bytes": size,
            "disk_preflight_required": 25 * GIB + size * 3,
        },
        "images": [],
        "volumes": {},
    }
    if persist:
        atomic(root / "installation.json", data)
    return data


def prepare(root: Path, state: dict[str, Any]) -> None:
    for name in (*PRIVATE, "artifacts"):
        path = root / name
        if not path.exists():
            path.mkdir(mode=0o700)
        safe_path(path)
    names = ["control_db_password"]
    if state["demo"]:
        names += ["demo_source_admin_password", "demo_source_reader_password"]
    for name in names:
        path = root / "secrets" / name
        if not path.exists():
            require(state["last_completed_step"] == "prepared", "SECRET_MISSING")
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o444)
            with os.fdopen(fd, "w") as stream:
                stream.write(secrets.token_hex(32))
                stream.flush()
                os.fsync(stream.fileno())
        private(path, 0o444)
        require(re.fullmatch(r"[a-f0-9]{64}", path.read_text()), "SECRET_FORMAT")


def verify(acquired: Path, trusted: dict[str, Any]) -> dict[str, Any]:
    consumer.validate_inventory(trusted)
    for item in trusted["files"]:
        path = acquired / item["path"]
        safe_path(path)
        require(
            path.is_file()
            and path.stat().st_size == item["size_bytes"]
            and sha(path) == item["sha256"],
            "TRUSTED_HASH_MISMATCH",
        )
    spec = importlib.util.spec_from_file_location(
        "trusted_delivery_reader", acquired / "toolkit/tools/custometry_quality/delivery_bundle.py"
    )
    assert spec and spec.loader
    reader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reader)
    record = reader.read_record(acquired / "bundle/delivery-manifest.json", "internal-development")
    reader.check_payload(record, reader.candidate_payload(record, acquired / "bundle"))
    reader.check_image_archives(record, acquired / "images")
    return dict(record)


def acquire(root: Path, state: dict[str, Any]) -> dict[str, Any]:
    destination = root / "acquisition/current"
    if not destination.exists():
        # Interrupted temporary directories are retained, never adopted or recursively deleted.
        stage = root / "acquisition" / ("attempt-" + secrets.token_hex(8))
        consumer.checked_copy(Path(state["source"]), stage, state["trust"])
        consumer.unpack(stage / "delivery.zip", stage / "bundle")
        record = verify(stage, state["trust"])
        stage.rename(destination)
    else:
        record = verify(destination, state["trust"])
    state["version"] = record["application_version"]
    if state["demo"]:
        consumer.prepare_demo_mount(destination / "bundle")
    return record


class Runtime:
    def __init__(self, root: Path, state: dict[str, Any]):
        self.root, self.state = root, state
        self.docker = ["docker", "--context", state["engine"]["context"]]
        self.compose = self.docker + [
            "compose",
            "--project-name",
            state["id"],
            "--env-file",
            "/dev/null",
            "-f",
            str(root / "config/compose.json"),
            "--profile",
            "migration",
        ]
        if state["demo"]:
            self.compose += ["--profile", "demo"]

    def run(self, args: list[str], timeout: int = 5) -> str:
        return command(self.docker + args, timeout=timeout)

    def cp(self, args: list[str], timeout: int = 120) -> str:
        path = self.root / "config/compose.json"
        private(path, 0o600)
        require(sha(path) == self.state.get("config_sha256"), "CONFIG_CHANGED")
        return command(self.compose + args, timeout=timeout)

    def ownership(self) -> None:
        # Inspect before every mutation, including stop. Never adopt a name-only match.
        for kind, label_key in (("volume", "volume"), ("network", "network")):
            expected = self.state.get("volumes" if kind == "volume" else "networks", {})
            for name in expected:
                full = self.state["id"] + "_" + name
                existing = self.run([kind, "ls", "--format", "{{.Name}}"]).splitlines()
                if full not in existing:
                    continue
                item = json.loads(self.run([kind, "inspect", full]))[0]
                labels: dict[str, Any] = item.get("Labels") or {}
                require(
                    labels.get("com.docker.compose.project") == self.state["id"]
                    and labels.get("com.docker.compose." + label_key) == name
                    and labels.get("io.custometry.installation") == self.state["id"],
                    "FOREIGN_RESOURCE",
                )
        ids = self.run(
            ["ps", "-aq", "--filter", "label=com.docker.compose.project=" + self.state["id"]]
        ).splitlines()
        if ids:
            for item in json.loads(self.run(["inspect", *ids])):
                labels = dict(item["Config"].get("Labels") or {})
                require(
                    labels.get("io.custometry.installation") == self.state["id"], "FOREIGN_RESOURCE"
                )

    def import_images(self, record: dict[str, Any]) -> None:
        items = [
            i
            for i in record["retrieval"]["archives"]
            if i["architecture"] == self.state["engine"]["architecture"]
        ]
        require({i["role"] for i in items} == {"api", "web", "postgres"}, "PLATFORM_UNAVAILABLE")
        unpacked = sum(
            p["unpacked_bytes"]
            for image in record["images"].values()
            for p in image["platforms"]
            if p["architecture"] == self.state["engine"]["architecture"]
        )
        retained = sum(
            p.stat().st_size for p in (self.root / "acquisition").rglob("*") if p.is_file()
        )
        require(retained + unpacked < 25 * GIB, "OWNED_DATA_LIMIT")
        require(shutil.disk_usage(self.root).free >= 25 * GIB + unpacked, "INSUFFICIENT_DISK")
        self.state["resources"].update(
            retained_acquisition_bytes=retained,
            native_unpacked_image_bytes=unpacked,
            artifact_temporary_reserve_bytes=GIB,
        )
        for item in items:
            try:
                info = json.loads(self.run(["image", "inspect", item["docker_id"]]))[0]
            except consumer.ConsumerError:
                self.run(
                    [
                        "load",
                        "--input",
                        str(self.root / "acquisition/current/images" / item["path"]),
                    ],
                    600,
                )
                info = json.loads(self.run(["image", "inspect", item["docker_id"]]))[0]
            require(
                info["Architecture"] == item["architecture"] and info["Id"] == item["docker_id"],
                "IMPORTED_IDENTITY",
            )
        self.state["images"] = items

    def configure(self) -> None:
        bundle = self.root / "acquisition/current/bundle"
        config = json.loads((bundle / "compose.json").read_bytes())
        config["name"] = self.state["id"]
        images = {i["role"]: i["docker_id"] for i in self.state["images"]}
        if not self.state["demo"]:
            del config["services"]["demo-source-db"]
            del config["volumes"]["demo_source_data"]
            del config["networks"]["demo_source"]
            for key in ("demo_source_admin_password", "demo_source_reader_password"):
                del config["secrets"][key]
        roles = {
            "control-db": "postgres",
            "demo-source-db": "postgres",
            "api": "api",
            "migrate": "api",
            "web": "web",
            "edge": "web",
        }
        budget = self.state["engine"]["cpu_cap"]
        total = sum(float(s["cpus"]) for s in config["services"].values())
        for name, service in config["services"].items():
            service["image"] = images[roles[name]]
            require("build" not in service and service["pull_policy"] == "never", "BUILD_OR_PULL")
            service["cpus"] = str(round(float(service["cpus"]) * min(1, budget / total), 3))
            service["labels"] = {"io.custometry.installation": self.state["id"]}
            service["ports"] = []  # No HTTP fallback or installed ingress before S02.
            if name == "demo-source-db":
                service["volumes"][1] = (
                    str(bundle / "demo/init") + ":/docker-entrypoint-initdb.d:ro"
                )
        excess = round(sum(float(s["cpus"]) for s in config["services"].values()) - budget, 3)
        if excess > 0:
            service = config["services"]["control-db"]
            service["cpus"] = str(round(float(service["cpus"]) - excess, 3))
        config["services"]["api"]["volumes"] = [
            str(self.root / "artifacts") + ":/var/lib/custometry/artifacts"
        ]
        for name in config["secrets"]:
            config["secrets"][name] = {"file": str(self.root / "secrets" / name)}
        for kind in ("volumes", "networks"):
            for value in config[kind].values():
                value["labels"] = {"io.custometry.installation": self.state["id"]}
            self.state[kind] = {
                name: {
                    "com.docker.compose.project": self.state["id"],
                    "com.docker.compose." + kind[:-1]: name,
                    "io.custometry.installation": self.state["id"],
                }
                for name in config[kind]
            }
        candidate = self.root / "config/compose.json"
        if candidate.exists():
            require(json.loads(candidate.read_bytes()) == config, "CONFIG_CHANGED")
        else:
            atomic(candidate, config)
        self.state["config_sha256"] = sha(candidate)
        resolved = json.loads(self.cp(["config", "--format", "json"]))
        require(
            sum(int(s["mem_limit"]) for s in resolved["services"].values()) <= 6 * GIB,
            "MEMORY_LIMIT",
        )
        require(sum(float(s["cpus"]) for s in resolved["services"].values()) <= budget, "CPU_LIMIT")
        self.state["resources"]["configured_memory_bytes"] = sum(
            int(s["mem_limit"]) for s in resolved["services"].values()
        )

    def database_head(self) -> str:
        exists = self.cp(
            [
                "exec",
                "-T",
                "control-db",
                "psql",
                "-U",
                "custometry",
                "-d",
                "custometry",
                "-At",
                "-c",
                "SELECT to_regclass('public.alembic_version') IS NOT NULL;",
            ],
            5,
        )
        if exists == "f":
            return "empty"
        require(exists == "t", "SCHEMA_UNRECOGNIZED")
        return self.cp(
            [
                "exec",
                "-T",
                "control-db",
                "psql",
                "-U",
                "custometry",
                "-d",
                "custometry",
                "-At",
                "-c",
                "SELECT version_num FROM alembic_version;",
            ],
            5,
        )

    def migrate(self) -> None:
        self.ownership()
        # A timed-out Compose client may leave its one-shot job alive.
        active = self.run(
            [
                "ps",
                "-q",
                "--filter",
                "label=com.docker.compose.project=" + self.state["id"],
                "--filter",
                "label=com.docker.compose.service=migrate",
            ]
        )
        require(not active, "MIGRATION_RUNNING")
        databases = ["control-db"] + (["demo-source-db"] if self.state["demo"] else [])
        self.cp(["up", "-d", "--no-build", "--wait", "--wait-timeout", "120", *databases], 130)
        deadline = time.monotonic() + 120
        while True:
            try:
                self.cp(
                    [
                        "exec",
                        "-T",
                        "control-db",
                        "pg_isready",
                        "-h",
                        "127.0.0.1",
                        "-t",
                        "2",
                        "-U",
                        "custometry",
                        "-d",
                        "custometry",
                    ],
                    5,
                )
                break
            except consumer.ConsumerError:
                require(time.monotonic() < deadline, "DATABASE_TIMEOUT")
                time.sleep(2)
        current = self.database_head()
        require(current in ("empty", HEAD), "SCHEMA_FORWARD_REPAIR_REQUIRED")
        if current == "empty":
            self.cp(["run", "--rm", "--no-deps", "migrate"], 600)
        require(self.database_head() == HEAD, "MIGRATION_HEAD")
        self.state["migration_head"] = HEAD
        # Prepare only the fixed artifact mount using the existing API runtime UID.
        image = next(i["docker_id"] for i in self.state["images"] if i["role"] == "api")
        uid = self.run(["run", "--rm", "--network", "none", "--entrypoint", "id", image, "-u"], 30)
        require(uid.isdigit() and uid != "0", "ARTIFACT_UID")
        self.run(
            [
                "run",
                "--rm",
                "--network",
                "none",
                "--user",
                "0",
                "--entrypoint",
                "sh",
                "--mount",
                "type=bind,src=" + str(self.root / "artifacts") + ",dst=/owned",
                image,
                "-c",
                "chown " + uid + " /owned && chmod 700 /owned",
            ],
            30,
        )
        self.state["artifact_uid"] = int(uid)


def status(root: Path, data: dict[str, Any], runtime: Runtime) -> dict[str, Any]:
    runtime.ownership()
    code = data.get("failure_code") or "HTTPS_NOT_IMPLEMENTED"
    if data["last_completed_step"] == "migrated" and data["state"] != "stopped":
        try:
            if runtime.database_head() != HEAD:
                code = "SCHEMA_INCOMPATIBLE"
        except consumer.ConsumerError:
            code = "DATABASE_UNAVAILABLE"
    return {
        "schema_version": SCHEMA,
        "installation_id": data["id"],
        "state": data["state"],
        "last_completed_step": data["last_completed_step"],
        "ready": False,
        "code": code,
        "version": data.get("version"),
        "url": None,
        "next_action": "resume"
        if data["state"] in ("failed", "stopped")
        else "configure_https_in_s02",
    }


def execute(args: argparse.Namespace) -> dict[str, Any]:
    require(sys.version_info[:2] == (3, 12), "PYTHON_312_REQUIRED")
    root = args.root.absolute()
    safe_path(root)
    candidate = None
    if args.action == "install" and not (root / "installation.json").exists():
        if root.exists():
            private(root)
            require(not list(root.iterdir()), "FOREIGN_ROOT")
        candidate = initial(root, args, engine(), persist=False)
    with locked(root, args.action == "install"):
        if (root / "installation.json").exists():
            data = read_state(root)
            observed = engine(data["engine"]["context"])
            same_engine(data["engine"], observed)
        else:
            require(candidate is not None, "STATE_MISSING")
            data = dict(candidate or {})
            atomic(root / "installation.json", data)
        runtime = Runtime(root, data)
        if args.action == "status":
            return status(root, data, runtime)
        try:
            if args.action == "stop":
                runtime.ownership()
                if (root / "config/compose.json").exists():
                    require(
                        sha(root / "config/compose.json") == data.get("config_sha256"),
                        "CONFIG_CHANGED",
                    )
                    runtime.cp(["stop"], 120)
                data.update(state="stopped", failure_code=None)
                atomic(root / "installation.json", data)
            else:
                require(args.port in (0, data["port"]), "SAVED_ORIGIN_MISMATCH")
                require(not args.demo or data["demo"], "SAVED_DEMO_MISMATCH")
                require(
                    args.bind == "127.0.0.1" or args.bind == data["bind"], "SAVED_ORIGIN_MISMATCH"
                )
                require(shutil.disk_usage(root).free >= 25 * GIB, "INSUFFICIENT_DISK")
                prepare(root, data)
                record = acquire(root, data)
                runtime.import_images(record)
                runtime.configure()
                checkpoint(root, data, "acquired")
                runtime.migrate()
                checkpoint(root, data, "migrated")
        except Exception as error:
            data["state"] = "failed"
            data["failure_code"] = (
                str(error) if isinstance(error, consumer.ConsumerError) else "INSTALLATION_FAILED"
            )
            atomic(root / "installation.json", data)
            raise
        return status(root, data, runtime)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, prog="custometry-install")
    parser.add_argument("action", choices=("install", "status", "resume", "stop"))
    parser.add_argument("--root", type=Path)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--trust", type=Path)
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--lan", action="store_true")
    parser.add_argument("--bind", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=0)
    for name in ("certificate", "private-key", "trust-root"):
        parser.add_argument("--" + name, type=Path)
    args = parser.parse_args()
    try:
        if args.root is None and sys.stdin.isatty():
            args.root = Path(input("Installation directory: "))
        if args.root is None:
            raise consumer.ConsumerError("ROOT_REQUIRED")
        if args.action == "install" and not (args.root / "installation.json").exists():
            for key, label in (
                ("source", "Protected supply directory"),
                ("trust", "Independent inventory file"),
            ):
                if getattr(args, key) is None and sys.stdin.isatty():
                    setattr(args, key, Path(input(label + ": ")))
            require(args.source is not None and args.trust is not None, "SUPPLY_REQUIRED")
        result = execute(args)
    except Exception as error:
        code = str(error) if isinstance(error, consumer.ConsumerError) else "INSTALLATION_FAILED"
        print(json.dumps({"status": "failed", "code": code, "ready": False}))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
