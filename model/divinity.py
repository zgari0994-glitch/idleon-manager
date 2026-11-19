"""Divinity planner: points income, Coral Kid order, blessing buys ranked per currency, links, god rank -> Bish's Divinity block.

Inputs: snapshots/<LATEST>/toolbox/divinity.json, systems.json.gz (divinity materials), chars.json (links).
"""
import gzip, json, re
from pathlib import Path
import spend

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / 'snapshots' / (ROOT / 'snapshots' / 'LATEST').read_text().strip()
GODS = ['Snehebatu', 'Arctis', 'Nobisect', 'Harriep', 'Goharut', 'Omniphau', 'Purrmep', 'Flutterbis', 'Kattlekruk', 'Bagur']


def _n(s):
    s = s.replace(',', '').strip()
    m = re.match(r'([\d.]+)\s*(QQ|Q|[KMBT])?$', s)
    return float(m.group(1)) * {None: 1, 'K': 1e3, 'M': 1e6, 'B': 1e9, 'T': 1e12, 'Q': 1e15, 'QQ': 1e18}[m.group(2)] if m else None


def build():
    T = json.load(open(SNAP / 'toolbox' / 'divinity.json'))['tabs']
    g = T['Gods']['text'].replace('\xa0', ' ') + '\n'
    sy = json.load(gzip.open(SNAP / 'systems.json.gz'))['systems']['divinity']
    mat = {v['name']: v['blessing_material'] for v in sy.values()}
    head = {k: (re.search(k + r'\n([^\n]+)', g) or [0, None])[1] for k in ['God rank', 'Total Divinity LV', 'Divinity points', 'Divinity PTS/hr']}
    gods = {}
    for i, name in enumerate(GODS):
        a = g.find('\n' + name + '\nLv ')
        if a < 0: continue
        b = min([x for x in (g.find('\n' + n + '\nLv ', a + 5) for n in GODS) if x > a] or [len(g)])
        blk = g[a:b]
        lv = re.search(r'Lv (\d+) / (\d+)', blk)
        bl = re.search(r'Blessing\n\+?([\d,.]+)%? ([^\n]+)', blk)
        cost = re.search(r'\n(?:([^\n]+)\n/\n)?([^\n]+)\nCost to max\n([^\n]+)', blk)
        linked = re.findall(r'\n(Autis\w+)\n\+?([\d.,]+)', blk)
        gods[name] = {'lv': int(lv.group(1)), 'max': int(lv.group(2)), 'maxed': 'Maxed' in blk[:60],
                      'bless': float(bl.group(1).replace(',', '')) if bl else 0, 'bless_stat': bl.group(2) if bl else '',
                      'have': _n(cost.group(1)) if cost and cost.group(1) else None, 'next': _n(cost.group(2)) if cost else None,
                      'to_max': _n(cost.group(3)) if cost else None, 'material': mat.get(name), 'linked_shown': linked}
    # stat totals for marginal gain: Divinity PTS blessings are their own multipliers (Toolbox PTS/hr breakdown)
    opts = []
    try:
        speed = json.load(open(ROOT / 'model' / 'sailing.json')).get('speed_groups', {})
    except Exception:
        speed = {}
    for n, x in gods.items():
        if x['maxed'] or not x['next']: continue
        per = x['bless'] / max(1, x['lv'])
        gain = None
        if 'Divinity PTS' in x['bless_stat']: gain = 100 * per / (100 + x['bless'])
        elif n == 'Goharut': gain = 100 * per / (100 + x['bless'])                  # own speed group B
        elif n == 'Bagur' and speed.get('speed_multi_e'): gain = 100 * (per / 125) / speed['speed_multi_e']   # additive in group E (/125)
        opts.append({'item': f"{n} blessing {x['lv']}/{x['max']}", 'currency': x['material'], 'balance': x['have'], 'cost': x['next'],
                     'gain_pct': gain, 'stat': x['bless_stat'], 'note': (f"to max {spend.h(x['to_max'])}" + (' (you can MAX it)' if x['have'] and x['to_max'] and x['to_max'] <= x['have'] else '')) if x['to_max'] else ''})
    ranked = spend.rank(opts)
    # Coral Kid upgrades (Divinity points)
    ck = T['Coral Kid Upgrades']['text'].replace('\xa0', ' ')
    pts = _n(head['Divinity points'] or '0')
    coral = []
    for m in re.finditer(r'Lv (\d+)\n\n(.+?)\n(?:\n?Needs total Divinity LV\n([\d,]+)\n)?Divinity PTS\n([^\n]+)\n/\n([^\n]+)', ck, re.S):
        coral.append({'lv': int(m.group(1)), 'desc': ' '.join(m.group(2).split())[:110], 'needs_lv': int(m.group(3).replace(',', '')) if m.group(3) else 0,
                      'cost': _n(m.group(5))})
    spir = re.search(r'Singularity Spirals\n(\d+)', ck)
    st = T['Styles']['text'].replace('\xa0', ' ')
    styles = {}
    for m in re.finditer(r'\n(Kinesis|Chakra|Focus|Mantra|Vitalic|TranQi|Zen|Mindful)\n\n([^\n]+)\n\nGives ([^\n]+)\n(?:\nUSED BY\n((?:Autis\w+\nLv \d+\n?)+))?', st):
        styles[m.group(1)] = {'gives': m.group(3), 'used_by': re.findall(r'(Autis\w+)', m.group(4) or '')}
    ch = json.load(open(SNAP / 'chars.json'))['characters']
    links = {c['character_name']: c.get('divinity_link') for c in ch}
    pb = next((b['text'] for b in T['Gods']['breakdowns'] if b['label'].startswith('Divinity PTS/hr')), '') + '\n'
    x1 = re.findall(r'\n([A-Z][^\n]+)\n\n×1\n', pb)
    off = re.findall(r'Offering (\d): (\d+)% chance\n([^\n]+) pts\n(Can afford now)?', g)
    out = {'snapshot': SNAP.name, 'head': head, 'points': pts, 'gods': gods, 'blessing_rank': {k: v for k, v in ranked.items()},
           'coral': coral, 'spirals': int(spir.group(1)) if spir else None, 'styles': styles, 'links': links, 'pts_x1': x1,
           'offerings': [{'n': int(a), 'chance': int(b), 'cost': c, 'afford': bool(d)} for a, b, c, d in off],
           'purrmep_shown': gods.get('Purrmep', {}).get('linked_shown')}
    json.dump(out, open(ROOT / 'model' / 'divinity.json', 'w'), indent=1, default=str)
    return out


