"""Real S01 publication -> HTTP report -> independent readonly SQL and artifact bytes."""
from pathlib import Path
from decimal import Decimal
from concurrent.futures import ThreadPoolExecutor
import hashlib, json
import httpx, psycopg
from tools.custometry_quality import development_runtime as d
root=Path.cwd(); p=d.load_policy(root); paths=d.runtime_paths(root,p)
prepared=json.loads((paths.runtime_dir/'retail-report-output.json').read_text())
secret=json.loads((paths.secrets_dir/'retail-report.json').read_text())
base='http://127.0.0.1:5173'; origin={'Origin':base}
c=httpx.Client(base_url=base,timeout=60)
auth=c.post('/api/identity/login',json={'email':secret['analyst_email'],'password':secret['analyst_password'],'workspace_id':prepared['workspace_id'],'device_label':'MS-003-S02-proof'},headers=origin)
assert auth.status_code==200, auth.status_code
headers={**origin,'X-CSRF-Token':auth.json()['csrf_token']}
request={'semantic_dataset_version_id':prepared['semantic_dataset_version_id'],'comparison':'previous_year_same_dates'}
endpoint='/api/analytics/sales-reports/v1'
assert c.post(endpoint,json=request).status_code==403
with ThreadPoolExecutor(max_workers=4) as pool:
    replies=list(pool.map(lambda _:c.post(endpoint,json=request,headers=headers),range(4)))
assert all(r.status_code==200 for r in replies), [r.status_code for r in replies]
result=replies[0].json(); assert all(r.json()==result for r in replies)
cases=[]
with psycopg.connect(host='127.0.0.1',port=55433,dbname='northwind_retail',user='demo_reader',password=(paths.secrets_dir/'demo_source_reader_password').read_text().strip(),options='-c default_transaction_read_only=on') as db:
    for store,start,end in ((None,'2025-01-01','2025-11-30'),('1','2025-01-01','2025-11-30'),(None,'2024-01-01','2024-11-30'),(None,'2025-06-01','2025-06-30')):
        query={**request,'starts_on':start,'ends_on':end,'store_id':store}
        reply=c.post(endpoint,json=query,headers=headers); assert reply.status_code==200,reply.status_code
        actual=reply.json()
        expected=db.execute("""SELECT sum(net_amount),count(DISTINCT receipt_id),count(*) FILTER(WHERE customer_id IS NULL)
          FROM retail.receipts WHERE status='completed' AND currency='EUR'
          AND (receipt_datetime AT TIME ZONE 'UTC')::date BETWEEN %s AND %s
          AND (%s::text IS NULL OR store_id::text=%s)""",(start,end,store,store)).fetchone()
        assert Decimal(actual['totals']['net_revenue'])==expected[0]
        assert Decimal(actual['totals']['receipt_count'])==expected[1]
        assert Decimal(actual['totals']['average_receipt'])==expected[0]/expected[1]
        daily=db.execute("""SELECT (receipt_datetime AT TIME ZONE 'UTC')::date,sum(net_amount),count(DISTINCT receipt_id)
          FROM retail.receipts WHERE status='completed' AND currency='EUR'
          AND (receipt_datetime AT TIME ZONE 'UTC')::date BETWEEN %s AND %s
          AND (%s::text IS NULL OR store_id::text=%s) GROUP BY 1 ORDER BY 1""",(start,end,store,store)).fetchall()
        actual_days={r['date']:r for r in actual['daily']}
        for day,net,count in daily:
            a=actual_days[str(day)]; assert Decimal(a['net_revenue'])==net and Decimal(a['receipt_count'])==count
        raw=(paths.runtime_dir/'artifacts'/actual['manifest']['relative_uri']).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==actual['manifest']['content_hash']
        assert json.loads(raw)=={k:v for k,v in actual.items() if k!='manifest'}
        cases.append({'store_id':store,'start':start,'end':end,'result_id':actual['result_id'],'artifact_hash':actual['manifest']['content_hash'],'totals':actual['totals'],'anonymous_receipts':expected[2],'daily_sql_rows':len(daily)})
    assert result['comparison']['totals']==cases[2]['totals']
    assert db.execute('SELECT min(n),max(n) FROM (SELECT count(*) n FROM retail.receipt_items GROUP BY receipt_id) x').fetchone()==(3,3)
    quarantined=db.execute("""SELECT count(DISTINCT r.receipt_id), sum(r.net_amount) FROM retail.receipts r
      WHERE r.status='completed' AND r.currency='EUR' AND EXISTS
      (SELECT 1 FROM retail.receipt_items i WHERE i.receipt_id=r.receipt_id AND i.product_id=999999)""").fetchone()
assert len(result['lineage']['bindings'])==6
assert result['trust']['quality_accounting']['quarantined_count']==5
for key in ('product_id','category','brand'):
    assert c.post(endpoint,json={**request,key:'x'},headers=headers).status_code==422
assert c.post(endpoint,json={**request,'store_id':"1 OR 1=1"},headers=headers).status_code==400
assert c.get(endpoint+'/'+result['result_id']).status_code==200
# Revoke only this freshly created proof session through the real Identity API.
sessions=c.get('/api/identity/sessions').json()['sessions']
current=next(s for s in sessions if s['device_label']=='MS-003-S02-proof' and not s['revoked'])
assert c.delete('/api/identity/sessions/'+current['id'],headers=headers).status_code==204
assert c.get(endpoint+'/'+result['result_id']).status_code==401
assert c.post(endpoint,json=request,headers=headers).status_code==401
out={'status':'pass','boundary':'real-S01-source-HTTP-PostgreSQL-artifacts','dataset_version_id':prepared['semantic_dataset_version_id'],'metric_versions':result['metrics'],'cases':cases,'concurrent_identical_requests':4,'quarantined_item_linked_eligible_headers':{'count':quarantined[0],'net_amount':str(quarantined[1])},'quality_report_id':result['trust']['quality_report_id'],'revoked_session_read_and_reuse':'denied','unsupported_dimensions':'rejected','daily_source_sql':'matched each observed day; bounded unobserved days explicitly unavailable'}
(root/'.codex/delivery/evidence/MS-003/MS-003-S02/runtime-reconciliation.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'pass','cases':cases,'revocation':'denied'},indent=2))
