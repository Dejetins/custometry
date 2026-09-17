"""Backup the owned pre-upgrade control DB, then apply the additive migration."""
from pathlib import Path
from datetime import UTC, datetime
import hashlib
import json
import os
import subprocess
from tools.custometry_quality import development_runtime as d

root = Path.cwd()
policy = d.load_policy(root)
paths = d.runtime_paths(root, policy)
private = paths.runtime_dir / 'ms003-s03-backups'
private.mkdir(mode=0o700, exist_ok=True)
backup = private / (datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ') + '.dump')
env = {**os.environ, **d.host_environment(paths, policy, 'api'),
    'CUSTOMETRY_HYBRID_PROJECT_NAME':paths.project_name,
    'CUSTOMETRY_CONTROL_DB_PORT':str(policy.databases['control-db'].port),
    'CUSTOMETRY_DEMO_DB_PORT':str(policy.databases['demo-source-db'].port),
    'CUSTOMETRY_SECRETS_DIR':str(paths.secrets_dir), 'CUSTOMETRY_DATA_PROFILE':'demo',
    'CUSTOMETRY_ALLOW_BENCHMARK':'0'}
command = d.compose_command(paths, policy, 'exec', '-T', 'control-db', 'pg_dump',
    '-U', policy.databases['control-db'].user, '-d', policy.databases['control-db'].database, '-Fc')
fd = os.open(backup, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
with os.fdopen(fd, 'wb') as output:
    r = subprocess.run(command, env=env, stdout=output, stderr=subprocess.PIPE)
assert r.returncode == 0, 'owned backup failed'
assert backup.stat().st_size > 0
migration = subprocess.run(['uv','run','--locked','--package','custometry-api','alembic','-c',
    'migrations/alembic.ini','upgrade','head'], env=env, capture_output=True)
assert migration.returncode == 0, 'owned migration failed'
evidence = {'status':'pass', 'backup_retained_in_protected_owned_runtime':True,
    'backup_sha256':hashlib.sha256(backup.read_bytes()).hexdigest(),
    'backup_bytes':backup.stat().st_size, 'migration':'0010_sales_report -> 0011_presentation_drafts',
    'rollback':'Pre-upgrade backup with retained immutable artifacts or forward repair; no lossless document downgrade.'}
(root/'.codex/delivery/evidence/MS-003/MS-003-S03/runtime-upgrade.json').write_text(json.dumps(evidence, indent=2)+'\n')
print('owned backup retained; additive migration passed')
