"""Cooking planner: plate cap path, which meal to cook, kitchen spice spends, mastery unlocks -> Zemo's Cooking block.

Inputs: snapshots/<LATEST>/toolbox/cooking.json (tb_read.js), review.json.gz (AutoReview Cooking), model/sailing.json (Causticolumn odds).
"""
import gzip, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / 'snapshots' / (ROOT / 'snapshots' / 'LATEST').read_text().strip()
# plate-cap sources not yet owned -> (owner, how). Owners from model/system_index.yaml; Lunarheim = Spelunking (no owner yet)
CAP_SRC = {'Grimoire (at most 20)': ('Autiszemo', 'Grimoire upgrade "Supreme Head Chef Status" 0 -> 20 (+1 max plate level each)'),
           'Menagerie': ('Autisticles', 'Menagerie unlock 21: +10 max cooking LV, costs 29.75M Lumi and a higher Menagerie rank'),
           'Lore boss': ('Spelunking (no owner yet)', 'Defeat the Lunarheim cave lore boss in Spelunking: +10')}


def _t(s):
    """'1d 11h' / '37m 5s' / '<1s' / '> 999d' -> hours"""
    if '<' in s: return 0.0
    if '>' in s: return 1e9
    h = 0.0
    for v, u in re.findall(r'([\d.]+)\s*([dhms])', s):
        h += float(v) * {'d': 24, 'h': 1, 'm': 1 / 60, 's': 1 / 3600}[u]
    return h


def build():
    T = json.load(open(SNAP / 'toolbox' / 'cooking.json'))['tabs']
    B = {b['label']: b['text'] for t in T.values() for b in t['breakdowns']}
    capb = next((v for k, v in B.items() if k.startswith('Meal max level')), '') + '\n'
    cap = int(re.search(r'Meal max level\n(\d+)', capb).group(1)) if capb else None
    parts = re.findall(r'\n([A-Z][^\n]+)\n\n(\d+)\n', capb)
    have = {n: int(v) for n, v in parts}
    missing = [n for n in CAP_SRC if have.get(n, 0) == 0]
    # meals not at cap: name, level, next level time (all kitchens), ladles
    meals = []
    mt = T['Meals']['text'].replace('\xa0', ' ')
    for m in re.finditer(r'\n([A-Z][A-Za-z ]+)\nLv (\d+)\n\+?([^\n]+)\nProgress\n([^\n]+)\n / \n([^\n]+)\nNext level\n([^\n]+)\nAt Lv \d+\n([^\n]+)\n([^\n]+)\n', mt):
        meals.append({'name': m.group(1), 'lv': int(m.group(2)), 'bonus': m.group(3), 'next_h': _t(m.group(6)), 'next': m.group(6),
                      'ladles': m.group(8)})
    meals.sort(key=lambda x: x['next_h'])
    # kitchens: what they cook + upgrade levels and have/cost spice
    kt = T['Kitchens']['text'].replace('\xa0', ' ')
    kitchens = []
    for m in re.finditer(r'Kitchen (\d+)\n([^·\n]+) · ([^\n]+) meals/hr\nSpeed Lv (\d+)\n[^\n]+\n([^\n]+)\n/\n([^\n]+)\nFire Lv (\d+)\n[^\n]+\n([^\n]+)\n/\n([^\n]+)\nLuck Lv (\d+)\n[^\n]+\n([^\n]+)\n/\n([^\n]+)', kt):
        n = lambda s: float(s.replace(',', '').replace('K', 'e3').replace('M', 'e6').replace('B', 'e9'))
        kitchens.append({'k': int(m.group(1)), 'meal': m.group(2).strip(), 'rate': m.group(3),
                         'speed': (int(m.group(4)), n(m.group(5)), n(m.group(6))), 'fire': (int(m.group(7)), n(m.group(8)), n(m.group(9))),
                         'luck': (int(m.group(10)), n(m.group(11)), n(m.group(12)))})
    sc = re.search(r'Spice claims\n(\d+) / (\d+)', kt)
    # mastery
    ms = T['Mastery']['text']
    lv = re.search(r'Mastery level\n(\d+)', ms); rate = re.search(r'EXP rate\n([^\n]+)', ms); ttl = re.search(r'Time to level\n([^\n]+)', ms)
    div = next((x for x in meals if x['name'] == 'Divorce Cake'), None)
    rb = T['Ribbons']['text']
    rib = re.search(r'Ribboned meals\n(\d+) / (\d+)', rb); rpd = re.search(r'Ribbons per day\n([^\n]+)', rb)
    spd = next((v for k, v in B.items() if k.startswith('Kitchen 1 speed')), '') + '\n'
    x1 = re.findall(r'\n([A-Z][^\n]+)\n\n×1\n', spd)
    caust = None
    try:
        so = json.load(open(ROOT / 'model' / 'sailing.json'))
        for r in so['islands']:
            for t, n in zip(r['targets'], r['n_chests']):
                if t.startswith('Causticolumn'): caust = (t.split(' (')[0], n)
    except Exception:
        pass
    out = {'snapshot': SNAP.name, 'cap': cap, 'cap_parts': have, 'cap_missing': missing, 'meals_open': meals, 'kitchens': kitchens,
           'spice_claims': (int(sc.group(1)), int(sc.group(2))) if sc else None, 'mastery': {'lv': lv and int(lv.group(1)), 'rate': rate and rate.group(1), 'ttl': ttl and ttl.group(1)},
           'divorce_cake': div and div['lv'], 'ribbons': (int(rib.group(1)), int(rib.group(2))) if rib else None, 'ribbons_day': rpd and rpd.group(1),
           'speed_x1': x1, 'causticolumn': caust}
    json.dump(out, open(ROOT / 'model' / 'cooking.json', 'w'), indent=1)
    return out


