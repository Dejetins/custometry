# pyright: reportUnknownMemberType=false
from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import pytest

from packages.contracts.execution import (
    ExecutionActor,
    ExecutionControlFailure,
    ExecutionTerminalEventOutboxPort,
)
from packages.execution.domain.model import AttemptRecord
from packages.execution.infrastructure.control_postgres import PostgresExecutionControlStore
from tests.integration.execution_control.conftest import ExecutionRuntime


def actor(runtime: ExecutionRuntime) -> ExecutionActor:
    return ExecutionActor(
        runtime.operator.principal_id,
        runtime.workspace_id,
        runtime.operator.permissions,
        "policy-integration-v1",
    )


def deliver_and_claim(
    store: PostgresExecutionControlStore, run_id: UUID, execution_actor: ExecutionActor
) -> AttemptRecord:
    commands = store.pending_outbox()
    command = next(row for row in commands if UUID(str(row["run_id"])) == run_id)
    assert command["command_type"] == "execute"
    store.mark_outbox_published(UUID(str(command["id"])))
    _, attempts = store.get_run(execution_actor, "workspace", run_id)
    return store.claim_attempt(
        attempts[-1].attempt_id,
        worker_id="w38-disposable-worker",
        lease_seconds=30,
        request_id=f"claim-{run_id}",
    )


