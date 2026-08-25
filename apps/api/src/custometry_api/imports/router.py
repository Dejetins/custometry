"""Published-template-only API for bounded CSV/XLSX validation."""

from __future__ import annotations

import base64
import binascii
from typing import Annotated, Literal, cast
from uuid import UUID

import psycopg
from fastapi import Depends, FastAPI, Header, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from custometry_api.config import Settings
from packages.contracts.source_intake import (
    SOURCE_INTAKE_API_VERSION,
    SourceIntakeActor,
    SourceIntakeFailure,
)
from packages.data_documentation.application.service import FileImportTemplateService
from packages.data_documentation.domain.model import FileImportTemplateVersion, TemplateColumn
from packages.data_documentation.infrastructure.postgres import PostgresTemplateRepository
from packages.identity_access.application.service import IdentityService
from packages.identity_access.domain.policy import (
    Actor,
    PolicyViolation,
    require_permission,
)
from packages.identity_access.infrastructure.postgres import PostgresIdentityRepository
from plugins.connector_files import validate_file


MediaType = Literal[
    "text/csv",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class TemplateColumnRequest(StrictModel):
    source_header: str = Field(min_length=1, max_length=160)
    field_role: str = Field(min_length=1, max_length=160)
    data_type: Literal["string", "integer", "decimal", "date", "datetime", "boolean"]
    required: bool = True


class TemplateCreateRequest(StrictModel):
    name: str = Field(min_length=1, max_length=160)
    accepted_media_types: list[MediaType] = Field(min_length=1, max_length=2)
    allowed_sheet_names: list[str] = Field(default_factory=lambda: ["data"], max_length=20)
    required_sheet_names: list[str] = Field(default_factory=lambda: ["data"], max_length=20)
    columns: list[TemplateColumnRequest] = Field(min_length=1, max_length=500)
    row_limit: int = Field(default=100_000, ge=1, le=1_000_000)
    file_size_limit: int = Field(default=10_000_000, ge=1, le=100_000_000)
    decimal_separator: Literal[".", ","] = "."
    date_format: str = Field(default="%Y-%m-%d", min_length=2, max_length=80)
    error_policy: Literal["reject_file", "reject_rows_with_report"] = "reject_file"


class TemplatePublishRequest(StrictModel):
    expected_revision: int = Field(ge=1)


class TemplateColumnResponse(TemplateColumnRequest):
    pass


class TemplateResponse(StrictModel):
    template_id: UUID
    version: int
    revision: int
    name: str
    status: Literal["draft", "published", "deprecated", "archived"]
    accepted_media_types: list[str]
    allowed_sheet_names: list[str]
    required_sheet_names: list[str]
    columns: list[TemplateColumnResponse]
    row_limit: int
    file_size_limit: int
    decimal_separator: Literal[".", ","]
    date_format: str
    error_policy: Literal["reject_file", "reject_rows_with_report"]


class FileValidateRequest(StrictModel):
    media_type: MediaType
    content_base64: str = Field(min_length=1, max_length=140_000_000)


class RejectedRowResponse(StrictModel):
    row_number: int = Field(ge=1)
    code: str


class FileValidateResponse(StrictModel):
    template_id: UUID
    template_version: int
    media_type: str
    content_hash: str = Field(min_length=64, max_length=64)
    schema_fingerprint: str = Field(min_length=64, max_length=64)
    accepted_row_count: int = Field(ge=0)
    rejected_rows: list[RejectedRowResponse]


def _status_for(code: str) -> int:
    if code == "AUTHENTICATION_FAILED":
        return status.HTTP_401_UNAUTHORIZED
    if code == "FORBIDDEN":
        return status.HTTP_403_FORBIDDEN
    if code == "NOT_FOUND":
        return status.HTTP_404_NOT_FOUND
    if code == "CONFLICT":
        return status.HTTP_409_CONFLICT
    return status.HTTP_400_BAD_REQUEST


def _services(settings: Settings) -> tuple[IdentityService, FileImportTemplateService]:
    def connect() -> psycopg.Connection[object]:
        return psycopg.connect(
            host=settings.database_host,
            port=settings.database_port,
            dbname=settings.database_name,
            user=settings.database_user,
            password=settings.read_database_password(),
            connect_timeout=settings.database_connect_timeout_seconds,
        )

    def authorize(actor: SourceIntakeActor, permission: str) -> None:
        try:
            require_permission(cast(Actor, actor), permission)
        except PolicyViolation as exc:
            raise SourceIntakeFailure("FORBIDDEN") from exc

    return (
        IdentityService(PostgresIdentityRepository(connect), bootstrap_secret=None),
        FileImportTemplateService(PostgresTemplateRepository(connect), validate_file, authorize),
    )


def _template(template: FileImportTemplateVersion) -> TemplateResponse:
    return TemplateResponse(
        template_id=template.template_id,
        version=template.version,
        revision=template.revision,
        name=template.name,
        status=template.status,
        accepted_media_types=list(template.accepted_media_types),
        allowed_sheet_names=list(template.allowed_sheet_names),
        required_sheet_names=list(template.required_sheet_names),
        columns=[
            TemplateColumnResponse(
                source_header=column.source_header,
                field_role=column.field_role,
                data_type=column.data_type,
                required=column.required,
            )
            for column in template.columns
        ],
        row_limit=template.row_limit,
        file_size_limit=template.file_size_limit,
        decimal_separator=template.decimal_separator,
        date_format=template.date_format,
        error_policy=template.error_policy,
    )


def create_import_app(
    settings: Settings,
    *,
    identity_service: IdentityService | None = None,
    template_service: FileImportTemplateService | None = None,
) -> FastAPI:
    default_identity, default_templates = _services(settings)
    identity = identity_service or default_identity
    templates = template_service or default_templates
    app = FastAPI(
        title="Custometry File Import API",
        version=SOURCE_INTAKE_API_VERSION,
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi.json",
    )

    @app.exception_handler(SourceIntakeFailure)
    async def failure_handler(_: Request, exc: SourceIntakeFailure) -> JSONResponse:
        return JSONResponse(status_code=_status_for(exc.code), content={"code": exc.code})

    def authenticated(authorization: Annotated[str | None, Header()] = None) -> Actor:
        if authorization is None:
            raise SourceIntakeFailure("AUTHENTICATION_FAILED")
        scheme, _, token = authorization.partition(" ")
        if scheme.casefold() != "bearer" or not token:
            raise SourceIntakeFailure("AUTHENTICATION_FAILED")
        try:
            return identity.authenticate(token)
        except Exception as exc:
            raise SourceIntakeFailure("AUTHENTICATION_FAILED") from exc

    @app.post(
        "/templates",
        response_model=TemplateResponse,
        operation_id="create_file_import_template",
    )
    def create_template(
        payload: TemplateCreateRequest, actor: Actor = Depends(authenticated)
    ) -> TemplateResponse:
        columns = tuple(
            TemplateColumn(
                source_header=item.source_header,
                field_role=item.field_role,
                data_type=item.data_type,
                required=item.required,
            )
            for item in payload.columns
        )
        data = payload.model_dump(exclude={"columns"})
        return _template(
            templates.create_draft(
                actor,
                accepted_media_types=tuple(data.pop("accepted_media_types")),
                allowed_sheet_names=tuple(data.pop("allowed_sheet_names")),
                required_sheet_names=tuple(data.pop("required_sheet_names")),
                columns=columns,
                **data,
            )
        )

    @app.post(
        "/templates/{template_id}/publish",
        response_model=TemplateResponse,
        operation_id="publish_file_import_template",
    )
    def publish_template(
        template_id: UUID,
        payload: TemplatePublishRequest,
        actor: Actor = Depends(authenticated),
    ) -> TemplateResponse:
        return _template(
            templates.publish(actor, template_id, expected_revision=payload.expected_revision)
        )

    @app.post(
        "/templates/{template_id}/validate",
        response_model=FileValidateResponse,
        operation_id="validate_file_import",
    )
    def validate(
        template_id: UUID,
        payload: FileValidateRequest,
        actor: Actor = Depends(authenticated),
    ) -> FileValidateResponse:
        try:
            content = base64.b64decode(payload.content_base64, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise SourceIntakeFailure("FILE_ENCODING_REJECTED") from exc
        result = templates.validate(
            actor,
            template_id,
            content=content,
            media_type=payload.media_type,
        )
        return FileValidateResponse(
            template_id=result.template_id,
            template_version=result.template_version,
            media_type=result.media_type,
            content_hash=result.content_hash,
            schema_fingerprint=result.schema_fingerprint,
            accepted_row_count=len(result.rows),
            rejected_rows=[
                RejectedRowResponse(row_number=item.row_number, code=item.code)
                for item in result.rejected_rows
            ],
        )

    _ = (failure_handler, create_template, publish_template, validate)
    return app
