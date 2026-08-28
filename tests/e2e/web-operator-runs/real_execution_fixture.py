"""Disposable real W36 boundary for W34 browser evidence.

The fixture mounts the production Execution Control FastAPI adapter and store,
migrates a disposable PostgreSQL database, and uses the production Valkey
outbox/worker adapters. Only reset, drain, and identity helpers are fixture-only.
"""

from __future__ import annotations

import argparse
import os
import tempfile
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

import psycopg
import uvicorn
from alembic import command
from alembic.config import Config
from fastapi import FastAPI, Header, HTTPException
from psycopg import Connection
from redis import Redis
from testcontainers.core.container import DockerContainer
from testcontainers.core.wait_strategies import LogMessageWaitStrategy
from testcontainers.postgres import PostgresContainer

from custometry_api.config import Settings
from custometry_api.runs.router import create_runs_app
from packages.contracts.execution import ExecutionActor
from packages.execution.application.service import ExecutionControlService
from packages.execution.infrastructure.control_postgres import PostgresExecutionControlStore
from packages.execution.infrastructure.valkey import (
    DisposableExecutionWorker,
    ExecutionOutboxDispatcher,
    ValkeyTaskQueue,
)
from packages.identity_access.domain.policy import Actor


POSTGRES_IMAGE = (
    "postgres:17.5-alpine3.21@"
    "sha256:5d004e058f520673f1f6edbad6b1603d5dab4c818e257c041889ef64672a8cc4"
)
VALKEY_IMAGE = "valkey/valkey:8.0.1-alpine"
WORKSPACE_ID = UUID("11111111-1111-4111-8111-111111111111")
OWNER_ID = UUID("22222222-2222-4222-8222-222222222222")
OPERATOR_ID = UUID("33333333-3333-4333-8333-333333333333")
OUTSIDER_ID = UUID("44444444-4444-4444-8444-444444444444")


class TokenIdentity:
    def __init__(self) -> None:
        self.actors = {
            "operator": Actor(
                OPERATOR_ID, WORKSPACE_ID, "operator@example.invalid",
                frozenset({"run.read", "run.cancel", "run.retry", "run.create"}),
            ),
            "owner": Actor(OWNER_ID, WORKSPACE_ID, "owner@example.invalid", frozenset({"run.read"})),
            "no-permission": Actor(OUTSIDER_ID, WORKSPACE_ID, "outsider@example.invalid", frozenset()),
        }

    def authenticate(self, token: str) -> Actor:
        try:
            return self.actors[token]
        except KeyError as error:
            raise RuntimeError("unknown fixture token") from error


def migrate(host: str, port: int, password_file: Path) -> None:
    names = {
        "CUSTOMETRY_DATABASE_HOST": host,
        "CUSTOMETRY_DATABASE_PORT": str(port),
        "CUSTOMETRY_DATABASE_NAME": "custometry",
        "CUSTOMETRY_DATABASE_USER": "custometry",
        "CUSTOMETRY_DATABASE_PASSWORD_FILE": str(password_file),
    }
    previous = {name: os.environ.get(name) for name in names}
    os.environ.update(names)
    try:
        command.upgrade(Config("migrations/alembic.ini"), "head")
    finally:
        for name, value in previous.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value


