# pyright: reportUnknownArgumentType=false, reportUnknownMemberType=false
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from multiprocessing import get_context
from pathlib import Path
import time
from typing import TypedDict
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from custometry_api.config import Settings
from custometry_api.runs.router import create_runs_app
from packages.contracts.execution import ExecutionActor, ExecutionControlFailure
from packages.execution.application.service import ExecutionControlService
from packages.execution.infrastructure.control_postgres import PostgresExecutionControlStore
from packages.execution.infrastructure.valkey import (
    DisposableExecutionWorker,
    ExecutionOutboxDispatcher,
    IsolatedAttemptController,
    ValkeyTaskQueue,
)
from tests.integration.execution_control.conftest import (
    ExecutionBoundaries,
    ExecutionRuntime,
    migrate,
)


class MigrationArguments(TypedDict):
    host: str
    port: int
    database: str
    user: str
    password_file: Path


class TokenIdentity:
    def __init__(self, actors: dict[str, object]) -> None:
        self._actors = actors

    def authenticate(self, token: str):
        try:
            return self._actors[token]
        except KeyError as exc:
            raise ValueError("invalid token") from exc


def headers(token: str, *, request_id: str | None = None) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "X-Request-ID": request_id or f"request-{uuid4()}",
        "X-Contract-Version": "1.0.0",
    }


def api(runtime: ExecutionRuntime) -> tuple[TestClient, PostgresExecutionControlStore]:
    store = PostgresExecutionControlStore(runtime.connect)
    identity = TokenIdentity(
        {"owner": runtime.owner, "operator": runtime.operator, "outsider": runtime.outsider}
    )
    application = create_runs_app(
        Settings(database_password_file=Path("/not-read")),
        identity_service=identity,  # type: ignore[arg-type]
        execution_service=ExecutionControlService(store),
    )
    return TestClient(application), store


def execution_actor(runtime: ExecutionRuntime) -> ExecutionActor:
    return ExecutionActor(
        runtime.operator.principal_id,
        runtime.workspace_id,
        runtime.operator.permissions,
        "policy-integration-v1",
    )


def test_authenticated_api_filters_before_count_and_hides_cross_owner_runs(
    execution_runtime: ExecutionRuntime,
) -> None:
    client, store = api(execution_runtime)
    own = store.create_run(
        workspace_id=execution_runtime.workspace_id,
        owner_principal_id=execution_runtime.owner.principal_id,
        execution_kind="ingestion",
        safe_title="Owned retail extraction",
        safe_trace_id="safe-trace-owned",
        request_id="seed-own",
        policy_version="policy-v1",
    )
    hidden = store.create_run(
        workspace_id=execution_runtime.workspace_id,
        owner_principal_id=execution_runtime.operator.principal_id,
        execution_kind="analytics",
        safe_title="Operator analytics",
        safe_trace_id="safe-trace-hidden",
        request_id="seed-hidden",
        policy_version="policy-v1",
    )

    forbidden = client.get("/runs", headers=headers("outsider"))
    unauthenticated_headers = headers("outsider")
    unauthenticated_headers.pop("Authorization")
    unauthenticated = client.get("/runs", headers=unauthenticated_headers)
    invalid = client.get("/runs", headers=headers("unknown-token"))
    owner_list = client.get("/runs", headers=headers("owner"))
    hidden_detail = client.get(f"/runs/{hidden.run_id}", headers=headers("owner"))
    operator_list = client.get("/runs", headers=headers("operator"))
    summary = client.get("/queue-summary", headers=headers("operator"))

    assert forbidden.status_code == 403
    assert forbidden.json() == {"code": "FORBIDDEN"}
    assert unauthenticated.status_code == 401
    assert invalid.status_code == 401
    assert owner_list.status_code == 200
    assert owner_list.json()["visible_count"] == 1
    assert owner_list.json()["runs"][0]["run_id"] == str(own.run_id)
    assert hidden_detail.status_code == 404
    assert hidden_detail.json() == {"code": "NOT_FOUND"}
    assert operator_list.status_code == 200
    assert operator_list.json()["visible_count"] == 2
    assert "safe-trace-hidden" in {item["safe_trace_id"] for item in operator_list.json()["runs"]}
    assert summary.status_code == 200
    assert summary.json()["counts"] == {"QUEUED": 2}
    assert summary.json()["lane_counts"] == {"default": 2}
    assert summary.json()["freshness"] == "fresh"


