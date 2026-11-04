"""Public, versioned Semantic workspace-calendar boundary."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, Protocol, Callable
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

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
        "CALENDAR_TIMEZONE_UNAVAILABLE",
        "CALENDAR_ALREADY_CONFIGURED",
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


class ZonedCalendarInputV2(Strict):
    schema_version: Literal["business-calendar/v2"] = "business-calendar/v2"
    kind: Literal["month_based"] = "month_based"
    fiscal_year_start_month: Annotated[int, Field(strict=True, ge=1, le=12)] = 1
    fiscal_year_start_day: Literal[1] = 1
    year_label: Literal["start_year", "end_year"] = "end_year"
    timezone: Annotated[str, Field(min_length=1, max_length=128, pattern=r"^[A-Za-z0-9_+/-]+$")]
    week_start: Literal["monday"] = "monday"
    boundary_policy: Literal["earliest_midnight_or_reject"] = "earliest_midnight_or_reject"
    coverage_basis: Literal["intersecting_utc_source_days"] = "intersecting_utc_source_days"

    @field_validator("fiscal_year_start_day", mode="before")
    @classmethod
    def integer_day(cls, value: object) -> object:
        return BusinessCalendarProfile.integer_day(value)

    @field_validator("timezone")
    @classmethod
    def relative_zone(cls, value: str) -> str:
        if any(not segment or segment in (".", "..") for segment in value.split("/")):
            raise ValueError("CALENDAR_TIMEZONE_UNAVAILABLE")
        return value


class ZonedCalendarProfileV2(ZonedCalendarInputV2):
    tzdata_version: Annotated[str, Field(min_length=1, max_length=32)]
    tzif_base64: Annotated[str, Field(min_length=1, max_length=87384)]
    tzif_sha256: Hash

    @model_validator(mode="after")
    def valid_rules(self) -> ZonedCalendarProfileV2:
        import base64
        import binascii
        import hashlib
        from io import BytesIO
        from zoneinfo import ZoneInfo

        try:
            data = base64.b64decode(self.tzif_base64, validate=True)
            if len(data) > 65536 or hashlib.sha256(data).hexdigest() != self.tzif_sha256:
                raise ValueError("CALENDAR_TIMEZONE_UNAVAILABLE")
            ZoneInfo.from_file(BytesIO(data), key=self.timezone)
        except (ValueError, binascii.Error, EOFError) as exc:
            raise ValueError("CALENDAR_TIMEZONE_UNAVAILABLE") from exc
        return self


CalendarProfile = BusinessCalendarProfile | ZonedCalendarProfileV2
CalendarProfileFactory = Callable[[], tuple[CalendarProfile, str]]


class CalendarRulesPort(Protocol):
    def resolve(self, profile: ZonedCalendarInputV2) -> ZonedCalendarProfileV2: ...


class CalendarRef(Strict):
    version_id: UUID
    content_hash: Hash


class BusinessCalendarVersion(Strict):
    version_id: UUID
    workspace_id: UUID
    content_hash: Hash
    profile: CalendarProfile
    created_by: UUID | None  # null only for system-provisioned January version
    created_at: datetime
    previous_version_id: UUID | None


class WorkspaceCalendarDefault(Strict):
    workspace_id: UUID
    revision: Annotated[int, Field(strict=True, ge=0)]
    calendar: BusinessCalendarVersion


class UpdateCalendarRequest(Strict):
    profile: BusinessCalendarProfile | ZonedCalendarInputV2
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
        profile_factory: CalendarProfileFactory | None = None,
    ) -> WorkspaceCalendarDefault: ...
