from datetime import UTC, datetime
from io import BytesIO
from uuid import uuid4

from openpyxl import Workbook
import pytest

from packages.contracts.source_intake import SourceIntakeFailure
from packages.data_documentation.domain.model import FileImportTemplateVersion, TemplateColumn
from plugins.connector_files import validate_file


CSV = "text/csv"
XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def template(*, error_policy: str = "reject_rows_with_report") -> FileImportTemplateVersion:
    return FileImportTemplateVersion(
        template_id=uuid4(),
        workspace_id=uuid4(),
        version=1,
        revision=2,
        name="Retail receipts",
        status="published",
        accepted_media_types=(CSV, XLSX),
        allowed_sheet_names=("data",),
        required_sheet_names=("data",),
        columns=(
            TemplateColumn("receipt_id", "receipt_id", "integer", True),
            TemplateColumn("net_amount", "net_amount", "decimal", True),
            TemplateColumn("occurred_on", "occurred_on", "date", True),
        ),
        row_limit=100,
        file_size_limit=1_000_000,
        decimal_separator=".",
        date_format="%Y-%m-%d",
        error_policy=error_policy,  # type: ignore[arg-type]
        created_by=uuid4(),
        created_at=datetime.now(UTC),
    )


def workbook_bytes(rows: list[list[object]]) -> bytes:
    workbook = Workbook()
    sheet = workbook.active
    assert sheet is not None
    sheet.title = "data"
    sheet.append(["receipt_id", "net_amount", "occurred_on"])
    for row in rows:
        sheet.append(row)
    buffer = BytesIO()
    workbook.save(buffer)
    workbook.close()
    return buffer.getvalue()


def test_csv_and_xlsx_produce_the_same_typed_rows_and_schema_identity() -> None:
    published = template()
    csv_result = validate_file(
        published,
        b"receipt_id,net_amount,occurred_on\n1,10.25,2025-01-02\n",
        CSV,
    )
    xlsx_result = validate_file(
        published,
        workbook_bytes([[1, 10.25, "2025-01-02"]]),
        XLSX,
    )

    assert csv_result.rows == xlsx_result.rows
    assert csv_result.schema_fingerprint == xlsx_result.schema_fingerprint
    assert len(csv_result.content_hash) == 64
    assert len(xlsx_result.content_hash) == 64


@pytest.mark.parametrize(
    ("content", "code"),
    [
        (b"receipt_id,net_amount,unexpected\n1,10.25,x\n", "FILE_STRUCTURE_REJECTED"),
        (
            b"receipt_id,net_amount,occurred_on\n1,=2+2,2025-01-02\n",
            "FILE_FORMULA_REJECTED",
        ),
    ],
)
def test_csv_rejects_unknown_structure_and_formula_cells(content: bytes, code: str) -> None:
    with pytest.raises(SourceIntakeFailure) as caught:
        validate_file(template(), content, CSV)

    assert caught.value.code == code


def test_xlsx_rejects_formula_and_unknown_sheet_before_row_materialization() -> None:
    with pytest.raises(SourceIntakeFailure) as formula:
        validate_file(template(), workbook_bytes([[1, "=2+2", "2025-01-02"]]), XLSX)
    assert formula.value.code == "FILE_FORMULA_REJECTED"

    workbook = Workbook()
    sheet = workbook.active
    assert sheet is not None
    sheet.title = "unexpected"
    sheet.append(["receipt_id", "net_amount", "occurred_on"])
    buffer = BytesIO()
    workbook.save(buffer)
    workbook.close()
    with pytest.raises(SourceIntakeFailure) as sheet:
        validate_file(template(), buffer.getvalue(), XLSX)
    assert sheet.value.code == "FILE_SHEET_REJECTED"


def test_rejected_row_report_is_bounded_and_does_not_echo_source_values() -> None:
    result = validate_file(
        template(),
        b"receipt_id,net_amount,occurred_on\n1,not-a-number,2025-01-02\n2,3.50,2025-01-03\n",
        CSV,
    )

    assert len(result.rows) == 1
    assert [(item.row_number, item.code) for item in result.rejected_rows] == [
        (2, "TYPE_OR_REQUIRED_VALUE_INVALID")
    ]
    assert "not-a-number" not in repr(result.rejected_rows)