def test_real_valkey_cancel_fences_stale_worker_and_is_idempotent(
    execution_runtime: ExecutionRuntime,
) -> None:
    client, store = api(execution_runtime)
    run = store.create_run(
        workspace_id=execution_runtime.workspace_id,
        owner_principal_id=execution_runtime.owner.principal_id,
        execution_kind="ingestion",
        safe_title="Cancelable extraction",
        request_id="seed-cancel",
        policy_version="policy-v1",
    )
    queue = ValkeyTaskQueue(execution_runtime.valkey, namespace=f"w36:{run.run_id}")
    dispatcher = ExecutionOutboxDispatcher(store, queue)
    worker = DisposableExecutionWorker(store, queue, worker_id="disposable-w36")

    assert dispatcher.dispatch().published == 1
    claimed = worker.run_one()
    assert claimed is not None and claimed[0] == "execute"
    _, attempt_id, stale_token = claimed
    assert stale_token is not None

    mutation_headers = headers("operator", request_id="cancel-request")
    mutation_headers["Idempotency-Key"] = "cancel-key"
    cancelled = client.post(
        f"/runs/{run.run_id}/cancel",
        headers=mutation_headers,
        json={"expected_revision": 2, "reason": "operator requested cancellation"},
    )
    assert cancelled.status_code == 200, cancelled.text
    assert cancelled.json()["state"] == "CANCELLING"

    with pytest.raises(ExecutionControlFailure, match="STALE_FENCING_TOKEN"):
        store.publish_attempt_state(
            attempt_id,
            fencing_token=stale_token,
            state="SUCCEEDED",
            worker_id="stale-worker",
            reason="STALE_COMPLETION",
            request_id="stale-completion",
        )

    assert dispatcher.dispatch().published == 1
    applied = worker.run_one()
    assert applied is not None and applied[0] == "cancel"
    replay = client.post(
        f"/runs/{run.run_id}/cancel",
        headers=mutation_headers,
        json={"expected_revision": 2, "reason": "operator requested cancellation"},
    )
    assert replay.status_code == 200
    assert replay.json()["state"] == "CANCELLED"

    conflict = client.post(
        f"/runs/{run.run_id}/cancel",
        headers=mutation_headers,
        json={"expected_revision": 2, "reason": "different cancellation reason"},
    )
    assert conflict.status_code == 409
    assert conflict.json() == {"code": "IDEMPOTENCY_CONFLICT"}

    with execution_runtime.connect() as connection, connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT previous_state, new_state, reason_code, request_id
            FROM execution_transition_history WHERE run_id = %s ORDER BY occurred_at, id
            """,
            (run.run_id,),
        )
        history = cursor.fetchall()
    assert ("RUNNING", "CANCELLING", "operator requested cancellation", "cancel-request") in history
    assert any(item[1:] == ("CANCELLED", "CANCEL_CLEANUP_COMPLETE", item[3]) for item in history)


def test_manual_retry_creates_new_run_and_attempt_ancestry(
    execution_runtime: ExecutionRuntime,
) -> None:
    client, store = api(execution_runtime)
    failed = store.create_run(
        workspace_id=execution_runtime.workspace_id,
        owner_principal_id=execution_runtime.owner.principal_id,
        execution_kind="analytics",
        safe_title="Failed analysis",
        request_id="seed-retry",
        policy_version="policy-v1",
    )
    queue = ValkeyTaskQueue(execution_runtime.valkey, namespace=f"w36:{failed.run_id}")
    dispatcher = ExecutionOutboxDispatcher(store, queue)
    worker = DisposableExecutionWorker(store, queue, worker_id="retry-worker")
    assert dispatcher.dispatch().published == 1
    delivered = worker.run_one()
    assert delivered is not None and delivered[0] == "execute"
    actor = execution_actor(execution_runtime)
    _, attempts = store.get_run(actor, "workspace", failed.run_id)
    claimed = attempts[0]
    store.publish_attempt_state(
        claimed.attempt_id,
        fencing_token=claimed.fencing_token,
        state="FAILED",
        worker_id="failing-worker",
        reason="SAFE_FAILURE_CODE",
        request_id="publish-failed",
    )

    retry_headers = headers("operator", request_id="retry-request")
    retry_headers["Idempotency-Key"] = "retry-key"
    response = client.post(
        f"/runs/{failed.run_id}/retry",
        headers=retry_headers,
        json={
            "expected_revision": 3,
            "reason": "retry failed attempt after remediation",
            "mode": "failed_nodes",
        },
    )
    assert response.status_code == 200, response.text
    retried_id = UUID(response.json()["run_id"])
    assert retried_id != failed.run_id
    assert response.json()["retry_of_id"] == str(failed.run_id)
    assert response.json()["state"] == "CREATED"

    detail = client.get(f"/runs/{retried_id}", headers=headers("operator"))
    assert detail.status_code == 200
    assert detail.json()["attempts"][0]["retry_of_id"] == str(claimed.attempt_id)
    assert dispatcher.dispatch().published == 1
    retry_delivery = worker.run_one()
    assert retry_delivery is not None and retry_delivery[0] == "execute"
    assert retry_delivery[1] == UUID(detail.json()["attempts"][0]["attempt_id"])
    replay = client.post(
        f"/runs/{failed.run_id}/retry",
        headers=retry_headers,
        json={
            "expected_revision": 3,
            "reason": "retry failed attempt after remediation",
            "mode": "failed_nodes",
        },
    )
    assert replay.json()["run_id"] == str(retried_id)


def test_cancelling_waits_until_every_active_attempt_is_fenced_and_cleaned(
    execution_runtime: ExecutionRuntime,
) -> None:
    client, store = api(execution_runtime)
    run = store.create_run(
        workspace_id=execution_runtime.workspace_id,
        owner_principal_id=execution_runtime.owner.principal_id,
        execution_kind="pipeline",
        safe_title="Two active nodes",
        request_id="seed-two-attempts",
        policy_version="policy-v1",
    )
    queue = ValkeyTaskQueue(execution_runtime.valkey, namespace=f"w36:{run.run_id}")
    dispatcher = ExecutionOutboxDispatcher(store, queue)
    worker = DisposableExecutionWorker(store, queue, worker_id="multi-worker")
    dispatcher.dispatch()
    first_claim = worker.run_one()
    assert first_claim is not None
    second_attempt = uuid4()
    with execution_runtime.connect() as connection, connection.transaction(), connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO execution_attempts
              (id, run_id, workspace_id, attempt_number, state, fencing_token)
            VALUES (%s, %s, %s, 2, 'READY', 0)
            """,
            (second_attempt, run.run_id, execution_runtime.workspace_id),
        )
    store.claim_attempt(
        second_attempt,
        worker_id="multi-worker-2",
        lease_seconds=30,
        request_id="claim-second",
    )
    cancel_headers = headers("operator", request_id="cancel-multi")
    cancel_headers["Idempotency-Key"] = "cancel-multi"
    response = client.post(
        f"/runs/{run.run_id}/cancel",
        headers=cancel_headers,
        json={"expected_revision": 2, "reason": "cancel every active node"},
    )
    assert response.status_code == 200
    assert dispatcher.dispatch().published == 2

    assert worker.run_one() is not None
    actor = execution_actor(execution_runtime)
    after_first, _ = store.get_run(actor, "workspace", run.run_id)
    assert after_first.state == "CANCELLING"
    assert worker.run_one() is not None
    after_second, _ = store.get_run(actor, "workspace", run.run_id)
    assert after_second.state == "CANCELLED"


