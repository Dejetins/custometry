from __future__ import annotations

import argparse
import json
import os
import re
import secrets
import shutil
import socket
import subprocess
import tempfile
import time
import uuid
from dataclasses import dataclass
from http.client import HTTPException
from pathlib import Path
from typing import Callable, Sequence, cast
from urllib.request import ProxyHandler, build_opener

from .core import (
    CheckResult,
    JsonObject,
    JsonValue,
    add_common_arguments,
    add_command_failure,
    json_integer,
    json_list,
    json_number,
    json_object,
    json_string,
    load_json,
    load_yaml,
    main_guard,
    render_result,
    require_file,
    run_command,
    string_list,
)


@dataclass(frozen=True, slots=True)
class NegativeEgressProbe:
    preflight: tuple[str, ...]
    external: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RuntimePolicy:
    public_services: dict[str, int]
    public_health_paths: dict[str, str]
    internal_networks: set[str]
    edge_networks: set[str]
    edge_allowlist: set[str]
    edge_service: str
    web_service: str
    api_service: str
    edge_to_web_network: str
    web_to_api_network: str
    web_target: str
    api_target: str
    edge_proxy_source: Path
    edge_upstream_name: str
    ingress_allowed_probe: tuple[str, ...]
    ingress_denied_probe: tuple[str, ...]
    egress_networks: set[str]
    egress_allowlist: set[str]
    negative_egress_probes: dict[str, NegativeEgressProbe]
    max_runtime_memory_gib: float
    database_services: tuple[str, ...]
    migration_service: str
    application_services: tuple[str, ...]
    profiles: tuple[str, ...]


def _service_target(value: JsonValue, label: str, expected_service: str) -> str:
    target = json_string(value, label)
    match = re.fullmatch(r"([a-zA-Z0-9][a-zA-Z0-9_.-]*):([1-9]\d{0,4})", target)
    if match is None:
        raise ValueError(f"{label} must be a service:port target")
    service, raw_port = match.groups()
    if service != expected_service:
        raise ValueError(f"{label} must target declared service {expected_service}")
    if int(raw_port) > 65535:
        raise ValueError(f"{label} port must be within 1..65535")
    return target


