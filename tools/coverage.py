#!/usr/bin/env python3
"""Creator coverage per system (Zack 2026-11-25): how much Griffy / Pulse / Nocturne say about each system,
how recent, and a bucket to decide on. Same claim matching as tools/lookup.py (tag 'system' == the system's slug).
Writes sources/findings/coverage_table.md + .json.  Usage: tools/coverage.py
Buckets on recent ADVICE claims (priority/how-to/setup/skip/warning/target, 2024-06+): GAP 0 | THIN 1-5 | OK 6-19 | STRONG 20+ with 5+ from Griffy.
Note: systems sharing a tag (the 4 lab parts, alchemy parts) share counts; read per-item detail with tools/lookup.py.
"""
import csv, glob, json
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
IDX = yaml.safe_load(open(ROOT / 'model' / 'system_index.yaml'))
MAP = yaml.safe_load(open(ROOT / 'model' / 'data_map.yaml'))
USEFUL = {'priority', 'how_to', 'setup', 'skip', 'warning', 'target', 'comparison', 'meta_change', 'opinion', 'mechanic'}
ADVICE = {'priority', 'how_to', 'setup', 'skip', 'warning', 'target'}
CUT = '2024-06'

by_slug = defaultdict(list)
for f in glob.glob(str(ROOT / 'sources/creators/*/tags/*.csv')):
    for r in csv.DictReader(open(f)):
        if r.get('claim_type') in USEFUL:
            by_slug[r.get('system')].append(r)

rows = []
for s, v in sorted(IDX.items()):
    if MAP.get(s, {}).get('meta'):
        continue
    tr = v.get('transcripts'); slug = (tr.get('slug') if isinstance(tr, dict) else None) or s
    tg = MAP.get(s, {}).get('tags') or [slug]; kw = MAP.get(s, {}).get('kw') or []
    pool = [r for t in tg for r in by_slug.get(t, [])] + ([r for rs in by_slug.values() for r in rs if any(k in r['statement'].lower() for k in kw)] if kw else [])
    seen, cl = set(), []
    for r in pool:
        k = (r['creator'], r['statement'])
        if k not in seen:
            seen.add(k); cl.append(r)
    per = {}
    for c in ('griffybit', 'pulseidle', 'nocturne'):
        mine = [r for r in cl if r['creator'] == c]
        rec = [r for r in mine if r.get('date', '') >= CUT]
        dates = sorted(r['date'] for r in mine if r.get('date', '')[:2] == '20')
        per[c] = {'all': len(mine), 'recent': len(rec), 'advice': sum(1 for r in rec if r['claim_type'] in ADVICE), 'newest': dates[-1] if dates else ''}
    other = [r for r in cl if r['creator'] not in per]
    recent = sum(p['recent'] for p in per.values())
    advice = sum(p['advice'] for p in per.values())
    total = sum(p['all'] for p in per.values())
    g = per['griffybit']['advice']
    if advice == 0:
        b = 'GAP'
    elif advice <= 5:
        b = 'THIN'
    elif advice >= 20 and g >= 5:
        b = 'STRONG'
    else:
        b = 'OK'
    newest = max([p['newest'] for p in per.values()] + [''])
    rows.append({'system': s, 'owners': v.get('owners', []), 'bucket': b, 'recent': recent, 'advice': advice, 'total': total,
                 'newest': newest, 'per': per, 'other': len(other), 'in_parser': bool(MAP.get(s, {}).get('path'))})

order = ['GAP', 'THIN', 'OK', 'STRONG']
rows.sort(key=lambda r: (order.index(r['bucket']), r['advice'], r['system']))
cnt = {b: sum(1 for r in rows if r['bucket'] == b) for b in order}
md = ['# Creator coverage per system', f"Claims tagged to each system (recent = {CUT}+; advice = priority/how-to/setup/skip/warning/target).",
      ' | '.join(f"{b}: {n}" for b, n in cnt.items()), '',
      '| system | owner | bucket | recent (advice) | Griffy | Pulse | Nocturne | newest | data |', '|---|---|---|---|---|---|---|---|---|']
for r in rows:
    p = r['per']
    f = lambda c: f"{p[c]['recent']}/{p[c]['all']}" if p[c]['all'] else '-'
    md.append(f"| {r['system']} | {', '.join(o[6:] if o.startswith('Autist') else o for o in r['owners']) or '-'} | {r['bucket']} | {r['recent']} ({r['advice']}) | "
              f"{f('griffybit')} | {f('pulseidle')} | {f('nocturne')} | {r['newest']} | {'yes' if r['in_parser'] else 'AR/raw'} |")
md += ['', 'Creator columns = recent/all claims. "data" = numbers available from the Toolbox parser.']
(ROOT / 'sources/findings/coverage_table.md').write_text('\n'.join(md) + '\n')
json.dump(rows, open(ROOT / 'sources/findings/coverage_table.json', 'w'), indent=1)
print(' | '.join(f"{b}: {n}" for b, n in cnt.items()))
for b in order[:3]:
    pass
for b in order:
    print(b + ':', ', '.join(f"{r['system']}({r['advice']})" for r in rows if r['bucket'] == b))
