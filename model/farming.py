"""Farming planner: GMO crop stacks, crop discovery math, Rank DB points, Night/Day/Exotic market -> Zemo's Farming block.

Inputs: raw save (FarmCrop counts, FarmUpg levels+beans), snapshots/<LATEST>/toolbox/farming.json (tb_read.js).
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
    tb = json.load(open(SNAP / 'toolbox' / 'farming.json'))['tabs']
    plot = tb['Plot']; bds = {}
    for b in plot['breakdowns']: bds.setdefault(b['label'].split(' breakdown')[0], b['text'])   # first = open plots

    stacks = {n: sum(1 for v in crops.values() if v >= t) for n, t in STACKS}
    found = len(crops)
    # crop discovery: open plots' evolution chance = base x multi (Toolbox breakdown)
    evo = bds.get('Crop evolution chance', '')
    base = _n((re.search(r'Base evolution chance\n\n([^\n]+)', evo) or [0, '0'])[1].replace('e-', 'E-')) if evo else None
    bm = re.search(r'Base evolution chance\n\n([\d.e+-]+)', evo); base = float(bm.group(1)) if bm else None
    gm = re.search(r'Group 1\n\n×([\d.e+-]+)', evo); multi = float(gm.group(1)) if gm else None
    gmo = re.search(r'Evolution GMO \(Market\)\n\n×([\d,.]+)', evo); gmo_x = float(gmo.group(1).replace(',', '')) if gmo else None
    per_stack = 2.13
    mk = market(tb['Market']['text'])
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
    ro = tb['Rank Optimizer']['text']
    rp = re.search(r'Rank points\n([\d,]+) / ([\d,]+)', plot['text'])
    unspent = int(rp.group(2).replace(',', '')) - int(rp.group(1).replace(',', '')) if rp else 0
    plan = [(m.group(1), m.group(2), m.group(3), m.group(4)) for m in
            re.finditer(r'\n(Evolution [A-Za-z]+|[A-Z][a-z]+ [A-Za-z]+)\nLv ([\d,]+) → ([\d,]+)\nx(\d+)', ro)]

    night = [u for u in mk if u['market'] == 'Night' and not u['maxed']]
    day = [u for u in mk if u['market'] == 'Day' and not u['maxed']]
    # Exotic: current rotation + purchases left
    ex = tb['Exotic Market']['text']
    pl = re.search(r'Purchases left this week\n(\d+) / (\d+)', ex)
    cur = re.search(r'Current rotation\nNext in ([^\n]+)\n(.*?)\nOff rotation', ex, re.S)
    rot = []
    if cur:
        for m in re.finditer(r'\n?([A-Z0-9][A-Za-z0-9 ]+)\nLv ([\d,]+) · Returns in (\d+w)\nEffect\n[^\n]+\n\n([^\n]+)', '\n' + cur.group(2)):
            nm = m.group(1).strip()
            note = next((v for k, v in EXOTIC_SRC.items() if nm.startswith(k)), None)
            rot.append({'name': nm, 'lv': int(m.group(2).replace(',', '')), 'returns': m.group(3), 'desc': m.group(4), 'creator': note})
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
           'night': night, 'day': day, 'exotic_left': (int(pl.group(1)), int(pl.group(2))) if pl else None,
           'exotic_next': cur.group(1) if cur else None, 'exotic_rotation': rot,
           'growth_speed': (re.search(r'Growth Speed\n([^\n]+)', plot['text']) or [0, ''])[1],
           'crop_value': (re.search(r'Crop Value\n([^\n]+)', plot['text']) or [0, ''])[1],
           'vine': (re.search(r'Crops on Vine\n([^\n]+)', plot['text']) or [0, ''])[1]}
    json.dump(out, open(ROOT / 'model' / 'farming.json', 'w'), indent=1)
    return out


def card_lines(o):
    L = []
    s = o['stacks']
    L.append(f"TOP: hold 200+ of every crop you've found. Evolution GMO stacks {s['Evolution GMO']}/{o['found']} (x{o['per_stack']} evo chance each). "
             f"Lock crops before a bean trade so the trade can't take them to 0 (Griffy 2026-11 locks crops he needs; show-lock-all setting).")
    if o['evo_chance'] is not None:
        L.append(f"Why: open plots' next-crop chance is {o['evo_chance']:.1e} per harvest (base {o['evo_base']:.1e} x multi {o['evo_multi']:.2e}). "
                 f"~{o['stacks_for_next_crop']} more 200-stacks make it ~100%. Check: Toolbox Plot > Crop evolution breakdown, 'Evolution GMO' should climb from x{o['evo_gmo_x']:,.0f}.")
    fs = ', '.join(f"{f} {a}/{n}" for f, (a, n) in o['family_stacks'].items())
    L.append(f"Stacks by family (200+ / found): {fs}. Basic grows in 1m46s, so it's the fastest place to build stacks. Pulse 2026-11: farm the low-quantity families first, then Basic.")
    L.append(f"Other GMO stacks: Speed (1,000) {s['Speed GMO']}, EXP (2,500) {s['EXP GMO']}, Value (10,000) {s['Value GMO']}, Super (100,000) {s['Super GMO']}.")
    if o['rank_unspent'] > 0:
        L.append(f"{o['rank_unspent']} Land Rank points unspent. Toolbox Rank Optimizer (Crop Evolution) puts points into: " +
                 ', '.join(f"{n} (now {a})" for n, a, b, _ in o['rank_plan'][:4]) + '. Pulse 2026-11: resetting and repushing the rank database raises next-crop chance.')
    nr = o.get('night_rank', [])
    L.append(f"Night Market ({o['beans']:,.0f} beans), best value first (gain per share of beans; Super GMO weighted up per Pulse 2026-11, Evolution GMO per Pulse): " +
             ' > '.join(spend.fmt(x) + ('' if x['afford'] else ' (save up)') for x in nr) + '. GMO gains scale with stacks, so they rise as you hold crops.')
    blocked = [u for u in o['day'] if u['have'] is not None and u['cost'] and u['have'] < u['cost']]
    if blocked:
        L.append('Day Market is paid in crops; blocked now: ' + ', '.join(f"{u['name']} {u['lv']} (have {u['have']:,.0f} / {u['cost']:,.0f})" for u in blocked[:6]) + '. Holding crops unblocks these too.')
    if o['exotic_left']:
        picks = [x for x in o['exotic_rotation'] if x['creator']]
        L.append(f"Exotic Market: {o['exotic_left'][0]}/{o['exotic_left'][1]} purchases left, rotation ends in {o['exotic_next']}. Every exotic is Lv 0. "
                 + ('Creator picks in this rotation: ' + '; '.join(f"{x['name']} (returns {x['returns']}, {x['creator']})" for x in picks) if picks else 'No creator-ranked pick in this rotation.')
                 + ' GAP: exotic cost per purchase not mapped yet.')
    return L


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l, '\n')
