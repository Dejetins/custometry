"""Public contracts for operator-facing execution control."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Protocol
from uuid import UUID


EXECUTION_CONTROL_API_VERSION = "1.0.0"
EXECUTION_TERMINAL_EVENT_VERSION = "1.0.0"
VisibilityScope = Literal["owner", "workspace"]
ExecutionTerminalEventType = Literal[
    "execution.run.failed",
    "execution.run.stuck",
    "execution.run.recovered",
]
ExecutionTerminalStatus = Literal["FAILED", "STUCK", "RECOVERED"]
ExecutionTerminalSeverity = Literal["info", "warning", "critical"]


class ExecutionControlFailure(RuntimeError):
    """Stable, redacted failure envelope for the execution-control boundary."""

    def __init__(self, code: str, *, current_state: str | None = None) -> None:
        super().__init__(code)
        self.code = code
        self.current_state = current_state


@dataclass(frozen=True, slots=True)
class ExecutionActor:
    principal_id: UUID
    workspace_id: UUID
    permissions: frozenset[str]
    policy_version: str


class ExecutionAuthorizationPort(Protocol):
    """Resolve a SQL-applicable visibility scope without loading run rows."""

    def authorize(self, actor: ExecutionActor, action: str) -> VisibilityScope: ...


@dataclass(frozen=True, slots=True)
class ExecutionTerminalEvent:
    """Versioned locale-neutral event safe for cross-context consumption."""

    event_id: UUID
    event_type: ExecutionTerminalEventType
    event_version: Literal["1.0.0"]
    source_owner: Literal["execution"]
    workspace_id: UUID
    resource_type: Literal["run"]
    resource_id: UUID
    run_id: UUID
    attempt_id: UUID
    retry_of_run_id: UUID | None
    retry_of_attempt_id: UUID | None
    status_code: ExecutionTerminalStatus
    reason_code: str
    severity: ExecutionTerminalSeverity
    category: Literal["execution"]
    occurred_at: datetime
    message_code: Literal["RUN_FAILED", "RUN_STUCK", "RUN_RECOVERED"]
    message_parameters: tuple[tuple[str, str], ...]
    group_key: str
    route_id: Literal["UI-OPS-002"]
    route_parameters: tuple[tuple[str, str], ...]
    trace_id: str | None


class ExecutionTerminalEventOutboxPort(Protocol):
    """Public at-least-once event port; consumers never read Execution tables."""

    def claim_terminal_events(self, *, limit: int = 100) -> tuple[ExecutionTerminalEvent, ...]: ...

    def mark_terminal_event_published(self, event_id: UUID) -> None: ...

    def release_terminal_event(self, event_id: UUID, error_code: str) -> None: ...


__all__ = [
    "EXECUTION_CONTROL_API_VERSION",
    "EXECUTION_TERMINAL_EVENT_VERSION",
    "ExecutionActor",
    "ExecutionAuthorizationPort",
    "ExecutionControlFailure",
    "ExecutionTerminalEvent",
    "ExecutionTerminalEventOutboxPort",
    "ExecutionTerminalEventType",
    "ExecutionTerminalSeverity",
    "ExecutionTerminalStatus",
    "VisibilityScope",
]
