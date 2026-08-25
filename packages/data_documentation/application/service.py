"""Template lifecycle and governed file-validation use cases."""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from typing import Protocol
from uuid import UUID, uuid4

from packages.contracts.source_intake import (
    PermissionAuthorizer,
    SourceIntakeActor,
    SourceIntakeFailure,
)
from packages.data_documentation.domain.model import (
    FileImportTemplateVersion,
    TemplateColumn,
    ValidatedFileImport,
)


class TemplateRepository(Protocol):
    def create(self, template: FileImportTemplateVersion) -> None: ...

    def get(self, *, workspace_id: UUID, template_id: UUID) -> FileImportTemplateVersion | None: ...

    def publish(
        self,
        *,
        workspace_id: UUID,
        template_id: UUID,
        expected_revision: int,
        actor_id: UUID,
        at: datetime,
    ) -> FileImportTemplateVersion: ...


FileValidator = Callable[[FileImportTemplateVersion, bytes, str], ValidatedFileImport]


class FileImportTemplateService:
    def __init__(
        self,
        repository: TemplateRepository,
        validator: FileValidator,
        authorize: PermissionAuthorizer,
    ) -> None:
        self._repository = repository
        self._validator = validator
        self._authorize = authorize

    def _permission(self, actor: SourceIntakeActor, permission: str) -> None:
        self._authorize(actor, permission)

    def create_draft(
        self,
        actor: SourceIntakeActor,
        *,
        name: str,
        accepted_media_types: tuple[str, ...],
        allowed_sheet_names: tuple[str, ...],
        required_sheet_names: tuple[str, ...],
        columns: tuple[TemplateColumn, ...],
        row_limit: int,
        file_size_limit: int,
        decimal_separator: str,
        date_format: str,
        error_policy: str,
    ) -> FileImportTemplateVersion:
        self._permission(actor, "file_import_template.manage")
        supported = {
            "text/csv",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        }
        headers = [column.source_header for column in columns]
        if (
            not name.strip()
            or not accepted_media_types
            or not set(accepted_media_types) <= supported
            or not columns
            or len(headers) != len(set(headers))
            or not 1 <= row_limit <= 1_000_000
            or not 1 <= file_size_limit <= 100_000_000
            or decimal_separator not in {".", ","}
            or error_policy not in {"reject_file", "reject_rows_with_report"}
            or not date_format
            or not set(required_sheet_names) <= set(allowed_sheet_names)
        ):
            raise SourceIntakeFailure("INVALID_INPUT")
        now = datetime.now(UTC)
        template = FileImportTemplateVersion(
            template_id=uuid4(),
            workspace_id=actor.workspace_id,
            version=1,
            revision=1,
            name=name.strip(),
            status="draft",
            accepted_media_types=accepted_media_types,
            allowed_sheet_names=allowed_sheet_names,
            required_sheet_names=required_sheet_names,
            columns=columns,
            row_limit=row_limit,
            file_size_limit=file_size_limit,
            decimal_separator=decimal_separator,  # type: ignore[arg-type]
            date_format=date_format,
            error_policy=error_policy,  # type: ignore[arg-type]
            created_by=actor.principal_id,
            created_at=now,
        )
        self._repository.create(template)
        return template

    def publish(
        self, actor: SourceIntakeActor, template_id: UUID, *, expected_revision: int
    ) -> FileImportTemplateVersion:
        self._permission(actor, "file_import_template.publish")
        return self._repository.publish(
            workspace_id=actor.workspace_id,
            template_id=template_id,
            expected_revision=expected_revision,
            actor_id=actor.principal_id,
            at=datetime.now(UTC),
        )

    def validate(
        self,
        actor: SourceIntakeActor,
        template_id: UUID,
        *,
        content: bytes,
        media_type: str,
    ) -> ValidatedFileImport:
        self._permission(actor, "file_import.create")
        template = self._repository.get(workspace_id=actor.workspace_id, template_id=template_id)
        if template is None:
            raise SourceIntakeFailure("NOT_FOUND")
        if template.status != "published":
            raise SourceIntakeFailure("TEMPLATE_NOT_PUBLISHED")
        return self._validator(template, content, media_type)
