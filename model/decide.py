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
    if not SPEND.search(line): return None
    for res, holds in reserves.items():
        stem = res.rstrip('s')
        if re.search(rf'\b{stem}s?\b', line, re.I):
            h = holds[0]; return f"{res} held for {h['for']} ({h['why']})"
    return None

def classify(line):
    if INFO.match(line) or not ACT.match(line.split(': ', 1)[-1] if ':' in line[:40] else line): return 'info'
    return 'do'

dec, by_char, holes = [], {}, []
for s in rep['systems']:
    slug, owners = s['system'], s['owners'] or ['account']
    chk = [c for c in check if f'[[{slug}]]' in c]
    if s['errors']:
        dec.append({'system': slug, 'verdict': 'FIX', 'why': '; '.join(s['errors'])}); holes.append((3, f'{slug}: planner broken')); continue
    if not s['planners']:
        dec.append({'system': slug, 'verdict': 'BUILD', 'why': 'nothing checks this', 'checklist': len(chk)})
        holes.append((2 + len(chk), f"{slug}: nothing checks it" + (f" ({len(chk)} checklist item{'s' * (len(chk) > 1)})" if chk else ''))); continue
    items = [(owners[0], l) for l in s['lines']] + [(c, l) for c, v in s['per_char'].items() for l in v] + [(c, l) for c, v in s['routed'].items() for l in v]
    dos, info, holds = [], 0, []
    for who, l in items:
        r = reserve_hit(l)
        if r: holds.append((who, l, r)); continue
        if classify(l) == 'do': dos.append((who, l, bool(GOAL.search(l))))
        else: info += 1
    for who, l, g in dos: by_char.setdefault(who, {'goal': [], 'do': [], 'hold': []})['goal' if g else 'do'].append(f'{slug}: {l}')
    for who, l, r in holds: by_char.setdefault(who, {'goal': [], 'do': [], 'hold': []})['hold'].append(f'{slug}: {l}  [HOLD: {r}]')
    v = 'DO' if dos else ('HOLD' if holds else 'NOTHING')
    why = '' if dos else ('reserve' if holds else (f'{info} info lines, no action' if info else 'planner returned nothing (needs a reason)'))
    if v == 'NOTHING' and not info: holes.append((1, f'{slug}: planner gives no reason'))
    if not plan_written(slug): holes.append((0.5, f'{slug}: no written plan in brain'))
    dec.append({'system': slug, 'verdict': v, 'why': why, 'do': len(dos), 'info': info, 'hold': len(holds), 'checklist': len(chk)})

holes.sort(key=lambda h: -h[0])
json.dump({'save': SAVE, 'systems': dec, 'by_char': by_char, 'holes': [h[1] for h in holes]}, open(OUT / 'decisions.json', 'w'), indent=1)
cnt = {k: sum(d['verdict'] == k for d in dec) for k in ('DO', 'HOLD', 'NOTHING', 'BUILD', 'FIX')}
md = [f'# Decisions {SAVE}', '', ' · '.join(f'{k} {v}' for k, v in cnt.items()), '', '## Biggest holes (fix the system, not just today)']
md += [f'- {h[1]}' for h in holes if h[0] >= 1][:25]
md += ['', '## Per character (goal first, then do, then holds). Claude reviews before cards.']
for who, b in by_char.items():
    md.append(f'### {who}')
    md += [f'- GOAL {x}' for x in b['goal']] + [f'- {x}' for x in b['do']] + [f'- {x}' for x in b['hold']]
md += ['', '## Every system', '| system | verdict | why | do | info | hold | checklist |', '|---|---|---|---|---|---|---|']
md += [f"| {d['system']} | {d['verdict']} | {d.get('why', '')} | {d.get('do', '')} | {d.get('info', '')} | {d.get('hold', '')} | {d.get('checklist') or ''} |" for d in dec]
(OUT / 'decisions.md').write_text('\n'.join(md) + '\n')
print(md[2])
