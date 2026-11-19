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
    s_tiers = o['tiers']
    cheap = sorted([s for s in o['sigils'] if s['state'] != 'Undiscovered' and not s['charging']], key=lambda s: s['hours_1char'])
    L.append(f"TOP: sigils are AutoReview tier {s_tiers.get('Sigils')}, the weakest Alchemy part. Only {', '.join(on_sig) or 'nobody'} charges a sigil (Pea Pod). "
             f"One character charges ~{o['sigil_speed']:.0f} points/hr (measured: Pea Pod +454 in 7.2h). Cheapest next levels for 1 character: " +
             ', '.join(f"{s['name']} {s['hours_1char']}h (-> {s['next_gives']})" for s in cheap[:5]) + '.')
    L.append("Sources: Griffy 2026-01: sigils are not an early priority, finish unlocking bubbles first; sigil XP ballot needs sigils active. "
             "Griffy 2026-02 (sigil options): Loot Pile (more sailing chests = artifact rolls) and mob respawn. Pulse 2026-09 said the 11th character gives no sigil progress; "
             "your save shows Autistachio's Pea Pod gaining ~63/hr, so it works now.")
    lp = next((s for s in o['sigils'] if s['name'] == 'Loot Pile'), None)
    if lp: L.append(f"Loot Pile sigil (Sailing chest capacity): undiscovered, {lp['cur']:,}/{lp['goal']:,} = {lp['hours_1char']:,}h for 1 character ({lp['hours_1char'] / 24:.0f} days). Pea Pod's next level (15,000) adds +100% in sigil speed group 1 (6.78x -> 7.78x, about +15% on every sigil).")
    L.append('Cauldron seats: ' + '; '.join(f"{s}: {', '.join(cs)}" for s, cs in by.items()) + '. GAP: per-cauldron value vs a sigil seat is not modeled yet, so seat moves are your call.')
    L.append(f"Bubbles (tier {s_tiers.get('Bubbles')}): daily auto-levels {o['daily'].get('Kattlekruk levels per day')} (Kattlekruk link) and {o['daily'].get('Grind Time levels per day')} Grind Time (Coral Reef). "
             'Targets: ' + '; '.join(o['bubble_targets'][:8]) + '. GAP: bubble costs are not on the Toolbox page text, so bubble buys are not efficiency-ranked yet.')
    if o['vials_next']: L.append(f"Vials (tier {s_tiers.get('Vials')}), max next without breaking greenstacks: " + '; '.join(o['vials_next'][:6]) +
                                 '. Unlock Turtle Tisane (Tuttle): x1 in Sailing artifact odds, kitchen speed and sigil speed.')
    return L


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)


def routed(o):
    lp = next((s for s in o['sigils'] if s['name'] == 'Loot Pile'), None)
    return {'Autisticles': [f"Alchemy (Cat): Loot Pile sigil adds sailing chest capacity, {lp['cur']:,}/{lp['goal']:,} undiscovered"]} if lp else {}
