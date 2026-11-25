#!/usr/bin/env python3
"""Data check after every pull (Zack 2026-11-25). Fails loudly instead of quietly.
For every system in model/data_map.yaml: present? non-empty? Then save age, cross-checks against AutoReview,
and sanity vs the previous snapshot (levels never go down, nothing drops to zero).
Writes snapshots/<save>/check.md + check.json. Exit 1 if any mapped system is missing or a cross-check fails.
Usage: tools/check_data.py [stamp]
"""
import json, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'model'))
from data import load, DataMissing, MAP, SNAPS  # noqa: E402

stamp = sys.argv[1] if len(sys.argv) > 1 else (SNAPS / 'LATEST').read_text().strip()
D = load(stamp)
rows, fails, warns = [], [], []

# 1. every system: present and non-empty
for name, m in sorted(MAP.items()):
    if m.get('meta'):
        continue
    if not m.get('path'):
        rows.append((name, 'NOT IN PARSER', 'use AutoReview / raw save')); warns.append(f"{name}: not in Toolbox's parser"); continue
    try:
        v = D.system(name)
        size = len(v) if isinstance(v, (list, dict, str)) else 1
        rows.append((name, 'OK', f"{size} entries"))
    except DataMissing as e:
        rows.append((name, 'MISSING', str(e))); fails.append(f"{name}: {e}")

# 2. save age
age = D.age_hours
if age is None:
    fails.append('save time unknown')
elif age > 24:
    warns.append(f"save is {age:.0f}h old: ask Zack to cloud save")

# 3. cross-check against AutoReview's own read of the same save
try:
    ar = json.load(open(SNAPS / stamp / 'chars.json'))['characters']
    for a in ar:
        c = D.char(a['character_name'])
        if int(c.get('level') or 0) != int(a['combat_level']):
            fails.append(f"{a['character_name']}: Toolbox level {c.get('level')} vs AutoReview {a['combat_level']}")
except (FileNotFoundError, DataMissing) as e:
    warns.append(f"AutoReview cross-check skipped: {e}")

# 4. sanity vs the previous snapshot that has a Toolbox parse
prev = sorted(p.name for p in SNAPS.iterdir() if p.is_dir() and p.name < stamp and (p / 'tb_parsed.json.gz').exists())
if prev:
    P = load(prev[-1])
    for c in D.characters:
        try:
            pc = P.char(c['name'])
        except DataMissing:
            continue
        if (c.get('level') or 0) < (pc.get('level') or 0):
            fails.append(f"{c['name']}: level went down {pc.get('level')} -> {c.get('level')}")
        for sk, lv in (c.get('skillsInfo') or {}).items():
            plv = ((pc.get('skillsInfo') or {}).get(sk) or {}).get('level')
            if isinstance(lv, dict) and plv and (lv.get('level') or 0) < plv:
                fails.append(f"{c['name']}: {sk} went down {plv} -> {lv.get('level')}")
    for name, m in MAP.items():
        if m.get('meta') or not m.get('path'):
            continue
        try:
            P.system(name); had = True
        except DataMissing:
            had = False
        if had and any(r[0] == name and r[1] == 'MISSING' for r in rows):
            fails.append(f"{name}: was there in {prev[-1]}, gone now")
else:
    warns.append('no earlier snapshot with a Toolbox parse to compare against')

ok = sum(1 for r in rows if r[1] == 'OK')
md = [f"# Data check {stamp}", f"Save age: {age:.1f}h" if age is not None else 'Save age: unknown',
      f"Toolbox source: {D.raw.get('_meta', {}).get('toolbox_commit', '')[:10]}  |  compared with: {prev[-1] if prev else 'none'}",
      f"Systems: {ok} OK, {sum(1 for r in rows if r[1] == 'MISSING')} missing, {sum(1 for r in rows if r[1] == 'NOT IN PARSER')} not in parser", '']
md += ['## FAILS'] + [f"- {f}" for f in fails] + [''] if fails else ['## FAILS', '- none', '']
md += ['## Warnings'] + [f"- {w}" for w in warns] + ['', '## Systems', '| system | status | detail |', '|---|---|---|']
md += [f"| {a} | {b} | {c} |" for a, b, c in rows]
(SNAPS / stamp / 'check.md').write_text('\n'.join(md) + '\n')
json.dump({'stamp': stamp, 'age_h': age, 'fails': fails, 'warns': warns, 'rows': rows}, open(SNAPS / stamp / 'check.json', 'w'), indent=1)
print(f"data check {stamp}: {ok} OK, {len(fails)} fails, {len(warns)} warnings" + (''.join(f"\n  FAIL {f}" for f in fails[:12])))
sys.exit(1 if fails else 0)
