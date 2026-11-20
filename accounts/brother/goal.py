"""Brother's account goal (Zack 2026-11-20: same standards as Zack; the rinse guides progress until the goal is met).
Copied into the throwaway build as model/bro_goal.py; cards2.goal_card is replaced by goal_card() below.

Rule:
- The goal = the AutoReview group (section + group) holding the top rinse score, all its open items brought to target.
- It is kept (state/goal.json) until every item in that group reaches its target, then the next top rinse group is set.
- Levers = the group's open items, best rinse score first, routed to the owner of that section in jobs.yaml.
"""
import json, os, datetime as dt
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent          # the build copy root
STATE = Path(os.environ['BRO_STATE']) / 'goal.json'    # accounts/brother/state/goal.json (persists between runs)

def _owners():
    Y = yaml.safe_load(open(ROOT / 'model' / 'jobs.yaml'))
    own = {}
    for name, c in Y['characters'].items():
        for j in c.get('jobs', []):
            for s in j.get('sections', []):
                own.setdefault(s if isinstance(s, str) else s.get('s'), name)
    for e in Y.get('every_character', []):
        for s in e.get('sections', []):
            own.setdefault(s if isinstance(s, str) else s.get('s'), 'every character')
    for e in Y.get('account_wide', []):
        for s in e.get('sections', []):
            own.setdefault(s if isinstance(s, str) else s.get('s'), 'anyone')
    return own

def _short(x):
    try:
        n = float(str(x).replace(',', ''))
    except ValueError:
        return str(x)
    for v, s in ((1e12, 'T'), (1e9, 'B'), (1e6, 'M'), (1e3, 'K')):
        if n >= v: return f"{n / v:.3g}{s}"
    return f"{n:g}"

def goal_card():
    rows = json.load(open(ROOT / 'rinse' / 'latest.json'))['rows']
    rows = [r for r in rows if not str(r.get('section', '')).startswith('Pinchy')]   # Pinchy = reference only
    rows.sort(key=lambda r: -r['score'])
    own = _owners()
    cur = json.load(open(STATE)) if STATE.exists() else None
    open_in = lambda g: [r for r in rows if r['section'] == g['section'] and r.get('group') == g['group']]
    if cur and not open_in(cur):
        cur['done_on'] = dt.date.today().isoformat()
        hist = STATE.with_name('goal_history.json')
        h = json.load(open(hist)) if hist.exists() else []
        h.append(cur); json.dump(h, open(hist, 'w'), indent=1)
        cur = None
    if not cur and rows:
        top = rows[0]
        cur = {'section': top['section'], 'group': top.get('group', ''), 'set_on': dt.date.today().isoformat(),
               'start_open': len(open_in({'section': top['section'], 'group': top.get('group', '')}))}
        json.dump(cur, open(STATE, 'w'), indent=1)
    if not cur:
        return {'name': 'No open AutoReview items', 'why': '', 'now': None, 'target': None, 'prereqs': [], 'levers': [], 'unknown': []}
    left = open_in(cur)
    who = own.get(cur['section'], 'needs an owner')
    total = max(cur.get('start_open', len(left)), len(left))
    levers = [{'who': who, 'do': f"{r['label']}: {_short(r['cur'])} -> {_short(r['goal'])}", 'size': ''} for r in left[:8]]
    if len(left) > 8:
        levers.append({'who': who, 'do': f"...and {len(left) - 8} more in this group", 'size': ''})
    return {'name': f"{cur['section']}: {cur['group']}".strip(': ')[:90],
            'why': f"Top of the rinse (Griffy-weighted AutoReview) since {cur['set_on']}. Owner: {who}. "
                   f"{total - len(left)} of {total} done; the next goal is picked when this group is finished.",
            'now': None, 'target': None, 'prereqs': [], 'levers': levers,
            'unknown': ['Toolbox page reads (not available for this account)']}
