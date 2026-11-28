"""Farming planner: GMO crop stacks, crop discovery math, Rank DB points, Night/Day/Exotic market -> Zemo's Farming block.

Inputs: raw save (FarmCrop counts, FarmUpg levels+beans), data.py (Toolbox parser).
Output: model/farming.json ; card_lines(o) for plan.py.
"""
import gzip, json, math, re
import spend
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / 'snapshots' / (ROOT / 'snapshots' / 'LATEST').read_text().strip()
# crop index ranges per family (Toolbox Crop tab order, checked against raw FarmCrop counts 2026-11-19)
FAMILIES = [('Basic', 0, 20, '1m46s'), ('Earthy', 21, 45, '2m40s'), ('Bulbo', 46, 60, '4m'), ('Sushi', 61, 83, '5m59s'),
            ('Mushie', 84, 106, '8m59s'), ('Glassy', 107, 229, '13m29s'), ('Medal', 230, 330, '7h')]
STACKS = [('Evolution GMO', 200), ('Speed GMO', 1000), ('EXP GMO', 2500), ('Value GMO', 10000), ('Super GMO', 100000)]
# Exotic picks the creators named (Pulse 2026-10/11 exotic tier talk). name -> note
EXOTIC_SRC = {
    'Free Exotic': 'Pulse 2026-11: all clicks in, back in 10 weeks', 'Better Exotic': 'Pulse 2026-10: #1/#2 with Free Exotic',
    'Plump Database': 'Pulse 2026-10: top 5', 'Scienterrific': 'Pulse 2026-10: amazing (Crop Scientist bonuses)',
    'Largumes II': 'Pulse 2026-10: top pick, direct beans multi', 'Legumioso III': 'Pulse 2026-10: 2nd pick, beans',
    'Vigouroot I': 'Pulse 2026-10: 3rd pick, land rank EXP multi', 'Stableroot II': 'Pulse 2026-10: 4th pick',
    'Sap Surge': 'Pulse 2026-10: strong, ~6th (Spelunking amber)', 'Gravel Pound': 'Pulse 2026-10: strong, ~7th (Spelunking POW)',
    'Geneology': 'Pulse 2026-10: a few levels, it returns rarely', '4 Leaf Clover': 'Pulse 2026-11: a few clicks (palette)',
    'Stalk Value': 'Pulse 2026-10: fills the top 10', 'Bountiful': 'Pulse 2026-11: worth the points, rare return'}


def fam(i):
    return next((f for f in FAMILIES if f[1] <= i <= f[2]), ('?', 0, 0, '?'))


def _n(s):
    s = s.replace(',', '').strip()
    m = re.match(r'([\d.]+)\s*(QQ|Q|[KMBT])?', s)
    return float(m.group(1)) * {None: 1, 'K': 1e3, 'M': 1e6, 'B': 1e9, 'T': 1e12, 'Q': 1e15, 'QQ': 1e18}[m.group(2)] if m else None


def market(text):
    """Toolbox Market tab -> [{name, lv, max, market, have, cost}]"""
    out = []
    for m in re.finditer(r'\n([A-Z][A-Za-z ]+)\nLv ([\d,]+) / ([\d,]+) · (Day|Night) market\n(.*?)(?=\n[A-Z][A-Za-z ]+\nLv |\Z)', text, re.S):
        body = m.group(5)
        nc = re.search(r'NEXT COST\n([^\n]+)\n/\n([^\n]+)', body)
        out.append({'name': m.group(1).strip(), 'lv': int(m.group(2).replace(',', '')), 'max': int(m.group(3).replace(',', '')),
                    'market': m.group(4), 'maxed': 'Maxed' in body[:40],
                    'have': _n(nc.group(1)) if nc else None, 'cost': _n(nc.group(2)) if nc else None,
                    'desc': next((x.strip() for x in body.split('\n') if x.strip() and x.strip() != 'Maxed'), '')})
    return out


