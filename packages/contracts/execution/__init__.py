"""Public contracts for operator-facing execution control."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol
from uuid import UUID


EXECUTION_CONTROL_API_VERSION = "1.0.0"
VisibilityScope = Literal["owner", "workspace"]


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


__all__ = [
    "EXECUTION_CONTROL_API_VERSION",
    "ExecutionActor",
    "ExecutionAuthorizationPort",
    "ExecutionControlFailure",
    "VisibilityScope",
]
