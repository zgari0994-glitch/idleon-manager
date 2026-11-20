"""Alchemy planner: cauldron seats, sigil charge plan (hours per target at the measured rate), vial max/unlock order, bubble targets
-> Autistocat's Alchemy block.

Inputs: chars.json (alchemy_job_string), toolbox/alchemy.json (sigils page), toolbox/bubbles.json (daily levels), review.json.gz.
Sigil rate per character measured from snapshots: Pea Pod 1178 -> 1632 in 7.2h = ~63/hr = Toolbox 'Sigil speed' x 1/hr.
"""
import gzip, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / 'snapshots' / (ROOT / 'snapshots' / 'LATEST').read_text().strip()


def _ar(sec):
    r = json.load(gzip.open(SNAP / 'review.json.gz'))
    for w in r['worlds']:
        for s in (w.get('sections') or []):
            if s.get('name') == sec: return s
    return None


def _items(s):
    out = []
    def walk(x, grp=''):
        if isinstance(x, dict):
            if 'label' in x and 'cur' in x and not x.get('completed'): out.append((grp, x))
            g = x.get('name') or grp
            for k in ('groups', 'items'):
                if k in x: walk(x[k], g)
        elif isinstance(x, list):
            for y in x: walk(y, grp)
    walk(s or {})
    return out


def build():
    ch = json.load(open(SNAP / 'chars.json'))['characters']
    seats = {c['character_name']: c.get('alchemy_job_string') for c in ch}
    T = json.load(open(SNAP / 'toolbox' / 'alchemy.json'))['tabs']['sigils:_page']['text'].replace('\xa0', ' ') + '\n'
    speed = float(re.search(r'Sigil speed\n([\d.]+)x', T).group(1))
    sig = []
    for m in re.finditer(r'\n([A-Z][A-Za-z ]+)\n(Unlocked|Boosted|Undiscovered|Jade|Eclectic|Ethereal)\n(?:●\nCharging\n)?\n(.+?)\nProgress\n([\d,]+) / ([\d,]+)', T, re.S):
        name, state = m.group(1).strip(), m.group(2)
        cur, goal = int(m.group(4).replace(',', '')), int(m.group(5).replace(',', ''))
        gives = re.search(r'gives\n([^\n]+)', m.group(3))
        sig.append({'name': name, 'state': state, 'cur': cur, 'goal': goal, 'hours_1char': round((goal - cur) / speed, 1),
                    'charging': 'Charging' in m.group(0), 'desc': m.group(3).split('\n')[0][:80], 'next_gives': gives and gives.group(1)})
    bt = ''
    try: bt = json.load(open(SNAP / 'toolbox' / 'bubbles.json'))['tabs']['_page']['text']
    except Exception: pass
    daily = {k: (re.search(k + r'\n([^\n]+)', bt) or [0, None])[1] for k in ('Kattlekruk levels per day', 'Grind Time levels per day', 'Particle upgrades', 'Upgraded daily')}
    nmlb = re.search(r'No Bubble Left Behind\n([^\n]+)\n([^\n]+)', bt)
    ar_tiers = {s: (_ar(s) or {}).get('tier') for s in ('Bubbles', 'Vials', 'Sigils', 'Pay2Win')}
    vials = [x['label'] for g, x in _items(_ar('Vials')) if g.startswith('Vials to max next')]
    bub = [(g, x) for g, x in _items(_ar('Bubbles')) if 'sample-boosting' in g or 'Tier' in g]
    out = {'snapshot': SNAP.name, 'seats': seats, 'sigil_speed': speed, 'sigils': sig, 'daily': daily, 'nmlb': nmlb and nmlb.groups(),
           'tiers': ar_tiers, 'vials_next': vials, 'bubble_targets': [f"{x['label']} {x['cur']} -> {x['goal']}" for g, x in bub][:14],
           'sigil_tier2': [f"{x['label']} {x['cur']} -> {x['goal']}" for g, x in _items(_ar('Sigils')) if 'Tier 2' in g or 'Tier 3' in g][:10]}
    json.dump(out, open(ROOT / 'model' / 'alchemy.json', 'w'), indent=1)
    return out


def card_lines(o):
    L = []
    by = {}
    for c, s in o['seats'].items(): by.setdefault(s, []).append(c)
    on_sig = [c for c, s in o['seats'].items() if s and s not in ('Orange', 'Green', 'Purple', 'Yellow', 'Liquid Nitrogen', 'Water', 'Dense Water', 'Toxic Mercury', 'Liquid', None)]
    cheap = sorted([s for s in o['sigils'] if s['state'] != 'Undiscovered' and not s['charging']], key=lambda s: s['hours_1char'])
    L.append(f"Sigils are the weakest part of Alchemy (tier {o['tiers'].get('Sigils')}). Only {', '.join(on_sig) or 'nobody'} is charging one." + (f" Quickest next levels: {', '.join(s['name'] for s in cheap[:3])}." if cheap else ''))
    lp = next((s for s in o['sigils'] if s['name'] == 'Loot Pile'), None)
    if lp: L.append(f"The Loot Pile sigil (more sailing chests) would take one character about {lp['hours_1char'] / 24:.0f} days. Griffy rates it as a good pick.")
    L.append("Seats follow the biggest need: move someone onto sigils only while something is waiting on them, and never empty the cauldrons. Griffy: finish unlocking bubbles before worrying about sigils.")
    if o['bubble_targets']: L.append('Bubble goals: ' + '; '.join(o['bubble_targets'][:4]) + '.')
    if o['vials_next']: L.append('Vials you can level without breaking greenstacks: ' + '; '.join(v.split(' (')[0] for v in o['vials_next'][:4]) + '.')
    return L


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)


def routed(o):
    lp = next((s for s in o['sigils'] if s['name'] == 'Loot Pile'), None)
    return {'Autisticles': [f"Alchemy (Cat): Loot Pile sigil adds sailing chest capacity, {lp['cur']:,}/{lp['goal']:,} undiscovered"]} if lp else {}
