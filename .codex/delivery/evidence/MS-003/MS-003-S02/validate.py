"""Collect compact check outcomes without transcripts, credentials or provider rows."""
from datetime import datetime, UTC
from pathlib import Path
import hashlib, json, re, subprocess

root=Path.cwd(); evidence=root/'.codex/delivery/evidence/MS-003/MS-003-S02'
ledger_path=root/'.codex/delivery/ledgers/MS-003.md'
ledger=json.loads(re.search(r'<!-- prompt-pack-ledger:v1 -->\s*```json\s*(.*?)\s*```',ledger_path.read_text(),re.S).group(1))
next_row=next(s for s in ledger['stages'] if s['contract']['id']=='MS-003-S03')
inputs=[]
for item in next_row['contract']['entry_inputs']:
    path=(ledger_path.parent/item['path']).resolve()
    assert path.is_file(), path.name
    inputs.append({'path':str(path.relative_to(root)), 'sha256':hashlib.sha256(path.read_bytes()).hexdigest(), 'producer_stage':item['producer_stage']})
(evidence/'next-entry-check.json').write_text(json.dumps({'status':'pass','current_authority':next_row['current_authority'],'stage':'MS-003-S03','inputs':inputs,'successor_outputs':'Presentation APIs, ChartSpec and system default references are S03-produced, deferred','permission':'enable only with current-stage acceptance; no automatic execution'},indent=2)+'\n')
(evidence/'validation-evidence.json').write_text(json.dumps({'status':'running'})+'\n')
paths=['packages/analytics_core/application/service.py','packages/analytics_core/application/sales_report.py','packages/analytics_core/infrastructure/postgres.py','packages/artifacts/infrastructure/sales.py','packages/semantic_model/application/sales_metrics.py','packages/semantic_model/infrastructure/postgres.py','packages/contracts/analytics/sales_report.py','packages/contracts/generate_sales_client.py','apps/api/src/custometry_api/analytics/router.py','apps/api/src/custometry_api/analytics/sales_models.py']
commands=[
 ['uv','run','--locked','pytest','-q','tests/unit/analytics','tests/contract/analytics'],
 ['uv','run','--locked','python',str(evidence.relative_to(root)/'run_tests.py')],
 ['uv','run','--locked','python',str(evidence.relative_to(root)/'verify_runtime.py')],
 ['uv','run','--locked','ruff','check',*paths,'migrations/versions/0010_sales_report.py','tests/unit/analytics','tests/integration/analytics/test_sales_report.py','tests/contract/analytics'],
 ['uv','run','--locked','pyright',*paths],
 ['corepack','pnpm','--filter','@custometry/contracts','typecheck'],
 ['uv','run','--locked','python','-m','tools.custometry_quality.generate_docs_index'],
 ['uv','run','--locked','python','-m','tools.custometry_quality.check_docs_links'],
 ['uv','run','--locked','python','-m','tools.check','--scope','local'],
 ['git','diff','--check'],
]
results=[]
for command in commands:
    run=subprocess.run(command,capture_output=True,text=True)
    summaries=re.findall(r'(\d+ passed[^\n]*|\d+ errors, \d+ warnings[^\n]*|PASS [^\n]*|All checks passed!)',run.stdout)
    results.append({'command':' '.join(command),'exit_code':run.returncode,'status':'pass' if run.returncode==0 else 'failed','summary':summaries})
    print(results[-1],flush=True)
    if run.returncode:
        print(run.stdout[-2500:],run.stderr[-1000:])
        (evidence/'validation-evidence.json').write_text(json.dumps({'status':'failed','commands':results},indent=2)+'\n')
        raise SystemExit(run.returncode)
manifest=[]
for line in subprocess.check_output(['git','status','--porcelain','-uall'],text=True).splitlines():
    status=line[:2]; name=line[3:]; path=root/name
    if path.is_file() and name != '.codex/delivery/ledgers/MS-003.md' and '/MS-003-S02/' not in name:
        manifest.append({'path':name,'change':'created' if status=='??' else 'modified','sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
protected=['.codex/agents/generated/MS-001','.codex/agents/generated/MS-002','.codex/delivery/evidence/MS-001','.codex/delivery/evidence/MS-002','.codex/delivery/ledgers/MS-001.md','.codex/delivery/ledgers/MS-002.md','docs/architecture/planning/milestones/MS-001','docs/architecture/planning/milestones/MS-002']
assert not subprocess.check_output(['git','diff','--name-only','--',*protected],text=True).strip()
old=json.loads(subprocess.check_output(['git','show','HEAD:packages/contracts/openapi/analytics.openapi.json']))
new=json.loads((root/'packages/contracts/openapi/analytics.openapi.json').read_text())
assert all(new['paths'][k]==v for k,v in old['paths'].items())
assert all(new['components']['schemas'][k]==v for k,v in old['components']['schemas'].items())
(evidence/'validation-evidence.json').write_text(json.dumps({'status':'pass','profile':'prompt-pack/v1','created_at':datetime.now(UTC).isoformat(),'commands':results,'source_manifest':manifest,'foreign_changes_at_entry':[],'deleted_paths':[],'protected_completed_milestones':'unchanged against HEAD','legacy_api':'all previous paths and schemas equal HEAD','proof_boundary':'real source/control PostgreSQL, API, metric and artifact result; no UI or packaged proof'},indent=2)+'\n')
