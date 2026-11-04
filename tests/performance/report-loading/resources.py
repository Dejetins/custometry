"""Read-only measurements of the task-owned database, artifacts and process tree."""

from pathlib import Path
import json
import sys
import time
import subprocess
from datetime import datetime, UTC
import psycopg

root = Path.cwd()
version = sys.argv[1]
runtime = root / ".runtime/w39" / ("candidate" if version.startswith("candidate") else "")
env = json.loads((runtime / "connection.json").read_text())


def sample():
    with psycopg.connect(
        host=env["CUSTOMETRY_DATABASE_HOST"],
        port=env["CUSTOMETRY_DATABASE_PORT"],
        dbname=env["CUSTOMETRY_DATABASE_NAME"],
        user=env["CUSTOMETRY_DATABASE_USER"],
        password=Path(env["CUSTOMETRY_DATABASE_PASSWORD_FILE"]).read_text().strip(),
    ) as c:
        tables = c.execute(
            "SELECT relname,n_tup_ins,n_tup_upd,n_tup_del,n_dead_tup,pg_relation_size(relid),pg_indexes_size(relid) FROM pg_stat_user_tables ORDER BY relname"
        ).fetchall()
        wal = c.execute("SELECT wal_records,wal_bytes::text FROM pg_stat_wal").fetchone()
        counts = c.execute(
            "SELECT 'sessions',count(*) FROM identity_sessions UNION ALL SELECT 'history',count(*) FROM identity_refresh_history UNION ALL SELECT 'audit',count(*) FROM identity_audit_events"
        ).fetchall()
        activity = c.execute(
            "SELECT device_label,last_seen_at::text,created_at::text,revoked_at IS NOT NULL FROM identity_sessions WHERE device_label LIKE 'W39 %% load %%' ORDER BY device_label"
        ).fetchall()
    artifacts = Path(env["CUSTOMETRY_DATABASE_PASSWORD_FILE"]).parent / "artifacts"
    pids = set()
    for port in (58140, 41740) if version.startswith("candidate") else (58139, 41739):
        out = subprocess.run(
            ["lsof", "-nP", f"-iTCP:{port}", "-sTCP:LISTEN", "-t"], capture_output=True, text=True
        ).stdout
        pids.update(int(p) for p in out.split())
    if len(sys.argv) > 2:
        stack = [int(sys.argv[2])]
        while stack:
            pid = stack.pop()
            if pid in pids:
                continue
            pids.add(pid)
            children = subprocess.run(
                ["pgrep", "-P", str(pid)], capture_output=True, text=True
            ).stdout
            stack.extend(int(p) for p in children.split())
    proc = (
        subprocess.run(
            ["ps", "-p", ",".join(map(str, sorted(pids))), "-o", "pid=,ppid=,rss=,time="],
            capture_output=True,
            text=True,
        ).stdout
        if pids
        else ""
    )
    return dict(
        at=datetime.now(UTC).isoformat(),
        tables=tables,
        wal=wal,
        counts=counts,
        activity=activity,
        artifact_bytes=sum(p.stat().st_size for p in artifacts.rglob("*") if p.is_file()),
        processes=proc,
    )


version = sys.argv[1]
out = (
    root
    / f".codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/{version}-resources.json"
)
records = []
for _ in range(int(sys.argv[5]) if len(sys.argv) > 5 else 121):
    records.append(sample())
    out.write_text(json.dumps(records, indent=2))
    print(f"{version}: resource sample {len(records)}", flush=True)
    time.sleep(float(sys.argv[4]) if len(sys.argv) > 4 else 30)
