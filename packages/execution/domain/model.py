from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from uuid import UUID


@dataclass(frozen=True, slots=True)
class ExecutionClaim:
    batch_id: UUID
    attempt_id: UUID
    fencing_token: int


RunState = Literal[
    "CREATED",
    "VALIDATING",
    "QUEUED",
    "RUNNING",
    "CANCELLING",
    "SUCCEEDED",
    "FAILED",
    "CANCELLED",
    "PARTIAL",
]
AttemptState = Literal[
    "PENDING", "READY", "RUNNING", "RETRY_WAIT", "SUCCEEDED", "FAILED", "CANCELLED"
]
RetryMode = Literal["failed_nodes", "full_rerun"]

TERMINAL_RUN_STATES = frozenset({"SUCCEEDED", "FAILED", "CANCELLED", "PARTIAL"})
TERMINAL_ATTEMPT_STATES = frozenset({"SUCCEEDED", "FAILED", "CANCELLED"})

RUN_TRANSITIONS: dict[str, frozenset[str]] = {
    "CREATED": frozenset({"VALIDATING", "QUEUED", "CANCELLING", "FAILED"}),
    "VALIDATING": frozenset({"QUEUED", "CANCELLING", "FAILED"}),
    "QUEUED": frozenset({"RUNNING", "CANCELLING", "FAILED"}),
    "RUNNING": frozenset({"CANCELLING", "SUCCEEDED", "FAILED", "PARTIAL"}),
    "CANCELLING": frozenset({"CANCELLED", "FAILED", "PARTIAL"}),
    "SUCCEEDED": frozenset(),
    "FAILED": frozenset(),
    "CANCELLED": frozenset(),
    "PARTIAL": frozenset(),
}


@dataclass(frozen=True, slots=True)
class RunRecord:
    run_id: UUID
    workspace_id: UUID
    owner_principal_id: UUID
    execution_kind: str
    lane: str
    safe_title: str
    safe_trace_id: str | None
    state: RunState
    revision: int
    retry_of_id: UUID | None
    retry_mode: RetryMode | None
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True, slots=True)
class AttemptRecord:
    attempt_id: UUID
    run_id: UUID
    state: AttemptState
    attempt_number: int
    fencing_token: int
    retry_of_id: UUID | None
    lease_expires_at: datetime | None
    failure_code: str | None
    observed_limit: int | None
    configured_limit: int | None
    safe_remediation: str | None


@dataclass(frozen=True, slots=True)
class RunQuery:
    states: tuple[str, ...] = ()
    execution_kind: str | None = None
    owner_principal_id: UUID | None = None
    created_from: datetime | None = None
    created_to: datetime | None = None
    safe_trace_id: str | None = None
    offset: int = 0
    limit: int = 50


@dataclass(frozen=True, slots=True)
class QueueSummary:
    counts: dict[str, int]
    lane_counts: dict[str, int]
    oldest_queued_age_seconds: int | None
    observed_at: datetime
    freshness: Literal["fresh", "stale", "degraded"]


def can_transition(previous: str, new: str) -> bool:
    return new in RUN_TRANSITIONS.get(previous, frozenset())
