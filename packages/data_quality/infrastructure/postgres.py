from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from typing import Any
from uuid import UUID

from psycopg import Connection
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from packages.data_quality.domain.model import QualityReport, QualityWaiver


Connect = Callable[[], Connection[Any]]


class PostgresQualityRepository:
    def __init__(self, connect: Connect) -> None:
        self._connect = connect

    def save_waiver(self, waiver: QualityWaiver) -> None:
        with self._connect() as connection, connection.transaction(), connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO data_quality_waivers
                  (id, workspace_id, rule_id, status, expires_at, approved_by, reason_code)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """,
                (
                    waiver.waiver_id,
                    waiver.workspace_id,
                    waiver.rule_id,
                    waiver.status,
                    waiver.expires_at,
                    waiver.approved_by,
                    waiver.reason_code,
                ),
            )

    def active_waivers(self, *, workspace_id: UUID, now: datetime) -> tuple[QualityWaiver, ...]:
        with self._connect() as connection, connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT id, workspace_id, rule_id, status, expires_at, approved_by, reason_code
                FROM data_quality_waivers
                WHERE workspace_id = %s AND status = 'active' AND expires_at > %s
                """,
                (workspace_id, now),
            )
            rows = cursor.fetchall()
        return tuple(
            QualityWaiver(
                waiver_id=UUID(str(row["id"])),
                workspace_id=UUID(str(row["workspace_id"])),
                rule_id=str(row["rule_id"]),
                status=str(row["status"]),  # type: ignore[arg-type]
                expires_at=row["expires_at"],
                approved_by=UUID(str(row["approved_by"])),
                reason_code=str(row["reason_code"]),
            )
            for row in rows
        )

    @staticmethod
    def record(cursor: Any, report: QualityReport, rule_versions: dict[str, int]) -> None:
        cursor.execute(
            """
            INSERT INTO data_quality_reports
              (id, workspace_id, batch_id, decision, rule_versions, violations,
               applied_waiver_ids, evaluated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                report.report_id,
                report.workspace_id,
                report.batch_id,
                report.decision,
                Jsonb(rule_versions),
                Jsonb(report.as_dict()["violations"]),
                Jsonb([str(item) for item in report.applied_waiver_ids]),
                report.evaluated_at,
            ),
        )