def _policy(data: JsonObject) -> RuntimePolicy:
    if data.get("schema_version") != 2:
        raise ValueError("runtime policy requires schema_version=2")
    public_raw = json_object(data.get("public_services"), "public_services")
    if not public_raw:
        raise ValueError("public_services must be a non-empty service -> target-port mapping")
    public: dict[str, int] = {}
    for name, value in public_raw.items():
        port = json_integer(value, f"public_services.{name}")
        if not 1 <= port <= 65535:
            raise ValueError(f"public_services.{name} must be a valid port")
        public[name] = port
    if len(public) != 1:
        raise ValueError("Foundation runtime policy requires exactly one public edge service")
    health_raw = json_object(data.get("public_health_paths"), "public_health_paths")
    if set(health_raw) != set(public):
        raise ValueError("public_health_paths keys must exactly match public_services")
    health_paths: dict[str, str] = {}
    for name, value in health_raw.items():
        path = json_string(value, f"public_health_paths.{name}")
        if not path.startswith("/") or path.startswith("//"):
            raise ValueError(f"public_health_paths.{name} must be an absolute HTTP path")
        health_paths[name] = path
    internal_networks = set(string_list(data.get("internal_networks"), "internal_networks"))
    edge_networks = set(string_list(data.get("edge_networks"), "edge_networks", non_empty=True))
    if len(edge_networks) != 1:
        raise ValueError("Foundation runtime policy requires exactly one ingress edge network")
    edge_allowlist = set(string_list(data.get("edge_allowlist"), "edge_allowlist", non_empty=True))
    egress_networks = set(string_list(data.get("egress_networks"), "egress_networks"))
    egress_allowlist = set(string_list(data.get("egress_allowlist"), "egress_allowlist"))
    network_classes = (internal_networks, edge_networks, egress_networks)
    if any(
        left.intersection(right)
        for index, left in enumerate(network_classes)
        for right in network_classes[index + 1 :]
    ):
        raise ValueError("internal, edge, and business-egress network classes must be disjoint")
    if edge_allowlist != set(public):
        raise ValueError("edge_allowlist must exactly match the declared public edge service")
    ingress_path = json_object(data.get("ingress_path"), "ingress_path")
    ingress_path_fields = {
        "edge_service",
        "web_service",
        "api_service",
        "edge_to_web_network",
        "web_to_api_network",
        "web_target",
        "api_target",
    }
    if set(ingress_path) != ingress_path_fields:
        raise ValueError(
            "ingress_path must contain exactly edge_service, web_service, api_service, "
            "edge_to_web_network, web_to_api_network, web_target, and api_target"
        )
    edge_service = json_string(ingress_path.get("edge_service"), "ingress_path.edge_service")
    web_service = json_string(ingress_path.get("web_service"), "ingress_path.web_service")
    api_service = json_string(ingress_path.get("api_service"), "ingress_path.api_service")
    edge_to_web_network = json_string(
        ingress_path.get("edge_to_web_network"),
        "ingress_path.edge_to_web_network",
    )
    web_to_api_network = json_string(
        ingress_path.get("web_to_api_network"),
        "ingress_path.web_to_api_network",
    )
    web_target = _service_target(
        ingress_path.get("web_target"),
        "ingress_path.web_target",
        web_service,
    )
    api_target = _service_target(
        ingress_path.get("api_target"),
        "ingress_path.api_target",
        api_service,
    )
    if len({edge_service, web_service, api_service}) != 3:
        raise ValueError("ingress_path service identities must be distinct")
    if edge_service not in public or edge_service not in edge_allowlist:
        raise ValueError("ingress_path.edge_service must be the declared public edge service")
    if edge_to_web_network == web_to_api_network:
        raise ValueError("ingress_path internal network identities must be distinct")
    if {edge_to_web_network, web_to_api_network} - internal_networks:
        raise ValueError("ingress_path networks must both be classified as internal")
    edge_proxy_contract = json_object(
        data.get("edge_proxy_contract"),
        "edge_proxy_contract",
    )
    if set(edge_proxy_contract) != {"source", "upstream_name"}:
        raise ValueError("edge_proxy_contract must contain exactly source and upstream_name")
    edge_proxy_source_raw = json_string(
        edge_proxy_contract.get("source"),
        "edge_proxy_contract.source",
    )
    edge_proxy_source = Path(edge_proxy_source_raw)
    if (
        edge_proxy_source.is_absolute()
        or ".." in edge_proxy_source.parts
        or edge_proxy_source.as_posix() != edge_proxy_source_raw
    ):
        raise ValueError("edge_proxy_contract.source must be a normalized repository-relative path")
    edge_upstream_name = json_string(
        edge_proxy_contract.get("upstream_name"),
        "edge_proxy_contract.upstream_name",
    )
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", edge_upstream_name) is None:
        raise ValueError("edge_proxy_contract.upstream_name must be a static Nginx identifier")
    isolation_raw = json_object(
        data.get("ingress_isolation_probes"),
        "ingress_isolation_probes",
    )
    if set(isolation_raw) != {"allowed", "denied"}:
        raise ValueError("ingress_isolation_probes must contain exactly allowed and denied")
    ingress_allowed_probe = tuple(
        string_list(
            isolation_raw.get("allowed"),
            "ingress_isolation_probes.allowed",
            non_empty=True,
        )
    )
    ingress_denied_probe = tuple(
        string_list(
            isolation_raw.get("denied"),
            "ingress_isolation_probes.denied",
            non_empty=True,
        )
    )
    if ingress_allowed_probe == ingress_denied_probe:
        raise ValueError("ingress isolation allowed and denied commands must differ")
    allowed_urls = [
        token for token in ingress_allowed_probe if token.startswith(("http://", "https://"))
    ]
    denied_urls = [
        token for token in ingress_denied_probe if token.startswith(("http://", "https://"))
    ]
    if allowed_urls != [f"http://{web_target}/health/live"]:
        raise ValueError(
            "ingress_isolation_probes.allowed must target the declared Web health endpoint"
        )
    if denied_urls != [f"http://{api_target}/health/live"]:
        raise ValueError(
            "ingress_isolation_probes.denied must target the declared API health endpoint"
        )
    max_runtime_memory_gib = json_number(
        data.get("max_runtime_memory_gib"), "max_runtime_memory_gib"
    )
    if max_runtime_memory_gib <= 0:
        raise ValueError("max_runtime_memory_gib must be positive")
    lifecycle = json_object(data.get("lifecycle"), "lifecycle")
    database_services = tuple(
        string_list(
            lifecycle.get("database_services"), "lifecycle.database_services", non_empty=True
        )
    )
    migration_service = json_string(
        lifecycle.get("migration_service"), "lifecycle.migration_service"
    )
    application_services = tuple(
        string_list(
            lifecycle.get("application_services"),
            "lifecycle.application_services",
            non_empty=True,
        )
    )
    profiles = tuple(string_list(lifecycle.get("profiles"), "lifecycle.profiles", non_empty=True))
    probe_raw = json_object(data.get("negative_egress_probes"), "negative_egress_probes")
    if set(probe_raw) != {api_service, web_service}:
        raise ValueError(
            "negative_egress_probes must contain exactly ingress_path api_service and web_service"
        )
    probes: dict[str, NegativeEgressProbe] = {}
    for service_name, raw_probe in probe_raw.items():
        probe = json_object(raw_probe, f"negative_egress_probes.{service_name}")
        preflight = tuple(
            string_list(
                probe.get("preflight"),
                f"negative_egress_probes.{service_name}.preflight",
                non_empty=True,
            )
        )
        external = tuple(
            string_list(
                probe.get("external"),
                f"negative_egress_probes.{service_name}.external",
                non_empty=True,
            )
        )
        if preflight == external:
            raise ValueError(
                f"negative_egress_probes.{service_name} preflight and external commands must differ"
            )
        probes[service_name] = NegativeEgressProbe(preflight=preflight, external=external)
    if not set(probes).issubset(application_services) or set(probes).intersection(public):
        raise ValueError("negative egress probes must target non-public application services")
    return RuntimePolicy(
        public_services=public,
        public_health_paths=health_paths,
        internal_networks=internal_networks,
        edge_networks=edge_networks,
        edge_allowlist=edge_allowlist,
        edge_service=edge_service,
        web_service=web_service,
        api_service=api_service,
        edge_to_web_network=edge_to_web_network,
        web_to_api_network=web_to_api_network,
        web_target=web_target,
        api_target=api_target,
        edge_proxy_source=edge_proxy_source,
        edge_upstream_name=edge_upstream_name,
        ingress_allowed_probe=ingress_allowed_probe,
        ingress_denied_probe=ingress_denied_probe,
        egress_networks=egress_networks,
        egress_allowlist=egress_allowlist,
        negative_egress_probes=probes,
        max_runtime_memory_gib=max_runtime_memory_gib,
        database_services=database_services,
        migration_service=migration_service,
        application_services=application_services,
        profiles=profiles,
    )


