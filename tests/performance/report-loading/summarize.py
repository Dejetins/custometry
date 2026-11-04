"""Nearest-rank timing summaries with all failure counts retained."""
import json
import math
from pathlib import Path

root = Path('.codex/delivery/evidence/W39-REPORT-LOADING-SESSION-EFFICIENCY')

def quantiles(values):
    values = sorted(v for v in values if v is not None)
    return {'n': len(values), **{f'p{p}': values[max(0, math.ceil(len(values)*p/100)-1)]
                                for p in (50,75,95,99)}} if values else {'n': 0}

summaries = {}
for path in sorted(root.glob('*w-*.json')):
    data = json.loads(path.read_text())
    if not isinstance(data, dict) or 'records' not in data:
        continue
    records = data['records']
    ok = [r for r in records if r['status'] == 'passed']
    result = {'attempts': len(records), 'passed': len(ok), 'failures': len(records)-len(ok),
              'failure_statuses': sorted({r['status'] for r in records if r['status'] != 'passed'}),
              'concurrency': data.get('concurrency'), 'workers': data.get('workers'),
              'preconditionConcurrency': data.get('preconditionConcurrency', 50),
              'units': 'milliseconds except heap/cache byte sizes',
              'successful_open_timings': {key: quantiles([r.get(key) for r in ok])
                                         for key in ('frameMs','firstGraphMs','allCardsMs')},
              'concurrent_interaction_events': quantiles([e['duration'] for r in ok for e in r.get('interactions', [])]),
              'foreground_two_toggle_latency_upper_bound': quantiles([
                  max([16, *[e['duration'] for e in r['foregroundInteractions']]])
                  for r in ok if 'foregroundInteractions' in r and 'foregroundInteractionError' not in r]),
              'foreground_censored_below_16ms_pages': sum(not r['foregroundInteractions'] for r in ok if 'foregroundInteractions' in r),
              'foreground_interaction_failures': sum('foregroundInteractionError' in r for r in ok),
              'large_json_parse': quantiles([e['duration'] for r in ok for e in r.get('parse', [])]),
              'heap_used_bytes': quantiles([m['value'] for r in ok for m in r.get('heap', []) if m['name']=='JSHeapUsedSize']),
              'notes': ['Quantiles cover successful openings only; failure counts remain explicit.',
                        'Event Timing values below 16ms are censored, not recorded as zero.',
                        'Concurrent interaction stress is not a typical single foreground interaction.']}
    spans=[]
    for r in ok:
        entries=[e for e in r.get('resources', []) if 0<=e['end']<=r['firstGraphMs']]
        if entries:
            spans.append({'dispatch': min(e['start'] for e in entries),
                          'last_complete_response_to_graph': r['firstGraphMs']-max(e['end'] for e in entries)})
    result['browser_spans']={key:quantiles([s[key] for s in spans]) for key in ('dispatch','last_complete_response_to_graph')}
    summaries[path.name]=result
(root/'timing-summary.json').write_text(json.dumps(summaries,indent=2)+'\n')
print(json.dumps({k:{'attempts':v['attempts'],'failures':v['failures']} for k,v in summaries.items()}))
