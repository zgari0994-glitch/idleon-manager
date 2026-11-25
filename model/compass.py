"""Compass planner (Autistacular, Wind Walker). Toolbox Compass page: upgrades + costs, optimizer, abominations, portals.
AutoReview Compass targets first, then cheap buys (<1% of a dust balance), portals, abomination target, print-day line."""
import json, re, gzip
from pathlib import Path
from spend import h

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / 'snapshots' / (ROOT / 'snapshots' / 'LATEST').read_text().strip()
OWNER = 'Autistacular'
DUST = ['Stardust', 'Moondust', 'Solardust', 'Cooldust', 'Novadust']


def _n(s):
    m = re.match(r'([\d.,]+)\s*([KMBTQ]?)', s.strip())
    return float(m.group(1).replace(',', '')) * {'': 1, 'K': 1e3, 'M': 1e6, 'B': 1e9, 'T': 1e12, 'Q': 1e15}[m.group(2)] if m else None


def _ar(name):
    r = json.load(gzip.open(SNAP / 'review.json.gz'))
    def walk(o):
        if isinstance(o, dict):
            if o.get('name') == name and 'groups' in o: yield o
            for v in o.values(): yield from walk(v)
        elif isinstance(o, list):
            for v in o: yield from walk(v)
    return next(walk(r), None)


def from_parsed(rows, cur_names, bal, cur_key, max_key='x4'):
    # Zack 2026-11-25: same shape as upgrades(), from Toolbox's parser
    out = []
    for u in rows:
        ci = u.get(cur_key); cur = cur_names[int(ci)] if isinstance(ci, (int, float)) and int(ci) < len(cur_names) else None
        mx = u.get(max_key); lv = u.get('level', 0)
        out.append({'name': u['name'].replace('_', ' '), 'lv': lv, 'max': int(mx) if isinstance(mx, (int, float)) and mx < 999999 else None,
                    'maxed': isinstance(mx, (int, float)) and lv >= mx, 'next': None, 'cost': u.get('cost'), 'currency': cur,
                    'desc': str(u.get('description', '')).replace('_', ' ')[:140], 'unlocked': u.get('unlocked', True)})
    return out


def upgrades(text, cur_names, bal):
    out = []
    for m in re.finditer(r'\n([A-Z][^\n]{2,40})\nLv (\d+)(?: / (\d+))?\n(.*?)(?=\n[A-Z][^\n]{2,40}\nLv \d|\nDiscord|\Z)', text, re.S):
        name, lv, mx, body = m.group(1), int(m.group(2)), m.group(3), m.group(4)
        nx = re.search(r'Next level\n([^\n]+)\n([\d.,]+[KMBTQ]?)\n/\n([\d.,]+[KMBTQ]?)', body)
        held = _n(nx.group(2)) if nx else None
        cur = next((c for c in cur_names if bal.get(c) and held and abs(bal[c] - held) / bal[c] < 0.02), None)
        desc = next((l for l in body.split('\n') if l.strip() and l.strip() not in ('Maxed', 'Next level')), '')
        out.append({'name': name, 'lv': lv, 'max': int(mx) if mx else None, 'maxed': 'Maxed' in body[:80], 'next': nx.group(1) if nx else None,
                    'cost': _n(nx.group(3)) if nx else None, 'currency': cur, 'desc': desc[:140]})
    return out