EPHEMERAL_PORT = re.compile(r"^\$\{[A-Z][A-Z0-9_]*:-0\}$")
LOOPBACK_HOST = re.compile(r"^\$\{[A-Z][A-Z0-9_]*:-(?:127\.0\.0\.1|::1)\}$")
MEMORY = re.compile(r"^(\d+(?:\.\d+)?)\s*([kmgt]?)(?:i?b)?$", re.IGNORECASE)
BIND_VISIBILITY_RETRY_DELAYS = (0.25, 0.75, 1.5)


def _port_binding(binding: JsonValue) -> tuple[str | None, int | str | None, int]:
    item = json_object(binding, "port binding (Compose long syntax)")
    raw_host = item.get("host_ip")
    host_ip = raw_host if isinstance(raw_host, str) else None
    raw_published = item.get("published")
    if raw_published is None:
        published: int | str | None = None
    elif isinstance(raw_published, str) and EPHEMERAL_PORT.fullmatch(raw_published):
        published = raw_published
    else:
        published = json_integer(raw_published, "published")
    target = json_integer(item.get("target"), "target")
    return host_ip, published, target


def _memory_bytes(value: JsonValue, label: str) -> int:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return int(value)
    if not isinstance(value, str):
        raise ValueError(f"{label} must be a Compose memory size")
    match = MEMORY.fullmatch(value.strip())
    if not match:
        raise ValueError(f"{label} has invalid memory size: {value}")
    amount, unit = float(match.group(1)), match.group(2).lower()
    power = {"": 0, "k": 1, "m": 2, "g": 3, "t": 4}[unit]
    return int(amount * (1024**power))


def _volume_is_read_only(value: JsonValue) -> bool:
    if isinstance(value, str):
        parts = value.split(":")
        return len(parts) >= 3 and "ro" in parts[-1].split(",")
    item = json_object(value, "volume")
    return item.get("read_only") is True or item.get("type") == "tmpfs"


def _environment_names(value: JsonValue) -> set[str]:
    if value is None:
        return set()
    if isinstance(value, dict):
        return set(json_object(value, "environment"))
    items = json_list(value, "environment")
    names: set[str] = set()
    for item in items:
        if not isinstance(item, str):
            raise ValueError("environment list entries must be strings")
        names.add(item.split("=", 1)[0])
    return names


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _write_atomic_private(path: Path, content: str) -> None:
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        with temporary.open("x", encoding="utf-8") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.chmod(0o600)
        os.replace(temporary, path)
        path.chmod(0o600)
        _fsync_directory(path.parent)
    finally:
        temporary.unlink(missing_ok=True)


def _is_bind_visibility_failure(completed: subprocess.CompletedProcess[str]) -> bool:
    output = f"{completed.stdout}\n{completed.stderr}".lower()
    return "invalid mount config" in output and "bind source path does not exist" in output


def decode_compose_ps_records(output: str) -> list[dict[str, object]]:
    text = output.strip()
    if not text:
        raise ValueError("docker compose ps returned empty output")

    def records_from(value: object) -> list[dict[str, object]]:
        if isinstance(value, dict):
            return [cast(dict[str, object], value)]
        if isinstance(value, list):
            items = cast(list[object], value)
            if all(isinstance(item, dict) for item in items):
                return cast(list[dict[str, object]], items)
        raise ValueError("docker compose ps JSON must contain objects")

    try:
        return records_from(cast(object, json.loads(text)))
    except json.JSONDecodeError:
        records: list[dict[str, object]] = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            try:
                decoded = cast(object, json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"docker compose ps NDJSON line {line_number} is invalid") from exc
            records.extend(records_from(decoded))
        if not records:
            raise ValueError("docker compose ps returned no service records")
        return records


def select_runtime_port(_project_name: str) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("127.0.0.1", 0))
        port = int(probe.getsockname()[1])
    if port < 1024:
        raise ValueError("operating system selected a privileged port")
    return port


def _port_is_available(port: int) -> bool:
    if not 1024 <= port <= 65535:
        return False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        try:
            probe.bind(("127.0.0.1", port))
        except OSError:
            return False
    return True


def _mapped_port(output: str) -> tuple[str, int]:
    value = output.strip().splitlines()[0] if output.strip() else ""
    match = re.fullmatch(r"(?:127\.0\.0\.1|localhost):(\d{1,5})", value)
    if not match:
        match = re.fullmatch(r"\[::1\]:(\d{1,5})", value)
    if not match:
        raise ValueError(f"not a loopback host mapping: {value!r}")
    port = int(match.group(1))
    if not 1024 <= port <= 65535:
        raise ValueError(f"mapped port is outside 1024..65535: {port}")
    return value.rsplit(":", 1)[0], port


def probe_http_status(url: str, timeout: float) -> int:
    opener = build_opener(ProxyHandler({}))
    with opener.open(url, timeout=timeout) as response:  # noqa: S310 - policy-built loopback URL
        response.read(1)
        return int(response.status)


