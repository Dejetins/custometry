"""PostgreSQL adapter for immutable file-template versions."""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from typing import Any, Literal, cast
from uuid import UUID, uuid4

from psycopg import Connection
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from packages.contracts.source_intake import SourceIntakeFailure
from packages.data_documentation.domain.model import FileImportTemplateVersion, TemplateColumn


Connect = Callable[[], Connection[Any]]


class PostgresTemplateRepository:
    def __init__(self, connect: Connect) -> None:
        self._connect = connect

    @staticmethod
    def _columns(template: FileImportTemplateVersion) -> list[dict[str, object]]:
        return [
            {
                "source_header": column.source_header,
                "field_role": column.field_role,
                "data_type": column.data_type,
                "required": column.required,
            }
            for column in template.columns
        ]

    def create(self, template: FileImportTemplateVersion) -> None:
        with self._connect() as connection, connection.transaction(), connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO file_import_templates
                  (id, workspace_id, current_version, created_by, created_at, updated_at)
                VALUES (%s, %s, 1, %s, %s, %s)
                """,
                (
                    template.template_id,
                    template.workspace_id,
                    template.created_by,
                    template.created_at,
                    template.created_at,
                ),
            )
            cursor.execute(
                """
                INSERT INTO file_import_template_versions
                  (template_id, version, revision, name, status, accepted_media_types,
                   allowed_sheet_names, required_sheet_names, columns, row_limit,
                   file_size_limit, decimal_separator, date_format, error_policy,
                   created_by, created_at)
                VALUES (%s, 1, 1, %s, 'draft', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    template.template_id,
                    template.name,
                    Jsonb(list(template.accepted_media_types)),
                    Jsonb(list(template.allowed_sheet_names)),
                    Jsonb(list(template.required_sheet_names)),
                    Jsonb(self._columns(template)),
                    template.row_limit,
                    template.file_size_limit,
                    template.decimal_separator,
                    template.date_format,
                    template.error_policy,
                    template.created_by,
                    template.created_at,
                ),
            )

    @staticmethod
    def _model(row: dict[str, object]) -> FileImportTemplateVersion:
        raw_columns = row["columns"]
        if not isinstance(raw_columns, list):
            raise SourceIntakeFailure("TEMPLATE_CORRUPT")
        column_values = cast(list[object], raw_columns)
        parsed_columns: list[TemplateColumn] = []
        for raw_item in column_values:
            if not isinstance(raw_item, dict):
                raise SourceIntakeFailure("TEMPLATE_CORRUPT")
            item = cast(dict[str, object], raw_item)
            parsed_columns.append(
                TemplateColumn(
                    source_header=str(item["source_header"]),
                    field_role=str(item["field_role"]),
                    data_type=cast(
                        Literal["string", "integer", "decimal", "date", "datetime", "boolean"],
                        str(item["data_type"]),
                    ),
                    required=bool(item["required"]),
                )
            )
        media_types = cast(list[object], row["accepted_media_types"])
        allowed_sheets = cast(list[object], row["allowed_sheet_names"])
        required_sheets = cast(list[object], row["required_sheet_names"])
        return FileImportTemplateVersion(
            template_id=UUID(str(row["template_id"])),
            workspace_id=UUID(str(row["workspace_id"])),
            version=int(str(row["version"])),
            revision=int(str(row["revision"])),
            name=str(row["name"]),
            status=str(row["status"]),  # type: ignore[arg-type]
            accepted_media_types=tuple(str(item) for item in media_types),
            allowed_sheet_names=tuple(str(item) for item in allowed_sheets),
            required_sheet_names=tuple(str(item) for item in required_sheets),
            columns=tuple(parsed_columns),
            row_limit=int(str(row["row_limit"])),
            file_size_limit=int(str(row["file_size_limit"])),
            decimal_separator=str(row["decimal_separator"]),  # type: ignore[arg-type]
            date_format=str(row["date_format"]),
            error_policy=str(row["error_policy"]),  # type: ignore[arg-type]
            created_by=UUID(str(row["created_by"])),
            created_at=cast(datetime, row["created_at"]),
        )

    def get(self, *, workspace_id: UUID, template_id: UUID) -> FileImportTemplateVersion | None:
        with self._connect() as connection, connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT t.workspace_id, v.*
                FROM file_import_templates AS t
                JOIN file_import_template_versions AS v
                  ON v.template_id = t.id AND v.version = t.current_version
                WHERE t.workspace_id = %s AND t.id = %s
                """,
                (workspace_id, template_id),
            )
            row = cursor.fetchone()
        return None if row is None else self._model(row)

    def publish(
        self,
        *,
        workspace_id: UUID,
        template_id: UUID,
        expected_revision: int,
        actor_id: UUID,
        at: datetime,
    ) -> FileImportTemplateVersion:
        with (
            self._connect() as connection,
            connection.transaction(),
            connection.cursor(row_factory=dict_row) as cursor,
        ):
            cursor.execute(
                """
                UPDATE file_import_template_versions AS v
                SET status = 'published', revision = revision + 1
                FROM file_import_templates AS t
                WHERE t.id = v.template_id AND t.workspace_id = %s
                  AND v.template_id = %s AND v.version = t.current_version
                  AND v.status = 'draft' AND v.revision = %s
                RETURNING t.workspace_id, v.*
                """,
                (workspace_id, template_id, expected_revision),
            )
            row = cursor.fetchone()
            if row is None:
                raise SourceIntakeFailure("CONFLICT")
            cursor.execute(
                """
                INSERT INTO source_intake_audit_events
                  (id, workspace_id, actor_id, action, resource_type, resource_id, metadata)
                VALUES (%s, %s, %s, 'file_import_template.published', 'file_import_template', %s, %s)
                """,
                (uuid4(), workspace_id, actor_id, str(template_id), Jsonb({"version": 1})),
            )
        return self._model(row)