def build():
    from data import load
    C = load().system('compass')
    bal = {d['name']: d['value'] for d in C['dusts']}
    names = [d['name'] for d in C['dusts']]
    ups = from_parsed(C['upgrades'], names, bal, 'x3')
    by = {u['name']: u for u in ups}
    ar = _ar('Compass'); targets = []
    for g in (ar or {}).get('groups', []):
        for tab in g.get('items', []):
            if not tab.get('tab', '').startswith('To reach Tier'): continue
            for it in tab['items']:
                nm = it['label'].split(': ', 1)[-1]
                targets.append({'tab': tab['tab'], 'name': nm, 'cur': it['cur'], 'goal': it['goal'], 'up': by.get(nm)})
    ab = C['abominations']; k = int(C.get('totalKilledAbominations') or 0)
    nxt = ab[k] if k < len(ab) else None
    out = {'snapshot': SNAP.name, 'balance': bal, 'total_levels': C['totalUpgradeLevels'], 'extra_dust': None,
           'upgrades': ups, 'targets': targets, 'optimizer': [], 'portals': [], 'abom_killed': k,
           'abom_next': (nxt['name'].replace('_', ' '), f"World {nxt['world']} · {nxt['map'].replace('_', ' ')}", f"{nxt['hp']}") if nxt else None,
           'gate': None, 'ar_tier': (ar or {}).get('tier'), 'medallions': C.get('totalAcquiredMedallions')}
    json.dump(out, open(ROOT / 'model' / 'compass.json', 'w'), indent=1)
    return out


def card_lines(o):
    L, bal = [], o['balance']
    star = [p for p in o['portals'] if p['afford'] and p['currency'] == 'Stardust']
    if star: L.append(f"TOP: open {len(star)} cheap portals in W1 and W2 (hold them for 2 seconds). They cost {h(sum(p['cost'] for p in star))} stardust total and you have {h(bal['Stardust'])}. Check in game that Autistacular can open them.")
    moon = sorted([p for p in o['portals'] if p['afford'] and p['currency'] == 'Moondust'], key=lambda p: p['cost']); run, pick = 0, []
    for p in moon:
        if run + p['cost'] <= bal.get('Moondust', 0) * 0.6: run += p['cost']; pick.append(p['map'])
    if pick: L.append(f"Then open {', '.join(pick)} with moondust ({h(run)} of your {h(bal['Moondust'])}, keeps some for upgrades).")
    nxt = [t for t in o['targets'] if t['tab'] == (o['targets'][0]['tab'] if o['targets'] else '')]
    if nxt: L.append('Next Compass tier needs: ' + ', '.join(f"{t['name']} {t['cur']} -> {t['goal']}" for t in nxt) + '.')
    ep = next((t['up'] for t in nxt if t['name'] == 'Elemental Path' and t['up']), None)
    if ep and ep.get('cost'): L.append(f"Elemental Path's next level costs {h(ep['cost'])} stardust, you're {h(max(0, ep['cost'] - bal.get('Stardust', 0)))} short.")
    cheapu = [u for u in o['upgrades'] if u['cost'] and u['currency'] and not u['maxed'] and u['cost'] <= 0.01 * bal[u['currency']]]
    if cheapu: L.append(f"{len(cheapu)} upgrades cost almost nothing right now, just buy them: " + ', '.join(u['name'] for u in sorted(cheapu, key=lambda u: u['cost'])[:6]) + '.')
    ex = next((u for u in o['upgrades'] if u['name'] == 'Exalted Stamps'), None)
    if ex and ex['cost']: L.append(f"Your call: Exalted Stamps ({h(ex['cost'])} stardust) gives one more stamp exalt, but it delays Elemental Path by the same amount. Griffy uses moons for an extra exalt.")
    if o['abom_next']: L.append(f"Kill {o['abom_next'][0]} next ({o['abom_next'][1].split(' · ')[-1]}). It's abomination #{o['abom_killed'] + 1} and it lets Tempest Form into the W3 town.")
    pl = print_line(o)
    if pl: L.append(pl)
    L.append('Griffy: farm every medallion and kill every abomination.')
    return L


def print_line(o=None):
    o = o or json.load(open(ROOT / 'model' / 'compass.json'))
    mp = next((u for u in o['upgrades'] if u['name'] == 'Moon of Print'), None)
    if not mp: return None
    return f"Print day: Moon of Print is {mp['lv']} of {mp['max']}, next level {h(mp['cost'])} stardust."


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)
    print(print_line(o))