def _check_edge_proxy_source(
    root: Path,
    config: RuntimePolicy,
    result: CheckResult,
) -> None:
    source_path = root / config.edge_proxy_source
    if not source_path.is_file():
        result.add(
            "edge-proxy-source-missing",
            f"declared Edge proxy source is absent: {config.edge_proxy_source}",
            source_path,
        )
        return
    try:
        source = source_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        result.add(
            "edge-proxy-source-unreadable",
            f"could not read declared Edge proxy source: {exc}",
            source_path,
        )
        return

    if re.search(r"(?m)^\s*resolver\s+[^;]+;", source):
        result.add(
            "edge-nginx-resolver-forbidden",
            "Edge proxy source must not define a dynamic Nginx resolver",
            source_path,
        )

    upstream_names = re.findall(
        r"(?m)^\s*upstream\s+([A-Za-z_][A-Za-z0-9_]*)\s*\{",
        source,
    )
    if upstream_names != [config.edge_upstream_name]:
        result.add(
            "edge-upstream-name-drift",
            f"Edge upstreams must be exactly [{config.edge_upstream_name!r}]; "
            f"got {upstream_names!r}",
            source_path,
        )

    upstream_targets = re.findall(
        r"(?m)^\s*server\s+([^;\s]+)\s*;",
        source,
    )
    if upstream_targets != [config.web_target]:
        result.add(
            "edge-upstream-target-drift",
            f"Edge upstream targets must be exactly [{config.web_target!r}]; "
            f"got {upstream_targets!r}",
            source_path,
        )

    proxy_targets = re.findall(
        r"(?m)^\s*proxy_pass\s+([^;\s]+)\s*;",
        source,
    )
    expected_proxy_target = f"http://{config.edge_upstream_name}"
    if not proxy_targets or any(target != expected_proxy_target for target in proxy_targets):
        result.add(
            "edge-proxy-pass-drift",
            f"every Edge proxy_pass must target {expected_proxy_target!r}; got {proxy_targets!r}",
            source_path,
        )


