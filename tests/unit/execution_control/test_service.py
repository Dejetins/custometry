from datetime import UTC, datetime
from uuid import UUID, uuid4

import pytest

from packages.contracts.execution import ExecutionActor, ExecutionControlFailure
from packages.execution.application.service import ExecutionControlService
from packages.execution.domain.model import QueueSummary, RunQuery


class RecordingStore:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def list_runs(self, actor, scope, query):
        self.calls.append(f"list:{scope}")
        return (), 0

    def get_run(self, actor, scope, run_id):
        self.calls.append(f"get:{scope}")
        raise AssertionError("not needed")

    def queue_summary(self, actor, scope):
        self.calls.append(f"summary:{scope}")
        return QueueSummary({}, {}, None, datetime.now(UTC), "fresh")

    def cancel(self, actor, scope, **kwargs):
        self.calls.append(f"cancel:{scope}")
        raise AssertionError("not needed")

    def retry(self, actor, scope, **kwargs):
        self.calls.append(f"retry:{scope}")
        raise AssertionError("not needed")


def actor(*permissions: str) -> ExecutionActor:
    return ExecutionActor(uuid4(), uuid4(), frozenset(permissions), "policy-v1")


def test_authorization_denies_before_repository_fetch_or_count() -> None:
    store = RecordingStore()
    service = ExecutionControlService(store)

    with pytest.raises(ExecutionControlFailure, match="FORBIDDEN"):
        service.list_runs(actor(), RunQuery())
    with pytest.raises(ExecutionControlFailure, match="FORBIDDEN"):
        service.queue_summary(actor())

    assert store.calls == []


def test_resource_owner_and_operator_scopes_are_resolved_before_query() -> None:
    store = RecordingStore()
    service = ExecutionControlService(store)

    service.list_runs(actor("run.read"), RunQuery())
    service.list_runs(actor("run.read", "run.cancel"), RunQuery())

    assert store.calls == ["list:owner", "list:workspace"]


@pytest.mark.parametrize("value", ["", "  ", "x", "xx"])
def test_mutations_require_a_bounded_audit_reason_before_store(value: str) -> None:
    store = RecordingStore()
    service = ExecutionControlService(store)

    with pytest.raises(ExecutionControlFailure, match="AUDIT_REASON_REQUIRED"):
        service.cancel(
            actor("run.cancel"),
            run_id=UUID(int=1),
            expected_revision=1,
            reason=value,
            request_id="request",
            idempotency_key="key",
            payload_hash="a" * 64,
        )

    assert store.calls == []


def test_full_rerun_requires_run_create_before_store() -> None:
    store = RecordingStore()
    service = ExecutionControlService(store)

    with pytest.raises(ExecutionControlFailure, match="FORBIDDEN"):
        service.retry(
            actor("run.retry"),
            run_id=UUID(int=1),
            expected_revision=1,
            mode="full_rerun",
            reason="operator requested rerun",
            request_id="request",
            idempotency_key="key",
            payload_hash="b" * 64,
        )

    assert store.calls == []
