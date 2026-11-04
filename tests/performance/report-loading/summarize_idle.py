"""Summarize retained read-only samples; do not infer unsampled exact boundaries."""
import json
from datetime import datetime, timedelta
from pathlib import Path

root = Path('.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY')
summary = {}
for version in ('baseline', 'candidate'):
    idle = json.loads((root / f'{version}-idle.json').read_text())
    end = datetime.fromisoformat(idle['finishedAt'])
    start = end - timedelta(minutes=30)
    samples = [s for s in json.loads((root / f'{version}-resources.json').read_text())
               if start <= datetime.fromisoformat(s['at']) <= end]
    first, last = samples[0], samples[-1]
    names = ('identity_sessions', 'identity_refresh_history', 'identity_audit_events')
    def rows(sample):
        return {r[0]: dict(zip(('insert', 'update', 'delete', 'dead_tuples', 'relation_bytes', 'index_bytes'), r[1:]))
                for r in sample['tables'] if r[0] in names}
    a, b = rows(first), rows(last)
    cohort = [r for r in last['activity'] if r[0].startswith(f'W39 {version} load ')]
    api_pid = 35040 if version == 'baseline' else 53625
    rss = [[int(line.split()[2]) * 1024 for line in s['processes'].splitlines()
            if int(line.split()[0]) == api_pid] for s in samples]
    rss = [r[0] for r in rss if r]
    summary[version] = {
        'idle': idle, 'sampled_from': first['at'], 'sampled_until': last['at'],
        'sample_count': len(samples), 'counts_before': dict(first['counts']),
        'counts_after': dict(last['counts']), 'tables_before': a, 'tables_after': b,
        'table_deltas': {name: {key: b[name][key] - a[name][key] for key in a[name]} for name in names},
        'wal_bytes_delta': int(last['wal'][1]) - int(first['wal'][1]),
        'artifact_bytes_before': first['artifact_bytes'], 'artifact_bytes_after': last['artifact_bytes'],
        'cohort_sessions': len(cohort), 'cohort_last_seen_differs_from_created': sum(r[1] != r[2] for r in cohort),
        'api_rss_bytes': {'first': rss[0], 'last': rss[-1], 'min': min(rss), 'max': max(rss)},
        'limitations': ['Samples bracket less than the full 30 minutes; no interpolation.',
                         'Visible iframe count is not a final graph assertion.',
                         'Other QA activity used the host, but separate databases.',
                         'Candidate used the initial one-worker pool limit of 16.'] if version == 'candidate' else
                        ['Reports had expired before the idle interval; zero writes is not successful session maintenance.'],
    }
summary['candidate']['write_attribution'] = {'refresh_history_inserts': 100, 'rotation_session_updates': 100,
    'refresh_audit_inserts': 100, 'diagnostic_login_sessions_and_audit_inserts': 2,
    'activity_updates': 0, 'heartbeat_audit_inserts': 0,
    'basis': 'All 50 candidate last_seen_at values equal created_at; two labelled profile logins; actual rotation counts.'}
(root / 'idle-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps({v: {'activity': summary[v]['cohort_last_seen_differs_from_created'],
                      'wal': summary[v]['wal_bytes_delta']} for v in ('baseline','candidate')}))
