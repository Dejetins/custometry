"""Upgrade only the current owned Hybrid database and replay the S01 preparation."""
from pathlib import Path
import subprocess
from tools.custometry_quality import development_runtime as d
root=Path.cwd(); policy=d.load_policy(root); paths=d.runtime_paths(root,policy)
env=d.host_environment(paths,policy,'api')
result=subprocess.run(['uv','run','--locked','--package','custometry-api','alembic','-c','migrations/alembic.ini','upgrade','head'],env=env,capture_output=True,text=True)
print('owned runtime migration exit=', result.returncode)
if result.returncode: raise SystemExit(result.returncode)
raise SystemExit(subprocess.run(['uv','run','--locked','python','-m','apps.worker_data.prepare_retail_report'],env=env).returncode)
