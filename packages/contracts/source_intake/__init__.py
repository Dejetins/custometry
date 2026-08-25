"""Stable public identifiers for the Source Intake API."""

from collections.abc import Callable
from typing import Final, Protocol
from uuid import UUID


class SourceIntakeFailure(ValueError):
    """Stable failure code without source or secret detail."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


class SourceIntakeActor(Protocol):
    """Minimum identity projection accepted by source-intake use cases."""

    @property
    def principal_id(self) -> UUID: ...

    @property
    def workspace_id(self) -> UUID: ...


PermissionAuthorizer = Callable[[SourceIntakeActor, str], None]


SOURCE_INTAKE_API_VERSION: Final = "1.0.0"
POSTGRESQL_CONNECTOR_ID: Final = "postgresql"
CSV_TEMPLATE_MEDIA_TYPE: Final = "text/csv"
XLSX_TEMPLATE_MEDIA_TYPE: Final = (
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


__all__ = [
    "CSV_TEMPLATE_MEDIA_TYPE",
    "POSTGRESQL_CONNECTOR_ID",
    "PermissionAuthorizer",
    "SOURCE_INTAKE_API_VERSION",
    "SourceIntakeActor",
    "SourceIntakeFailure",
    "XLSX_TEMPLATE_MEDIA_TYPE",
]
