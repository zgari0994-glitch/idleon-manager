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
    if str(h['Divinity PTS/hr']).startswith('0'):
        L.append(f"TOP: you're earning 0 Divinity points because nobody is meditating. Put someone on Mindful style at the W5 altar (Pulse: Mindful is best). You have {h['Divinity points']} banked.")
    L.append('Trick from Pulse and Griffy: characters linked to Goharut who sit in Lab tubes count as meditating, so they earn Divinity and Lab EXP at the same time.')
    aff = [c for c in o['coral'] if c['lv'] == 0 and c['cost'] and c['cost'] <= o['points']]
    if aff: L.append(f"Coral Kid: buy the cheapest upgrade now ({spend.h(aff[0]['cost'])} points): {aff[0]['desc'].split('!')[0][:70]}.")
    best = [ops[0] for cur, ops in o['blessing_rank'].items() if ops and ops[0]['afford']]
    if best: L.append('Best blessing buys: ' + ', '.join(x['item'].split(' blessing')[0] for x in best[:4]) + '.')
    L.append(f"God rank {h['God rank']}. Pulse says endgame is rank 25 to 30, and Super week is when you push it.")
    if o['purrmep_shown']: L.append(f"Check in game whether {o['purrmep_shown'][0][0]} is linked to Purrmep (Toolbox and the save disagree).")
    L.append('God links are on the review list for later.')
    return L


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)
