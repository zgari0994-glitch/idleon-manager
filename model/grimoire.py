"""Grimoire planner (Autiszemo, Death Bringer). Toolbox Grimoire page: upgrades + bone costs, optimizer, next unlock, bone mobs.
AutoReview targets (account-wide upgrades) first, optimizer damage buys, levels to next unlock, cross-system upgrades routed."""
import json, re
from pathlib import Path
from spend import h
from compass import from_parsed, _n, _ar, upgrades

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / 'snapshots' / (ROOT / 'snapshots' / 'LATEST').read_text().strip()
BONES = ['Femur', 'Ribcage', 'Cranium', 'Bovinae']
CROSS = {'Ribbon Winning': 'Cooking (meal ribbons)', 'Supreme Head Chef Status': 'Cooking', 'Land Rank Database Maxim': 'Farming (land rank)',
         'Superior Crop Research': 'Farming', 'Sacrifice of Harvest': 'Farming', 'Pure Opals': 'The Hole (villager opals)',
         'Villager Extraciricular': 'The Hole (villagers)', 'Grey Tome Book': 'Talents', 'Talents for Me, not for Thee': 'Talents'}
HOLE_OWNER = 'Autistabish'


def build():
    from data import load
    Gm = load().system('grimoire')
    bal = {BONES[i]: v for i, v in enumerate(Gm['bones']) if i < len(BONES)}
    ups = from_parsed(Gm['upgrades'], BONES, bal, 'boneType')
    by = {u['name']: u for u in ups}
    nu = Gm.get('nextUnlock') or {}
    ar = _ar('The Grimoire'); targets = []
    for g in (ar or {}).get('groups', []):
        for tab in g.get('items', []):
            if not tab.get('tab', '').startswith('To reach Tier'): continue
            for it in tab['items']: targets.append({'tab': tab['tab'], 'name': it['label'], 'cur': it['cur'], 'goal': it['goal'], 'up': by.get(it['label'])})
    out = {'snapshot': SNAP.name, 'balance': bal, 'total': Gm['totalUpgradeLevels'],
           'next_unlock': (nu['name'].replace('_', ' '), nu.get('unlockLevel')) if nu.get('name') else None, 'upgrades': ups, 'targets': targets,
           'optimizer': [], 'best_mobs': [], 'ar_tier': (ar or {}).get('tier')}
    json.dump(out, open(ROOT / 'model' / 'grimoire.json', 'w'), indent=1)
    return out


def card_lines(o):
    L, bal = [], o['balance']
    ready = [x for x in o['optimizer'] if 'ready now' in x[5]]
    if ready: L.append('TOP: buy ' + ' and '.join(f"{a} ({e} Femur)" for a, b, c, d, e, f in ready) + '. Toolbox ranks them as the best damage per bone.')
    if o['next_unlock']:
        nm, at = o['next_unlock']
        L.append(f"{at - o['total']} more upgrade levels unlock {nm}. Cheap Wraith levels are the fastest way there.")
    cheap = {t['name']: t for t in o['targets'] if t['up'] and t['up'].get('cost') and t['up'].get('currency') and t['up']['cost'] <= 0.02 * bal.get(t['up']['currency'], 0)}
    if cheap: L.append('Cheap and on AutoReview\'s list: ' + ', '.join(f"{k} ({h(v['up']['cost'])} {v['up']['currency']})" for k, v in cheap.items()) + '.')
    cross = [u for u in o['upgrades'] if u['name'] in CROSS and not u['maxed'] and u['cost']]
    if cross: L.append('These also help other systems: ' + ', '.join(f"{u['name']} for {CROSS[u['name']].split(' (')[0]}" for u in cross[:5]) + '.')
    if o['best_mobs']: L.append(f"Most bones per kill: {o['best_mobs'][0][0]} at {o['best_mobs'][0][1]}.")
    L.append('Griffy: max out AFK gains before spending bones, and keep accuracy high enough to hit.')
    return L


def routed(o):
    u = next((u for u in o['upgrades'] if u['name'] == 'Pure Opals'), None)
    if not u or u['maxed']: return {}
    return {HOLE_OWNER: [f"Hole opals (Zemo's Grimoire): Pure Opals Lv {u['lv']}/{u['max']}, next {h(u['cost'])} {u['currency']}. AutoReview wants 15 for Grimoire tier 4."]}


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)
    print(routed(o))