def static_check(root: Path, compose: Path, policy: Path) -> CheckResult:
    result = CheckResult("compose_lifecycle")
    compose_path, policy_path = root / compose, root / policy
    if not require_file(compose_path, result) or not require_file(policy_path, result):
        return result
    try:
        document = load_yaml(compose_path)
        config = _policy(load_json(policy_path))
    except ValueError as exc:
        result.add("compose-contract-invalid", str(exc))
        return result
    _check_edge_proxy_source(root, config, result)
    try:
        services = json_object(document.get("services"), "services")
    except ValueError as exc:
        result.observed = False
        result.add("compose-services-missing", str(exc), compose_path)
        return result
    if not services:
        result.observed = False
        result.add(
            "compose-services-missing", "Compose must define at least one service", compose_path
        )
        return result
    lifecycle_services = {
        *config.database_services,
        config.migration_service,
        *config.application_services,
    }
    for service_name in sorted(lifecycle_services - set(services)):
        result.add(
            "lifecycle-service-missing",
            f"runtime lifecycle references undefined service {service_name}",
            policy_path,
        )
    if not set(config.public_services).issubset(config.application_services):
        result.add(
            "public-service-lifecycle-missing",
            "every public service must be started in lifecycle.application_services",
            policy_path,
        )
    raw_networks = document.get("networks")
    try:
        networks = json_object(raw_networks, "networks") if raw_networks is not None else {}
    except ValueError:
        result.add("compose-networks-invalid", "networks must be a mapping", compose_path)
        networks = {}
    declared_networks = config.internal_networks | config.edge_networks | config.egress_networks
    for network in sorted(declared_networks - set(networks)):
        result.add(
            "policy-network-missing",
            f"runtime policy classifies undefined network {network}",
            policy_path,
        )
    classified_networks = declared_networks
    for network in sorted(set(networks) - classified_networks):
        result.add(
            "network-unclassified",
            f"network {network} must be classified as internal, edge, or business egress",
            compose_path,
        )
    for network in config.internal_networks:
        raw_network = networks.get(network)
        try:
            network_config = (
                json_object(raw_network, f"networks.{network}") if raw_network is not None else {}
            )
        except ValueError as exc:
            result.add("compose-network-invalid", str(exc), compose_path)
            continue
        if network_config.get("internal") is not True:
            result.add(
                "internal-network-unsealed",
                f"network {network} must set internal: true",
                compose_path,
            )
    for network in config.edge_networks:
        raw_network = networks.get(network)
        try:
            network_config = (
                json_object(raw_network, f"networks.{network}") if raw_network is not None else {}
            )
        except ValueError as exc:
            result.add("compose-network-invalid", str(exc), compose_path)
            continue
        if network_config.get("internal") is not False:
            result.add(
                "edge-network-not-explicit",
                f"edge network {network} must explicitly set internal: false",
                compose_path,
            )
    aggregate_memory = 0
    public_binding_count = 0
    service_networks: dict[str, set[str]] = {}
    for service_name, raw_service in services.items():
        try:
            service = json_object(raw_service, f"services.{service_name}")
        except ValueError:
            result.add(
                "compose-service-invalid", f"service {service_name} must be a mapping", compose_path
            )
            continue
        if service.get("privileged") is True or service.get("network_mode") == "host":
            result.add(
                "unsafe-container-privilege",
                f"service {service_name} uses privileged/host networking",
                compose_path,
            )
        raw_memory = service.get("mem_limit")
        if raw_memory is None:
            result.add(
                "service-memory-limit-missing",
                f"service {service_name} has no mem_limit",
                compose_path,
            )
        else:
            try:
                aggregate_memory += _memory_bytes(raw_memory, f"services.{service_name}.mem_limit")
            except ValueError as exc:
                result.add("service-memory-limit-invalid", str(exc), compose_path)
        raw_volumes = service.get("volumes")
        try:
            volumes = (
                json_list(raw_volumes, f"services.{service_name}.volumes") if raw_volumes else []
            )
        except ValueError as exc:
            result.add("compose-volumes-invalid", str(exc), compose_path)
            volumes = []
        if any("/var/run/docker.sock" in str(volume) for volume in volumes):
            result.add(
                "docker-socket-mounted",
                f"service {service_name} mounts Docker socket",
                compose_path,
            )
        raw_attached = service.get("networks")
        if raw_attached is None:
            attached_names: set[str] = set()
        elif isinstance(raw_attached, list):
            try:
                attached_names = set(string_list(raw_attached, f"services.{service_name}.networks"))
            except ValueError as exc:
                result.add("compose-service-networks-invalid", str(exc), compose_path)
                attached_names = set()
        else:
            try:
                attached_names = set(json_object(raw_attached, f"services.{service_name}.networks"))
            except ValueError as exc:
                result.add("compose-service-networks-invalid", str(exc), compose_path)
                attached_names = set()
        undefined_attached = sorted(attached_names - set(networks))
        service_networks[service_name] = attached_names
        if undefined_attached:
            result.add(
                "service-network-undefined",
                f"service {service_name} references undefined networks: {undefined_attached}",
                compose_path,
            )
        if (
            attached_names.intersection(config.egress_networks)
            and service_name not in config.egress_allowlist
        ):
            result.add(
                "egress-not-allowlisted",
                f"service {service_name} is attached to egress network",
                compose_path,
            )
        attached_edge = attached_names.intersection(config.edge_networks)
        if attached_edge and service_name not in config.edge_allowlist:
            result.add(
                "edge-network-not-allowlisted",
                f"non-public service {service_name} is attached to edge network",
                compose_path,
            )
        if service_name in config.edge_allowlist:
            if len(attached_edge) != 1:
                result.add(
                    "edge-network-attachment-invalid",
                    f"public edge {service_name} must attach to exactly one edge network",
                    compose_path,
                )
            expected_edge_networks = {
                config.edge_to_web_network,
                *config.edge_networks,
            }
            if attached_names != expected_edge_networks:
                result.add(
                    "edge-network-scope-invalid",
                    f"public edge {service_name} networks must be exactly {sorted(expected_edge_networks)}",
                    compose_path,
                )
            if attached_names.intersection(config.egress_networks):
                result.add(
                    "edge-business-egress-forbidden",
                    f"public edge {service_name} must not attach to a business-egress network",
                    compose_path,
                )
            if service.get("read_only") is not True:
                result.add(
                    "edge-root-filesystem-writable",
                    f"public edge {service_name} must set read_only: true",
                    compose_path,
                )
            if service.get("secrets"):
                result.add(
                    "edge-secret-mounted",
                    f"public edge {service_name} must remain secretless",
                    compose_path,
                )
            if service.get("env_file"):
                result.add(
                    "edge-env-file-forbidden",
                    f"public edge {service_name} must not load an env_file",
                    compose_path,
                )
            environment_names: set[str]
            try:
                environment_names = _environment_names(service.get("environment"))
            except ValueError as exc:
                result.add("compose-environment-invalid", f"{service_name}: {exc}", compose_path)
                environment_names = set[str]()
            if environment_names:
                result.add(
                    "edge-environment-forbidden",
                    f"public edge {service_name} must not accept environment overrides",
                    compose_path,
                )
            for resolver_field in ("dns", "dns_search", "extra_hosts"):
                if service.get(resolver_field):
                    result.add(
                        "edge-custom-resolver-forbidden",
                        f"public edge {service_name} must not set {resolver_field}",
                        compose_path,
                    )
            raw_command = service.get("command")
            command: list[str] = []
            if isinstance(raw_command, list):
                try:
                    command = string_list(raw_command, f"services.{service_name}.command")
                except ValueError as exc:
                    result.add("compose-command-invalid", str(exc), compose_path)
            expected_edge_command = [
                "nginx",
                "-c",
                "/etc/nginx/edge.conf",
                "-g",
                "daemon off;",
            ]
            if command != expected_edge_command:
                result.add(
                    "edge-fixed-proxy-command-missing",
                    f"public edge {service_name} must run the exact baked fixed proxy command",
                    compose_path,
                )
            if service.get("build"):
                result.add(
                    "edge-independent-build-forbidden",
                    f"public edge {service_name} must reuse the immutable Web artifact",
                    compose_path,
                )
            web_service = services.get(config.web_service)
            if isinstance(web_service, dict) and service.get("image") != web_service.get("image"):
                result.add(
                    "edge-web-artifact-drift",
                    f"public edge {service_name} must reuse the Web image",
                    compose_path,
                )
            if volumes or service.get("configs"):
                result.add(
                    "edge-artifact-override-forbidden",
                    f"public edge {service_name} must not mount volumes or configs",
                    compose_path,
                )
            for volume in volumes:
                try:
                    read_only = _volume_is_read_only(volume)
                except ValueError as exc:
                    result.add("compose-volume-invalid", f"{service_name}: {exc}", compose_path)
                    continue
                if not read_only:
                    result.add(
                        "edge-writable-volume-forbidden",
                        f"public edge {service_name} has a writable volume mount",
                        compose_path,
                    )
        if service_name in config.negative_egress_probes:
            if not attached_names or not attached_names.issubset(config.internal_networks):
                result.add(
                    "negative-egress-service-network-invalid",
                    f"probe target {service_name} must attach only to internal networks",
                    compose_path,
                )
        raw_ports = service.get("ports")
        try:
            ports = json_list(raw_ports, f"services.{service_name}.ports") if raw_ports else []
        except ValueError as exc:
            result.add("compose-ports-invalid", str(exc), compose_path)
            ports = []
        if ports and service_name not in config.public_services:
            result.add(
                "unexpected-host-port",
                f"non-public service {service_name} publishes ports",
                compose_path,
            )
        if service_name in config.public_services:
            public_binding_count += len(ports)
            if len(ports) != 1:
                result.add(
                    "public-port-count-invalid",
                    f"public edge {service_name} must have exactly one host port binding",
                    compose_path,
                )
        for binding in ports:
            try:
                host_ip, published, target = _port_binding(binding)
            except ValueError as exc:
                result.add("port-binding-invalid", f"{service_name}: {exc}", compose_path)
                continue
            if host_ip not in {"127.0.0.1", "::1"} and not (
                isinstance(host_ip, str) and LOOPBACK_HOST.fullmatch(host_ip)
            ):
                result.add(
                    "port-not-loopback", f"{service_name} must bind only loopback", compose_path
                )
            if published not in (None, 0) and not (
                isinstance(published, str) and EPHEMERAL_PORT.fullmatch(published)
            ):
                result.add(
                    "fixed-host-port",
                    f"{service_name} must request an ephemeral host port",
                    compose_path,
                )
            if target != config.public_services.get(service_name):
                result.add(
                    "public-target-port-drift",
                    f"{service_name} target port does not match policy",
                    compose_path,
                )
        if service_name in config.public_services and not ports:
            result.add(
                "public-port-missing",
                f"public service {service_name} has no port binding",
                compose_path,
            )
        image = service.get("image")
        build = service.get("build")
        if not image and not build:
            result.add(
                "service-artifact-undefined",
                f"service {service_name} has neither image nor build",
                compose_path,
            )
        if isinstance(image, str) and (
            image.endswith(":latest") or ":" not in image.split("/")[-1]
        ):
            result.add(
                "mutable-image-reference",
                f"service {service_name} uses an unpinned image tag",
                compose_path,
            )
        if service_name in {
            *config.database_services,
            *config.application_services,
        } and not isinstance(service.get("healthcheck"), dict):
            result.add(
                "lifecycle-healthcheck-missing",
                f"service {service_name} requires a healthcheck for --wait lifecycle",
                compose_path,
            )
        if service_name == config.migration_service:
            raw_profiles = service.get("profiles")
            try:
                migration_profiles = set(
                    string_list(raw_profiles, f"services.{service_name}.profiles", non_empty=True)
                )
            except ValueError as exc:
                result.add("migration-profile-invalid", str(exc), compose_path)
            else:
                missing_profiles = set(config.profiles) - migration_profiles
                if missing_profiles:
                    result.add(
                        "migration-profile-missing",
                        f"migration service lacks profiles: {sorted(missing_profiles)}",
                        compose_path,
                    )
            if service.get("restart") != "no":
                result.add(
                    "migration-restart-invalid",
                    "migration service must use restart: no",
                    compose_path,
                )
    edge_to_web_members = {
        service_name
        for service_name, attached in service_networks.items()
        if config.edge_to_web_network in attached
    }
    expected_edge_to_web_members = {config.edge_service, config.web_service}
    if edge_to_web_members != expected_edge_to_web_members:
        result.add(
            "edge-web-network-members-invalid",
            f"{config.edge_to_web_network} members must be exactly "
            f"{sorted(expected_edge_to_web_members)}; got {sorted(edge_to_web_members)}",
            compose_path,
        )
    web_to_api_members = {
        service_name
        for service_name, attached in service_networks.items()
        if config.web_to_api_network in attached
    }
    expected_web_to_api_members = {config.web_service, config.api_service}
    if web_to_api_members != expected_web_to_api_members:
        result.add(
            "web-api-network-members-invalid",
            f"{config.web_to_api_network} members must be exactly "
            f"{sorted(expected_web_to_api_members)}; got {sorted(web_to_api_members)}",
            compose_path,
        )
    expected_web_networks = {
        config.edge_to_web_network,
        config.web_to_api_network,
    }
    actual_web_networks = service_networks.get(config.web_service, set())
    if actual_web_networks != expected_web_networks:
        result.add(
            "web-network-scope-invalid",
            f"{config.web_service} networks must be exactly "
            f"{sorted(expected_web_networks)}; got {sorted(actual_web_networks)}",
            compose_path,
        )
    actual_api_networks = service_networks.get(config.api_service, set())
    forbidden_api_networks = {
        config.edge_to_web_network,
        *config.edge_networks,
    }
    if config.web_to_api_network not in actual_api_networks or actual_api_networks.intersection(
        forbidden_api_networks
    ):
        result.add(
            "api-network-scope-invalid",
            f"{config.api_service} must attach to {config.web_to_api_network} "
            f"and must not attach to {sorted(forbidden_api_networks)}",
            compose_path,
        )
    edge_api_overlap = service_networks.get(config.edge_service, set()).intersection(
        actual_api_networks
    )
    if edge_api_overlap:
        result.add(
            "edge-api-network-overlap",
            f"{config.edge_service} and {config.api_service} must not share networks: "
            f"{sorted(edge_api_overlap)}",
            compose_path,
        )
    result.details.update(
        mode="static",
        services=len(services),
        public_services=len(config.public_services),
        aggregate_memory_gib=round(aggregate_memory / (1024**3), 3),
        max_runtime_memory_gib=config.max_runtime_memory_gib,
        edge_networks=len(config.edge_networks),
        ingress_path={
            "edge_to_web": config.edge_to_web_network,
            "web_to_api": config.web_to_api_network,
            "edge_proxy_source": config.edge_proxy_source.as_posix(),
            "web_target": config.web_target,
            "api_target": config.api_target,
        },
    )
    if public_binding_count != 1:
        result.add(
            "public-binding-count-invalid",
            f"Foundation runtime must expose exactly one loopback binding; found {public_binding_count}",
            compose_path,
        )
    if aggregate_memory > config.max_runtime_memory_gib * (1024**3):
        result.add(
            "runtime-memory-budget-exceeded",
            f"aggregate mem_limit is {aggregate_memory / (1024**3):.3f} GiB; policy max is {config.max_runtime_memory_gib:.3f} GiB",
            compose_path,
        )
    return result


