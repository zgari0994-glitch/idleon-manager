"""Sailing planner: artifacts, islands, boats, captains -> daily moves for the Siege Breaker.

Inputs (per snapshot):
  systems.json.gz  sailing (artifact forms, islands, captains, boats)  [AutoReview parse]
  toolbox/sail_detail.txt       Toolbox Boats and Captains tab (details on)
  toolbox/sail_breakdowns.json  Toolbox artifact odds / min travel / loot breakdowns + game constants
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
        if bu: shop.append({'buffs': [(n.strip(), int(v)) for n, v in bu]})
    for c in re.split(r'\n(?=Captain [A-Z]\n)', '\n' + cap_txt):
        m = re.match(r'\nCaptain ([A-Z])\nLv (\d+)(?: · Boat (\d+))?', c) or re.match(r'Captain ([A-Z])\nLv (\d+)(?: · Boat (\d+))?', c)
        if not m: continue
        bu = re.findall(r'([A-Za-z ]+)\n\+([\d,.]+)% \(\+(\d+)% per level\)', c)
        caps[m.group(1)] = {'captain': m.group(1), 'level': int(m.group(2)), 'boat': int(m.group(3)) if m.group(3) else None,
                            'buffs': [(n.strip(), float(v.replace(',', '')), int(p)) for n, v, p in bu]}
    return boats, caps, shop


def build():
    sy = json.load(gzip.open(SNAP / 'systems.json.gz'))['systems']['sailing']
    bd = json.load(open(SNAP / 'toolbox' / 'sail_breakdowns.json'))
    X = bd['server_vars']['AncientOddPerIsland']; Y = bd['server_vars']['AncientArtiPCT']
    boats, caps, shop = parse_toolbox((SNAP / 'toolbox' / 'sail_detail.txt').read_text())
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

    # ---- allocation: spread boats over islands with cheap targets so every claim pushes several artifacts
    CHEAP = 1500   # chests; above this a target is a later phase (needs more odds or speed)
    for r in rank:
        live = [a for a in isl[r['island']]['arts'] if a['denom']]
        r['n_chests'] = [round(a['denom'] / (k * base_odds)) for a in live]   # same order as r['targets']
        r['cheap'] = [n for n in r['n_chests'] if n <= CHEAP]
    md = sorted(b['min_dist'] for b in boats if b['speed'])
    cheap_isl = [r for r in rank if r['cheap'] and r['distance'] <= md[len(md) // 2]]   # reachable in min travel time by most boats
    nb = len(boats)
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
    for i in order:
        cand = [p for p in free if mdist[p['boat']] >= isl[i]['distance']] or free
        if not cand: break
        p = cand[0]; free.remove(p); p['go'] = i; moves.append(p)
    for p in plan:
        p['go_pct'] = round(100 * chance(odds_of(p['captain']), p.get('go', p['now']), k), 3)
    later = [{'island': r['island'], 'targets': [t for t, n in zip(r['targets'], r['n_chests']) if n > CHEAP]} for r in rank if any(n > CHEAP for n in r['n_chests'])]

    missing_multi = [n for n, v in bd['multipliers'].items() if v == 1]
    missing_add = [n for n, v in bd['additive_pct'].items() if v == 0]
    chests_per_h = len(boats) / min_t
    out = {'snapshot': SNAP.name, 'k_calibration': round(k, 4), 'min_travel_min': bd['min_travel_min'], 'base_odds': round(base_odds, 2),
           'odds_multi_group': round(multi, 2), 'additive_wo_captain': round(add_wo, 1), 'pile_fill_min': round(30 / chests_per_h * 60),
           'alloc': alloc, 'moves': [{'boat': p['boat'], 'captain': p['captain'], 'from': p['now'], 'to': p['go'], 'pct_from': p['now_pct'], 'pct_to': p['go_pct'], 'trip_from_h': round(p['trip_h'], 1)} for p in moves],
           'later': later, 'chests_per_hour': round(chests_per_h, 1),
           'islands': rank, 'boats': plan, 'captains': cap_rank, 'shop': shop_rank, 'artifacts': arts,
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


ROUTE = [  # odds source -> system keyword used to find its owner on the cards
    ('Killroy', 'Killroy'), ('Vial', 'Alchemy'), ('Tome', 'Tome'), ('Sneaking', 'Sneaking'), ('Summoning - Vote', 'Summoning'),
    ('Monument', 'Monument'), ('Exotic Market', 'Farming'), ('Palette', 'Gaming'), ('Spelunking', 'Spelunking'),
    ('Button', 'Button'), ('The Maw', 'Research'), ('Jelly', 'Research'), ('Nightmariner', 'Menagerie'),
    ('Purple Chest Slugs', 'Sushi'), ('Companion', 'Companions'), ('Sticker', 'Sticker'), ('Fractal', 'Fractal')]


def card_lines(o):
    """Daily lines for the Siege Breaker's Sailing block. Top move first."""
    L = []
    mv = o['moves']
    L.append(f"Claim chests every session: pile holds 30, 20 boats fill it in ~{o['pile_fill_min']} min (min travel {o['min_travel_min']} min). Every chest is an artifact roll.")
    if mv:
        L.append(f"MOVE {len(mv)} boats (best per-chest odds for the artifacts still cheap to finish):")
        for m in sorted(mv, key=lambda m: m['boat']):
            slow = f", trip {m['trip_from_h']}h -> {o['min_travel_min']} min" if m.get('trip_from_h', 0) > o['min_travel_min'] / 60 + .05 else ''
            L.append(f"  Boat {m['boat']} (Captain {m['captain']}): {m['from']} -> {m['to']} ({m['pct_from']}% -> {m['pct_to']}% per chest{slow})")
    keep = {i: n for i, n in o['alloc'].items()}
    L.append('Island targets now: ' + '; '.join(f"{r['island']} x{keep[r['island']]}: " + ', '.join(t.split(' (')[0] + f" 1/{n:,}" for t, n in zip(r['targets'], r['n_chests']) if n <= 1500)
                                                 for r in o['islands'] if r['island'] in keep))
    if o['later']:
        L.append('Later (too costly per chest right now): ' + '; '.join(f"{x['island']}: " + ', '.join(t.split(' (')[0] for t in x['targets'][:2]) for x in o['later'][:6]))
    und = [a['name'] for a in o['artifacts'] if a['acq'] == 0]
    L.append(f"Never found ({len(und)}): {', '.join(und)}. World's End trips take 5.6h+ (5B distance, best speed 888M); The Maw needs 200B and is locked. Speed is the gate there, not odds.")
    L.append(f"Artifact odds {o['base_odds']:,.0f}x (no captain). Sources still at x1: {', '.join(o['odds_missing_multipliers'][:12])}")
    afc = [c for c in o['captains'] if c['afc']]
    L.append('AFC captains: ' + ', '.join(f"{c['captain']} +{c['afc']:g}% (boat {c['boat']})" for c in afc) + f". Each +100% AFC = +{100 / (100 + o['additive_wo_captain']) * 100:.0f}% odds.")
    sh = [s for s in o['shop'] if s['afc_at_avg']]
    if sh: L.append('Shop captains with AFC: ' + '; '.join(' / '.join(f"{n} {v}%/lv" for n, v in s['buffs']) for s in sh) + ' (only worth it if a captain slot is free)')
    return L
