"""Breeding planner: upgrade buys ranked for DNA efficiency, territory spice -> Cooking, eggs, shiny targets, Menagerie prereqs
-> Autistacular's Breeding block.

Inputs: data.py (Toolbox parser), review.json.gz (AutoReview Breeding).
GAP: Mobs tab was read with a filter on (fence only); per-pet shiny levels come from AutoReview until the reader clears filters.
"""
import gzip, json, re
from pathlib import Path
import spend

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / 'snapshots' / (ROOT / 'snapshots' / 'LATEST').read_text().strip()
# priority weights from sources: Pulse 2026-10 "priority one is faster shinies, then meal bonuses"; AutoReview Blooming Axe 2->10 (pet damage)
NOSTAT = {'Shattershell Iteration', 'Gene Splicing', 'Overwhelmed Golden Egg', 'Failsafe Restitution Cloud', 'Rarity of the Egg'}   # chance/cost effects, not a stat %
WEIGHT = {'Grand Martial of Shinytown': 3, 'Paint Bucket': 1.5, 'Blooming Axe': 2, 'Breedability Mobs': 1.5}
NOTE = {'Grand Martial of Shinytown': 'Pulse 2026-10: faster shinies is priority one', 'Blooming Axe': 'AutoReview: 2 -> 10 for pet damage',
        'Breedability Mobs': 'Heart VII pets 0/68 (AutoReview)', 'Gene Splicing': 'only helps unlock new mob types',
        'Overwhelmed Golden Egg': 'new mob chance only', 'Failsafe Restitution Cloud': 'new/shiny mob chance'}


def _n(s):
    s = s.replace(',', '').strip()
    m = re.match(r'([\d.]+)(?:e\+?(\d+))?\s*(QQ|Q|[KMBT])?$', s)
    if not m: return None
    v = float(m.group(1)) * (10 ** int(m.group(2)) if m.group(2) else 1)
    return v * {None: 1, 'K': 1e3, 'M': 1e6, 'B': 1e9, 'T': 1e12, 'Q': 1e15, 'QQ': 1e18}[m.group(3)]


def build():
    # Zack 2026-11-25: Toolbox parser numbers (model/data.py); costs = Toolbox page formulas (BreedingUpgrades.jsx)
    from data import load
    B = load().system('breeding')
    dna = B['deadCells']; ups, opts = [], []
    for u in B['petUpgrades']:
        name = str(u['name']).split('}')[0].replace('_', ' ').strip()
        if not name or name == 'No Upgrade Selected' or name == 'Filler': continue
        lv, mx = u['level'], u['maxLevel']
        cell = u['baseMatCost'] * (1 + lv) * u['costMatScale'] ** lv
        food = u['baseCost'] * (1 + lv) * u['costScale'] ** lv
        eff = str(u.get('boostEffect', '')).replace('_', ' ')
        ups.append({'name': name, 'lv': lv, 'max': mx, 'maxed': lv >= mx, 'effect': eff, 'have': dna, 'cost': cell, 'meal_cost': food})
        if lv >= mx: continue
        opts.append({'item': f"{name} {lv}/{mx}", 'currency': 'DNA', 'balance': dna, 'cost': cell, 'gain_pct': None,
                     'stat': eff, 'weight': WEIGHT.get(name, 1), 'note': NOTE.get(name, '')})
    ranked = spend.rank(opts)['DNA'] if opts else []
    terr = []
    eggs = (sum(1 for e in B['eggs'] if e), int(B['eggCapacity']))
    tpe = f"{B['timeToNextEgg'] / 3600:.1f}h" if B.get('timeToNextEgg') else None
    fence = None
    wave = B.get('maxArenaLevel')
    # AutoReview shiny targets: fastest days-to-level per bonus
    r = json.load(gzip.open(SNAP / 'review.json.gz')); shiny = []
    for w in r['worlds']:
        for s in (w.get('sections') or []):
            if s.get('name') != 'Breeding': continue
            for gp in s['groups']:
                if not gp['name'].startswith('Level Shinies'): continue
                for it in gp['items']:
                    for x in it.get('items', []):
                        m = re.match(r'(.+?): (.+?)([\d,.]+) base days to level', x['label'])
                        if m: shiny.append({'bonus': m.group(1), 'pet': m.group(2), 'days': float(m.group(3).replace(',', '')), 'cur': x['cur'], 'goal': x['goal'], 'tier': it.get('tab', '')})
    shiny.sort(key=lambda x: x['days'])
    out = {'snapshot': SNAP.name, 'upgrades': ups, 'rank': ranked, 'territory': terr, 'eggs': eggs, 'dna': dna,
           'time_per_egg': tpe, 'fence': fence, 'wave': wave, 'shiny_targets': shiny}
    json.dump(out, open(ROOT / 'model' / 'breeding.json', 'w'), indent=1)
    return out


def card_lines(o):
    L = []
    # Zack 2026-11-21: sourced order beats my gain-per-cost math. Faster shinies first (Pulse: priority one), never a weighted pick ahead of it.
    SOURCED = ['Grand Martial of Shinytown']
    rk = [x for x in o['rank'] if x['afford']]
    rk = sorted(rk, key=lambda x: (0 if any(x['item'].startswith(s) for s in SOURCED) else 1))
    if rk: L.append(f"TOP: spend Dead DNA on Grand Martial of Shinytown first (faster shiny levels; Pulse: faster shinies are priority one), then {', '.join(x['item'].split(' ')[0] + ' ' + x['item'].split(' ')[1] for x in rk[1:3] if not x['item'].startswith('Grand'))}. Dead DNA comes from trashing pets (2 to 6 each, idleon.wiki), so trash every egg you don't keep.")
    claim = sum(t['claim'] for t in o['territory'])
    if claim: L.append(f"Claim {claim:,} territory spice. It pays for kitchen upgrades on Autiszemo.")
    if o['eggs'] and o['eggs'][0] == o['eggs'][1]: L.append('Eggs are full. Pulse: keep clicking them past full to level them.')
    if o['fence']:
        n, lv, mx, cnt, days, nxt = o['fence']
        L.append(f"Fence: {n} at shiny level {lv} of {mx}, next level in {nxt}. Stick to one type at a time.")
    if o['shiny_targets']: L.append('Quickest shiny goals: ' + ', '.join(f"{x['pet']} for {x['bonus'].lower()}" for x in o['shiny_targets'][:3]) + '.')
    L.append("Zack's plan (2026-11-21): while pushing Dead DNA, hatch and trash as many eggs as possible (no multiplying focus). One shiny spot is given up to raise breedability on one pet at a time toward heart 7 (Equinox and other places need a set number of heart 7 pets). Card switches to the next pet when one reaches heart 7.")
    L.append('The Crucible (big cooking speed) opens through the Menagerie on Autisticles.')
    return L


def routed(o):
    return {'Autisticles': ['Breeding (Tacular): Luminous Menagerie unlocks the Crucible (10x/20x cooking speed waves) and Shiny OverLVs (unlock 12)']}


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)
