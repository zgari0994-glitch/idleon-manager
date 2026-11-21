"""The Report: every system, every pull, nothing trimmed. Stored per save in reports/<save>/.
Runs every planner (build + card_lines + char_lines + routed), attaches AutoReview tiers for the system,
and lists systems nothing checks. The decision layer (decide.py) reads this, never the raw planners.
Run from the AutoReview folder: PYTHONPATH=.:<repo>/model python3 <repo>/model/report.py
"""
import gzip, importlib, json, sys, traceback, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SAVE = (ROOT / 'snapshots' / 'LATEST').read_text().strip()
SNAP = ROOT / 'snapshots' / SAVE
OUT = ROOT / 'reports' / SAVE; (OUT / 'systems').mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT / 'tools')); sys.path.insert(0, str(ROOT / 'model'))
from build_brain import PLANNER, EXTRA, NOT_SYSTEM   # one source of truth for planner -> systems
import yaml

idx = yaml.safe_load(open(ROOT / 'model' / 'system_index.yaml'))
chars = [c['character_name'] for c in json.load(open(SNAP / 'chars.json'))['characters']]
meta = json.load(open(SNAP / 'meta.json'))

# AutoReview: section name -> tier info (whatever run_ar stored), searched by name
review = json.load(gzip.open(SNAP / 'review.json.gz'))
def ar_sections(names):
    found = []
    def walk(x):
        if isinstance(x, dict):
            n = x.get('name') or x.get('section') or x.get('title')
            if n and any(a.lower() == str(n).lower() for a in names):
                found.append({k: x[k] for k in x if k in ('name', 'section', 'title', 'tier', 'max_tier', 'pinchy', 'header', 'groups', 'advice')})
            for v in x.values(): walk(v)
        elif isinstance(x, list):
            for v in x: walk(v)
    walk(review.get('worlds', review)); return found

def safe(o):
    try: json.dumps(o); return o
    except Exception: return json.loads(json.dumps(o, default=str))

results = {}
for mod in PLANNER:
    r = {'module': mod, 'systems': PLANNER[mod], 'ok': False}
    try:
        m = importlib.import_module(mod)
        o = m.build() if hasattr(m, 'build') else None
        r['card_lines'] = list(m.card_lines(o)) if hasattr(m, 'card_lines') else []
        r['char_lines'] = {c: list(m.char_lines(o, c)) for c in chars} if hasattr(m, 'char_lines') else {}
        r['char_lines'] = {c: v for c, v in r['char_lines'].items() if v}
        r['routed'] = m.routed(o) if hasattr(m, 'routed') else {}
        r['build'] = safe(o); r['ok'] = True
    except Exception as e:
        r['error'] = f'{type(e).__name__}: {e}'; r['trace'] = traceback.format_exc()[-1500:]
    json.dump(safe(r), open(OUT / 'systems' / f'{mod}.json', 'w'), indent=1, default=str)
    results[mod] = r

# one row per system (brain index order), with everything the decision layer needs
rows = []
for slug in [s for s in list(idx) + list(EXTRA) if s not in NOT_SYSTEM]:
    e = idx.get(slug, {})
    mods = [m for m, s in PLANNER.items() if slug in s]
    lines, per_char, routed, errs = [], {}, {}, []
    for m in mods:
        r = results[m]
        if not r['ok']: errs.append(f"{m}: {r['error']}"); continue
        lines += r['card_lines']
        for c, v in r['char_lines'].items(): per_char.setdefault(c, []).extend(v)
        for c, v in (r['routed'] or {}).items(): routed.setdefault(c, []).extend(v)
    rows.append({'system': slug, 'owners': e.get('owners') or [], 'planners': mods, 'errors': errs,
                 'autoreview': ar_sections(e.get('autoreview') or []), 'lines': lines, 'per_char': per_char, 'routed': routed,
                 'checked': bool(mods) and not errs})
json.dump(safe({'save': SAVE, 'meta': meta, 'systems': rows}), open(OUT / 'report.json', 'w'), indent=1, default=str)

md = [f"# Report {SAVE} (game save {meta.get('game_save_utc', '?')})", '',
      f"{len(rows)} systems · {sum(r['checked'] for r in rows)} checked · {sum(not r['planners'] for r in rows)} with nothing checking · "
      f"{sum(bool(r['errors']) for r in rows)} planner errors", '']
for r in rows:
    tiers = '; '.join(f"{a.get('name') or a.get('section')}: {a.get('tier', '?')}/{a.get('max_tier', '?')}" for a in r['autoreview']) or 'not rated'
    md.append(f"## {r['system']}  ({', '.join(r['owners']) or 'UNOWNED'})  AR {tiers}")
    if not r['planners']: md.append('- NOTHING CHECKS THIS'); continue
    for x in r['errors']: md.append(f'- PLANNER ERROR {x}')
    for x in r['lines']: md.append(f'- {x}')
    for c, v in r['per_char'].items():
        for x in v: md.append(f'- [{c}] {x}')
    for c, v in r['routed'].items():
        for x in v: md.append(f'- [routed to {c}] {x}')
    md.append('')
(OUT / 'report.md').write_text('\n'.join(md))
print(md[2]); print('wrote', OUT.relative_to(ROOT))
