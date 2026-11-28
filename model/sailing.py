"""Sailing planner: artifacts, islands, boats, captains -> daily moves for the Siege Breaker.

Inputs (per snapshot):
  systems.json.gz  sailing (artifact forms, islands, captains, boats)  [AutoReview parse]
  toolbox/sail_detail.txt       Toolbox Boats and Captains tab (details on)
  model/sail_consts.json  artifact base find odds (game constants); live breakdowns come from the parser
Island find formula = Toolbox bundle (sources/toolbox/sailing_js_snippet.txt), calibrated to Toolbox's
own per-boat 'Artifact chance'.
Output: model/sailing.json + model/sailing.md
"""
import gzip, json, math, re, statistics, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / 'snapshots' / (ROOT / 'snapshots' / 'LATEST').read_text().strip()
FORMS = ['Undiscovered', 'Ancient', 'Eldritch', 'Sovereign', 'Omnipotent', 'Transcendent', 'Verisimilitude']
# acquired index: 0 none/base, 1 base found (Ancient next)... AutoReview 'form' names the CURRENT form.
FORM_IDX = {'Undiscovered': 0, 'Base': 1, 'Ancient': 2, 'Eldritch': 3, 'Sovereign': 4, 'Omnipotent': 5,
            'Transcendent': 6, 'Verisimilitude': 7}
NEXT = {0: 'Base', 1: 'Ancient', 2: 'Eldritch', 3: 'Sovereign', 4: 'Omnipotent', 5: 'Transcendent', 6: 'Verisimilitude'}
LETTER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def _num(s):
    s = s.replace(',', '').strip()
    m = re.match(r'([\d.]+)\s*([KMBTQ]?)', s)
    if not m: return None
    return float(m.group(1)) * {'': 1, 'K': 1e3, 'M': 1e6, 'B': 1e9, 'T': 1e12, 'Q': 1e15}[m.group(2)]


def denom(acq, s, X=960, Y=0):
    """Toolbox: odds needed for the NEXT form of an artifact at island index s (acq = current acquired idx)."""
    f = 1 + Y / 100
    if acq == 1: return 850 if s < 3 else (1000 + (s - 3) * X) / f
    if acq == 2: return 900 + 250 * s if s < 3 else (1000 + (s - 3) * X) / f * 4
    if acq == 3: return 9e3 + 2e3 * s if s < 5 else (1000 + 1.25 * (s - 3) * X) / f * 180
    if acq == 4: return 12e4 + 4e4 * s if s < 6 else 1e4 * (1 + 50 * (s - 5) / 100) * ((3e3 + 3 * (s - 5) * X) / f)
    if acq == 5:
        return 4e7 + 6e7 * s if s < 6 else 1e6 * (1 + (s - 5)) * max(1, 1.7 ** max(0, s - 7)) * (1 + .5 * max(0, s - 9)) * ((1e4 + 5e3 * (s - 5) * (X / 960)) / f)
    if acq == 6:
        return 5e14 * 3 ** s if s < 6 else 1e16 * (1 + .1 * (s - 5)) * max(1, 1.4 ** max(0, s - 7)) * (1 + .1 * max(0, s - 9)) * ((1e4 + 1e3 * (s - 5) * (X / 960)) / f)
    return None