def test_failed_event_is_durable_redacted_duplicate_safe_and_command_isolated(
    execution_runtime: ExecutionRuntime,
) -> None:
    store = PostgresExecutionControlStore(execution_runtime.connect)
    port: ExecutionTerminalEventOutboxPort = store
    execution_actor = actor(execution_runtime)
    run = store.create_run(
        workspace_id=execution_runtime.workspace_id,
        owner_principal_id=execution_runtime.owner.principal_id,
        execution_kind="analytics",
        safe_title="Customer alice@example.test secret-token https://unsafe.test",
        safe_trace_id="trace-w38-failed",
        request_id="seed-w38-failed",
        policy_version="policy-v1",
    )
    claimed = deliver_and_claim(store, run.run_id, execution_actor)
    terminal = store.publish_attempt_state(
        claimed.attempt_id,
        fencing_token=claimed.fencing_token,
        state="FAILED",
        worker_id="w38-failure-worker",
        reason="raw provider failure alice@example.test https://unsafe.test secret-token",
        request_id="w38-failed",
    )
    assert terminal.state == "FAILED"

    assert store.pending_outbox() == ()
    events = port.claim_terminal_events()
    assert len(events) == 1
    event = events[0]
    assert event.event_type == "execution.run.failed"
    assert event.event_version == "1.0.0"
    assert event.workspace_id == execution_runtime.workspace_id
    assert event.resource_id == run.run_id == event.run_id
    assert event.attempt_id == claimed.attempt_id
    assert event.status_code == "FAILED"
    assert event.reason_code == "EXECUTION_FAILED"
    assert event.message_code == "RUN_FAILED"
    assert event.group_key == f"execution-run:{run.run_id}"
    assert event.route_id == "UI-OPS-002"
    assert dict(event.route_parameters) == {"run_id": str(run.run_id)}
    assert event.trace_id == "trace-w38-failed"
    event_text = repr(event)
    assert "alice@example.test" not in event_text
    assert "https://unsafe.test" not in event_text
    assert "secret-token" not in event_text

    with pytest.raises(ExecutionControlFailure, match="OUTBOX_STATE_CONFLICT"):
        store.mark_outbox_published(event.event_id)
    port.release_terminal_event(event.event_id, "CONSUMER_UNAVAILABLE")
    with (
        execution_runtime.connect() as connection,
        connection.transaction(),
        connection.cursor() as cursor,
    ):
        cursor.execute(
            "UPDATE execution_outbox SET available_at = CURRENT_TIMESTAMP WHERE id = %s",
            (event.event_id,),
        )
    replay = port.claim_terminal_events()
    assert len(replay) == 1
    assert replay[0].event_id == event.event_id
    port.mark_terminal_event_published(event.event_id)

    store.publish_attempt_state(
        claimed.attempt_id,
        fencing_token=claimed.fencing_token,
        state="FAILED",
        worker_id="w38-failure-worker",
        reason="different replay reason that must not create another event",
        request_id="w38-failed-replay",
    )
    assert port.claim_terminal_events() == ()
    with execution_runtime.connect() as connection, connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT count(*), min(payload->>'workspace_id'), max(payload->>'workspace_id')
            FROM execution_outbox WHERE command_type = 'event.execution.failed.v1'
              AND run_id = %s
            """,
            (run.run_id,),
        )
        count_row = cursor.fetchone()
    assert count_row is not None
    count, minimum_workspace, maximum_workspace = count_row
    assert count == 1
    assert minimum_workspace == maximum_workspace == str(execution_runtime.workspace_id)

    other_workspace = uuid4()
    with (
        execution_runtime.connect() as connection,
        connection.transaction(),
        connection.cursor() as cursor,
    ):
        cursor.execute(
            """
            INSERT INTO identity_workspaces (id, key, name, active)
            VALUES (%s, %s, 'W38 Isolated Workspace', true)
            """,
            (other_workspace, f"w38-isolated-{other_workspace.hex[:16]}"),
        )
    other_actor = ExecutionActor(
        execution_runtime.operator.principal_id,
        other_workspace,
        execution_runtime.operator.permissions,
        "policy-isolated-v1",
    )
    other_run = store.create_run(
        workspace_id=other_workspace,
        owner_principal_id=execution_runtime.owner.principal_id,
        execution_kind="analytics",
        safe_title="Isolated workspace failure",
        request_id="seed-w38-isolated",
        policy_version="policy-isolated-v1",
    )
    other_attempt = deliver_and_claim(store, other_run.run_id, other_actor)
    store.publish_attempt_state(
        other_attempt.attempt_id,
        fencing_token=other_attempt.fencing_token,
        state="FAILED",
        worker_id="w38-isolated-worker",
        reason="ISOLATED_FAILURE",
        request_id="w38-isolated-failed",
    )
    isolated_event = port.claim_terminal_events()[0]
    assert isolated_event.workspace_id == other_workspace
    assert isolated_event.run_id == other_run.run_id
    assert str(execution_runtime.workspace_id) not in repr(isolated_event)
    port.mark_terminal_event_published(isolated_event.event_id)
    with (
        execution_runtime.connect() as connection,
        connection.transaction(),
        connection.cursor() as cursor,
    ):
        cursor.execute("DELETE FROM identity_workspaces WHERE id = %s", (other_workspace,))


def test_stuck_event_is_published_with_retry_command_but_never_claimed_as_a_command(
    execution_runtime: ExecutionRuntime,
) -> None:
    store = PostgresExecutionControlStore(execution_runtime.connect)
    execution_actor = actor(execution_runtime)
    run = store.create_run(
        workspace_id=execution_runtime.workspace_id,
        owner_principal_id=execution_runtime.owner.principal_id,
        execution_kind="ingestion",
        safe_title="Lease expiry",
        request_id="seed-w38-stuck",
        policy_version="policy-v1",
    )
    claimed = deliver_and_claim(store, run.run_id, execution_actor)
    observed_at = datetime.now(UTC)
    with (
        execution_runtime.connect() as connection,
        connection.transaction(),
        connection.cursor() as cursor,
    ):
        cursor.execute(
            "UPDATE execution_attempts SET lease_expires_at = %s WHERE id = %s",
            (observed_at - timedelta(seconds=5), claimed.attempt_id),
        )
    assert store.reconcile(observed_at=observed_at, request_id="w38-stuck") == (
        "EXPIRED_LEASE_FENCED_AND_RETRIED",
    )

    commands = store.pending_outbox()
    assert len(commands) == 1
    assert commands[0]["command_type"] == "execute"
    assert UUID(str(commands[0]["attempt_id"])) != claimed.attempt_id
    events = store.claim_terminal_events()
    assert len(events) == 1
    event = events[0]
    assert event.event_type == "execution.run.stuck"
    assert event.status_code == "STUCK"
    assert event.reason_code == "LEASE_EXPIRED"
    assert event.attempt_id == claimed.attempt_id
    assert event.workspace_id == execution_runtime.workspace_id


def test_reconciled_terminal_failure_publishes_event_in_the_repair_transaction(
    execution_runtime: ExecutionRuntime,
) -> None:
    store = PostgresExecutionControlStore(execution_runtime.connect)
    execution_actor = actor(execution_runtime)
    run = store.create_run(
        workspace_id=execution_runtime.workspace_id,
        owner_principal_id=execution_runtime.owner.principal_id,
        execution_kind="pipeline",
        safe_title="Reconciled failure",
        request_id="seed-w38-reconciled-failure",
        policy_version="policy-v1",
    )
    _, attempts = store.get_run(execution_actor, "workspace", run.run_id)
    with (
        execution_runtime.connect() as connection,
        connection.transaction(),
        connection.cursor() as cursor,
    ):
        cursor.execute(
            "UPDATE execution_attempts SET state = 'FAILED' WHERE id = %s",
            (attempts[0].attempt_id,),
        )
        cursor.execute(
            "UPDATE execution_runs SET state = 'RUNNING' WHERE id = %s",
            (run.run_id,),
        )
    observed_at = datetime.now(UTC)
    assert store.reconcile(observed_at=observed_at, request_id="w38-reconcile-terminal") == (
        "UNFINISHED_AGGREGATE_REPAIRED",
    )
    events = store.claim_terminal_events()
    assert len(events) == 1
    assert events[0].event_type == "execution.run.failed"
    assert events[0].run_id == run.run_id
    assert events[0].attempt_id == attempts[0].attempt_id
    assert events[0].occurred_at == observed_at


def test_manual_retry_success_publishes_recovered_and_plain_success_or_cancel_do_not(
    execution_runtime: ExecutionRuntime,
) -> None:
    store = PostgresExecutionControlStore(execution_runtime.connect)
    execution_actor = actor(execution_runtime)
    failed_run = store.create_run(
        workspace_id=execution_runtime.workspace_id,
        owner_principal_id=execution_runtime.owner.principal_id,
        execution_kind="analytics",
        safe_title="Recoverable run",
        request_id="seed-w38-recovered",
        policy_version="policy-v1",
    )
    failed_attempt = deliver_and_claim(store, failed_run.run_id, execution_actor)
    store.publish_attempt_state(
        failed_attempt.attempt_id,
        fencing_token=failed_attempt.fencing_token,
        state="FAILED",
        worker_id="w38-failure-worker",
        reason="SAFE_FAILURE",
        request_id="w38-source-failed",
    )
    failed_event = store.claim_terminal_events()[0]
    store.mark_terminal_event_published(failed_event.event_id)

    retry = store.retry(
        execution_actor,
        "workspace",
        run_id=failed_run.run_id,
        expected_revision=3,
        mode="failed_nodes",
        reason="bounded retry after remediation",
        request_id="w38-retry",
        idempotency_key="w38-retry-key",
        payload_hash="a" * 64,
    )
    retry_attempt = deliver_and_claim(store, retry.run_id, execution_actor)
    recovered_run = store.publish_attempt_state(
        retry_attempt.attempt_id,
        fencing_token=retry_attempt.fencing_token,
        state="SUCCEEDED",
        worker_id="w38-recovery-worker",
        reason="RETRY_COMPLETE",
        request_id="w38-recovered",
    )
    assert recovered_run.state == "SUCCEEDED"
    recovered = store.claim_terminal_events()
    assert len(recovered) == 1
    event = recovered[0]
    assert event.event_type == "execution.run.recovered"
    assert event.retry_of_run_id == failed_run.run_id
    assert event.retry_of_attempt_id == failed_attempt.attempt_id
    assert event.group_key == failed_event.group_key
    assert event.message_code == "RUN_RECOVERED"

    plain = store.create_run(
        workspace_id=execution_runtime.workspace_id,
        owner_principal_id=execution_runtime.owner.principal_id,
        execution_kind="analytics",
        safe_title="Plain success",
        request_id="seed-w38-plain",
        policy_version="policy-v1",
    )
    plain_attempt = deliver_and_claim(store, plain.run_id, execution_actor)
    store.publish_attempt_state(
        plain_attempt.attempt_id,
        fencing_token=plain_attempt.fencing_token,
        state="SUCCEEDED",
        worker_id="w38-success-worker",
        reason="SUCCESS",
        request_id="w38-plain-success",
    )
    assert store.claim_terminal_events() == ()

    cancelled = store.create_run(
        workspace_id=execution_runtime.workspace_id,
        owner_principal_id=execution_runtime.owner.principal_id,
        execution_kind="ingestion",
        safe_title="Cancelled run",
        request_id="seed-w38-cancelled",
        policy_version="policy-v1",
    )
    cancelled_attempt = deliver_and_claim(store, cancelled.run_id, execution_actor)
    store.publish_attempt_state(
        cancelled_attempt.attempt_id,
        fencing_token=cancelled_attempt.fencing_token,
        state="CANCELLED",
        worker_id="w38-cancel-worker",
        reason="CANCEL_CLEANUP_COMPLETE",
        request_id="w38-cancelled",
    )
    assert store.claim_terminal_events() == ()
