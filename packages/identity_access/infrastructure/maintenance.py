"""Privileged bounded retention adapter; never exposed as an application delete API."""

from datetime import UTC, datetime, timedelta
from time import monotonic
from packages.identity_access.infrastructure.postgres import Connect


class IdentityMaintenance:
    def __init__(self, connect: Connect):
        self.connect = connect

    def run(
        self,
        *,
        at: datetime | None = None,
        session_days: int = 7,
        audit_days: int = 90,
        batch_size: int = 500,
        max_batches: int = 32,
        budget_seconds: float = 2,
    ) -> dict[str, int | str]:
        if not (
            session_days >= 7
            and audit_days >= 1
            and 1 <= batch_size <= 1000
            and 1 <= max_batches <= 100
            and 0 < budget_seconds <= 30
        ):
            raise ValueError("INVALID_RETENTION_BUDGET")
        at = at or datetime.now(UTC)
        started = monotonic()
        sessions = events = histories = 0
        with self.connect() as c, c.transaction():
            c.execute("SET LOCAL statement_timeout = '2000ms'")
            c.execute("SET LOCAL lock_timeout = '100ms'")
            lock = c.execute("SELECT pg_try_advisory_xact_lock(390023)").fetchone()
            if not lock or not lock[0]:
                return {"status": "busy", "sessions": 0, "events": 0}
            last = c.execute(
                "SELECT last_completed_at FROM identity_maintenance_state WHERE id=1 FOR UPDATE"
            ).fetchone()
            if last and last[0] and last[0] > at - timedelta(days=1):
                return {"status": "not_due", "sessions": 0, "events": 0}

            def statement_budget() -> None:
                remaining = budget_seconds - (monotonic() - started)
                if remaining <= 0:
                    raise TimeoutError("IDENTITY_RETENTION_BUDGET_EXHAUSTED")
                c.execute(
                    "SELECT set_config('statement_timeout', %s, true)",
                    (str(max(1, int(remaining * 1000))),),
                )

            for _ in range(max_batches):
                if monotonic() - started >= budget_seconds:
                    break
                statement_budget()
                history = c.execute(
                    """DELETE FROM identity_refresh_history WHERE token_hash IN (
                    SELECT h.token_hash FROM identity_refresh_history h JOIN identity_sessions s ON s.id=h.session_id
                    WHERE s.absolute_expires_at < %s ORDER BY s.absolute_expires_at,s.id
                    LIMIT %s FOR UPDATE OF h SKIP LOCKED) RETURNING token_hash""",
                    (at - timedelta(days=session_days), batch_size),
                ).fetchall()
                histories += len(history)
                statement_budget()
                rows = c.execute(
                    """DELETE FROM identity_sessions WHERE id IN (
                    SELECT id FROM identity_sessions s WHERE absolute_expires_at < %s
                    AND NOT EXISTS(SELECT 1 FROM identity_refresh_history h WHERE h.session_id=s.id)
                    ORDER BY absolute_expires_at,id LIMIT %s FOR UPDATE SKIP LOCKED)
                    RETURNING id""",
                    (at - timedelta(days=session_days), batch_size),
                ).fetchall()
                sessions += len(rows)
                statement_budget()
                old = c.execute(
                    """DELETE FROM identity_audit_events WHERE id IN (
                    SELECT id FROM identity_audit_events WHERE occurred_at < %s
                    AND (action LIKE 'session.%%' OR action LIKE 'password.%%')
                    ORDER BY occurred_at,id LIMIT %s FOR UPDATE SKIP LOCKED)
                    RETURNING id""",
                    (at - timedelta(days=audit_days), batch_size),
                ).fetchall()
                events += len(old)
                if len(history) < batch_size and len(rows) < batch_size and len(old) < batch_size:
                    break
            c.execute(
                """UPDATE identity_maintenance_state SET last_completed_at=%s,
                sessions_deleted=sessions_deleted+%s, events_deleted=events_deleted+%s WHERE id=1""",
                (at, sessions, events),
            )
        return {
            "status": "completed",
            "sessions": sessions,
            "events": events,
            "histories": histories,
        }