def parse_toolbox(txt):
    t = txt.replace('\\n', '\n')
    boats, caps, shop = [], {}, []
    bpart = t.split('\nIslands\n')[0]
    for blk in re.split(r'\nBoat (\d+)\n', bpart)[1:]:
        pass
    chunks = re.split(r'\n(?=Boat \d+\nLv )', bpart)
    for c in chunks:
        m = re.match(r'Boat (\d+)\nLv (\d+) · (?:Captain ([A-Z]) · )?(.+)\n', c)
        if not m: continue
        g = lambda k: (re.search(k + r'\n([^\n]+)', c) or [None, None])[1]
        lootlv = re.search(r'LOOT · LV (\d+)\n([^\n]+)\n/\n([^\n]+)', c)
        spdlv = re.search(r'SPEED · LV (\d+)\n([^\n]+)\n/\n([^\n]+)', c)
        nl = re.search(r'LOOT · LV \d+.*?\nLv (\d+): [^\n]+\n(\d+) left', c, re.S)
        ns = re.search(r'SPEED · LV \d+.*?\nLv (\d+): [^\n]+\n(\d+) left', c, re.S)
        need_s = re.search(r'SPEED · LV \d+\n[^\n]+\n/\n[^\n]+\nneed ([^\n]+) more', c)
        need_l = re.search(r'LOOT · LV \d+\n[^\n]+\n/\n[^\n]+\nneed ([^\n]+) more', c)
        boats.append({'boat': int(m.group(1)), 'level': int(m.group(2)), 'captain': m.group(3), 'island': m.group(4).strip(),
                      'loot': _num(g('Loot')), 'speed': _num(g('Speed')), 'min_dist': _num(g('Min travel distance') or '0'),
                      'odds': _num(g('Artifact odds') or '0'), 'chance': _num((g('Artifact chance') or '0').rstrip('%')),
                      'arrives': g('Arrives in'), 'loot_lv': int(lootlv.group(1)) if lootlv else None,
                      'speed_lv': int(spdlv.group(1)) if spdlv else None,
                      'loot_buy': (int(nl.group(1)), int(nl.group(2))) if nl and not need_l else None,
                      'speed_buy': (int(ns.group(1)), int(ns.group(2))) if ns and not need_s else None,
                      'loot_need': need_l.group(1) if need_l else None, 'speed_need': need_s.group(1) if need_s else None})
    cpart = t.split('\nCaptains shop\n')[1] if '\nCaptains shop\n' in t else ''
    shop_txt, _, cap_txt = cpart.partition('\nCaptains\n')
    for c in re.split(r'\nShop captain\n|^Shop captain\n', shop_txt):
        bu = re.findall(r'([A-Za-z ]+)\n\+(\d+)% per level', c)
        cm = re.search(r'\n[\d.]+[KMBTQ]?\n/\n([\d.]+[KMBTQ]?)', c)
        if bu: shop.append({'buffs': [(n.strip(), int(v)) for n, v in bu], 'cost': cm.group(1) if cm else None})
    for c in re.split(r'\n(?=Captain [A-Z]\n)', '\n' + cap_txt):
        m = re.match(r'\nCaptain ([A-Z])\nLv (\d+)(?: · Boat (\d+))?', c) or re.match(r'Captain ([A-Z])\nLv (\d+)(?: · Boat (\d+))?', c)
        if not m: continue
        bu = re.findall(r'([A-Za-z ]+)\n\+([\d,.]+)% \(\+(\d+)% per level\)', c)
        caps[m.group(1)] = {'captain': m.group(1), 'level': int(m.group(2)), 'boat': int(m.group(3)) if m.group(3) else None,
                            'buffs': [(n.strip(), float(v.replace(',', '')), int(p)) for n, v, p in bu]}
    return boats, caps, shop


