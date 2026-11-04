"""Warm single-request CPU profile of the real editor route and JSON serialization.

This excludes waits/other threads via thread_time and is diagnostic, not an SLA
measurement. Synthetic login is outside the profile. No response data is saved.
"""
from pathlib import Path
import cProfile
import io
import json
import os
import pstats
from time import thread_time
from uuid import UUID
from starlette.requests import Request
from custometry_api.config import Settings
from custometry_api.identity.router import create_identity_service
from custometry_api.reports.router import create_reports_app

root = Path.cwd()
os.environ.update(json.loads((root / '.runtime/w39/candidate/connection.json').read_text()))
settings = Settings(analytics_artifact_root=Path(os.environ['CUSTOMETRY_DATABASE_PASSWORD_FILE']).parent / 'artifacts')
fixture = json.loads((root / '.runtime/w39/load-fixtures.json').read_text())[0]
login = create_identity_service(settings).login(email=fixture['email'], password='synthetic-w39-password', workspace_id=UUID(fixture['workspace']), device_label='W39 CPU profile')
route = next(r for r in create_reports_app(settings).routes if getattr(r, 'path', '') == '/v2/{report_id}' and 'GET' in getattr(r, 'methods', set()))

def read():
    request = Request({'type': 'http', 'method': 'GET', 'headers': [(b'authorization', ('Bearer ' + login.access_token).encode())]})
    value = route.endpoint(UUID(fixture['report']), request)
    if hasattr(value, "model_dump_json"):
        return value.model_dump_json().encode()
    return value.body

read()
profile = cProfile.Profile(timer=thread_time)
profile.enable()
read()
profile.disable()
buffer = io.StringIO()
pstats.Stats(profile, stream=buffer).sort_stats('cumulative').print_stats(50)
(root / '.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/candidate-cpu-profile.txt').write_text(buffer.getvalue())
print(buffer.getvalue())

if os.environ.get('W39_SQL_COUNTS') == '1':
    import re
    import psycopg
    from collections import Counter
    counts = Counter()
    execute = psycopg.Cursor.execute
    def counted(cursor, query, *args, **kwargs):
        table = re.search(r'\bFROM\s+([a-z_]+)', str(query), re.IGNORECASE)
        counts[table[1] if table else 'other'] += 1
        return execute(cursor, query, *args, **kwargs)
    psycopg.Cursor.execute = counted
    try:
        read()
    finally:
        psycopg.Cursor.execute = execute
    (root / '.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/metadata-query-counts.json').write_text(json.dumps(dict(counts), indent=2))

if os.environ.get('W39_PARSE_BENCH') == '1':
    from pydantic_core import from_json
    import statistics
    payload = read()
    parsers = {'stdlib': json.loads, 'pydantic_core': lambda body: from_json(body, cache_strings=False)}
    assert parsers['stdlib'](payload) == parsers['pydantic_core'](payload)
    timings = {}
    for name, parser in parsers.items():
        for _ in range(5):
            parser(payload)
        samples = []
        for _ in range(100):
            start = thread_time()
            parser(payload)
            samples.append((thread_time() - start) * 1000)
        timings[name] = {'median_cpu_ms': statistics.median(samples), 'samples_cpu_ms': samples}
    (root / '.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY/json-parser-diagnostic.json').write_text(json.dumps({'bytes': len(payload), 'equal_values': True, 'string_cache': False, 'timings': timings}, indent=2))
