"""Cooking planner: plate cap path, which meal to cook, kitchen spice spends, mastery unlocks -> Zemo's Cooking block.

Inputs: snapshots/<LATEST>/toolbox/cooking.json (tb_read.js), review.json.gz (AutoReview Cooking), model/sailing.json (Causticolumn odds).
"""
import gzip, json, re
import spend
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / 'snapshots' / (ROOT / 'snapshots' / 'LATEST').read_text().strip()
# plate-cap sources not yet owned -> (owner, how). Owners from model/jobs.yaml (Spelunking = Autistomatic)
CAP_SRC = {'Grimoire (at most 20)': ('Autiszemo', 'Grimoire upgrade "Supreme Head Chef Status" 0 -> 20 (+1 max plate level each)'),
           'Menagerie': ('Autisticles', 'Menagerie unlock 21: +10 max cooking LV, costs 29.75M Lumi and a higher Menagerie rank'),
           'Lore boss': ('Autistomatic', 'Defeat the Lunarheim cave lore boss in Spelunking: +10')}


def _t(s):
    """'1d 11h' / '37m 5s' / '<1s' / '> 999d' -> hours"""
    if '<' in s: return 0.0
    if '>' in s: return 1e9
    h = 0.0
    for v, u in re.findall(r'([\d.]+)\s*([dhms])', s):
        h += float(v) * {'d': 24, 'h': 1, 'm': 1 / 60, 's': 1 / 3600}[u]
    return h


def build():
    # Zack 2026-11-25: Toolbox parser numbers (model/data.py). Meal cap breakdown and next-level times are website-only.
    from data import load
    C = load().system('cooking')
    cap = int(C['mealMaxLevel'])
    meals = []
    for m in C['meals']:
        if not m.get('name') or m['level'] >= cap: continue
        need = (m.get('levelCost') or 0) - (m.get('amount') or 0)
        meals.append({'name': m['name'].replace('_', ' '), 'lv': m['level'], 'bonus': str(m.get('effect', '')).replace('_', ' '), 'next_h': None, 'next': None,
                      'ladles': None, 'short': need if need > 0 else 0})
    meals.sort(key=lambda x: x['lv'])
    kitchens = []
    for i, k in enumerate(C['kitchens']):
        kitchens.append({'k': i + 1, 'meal': '', 'rate': None, 'speed': (k.get('speedLv'), None, k.get('speedCost')), 'fire': (k.get('fireLv'), None, k.get('fireCost')),
                         'luck': (k.get('luckLv'), None, k.get('luckCost'))})
    M = C.get('cookingMastery') or {}
    rb = M.get('ribbons') or {}
    div = next((x for x in C['meals'] if x.get('name') == 'Divorce_Cake'), None)
    caust = None
    try:
        so = json.load(open(ROOT / 'model' / 'sailing.json'))
        for r in so['islands']:
            for t, n in zip(r['targets'], r['n_chests']):
                if t.startswith('Causticolumn'): caust = (t.split(' (')[0], n)
    except Exception:
        pass
    out = {'snapshot': SNAP.name, 'cap': cap, 'cap_parts': {}, 'cap_missing': [], 'meals_open': meals, 'kitchens': kitchens,
           'spice_claims': None, 'mastery': {'lv': M.get('level'), 'rate': M.get('expRate'), 'ttl': None},
           'divorce_cake': div and div['level'], 'ribbons': (rb.get('lowest'), rb.get('highest')) if rb else None, 'ribbons_day': None,
           'speed_x1': [], 'causticolumn': caust}
    json.dump(out, open(ROOT / 'model' / 'cooking.json', 'w'), indent=1)
    return out


def card_lines(o):
    L = []
    nxt = o['meals_open']
    low = ', '.join(m['name'] + ' ' + str(m['lv']) for m in nxt[:4])
    if nxt: L.append(f"Lowest meals: {low} (cap {o['cap']}). Cook the meal closest to its next level (my read).")
    if o['cap']: L.append(f"Meals cap at level {o['cap']}. Lunarheim (Spelunking cave) adds +30.")
    m = o['mastery']
    if m['lv'] is not None: L.append(f"Cooking Mastery is level {m['lv']}. Sweet unlocks when Divorce Cake reaches 75 (it's {o['divorce_cake']}).")
    if o['ribbons']: L.append(f"Ribbons: lowest rank {o['ribbons'][0]}, highest {o['ribbons'][1]}.")
    return L


def routed(o):
    out = {}
    for n in o['cap_missing']:
        w, how = CAP_SRC[n]
        if w.startswith('Autis') and w != 'Autiszemo':
            out.setdefault(w, []).append(f"Cooking plate cap (Zemo): {how}")
    return out


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l, '\n')