def card_lines(o):
    L = []
    h = o['head']
    used = {s: v['used_by'] for s, v in o['styles'].items() if v['used_by']}
    L.append(f"TOP: Divinity points income is {h['Divinity PTS/hr']} (Toolbox PTS/hr: style rate 0, nobody meditating). Banked {h['Divinity points']}. "
             "Points only come while a character is meditating at the Divinity altar (W5); Pulse 2026-11: put characters on the Divinity platform before Super week, Mindful is the best style.")
    L.append('Styles now: ' + '; '.join(f"{s} ({o['styles'][s]['gives']}): {', '.join(u)}" for s, u in used.items()))
    g = o['gods'].get('Goharut', {})
    L.append("Goharut trick (Pulse 2026-10 + Griffy 2026-09): characters linked to Goharut who sit in Lab tubes count as at the altar, so they earn Divinity and Lab EXP at once. "
             "Pulse 2026-10: his first Arcane Cultist sits in Lab on Goharut for both. Check: Toolbox Divinity PTS/hr goes above 0 after the change.")
    nxt = [c for c in o['coral'] if c['lv'] == 0]
    if nxt:
        L.append(f"Coral Kid (all Lv 0, total Divinity LV {h['Total Divinity LV']} meets every LV requirement shown). In cost order with {spend.h(o['points'])} points:")
        for c in sorted(nxt, key=lambda c: c['cost'] or 9e99)[:6]:
            L.append(f"  {c['desc']} - {spend.h(c['cost'])} pts" + (' AFFORDABLE NOW' if c['cost'] and c['cost'] <= o['points'] else f" (need {spend.h(c['cost'] - o['points'])} more)"))
    L.append('Blessings, best buy first within each currency (gain per share of that balance). Points multipliers only pay once income is running:')
    for cur, ops in o['blessing_rank'].items():
        shared = ' (shared with Sailing boat upgrades)' if cur.startswith('sailing-treasure') else ''
        L.append(f"  {cur}{shared}: " + ' > '.join(spend.fmt(x) + ('' if x['afford'] is not False else ' NOT AFFORDABLE') for x in ops))
    L.append(f"God rank {h['God rank']}. Pulse 2026-11: endgame aims for rank 25-30; Divinity/Super week is the push (claim one by one, spend 90% of points, then singularities). Singularity spirals {o['spirals']}.")
    lk = {}
    for c, g in o['links'].items(): lk.setdefault(g, []).append(c)
    L.append('Links (save): ' + '; '.join(f"{g}: {', '.join(cs)}" for g, cs in lk.items()) +
             (f". CONFLICT: Toolbox lists {', '.join(c for c, _ in o['purrmep_shown'])} under Purrmep; confirm in game." if o['purrmep_shown'] else ''))
    L.append("Links per Griffy (review list, sources/findings/review_list.md): 1 Elemental Sorcerer on Purrmep via the bottom-left Divinity talent (2x Divinity + EXP), "
             "keep 1 on Harriep (3x printer), Arctis for the rest (talent levels + Lab mainframe), Snehebatu over Nobisect, Goharut for anyone in Lab tubes. Coral Kid 1 god choice: open.")
    if o['pts_x1']: L.append('Divinity PTS sources still x1: ' + ', '.join(o['pts_x1']))
    return L


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)
