"""Record bounded final command outcomes and the exact owned source manifest."""
from datetime import UTC, datetime
import hashlib
import json
from pathlib import Path
import shlex
import subprocess

root = Path.cwd()
stage = root / '.codex/delivery/evidence/MS-003/MS-003-S03'
python_targets = [
    'packages/presentation/application/reports.py', 'packages/presentation/domain',
    'packages/presentation/infrastructure', 'packages/contracts/presentation',
    'packages/contracts/generate_reports_client.py',
    'packages/artifacts/infrastructure/document_snapshots.py',
    'apps/api/src/custometry_api/reports', 'apps/api/src/custometry_api/main.py',
    'apps/api/src/custometry_api/analytics/router.py',
    'migrations/versions/0011_presentation_drafts.py',
    'tests/unit/presentation', 'tests/contract/presentation', 'tests/integration/presentation',
]
commands = [
    ['uv','run','--locked','pytest','-q','tests/unit/presentation','tests/contract/presentation',
        'tests/unit/analytics','tests/contract/analytics'],
    ['uv','run','--locked','python',str(stage.relative_to(root)/'run_tests.py')],
    ['uv','run','--locked','python',str(stage.relative_to(root)/'verify_runtime.py')],
    ['uv','run','--locked','ruff','check',*python_targets],
    ['uv','run','--locked','pyright',*python_targets],
    ['pnpm','--filter','@custometry/contracts','typecheck'],
    ['uv','run','--locked','python','-m','tools.check','--scope','local'],
    ['git','diff','--check'],
]
evidence = {'status':'running','profile':'prompt-pack/v1',
    'created_at':datetime.now(UTC).isoformat(), 'commands':[],
    'proof_boundary':'real local PostgreSQL, production owner services, immutable artifacts, authenticated HTTP and fresh API process; no browser/package/release'}
for command in commands:
    completed = subprocess.run(command, capture_output=True, text=True)
    output = completed.stdout + completed.stderr
    # Keep only command summaries, never whole pytest traces or provider payloads.
    summary = [line for line in output.splitlines() if (' passed' in line or ' failed' in line
        or 'All checks passed' in line or line.startswith('PASS ') or '0 errors' in line
        or line.startswith('previous-head migration exit='))]
    if command[-1].endswith('verify_runtime.py') and completed.returncode == 0:
        summary = ['Real authenticated HTTP, reference integrity, root faults and fresh-process reopen passed.']
    evidence['commands'].append({'command':shlex.join(command),'exit_code':completed.returncode,
        'status':'pass' if completed.returncode == 0 else 'fail','summary':summary})
    (stage/'validation-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print(shlex.join(command), 'exit=', completed.returncode, flush=True)
    if completed.returncode:
        print(output[-6000:])
        raise SystemExit(completed.returncode)
tracked = subprocess.check_output(['git','diff','--name-only'],text=True).splitlines()
new = subprocess.check_output(['git','ls-files','--others','--exclude-standard'],text=True).splitlines()
owned = []
for path in sorted(set(tracked + new)):
    if path == '.codex/delivery/ledgers/MS-003.md' or path.startswith(str(stage.relative_to(root))):
        continue
    file = root/path
    owned.append({'path':path,'change':'created' if path in new else 'modified',
        'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
evidence.update(status='pass', completed_at=datetime.now(UTC).isoformat(), owned_source_manifest=owned,
    foreign_changes_excluded=[], deleted_paths=[],
    extra_provider_path_reason='Artifact Lifecycle owns root/page manifest IO; Presentation uses only its public port.')
(stage/'validation-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
print('S03 final validation passed', flush=True)
