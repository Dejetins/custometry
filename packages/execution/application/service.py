"""Policy-first execution-control queries and commands."""

from __future__ import annotations

from typing import Protocol
from uuid import UUID

from packages.contracts.execution import (
    ExecutionActor,
    ExecutionAuthorizationPort,
    ExecutionControlFailure,
    VisibilityScope,
)
from packages.execution.domain.model import (
    AttemptRecord,
    QueueSummary,
    RetryMode,
    RunQuery,
    RunRecord,
)


class ExecutionControlStorePort(Protocol):
    def list_runs(
        self, actor: ExecutionActor, scope: VisibilityScope, query: RunQuery
    ) -> tuple[tuple[RunRecord, ...], int]: ...

    def queue_summary(
        self, actor: ExecutionActor, scope: VisibilityScope
    ) -> QueueSummary: ...

    def get_run(
        self, actor: ExecutionActor, scope: VisibilityScope, run_id: UUID
    ) -> tuple[RunRecord, tuple[AttemptRecord, ...]]: ...

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
    ) -> RunRecord: ...

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
    ) -> RunRecord: ...


class FunctionalExecutionAuthorization:
    """Fail closed before repository fetch/count and return a SQL visibility scope."""

    def authorize(self, actor: ExecutionActor, action: str) -> VisibilityScope:
        if action not in actor.permissions:
            raise ExecutionControlFailure("FORBIDDEN")
        operator = bool({"run.cancel", "run.retry"}.intersection(actor.permissions))
        return "workspace" if operator else "owner"


class ExecutionControlService:
    def __init__(
        self,
        store: ExecutionControlStorePort,
        authorization: ExecutionAuthorizationPort | None = None,
    ) -> None:
        self._store = store
        self._authorization = authorization or FunctionalExecutionAuthorization()

    @staticmethod
    def _reason(value: str) -> str:
        normalized = value.strip()
        if not (3 <= len(normalized) <= 500):
            raise ExecutionControlFailure("AUDIT_REASON_REQUIRED")
        return normalized

    @staticmethod
    def _identity(value: str, *, code: str, maximum: int) -> str:
        normalized = value.strip()
        if not normalized or len(normalized) > maximum:
            raise ExecutionControlFailure(code)
        return normalized

    def list_runs(
        self, actor: ExecutionActor, query: RunQuery
    ) -> tuple[tuple[RunRecord, ...], int]:
        scope = self._authorization.authorize(actor, "run.read")
        if query.offset < 0 or not 1 <= query.limit <= 100:
            raise ExecutionControlFailure("INVALID_INPUT")
        return self._store.list_runs(actor, scope, query)

    def queue_summary(self, actor: ExecutionActor) -> QueueSummary:
        scope = self._authorization.authorize(actor, "run.read")
        return self._store.queue_summary(actor, scope)

    def get_run(
        self, actor: ExecutionActor, run_id: UUID
    ) -> tuple[RunRecord, tuple[AttemptRecord, ...]]:
        scope = self._authorization.authorize(actor, "run.read")
        return self._store.get_run(actor, scope, run_id)

    def cancel(
        self,
        actor: ExecutionActor,
        *,
        run_id: UUID,
        expected_revision: int,
        reason: str,
        request_id: str,
        idempotency_key: str,
        payload_hash: str,
    ) -> RunRecord:
        scope = self._authorization.authorize(actor, "run.cancel")
        return self._store.cancel(
            actor,
            scope,
            run_id=run_id,
            expected_revision=expected_revision,
            reason=self._reason(reason),
            request_id=self._identity(request_id, code="REQUEST_ID_REQUIRED", maximum=128),
            idempotency_key=self._identity(
                idempotency_key, code="IDEMPOTENCY_KEY_REQUIRED", maximum=128
            ),
            payload_hash=self._identity(payload_hash, code="INVALID_PAYLOAD_HASH", maximum=64),
        )

    def retry(
        self,
        actor: ExecutionActor,
        *,
        run_id: UUID,
        expected_revision: int,
        mode: RetryMode,
        reason: str,
        request_id: str,
        idempotency_key: str,
        payload_hash: str,
    ) -> RunRecord:
        scope = self._authorization.authorize(actor, "run.retry")
        if mode == "full_rerun" and "run.create" not in actor.permissions:
            raise ExecutionControlFailure("FORBIDDEN")
        return self._store.retry(
            actor,
            scope,
            run_id=run_id,
            expected_revision=expected_revision,
            mode=mode,
            reason=self._reason(reason),
            request_id=self._identity(request_id, code="REQUEST_ID_REQUIRED", maximum=128),
            idempotency_key=self._identity(
                idempotency_key, code="IDEMPOTENCY_KEY_REQUIRED", maximum=128
            ),
            payload_hash=self._identity(payload_hash, code="INVALID_PAYLOAD_HASH", maximum=64),
        )


__all__ = [
    "ExecutionControlService",
    "ExecutionControlStorePort",
    "FunctionalExecutionAuthorization",
]
