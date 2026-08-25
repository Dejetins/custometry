"""Published file-import template contracts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from uuid import UUID


@dataclass(frozen=True, slots=True)
class TemplateColumn:
    source_header: str
    field_role: str
    data_type: Literal["string", "integer", "decimal", "date", "datetime", "boolean"]
    required: bool


@dataclass(frozen=True, slots=True)
class FileImportTemplateVersion:
    template_id: UUID
    workspace_id: UUID
    version: int
    revision: int
    name: str
    status: Literal["draft", "published", "deprecated", "archived"]
    accepted_media_types: tuple[str, ...]
    allowed_sheet_names: tuple[str, ...]
    required_sheet_names: tuple[str, ...]
    columns: tuple[TemplateColumn, ...]
    row_limit: int
    file_size_limit: int
    decimal_separator: Literal[".", ","]
    date_format: str
    error_policy: Literal["reject_file", "reject_rows_with_report"]
    created_by: UUID
    created_at: datetime


@dataclass(frozen=True, slots=True)
class RejectedRow:
    row_number: int
    code: str


@dataclass(frozen=True, slots=True)
class ValidatedFileImport:
    template_id: UUID
    template_version: int
    media_type: str
    content_hash: str
    schema_fingerprint: str
    rows: tuple[dict[str, object], ...]
    rejected_rows: tuple[RejectedRow, ...]
