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


STYLES = ['Kinesis', 'Chakra', 'Focus', 'Mantra', 'Vitalic', 'TranQi', 'Zen', 'Mindful']


def build():
    # Zack 2026-11-25: Toolbox parser numbers (model/data.py)
    from data import load
    D = load(); V = D.system('divinity')
    sy = json.load(gzip.open(SNAP / 'systems.json.gz'))['systems']['divinity']
    mat = {v['name']: v['blessing_material'] for v in sy.values()}
    pts = V['divinityPoints']
    head = {'God rank': V['godRank'], 'Total Divinity LV': None, 'Divinity points': f"{pts:,.0f}", 'Divinity PTS/hr': None}
    gods = {}
    for d in V['deities']:
        i = int(d.get('godIndex', 0)); name = d.get('name') or (GODS[i] if i < len(GODS) else str(i))
        c = d.get('cost') or {}
        hv = c.get('currency')
        if isinstance(hv, dict): hv = hv.get('value') or hv.get('amount') or hv.get('totalAmount')
        gods[name] = {'lv': d['level'], 'max': d['maxLevel'], 'maxed': d['level'] >= d['maxLevel'], 'bless': d.get('blessingBonus') or 0,
                      'bless_stat': str(d.get('blessing', '')).replace('_', ' ').replace('{', ''), 'have': hv, 'next': c.get('nextLevelCost') or c.get('cost'),
                      'to_max': c.get('costToMax'), 'material': c.get('type') or mat.get(name), 'linked_shown': []}
    opts = []
    for n, x in gods.items():
        if x['maxed'] or not x['next']: continue
        per = x['bless'] / max(1, x['lv']); gain = 100 * per / (100 + x['bless']) if 'Divinity PTS' in x['bless_stat'] or n == 'Goharut' else None
        opts.append({'item': f"{n} blessing {x['lv']}/{x['max']}", 'currency': x['material'], 'balance': x['have'], 'cost': x['next'], 'gain_pct': gain, 'stat': x['bless_stat'],
                     'note': ('you can MAX it' if x['have'] and x['to_max'] and x['to_max'] <= x['have'] else '')})
    ranked = spend.rank(opts)
    coral = [{'lv': k['level'], 'desc': str(k['description']).replace('_', ' ').replace(' @ ', ' ')[:110], 'needs_lv': k.get('divinityLevelReq') or 0, 'cost': k['cost']}
             for k in D.get('account.coralReef.coralKidUpgrades', True)]
    names = [c['name'] for c in D.characters]
    styles = {}
    for i, st in enumerate(V.get('linkedStyles') or []):
        if i < len(names) and isinstance(st, int) and st < len(STYLES):
            styles.setdefault(STYLES[st], {'gives': '', 'used_by': []})['used_by'].append(names[i])
    ch = json.load(open(SNAP / 'chars.json'))['characters']
    links = {c['character_name']: c.get('divinity_link') for c in ch}
    off = [{'n': i + 1, 'chance': int(o['chance'] * 100), 'cost': f"{o['cost']:,.0f}", 'afford': o['cost'] <= pts} for i, o in enumerate(V.get('offerings') or [])]
    out = {'snapshot': SNAP.name, 'head': head, 'points': pts, 'gods': gods, 'blessing_rank': {k: v for k, v in ranked.items()},
           'coral': coral, 'spirals': None, 'styles': styles, 'links': links, 'pts_x1': [], 'offerings': off, 'purrmep_shown': []}
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
