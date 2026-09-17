"""Create and remove only this invocation's isolated test database."""

import os
import subprocess
from pathlib import Path
from uuid import uuid4
import psycopg
from psycopg import sql
from tools.custometry_quality import development_runtime as d

root = Path.cwd()
policy = d.load_policy(root)
paths = d.runtime_paths(root, policy)
control = policy.databases["control-db"]
name = "custometry_ms003_s04_" + uuid4().hex[:12]
connection = dict(
    host=control.host,
    port=control.port,
    dbname=control.database,
    user=control.user,
    password=(paths.secrets_dir / "control_db_password").read_text().strip(),
)
with psycopg.connect(**connection, autocommit=True) as c:
    c.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(name)))
env = {**os.environ, **d.host_environment(paths, policy, "api")}
env.update(
    CUSTOMETRY_DATABASE_NAME=name,
    CUSTOMETRY_TEST_DATABASE_NAME=name,
    CUSTOMETRY_TEST_DATABASE_PASSWORD_FILE=str(paths.secrets_dir / "control_db_password"),
    CUSTOMETRY_TEST_SOURCE_PASSWORD_FILE=str(paths.secrets_dir / "demo_source_reader_password"),
)
try:
    r = subprocess.run(
        [
            "uv",
            "run",
            "--locked",
            "--package",
            "custometry-api",
            "alembic",
            "-c",
            "migrations/alembic.ini",
            "upgrade",
            "head",
        ],
        env=env,
        capture_output=True,
    )
    assert r.returncode == 0, "isolated migration failed"
    raise SystemExit(
        subprocess.run(
            [
                "uv",
                "run",
                "--locked",
                "pytest",
                "-q",
                "tests/integration/presentation/test_report_context.py",
            ],
            env=env,
        ).returncode
    )
finally:
    with psycopg.connect(**connection, autocommit=True) as c:
        c.execute(sql.SQL("DROP DATABASE {}").format(sql.Identifier(name)))