def fixture_app(connect: Callable[[], Connection[Any]], valkey: Redis) -> FastAPI:
    identity = TokenIdentity()
    store = PostgresExecutionControlStore(connect)
    queue = ValkeyTaskQueue(valkey, namespace="custometry:w34:execution")
    dispatcher = ExecutionOutboxDispatcher(store, queue)
    worker = DisposableExecutionWorker(store, queue, worker_id="w34-disposable-worker")
    application = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    application.mount(
        "/execution",
        create_runs_app(
            Settings(database_password_file=Path("/not-read"), version="w34-real-w36-fixture"),
            identity_service=identity,  # type: ignore[arg-type]
            execution_service=ExecutionControlService(store),
        ),
    )
    fixture_ids: dict[str, str] = {}

    def actor_from_header(authorization: str | None) -> Actor:
        if authorization is None:
            raise HTTPException(status_code=401)
        scheme, _, token = authorization.partition(" ")
        if scheme.casefold() != "bearer":
            raise HTTPException(status_code=401)
        try:
            return identity.authenticate(token)
        except RuntimeError as error:
            raise HTTPException(status_code=401) from error

    operator = ExecutionActor(
        OPERATOR_ID,
        WORKSPACE_ID,
        frozenset({"run.read", "run.cancel", "run.retry", "run.create"}),
        "w34-policy-v1",
    )

    def create_and_claim(title: str, kind: str, trace: str):
        run = store.create_run(
            workspace_id=WORKSPACE_ID,
            owner_principal_id=OWNER_ID,
            execution_kind=kind,
            lane="priority" if kind == "analytics" else "default",
            safe_title=title,
            safe_trace_id=trace,
            request_id=f"seed-{uuid4()}",
            policy_version="w34-policy-v1",
        )
        dispatched = dispatcher.dispatch()
        assert dispatched.published == 1
        claimed = worker.run_one()
        assert claimed is not None and claimed[0] == "execute" and claimed[2] is not None
        return run, claimed[1], claimed[2]

    def reset_data() -> dict[str, str]:
        with connect() as connection, connection.transaction(), connection.cursor() as cursor:
            cursor.execute(
                """
                TRUNCATE TABLE execution_reconciliation_findings, execution_idempotency,
                  execution_outbox, execution_transition_history, execution_attempts,
                  execution_runs CASCADE
                """
            )
        valkey.flushdb()
        fixture_ids.clear()

        running, _, _ = create_and_claim("Daily retail ingestion", "ingestion", "trace-running-safe")
        fixture_ids["running"] = str(running.run_id)

        succeeded, succeeded_attempt, succeeded_token = create_and_claim(
            "Published customer mart", "pipeline", "trace-succeeded-safe"
        )
        store.publish_attempt_state(
            succeeded_attempt, fencing_token=succeeded_token, state="SUCCEEDED",
            worker_id="w34-success-worker", reason="PUBLISHED", request_id="seed-succeeded",
        )
        fixture_ids["succeeded"] = str(succeeded.run_id)

        failed, failed_attempt, failed_token = create_and_claim(
            "Margin analysis", "analytics", "trace-failed-safe"
        )
        store.publish_attempt_state(
            failed_attempt, fencing_token=failed_token, state="FAILED",
            worker_id="w34-failure-worker", reason="RESOURCE_LIMIT_EXCEEDED",
            request_id="seed-failed", failure_code="RESOURCE_LIMIT_EXCEEDED",
            observed_limit=1024, configured_limit=768,
            safe_remediation="Reduce the bounded input range and retry failed nodes.",
        )
        fixture_ids["failed"] = str(failed.run_id)

        reconciled, reconciled_attempt, _ = create_and_claim(
            "Reconciled lease", "pipeline", "trace-reconciled-safe"
        )

        cancelling, _, _ = create_and_claim(
            "Cancelable forecast", "forecast", "trace-cancelling-safe"
        )
        store.cancel(
            operator, "workspace", run_id=cancelling.run_id, expected_revision=2,
            reason="seed operator cancellation", request_id="seed-cancelling",
            idempotency_key="seed-cancelling", payload_hash="a" * 64,
        )
        fixture_ids["cancelling"] = str(cancelling.run_id)

        with connect() as connection, connection.transaction(), connection.cursor() as cursor:
            cursor.execute(
                "UPDATE execution_attempts SET lease_expires_at = %s WHERE id = %s",
                (datetime.now(UTC) - timedelta(seconds=5), reconciled_attempt),
            )
        findings = store.reconcile(observed_at=datetime.now(UTC), request_id="seed-reconcile")
        assert findings == ("EXPIRED_LEASE_FENCED_AND_RETRIED",)
        fixture_ids["reconciled"] = str(reconciled.run_id)

        queued = store.create_run(
            workspace_id=WORKSPACE_ID, owner_principal_id=OWNER_ID,
            execution_kind="ingestion", lane="bulk", safe_title="Queued loyalty import",
            safe_trace_id="trace-queued-safe", request_id="seed-queued",
            policy_version="w34-policy-v1",
        )
        fixture_ids["queued"] = str(queued.run_id)
        return dict(fixture_ids)

    @application.get("/health/ready")
    def ready() -> dict[str, str]:
        with connect() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        assert valkey.ping()
        return {"status": "ready", "version": "w34-real-w36-fixture"}

    @application.get("/identity/me")
    def me(authorization: str | None = Header(default=None)) -> dict[str, object]:
        actor = actor_from_header(authorization)
        return {
            "principal_id": str(actor.principal_id), "workspace_id": str(actor.workspace_id),
            "email": actor.email, "permissions": sorted(actor.permissions),
            "installation_admin": False, "token_kind": "fixture",
        }

    @application.post("/__fixture__/reset")
    def reset() -> dict[str, str]:
        return reset_data()

    @application.get("/__fixture__/ids")
    def ids() -> dict[str, str]:
        return dict(fixture_ids)

    @application.post("/__fixture__/drain")
    def drain() -> dict[str, int]:
        dispatched = dispatcher.dispatch()
        worked = 0
        for _ in range(dispatched.published):
            if worker.run_one() is not None:
                worked += 1
        return {"selected": dispatched.selected, "published": dispatched.published, "worked": worked}

    reset_data()
    return application


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    secret = "w34-disposable-postgres-only"
    with tempfile.TemporaryDirectory(prefix="custometry-w34-") as temporary:
        password_file = Path(temporary) / "postgres-password"
        password_file.write_text(secret, encoding="utf-8")
        with PostgresContainer(
            image=POSTGRES_IMAGE, username="custometry", password=secret, dbname="custometry",
        ) as postgres_container:
            host = postgres_container.get_container_host_ip()
            port = int(postgres_container.get_exposed_port(5432))

            def connect() -> Connection[Any]:
                return psycopg.connect(
                    host=host, port=port, dbname="custometry", user="custometry",
                    password=secret, connect_timeout=3,
                )

            migrate(host, port, password_file)
            valkey_ready = LogMessageWaitStrategy("Ready to accept connections").with_startup_timeout(30)
            with DockerContainer(VALKEY_IMAGE).with_exposed_ports(6379).waiting_for(valkey_ready) as valkey_container:
                valkey = Redis(
                    host=valkey_container.get_container_host_ip(),
                    port=int(valkey_container.get_exposed_port(6379)),
                    decode_responses=False, socket_timeout=3,
                )
                assert valkey.ping()
                with connect() as connection, connection.transaction(), connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO identity_workspaces (id, key, name, active) VALUES (%s, 'northwind-retail', 'Northwind Retail', true)",
                        (WORKSPACE_ID,),
                    )
                    for principal_id, label in ((OWNER_ID, "owner"), (OPERATOR_ID, "operator"), (OUTSIDER_ID, "outsider")):
                        cursor.execute(
                            "INSERT INTO identity_principals (id, email, password_hash, installation_admin, active) VALUES (%s, %s, 'fixture-only', false, true)",
                            (principal_id, f"{label}@example.invalid"),
                        )
                uvicorn.run(fixture_app(connect, valkey), host="127.0.0.1", port=args.port, log_level="warning")


if __name__ == "__main__":
    main()