def check(
    root: Path,
    *,
    mode: str,
    compose: Path,
    policy: Path,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    project_name_factory: Callable[[], str] = lambda: f"custometry-ci-{uuid.uuid4().hex[:12]}",
    release_env: Path | None = None,
    release_overlay: Path = Path("deploy/compose/compose.release.yaml"),
    http_port: int | None = None,
    port_selector: Callable[[str], int] = select_runtime_port,
    health_probe: Callable[[str, float], int] = probe_http_status,
    sleep: Callable[[float], None] = time.sleep,
) -> CheckResult:
    result = static_check(root, compose, policy)
    if mode == "static" or not result.ok:
        return result
    config = _policy(load_json(root / policy))
    result.details["mode"] = "runtime"
    project_name = project_name_factory()
    if not re.fullmatch(r"custometry-ci-[a-z0-9]{6,32}", project_name):
        result.add(
            "disposable-project-name-invalid",
            "runtime project must use unique custometry-ci-* name",
        )
        return result
    selected_port = http_port if http_port is not None else port_selector(project_name)
    if not _port_is_available(selected_port):
        result.add(
            "runtime-http-port-unavailable",
            f"loopback port {selected_port} is invalid or occupied before Compose start",
        )
        return result
    release_env_path: Path | None = None
    overlay_path = release_overlay if release_overlay.is_absolute() else root / release_overlay
    if release_env is not None:
        release_env_path = release_env if release_env.is_absolute() else root / release_env
        if not release_env_path.is_file() or not overlay_path.is_file():
            result.observed = False
            result.add(
                "release-compose-input-missing",
                "release runtime requires release env and Compose overlay",
                release_env_path if not release_env_path.is_file() else overlay_path,
            )
            return result
    # Docker Desktop can permanently negative-cache repeatedly recreated nested
    # bind roots. Keep each invocation one level below the checkout-owned
    # `.runtime` root; the random child remains the exact cleanup boundary.
    runtime_parent = root / ".runtime"
    runtime_parent.mkdir(parents=True, exist_ok=True)
    runtime_parent.chmod(0o700)
    _fsync_directory(runtime_parent.parent)
    runtime_dir = Path(tempfile.mkdtemp(prefix=f"{project_name}-", dir=runtime_parent))
    runtime_dir.chmod(0o700)
    _fsync_directory(runtime_parent)
    secrets_dir = runtime_dir / "secrets"
    secrets_dir.mkdir(mode=0o700)
    secrets_dir.chmod(0o700)
    _fsync_directory(runtime_dir)
    for name in (
        "control_db_password",
        "demo_source_admin_password",
        "demo_source_reader_password",
    ):
        secret = secrets_dir / name
        _write_atomic_private(secret, secrets.token_hex(32))
    env_file = runtime_dir / "runtime.env"
    _write_atomic_private(
        env_file,
        "\n".join(
            (
                f"COMPOSE_PROJECT_NAME={project_name}",
                "CUSTOMETRY_BIND_HOST=127.0.0.1",
                f"CUSTOMETRY_HTTP_PORT={selected_port}",
                f"CUSTOMETRY_SECRETS_DIR={secrets_dir}",
            )
        )
        + "\n",
    )
    prefix = [
        "docker",
        "compose",
        "--project-name",
        project_name,
        "-f",
        str((root / compose).resolve()),
        *(["-f", str(overlay_path.resolve())] if release_env_path is not None else []),
        "--env-file",
        str(env_file),
        *(["--env-file", str(release_env_path.resolve())] if release_env_path is not None else []),
    ]
    profiled_prefix = [
        *prefix,
        *(argument for profile in config.profiles for argument in ("--profile", profile)),
    ]
    database_up = [*profiled_prefix, "up", "-d", "--wait", *config.database_services]
    commands = [
        [*profiled_prefix, "config", "--quiet"],
        [
            *profiled_prefix,
            "pull" if release_env_path is not None else "build",
            *dict.fromkeys(
                (
                    *config.database_services,
                    config.migration_service,
                    *config.application_services,
                )
                if release_env_path is not None
                else (config.migration_service, *config.application_services)
            ),
        ],
        database_up,
        [*profiled_prefix, "run", "--rm", config.migration_service],
        [*profiled_prefix, "up", "-d", "--wait", *config.application_services],
        [*profiled_prefix, "ps", "--format", "json"],
    ]
    bind_visibility_retries = 0
    try:
        for command in commands:
            completed = run_command(command, cwd=root, runner=runner, timeout=600)
            if command == database_up:
                for delay in BIND_VISIBILITY_RETRY_DELAYS:
                    if completed.returncode == 0 or not _is_bind_visibility_failure(completed):
                        break
                    bind_visibility_retries += 1
                    sleep(delay)
                    completed = run_command(command, cwd=root, runner=runner, timeout=600)
            if completed.returncode != 0:
                code = (
                    "compose-bind-visibility-failed"
                    if command == database_up and _is_bind_visibility_failure(completed)
                    else "compose-runtime-failed"
                )
                add_command_failure(result, command, completed, code=code)
                break
            if command[-3:] == ["ps", "--format", "json"]:
                try:
                    records = decode_compose_ps_records(completed.stdout)
                except ValueError as exc:
                    result.add("compose-ps-invalid", str(exc))
                    break
                if not records:
                    result.add("compose-services-unobserved", "no running services were returned")
                    break
                observed_services = {
                    str(item.get("Service")) for item in records if item.get("Service")
                }
                expected_services = {
                    *config.database_services,
                    *config.application_services,
                }
                missing_services = sorted(expected_services - observed_services)
                if missing_services:
                    result.add(
                        "compose-services-unobserved",
                        f"expected running services were absent: {missing_services}",
                    )
                    break
                unhealthy = [
                    item.get("Service")
                    for item in records
                    if item.get("Service") in expected_services
                    and (item.get("State") != "running" or item.get("Health") != "healthy")
                ]
                if unhealthy:
                    result.add("compose-services-unhealthy", f"unhealthy services: {unhealthy}")
        mapped_ports: dict[str, int] = {}
        public_health: dict[str, dict[str, str | int]] = {}
        if result.ok:
            for service_name, target_port in sorted(config.public_services.items()):
                command = [*profiled_prefix, "port", service_name, str(target_port)]
                completed = run_command(command, cwd=root, runner=runner, timeout=30)
                if completed.returncode != 0:
                    add_command_failure(
                        result, command, completed, code="compose-host-port-unobserved"
                    )
                    continue
                try:
                    host, mapped = _mapped_port(completed.stdout)
                except ValueError as exc:
                    result.add("compose-host-port-invalid", str(exc))
                    continue
                if mapped != selected_port:
                    result.add(
                        "compose-host-port-drift",
                        f"{service_name} mapped {mapped}; runtime env selected {selected_port}",
                    )
                    continue
                mapped_ports[service_name] = mapped
                health_url = f"http://{host}:{mapped}{config.public_health_paths[service_name]}"
                try:
                    health_status = health_probe(health_url, 10.0)
                except (HTTPException, OSError, TimeoutError, ValueError) as exc:
                    result.add(
                        "compose-public-health-failed",
                        f"{service_name} did not answer through mapped loopback port: {exc}",
                    )
                    continue
                if not 200 <= health_status < 400:
                    result.add(
                        "compose-public-health-invalid",
                        f"{service_name} returned HTTP {health_status} through mapped loopback port",
                    )
                    continue
                public_health[service_name] = {
                    "url": health_url,
                    "status": health_status,
                }
        ingress_isolation_observed = {
            "edge_to_web": False,
            "edge_to_api_denied": False,
        }
        if result.ok:
            allowed = [
                *profiled_prefix,
                "exec",
                "-T",
                config.edge_service,
                *config.ingress_allowed_probe,
            ]
            completed = run_command(allowed, cwd=root, runner=runner, timeout=30)
            if completed.returncode != 0:
                add_command_failure(
                    result,
                    allowed,
                    completed,
                    code="ingress-isolation-preflight-failed",
                )
            else:
                ingress_isolation_observed["edge_to_web"] = True
                denied = [
                    *profiled_prefix,
                    "exec",
                    "-T",
                    config.edge_service,
                    *config.ingress_denied_probe,
                ]
                completed = run_command(denied, cwd=root, runner=runner, timeout=30)
                if completed.returncode == 0:
                    result.add(
                        "edge-api-isolation-breached",
                        f"{config.edge_service} reached the forbidden API target "
                        f"{config.api_target}",
                    )
                else:
                    ingress_isolation_observed["edge_to_api_denied"] = True
        negative_egress_observed: list[str] = []
        if result.ok:
            for service_name, probe in sorted(config.negative_egress_probes.items()):
                preflight = [*profiled_prefix, "exec", "-T", service_name, *probe.preflight]
                completed = run_command(preflight, cwd=root, runner=runner, timeout=30)
                if completed.returncode != 0:
                    add_command_failure(
                        result,
                        preflight,
                        completed,
                        code="negative-egress-preflight-failed",
                    )
                    continue
                external = [*profiled_prefix, "exec", "-T", service_name, *probe.external]
                completed = run_command(external, cwd=root, runner=runner, timeout=30)
                if completed.returncode == 0:
                    result.add(
                        "unexpected-runtime-egress",
                        f"{service_name} reached the external probe target",
                    )
                    continue
                negative_egress_observed.append(service_name)
        result.details.update(
            disposable_project=project_name,
            artifact_mode="pull" if release_env_path is not None else "build",
            selected_http_port=selected_port,
            mapped_ports=mapped_ports,
            public_health=public_health,
            ingress_isolation_observed=ingress_isolation_observed,
            negative_egress_observed=negative_egress_observed,
            bind_visibility_retries=bind_visibility_retries,
        )
    finally:
        down = [*profiled_prefix, "down", "--volumes", "--remove-orphans"]
        completed = run_command(down, cwd=root, runner=runner, timeout=300)
        if completed.returncode != 0:
            add_command_failure(result, down, completed, code="compose-cleanup-failed")
        try:
            shutil.rmtree(runtime_dir)
        except OSError as exc:
            result.add(
                "runtime-state-cleanup-failed",
                f"could not remove exact disposable state {runtime_dir}: {exc}",
            )
    result.details["runtime_observed"] = result.ok
    return result


def cli(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate and execute disposable Compose lifecycle"
    )
    add_common_arguments(parser)
    parser.add_argument("--mode", choices=("static", "runtime"), default="static")
    parser.add_argument("--compose", type=Path, default=Path("compose.yaml"))
    parser.add_argument("--policy", type=Path, default=Path("deploy/compose/runtime-policy.json"))
    parser.add_argument("--release-env", type=Path)
    parser.add_argument(
        "--release-overlay", type=Path, default=Path("deploy/compose/compose.release.yaml")
    )
    parser.add_argument("--http-port", type=int)
    args = parser.parse_args(argv)
    return render_result(
        check(
            args.root.resolve(),
            mode=args.mode,
            compose=args.compose,
            policy=args.policy,
            release_env=args.release_env,
            release_overlay=args.release_overlay,
            http_port=args.http_port,
        ),
        args.json,
    )


if __name__ == "__main__":
    main_guard(cli)