def from_parsed():
    # Zack 2026-11-25: same shapes as parse_toolbox()/read_trades(), from Toolbox's parser (model/data.py)
    from data import load
    D = load(); S = D.system('sailing')
    cl = lambda x: str(x).replace('_', ' ')
    def total(tree):
        add, mul = 0, 1
        for g_ in tree:
            for ch in g_.get('children', []):
                if ch.get('unit') == 'percent': add += ch.get('value') or 0
                else: mul *= ch.get('value') or 1
        return (1 + add / 100) * mul
    mt_h = float(S['minimumTravelTime']) / 60
    boats = []
    for b in S['boats']:
        res = b.get('resources') or []
        aff = lambda i: len(res) > i and res[i]['amount'] >= res[i]['required']
        co = b.get('chestOdds') or {}
        boats.append({'boat': int(b['boatIndex']) + 1, 'level': int(b['level']), 'captain': b.get('captainMappedIndex') if int(b.get('captainIndex', -1)) >= 0 else None,
                      'island': cl((b.get('island') or {}).get('name', '')), 'loot': b['loot']['value'], 'speed': float(b['speed']['raw']),
                      'min_dist': float(b['speed']['raw']) * mt_h, 'odds': total(b['artifactChance']['breakdown']['tree']), 'chance': float(co.get('expectedArtifactChance') or 0),
                      'arrives': f"{float(b.get('timeLeft') or 0) / 3600:.1f}h", 'loot_lv': int(b['lootLevel']), 'speed_lv': int(b['speedLevel']),
                      'loot_buy': (int(b['lootLevel']) + 1, 1) if aff(0) else None, 'speed_buy': (int(b['speedLevel']) + 1, 1) if aff(1) else None,
                      'loot_need': None, 'speed_need': None})
    on = S.get('captainsOnBoats') or {}
    def buffs(c, per=True):
        out = []
        for k in ('first', 'second'):
            if int(c.get(f'{k}BonusIndex', -1)) < 0: continue
            nm = cl(c.get(f'{k}BonusName', '')).replace('Disc', 'Discover') if c.get(f'{k}BonusName') else ''
            nm = cl(str(c.get(f'{k}BonusDescription', '')).split('%', 1)[-1]).strip() or nm
            out.append((nm, float(c.get(f'{k}Bonus') or 0), int(c.get(f'{k}BonusValue') or 0)) if per else (nm, int(c.get(f'{k}BonusValue') or 0)))
        return out
    caps = {c['captainIndex']: {'captain': c['captainIndex'], 'level': int(c['level']), 'boat': (on[c['captainIndex']] + 1) if isinstance(on.get(c['captainIndex']), int) and on[c['captainIndex']] >= 0 else None,
                                'buffs': buffs(c)} for c in S['captains']}
    shop = [{'buffs': buffs(c, False), 'cost': f"{c.get('cost'):,.0f}" if c.get('cost') is not None else None} for c in S['shopCaptains']]
    return boats, caps, shop


def read_trades():
    # Zack 2026-11-25: trades from Toolbox's parser
    from data import load
    out = []
    for t in load().system('sailing').get('trades') or []:
        g, r = t.get('lootItemCost') or 0, t.get('moneyValue') or 0
        out.append({'when': '', 'give': f"{g:,.0f}", 'get': f"{r:,.0f}", 'ratio': r / max(g, 1), 'item': t.get('rawName')})
    return out

def b_speed(boats, bn):
    return next(b['speed'] for b in boats if b['boat'] == bn)


