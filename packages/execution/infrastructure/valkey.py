"""Disposable Valkey delivery adapter and bounded worker mechanics."""

from __future__ import annotations

import json
from dataclasses import dataclass
from multiprocessing.process import BaseProcess
from typing import Callable, Protocol
from uuid import UUID, uuid4

from redis import Redis

from packages.contracts.execution import ExecutionControlFailure
from packages.execution.infrastructure.control_postgres import PostgresExecutionControlStore


class TaskQueuePort(Protocol):
    def publish(self, identity: str, payload: dict[str, object]) -> bool: ...

    def pop(self, timeout_seconds: int = 1) -> dict[str, object] | None: ...


class ValkeyTaskQueue:
    """At-least-once queue with workspace/policy-scoped duplicate suppression."""

    def __init__(self, client: Redis, *, namespace: str = "custometry:execution:v1") -> None:
        self._client = client
        self._namespace = namespace

    def publish(self, identity: str, payload: dict[str, object]) -> bool:
        dedupe_key = f"{self._namespace}:dedupe:{identity}"
        serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        created = self._client.set(dedupe_key, "1", nx=True, ex=3600)
        if created:
            self._client.rpush(f"{self._namespace}:tasks", serialized)
        return bool(created)

    def pop(self, timeout_seconds: int = 1) -> dict[str, object] | None:
        item = self._client.blpop(f"{self._namespace}:tasks", timeout=timeout_seconds)
        if item is None:
            return None
        raw = item[1]
        decoded = raw.decode("utf-8") if isinstance(raw, bytes) else str(raw)
        value = json.loads(decoded)
        if not isinstance(value, dict):
            raise ExecutionControlFailure("INVALID_TASK_PAYLOAD")
        return value


@dataclass(frozen=True, slots=True)
class DispatchResult:
    selected: int
    published: int
    deduplicated: int


@dataclass(slots=True)
class IsolatedAttemptController:
    """Cancel a driver operation before hard-stopping one isolated attempt process."""

    process: BaseProcess
    cancel_database_statement: Callable[[], None]
    cleanup_uncommitted: Callable[[], None]

    def cancel(self, *, grace_seconds: float = 0.2) -> bool:
        self.cancel_database_statement()
        self.process.join(timeout=grace_seconds)
        hard_stopped = self.process.is_alive()
        if hard_stopped:
            self.process.terminate()
            self.process.join(timeout=grace_seconds)
        self.cleanup_uncommitted()
        return hard_stopped


class ExecutionOutboxDispatcher:
    def __init__(self, store: PostgresExecutionControlStore, queue: TaskQueuePort) -> None:
        self._store = store
        self._queue = queue

    def dispatch(self, *, limit: int = 100) -> DispatchResult:
        selected = self._store.pending_outbox(limit=limit)
        published = 0
        deduplicated = 0
        for row in selected:
            payload = dict(row["payload"])
            payload["command_type"] = str(row["command_type"])
            payload["outbox_id"] = str(row["id"])
            identity = ":".join(
                (
                    str(row["workspace_id"]),
                    str(payload.get("policy_version", "current")),
                    str(row["run_id"]),
                    str(row["attempt_id"] or "aggregate"),
                    str(row["command_type"]),
                    str(row["delivery_attempts"] + 1),
                )
            )
            try:
                created = self._queue.publish(identity, payload)
                self._store.mark_outbox_published(UUID(str(row["id"])))
                if created:
                    published += 1
                else:
                    deduplicated += 1
            except Exception as exc:
                self._store.release_outbox(UUID(str(row["id"])), "DELIVERY_UNAVAILABLE")
                raise ExecutionControlFailure("DELIVERY_UNAVAILABLE") from exc
        return DispatchResult(len(selected), published, deduplicated)


class DisposableExecutionWorker:
    """Small worker seam used to observe claim, fencing, cancel, and terminal publication."""

    def __init__(
        self,
        store: PostgresExecutionControlStore,
        queue: TaskQueuePort,
        *,
        worker_id: str,
    ) -> None:
        self._store = store
        self._queue = queue
        self._worker_id = worker_id

    def run_one(self) -> tuple[str, UUID, int | None] | None:
        payload = self._queue.pop()
        if payload is None:
            return None
        command = str(payload.get("command_type"))
        run_id = UUID(str(payload["run_id"]))
        request_id = f"worker-{uuid4()}"
        if command == "execute":
            attempt = self._store.claim_attempt(
                UUID(str(payload["attempt_id"])),
                worker_id=self._worker_id,
                lease_seconds=30,
                request_id=request_id,
            )
            return command, attempt.attempt_id, attempt.fencing_token
        if command == "cancel":
            raw_attempt = payload.get("attempt_id")
            attempt_id = None if raw_attempt is None else UUID(str(raw_attempt))
            raw_token = payload.get("fencing_token")
            token = None if raw_token is None else int(str(raw_token))
            self._store.apply_cancel(
                run_id=run_id,
                attempt_id=attempt_id,
                fencing_token=token,
                request_id=request_id,
            )
            return command, attempt_id or run_id, token
        raise ExecutionControlFailure("UNKNOWN_TASK_COMMAND")


__all__ = [
    "DispatchResult",
    "DisposableExecutionWorker",
    "ExecutionOutboxDispatcher",
    "IsolatedAttemptController",
    "TaskQueuePort",
    "ValkeyTaskQueue",
]
