"""Decision layer v1: reads reports/<save>/report.json + brain (reserves, plans, links, checklist) and writes
reports/<save>/decisions.md + decisions.json. Every system gets a verdict; Claude reviews this file before cards.
Verdicts: DO (in-game action) / HOLD (reserve or conflict, with why) / NOTHING (with why) / BUILD (nothing checks it) / FIX (planner error).
Lines that are information, not actions, stay in the Report and never reach cards.
"""
import json, re, yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SAVE = (ROOT / 'snapshots' / 'LATEST').read_text().strip()
OUT = ROOT / 'reports' / SAVE
rep = json.load(open(OUT / 'report.json'))
reserves = yaml.safe_load(open(ROOT / 'brain' / 'reserves.yaml')) or {}
check = [l for l in (ROOT / 'brain' / 'checklist_2026-11-21.md').read_text().splitlines() if l.strip().startswith('- [ ]')]

ACT = re.compile(r'^\W*(push|buy|spend|move|take|use|level|swap|put|collect|claim|read|cook|unlock|turn in|equip|switch|set|send|fight|do|grab|craft|vote|plant|trade|start|run|reset|feed|upgrade|max|get|go|keep)\b', re.I)
SPEND = re.compile(r'\b(spend|use|buy|put|level|upgrade|cook|trade)\b', re.I)
GOAL = re.compile(r'\b(POW|Spelunk\w*|Pillar Coral|Seaweed Street|Jelly|Sushi|amber|Vibrant Coral|Boomy)\b', re.I)
INFO = re.compile(r'^(TOP:|CREATORS:|WHY:|Note:|\(|Now on|Printing:|Prayers on:)', re.I)

def plan_written(slug):
    p = ROOT / 'brain' / 'systems' / f'{slug}.md'
    return p.exists() and bool(re.search(r'## Plan\n- Now: \S', p.read_text()))

def reserve_hit(line):
    if re.search(r"\b(don't|do not|never) (spend|use)\b|Griffy: ", line, re.I): return None   # warnings and quotes aren't spends
    for res, holds in reserves.items():
        for h in holds:
            if re.search(h['match'], line, re.I): return f"{res} held for {h['for']}: {h['why']}"
    return None

TARGET = re.compile(r'\bpush\b.*\bto\b.*\(now ', re.I)   # multi-day targets: stay in the Report, not cards
def classify(line, src=''):
    if line.startswith('PARK: '): return 'park'
    if TARGET.search(line) or re.search(r'nothing needed|nothing to buy', line, re.I): return 'info'
    if src == 'card_engine' and not INFO.match(line.split(': ', 1)[-1]): return 'do'
    if INFO.match(line) or not ACT.match(line.split(': ', 1)[-1] if ':' in line[:40] else line): return 'info'
    return 'do'

dec, by_char, holes = [], {}, []
for s in rep['systems']:
    slug, owners = s['system'], s['owners'] or ['account']
    chk = [c for c in check if f'[[{slug}]]' in c]
    if s['errors']:
        dec.append({'system': slug, 'verdict': 'FIX', 'why': '; '.join(s['errors'])}); holes.append((3, f'{slug}: planner broken')); continue
    if not s['planners']:
        nx = [n for n in s.get('notes', []) if n.startswith('Next:')]
        for o in owners: by_char.setdefault(o, {'goal': [], 'do': [], 'hold': [], 'notes': [], 'park': []})['notes'].append(f"{slug}: " + (nx[0][6:] if nx else (s.get('notes') or ['?'])[0]))
        dec.append({'system': slug, 'verdict': 'GLANCE' if s.get('notes') and 'needs a data source' not in s['notes'][0] else 'BUILD',
                    'why': 'lean AutoReview check only, no planner', 'checklist': len(chk)})
        holes.append((2 + len(chk), f"{slug}: nothing checks it" + (f" ({len(chk)} checklist item{'s' * (len(chk) > 1)})" if chk else ''))); continue
    items = [(owners[0], l) for l in s['lines']] + [(c, l) for c, v in s['per_char'].items() for l in v] + [(c, l) for c, v in s['routed'].items() for l in v]
    dos, info, holds = [], 0, []
    for who, l in items:
        r = reserve_hit(l)
        if r: holds.append((who, l, r)); continue
        k = classify(l, slug)
        if k == 'park': by_char.setdefault(who, {'goal': [], 'do': [], 'hold': [], 'notes': [], 'park': []}).setdefault('park', []).append(l[6:])
        elif k == 'do': dos.append((who, l, bool(GOAL.search(l))))
        else: info += 1
    for who, l, g in dos: by_char.setdefault(who, {'goal': [], 'do': [], 'hold': [], 'notes': [], 'park': []})['goal' if g else 'do'].append(f'{slug}: {l}')
    for who, l, r in holds: by_char.setdefault(who, {'goal': [], 'do': [], 'hold': [], 'notes': [], 'park': []})['hold'].append(f'{slug}: {l}  [HOLD: {r}]')
    v = 'DO' if dos else ('HOLD' if holds else 'NOTHING')
    why = '' if dos else ('reserve' if holds else (f'{info} info lines, no action' if info else 'planner returned nothing (needs a reason)'))
    if v == 'NOTHING' and not info: holes.append((1, f'{slug}: planner gives no reason'))
    if not plan_written(slug): holes.append((0.5, f'{slug}: no written plan in brain'))
    dec.append({'system': slug, 'verdict': v, 'why': why, 'do': len(dos), 'info': info, 'hold': len(holds), 'checklist': len(chk)})

for b in by_char.values():   # same line from a planner and the card engine: keep one
    for k in b:
        seen, keep = set(), []
        for x in b[k]:
            key = re.sub(r'^([\w +()]+?: ){1,3}', '', x).lower().rstrip('.')[:70]
            if key not in seen: seen.add(key); keep.append(x)
        b[k] = keep
holes.sort(key=lambda h: -h[0])
json.dump({'save': SAVE, 'systems': dec, 'by_char': by_char, 'holes': [h[1] for h in holes]}, open(OUT / 'decisions.json', 'w'), indent=1)
cnt = {k: sum(d['verdict'] == k for d in dec) for k in ('DO', 'HOLD', 'NOTHING', 'GLANCE', 'BUILD', 'FIX')}
md = [f'# Decisions {SAVE}', '', ' · '.join(f'{k} {v}' for k, v in cnt.items()), '', '## Biggest holes (fix the system, not just today)']
md += [f'- {h[1]}' for h in holes if h[0] >= 1][:25]
md += ['', '## Per character (goal first, then do, then holds). Claude reviews before cards.']
for who, b in by_char.items():
    md.append(f'### {who}')
    md += [f'- GOAL {x}' for x in b['goal']] + [f'- {x}' for x in b['do']] + [f'- {x}' for x in b['hold']] + [f'- NOTE {x}' for x in b['notes']]
md += ['', '## Every system', '| system | verdict | why | do | info | hold | checklist |', '|---|---|---|---|---|---|---|']
md += [f"| {d['system']} | {d['verdict']} | {d.get('why', '')} | {d.get('do', '')} | {d.get('info', '')} | {d.get('hold', '')} | {d.get('checklist') or ''} |" for d in dec]
(OUT / 'decisions.md').write_text('\n'.join(md) + '\n')
print(md[2])
