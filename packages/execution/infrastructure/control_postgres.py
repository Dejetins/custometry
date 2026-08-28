"""PostgreSQL state truth for the operator execution-control API."""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any, Literal, cast
from uuid import UUID, uuid4, uuid5

from psycopg import Connection
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from packages.contracts.execution import (
    ExecutionActor,
    ExecutionControlFailure,
    ExecutionTerminalEvent,
    ExecutionTerminalEventType,
    ExecutionTerminalSeverity,
    ExecutionTerminalStatus,
    VisibilityScope,
)
from packages.execution.domain.model import (
    AttemptRecord,
    QueueSummary,
    RetryMode,
    RunQuery,
    RunRecord,
    TERMINAL_RUN_STATES,
    can_transition,
)


Connect = Callable[[], Connection[Any]]
TERMINAL_EVENT_NAMESPACE = UUID("94d68fc8-568a-4c76-9682-e12eb459d861")
TERMINAL_EVENT_COMMANDS = frozenset(
    {
        "event.execution.failed.v1",
        "event.execution.stuck.v1",
        "event.execution.recovered.v1",
    }
)


class PostgresExecutionControlStore:
    """Persist CAS transitions, audit history, idempotency, and outbox atomically."""

    def __init__(self, connect: Connect) -> None:
        self._connect = connect

    @staticmethod
    def _run(row: Any) -> RunRecord:
        return RunRecord(
            run_id=UUID(str(row["id"])),
            workspace_id=UUID(str(row["workspace_id"])),
            owner_principal_id=UUID(str(row["owner_principal_id"])),
            execution_kind=str(row["execution_kind"]),
            lane=str(row["lane"]),
            safe_title=str(row["safe_title"]),
            safe_trace_id=(None if row["safe_trace_id"] is None else str(row["safe_trace_id"])),
            state=str(row["state"]),  # type: ignore[arg-type]
            revision=int(row["revision"]),
            retry_of_id=(None if row["retry_of_id"] is None else UUID(str(row["retry_of_id"]))),
            retry_mode=(None if row["retry_mode"] is None else str(row["retry_mode"])),  # type: ignore[arg-type]
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    @staticmethod
    def _attempt(row: Any) -> AttemptRecord:
        return AttemptRecord(
            attempt_id=UUID(str(row["id"])),
            run_id=UUID(str(row["run_id"])),
            state=str(row["state"]),  # type: ignore[arg-type]
            attempt_number=int(row["attempt_number"]),
            fencing_token=int(row["fencing_token"]),
            retry_of_id=(None if row["retry_of_id"] is None else UUID(str(row["retry_of_id"]))),
            lease_expires_at=row["lease_expires_at"],
            failure_code=(None if row["failure_code"] is None else str(row["failure_code"])),
            observed_limit=(
                None if row["observed_limit"] is None else int(row["observed_limit"])
            ),
            configured_limit=(
                None if row["configured_limit"] is None else int(row["configured_limit"])
            ),
            safe_remediation=(
                None if row["safe_remediation"] is None else str(row["safe_remediation"])
            ),
        )

    @staticmethod
    def _terminal_event_from_row(row: Any) -> ExecutionTerminalEvent:
        payload = dict(row["payload"])
        return ExecutionTerminalEvent(
            event_id=UUID(str(row["id"])),
            event_type=cast(ExecutionTerminalEventType, str(payload["event_type"])),
            event_version="1.0.0",
            source_owner="execution",
            workspace_id=UUID(str(row["workspace_id"])),
            resource_type="run",
            resource_id=UUID(str(payload["resource_id"])),
            run_id=UUID(str(row["run_id"])),
            attempt_id=UUID(str(row["attempt_id"])),
            retry_of_run_id=(
                None
                if payload.get("retry_of_run_id") is None
                else UUID(str(payload["retry_of_run_id"]))
            ),
            retry_of_attempt_id=(
                None
                if payload.get("retry_of_attempt_id") is None
                else UUID(str(payload["retry_of_attempt_id"]))
            ),
            status_code=cast(ExecutionTerminalStatus, str(payload["status_code"])),
            reason_code=str(payload["reason_code"]),
            severity=cast(ExecutionTerminalSeverity, str(payload["severity"])),
            category="execution",
            occurred_at=datetime.fromisoformat(str(payload["occurred_at"])),
            message_code=cast(
                Literal["RUN_FAILED", "RUN_STUCK", "RUN_RECOVERED"],
                str(payload["message_code"]),
            ),
            message_parameters=tuple(
                sorted(
                    (str(key), str(value))
                    for key, value in dict(payload["message_parameters"]).items()
                )
            ),
            group_key=str(payload["group_key"]),
            route_id="UI-OPS-002",
            route_parameters=tuple(
                sorted(
                    (str(key), str(value))
                    for key, value in dict(payload["route_parameters"]).items()
                )
            ),
            trace_id=None if payload.get("trace_id") is None else str(payload["trace_id"]),
        )

    @staticmethod
    def _visibility(scope: VisibilityScope) -> str:
        return "" if scope == "workspace" else " AND owner_principal_id = %s"

    @staticmethod
    def _visibility_values(actor: ExecutionActor, scope: VisibilityScope) -> tuple[UUID, ...]:
        return () if scope == "workspace" else (actor.principal_id,)

    @staticmethod
    def _history(
        cursor: Any,
        *,
        workspace_id: UUID,
        run_id: UUID,
        attempt_id: UUID | None,
        previous_state: str | None,
        new_state: str,
        actor_or_service: str,
        reason: str,
        request_id: str,
    ) -> None:
        cursor.execute(
            """
            INSERT INTO execution_transition_history
              (id, workspace_id, run_id, attempt_id, previous_state, new_state,
               actor_or_service, reason_code, request_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                uuid4(),
                workspace_id,
                run_id,
                attempt_id,
                previous_state,
                new_state,
                actor_or_service,
                reason,
                request_id,
            ),
        )

    @staticmethod
    def _outbox(
        cursor: Any,
        *,
        workspace_id: UUID,
        run_id: UUID,
        attempt_id: UUID | None,
        command_type: str,
        payload: dict[str, object],
    ) -> None:
        cursor.execute(
            """
            INSERT INTO execution_outbox
              (id, workspace_id, run_id, attempt_id, command_type, payload, state, available_at)
            VALUES (%s, %s, %s, %s, %s, %s, 'pending', CURRENT_TIMESTAMP)
            ON CONFLICT (run_id, attempt_id, command_type) DO UPDATE SET
              payload = EXCLUDED.payload, state = 'pending', available_at = CURRENT_TIMESTAMP,
              updated_at = CURRENT_TIMESTAMP, last_error_code = NULL
            """,
            (uuid4(), workspace_id, run_id, attempt_id, command_type, Jsonb(payload)),
        )

    @staticmethod
    def _terminal_event(
        cursor: Any,
        *,
        event_type: ExecutionTerminalEventType,
        workspace_id: UUID,
        run_id: UUID,
        attempt_id: UUID,
        retry_of_run_id: UUID | None,
        retry_of_attempt_id: UUID | None,
        status_code: ExecutionTerminalStatus,
        reason_code: str,
        severity: ExecutionTerminalSeverity,
        occurred_at: datetime,
        trace_id: str | None,
    ) -> None:
        suffix = event_type.rsplit(".", maxsplit=1)[-1]
        command_type = f"event.execution.{suffix}.v1"
        event_id = uuid5(
            TERMINAL_EVENT_NAMESPACE,
            f"1.0.0:{workspace_id}:{run_id}:{attempt_id}:{event_type}",
        )
        cursor.execute(
            """
            WITH RECURSIVE lineage AS (
              SELECT id, retry_of_id FROM execution_runs WHERE id = %s
              UNION ALL
              SELECT parent.id, parent.retry_of_id
              FROM execution_runs AS parent
              JOIN lineage AS child ON child.retry_of_id = parent.id
            )
            SELECT id FROM lineage WHERE retry_of_id IS NULL LIMIT 1
            """,
            (run_id,),
        )
        root = cursor.fetchone()
        group_run_id = UUID(str(root["id"])) if root is not None else (retry_of_run_id or run_id)
        message_code = cast(
            Literal["RUN_FAILED", "RUN_STUCK", "RUN_RECOVERED"],
            f"RUN_{status_code}",
        )
        payload: dict[str, object] = {
            "event_id": str(event_id),
            "event_type": event_type,
            "event_version": "1.0.0",
            "source_owner": "execution",
            "workspace_id": str(workspace_id),
            "resource_type": "run",
            "resource_id": str(run_id),
            "run_id": str(run_id),
            "attempt_id": str(attempt_id),
            "retry_of_run_id": None if retry_of_run_id is None else str(retry_of_run_id),
            "retry_of_attempt_id": (
                None if retry_of_attempt_id is None else str(retry_of_attempt_id)
            ),
            "status_code": status_code,
            "reason_code": reason_code,
            "severity": severity,
            "category": "execution",
            "occurred_at": occurred_at.astimezone(UTC).isoformat(),
            "message_code": message_code,
            "message_parameters": {"status_code": status_code, "reason_code": reason_code},
            "group_key": f"execution-run:{group_run_id}",
            "route_id": "UI-OPS-002",
            "route_parameters": {"run_id": str(run_id)},
            "trace_id": trace_id,
        }
        cursor.execute(
            """
            INSERT INTO execution_outbox
              (id, workspace_id, run_id, attempt_id, command_type, payload, state, available_at)
            VALUES (%s, %s, %s, %s, %s, %s, 'pending', CURRENT_TIMESTAMP)
            ON CONFLICT (run_id, attempt_id, command_type) DO NOTHING
            """,
            (event_id, workspace_id, run_id, attempt_id, command_type, Jsonb(payload)),
        )

    def create_run(
        self,
        *,
        workspace_id: UUID,
        owner_principal_id: UUID,
        execution_kind: str,
        lane: str = "default",
        safe_title: str,
        request_id: str,
        policy_version: str,
        safe_trace_id: str | None = None,
        state: str = "QUEUED",
    ) -> RunRecord:
        """Public owner-context command used by orchestrators, not by the query API."""

        if state not in {"CREATED", "VALIDATING", "QUEUED"}:
            raise ExecutionControlFailure("INVALID_INITIAL_STATE")
        run_id = uuid4()
        attempt_id = uuid4()
        with (
            self._connect() as connection,
            connection.transaction(),
            connection.cursor(row_factory=dict_row) as cursor,
        ):
            cursor.execute(
                """
                INSERT INTO execution_runs
                  (id, workspace_id, owner_principal_id, execution_kind, lane, safe_title,
                   safe_trace_id, state, revision, policy_version, last_request_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 1, %s, %s)
                RETURNING *
                """,
                (
                    run_id,
                    workspace_id,
                    owner_principal_id,
                    execution_kind,
                    lane,
                    safe_title,
                    safe_trace_id,
                    state,
                    policy_version,
                    request_id,
                ),
            )
            row = cursor.fetchone()
            cursor.execute(
                """
                INSERT INTO execution_attempts
                  (id, run_id, workspace_id, attempt_number, state, fencing_token)
                VALUES (%s, %s, %s, 1, 'READY', 0)
                """,
                (attempt_id, run_id, workspace_id),
            )
            self._history(
                cursor,
                workspace_id=workspace_id,
                run_id=run_id,
                attempt_id=None,
                previous_state=None,
                new_state=state,
                actor_or_service="orchestrator",
                reason="RUN_CREATED",
                request_id=request_id,
            )
            self._outbox(
                cursor,
                workspace_id=workspace_id,
                run_id=run_id,
                attempt_id=attempt_id,
                command_type="execute",
                payload={
                    "workspace_id": str(workspace_id),
                    "run_id": str(run_id),
                    "attempt_id": str(attempt_id),
                    "policy_version": policy_version,
                },
            )
        assert row is not None
        return self._run(row)

    def list_runs(
        self, actor: ExecutionActor, scope: VisibilityScope, query: RunQuery
    ) -> tuple[tuple[RunRecord, ...], int]:
        where = ["workspace_id = %s"]
        values: list[object] = [actor.workspace_id]
        if scope == "owner":
            where.append("owner_principal_id = %s")
            values.append(actor.principal_id)
        if query.states:
            where.append("state = ANY(%s)")
            values.append(list(query.states))
        if query.execution_kind is not None:
            where.append("execution_kind = %s")
            values.append(query.execution_kind)
        if query.owner_principal_id is not None:
            where.append("owner_principal_id = %s")
            values.append(query.owner_principal_id)
        if query.created_from is not None:
            where.append("created_at >= %s")
            values.append(query.created_from)
        if query.created_to is not None:
            where.append("created_at < %s")
            values.append(query.created_to)
        if query.safe_trace_id is not None:
            where.append("safe_trace_id = %s")
            values.append(query.safe_trace_id)
        predicate = " AND ".join(where)
        with self._connect() as connection, connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f"SELECT count(*) AS count FROM execution_runs WHERE {predicate}", values)
            count_row = cursor.fetchone()
            cursor.execute(
                f"""
                SELECT * FROM execution_runs WHERE {predicate}
                ORDER BY created_at DESC, id DESC OFFSET %s LIMIT %s
                """,
                (*values, query.offset, query.limit),
            )
            rows = cursor.fetchall()
        assert count_row is not None
        return tuple(self._run(row) for row in rows), int(count_row["count"])

    def queue_summary(
        self, actor: ExecutionActor, scope: VisibilityScope
    ) -> QueueSummary:
        suffix = self._visibility(scope)
        values = (actor.workspace_id, *self._visibility_values(actor, scope))
        with self._connect() as connection, connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                f"""
                SELECT state, count(*) AS count,
                       min(created_at) FILTER (WHERE state = 'QUEUED') AS oldest_queued
                FROM execution_runs WHERE workspace_id = %s{suffix} GROUP BY state
                """,
                values,
            )
            rows = cursor.fetchall()
            cursor.execute(
                f"""
                SELECT lane, count(*) AS count FROM execution_runs
                WHERE workspace_id = %s{suffix} GROUP BY lane
                """,
                values,
            )
            lane_rows = cursor.fetchall()
        observed_at = datetime.now(UTC)
        counts = {str(row["state"]): int(row["count"]) for row in rows}
        oldest_values = [row["oldest_queued"] for row in rows if row["oldest_queued"] is not None]
        age = None
        if oldest_values:
            age = max(0, int((observed_at - min(oldest_values)).total_seconds()))
        lane_counts = {str(row["lane"]): int(row["count"]) for row in lane_rows}
        return QueueSummary(
            counts=counts,
            lane_counts=lane_counts,
            oldest_queued_age_seconds=age,
            observed_at=observed_at,
            freshness="fresh",
        )

    def get_run(
        self, actor: ExecutionActor, scope: VisibilityScope, run_id: UUID
    ) -> tuple[RunRecord, tuple[AttemptRecord, ...]]:
        with (
            self._connect() as connection,
            connection.transaction(),
            connection.cursor(row_factory=dict_row) as cursor,
        ):
            run = self._visible_run(cursor, actor, scope, run_id)
            cursor.execute(
                """
                SELECT * FROM execution_attempts WHERE run_id = %s
                ORDER BY attempt_number, id
                """,
                (run_id,),
            )
            attempts = cursor.fetchall()
        return self._run(run), tuple(self._attempt(row) for row in attempts)

    @staticmethod
    def _visible_run(
        cursor: Any,
        actor: ExecutionActor,
        scope: VisibilityScope,
        run_id: UUID,
    ) -> Any:
        suffix = "" if scope == "workspace" else " AND owner_principal_id = %s"
        values: tuple[object, ...] = (run_id, actor.workspace_id)
        if scope == "owner":
            values = (*values, actor.principal_id)
        cursor.execute(
            f"SELECT * FROM execution_runs WHERE id = %s AND workspace_id = %s{suffix} FOR UPDATE",
            values,
        )
        row = cursor.fetchone()
        if row is None:
            raise ExecutionControlFailure("NOT_FOUND")
        return row

    @staticmethod
    def _replay(
        cursor: Any,
        actor: ExecutionActor,
        *,
        route: str,
        key: str,
        payload_hash: str,
    ) -> Any | None:
        cursor.execute(
            """
            SELECT payload_hash, response_run_id FROM execution_idempotency
            WHERE workspace_id = %s AND actor_id = %s AND route = %s
              AND idempotency_key = %s FOR UPDATE
            """,
            (actor.workspace_id, actor.principal_id, route, key),
        )
        replay = cursor.fetchone()
        if replay is None:
            return None
        if str(replay["payload_hash"]) != payload_hash:
            raise ExecutionControlFailure("IDEMPOTENCY_CONFLICT")
        cursor.execute("SELECT * FROM execution_runs WHERE id = %s", (replay["response_run_id"],))
        return cursor.fetchone()

    @staticmethod
    def _remember(
        cursor: Any,
        actor: ExecutionActor,
        *,
        route: str,
        key: str,
        payload_hash: str,
        response_run_id: UUID,
    ) -> None:
        cursor.execute(
            """
            INSERT INTO execution_idempotency
              (workspace_id, actor_id, route, idempotency_key, payload_hash, response_run_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (actor.workspace_id, actor.principal_id, route, key, payload_hash, response_run_id),
        )

    def cancel(
        self,
        actor: ExecutionActor,
        scope: VisibilityScope,
        *,
        run_id: UUID,
        expected_revision: int,
        reason: str,
        request_id: str,
        idempotency_key: str,
        payload_hash: str,
    ) -> RunRecord:
        with (
            self._connect() as connection,
            connection.transaction(),
            connection.cursor(row_factory=dict_row) as cursor,
        ):
            replay = self._replay(
                cursor,
                actor,
                route="cancel",
                key=idempotency_key,
                payload_hash=payload_hash,
            )
            if replay is not None:
                return self._run(replay)
            row = self._visible_run(cursor, actor, scope, run_id)
            previous = str(row["state"])
            revision = int(row["revision"])
            if previous not in TERMINAL_RUN_STATES and previous != "CANCELLING":
                if revision != expected_revision:
                    raise ExecutionControlFailure("STALE_REVISION", current_state=previous)
                if not can_transition(previous, "CANCELLING"):
                    raise ExecutionControlFailure("INVALID_TRANSITION", current_state=previous)
                cursor.execute(
                    """
                    UPDATE execution_runs SET state = 'CANCELLING', revision = revision + 1,
                      last_request_id = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s AND revision = %s RETURNING *
                    """,
                    (request_id, run_id, expected_revision),
                )
                row = cursor.fetchone()
                if row is None:
                    raise ExecutionControlFailure("STALE_REVISION", current_state=previous)
                self._history(
                    cursor,
                    workspace_id=actor.workspace_id,
                    run_id=run_id,
                    attempt_id=None,
                    previous_state=previous,
                    new_state="CANCELLING",
                    actor_or_service=str(actor.principal_id),
                    reason=reason,
                    request_id=request_id,
                )
                cursor.execute(
                    """
                    UPDATE execution_attempts SET cancellation_requested = TRUE,
                      fencing_token = fencing_token + 1, updated_at = CURRENT_TIMESTAMP
                    WHERE run_id = %s AND state IN ('PENDING','READY','RUNNING','RETRY_WAIT')
                    RETURNING id, fencing_token
                    """,
                    (run_id,),
                )
                attempts = cursor.fetchall()
                if attempts:
                    for attempt in attempts:
                        self._outbox(
                            cursor,
                            workspace_id=actor.workspace_id,
                            run_id=run_id,
                            attempt_id=UUID(str(attempt["id"])),
                            command_type="cancel",
                            payload={
                                "workspace_id": str(actor.workspace_id),
                                "run_id": str(run_id),
                                "attempt_id": str(attempt["id"]),
                                "fencing_token": int(attempt["fencing_token"]),
                                "policy_version": actor.policy_version,
                            },
                        )
                else:
                    self._outbox(
                        cursor,
                        workspace_id=actor.workspace_id,
                        run_id=run_id,
                        attempt_id=None,
                        command_type="cancel",
                        payload={
                            "workspace_id": str(actor.workspace_id),
                            "run_id": str(run_id),
                            "policy_version": actor.policy_version,
                        },
                    )
            self._remember(
                cursor,
                actor,
                route="cancel",
                key=idempotency_key,
                payload_hash=payload_hash,
                response_run_id=run_id,
            )
        assert row is not None
        return self._run(row)

    def retry(
        self,
        actor: ExecutionActor,
        scope: VisibilityScope,
        *,
        run_id: UUID,
        expected_revision: int,
        mode: RetryMode,
        reason: str,
        request_id: str,
        idempotency_key: str,
        payload_hash: str,
    ) -> RunRecord:
        with (
            self._connect() as connection,
            connection.transaction(),
            connection.cursor(row_factory=dict_row) as cursor,
        ):
            replay = self._replay(
                cursor,
                actor,
                route="retry",
                key=idempotency_key,
                payload_hash=payload_hash,
            )
            if replay is not None:
                return self._run(replay)
            source = self._visible_run(cursor, actor, scope, run_id)
            source_state = str(source["state"])
            if int(source["revision"]) != expected_revision:
                raise ExecutionControlFailure("STALE_REVISION", current_state=source_state)
            eligible = {"FAILED", "CANCELLED", "PARTIAL"}
            if source_state not in eligible:
                raise ExecutionControlFailure("RETRY_NOT_ELIGIBLE", current_state=source_state)
            cursor.execute(
                """
                SELECT id FROM execution_attempts
                WHERE run_id = %s AND state IN ('FAILED','CANCELLED')
                ORDER BY attempt_number DESC LIMIT 1
                """,
                (run_id,),
            )
            failed_attempt = cursor.fetchone()
            if mode == "failed_nodes" and failed_attempt is None:
                raise ExecutionControlFailure("RETRY_NOT_ELIGIBLE", current_state=source_state)
            new_run_id = uuid4()
            new_attempt_id = uuid4()
            cursor.execute(
                """
                INSERT INTO execution_runs
                  (id, workspace_id, owner_principal_id, execution_kind, lane, safe_title,
                   safe_trace_id, state, revision, retry_of_id, retry_mode,
                   policy_version, last_request_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'CREATED', 1, %s, %s, %s, %s)
                RETURNING *
                """,
                (
                    new_run_id,
                    actor.workspace_id,
                    source["owner_principal_id"],
                    source["execution_kind"],
                    source["lane"],
                    source["safe_title"],
                    source["safe_trace_id"],
                    run_id,
                    mode,
                    actor.policy_version,
                    request_id,
                ),
            )
            new_row = cursor.fetchone()
            cursor.execute(
                """
                INSERT INTO execution_attempts
                  (id, run_id, workspace_id, attempt_number, state, fencing_token, retry_of_id)
                VALUES (%s, %s, %s, 1, 'READY', 0, %s)
                """,
                (
                    new_attempt_id,
                    new_run_id,
                    actor.workspace_id,
                    None if mode == "full_rerun" or failed_attempt is None else failed_attempt["id"],
                ),
            )
            self._history(
                cursor,
                workspace_id=actor.workspace_id,
                run_id=new_run_id,
                attempt_id=None,
                previous_state=None,
                new_state="CREATED",
                actor_or_service=str(actor.principal_id),
                reason=reason,
                request_id=request_id,
            )
            self._outbox(
                cursor,
                workspace_id=actor.workspace_id,
                run_id=new_run_id,
                attempt_id=new_attempt_id,
                command_type="execute",
                payload={
                    "workspace_id": str(actor.workspace_id),
                    "run_id": str(new_run_id),
                    "attempt_id": str(new_attempt_id),
                    "retry_of_id": str(run_id),
                    "retry_mode": mode,
                    "policy_version": actor.policy_version,
                },
            )
            self._remember(
                cursor,
                actor,
                route="retry",
                key=idempotency_key,
                payload_hash=payload_hash,
                response_run_id=new_run_id,
            )
        assert new_row is not None
        return self._run(new_row)

    def pending_outbox(self, *, limit: int = 100) -> tuple[dict[str, object], ...]:
        with (
            self._connect() as connection,
            connection.transaction(),
            connection.cursor(row_factory=dict_row) as cursor,
        ):
            cursor.execute(
                """
                SELECT * FROM execution_outbox
                WHERE command_type IN ('execute', 'cancel')
                  AND state = 'pending' AND available_at <= CURRENT_TIMESTAMP
                ORDER BY created_at FOR UPDATE SKIP LOCKED LIMIT %s
                """,
                (limit,),
            )
            rows = cursor.fetchall()
            ids = [row["id"] for row in rows]
            if ids:
                cursor.execute(
                    """
                    UPDATE execution_outbox SET state = 'publishing',
                      delivery_attempts = delivery_attempts + 1, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ANY(%s)
                    """,
                    (ids,),
                )
        return tuple(dict(row) for row in rows)

    def claim_terminal_events(self, *, limit: int = 100) -> tuple[ExecutionTerminalEvent, ...]:
        with (
            self._connect() as connection,
            connection.transaction(),
            connection.cursor(row_factory=dict_row) as cursor,
        ):
            cursor.execute(
                """
                SELECT * FROM execution_outbox
                WHERE command_type = ANY(%s)
                  AND state = 'pending' AND available_at <= CURRENT_TIMESTAMP
                ORDER BY created_at FOR UPDATE SKIP LOCKED LIMIT %s
                """,
                (list(sorted(TERMINAL_EVENT_COMMANDS)), limit),
            )
            rows = cursor.fetchall()
            ids = [row["id"] for row in rows]
            if ids:
                cursor.execute(
                    """
                    UPDATE execution_outbox SET state = 'publishing',
                      delivery_attempts = delivery_attempts + 1, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ANY(%s)
                    """,
                    (ids,),
                )
        return tuple(self._terminal_event_from_row(row) for row in rows)

    def mark_terminal_event_published(self, event_id: UUID) -> None:
        with self._connect() as connection, connection.transaction(), connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE execution_outbox SET state = 'published', published_at = CURRENT_TIMESTAMP,
                  updated_at = CURRENT_TIMESTAMP
                WHERE id = %s AND command_type = ANY(%s) AND state = 'publishing'
                """,
                (event_id, list(sorted(TERMINAL_EVENT_COMMANDS))),
            )
            if cursor.rowcount != 1:
                raise ExecutionControlFailure("EVENT_OUTBOX_STATE_CONFLICT")

    def release_terminal_event(self, event_id: UUID, error_code: str) -> None:
        with self._connect() as connection, connection.transaction(), connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE execution_outbox SET state = 'pending', last_error_code = %s,
                  available_at = CURRENT_TIMESTAMP + interval '1 second',
                  updated_at = CURRENT_TIMESTAMP
                WHERE id = %s AND command_type = ANY(%s) AND state = 'publishing'
                """,
                (error_code, event_id, list(sorted(TERMINAL_EVENT_COMMANDS))),
            )
            if cursor.rowcount != 1:
                raise ExecutionControlFailure("EVENT_OUTBOX_STATE_CONFLICT")

    def mark_outbox_published(self, outbox_id: UUID) -> None:
        with self._connect() as connection, connection.transaction(), connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE execution_outbox SET state = 'published', published_at = CURRENT_TIMESTAMP,
                  updated_at = CURRENT_TIMESTAMP
                WHERE id = %s AND command_type IN ('execute', 'cancel') AND state = 'publishing'
                """,
                (outbox_id,),
            )
            if cursor.rowcount != 1:
                raise ExecutionControlFailure("OUTBOX_STATE_CONFLICT")

    def release_outbox(self, outbox_id: UUID, error_code: str) -> None:
        with self._connect() as connection, connection.transaction(), connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE execution_outbox SET state = 'pending', last_error_code = %s,
                  available_at = CURRENT_TIMESTAMP + interval '1 second',
                  updated_at = CURRENT_TIMESTAMP
                WHERE id = %s AND command_type IN ('execute', 'cancel') AND state = 'publishing'
                """,
                (error_code, outbox_id),
            )

    def claim_attempt(
        self, attempt_id: UUID, *, worker_id: str, lease_seconds: int, request_id: str
    ) -> AttemptRecord:
        with (
            self._connect() as connection,
            connection.transaction(),
            connection.cursor(row_factory=dict_row) as cursor,
        ):
            cursor.execute(
                """
                SELECT a.*, r.state AS run_state FROM execution_attempts AS a
                JOIN execution_runs AS r ON r.id = a.run_id
                WHERE a.id = %s FOR UPDATE OF a, r
                """,
                (attempt_id,),
            )
            row = cursor.fetchone()
            if row is None:
                raise ExecutionControlFailure("ATTEMPT_NOT_FOUND")
            if bool(row["cancellation_requested"]) or row["run_state"] == "CANCELLING":
                raise ExecutionControlFailure("CANCELLATION_REQUESTED")
            if row["state"] == "RUNNING":
                return self._attempt(row)
            if row["state"] not in {"PENDING", "READY", "RETRY_WAIT"}:
                raise ExecutionControlFailure("ATTEMPT_NOT_CLAIMABLE")
            previous = str(row["state"])
            cursor.execute(
                """
                UPDATE execution_attempts SET state = 'RUNNING', fencing_token = fencing_token + 1,
                  worker_id = %s, lease_expires_at = CURRENT_TIMESTAMP + (%s * interval '1 second'),
                  updated_at = CURRENT_TIMESTAMP WHERE id = %s RETURNING *
                """,
                (worker_id, lease_seconds, attempt_id),
            )
            claimed = cursor.fetchone()
            assert claimed is not None
            cursor.execute(
                """
                UPDATE execution_runs SET state = 'RUNNING', revision = revision + 1,
                  last_request_id = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s AND state IN ('CREATED','VALIDATING','QUEUED')
                """,
                (request_id, claimed["run_id"]),
            )
            self._history(
                cursor,
                workspace_id=UUID(str(claimed["workspace_id"])),
                run_id=UUID(str(claimed["run_id"])),
                attempt_id=attempt_id,
                previous_state=previous,
                new_state="RUNNING",
                actor_or_service=worker_id,
                reason="WORKER_CLAIM",
                request_id=request_id,
            )
        return self._attempt(claimed)

    def publish_attempt_state(
        self,
        attempt_id: UUID,
        *,
        fencing_token: int,
        state: str,
        worker_id: str,
        reason: str,
        request_id: str,
        failure_code: str | None = None,
        observed_limit: int | None = None,
        configured_limit: int | None = None,
        safe_remediation: str | None = None,
    ) -> RunRecord:
        if state not in {"SUCCEEDED", "FAILED", "CANCELLED"}:
            raise ExecutionControlFailure("INVALID_ATTEMPT_STATE")
        breach_values = (observed_limit, configured_limit, safe_remediation)
        if failure_code is None:
            if any(value is not None for value in breach_values):
                raise ExecutionControlFailure("INVALID_RESOURCE_BREACH")
        elif (
            state != "FAILED"
            or failure_code != "RESOURCE_LIMIT_EXCEEDED"
            or observed_limit is None
            or configured_limit is None
            or observed_limit <= configured_limit
            or safe_remediation is None
            or not safe_remediation.strip()
        ):
            raise ExecutionControlFailure("INVALID_RESOURCE_BREACH")
        with (
            self._connect() as connection,
            connection.transaction(),
            connection.cursor(row_factory=dict_row) as cursor,
        ):
            cursor.execute(
                """
                SELECT * FROM execution_attempts WHERE id = %s FOR UPDATE
                """,
                (attempt_id,),
            )
            attempt = cursor.fetchone()
            if attempt is None:
                raise ExecutionControlFailure("ATTEMPT_NOT_FOUND")
            if int(attempt["fencing_token"]) != fencing_token:
                raise ExecutionControlFailure("STALE_FENCING_TOKEN")
            previous = str(attempt["state"])
            if previous in {"SUCCEEDED", "FAILED", "CANCELLED"}:
                if previous != state:
                    raise ExecutionControlFailure("TERMINAL_STATE_IMMUTABLE")
            else:
                cursor.execute(
                    """
                    UPDATE execution_attempts SET state = %s, lease_expires_at = NULL,
                      failure_code = %s, observed_limit = %s, configured_limit = %s,
                      safe_remediation = %s,
                      updated_at = CURRENT_TIMESTAMP WHERE id = %s
                    """,
                    (
                        state,
                        failure_code,
                        observed_limit,
                        configured_limit,
                        None if safe_remediation is None else safe_remediation.strip(),
                        attempt_id,
                    ),
                )
                self._history(
                    cursor,
                    workspace_id=UUID(str(attempt["workspace_id"])),
                    run_id=UUID(str(attempt["run_id"])),
                    attempt_id=attempt_id,
                    previous_state=previous,
                    new_state=state,
                    actor_or_service=worker_id,
                    reason=reason,
                    request_id=request_id,
                )
            cursor.execute(
                "SELECT * FROM execution_runs WHERE id = %s FOR UPDATE",
                (attempt["run_id"],),
            )
            run = cursor.fetchone()
            assert run is not None
            cursor.execute(
                """
                SELECT
                  count(*) FILTER (
                    WHERE state IN ('PENDING','READY','RUNNING','RETRY_WAIT')
                  ) AS active_count,
                  count(*) FILTER (WHERE state = 'SUCCEEDED') AS succeeded_count,
                  count(*) FILTER (WHERE state = 'FAILED') AS failed_count,
                  count(*) FILTER (WHERE state = 'CANCELLED') AS cancelled_count
                FROM execution_attempts WHERE run_id = %s
                """,
                (run["id"],),
            )
            aggregate = cursor.fetchone()
            assert aggregate is not None
            target: str | None = None
            if int(aggregate["active_count"]) == 0:
                succeeded = int(aggregate["succeeded_count"])
                failed = int(aggregate["failed_count"])
                cancelled = int(aggregate["cancelled_count"])
                if run["state"] == "CANCELLING":
                    target = "FAILED" if failed > 0 else "CANCELLED"
                elif failed > 0 and succeeded > 0 and bool(run["partial_policy"]):
                    target = "PARTIAL"
                elif failed > 0:
                    target = "FAILED"
                elif cancelled > 0:
                    target = "CANCELLED"
                elif succeeded > 0:
                    target = "SUCCEEDED"
            if target is not None and run["state"] not in TERMINAL_RUN_STATES:
                cursor.execute(
                    """
                    UPDATE execution_runs SET state = %s, revision = revision + 1,
                      last_request_id = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s RETURNING *
                    """,
                    (target, request_id, run["id"]),
                )
                updated = cursor.fetchone()
                assert updated is not None
                self._history(
                    cursor,
                    workspace_id=UUID(str(run["workspace_id"])),
                    run_id=UUID(str(run["id"])),
                    attempt_id=None,
                    previous_state=str(run["state"]),
                    new_state=target,
                    actor_or_service=worker_id,
                    reason=reason,
                    request_id=request_id,
                )
                run = updated
                if target == "FAILED":
                    self._terminal_event(
                        cursor,
                        event_type="execution.run.failed",
                        workspace_id=UUID(str(run["workspace_id"])),
                        run_id=UUID(str(run["id"])),
                        attempt_id=attempt_id,
                        retry_of_run_id=(
                            None if run["retry_of_id"] is None else UUID(str(run["retry_of_id"]))
                        ),
                        retry_of_attempt_id=(
                            None
                            if attempt["retry_of_id"] is None
                            else UUID(str(attempt["retry_of_id"]))
                        ),
                        status_code="FAILED",
                        reason_code=(
                            "RESOURCE_LIMIT_EXCEEDED"
                            if failure_code == "RESOURCE_LIMIT_EXCEEDED"
                            else "EXECUTION_FAILED"
                        ),
                        severity="critical",
                        occurred_at=datetime.now(UTC),
                        trace_id=(
                            None if run["safe_trace_id"] is None else str(run["safe_trace_id"])
                        ),
                    )
                elif target == "SUCCEEDED" and (
                    run["retry_of_id"] is not None or attempt["retry_of_id"] is not None
                ):
                    self._terminal_event(
                        cursor,
                        event_type="execution.run.recovered",
                        workspace_id=UUID(str(run["workspace_id"])),
                        run_id=UUID(str(run["id"])),
                        attempt_id=attempt_id,
                        retry_of_run_id=(
                            None if run["retry_of_id"] is None else UUID(str(run["retry_of_id"]))
                        ),
                        retry_of_attempt_id=(
                            None
                            if attempt["retry_of_id"] is None
                            else UUID(str(attempt["retry_of_id"]))
                        ),
                        status_code="RECOVERED",
                        reason_code="RETRY_SUCCEEDED",
                        severity="info",
                        occurred_at=datetime.now(UTC),
                        trace_id=(
                            None if run["safe_trace_id"] is None else str(run["safe_trace_id"])
                        ),
                    )
        return self._run(run)

    def apply_cancel(
        self,
        *,
        run_id: UUID,
        attempt_id: UUID | None,
        fencing_token: int | None,
        request_id: str,
    ) -> RunRecord:
        if attempt_id is not None:
            assert fencing_token is not None
            return self.publish_attempt_state(
                attempt_id,
                fencing_token=fencing_token,
                state="CANCELLED",
                worker_id="worker-cancel",
                reason="CANCEL_CLEANUP_COMPLETE",
                request_id=request_id,
            )
        with (
            self._connect() as connection,
            connection.transaction(),
            connection.cursor(row_factory=dict_row) as cursor,
        ):
            cursor.execute("SELECT * FROM execution_runs WHERE id = %s FOR UPDATE", (run_id,))
            run = cursor.fetchone()
            if run is None:
                raise ExecutionControlFailure("NOT_FOUND")
            if run["state"] == "CANCELLING":
                cursor.execute(
                    """
                    UPDATE execution_runs SET state = 'CANCELLED', revision = revision + 1,
                      last_request_id = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s RETURNING *
                    """,
                    (request_id, run_id),
                )
                updated = cursor.fetchone()
                assert updated is not None
                self._history(
                    cursor,
                    workspace_id=UUID(str(run["workspace_id"])),
                    run_id=run_id,
                    attempt_id=None,
                    previous_state="CANCELLING",
                    new_state="CANCELLED",
                    actor_or_service="worker-cancel",
                    reason="CANCEL_CLEANUP_COMPLETE",
                    request_id=request_id,
                )
                run = updated
        return self._run(run)

    def reconcile(self, *, observed_at: datetime, request_id: str) -> tuple[str, ...]:
        findings: list[str] = []
        with (
            self._connect() as connection,
            connection.transaction(),
            connection.cursor(row_factory=dict_row) as cursor,
        ):
            cursor.execute(
                """
                SELECT id, run_id, attempt_id, workspace_id FROM execution_outbox
                WHERE state = 'publishing' AND updated_at < %s - interval '1 second'
                FOR UPDATE
                """,
                (observed_at,),
            )
            for incomplete in cursor.fetchall():
                cursor.execute(
                    """
                    UPDATE execution_outbox SET state = 'pending', available_at = %s,
                      last_error_code = 'INCOMPLETE_DELIVERY_COMMIT',
                      updated_at = CURRENT_TIMESTAMP WHERE id = %s
                    """,
                    (observed_at, incomplete["id"]),
                )
                findings.append("INCOMPLETE_DELIVERY_COMMIT_REPAIRED")
                self._finding(
                    cursor,
                    incomplete,
                    "INCOMPLETE_DELIVERY_COMMIT",
                    "RESET_PENDING",
                    request_id,
                    observed_at,
                )

            cursor.execute(
                """
                SELECT o.id, o.run_id, o.attempt_id, o.workspace_id
                FROM execution_outbox AS o
                JOIN execution_attempts AS a ON a.id = o.attempt_id
                WHERE o.command_type = 'execute' AND o.state = 'published'
                  AND a.state IN ('PENDING','READY')
                  AND o.published_at < %s - interval '1 second'
                FOR UPDATE OF o
                """,
                (observed_at,),
            )
            for lost in cursor.fetchall():
                cursor.execute(
                    """
                    UPDATE execution_outbox SET state = 'pending', available_at = %s,
                      updated_at = CURRENT_TIMESTAMP WHERE id = %s
                    """,
                    (observed_at, lost["id"]),
                )
                findings.append("LOST_DELIVERY_REQUEUED")
                self._finding(cursor, lost, "LOST_DELIVERY", "REQUEUE", request_id, observed_at)

            cursor.execute(
                """
                SELECT a.*, r.state AS run_state, r.retry_of_id AS retry_of_run_id,
                       r.safe_trace_id AS run_safe_trace_id
                FROM execution_attempts AS a
                JOIN execution_runs AS r ON r.id = a.run_id
                WHERE a.state = 'RUNNING' AND a.lease_expires_at < %s
                FOR UPDATE OF a, r
                """,
                (observed_at,),
            )
            for expired in cursor.fetchall():
                if expired["run_state"] == "CANCELLING":
                    cursor.execute(
                        """
                        UPDATE execution_attempts SET state = 'CANCELLED',
                          fencing_token = fencing_token + 1, lease_expires_at = NULL,
                          updated_at = CURRENT_TIMESTAMP WHERE id = %s
                        """,
                        (expired["id"],),
                    )
                    self._history(
                        cursor,
                        workspace_id=UUID(str(expired["workspace_id"])),
                        run_id=UUID(str(expired["run_id"])),
                        attempt_id=UUID(str(expired["id"])),
                        previous_state="RUNNING",
                        new_state="CANCELLED",
                        actor_or_service="reconciler",
                        reason="EXPIRED_LEASE_FENCED_DURING_CANCEL",
                        request_id=request_id,
                    )
                    findings.append("EXPIRED_LEASE_FENCED_AND_CANCELLED")
                    self._finding(
                        cursor,
                        expired,
                        "EXPIRED_LEASE_DURING_CANCEL",
                        "FENCE_AND_CANCEL",
                        request_id,
                        observed_at,
                    )
                    continue
                cursor.execute(
                    """
                    UPDATE execution_attempts SET state = 'RETRY_WAIT',
                      fencing_token = fencing_token + 1, lease_expires_at = NULL,
                      updated_at = CURRENT_TIMESTAMP WHERE id = %s
                    """,
                    (expired["id"],),
                )
                new_attempt = uuid4()
                next_number = int(expired["attempt_number"]) + 1
                cursor.execute(
                    """
                    INSERT INTO execution_attempts
                      (id, run_id, workspace_id, attempt_number, state, fencing_token, retry_of_id)
                    VALUES (%s, %s, %s, %s, 'READY', 0, %s)
                    """,
                    (
                        new_attempt,
                        expired["run_id"],
                        expired["workspace_id"],
                        next_number,
                        expired["id"],
                    ),
                )
                self._outbox(
                    cursor,
                    workspace_id=UUID(str(expired["workspace_id"])),
                    run_id=UUID(str(expired["run_id"])),
                    attempt_id=new_attempt,
                    command_type="execute",
                    payload={
                        "workspace_id": str(expired["workspace_id"]),
                        "run_id": str(expired["run_id"]),
                        "attempt_id": str(new_attempt),
                        "retry_of_id": str(expired["id"]),
                    },
                )
                self._terminal_event(
                    cursor,
                    event_type="execution.run.stuck",
                    workspace_id=UUID(str(expired["workspace_id"])),
                    run_id=UUID(str(expired["run_id"])),
                    attempt_id=UUID(str(expired["id"])),
                    retry_of_run_id=(
                        None
                        if expired["retry_of_run_id"] is None
                        else UUID(str(expired["retry_of_run_id"]))
                    ),
                    retry_of_attempt_id=(
                        None
                        if expired["retry_of_id"] is None
                        else UUID(str(expired["retry_of_id"]))
                    ),
                    status_code="STUCK",
                    reason_code="LEASE_EXPIRED",
                    severity="warning",
                    occurred_at=observed_at,
                    trace_id=(
                        None
                        if expired["run_safe_trace_id"] is None
                        else str(expired["run_safe_trace_id"])
                    ),
                )
                findings.append("EXPIRED_LEASE_FENCED_AND_RETRIED")
                self._finding(cursor, expired, "EXPIRED_LEASE", "FENCE_AND_RETRY", request_id, observed_at)

            cursor.execute(
                """
                SELECT r.*, stats.active_count, stats.succeeded_count,
                       stats.failed_count, stats.cancelled_count
                FROM execution_runs AS r
                CROSS JOIN LATERAL (
                  SELECT
                    count(*) FILTER (
                      WHERE state IN ('PENDING','READY','RUNNING','RETRY_WAIT')
                    ) AS active_count,
                    count(*) FILTER (WHERE state = 'SUCCEEDED') AS succeeded_count,
                    count(*) FILTER (WHERE state = 'FAILED') AS failed_count,
                    count(*) FILTER (WHERE state = 'CANCELLED') AS cancelled_count,
                    count(*) AS total_count
                  FROM execution_attempts WHERE run_id = r.id
                ) AS stats
                WHERE r.state IN ('CREATED','VALIDATING','QUEUED','RUNNING','CANCELLING')
                  AND stats.total_count > 0 AND stats.active_count = 0
                FOR UPDATE OF r
                """
            )
            for unfinished in cursor.fetchall():
                succeeded = int(unfinished["succeeded_count"])
                failed = int(unfinished["failed_count"])
                cancelled = int(unfinished["cancelled_count"])
                if unfinished["state"] == "CANCELLING" or cancelled > 0:
                    target = "CANCELLED"
                elif failed > 0 and succeeded > 0 and bool(unfinished["partial_policy"]):
                    target = "PARTIAL"
                elif failed > 0:
                    target = "FAILED"
                elif succeeded > 0:
                    target = "SUCCEEDED"
                else:
                    continue
                cursor.execute(
                    """
                    UPDATE execution_runs SET state = %s, revision = revision + 1,
                      last_request_id = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                    """,
                    (target, request_id, unfinished["id"]),
                )
                self._history(
                    cursor,
                    workspace_id=UUID(str(unfinished["workspace_id"])),
                    run_id=UUID(str(unfinished["id"])),
                    attempt_id=None,
                    previous_state=str(unfinished["state"]),
                    new_state=target,
                    actor_or_service="reconciler",
                    reason="UNFINISHED_AGGREGATE_REPAIRED",
                    request_id=request_id,
                )
                findings.append("UNFINISHED_AGGREGATE_REPAIRED")
                finding_row = dict(unfinished)
                finding_row["run_id"] = unfinished["id"]
                finding_row["attempt_id"] = None
                self._finding(
                    cursor,
                    finding_row,
                    "UNFINISHED_AGGREGATE",
                    f"DERIVE_{target}",
                    request_id,
                    observed_at,
                )
                if target in {"FAILED", "SUCCEEDED"}:
                    cursor.execute(
                        """
                        SELECT id, retry_of_id, failure_code
                        FROM execution_attempts
                        WHERE run_id = %s AND state = %s
                        ORDER BY attempt_number DESC LIMIT 1
                        """,
                        (unfinished["id"], target),
                    )
                    terminal_attempt = cursor.fetchone()
                    if terminal_attempt is not None and target == "FAILED":
                        self._terminal_event(
                            cursor,
                            event_type="execution.run.failed",
                            workspace_id=UUID(str(unfinished["workspace_id"])),
                            run_id=UUID(str(unfinished["id"])),
                            attempt_id=UUID(str(terminal_attempt["id"])),
                            retry_of_run_id=(
                                None
                                if unfinished["retry_of_id"] is None
                                else UUID(str(unfinished["retry_of_id"]))
                            ),
                            retry_of_attempt_id=(
                                None
                                if terminal_attempt["retry_of_id"] is None
                                else UUID(str(terminal_attempt["retry_of_id"]))
                            ),
                            status_code="FAILED",
                            reason_code=(
                                "RESOURCE_LIMIT_EXCEEDED"
                                if terminal_attempt["failure_code"] == "RESOURCE_LIMIT_EXCEEDED"
                                else "EXECUTION_FAILED"
                            ),
                            severity="critical",
                            occurred_at=observed_at,
                            trace_id=(
                                None
                                if unfinished["safe_trace_id"] is None
                                else str(unfinished["safe_trace_id"])
                            ),
                        )
                    elif terminal_attempt is not None and (
                        unfinished["retry_of_id"] is not None
                        or terminal_attempt["retry_of_id"] is not None
                    ):
                        self._terminal_event(
                            cursor,
                            event_type="execution.run.recovered",
                            workspace_id=UUID(str(unfinished["workspace_id"])),
                            run_id=UUID(str(unfinished["id"])),
                            attempt_id=UUID(str(terminal_attempt["id"])),
                            retry_of_run_id=(
                                None
                                if unfinished["retry_of_id"] is None
                                else UUID(str(unfinished["retry_of_id"]))
                            ),
                            retry_of_attempt_id=(
                                None
                                if terminal_attempt["retry_of_id"] is None
                                else UUID(str(terminal_attempt["retry_of_id"]))
                            ),
                            status_code="RECOVERED",
                            reason_code="RETRY_SUCCEEDED",
                            severity="info",
                            occurred_at=observed_at,
                            trace_id=(
                                None
                                if unfinished["safe_trace_id"] is None
                                else str(unfinished["safe_trace_id"])
                            ),
                        )
        return tuple(findings)

    @staticmethod
    def _finding(
        cursor: Any,
        row: Any,
        finding_code: str,
        repair_action: str,
        request_id: str,
        observed_at: datetime,
    ) -> None:
        cursor.execute(
            """
            INSERT INTO execution_reconciliation_findings
              (id, workspace_id, run_id, attempt_id, finding_code, repair_action,
               request_id, observed_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """,
            (
                uuid4(),
                row["workspace_id"],
                row["run_id"],
                row.get("attempt_id", row.get("id")),
                finding_code,
                repair_action,
                request_id,
                observed_at,
            ),
        )


__all__ = ["PostgresExecutionControlStore"]