def test_reconciliation_repairs_lost_delivery_and_expired_lease_with_fencing(
    execution_runtime: ExecutionRuntime,
) -> None:
    _, store = api(execution_runtime)
    run = store.create_run(
        workspace_id=execution_runtime.workspace_id,
        owner_principal_id=execution_runtime.owner.principal_id,
        execution_kind="ingestion",
        safe_title="Reconciled extraction",
        request_id="seed-reconcile",
        policy_version="policy-v1",
    )
    queue = ValkeyTaskQueue(execution_runtime.valkey, namespace=f"w36:{run.run_id}")
    dispatcher = ExecutionOutboxDispatcher(store, queue)
    worker = DisposableExecutionWorker(store, queue, worker_id="lease-worker")
    dispatcher.dispatch()
    with execution_runtime.connect() as connection, connection.transaction(), connection.cursor() as cursor:
        cursor.execute(
            "UPDATE execution_outbox SET published_at = CURRENT_TIMESTAMP - interval '5 seconds' WHERE run_id = %s",
            (run.run_id,),
        )
    findings = store.reconcile(observed_at=datetime.now(UTC), request_id="reconcile-lost")
    assert findings == ("LOST_DELIVERY_REQUEUED",)
    dispatcher.dispatch()
    claimed = worker.run_one()
    assert claimed is not None and claimed[2] is not None
    stale_attempt, stale_token = claimed[1], claimed[2]
    with execution_runtime.connect() as connection, connection.transaction(), connection.cursor() as cursor:
        cursor.execute(
            "UPDATE execution_attempts SET lease_expires_at = %s WHERE id = %s",
            (datetime.now(UTC) - timedelta(seconds=5), stale_attempt),
        )
    expired = store.reconcile(observed_at=datetime.now(UTC), request_id="reconcile-lease")
    assert expired == ("EXPIRED_LEASE_FENCED_AND_RETRIED",)
    with pytest.raises(ExecutionControlFailure, match="STALE_FENCING_TOKEN"):
        store.publish_attempt_state(
            stale_attempt,
            fencing_token=stale_token,
            state="SUCCEEDED",
            worker_id="expired-worker",
            reason="LATE_SUCCESS",
            request_id="late-success",
        )
    actor = execution_actor(execution_runtime)
    _, attempts = store.get_run(actor, "workspace", run.run_id)
    assert len(attempts) == 2
    assert attempts[1].retry_of_id == stale_attempt
    assert attempts[0].state == "RETRY_WAIT"


