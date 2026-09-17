"""Fresh stage-owned database; never truncate or downgrade the prepared runtime."""
from pathlib import Path
import subprocess
from uuid import uuid4
import psycopg
from tools.custometry_quality import development_runtime as d

root = Path.cwd()
policy = d.load_policy(root)
paths = d.runtime_paths(root, policy)
control = policy.databases['control-db']
name = 'custometry_ms003_s03_' + uuid4().hex[:12]
with psycopg.connect(host=control.host, port=control.port, dbname=control.database,
    user=control.user, password=(paths.secrets_dir/'control_db_password').read_text().strip(),
    autocommit=True) as c:
    c.execute(psycopg.sql.SQL('CREATE DATABASE {}').format(psycopg.sql.Identifier(name)))
env = d.host_environment(paths, policy, 'api')
env.update(CUSTOMETRY_DATABASE_NAME=name, CUSTOMETRY_TEST_DATABASE_NAME=name,
    CUSTOMETRY_TEST_DATABASE_PASSWORD_FILE=str(paths.secrets_dir/'control_db_password'),
    CUSTOMETRY_TEST_SOURCE_PASSWORD_FILE=str(paths.secrets_dir/'demo_source_reader_password'))
r = subprocess.run(['uv','run','--locked','--package','custometry-api','alembic','-c',
    'migrations/alembic.ini','upgrade','0010_sales_report'], env=env, capture_output=True, text=True)
print('previous-head migration exit=', r.returncode)
if r.returncode:
    raise SystemExit(r.returncode)
raise SystemExit(subprocess.run(['uv','run','--locked','pytest','-q',
    'tests/integration/presentation'], env=env).returncode)
