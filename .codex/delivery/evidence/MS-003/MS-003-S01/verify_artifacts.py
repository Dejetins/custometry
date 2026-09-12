from pathlib import Path
from decimal import Decimal
import hashlib,json
import psycopg
import pyarrow.parquet as pq
from tools.custometry_quality import development_runtime as d
root=Path.cwd(); p=d.load_policy(root); paths=d.runtime_paths(root,p)
o=json.loads((paths.runtime_dir/'retail-report-output.json').read_text())
artifacts={a['entity']:a for a in o['artifacts']}
rows={}
for entity,a in artifacts.items():
 path=paths.runtime_dir/'artifacts'/a['relative_uri']
 assert hashlib.sha256(path.read_bytes()).hexdigest()==a['content_hash']
 table=pq.read_table(path)
 assert table.num_rows==a['row_count']
 rows[entity]=table.to_pylist()
with psycopg.connect(host='127.0.0.1',port=55433,dbname='northwind_retail',user='demo_reader',password=(paths.secrets_dir/'demo_source_reader_password').read_text().strip(),options='-c default_transaction_read_only=on') as c:
 source=c.execute('SELECT currency, count(*), sum(net_amount), count(*) FILTER (WHERE customer_id IS NULL) FROM retail.receipts GROUP BY currency ORDER BY currency').fetchall()
 raw_count=c.execute('SELECT count(*) FROM retail.receipt_items').fetchone()[0]
negative=[r for r in rows['QuarantineReceiptItem']]
canonical={}
for r in rows['Receipt']:
 key=r['currency']; v=canonical.setdefault(key,[0,Decimal(0),0]);v[0]+=1;v[1]+=r['net_amount'];v[2]+=int(r['customer_id'] is None)
assert {r[0]:list(r[1:]) for r in source}==canonical
assert raw_count==15000 and len(negative)==5 and len(rows['ReceiptItem'])==14995
summary={'status':'pass','boundary':'readonly-source-SQL-to-committed-Parquet',
'counts':{e:len(r) for e,r in rows.items()},
'receipt_totals_by_currency':{k:{'count':v[0],'net_amount':str(v[1]),'anonymous_count':v[2]} for k,v in canonical.items()},
'quality_accounting':o['publication']['impact_summary']['quality_accounting'],
'ids':{k:v for k,v in o.items() if k.endswith('_id')},
'artifacts':[{'entity':a['entity'],'id':a['artifact_id'],'content_hash':a['content_hash'],'row_count':a['row_count'],'relative_uri':a['relative_uri']} for a in o['artifacts']],
'bindings':o['publication']['bindings'], 'relationships':o['publication']['impact_summary']['relationships'],
'calendar_date_min':str(min(r['calendar_date'] for r in rows['Calendar'])),
'calendar_date_max':str(max(r['calendar_date'] for r in rows['Calendar'])),
'policy':o['publication']['impact_summary']['relationship_policy'],
'source_fingerprint':o['source_fingerprint']}
(root/'.codex/delivery/evidence/MS-003/MS-003-S01/artifact-reconciliation.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'pass','counts':summary['counts'],'receipt_totals_by_currency':summary['receipt_totals_by_currency']},indent=2))