def test_reconciliation_repairs_incomplete_delivery_and_unfinished_aggregate(
    execution_runtime: ExecutionRuntime,
) -> None:
    _, store = api(execution_runtime)
    run = store.create_run(
        workspace_id=execution_runtime.workspace_id,
        owner_principal_id=execution_runtime.owner.principal_id,
        execution_kind="analytics",
        safe_title="Incomplete aggregate",
        request_id="seed-incomplete",
        policy_version="policy-v1",
    )
    selected = store.pending_outbox()
    assert len(selected) == 1
    with execution_runtime.connect() as connection, connection.transaction(), connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE execution_outbox SET updated_at = CURRENT_TIMESTAMP - interval '5 seconds'
            WHERE run_id = %s
            """,
            (run.run_id,),
        )
        cursor.execute(
            "UPDATE execution_attempts SET state = 'SUCCEEDED' WHERE run_id = %s",
            (run.run_id,),
        )
        cursor.execute(
            "UPDATE execution_runs SET state = 'RUNNING' WHERE id = %s",
            (run.run_id,),
        )
    findings = store.reconcile(observed_at=datetime.now(UTC), request_id="reconcile-incomplete")
    assert findings == (
        "INCOMPLETE_DELIVERY_COMMIT_REPAIRED",
        "UNFINISHED_AGGREGATE_REPAIRED",
    )
    actor = execution_actor(execution_runtime)
    repaired, _ = store.get_run(actor, "workspace", run.run_id)
    assert repaired.state == "SUCCEEDED"


def test_concurrent_terminal_publication_preserves_one_immutable_result(
    execution_runtime: ExecutionRuntime,
) -> None:
    _, store = api(execution_runtime)
    run = store.create_run(
        workspace_id=execution_runtime.workspace_id,
        owner_principal_id=execution_runtime.owner.principal_id,
        execution_kind="analytics",
        safe_title="Concurrent completion",
        request_id="seed-concurrency",
        policy_version="policy-v1",
    )
    actor = execution_actor(execution_runtime)
    _, attempts = store.get_run(actor, "workspace", run.run_id)
    claimed = store.claim_attempt(
        attempts[0].attempt_id,
        worker_id="race-worker",
        lease_seconds=30,
        request_id="race-claim",
    )

    def publish(state: str) -> str:
        try:
            result = store.publish_attempt_state(
                claimed.attempt_id,
                fencing_token=claimed.fencing_token,
                state=state,
                worker_id=f"race-{state.casefold()}",
                reason=f"RACE_{state}",
                request_id=f"race-{state.casefold()}",
            )
            return result.state
        except ExecutionControlFailure as exc:
            return exc.code

    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = set(pool.map(publish, ("SUCCEEDED", "FAILED")))

    assert len(outcomes.intersection({"SUCCEEDED", "FAILED"})) == 1
    assert "TERMINAL_STATE_IMMUTABLE" in outcomes


def test_resource_breach_envelope_and_driver_cancel_plus_hard_process_stop(
    execution_runtime: ExecutionRuntime,
) -> None:
    client, store = api(execution_runtime)
    run = store.create_run(
        workspace_id=execution_runtime.workspace_id,
        owner_principal_id=execution_runtime.owner.principal_id,
        execution_kind="ingestion",
        safe_title="Bounded extraction",
        request_id="seed-resource",
        policy_version="policy-v1",
    )
    actor = execution_actor(execution_runtime)
    _, attempts = store.get_run(actor, "workspace", run.run_id)
    claimed = store.claim_attempt(
        attempts[0].attempt_id,
        worker_id="resource-worker",
        lease_seconds=30,
        request_id="resource-claim",
    )
    store.publish_attempt_state(
        claimed.attempt_id,
        fencing_token=claimed.fencing_token,
        state="FAILED",
        worker_id="resource-worker",
        reason="RESOURCE_LIMIT_EXCEEDED",
        request_id="resource-failure",
        failure_code="RESOURCE_LIMIT_EXCEEDED",
        observed_limit=2048,
        configured_limit=1024,
        safe_remediation="Reduce batch size or request a bounded workspace quota change.",
    )
    detail = client.get(f"/runs/{run.run_id}", headers=headers("operator"))
    assert detail.status_code == 200
    attempt = detail.json()["attempts"][0]
    assert attempt["failure_code"] == "RESOURCE_LIMIT_EXCEEDED"
    assert attempt["observed_limit"] == 2048
    assert attempt["configured_limit"] == 1024
    assert "batch size" in attempt["safe_remediation"]

    database = execution_runtime.connect()
    process = get_context("spawn").Process(target=time.sleep, args=(30,))
    process.start()
    cleaned: list[str] = []
    try:
        with ThreadPoolExecutor(max_workers=1) as pool:
            sleeping = pool.submit(database.execute, "SELECT pg_sleep(10)")
            time.sleep(0.1)
            controller = IsolatedAttemptController(
                process=process,
                cancel_database_statement=database.cancel_safe,
                cleanup_uncommitted=lambda: cleaned.append("cleanup"),
            )
            assert controller.cancel(grace_seconds=0.1) is True
            with pytest.raises(Exception, match="canceling statement"):
                sleeping.result(timeout=3)
    finally:
        if process.is_alive():
            process.terminate()
            process.join(timeout=1)
        database.close()
    assert process.exitcode is not None
    assert cleaned == ["cleanup"]


def test_z_real_postgresql_migration_repeat_downgrade_and_reupgrade(
    execution_boundaries: ExecutionBoundaries,
) -> None:
    arguments: MigrationArguments = {
        "host": execution_boundaries.database_host,
        "port": execution_boundaries.database_port,
        "database": "custometry",
        "user": "custometry",
        "password_file": execution_boundaries.database_password_file,
    }
    migrate(**arguments, revision="head")
    migrate(**arguments, revision="-0007_contributor_projection")
    with execution_boundaries.connect() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT to_regclass('public.execution_runs')")
        assert cursor.fetchone() == (None,)
    migrate(**arguments, revision="head")
    with execution_boundaries.connect() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT version_num FROM alembic_version")
        assert cursor.fetchone() == ("0009_notifications",)