def build():
    sy = json.load(gzip.open(SNAP / 'systems.json.gz'))['systems']['sailing']
    from data import load
    sv = load().get('account.serverVars')
    X = sv.get('AncientOddPerIsland', 960); Y = sv.get('AncientArtiPCT', 0)
    # base_find = game constants (artifact base odds); read from the newest snapshot that has them
    bd = {'base_find': json.load(open(ROOT / 'model' / 'sail_consts.json'))['base_find']}   # game constants (L18 migration 2026-11-28)
    boats, caps, shop = from_parsed()
    # live breakdown numbers from the parser (replace the 11-19 page read; base_find stays as game constants)
    S_ = load().system('sailing')
    def split(tree):
        add, mul = {}, {}
        for g_ in tree:
            for ch in g_.get('children', []):
                (add if ch.get('unit') == 'percent' else mul)[ch['name']] = ch.get('value') or 0
        return add, mul
    a_, m_ = split(S_['boats'][0]['artifactChance']['breakdown']['tree'])
    tot = (1 + sum(a_.values()) / 100)
    for v_ in m_.values(): tot *= (v_ or 1)
    la, lm = split((S_.get('lootMulti') or {}).get('breakdown', {}).get('tree', []))
    lt = (1 + sum(la.values()) / 100)
    for v_ in lm.values(): lt *= (v_ or 1)
    bd = dict(bd, artifact_odds_total=tot, additive_pct=a_, multipliers=m_, min_travel_min=float(S_['minimumTravelTime']),
              loot_multi=lt, loot_additive_pct=la, loot_multipliers=lm, server_vars={'AncientOddPerIsland': X, 'AncientArtiPCT': Y})
    isl_names = list(sy['islands'])
    isl = {n: {'idx': i, 'distance': float(v['distance']), 'unlocked': v['unlocked'], 'arts': []} for i, (n, v) in enumerate(sy['islands'].items())}
    tier_cap = sy.get('unlocked_artifact_tier', 7)
    arts = []
    for a in sy['artifacts'].values():
        acq = FORM_IDX.get(a.get('form'), 0)
        key = a['name'].replace(' ', '_')
        base = bd['base_find'].get(key)
        d = base if acq == 0 else denom(acq, isl[a['island']]['idx'], X, Y)
        nxt = NEXT.get(acq) if acq < tier_cap else None
        rec = {'name': a['name'], 'island': a['island'], 'form': a.get('form'), 'acq': acq, 'next': nxt, 'denom': d if nxt else None}
        arts.append(rec); isl[a['island']]['arts'].append(rec)

    def chance(odds, island, k=1.0):
        p = 1.0
        for r in isl[island]['arts']:
            if r['denom']: p *= max(0.0, 1 - k * odds / r['denom'])
        return 1 - p

    # calibrate k so our per-chest chance matches Toolbox's own number per boat
    ks = []
    for b in boats:
        if b['odds'] and b['chance'] and b['island'] in isl:
            raw = chance(b['odds'], b['island'])
            if raw > 0: ks.append(b['chance'] / 100 / raw)
    k = statistics.median(ks) if ks else 1.0
    min_t = bd['min_travel_min'] / 60
    # artifact odds model: odds = multi * (1 + (add_wo_captain + captain_afc)/100)
    add_wo = sum(v for n, v in bd['additive_pct'].items() if n != 'Captain')
    multi = bd['artifact_odds_total'] / (1 + (add_wo + bd['additive_pct']['Captain']) / 100)
    afc = lambda c: sum(v for n, v, _ in caps[c]['buffs'] if n == 'Artifact Find Chance') if c in caps else 0
    odds_of = lambda c: multi * (1 + (add_wo + afc(c)) / 100)

    # per-island ranking for a no-AFC boat
    base_odds = multi * (1 + add_wo / 100)
    rank = []
    for n, v in isl.items():
        live = sorted([r for r in v['arts'] if r['denom']], key=lambda r: r['denom'])
        v['arts'] = sorted(v['arts'], key=lambda r: r['denom'] or 9e99)
        if not v['unlocked'] or not live: continue
        rank.append({'island': n, 'idx': v['idx'], 'distance': v['distance'], 'per_chest_pct': round(100 * chance(base_odds, n, k), 3),
                     'targets': [f"{r['name']} {r['form']}->{r['next']} (1 in {r['denom'] / (k * base_odds):,.0f} chests)" for r in live]})
    rank.sort(key=lambda r: -r['per_chest_pct'])

    # each boat: best reachable island inside min travel time (pile caps throughput, so per-chest chance rules)
    plan = []
    for b in boats:
        o = odds_of(b['captain'])
        reach = [r for r in rank if b['speed'] and r['distance'] <= b['min_dist']] or rank[-1:]
        best = max(reach, key=lambda r: chance(o, r['island'], k))
        cur = 100 * chance(o, b['island'], k) if b['island'] in isl else 0
        new = 100 * chance(o, best['island'], k)
        plan.append({'boat': b['boat'], 'captain': b['captain'], 'now': b['island'], 'now_pct': round(cur, 3),
                     'best': best['island'], 'best_pct': round(new, 3), 'move': best['island'] != b['island'] and new > cur * 1.05,
                     'speed_buy': b['speed_buy'], 'loot_buy': b['loot_buy'], 'speed_lv': b['speed_lv'], 'loot_lv': b['loot_lv'],
                     'trip_h': max(min_t, b['island'] in isl and isl[b['island']]['distance'] / b['speed'] if b['speed'] else 99)})

    # captains: AFC ranking; shop captains at the owned average level
    lv_avg = round(statistics.mean(c['level'] for c in caps.values())) if caps else 15
    cap_rank = sorted(({'captain': c, 'level': v['level'], 'boat': v['boat'], 'afc': afc(c),
                        'buffs': [f"{n} +{val:g}%" for n, val, _ in v['buffs']]} for c, v in caps.items()), key=lambda r: -r['afc'])
    shop_rank = [{'buffs': s['buffs'], 'afc_at_avg': sum(p for n, p in s['buffs'] if n == 'Artifact Find Chance') * lv_avg} for s in shop]

    # ---- Phase 2: speed captains on the highest speed-level boats -> World's End boats
    spd = lambda c: sum(v for n, v, _ in caps[c]['buffs'] if n == 'Boat Speed') if c in caps else 0
    base_spd = {b['boat']: b['speed'] / (1 + spd(b['captain']) / 100) for b in boats if b['speed']}
    we = isl["World's End"]['distance']; swaps = []; we_boats = {}
    scap = sorted([c for c in caps if spd(c) >= 300], key=lambda c: -spd(c))
    sboat = sorted(base_spd, key=lambda b: -base_spd[b])
    bcap = {b['boat']: b['captain'] for b in boats}
    for c, bn in zip(scap, sboat):
        new = base_spd[bn] * (1 + spd(c) / 100); trip = we / new
        if trip > 2.0: continue
        old_c = bcap[bn]; old_b = caps[c]['boat']
        if old_c != c:
            swaps.append({'captain': c, 'to_boat': bn, 'from_boat': old_b, 'other': old_c,
                          'speed_now': b_speed(boats, bn), 'speed_new': new, 'we_trip_h': round(trip, 2), 'ballot_trip_h': round(we / (new * 2.01), 2)})
            bcap[bn], bcap[old_b] = c, old_c
        we_boats[bn] = {'captain': c, 'speed': new, 'trip_h': max(min_t, trip), 'ballot_trip_h': max(min_t, we / (new * 2.01))}
    for b in boats:
        b['captain'] = bcap[b['boat']]
    plan = [p for p in plan if p['boat'] not in we_boats]
    for p in plan: p['captain'] = bcap[p['boat']]
    for w in swaps:
        caps[w['captain']]['boat'] = w['to_boat']
        if w['other'] in caps: caps[w['other']]['boat'] = w['from_boat']
    for r in cap_rank: r['boat'] = caps[r['captain']]['boat']

    # ---- allocation: spread boats over islands with cheap targets so every claim pushes several artifacts
    CHEAP = 1500   # chests; above this a target is a later phase (needs more odds or speed)
    for r in rank:
        live = [a for a in isl[r['island']]['arts'] if a['denom']]
        r['n_chests'] = [round(a['denom'] / (k * base_odds)) for a in live]   # same order as r['targets']
        r['cheap'] = [n for n in r['n_chests'] if n <= CHEAP]
    md = sorted(b['min_dist'] for b in boats if b['speed'])
    cheap_isl = [r for r in rank if r['cheap'] and r['distance'] <= md[len(md) // 2]]   # reachable in min travel time by most boats
    nb = len(plan)
    w = {r['island']: max(r['cheap']) for r in cheap_isl}
    alloc = {i: 1 for i in w}
    for _ in range(max(0, nb - len(alloc))):   # give the next boat to the island with most chests per boat left
        i = max(w, key=lambda i: w[i] / alloc[i]); alloc[i] += 1
    # keep boats already on a wanted island there; move the rest; AFC captains go to the slowest islands
    need = dict(alloc); moves = []; free = []
    for p in sorted(plan, key=lambda p: -afc(p['captain'])):
        if need.get(p['now'], 0) > 0: need[p['now']] -= 1; p['go'] = p['now']
        else: free.append(p)
    order = sorted([i for i in need for _ in range(need[i])], key=lambda i: -isl[i]['distance'])   # far islands first
    mdist = {b['boat']: b['min_dist'] for b in boats}
    for bn, w_ in we_boats.items():
        o_ = odds_of(w_['captain'])
        nb_ = next(b for b in boats if b['boat'] == bn)
        moves.append({'boat': bn, 'captain': w_['captain'], 'now': nb_['island'], 'go': "World's End", 'we': True,
                      'now_pct': round(100 * chance(o_, nb_['island'], k), 3), 'go_pct': 0, 'trip_h': w_['trip_h']})
    for i in order:
        cand = [p for p in free if mdist[p['boat']] >= isl[i]['distance']] or free
        if not cand: break
        p = cand[0]; free.remove(p); p['go'] = i; moves.append(p)
    for p in plan + [m for m in moves if m['boat'] in we_boats]:
        p['go_pct'] = round(100 * chance(odds_of(p['captain']), p.get('go', p['now']), k), 3)
    later = [{'island': r['island'], 'targets': [t for t, n in zip(r['targets'], r['n_chests']) if n > CHEAP]} for r in rank if any(n > CHEAP for n in r['n_chests'])]

    missing_multi = [n for n, v in bd['multipliers'].items() if v == 1]
    missing_add = [n for n, v in bd['additive_pct'].items() if v == 0]
    chests_per_h = len(boats) / min_t
    out = {'snapshot': SNAP.name, 'k_calibration': round(k, 4), 'min_travel_min': bd['min_travel_min'], 'base_odds': round(base_odds, 2),
           'odds_multi_group': round(multi, 2), 'additive_wo_captain': round(add_wo, 1), 'pile_fill_min': round(30 / chests_per_h * 60),
           'alloc': alloc, 'speed_swaps': swaps, 'we_boats': {str(k): {kk: (round(vv, 2) if isinstance(vv, float) else vv) for kk, vv in v.items()} for k, v in we_boats.items()},
           'speed_multi': sy.get('speed_multi'), 'speed_groups': {k: sy.get(k) for k in ['speed_multi_a', 'speed_multi_b', 'speed_multi_c', 'speed_multi_d', 'speed_multi_e', 'speed_multi_f']},
           'purrmep_linked': sy.get('purrmep_linked'), 'ballot': sy.get('_ballot_buff'), 'moves': [{'boat': p['boat'], 'captain': p['captain'], 'from': p['now'], 'to': p['go'], 'pct_from': p['now_pct'], 'pct_to': p['go_pct'], 'trip_from_h': round(p['trip_h'], 1), 'we': p.get('we', False)} for p in moves],
           'later': later, 'chests_per_hour': round(chests_per_h, 1),
           'islands': rank, 'boats': plan, 'captains': cap_rank, 'shop': shop_rank, '_caps': caps, '_shop': shop, '_trades': read_trades(), 'artifacts': arts,
           'odds_missing_multipliers': missing_multi, 'odds_missing_additive': missing_add, 'tier_cap': tier_cap,
           'maw': {'distance': isl['The Maw']['distance'], 'unlocked': isl['The Maw']['unlocked']}}
    json.dump(out, open(ROOT / 'model' / 'sailing.json', 'w'), indent=1)
    return out


if __name__ == '__main__':
    o = build()
    print('k', o['k_calibration'], 'base odds', o['base_odds'], 'pile fill min', o['pile_fill_min'])
    for r in o['islands'][:8]: print(r['island'], r['per_chest_pct'], r['targets'][:3])
    print(o['alloc']); print(len(o['moves']), 'moves')
    for m in o['moves']: print(m)


ROUTE = [  # odds source -> system_index key (owners come from model/system_index.yaml)
    ('Killroy', 'killroy'), ('Vial', 'alchemy_vials'), ('Tome', 'tome'), ('Sneaking', 'sneaking'), ('Summoning - Win', 'summoning'),
    ('Summoning - Vote', 'summoning'), ('Exotic Market', 'farming'), ('Palette', 'gaming'), ('Spelunking', 'spelunking'),
    ('Button', 'the_button'), ('The Maw', 'research'), ('Jelly', 'research'), ('Nightmariner', 'menagerie'),
    ('Purple Chest Slugs', 'sushi_station'), ('Companion', 'companions'), ('Monument', 'monument'), ('Sticker', 'stickers'), ('Fractal', 'fractal')]


def routed(o):
    """owner -> lines for each artifact-odds source still at x1/+0."""
    import yaml
    si = yaml.safe_load(open(ROOT / 'model' / 'system_index.yaml'))
    si = si if isinstance(si, dict) else {x.get('system'): x for x in si}
    out = {}
    for src in o['odds_missing_multipliers'] + o['odds_missing_additive']:
        key = next((k for w, k in ROUTE if w in src), None)
        owners = (si.get(key) or {}).get('owners', []) if key else []
        owners = [w for w in owners if w.startswith('Autis')][:1] or ['Account-wide']
        for w in owners:
            out.setdefault(w, []).append(f"Sailing artifact odds: {src} is still {'x1' if src in o['odds_missing_multipliers'] else '+0%'} (Autisticles' artifact hunt)")
    return out


# ---- Sailing goal: raise artifact find (Zack 2026-11-26) ----
# Lv 400 for every boat costs 50x-14,000x the banked loot (Toolbox getBoatUpgradeCost), so boat levels
# are not the lever yet. Ranked multipliers still at x1, from Toolbox sailing.ts getBoatArtifactChance.
# (match text, gain, how to get it, reachable now?)
ODDS_GOAL = [
    ('Magni Pufferfin', '5x artifact find + 25x sailing loot', 'W7 pet companion (Companion Park: weekly free pull, Pet Crystals or trades; fan source DigitalTQ)', True),
    ('Glimbo', '2x artifact find (3x upgraded)', 'W7 pet companion, same Companion Park routes', True),
    ('Spelunking Discoveries', '1.02x per Spelunking discovery (35 now = 2.0x)', "Gaming superbit 'Artifacto Discoveries' (Autistastic), grows with the Spelunking goal", True),
    ('Purple Chest Slugs', '1.5x per copy', 'Summer event shop item 48, buy when the event is up', False),
    ('Nightmariner', 'up to ~2000x', 'needs Lv 600 boats + Menagerie rank 21 (1.59M Lumi); you are rank 5', False),
]
BOAT_400 = ("Undead Battalion (3x) needs boat Lv 400 plus Research grid 105; Lv 400 costs 50x+ your banked loot. "
            "Boat Discount (event shop 55, 30% off boat upgrades) is not owned, buy it when it rotates in.")


def goal_lines(o):
    miss = ' | '.join(o.get('odds_missing_multipliers', []) + o.get('odds_missing_additive', []))
    L = ["GOAL: raise artifact find so new tiers are reachable. Fill these in order:"]
    for i, (key, gain, how, now) in enumerate([g for g in ODDS_GOAL if not miss or g[0] in miss], 1):
        L.append(f"  {i}. {key}: {gain}. {how}{'' if now else ' (not reachable yet)'}")
    L.append("  Boat levels: " + BOAT_400)
    return L


def card_lines(o):
    """Daily lines for the Siege Breaker's Sailing block. Top move first."""
    L = goal_lines(o)
    mv = [m for m in o['moves'] if m['from'] != m['to']]
    L.append(f"Claim chests every time you're on. The pile holds 30 and fills in about {o['pile_fill_min']} minutes, and every chest is an artifact roll.")
    if mv:
        L.append(f"TOP: move {len(mv)} boats to the islands with the best odds for what's left to find:")
        for m in sorted(mv, key=lambda m: m['boat']):
            L.append(f"  Boat {m['boat']} (Captain {m['captain']}): {m['from']} -> {m['to']} ({m['pct_from']}% -> {m['pct_to']}% a chest)")
    for w in o['speed_swaps']:
        L.append(f"  Swap Captain {w['captain']} onto Boat {w['to_boat']} (Captain {w['other']} goes to Boat {w['from_boat']}). That cuts the World's End trip to about {w['we_trip_h']}h.")
    if o['we_boats']: L.append(f"{' and '.join('Boat ' + k for k in o['we_boats'])} go to World's End to hunt the ones you've never found.")
    und = [a['name'] for a in o['artifacts'] if a['acq'] == 0]
    if und: L.append(f"Never found: {', '.join(und)}. Four of them are in The Maw, which opens from the Research grid node The Maw (not clouds).")
    try:
        pm = json.load(open(ROOT / 'model' / 'divinity.json')).get('purrmep_shown') or []
    except Exception:
        pm = []
    if pm: L.append(f"Check in game that {pm[0][0]} is linked to Purrmep in Divinity (boat speed). Toolbox says yes, AutoReview says no.")
    L.append("When the Sailing Speed ballot is up, World's End trips take half as long.")
    L += daily_checks(o)
    return L


# ---- Daily captain / trade / boat-upgrade checks (Zack 2026-11-21) ----
CLOUDS_DONE = True   # Zack 2026-11-21: every cloud is discovered, so Cloud Discover Rate is a dead stat
DEAD = {'Cloud Discover Rate'} if CLOUDS_DONE else set()


def _live(buffs):
    """per-level total of the stats that still do something"""
    return sum(p for n, p in buffs if n not in DEAD)


def daily_checks(o):
    L = []
    caps = o.get('_caps') or {}
    shop = o.get('_shop') or []
    plan_to = {m['boat']: m['to'] for m in o.get('moves', [])}
    stale = False   # data comes from this save's parse now (Zack 2026-11-25)
    if stale: L.append("Sailing page didn't refresh on the last read, so the captain shop below is old (it resets daily). Check the shop in game before buying.")
    if caps and shop:
        own = sorted(((_live([(n, p) for n, _, p in v['buffs']]), c, v) for c, v in caps.items()), key=lambda r: r[0])
        used = set()
        for s in sorted(shop, key=lambda s: -_live(s['buffs'])):
            sv = _live(s['buffs'])
            types = {n for n, _ in s['buffs'] if n not in DEAD}
            same = [(lv, c, v) for lv, c, v in own if c not in used and types & {n for n, _, _ in v['buffs']}]
            weak = (same or [(lv, c, v) for lv, c, v in own if c not in used] or [None])[0]   # like-for-like first (Zack 2026-11-21)
            if not weak or sv < weak[0] * 1.5: continue   # my read: only worth a level-1 restart at 1.5x the per-level stats
            lv, c, v = weak; used.add(c)
            stats = ' and '.join(f"{n} +{p}%" for n, p in s['buffs'])
            old = ' and '.join(f"{n} +{p}%" for n, _, p in v['buffs'])
            dest = plan_to.get(v['boat']) or next((b['now'] for b in o.get('boats', []) if b['boat'] == v['boat']), 'its island')
            cost = f" for {s['cost']} gold bars" if s.get('cost') else ''
            L.append(f"Captains: buy the shop captain with {stats} per level{cost}. It replaces Captain {c} ({old} per level) on Boat {v['boat']}. "
                     f"Send Boat {v['boat']} home, take {c} off, delete {c}, put the new one on, send Boat {v['boat']} to {dest}. "
                     f"Griffy: replace low base-roll captains, the stronger roll passes them at equal levels; keep captains equal to boats.")
        if not any(x.startswith('Captains:') for x in L):
            L.append("Captains: nothing in today's shop beats your weakest captain by enough to restart at level 1 (Griffy: replace only for stronger base rolls).")
    tr = o.get('_trades') or []
    if tr:
        best = sorted(tr, key=lambda r: -r['ratio'])[:3]
        L.append("Trades: best upcoming gold bar trades: " + '; '.join(f"{r['when']} give {r['give']} get {r['get']}" for r in best) + ". (Griffy: trade treasures for gold bars to upgrade boats)")
    ups = [b for b in o.get('boats', []) if b.get('speed_buy') or b.get('loot_buy')]
    if ups:
        we = set(o.get('we_boats') or {})
        lines = []
        for b in ups:
            if str(b['boat']) in we and b.get('speed_buy'): lines.append(f"Boat {b['boat']} speed to {b['speed_buy'][0]} (World's End boat, speed first)")
            elif b.get('loot_buy'): lines.append(f"Boat {b['boat']} loot to {b['loot_buy'][0]}")
        if lines: L.append("Boat upgrades you can afford now: " + '; '.join(lines[:6]) + ". (my read: speed on World's End boats, loot elsewhere)")
    return L



