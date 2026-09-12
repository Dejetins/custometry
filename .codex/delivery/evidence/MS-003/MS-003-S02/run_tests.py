from pathlib import Path
import os, subprocess
import psycopg
from tools.custometry_quality import development_runtime as d
root=Path.cwd(); policy=d.load_policy(root); paths=d.runtime_paths(root,policy)
control=policy.databases['control-db']
name='custometry_ms003_s02_tests'
with psycopg.connect(host=control.host,port=control.port,dbname=control.database,user=control.user,password=(paths.secrets_dir/'control_db_password').read_text().strip(),autocommit=True) as c:
    if not c.execute('SELECT 1 FROM pg_database WHERE datname=%s',(name,)).fetchone():
        c.execute(psycopg.sql.SQL('CREATE DATABASE {}').format(psycopg.sql.Identifier(name)))
env=d.host_environment(paths,policy,'api')
env.update(CUSTOMETRY_DATABASE_NAME=name, CUSTOMETRY_TEST_DATABASE_NAME=name,
           CUSTOMETRY_TEST_DATABASE_PASSWORD_FILE=str(paths.secrets_dir/'control_db_password'),
           CUSTOMETRY_TEST_SOURCE_PASSWORD_FILE=str(paths.secrets_dir/'demo_source_reader_password'))
r=subprocess.run(['uv','run','--locked','--package','custometry-api','alembic','-c','migrations/alembic.ini','upgrade','head'],env=env,capture_output=True,text=True)
print('test-database migration exit=',r.returncode)
if r.returncode: raise SystemExit(r.returncode)
raise SystemExit(subprocess.run(['uv','run','--locked','pytest','-q','tests/integration/analytics'],env=env).returncode)
