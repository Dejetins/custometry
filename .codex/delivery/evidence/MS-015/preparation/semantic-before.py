"""Public, versioned Semantic workspace-calendar boundary."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, Protocol
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator

Hash = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class CalendarFailure(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


class CalendarError(Strict):
    code: Literal[
        "AUTHENTICATION_FAILED",
        "FORBIDDEN",
        "CSRF_FAILED",
        "NOT_FOUND",
        "CALENDAR_REVISION_CONFLICT",
        "CALENDAR_IDEMPOTENCY_CONFLICT",
        "STORAGE_UNAVAILABLE",
    ]


class BusinessCalendarProfile(Strict):
    schema_version: Literal["business-calendar/v1"] = "business-calendar/v1"
    kind: Literal["month_based"] = "month_based"
    fiscal_year_start_month: Annotated[int, Field(strict=True, ge=1, le=12)] = 1
    fiscal_year_start_day: Literal[1] = 1
    year_label: Literal["start_year", "end_year"] = "end_year"
    timezone: Literal["UTC"] = "UTC"
    week_start: Literal["monday"] = "monday"

    @field_validator("fiscal_year_start_day", mode="before")
    @classmethod
    def integer_day(cls, value: object) -> object:
        if type(value) is not int:
            raise ValueError("UNSUPPORTED_CALENDAR_PROFILE")
        return value


class CalendarRef(Strict):
    version_id: UUID
    content_hash: Hash


class BusinessCalendarVersion(Strict):
    version_id: UUID
    workspace_id: UUID
    content_hash: Hash
    profile: BusinessCalendarProfile
    created_by: UUID | None  # null only for system-provisioned January version
    created_at: datetime
    previous_version_id: UUID | None


class WorkspaceCalendarDefault(Strict):
    workspace_id: UUID
    revision: Annotated[int, Field(strict=True, ge=0)]
    calendar: BusinessCalendarVersion


class UpdateCalendarRequest(Strict):
    profile: BusinessCalendarProfile
    expected_revision: Annotated[int, Field(strict=True, ge=0)]
    idempotency_key: UUID


class CalendarActor(Protocol):
    @property
    def workspace_id(self) -> UUID: ...
    @property
    def principal_id(self) -> UUID: ...
    @property
    def permissions(self) -> frozenset[str]: ...


class WorkspaceCalendarPort(Protocol):
    def provision(self, workspace_id: UUID) -> None: ...
    def get_default(self, workspace_id: UUID, actor: CalendarActor) -> WorkspaceCalendarDefault: ...
    def get_version(self, ref: CalendarRef, actor: CalendarActor) -> BusinessCalendarVersion: ...
    def update_default(
        self, request: UpdateCalendarRequest, actor: CalendarActor
    ) -> WorkspaceCalendarDefault: ...


class CalendarRepository(Protocol):
    def provision(
        self,
        workspace_id: UUID,
        version_id: UUID,
        profile: BusinessCalendarProfile,
        content_hash: str,
    ) -> None: ...
    def get_default(self, workspace_id: UUID) -> WorkspaceCalendarDefault: ...
    def get_version(self, workspace_id: UUID, version_id: UUID) -> BusinessCalendarVersion: ...
    def update_default(
        self,
        workspace_id: UUID,
        principal_id: UUID,
        request: UpdateCalendarRequest,
        content_hash: str,
        request_hash: str,
    ) -> WorkspaceCalendarDefault: ...
