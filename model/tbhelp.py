"""Shared helpers for Toolbox-page planners."""
import json, re, gzip
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / 'snapshots' / (ROOT / 'snapshots' / 'LATEST').read_text().strip()
_R = None


def n(s):
    s = str(s).strip()
    m = re.match(r'([\d.,]+)(e[+-]?\d+)?\s*(QQ|Q|T|B|M|K)?', s)
    if not m: return None
    return float(m.group(1).replace(',', '') + (m.group(2) or '')) * {None: 1, 'K': 1e3, 'M': 1e6, 'B': 1e9, 'T': 1e12, 'Q': 1e15, 'QQ': 1e18}[m.group(3)]


def tb(name):
    # Zack 2026-11-25: retired. Old website page reads were stale; planners read model/data.py (Toolbox's parser on the save).
    raise RuntimeError(f"tb('{name}') is retired: read it through model/data.py")


def ar(name):
    global _R
    if _R is None: _R = json.load(gzip.open(SNAP / 'review.json.gz'))
    def walk(o):
        if isinstance(o, dict):
            if o.get('name') == name and 'groups' in o: yield o
            for v in o.values(): yield from walk(v)
        elif isinstance(o, list):
            for v in o: yield from walk(v)
    return next(walk(_R), None)


def ar_items(name):
    d = ar(name) or {}
    return d.get('tier'), [{'group': g['name'], 'tab': t.get('tab', ''), **i} for g in d.get('groups', []) for t in g.get('items', []) for i in t['items']]


def save(name, o):
    o['snapshot'] = SNAP.name
    json.dump(o, open(ROOT / 'model' / f'{name}.json', 'w'), indent=1)
    return o
