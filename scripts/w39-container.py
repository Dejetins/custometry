"""Task-owned API beside its PostgreSQL, with source and resource identities."""
import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import time

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--version', choices=['baseline', 'candidate'], required=True)
parser.add_argument('--port', type=int, choices=[58142, 58143, 58160], required=True)
parser.add_argument('--workers', type=int, choices=[8], required=True)
args = parser.parse_args()
balanced = os.environ.get('W39_BALANCED') == '1'
runtime = root / '.runtime/w39' / ('candidate' if args.version == 'candidate' else '')
settings = json.loads((runtime / 'connection.json').read_text())
password = Path(settings['CUSTOMETRY_DATABASE_PASSWORD_FILE'])
source = root if args.version == 'candidate' else root / '.runtime/w39/baseline'
database = 'custometry-w39-candidate-c67c' if args.version == 'candidate' else 'custometry-w39-3100d0f03545'
name = f'custometry-w39-api-{args.version}-{os.getpid()}'
image = subprocess.check_output(['docker', 'image', 'inspect', '--format', '{{.Id}}', 'custometry-w39-api:c67c'], text=True).strip()
env = {**settings, 'CUSTOMETRY_DATABASE_HOST': database, 'CUSTOMETRY_DATABASE_PORT': '5432',
       'CUSTOMETRY_DATABASE_PASSWORD_FILE': '/run/secrets/password',
       'CUSTOMETRY_ANALYTICS_ARTIFACT_ROOT': '/data/artifacts',
       'CUSTOMETRY_CORS_ALLOWED_ORIGINS': '["http://127.0.0.1:41742","http://127.0.0.1:41743","http://127.0.0.1:41746","http://localhost:41746"]',
       'CUSTOMETRY_IDENTITY_COOKIE_SECURE': 'false',
       'PYTHONPATH': '/workspace/apps/api/src:/workspace:/opt/w39scripts'}
if args.version == 'candidate':
    if os.environ.get('W39_THREAD_LIMIT'):
        env['CUSTOMETRY_API_SYNC_THREAD_LIMIT'] = os.environ['W39_THREAD_LIMIT']
    if os.environ.get('W39_GC_THRESHOLD'):
        env['CUSTOMETRY_API_GC_ALLOCATION_THRESHOLD'] = os.environ['W39_GC_THRESHOLD']
env.update({key: value for key, value in os.environ.items() if key in {
    'W39_THREAD_LIMIT', 'W39_GC_THRESHOLD', 'W39_THREAD_SWITCH_SECONDS', 'W39_POOL_SIZE', 'W39_INSTRUMENT'}})
command = ['docker', 'run', '--rm', '--name', name, '--label', 'custometry.owner=W39',
           '--network', 'custometry-w39-serving-c67c', '--memory', '4g', '--cpus', '8',
           '--mount', f'type=bind,src={source},dst=/workspace,readonly',
           '--mount', f'type=bind,src={root / "scripts"},dst=/opt/w39scripts,readonly',
           '--mount', f'type=bind,src={password},dst=/run/secrets/password,readonly',
           '--mount', f'type=bind,src={password.parent / "artifacts"},dst=/data/artifacts']
for offset in range(8 if balanced else 1):
    command.extend(['-p', f'127.0.0.1:{args.port+offset}:{8000+offset}'])
for key, value in env.items():
    command.extend(['-e', f'{key}={value}'])
command.extend([image, 'python', '/opt/w39scripts/w39-container-workers.py'] if balanced else [image, 'python', '-m', 'uvicorn',
    'w39_instrumented:create_app' if os.environ.get('W39_INSTRUMENT') == '1' else 'custometry_api.main:create_app',
    '--factory', '--host', '0.0.0.0', '--port', '8000', '--workers', str(args.workers),
    '--timeout-graceful-shutdown', '3', '--log-level', 'warning', '--no-access-log'])
(root / '.runtime/w39/container-run.json').write_text(json.dumps({
    'name': name, 'image': image, 'version': args.version, 'workers': args.workers,
    'apiCpuLimit': 8, 'apiMemoryGiB': 4, 'databaseCpuLimit': 4, 'databaseMemoryGiB': 2,
    'network': 'custometry-w39-serving-c67c', 'sourceReadOnly': True, 'balanced': balanced,
    'database': database, 'at': time.time()}, indent=2))
child = subprocess.Popen(command)
stopped = False
def stop(*_):
    global stopped
    stopped = True
signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGINT, stop)
try:
    while not stopped and child.poll() is None:
        time.sleep(.1)
finally:
    if child.poll() is None:
        subprocess.run(['docker', 'stop', '--time', '3', name], capture_output=True, timeout=10)
        child.wait(timeout=5)
raise SystemExit(child.returncode)
