"""Real ordinary session and Vite/API save, fresh-process exact reopen and revoke."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import subprocess
import time
from uuid import uuid4
import httpx
from tools.custometry_quality import development_runtime as d

root = Path.cwd()
policy = d.load_policy(root)
paths = d.runtime_paths(root, policy)
prepared = json.loads((paths.runtime_dir/'retail-report-output.json').read_text())
secret = json.loads((paths.secrets_dir/'retail-report.json').read_text())
base = 'http://127.0.0.1:5173'
c = httpx.Client(base_url=base, timeout=60)
origin = {'Origin':base}
proof_label = 'MS-003-S03-' + uuid4().hex[:10]
admin_label = proof_label + '-admin'
auth = c.post('/api/identity/login', json={'email':secret['analyst_email'],
    'password':secret['analyst_password'], 'workspace_id':prepared['workspace_id'],
    'device_label':proof_label}, headers=origin)
assert auth.status_code == 200, auth.status_code
headers = {**origin, 'X-CSRF-Token':auth.json()['csrf_token']}
result = c.post('/api/analytics/sales-reports/v1', json={
    'semantic_dataset_version_id':prepared['semantic_dataset_version_id'],
    'comparison':'previous_year_same_dates'}, headers=headers)
assert result.status_code == 200, result.status_code
result = result.json()
prepare_input = {'contract_version':'draft-report/v1','result_id':result['result_id']}
reply = c.post('/api/reports/prepare', json=prepare_input, headers=headers)
assert reply.status_code == 200, (reply.status_code, reply.text[:100])
refs = reply.json()
request = {**prepare_input, 'title':'Northwind Retail — saved analyst report',
    'expected_revision':0,'idempotency_key':str(uuid4()),
    **{k:refs[k]['reference'] for k in ('chart_spec','brand_profile','company_pack')}}
assert c.post('/api/reports/', json=request).status_code == 403
assert c.post('/api/reports/', json={k:v for k,v in request.items() if k!='contract_version'}, headers=headers).status_code == 422
with ThreadPoolExecutor(max_workers=4) as pool:
    replies = list(pool.map(lambda _:c.post('/api/reports/', json=request, headers=headers), range(4)))
assert all(r.status_code == 200 for r in replies), [r.status_code for r in replies]
saved = replies[0].json()
assert all(r.json() == saved for r in replies)
report_url = '/api/reports/' + saved['report_id']
exact_url = report_url + '/snapshots/' + saved['snapshot_id']
assert c.get(exact_url).json() == saved
assert c.get(exact_url, params={'version_id':saved['version_id'], 'page_id':saved['composition']['default_page_id'], 'block_id':saved['composition']['blocks'][1]['block_id']}).json() == saved
assert c.get(exact_url, params={'page_id':str(uuid4())}).status_code == 404
assert c.get(report_url).headers['cache-control'] == 'no-store'
assert c.get(report_url).json() == saved
assert saved['result'] == result
assert saved['references'] == refs
for name in ('chart_spec','brand_profile','company_pack'):
    invalid = {**request, 'expected_revision':1, 'idempotency_key':str(uuid4()),
        name:{'id':str(uuid4()),'content_hash':'0'*64}}
    failure = c.post(report_url+'/versions', json=invalid, headers=headers)
    assert failure.status_code == 400 and failure.json()['code'] == 'INVALID_REFERENCE'
    assert c.get(report_url).json() == saved
edited = {**request,'title':'Northwind Retail — revision 2','expected_revision':1,'idempotency_key':str(uuid4())}
latest = c.post(report_url+'/versions', json=edited, headers=headers)
assert latest.status_code == 200, latest.status_code
latest = latest.json()
assert latest['revision'] == 2
assert c.get(exact_url).json() == saved
assert c.post(report_url+'/versions', json={**edited,'idempotency_key':str(uuid4())}, headers=headers).status_code == 409
# Inject faults only into the new stage-owned root artifact, then restore exact bytes.
owned_root = paths.runtime_dir / 'artifacts' / 'objects' / (latest['snapshot_id'] + '.json')
root_bytes = owned_root.read_bytes()
try:
    owned_root.write_bytes(b'S03_CORRUPT_OWNED_PREVIEW')
    failed = c.get(report_url)
    assert failed.status_code == 400 and failed.json() == {'code':'ARTIFACT_CORRUPT'}
    owned_root.unlink()
    failed = c.get(report_url)
    assert failed.status_code == 400 and failed.json() == {'code':'ARTIFACT_MISSING'}
finally:
    owned_root.write_bytes(root_bytes)
assert c.get(report_url).json() == latest
# The real installation administrator has no implicit report/source access.
admin = httpx.Client(base_url=base, timeout=30)
admin_login = admin.post('/api/identity/login', json={'email':secret['admin_email'],
    'password':secret['admin_password'], 'workspace_id':prepared['workspace_id'],
    'device_label':admin_label}, headers=origin)
assert admin_login.status_code == 200
admin_headers = {**origin,'X-CSRF-Token':admin_login.json()['csrf_token']}
assert admin.get(report_url).status_code == 404
assert admin.get('/api/reports/').json() == {'reports':[], 'visible_count':0}
admin_sessions = admin.get('/api/identity/sessions').json()['sessions']
admin_current = next(s for s in admin_sessions if s['device_label']==admin_label and not s['revoked'])
assert admin.delete('/api/identity/sessions/'+admin_current['id'], headers=admin_headers).status_code == 204
# A fresh process uses the same durable DB/artifacts and production session adapter.
server = subprocess.Popen(['uv','run','--locked','python', str(Path(__file__).with_name('reopen_server.py'))],
    env=d.host_environment(paths, policy, 'api'), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    restarted = httpx.Client(base_url='http://127.0.0.1:58103', cookies=c.cookies, timeout=10)
    for _ in range(100):
        try:
            if restarted.get('/api/health/live').status_code == 200:
                break
        except httpx.TransportError:
            pass
        assert server.poll() is None, 'fresh API process exited'
        time.sleep(0.1)
    else:
        raise AssertionError('fresh API readiness timeout')
    disabled = restarted.post('/api/analytics/sales-reports/v1', json={
        'semantic_dataset_version_id':prepared['semantic_dataset_version_id']}, headers=headers)
    assert disabled.status_code == 400 and disabled.json()['code'] == 'S03_PROOF_COMPUTATION_AND_SOURCE_DISABLED'
    assert restarted.get(report_url).json() == latest
    assert restarted.get(exact_url).json() == saved
    # Server-side block proof uses the read-only result owner port; no live directory fetch.
    assert latest['result']['trust']['quality_accounting']['quarantined_count'] == 5
    assert len(latest['snapshot']['resolved_document_context']['lineage']['bindings']) == 6
    assert latest['references'] == refs
    sessions = c.get('/api/identity/sessions').json()['sessions']
    current = next(s for s in sessions if s['device_label']==proof_label and not s['revoked'])
    assert c.delete('/api/identity/sessions/'+current['id'], headers=headers).status_code == 204
    assert c.get(report_url).status_code == 401
    assert restarted.get(exact_url).status_code == 401
finally:
    server.terminate()
    server.wait(timeout=10)
out = {'status':'pass','boundary':'real-Vite-HTTP-Identity-PostgreSQL-artifacts-and-fresh-API-process',
    'report_id':saved['report_id'],'snapshot_id':saved['snapshot_id'],'latest_snapshot_id':latest['snapshot_id'],
    'result_id':result['result_id'],'totals':result['totals'],'references':refs,
    'dataset_version_id':prepared['semantic_dataset_version_id'],
    'quality_report_id':result['trust']['quality_report_id'],
    'root_manifest':saved['manifest'],'page_manifest':saved['snapshot']['page_snapshot_refs'][0]['manifest'],
    'same_key_requests':4,'revisions':2,'revoked_session':'denied',
    'fresh_process_compute_source_disabled':'exact latest and historical snapshots reopened'}
Path(__file__).with_name('runtime-proof.json').write_text(json.dumps(out, indent=2, ensure_ascii=False)+'\n')
print(json.dumps({k:out[k] for k in ('status','report_id','snapshot_id','result_id','totals')}, indent=2))