def build():
    r = json.load(gzip.open(SNAP / 'raw.json.gz')); d = r.get('data', r)
    crops = d['FarmCrop']; crops = json.loads(crops) if isinstance(crops, str) else crops
    crops = {int(k): float(v) for k, v in crops.items()}
    upg = d['FarmUpg']; upg = json.loads(upg) if isinstance(upg, str) else upg
    beans = float(upg[1])
    # Zack 2026-11-25: Toolbox parser numbers (model/data.py). Evolution-chance breakdown and the Rank Optimizer are website-only.
    from data import load
    F = load().system('farming')
    bds = {}

    stacks = {n: sum(1 for v in crops.values() if v >= t) for n, t in STACKS}
    found = len(crops)
    # crop discovery: open plots' evolution chance = base x multi (Toolbox breakdown)
    evo = bds.get('Crop evolution chance', '')
    base = _n((re.search(r'Base evolution chance\n\n([^\n]+)', evo) or [0, '0'])[1].replace('e-', 'E-')) if evo else None
    bm = re.search(r'Base evolution chance\n\n([\d.e+-]+)', evo); base = float(bm.group(1)) if bm else None
    gm = re.search(r'Group 1\n\n×([\d.e+-]+)', evo); multi = float(gm.group(1)) if gm else None
    gmo = re.search(r'Evolution GMO \(Market\)\n\n×([\d,.]+)', evo); gmo_x = float(gmo.group(1).replace(',', '')) if gmo else None
    per_stack = 2.13
    mk = []
    for i, u in enumerate(F['market']):
        night = i >= 8   # Toolbox order: 8 day-market upgrades, then the night market
        have = beans if night else crops.get(int(u.get('cropId') or 0), 0)
        mk.append({'name': u['name'].replace('_', ' ').title(), 'lv': u['level'], 'max': u['maxLvl'], 'market': 'Night' if night else 'Day', 'maxed': u['level'] >= u['maxLvl'],
                   'have': have, 'cost': u.get('cost'), 'desc': str(u.get('bonus', '')).replace('_', ' ').replace('{', str(u.get('value', '')))})
    for u in mk:
        if u['name'] == 'Evolution Gmo': per_stack = float(re.search(r'([\d.]+)x', u['desc']).group(1)) if re.search(r'([\d.]+)x', u['desc']) else per_stack
    chance = base * multi if base and multi else None
    need_stacks = math.ceil(math.log(1 / chance) / math.log(per_stack)) if chance and chance < 1 else 0

    # stack queue: crops under 200, closest first, fastest family first on ties
    under = sorted([(i, v) for i, v in crops.items() if v < 200], key=lambda x: (-x[1], x[0]))
    fam_need = {}
    for i, v in crops.items():
        f = fam(i)[0]
        fam_need.setdefault(f, [0, 0]); fam_need[f][1] += 1
        if v >= 200: fam_need[f][0] += 1

    # Rank DB optimizer plan
    unspent = int(F.get('availablePoints') or 0)
    plan = []

    night = [u for u in mk if u['market'] == 'Night' and not u['maxed']]
    day = [u for u in mk if u['market'] == 'Day' and not u['maxed']]
    # Exotic: current rotation + purchases left
    rot = []
    for x in F['exoticMarket']:
        if not x.get('isAvailableThisWeek'): continue
        nm = x['name'].replace('_', ' ').title()
        note = next((v for k, v in EXOTIC_SRC.items() if nm.lower().startswith(k.lower())), None)
        rot.append({'name': nm, 'lv': x['level'], 'returns': '', 'desc': str(x.get('displayText', '')).replace('_', ' '), 'creator': note})
    pl = (int(F['exoticMarkeMaxPurchases']) - int(F['exoticMarketUpgradesPurchased']), int(F['exoticMarkeMaxPurchases']))
    # Night Market buys ranked by gain per share of beans (marginal % of each GMO's own effect, x stacks it applies to)
    st_for = {'Evolution Gmo': 'Evolution GMO', 'Speed Gmo': 'Speed GMO', 'EXP Gmo': 'EXP GMO', 'Value Gmo': 'Value GMO', 'Super Gmo': 'Super GMO'}
    wt = {'Super Gmo': 3, 'Evolution Gmo': 2}   # Pulse 2026-11: Super GMO most important; raise Evolution GMO for deeper crops
    opts = []
    for u in night:
        if not u['cost']: continue
        num = re.search(r'([\d.]+)(x|%)', u['desc']); gain = None
        if num and u['lv']:
            v = float(num.group(1)); per = (v - (1 if num.group(2) == 'x' else 0)) / u['lv']
            if u['name'] in st_for:
                k = stacks.get(st_for[u['name']], 0)
                if num.group(2) == 'x': gain = 100 * (((v + per) / v) ** k - 1)
                else: gain = 100 * per * k / (100 + v * k)
            elif num.group(2) == 'x': gain = 100 * per / v
        opts.append({'item': f"{u['name']} {u['lv']}/{u['max']}", 'currency': 'beans', 'balance': beans, 'cost': u['cost'], 'gain_pct': gain,
                     'stat': u['desc'][:40], 'weight': wt.get(u['name'], 1)})
    night_rank = spend.rank(opts).get('beans', [])
    out = {'snapshot': SNAP.name, 'found': found, 'night_rank': night_rank, 'stacks': stacks, 'beans': beans, 'evo_base': base, 'evo_multi': multi,
           'evo_chance': chance, 'evo_gmo_x': gmo_x, 'per_stack': per_stack, 'stacks_for_next_crop': need_stacks,
           'under_200': [{'crop': i, 'family': fam(i)[0], 'have': v} for i, v in under],
           'family_stacks': fam_need, 'rank_unspent': unspent, 'rank_plan': plan,
           'night': night, 'day': day, 'exotic_left': pl,
           'exotic_next': None, 'exotic_rotation': rot,
           'growth_speed': ((F.get('maxTimes') or [{}])[0].get('breakdown') or {}).get('totalValue'),
           'crop_value': ((F.get('stats') or {}).get('cropValue') or {}).get('totalValue'),
           'vine': F.get('cropsOnVine')}
    json.dump(out, open(ROOT / 'model' / 'farming.json', 'w'), indent=1)
    return out


