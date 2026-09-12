"""Explicit loopback-only S01 preparation using production owner services."""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
from pathlib import Path
import secrets
from typing import Any
from uuid import UUID, uuid4

import psycopg

from custometry_api.config import Settings
from custometry_api.connections.router import create_connection_services
from custometry_api.identity.router import create_identity_service
from apps.worker_data.vertical_slice import DataPipelineRunner
from packages.artifacts.infrastructure.local import LocalArtifactStore
from packages.contracts.data_pipeline import DataPipelineFailure
from packages.identity_access.domain.policy import require_permission
from packages.ingestion.domain.model import ExtractionBatchRequest, RETAIL_REPORT_OBJECTS
from packages.semantic_model.infrastructure.postgres import PostgresSemanticRepository
from tools.custometry_quality import development_runtime as runtime


def _save(path: Path, value: dict[str, Any]) -> None:
    temporary = path.with_suffix(".tmp")
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "w") as stream:
        json.dump(value, stream, sort_keys=True, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def prepare(root: Path) -> dict[str, Any]:
    policy = runtime.load_policy(root)
    paths = runtime.runtime_paths(root, policy)
    runtime.prepare_runtime(paths, policy)
    if runtime.compose_health(paths, policy) != {
        "control-db": "healthy",
        "demo-source-db": "healthy",
    }:
        raise DataPipelineFailure("OWNED_HYBRID_DATABASES_REQUIRED")
    lock_path = paths.runtime_dir / "retail-report.lock"
    fd = os.open(lock_path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return _prepare_locked(paths, policy)


def _prepare_locked(paths: runtime.RuntimePaths, policy: runtime.RuntimePolicy) -> dict[str, Any]:
    state_path = paths.secrets_dir / "retail-report.json"
    if state_path.is_symlink():
        raise DataPipelineFailure("PREPARATION_STATE_UNSAFE")
    if state_path.exists():
        if state_path.stat().st_mode & 0o077:
            raise DataPipelineFailure("PREPARATION_STATE_UNSAFE")
        state = json.loads(state_path.read_text())
        if (
            state.get("runtime_id") != paths.project_name
            or state.get("profile") != "retail-report/v1"
        ):
            raise DataPipelineFailure("PREPARATION_IDENTITY_CONFLICT")
    else:
        state = {
            "runtime_id": paths.project_name,
            "profile": "retail-report/v1",
            "admin_email": "setup-ms003@example.invalid",
            "analyst_email": "analyst-ms003@example.invalid",
            "admin_password": secrets.token_urlsafe(32),
            "analyst_password": secrets.token_urlsafe(32),
        }
        _save(state_path, state)
    bootstrap_path = paths.secrets_dir / "bootstrap_token"
    if not bootstrap_path.exists():
        fd = os.open(bootstrap_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, "w") as stream:
            stream.write(secrets.token_urlsafe(32))
    if bootstrap_path.is_symlink() or bootstrap_path.stat().st_mode & 0o077:
        raise DataPipelineFailure("PREPARATION_SECRET_UNSAFE")
    env = runtime.host_environment(paths, policy, "api")
    settings = Settings.model_validate(
        {
            k.removeprefix("CUSTOMETRY_").lower(): v
            for k, v in env.items()
            if k.startswith("CUSTOMETRY_")
        }
    )
    identity = create_identity_service(settings)
    _, catalog, adapters = create_connection_services(settings)
    if "workspace_id" not in state:
        outcome = identity.bootstrap(
            presented_secret=bootstrap_path.read_text(),
            email=state["admin_email"],
            password=state["admin_password"],
            workspace_key="ms003-retail-report",
            workspace_name="MS-003 Retail Report",
        )
        state.update(workspace_id=str(outcome.workspace_id), admin_id=str(outcome.principal_id))
        _save(state_path, state)
    workspace_id = UUID(state["workspace_id"])
    admin_session = identity.login(
        email=state["admin_email"],
        password=state["admin_password"],
        workspace_id=workspace_id,
        device_label="local-preparation",
    )
    admin = identity.authenticate(admin_session.access_token)
    try:
        if str(admin.principal_id) != state["admin_id"] or not admin.installation_admin:
            raise DataPipelineFailure("PREPARATION_OWNER_CONFLICT")
        require_permission(admin, "connection.manage")
        if "analyst_id" not in state:
            invitation = identity.invite(
                admin,
                workspace_id=workspace_id,
                email=state["analyst_email"],
                roles=["analyst"],
                expires_in_hours=72,
            )
            state["analyst_id"] = str(
                identity.accept_invitation(
                    token=invitation.token, password=state["analyst_password"]
                )
            )
            _save(state_path, state)
        analyst_session = identity.login(
            email=state["analyst_email"],
            password=state["analyst_password"],
            workspace_id=workspace_id,
            device_label="local-preparation-check",
        )
        analyst = identity.authenticate(analyst_session.access_token)
        identity.logout(analyst_session.refresh_token, analyst_session.csrf_token)
        if (
            str(analyst.principal_id) != state["analyst_id"]
            or analyst.installation_admin
            or "connection.manage" in analyst.permissions
        ):
            raise DataPipelineFailure("PREPARATION_ANALYST_CONFLICT")
        require_permission(analyst, "analysis.run")
        if "connection_id" not in state:
            definition = catalog.create(
                admin,
                connector_id="postgresql",
                profile_ref="retail_demo",
                secret_ref="retail_demo_reader",
                display_name="MS-003 Northwind Retail",
            )
            state.update(
                connection_id=str(definition.connection_id),
                source_system_id=str(definition.source_system_id),
                dataset_id=str(uuid4()),
                batch_id=str(uuid4()),
            )
            _save(state_path, state)
        connection_id = UUID(state["connection_id"])
        definition = catalog.test(admin, connection_id)
        if str(definition.source_system_id) != state["source_system_id"]:
            raise DataPipelineFailure("PREPARATION_SOURCE_CONFLICT")
        connector = adapters[connection_id]
        session = connector.begin_extraction_session(
            workspace_id=workspace_id, source_system_id=definition.source_system_id
        )
        try:
            source_rows = {}
            for spec in RETAIL_REPORT_OBJECTS:
                source_rows[spec.semantic_entity] = sorted(
                    connector.extract(
                        session=session,
                        schema_name="retail",
                        object_name=spec.source_object,
                        columns=spec.columns,
                        limit=100_000,
                    ),
                    key=lambda r: str(r[spec.primary_key]),
                )
            fingerprint = hashlib.sha256(
                json.dumps(source_rows, sort_keys=True, default=str, separators=(",", ":")).encode()
            ).hexdigest()
        finally:
            connector.close_extraction_session(session, "committed")
        if state.get("source_fingerprint", fingerprint) != fingerprint:
            raise DataPipelineFailure("PREPARATION_SOURCE_FINGERPRINT_CONFLICT")
        state["source_fingerprint"] = fingerprint
        _save(state_path, state)

        def connect() -> psycopg.Connection[Any]:
            return psycopg.connect(
                host=settings.database_host,
                port=settings.database_port,
                dbname=settings.database_name,
                user=settings.database_user,
                password=settings.read_database_password(),
                connect_timeout=3,
            )

        result = DataPipelineRunner(
            connector=connector,
            connect=connect,
            artifact_store=LocalArtifactStore(settings.analytics_artifact_root),
        ).run(
            ExtractionBatchRequest(
                UUID(state["batch_id"]),
                workspace_id,
                connection_id,
                definition.source_system_id,
                UUID(state["dataset_id"]),
                "retail-report/v1:" + fingerprint,
                profile="retail-report/v1",
                source_fingerprint=fingerprint,
            )
        )
        if result.state != "committed" or result.semantic_dataset_version_id is None:
            raise DataPipelineFailure("RETAIL_REPORT_NOT_ADMITTED")
        with connect() as connection, connection.cursor() as cursor:
            publication = PostgresSemanticRepository.get(
                cursor, workspace_id=workspace_id, version_id=result.semantic_dataset_version_id
            )
        output = {
            "profile": "retail-report/v1",
            "workspace_id": str(workspace_id),
            "admin_id": state["admin_id"],
            "analyst_id": state["analyst_id"],
            "connection_id": state["connection_id"],
            "source_system_id": state["source_system_id"],
            "batch_id": state["batch_id"],
            "dataset_id": state["dataset_id"],
            "semantic_dataset_version_id": str(result.semantic_dataset_version_id),
            "quality_report_id": str(result.quality_report_id),
            "source_fingerprint": fingerprint,
            "reused": result.reused,
            "publication": publication,
            "artifacts": [m.as_dict() for m in result.artifact_manifests],
        }
        _save(paths.runtime_dir / "retail-report-output.json", output)
        return output
    finally:
        identity.logout(admin_session.refresh_token, admin_session.csrf_token)


def main() -> int:
    try:
        output = prepare(Path.cwd())
        print(
            json.dumps(
                {k: v for k, v in output.items() if k not in {"publication", "artifacts"}}, indent=2
            )
        )
        print(
            "Next: inspect .runtime/development/<runtime-id>/retail-report-output.json; use protected retail-report.json for analyst login through /api/identity/login."
        )
        return 0
    except Exception as exc:
        # Driver messages and arbitrary exception text may contain source secrets/rows.
        print("retail-report-preparation-error: " + str(getattr(exc, "code", type(exc).__name__)))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