def card_lines(o):
    L = []
    nxt = [m for m in o['meals_open']]
    cooking = sorted({k['meal'] for k in o['kitchens']})
    slow = [k for k in o['kitchens'] if k['meal'] in {m['name'] for m in nxt if m['next_h'] > 6}]
    if nxt:
        fast = [m for m in nxt if m['next_h'] < 1]
        L.append(f"TOP: all {len(o['kitchens'])} kitchens cook {', '.join(cooking)} ({next((m['next'] for m in nxt if m['name'] in cooking), '?')} per level). "
                 f"Level the cheap meals first: " + ', '.join(f"{m['name']} Lv {m['lv']} (next level {m['next']})" for m in fast) +
                 ". My read: put kitchens on the meal with the shortest 'Next level' in Toolbox Cooking > Meals and recheck each refresh.")
        L.append('Open meals by time to next level (all kitchens): ' + '; '.join(f"{m['name']} {m['lv']} {m['next']} [{m['bonus']}]" for m in nxt))
    if o['cap']:
        L.append(f"Plate cap {o['cap']} (AutoReview T11 needs 150, T12 180): " + ', '.join(f"{k} {v}" for k, v in o['cap_parts'].items() if v) +
                 '. Missing, in order:')
        for n in o['cap_missing']:
            w, how = CAP_SRC[n]; L.append(f"  {how} [{w}]")
        if o['causticolumn']:
            L.append(f"  Causticolumn next form (+10): {o['causticolumn'][0]}, 1 in {o['causticolumn'][1]:,} chests [Autisticles, Sailing 'Later']")
    cheap = []
    for k in o['kitchens']:
        for nm in ('speed', 'fire', 'luck'):
            lv, hv, cost = k[nm]
            if cost and hv >= cost * 20: cheap.append(f"K{k['k']} {nm.title()} {lv} (cost {cost:,.0f}, have {hv:,.0f})")
    if cheap:
        L.append(f"Spice to spend (cost under 5% of what you hold): {'; '.join(cheap[:12])}{' +' + str(len(cheap) - 12) + ' more' if len(cheap) > 12 else ''}. "
                 "Griffy (older clip): level every kitchen upgrade, every 10 levels adds kitchen speed.")
    if o['spice_claims']: L.append(f"Spice claims {o['spice_claims'][0]}/{o['spice_claims'][1]}.")
    m = o['mastery']
    if m['lv'] is not None:
        L.append(f"Cooking Mastery Lv {m['lv']}, {m['rate']} ({m['ttl']} to next). All EXP boosts at 0. Sweet unlocks when Divorce Cake passes 75 (now {o['divorce_cake']}); "
                 "Smoky (daily ribbons +1 rank) at mastery 10. Pulse 2026-11: mastery on Nyanborgir adds crop evo.")
    if o['ribbons']: L.append(f"Ribbons: {o['ribbons'][0]}/{o['ribbons'][1]} meals ribboned, {o['ribbons_day']} per day.")
    if o['speed_x1']: L.append('Kitchen speed sources still x1: ' + ', '.join(o['speed_x1']))
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