def card_lines(o):
    L = []
    s = o['stacks']
    L.append(f"TOP: hold 200 or more of every crop you've found ({s['Evolution GMO']} of {o['found']} so far). Each one raises the chance to discover new crops. Lock them before bean trades so a trade can't empty them (Griffy does this).")
    fam = sorted(o['family_stacks'].items(), key=lambda x: x[1][0] / max(1, x[1][1]))
    L.append(f"Weakest families: {', '.join(f'{f} ({a} of {n})' for f, (a, n) in fam[:3])}. Pulse: farm the low ones first. Basic grows fastest if you want quick stacks.")
    if o['rank_unspent'] > 0:
        L.append(f"Spend {o['rank_unspent']} Land Rank points, Toolbox's optimizer puts them into the Evolution boosts.")
    nr = [x for x in o.get('night_rank', []) if x['afford']]
    if nr: L.append(f"Night Market ({spend.h(o['beans'])} beans): buy {', '.join(x['item'].split(' ')[0] + ' ' + x['item'].split(' ')[1] if ' ' in x['item'] else x['item'] for x in nr[:3])} first.")
    blocked = [u for u in o['day'] if u['have'] is not None and u['cost'] and u['have'] < u['cost']]
    if blocked: L.append(f"Day Market is paid in crops and {len(blocked)} upgrades are waiting on them. Holding crops fixes this too.")
    if o['exotic_left']:
        picks = [x['name'] for x in o['exotic_rotation'] if x['creator']]
        L.append(f"Exotic Market: {o['exotic_left'][0]} buys left this rotation ({o['exotic_next']} left)." + (f" Pulse likes {' and '.join(picks)}." if picks else ''))
    return L


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l, '\n')
