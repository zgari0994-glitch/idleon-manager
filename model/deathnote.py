"""Death Note planner. Toolbox Death Note page (kills per mob, multikill per world, eclipse skulls) + AutoReview Death Note groups.
Autistopher: Super CHOWs (next tier). Autiszemo: ZOW/CHOW W7 list + closest Eclipse skulls. ETAs from kill gain between two Toolbox reads."""
import json, re
from pathlib import Path
from compass import _n, _ar

ROOT = Path(__file__).resolve().parent.parent
SNAPS = ROOT / 'snapshots'
SNAP = SNAPS / (SNAPS / 'LATEST').read_text().strip()
ECLIPSE = 1e9


def parse(path):
    d = json.load(open(path)); t = d['tabs']['_page']['text']
    kills = {}
    for wm in re.finditer(r'\n([^\n\t]+)\tKILLS\n(.*?)(?=\n[^\n\t]+\tKILLS|\Z)', t, re.S):
        for mob, k in re.findall(r'\n\n\n([^\n\t]+)\n\t([\d.]+[KMBT]?)\t', wm.group(2)):
            kills[mob] = (wm.group(1), _n(k))
    multi = dict(re.findall(r'\n([^\n]+) multikill\n([\d.]+%)', t))
    ecl = re.search(r'Eclipse skulls\n(\d+)\n([^\n]+)', t)
    return {'at': d.get('at'), 'kills': kills, 'multi': multi, 'eclipse': (int(ecl.group(1)), ecl.group(2)) if ecl else None}


def build():
    cur = parse(SNAP / 'toolbox' / 'deathnote.json')
    prev = None
    for s in sorted([p for p in SNAPS.iterdir() if p.is_dir() and p.name < SNAP.name], reverse=True):
        if (s / 'toolbox' / 'deathnote.json').exists(): prev = parse(s / 'toolbox' / 'deathnote.json'); break
    ar = _ar('Death Note'); groups = []
    for g in (ar or {}).get('groups', []):
        items = [i for tab in g.get('items', []) for i in tab['items']]
        groups.append({'name': g['name'], 'tier': g.get('tier'), 'items': items})
    out = {'snapshot': SNAP.name, 'cur': cur, 'prev_at': prev and prev['at'], 'groups': groups, 'ar_tier': (ar or {}).get('tier')}
    if prev:
        from datetime import datetime
        hrs = (datetime.fromisoformat(cur['at'].replace('Z', '')) - datetime.fromisoformat(prev['at'].replace('Z', ''))).total_seconds() / 3600
        out['rate'] = {m: (k - prev['kills'][m][1]) / hrs for m, (w, k) in cur['kills'].items() if m in prev['kills'] and hrs > 1 and k > prev['kills'][m][1]}
    json.dump(out, open(ROOT / 'model' / 'deathnote.json', 'w'), indent=1)
    return out


def _eta(o, mob, left):
    r = (o.get('rate') or {}).get(mob)
    return f", ETA {left / r / 24:.0f}d at {r:,.0f}/hr" if r else ''


def card_lines(o):
    c = o['cur']; L = []
    ecl = sorted([(m, w, k) for m, (w, k) in c['kills'].items() if 0 < k < ECLIPSE and w != 'Minibosses'], key=lambda x: -x[2])[:4]
    if ecl: L.append('Closest Eclipse skulls (1B): ' + ', '.join(f"{m} ({w}) {(ECLIPSE - k) / 1e6:,.0f}M left{_eta(o, m, ECLIPSE - k)}" for m, w, k in ecl))
    if c['eclipse']: L.append(f"Eclipse skulls {c['eclipse'][0]} ({c['eclipse'][1]}). Multikill: " + ', '.join(f"{k} {v}" for k, v in c['multi'].items()))
    if not o.get('rate'): L.append('Kill-rate ETAs start after the next Toolbox Death Note read (needs two reads).')
    L.append("Griffy: Eclipse skulls are painfully slow without big multikill; the Death Note building upgrade is worth it for multikill. WOWs skipped (weak scaling).")
    return L


def char_lines(o, name):
    L = []
    for g in o['groups']:
        if name not in g['name'] or 'WOW' in g['name']: continue   # WOWs skipped (Griffy: weak scaling)
        todo = [i for i in g['items'] if i.get('cur') not in ('100%',)]
        L.append(f"AutoReview: {g['name']}. Next: " + ', '.join(i['label'] for i in todo[:6]) + ('...' if len(todo) > 6 else ''))
    if name == 'Autistopher' and L: L[0] = 'TOP (Death Note tier ' + str(o['ar_tier']) + ' -> next): ' + L[0]
    return L


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)
    for n in ('Autiszemo', 'Autistopher'):
        print(n, char_lines(o, n))
