"""Redacted, read-only final-profile idle snapshot of the owned fixture DB."""

from pathlib import Path
import json
import sys
import subprocess
from datetime import datetime, UTC
import psycopg

root = Path.cwd()
env = json.loads((root / ".runtime/w39/candidate/connection.json").read_text())
with psycopg.connect(
    host=env["CUSTOMETRY_DATABASE_HOST"],
    port=env["CUSTOMETRY_DATABASE_PORT"],
    dbname=env["CUSTOMETRY_DATABASE_NAME"],
    user=env["CUSTOMETRY_DATABASE_USER"],
    password=Path(env["CUSTOMETRY_DATABASE_PASSWORD_FILE"]).read_text().strip(),
) as connection:
    label = "W39 " + sys.argv[1] + " load %"
    cohort = connection.execute(
        """SELECT count(*),count(*) FILTER (WHERE last_seen_at<>created_at),
        count(*) FILTER (WHERE revoked_at IS NOT NULL),count(DISTINCT principal_id) FROM identity_sessions WHERE device_label LIKE %s""",
        (label,),
    ).fetchone()
    history = connection.execute(
        """SELECT count(*) FROM identity_refresh_history h JOIN identity_sessions s
        ON s.id=h.session_id WHERE s.device_label LIKE %s""",
        (label,),
    ).fetchone()
    audit = connection.execute(
        """SELECT a.action,count(*) FROM identity_audit_events a JOIN identity_sessions s
        ON s.id::text=a.resource_id AND a.resource_type='session'
        WHERE s.device_label LIKE %s GROUP BY a.action ORDER BY a.action""",
        (label,),
    ).fetchall()
    tables = connection.execute("""SELECT relname,n_tup_ins,n_tup_upd,n_tup_del,n_dead_tup,
        pg_relation_size(relid),pg_indexes_size(relid) FROM pg_stat_user_tables
        WHERE relname IN ('identity_sessions','identity_refresh_history','identity_audit_events') ORDER BY relname""").fetchall()
    wal = connection.execute("SELECT wal_records,wal_bytes::text FROM pg_stat_wal").fetchone()
    counts = connection.execute(
        "SELECT 'sessions',count(*) FROM identity_sessions UNION ALL SELECT 'history',count(*) FROM identity_refresh_history UNION ALL SELECT 'audit',count(*) FROM identity_audit_events"
    ).fetchall()
run = json.loads((root / ".runtime/w39/container-run.json").read_text())
processes = subprocess.check_output(
    ["docker", "top", run["name"], "-eo", "pid,ppid,rss,time"], text=True
)
rows = [line.split() for line in processes.splitlines()]
artifacts = Path(env["CUSTOMETRY_DATABASE_PASSWORD_FILE"]).parent / "artifacts"
print(
    json.dumps(
        dict(
            at=datetime.now(UTC).isoformat(),
            cohort_sessions=cohort[0],
            cohort_activity_changed=cohort[1],
            cohort_revoked=cohort[2],
            cohort_principals=cohort[3],
            cohort_history=history[0],
            cohort_audit=dict(audit),
            counts=dict(counts),
            tables=tables,
            wal=wal,
            artifact_bytes=sum(p.stat().st_size for p in artifacts.rglob("*") if p.is_file()),
            api_rss_kib=sum(int(r[2]) for r in rows if len(r) >= 3 and r[0].isdigit()),
            processes=processes,
        )
    )
)
