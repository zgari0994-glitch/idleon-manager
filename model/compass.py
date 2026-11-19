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
    T = json.load(open(SNAP / 'toolbox' / 'compass.json'))['tabs']
    up = T['Upgrades']['text']
    bal = {d: _n(v) for d, v in re.findall(r'\n(' + '|'.join(DUST) + r')\n([\d.,]+[KMBTQ]?)(?=\n)', up)}
    ups = upgrades(up[up.find('Filters'):], DUST, bal)
    by = {u['name']: u for u in ups}
    # AutoReview targets (next tier only, plus the rest listed)
    ar = _ar('Compass'); targets = []
    for g in (ar or {}).get('groups', []):
        for tab in g.get('items', []):
            if not tab.get('tab', '').startswith('To reach Tier'): continue
            for it in tab['items']:
                nm = it['label'].split(': ', 1)[-1]
                targets.append({'tab': tab['tab'], 'name': nm, 'cur': it['cur'], 'goal': it['goal'], 'up': by.get(nm)})
    # optimizer
    opt = T['Upgrade Optimizer']['text']; i = opt.find('Recommended upgrade sequence')
    optl = [f"{a} {b} -> {c}: {d} for {e}" for a, b, c, d, e in re.findall(r'\n([A-Z][^\n]+)\nLv (\d+) → (\d+)\n(?:x\d+\n)?Damage\n([^\n]+)\n(?:Total cost|Cost)\n([^\n]+)', opt[i:])]
    # portals
    P = T['Portals']['text']; portals = []
    for b in re.split(r'\n(?=[A-Z][^\n]*\n(?:All unlocked\n)?\nPortal 1)', P[P.find('Filters'):]):
        name = b.split('\n')[0]
        for num, held, cost in re.findall(r'Portal (\d)\n\n([\d.,]+[KMBTQ]?)\n/\n([\d.,]+[KMBTQ]?)', b):
            hv = _n(held); cur = next((c for c in DUST if bal.get(c) and hv and abs(bal[c] - hv) / bal[c] < 0.02), 'Cooldust' if hv == 0 else '?')
            portals.append({'map': name, 'portal': int(num), 'cost': _n(cost), 'currency': cur, 'afford': hv >= _n(cost)})
    A = T['Abominations']['text']
    gate = re.search(r'(Tempest Form enters [^\n]+)', A)
    abom = [(n, w, hp) for n, w, hp in re.findall(r'\n([A-Z][^\n]+)\n(World \d+ · [^\n]+)\nWeakness\n[^\n]+\nHP\n([^\n]+)', A)]
    killed = len(re.findall(r'\nKilled\n', A))
    top = re.search(r'Total levels\n([\d,]+)\nExtra dust\n([^\n]+)', up)
    out = {'snapshot': SNAP.name, 'balance': bal, 'total_levels': top.group(1) if top else None, 'extra_dust': top.group(2) if top else None,
           'upgrades': ups, 'targets': targets, 'optimizer': optl, 'portals': portals, 'abom_killed': killed, 'abom_next': abom[0] if abom else None,
           'gate': gate.group(1) if gate else None, 'ar_tier': (ar or {}).get('tier')}
    json.dump(out, open(ROOT / 'model' / 'compass.json', 'w'), indent=1)
    return out


def card_lines(o):
    L, bal = [], o['balance']
    cheap = sorted([p for p in o['portals'] if p['afford']], key=lambda p: (p['currency'] != 'Stardust', p['cost']))
    star = [p for p in cheap if p['currency'] == 'Stardust']
    if star: L.append("TOP: open these portals (hold 2s), stardust: " + ', '.join(f"{p['map']} P{p['portal']} {h(p['cost'])}" for p in star)
                      + f" = {h(sum(p['cost'] for p in star))} of {h(bal['Stardust'])}. Check the portal character lock in game.")
    moon = [p for p in cheap if p['currency'] == 'Moondust']; run, pick = 0, []
    for p in moon:
        if run + p['cost'] <= bal.get('Moondust', 0) * 0.6: run += p['cost']; pick.append(p)
    if pick: L.append("Moondust portals (keeps 40% for upgrades): " + ', '.join(f"{p['map']} {h(p['cost'])}" for p in pick) + f" = {h(run)} of {h(bal['Moondust'])}.")
    nxt = [t for t in o['targets'] if t['tab'] == (o['targets'][0]['tab'] if o['targets'] else '')]
    for t in nxt:
        u = t['up'] or {}
        aff = u.get('cost') and u.get('currency') and u['cost'] <= bal.get(u['currency'], 0)
        cost = '' if not u.get('cost') else f" Next level {h(u['cost'])} {u.get('currency') or ''}" + (", buy now." if aff else f", short {h(u['cost'] - bal.get(u['currency'], 0))}." if u.get('currency') else '.')
        L.append(f"AutoReview {t['tab']} (now {o['ar_tier']}): {t['name']} {t['cur']} -> {t['goal']}.{cost}")
    later = {t['name'] for t in o['targets']} - {t['name'] for t in nxt}
    if later: L.append('Later AutoReview tiers also want: ' + ', '.join(sorted(later)))
    if o['optimizer']: L.append('Toolbox optimizer (damage): ' + '; '.join(o['optimizer'][:2]))
    cheapu = [u for u in o['upgrades'] if u['cost'] and u['currency'] and not u['maxed'] and u['cost'] <= 0.01 * bal[u['currency']]]
    if cheapu: L.append('Under 1% of balance (just buy): ' + ', '.join(f"{u['name']} {u['lv']}->{u['lv'] + 1} {h(u['cost'])} {u['currency'][:4]}" for u in sorted(cheapu, key=lambda u: u['cost'])[:8]))
    ex = next((u for u in o['upgrades'] if u['name'] == 'Exalted Stamps'), None)
    if ex and ex['cost']: L.append(f"Exalted Stamps Lv {ex['lv']} -> {ex['lv'] + 1}: {h(ex['cost'])} {ex['currency']} ({'affordable' if ex['cost'] <= bal.get(ex['currency'], 0) else 'short'}). One more exalt use (stamps planner exalt order). Griffy 2026-11: use moons for another Exalted Stamp. "
                                      f"Shares stardust with Elemental Path (tier 4): buying it pushes that back by {h(ex['cost'])}. Need outweighs math: pick by which is the bigger need (Zack).")
    pl = print_line(o)
    if pl: L.append('Print day: ' + pl + ' (one of the 6 print buffs; printer planner tracks its day counter).')
    if o['abom_next']: L.append(f"Abominations {o['abom_killed']} killed. Next: {o['abom_next'][0]} ({o['abom_next'][1]}, HP {o['abom_next'][2]}). {o['gate'] or ''}")
    L.append("Griffy 2026-10: farm all medallions (Tempest damage + accuracy per medallion), kill every abomination for class XP. Toolbox should show Total levels up from " + str(o['total_levels']) + " after buys.")
    return L


def print_line(o=None):
    o = o or json.load(open(ROOT / 'model' / 'compass.json'))
    mp = next((u for u in o['upgrades'] if u['name'] == 'Moon of Print'), None)
    if not mp: return None
    return f"Moon of Print Lv {mp['lv']}/{mp['max']} ({mp['desc']}); next level {h(mp['cost'])} {mp['currency']} on Autistacular's Compass."


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)
    print(print_line(o))
