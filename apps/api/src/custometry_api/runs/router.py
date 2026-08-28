"""Policy-filtered operator run query and command API."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

import psycopg
from fastapi import Depends, FastAPI, Header, Query, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from custometry_api.config import Settings
from packages.contracts.execution import (
    EXECUTION_CONTROL_API_VERSION,
    ExecutionActor,
    ExecutionControlFailure,
)
from packages.execution.application.service import ExecutionControlService
from packages.execution.domain.model import AttemptRecord, RunQuery, RunRecord
from packages.execution.infrastructure.control_postgres import PostgresExecutionControlStore
from packages.identity_access.application.service import IdentityService
from packages.identity_access.domain.policy import Actor
from packages.identity_access.infrastructure.postgres import PostgresIdentityRepository


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


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ErrorResponse(StrictModel):
    code: str
    current_state: str | None = None


class RunResponse(StrictModel):
    run_id: UUID
    owner_principal_id: UUID
    execution_kind: str
    lane: str
    safe_title: str
    safe_trace_id: str | None
    state: RunState
    revision: int = Field(ge=1)
    retry_of_id: UUID | None
    retry_mode: Literal["failed_nodes", "full_rerun"] | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_domain(cls, run: RunRecord) -> "RunResponse":
        return cls.model_validate(
            {
                "run_id": run.run_id,
                "owner_principal_id": run.owner_principal_id,
                "execution_kind": run.execution_kind,
                "lane": run.lane,
                "safe_title": run.safe_title,
                "safe_trace_id": run.safe_trace_id,
                "state": run.state,
                "revision": run.revision,
                "retry_of_id": run.retry_of_id,
                "retry_mode": run.retry_mode,
                "created_at": run.created_at,
                "updated_at": run.updated_at,
            }
        )


class AttemptResponse(StrictModel):
    attempt_id: UUID
    state: Literal[
        "PENDING", "READY", "RUNNING", "RETRY_WAIT", "SUCCEEDED", "FAILED", "CANCELLED"
    ]
    attempt_number: int = Field(ge=1)
    fencing_token: int = Field(ge=0)
    retry_of_id: UUID | None
    lease_expires_at: datetime | None
    failure_code: Literal["RESOURCE_LIMIT_EXCEEDED"] | None
    observed_limit: int | None = Field(default=None, ge=0)
    configured_limit: int | None = Field(default=None, ge=0)
    safe_remediation: str | None

    @classmethod
    def from_domain(cls, attempt: AttemptRecord) -> "AttemptResponse":
        return cls.model_validate(attempt, from_attributes=True)


class RunDetailResponse(RunResponse):
    attempts: list[AttemptResponse]


class RunListResponse(StrictModel):
    runs: list[RunResponse]
    visible_count: int = Field(ge=0)


class QueueSummaryResponse(StrictModel):
    counts: dict[str, int]
    lane_counts: dict[str, int]
    oldest_queued_age_seconds: int | None = Field(default=None, ge=0)
    observed_at: datetime
    freshness: Literal["fresh", "stale", "degraded"]


class CancelRequest(StrictModel):
    expected_revision: int = Field(ge=1)
    reason: str = Field(min_length=3, max_length=500)


class RetryRequest(CancelRequest):
    mode: Literal["failed_nodes", "full_rerun"]


@dataclass(frozen=True, slots=True)
class RequestContext:
    actor: ExecutionActor
    request_id: str


def _services(settings: Settings) -> tuple[IdentityService, ExecutionControlService]:
    def connect() -> psycopg.Connection[object]:
        return psycopg.connect(
            host=settings.database_host,
            port=settings.database_port,
            dbname=settings.database_name,
            user=settings.database_user,
            password=settings.read_database_password(),
            connect_timeout=settings.database_connect_timeout_seconds,
        )

    identity = IdentityService(PostgresIdentityRepository(connect), bootstrap_secret=None)
    return identity, ExecutionControlService(PostgresExecutionControlStore(connect))


def _status_for(code: str) -> int:
    if code == "AUTHENTICATION_FAILED":
        return status.HTTP_401_UNAUTHORIZED
    if code == "FORBIDDEN":
        return status.HTTP_403_FORBIDDEN
    if code in {"NOT_FOUND", "ATTEMPT_NOT_FOUND"}:
        return status.HTTP_404_NOT_FOUND
    if code in {
        "IDEMPOTENCY_CONFLICT",
        "STALE_REVISION",
        "INVALID_TRANSITION",
        "TERMINAL_STATE_IMMUTABLE",
        "RETRY_NOT_ELIGIBLE",
    }:
        return status.HTTP_409_CONFLICT
    if code in {"DELIVERY_UNAVAILABLE"}:
        return status.HTTP_503_SERVICE_UNAVAILABLE
    return status.HTTP_400_BAD_REQUEST


def _payload_hash(route: str, payload: BaseModel) -> str:
    canonical = json.dumps(
        {"route": route, "payload": payload.model_dump(mode="json")},
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _policy_version(actor: Actor) -> str:
    canonical = json.dumps(sorted(actor.permissions), separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def create_runs_app(
    settings: Settings,
    *,
    identity_service: IdentityService | None = None,
    execution_service: ExecutionControlService | None = None,
) -> FastAPI:
    default_identity, default_execution = _services(settings)
    identity = identity_service or default_identity
    execution = execution_service or default_execution
    app = FastAPI(
        title="Custometry Execution Control API",
        version=EXECUTION_CONTROL_API_VERSION,
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi.json",
    )

    @app.exception_handler(ExecutionControlFailure)
    async def execution_failure_handler(
        _: Request, exc: ExecutionControlFailure
    ) -> JSONResponse:
        payload = ErrorResponse(code=exc.code, current_state=exc.current_state)
        return JSONResponse(
            status_code=_status_for(exc.code),
            content=payload.model_dump(exclude_none=True),
        )

    def authenticated(
        authorization: Annotated[str | None, Header(alias="Authorization")] = None,
        request_id: Annotated[str | None, Header(alias="X-Request-ID")] = None,
        contract_version: Annotated[
            str | None, Header(alias="X-Contract-Version")
        ] = None,
    ) -> RequestContext:
        if request_id is None or not request_id.strip() or len(request_id) > 128:
            raise ExecutionControlFailure("REQUEST_ID_REQUIRED")
        if contract_version != EXECUTION_CONTROL_API_VERSION:
            raise ExecutionControlFailure("CONTRACT_VERSION_MISMATCH")
        if authorization is None:
            raise ExecutionControlFailure("AUTHENTICATION_FAILED")
        scheme, _, token = authorization.partition(" ")
        if scheme.casefold() != "bearer" or not token:
            raise ExecutionControlFailure("AUTHENTICATION_FAILED")
        try:
            actor = identity.authenticate(token)
        except Exception as exc:
            raise ExecutionControlFailure("AUTHENTICATION_FAILED") from exc
        return RequestContext(
            actor=ExecutionActor(
                principal_id=actor.principal_id,
                workspace_id=actor.workspace_id,
                permissions=actor.permissions,
                policy_version=_policy_version(actor),
            ),
            request_id=request_id.strip(),
        )

    @app.get("/runs", response_model=RunListResponse, operation_id="list_operator_runs")
    def list_runs(
        states: Annotated[list[RunState] | None, Query()] = None,
        execution_kind: Annotated[str | None, Query(min_length=1, max_length=64)] = None,
        owner_principal_id: Annotated[UUID | None, Query()] = None,
        created_from: Annotated[datetime | None, Query()] = None,
        created_to: Annotated[datetime | None, Query()] = None,
        safe_trace_id: Annotated[str | None, Query(min_length=1, max_length=128)] = None,
        offset: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=100)] = 50,
        context: RequestContext = Depends(authenticated),
    ) -> RunListResponse:
        runs, count = execution.list_runs(
            context.actor,
            RunQuery(
                states=tuple(states or ()),
                execution_kind=execution_kind,
                owner_principal_id=owner_principal_id,
                created_from=created_from,
                created_to=created_to,
                safe_trace_id=safe_trace_id,
                offset=offset,
                limit=limit,
            ),
        )
        return RunListResponse(
            runs=[RunResponse.from_domain(run) for run in runs], visible_count=count
        )

    @app.get(
        "/runs/{run_id}",
        response_model=RunDetailResponse,
        operation_id="get_operator_run",
    )
    def get_run(
        run_id: UUID, context: RequestContext = Depends(authenticated)
    ) -> RunDetailResponse:
        run, attempts = execution.get_run(context.actor, run_id)
        payload = RunResponse.from_domain(run).model_dump()
        payload["attempts"] = [AttemptResponse.from_domain(item).model_dump() for item in attempts]
        return RunDetailResponse.model_validate(payload)

    @app.get(
        "/queue-summary",
        response_model=QueueSummaryResponse,
        operation_id="get_operator_queue_summary",
    )
    def queue_summary(
        context: RequestContext = Depends(authenticated),
    ) -> QueueSummaryResponse:
        return QueueSummaryResponse.model_validate(
            execution.queue_summary(context.actor), from_attributes=True
        )

    @app.post(
        "/runs/{run_id}/cancel",
        response_model=RunResponse,
        operation_id="cancel_operator_run",
    )
    def cancel_run(
        run_id: UUID,
        payload: CancelRequest,
        idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
        context: RequestContext = Depends(authenticated),
    ) -> RunResponse:
        if idempotency_key is None:
            raise ExecutionControlFailure("IDEMPOTENCY_KEY_REQUIRED")
        run = execution.cancel(
            context.actor,
            run_id=run_id,
            expected_revision=payload.expected_revision,
            reason=payload.reason,
            request_id=context.request_id,
            idempotency_key=idempotency_key,
            payload_hash=_payload_hash(f"/runs/{run_id}/cancel", payload),
        )
        return RunResponse.from_domain(run)

    @app.post(
        "/runs/{run_id}/retry",
        response_model=RunResponse,
        operation_id="retry_operator_run",
    )
    def retry_run(
        run_id: UUID,
        payload: RetryRequest,
        idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
        context: RequestContext = Depends(authenticated),
    ) -> RunResponse:
        if idempotency_key is None:
            raise ExecutionControlFailure("IDEMPOTENCY_KEY_REQUIRED")
        run = execution.retry(
            context.actor,
            run_id=run_id,
            expected_revision=payload.expected_revision,
            mode=payload.mode,
            reason=payload.reason,
            request_id=context.request_id,
            idempotency_key=idempotency_key,
            payload_hash=_payload_hash(f"/runs/{run_id}/retry", payload),
        )
        return RunResponse.from_domain(run)

    _ = (
        execution_failure_handler,
        list_runs,
        get_run,
        queue_summary,
        cancel_run,
        retry_run,
    )
    return app


__all__ = ["create_runs_app"]
