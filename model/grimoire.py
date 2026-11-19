"""Grimoire planner (Autiszemo, Death Bringer). Toolbox Grimoire page: upgrades + bone costs, optimizer, next unlock, bone mobs.
AutoReview targets (account-wide upgrades) first, optimizer damage buys, levels to next unlock, cross-system upgrades routed."""
import json, re
from pathlib import Path
from spend import h
from compass import _n, _ar, upgrades

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / 'snapshots' / (ROOT / 'snapshots' / 'LATEST').read_text().strip()
BONES = ['Femur', 'Ribcage', 'Cranium', 'Bovinae']
CROSS = {'Ribbon Winning': 'Cooking (meal ribbons)', 'Supreme Head Chef Status': 'Cooking', 'Land Rank Database Maxim': 'Farming (land rank)',
         'Superior Crop Research': 'Farming', 'Sacrifice of Harvest': 'Farming', 'Pure Opals': 'The Hole (villager opals)',
         'Villager Extraciricular': 'The Hole (villagers)', 'Grey Tome Book': 'Talents', 'Talents for Me, not for Thee': 'Talents'}
HOLE_OWNER = 'Autistabish'


def build():
    T = json.load(open(SNAP / 'toolbox' / 'grimoire.json'))['tabs']
    up = T['Upgrades']['text']
    bal = {d: _n(v) for d, v in re.findall(r'\n(' + '|'.join(BONES) + r')\n([\d.,]+[KMBTQ]?)(?=\n)', up)}
    ups = upgrades(up[up.find('Filters'):], BONES, bal)
    by = {u['name']: u for u in ups}
    top = re.search(r'Total levels\n([\d,]+)', up); nxt = re.search(r'Next upgrade\n([^\n]+)\nAt ([\d,]+) total levels', up)
    ar = _ar('The Grimoire'); targets = []
    for g in (ar or {}).get('groups', []):
        for tab in g.get('items', []):
            if not tab.get('tab', '').startswith('To reach Tier'): continue
            for it in tab['items']: targets.append({'tab': tab['tab'], 'name': it['label'], 'cur': it['cur'], 'goal': it['goal'], 'up': by.get(it['label'])})
    opt = T['Upgrade Optimizer']['text']; i = opt.find('Recommended upgrade sequence')
    optl = [(a, b, c, d, e, f) for a, b, c, d, e, f in re.findall(r'\n([A-Z][^\n]+)\nLv (\d+) → (\d+)[^\n]*\n(?:x\d+\n)?Damage\n([^\n]+)\n(?:Total cost|Cost)\n([^\n]+)\n([^\n]+)', opt[i:])]
    M = T['Monsters']['text']
    mobs = sorted([(a, b, _n(c)) for a, b, c in re.findall(r'\n([A-Z][^\n]+)\n([^\n]+)\nBones per drop\n[^\n]+\nWith Extra bones\n([^\n]+)', M)], key=lambda x: -x[2])
    out = {'snapshot': SNAP.name, 'balance': bal, 'total': int(top.group(1).replace(',', '')) if top else None,
           'next_unlock': (nxt.group(1), int(nxt.group(2).replace(',', ''))) if nxt else None, 'upgrades': ups, 'targets': targets,
           'optimizer': optl, 'best_mobs': mobs[:5], 'ar_tier': (ar or {}).get('tier')}
    json.dump(out, open(ROOT / 'model' / 'grimoire.json', 'w'), indent=1)
    return out


def card_lines(o):
    L, bal = [], o['balance']
    ready = [x for x in o['optimizer'] if 'ready now' in x[5]]
    if ready: L.append('TOP: buy now (Toolbox optimizer, damage): ' + '; '.join(f"{a} {b} -> {c} for {e} ({d})" for a, b, c, d, e, f in ready))
    cheap = [t for t in o['targets'] if t['up'] and t['up'].get('cost') and t['up'].get('currency') and t['up']['cost'] <= 0.02 * bal.get(t['up']['currency'], 0)]
    if cheap: L.append('Cheap AutoReview targets (under 2% of balance, buy now): ' + ', '.join(dict.fromkeys(sorted({f"{t['name']} {t['cur']} -> {t['goal']} ({h(t['up']['cost'])} {t['up']['currency']} next level)" + (f" [{CROSS[t['name']]}]" if t['name'] in CROSS else '') for t in cheap if t['goal'] == min(x['goal'] for x in cheap if x['name'] == t['name'])}))))
    if o['next_unlock']:
        nm, at = o['next_unlock']; left = at - o['total']
        cheap = sorted([u['cost'] for u in o['upgrades'] if u['cost'] and u['currency'] == 'Femur' and not u['maxed']])
        L.append(f"Next unlock: {nm} at {at:,} total levels ({o['total']:,} now, {left} to go). Cheapest Femur levels run {h(cheap[0])} to {h(cheap[min(len(cheap) - 1, 9)])}; Femur {h(bal.get('Femur'))} held.")
    tabs = sorted({t['tab'] for t in o['targets']})
    for tab in tabs[:2]:
        items = [t for t in o['targets'] if t['tab'] == tab]
        L.append(f"AutoReview {tab} (now {o['ar_tier']}): " + '; '.join(
            f"{t['name']} {t['cur']} -> {t['goal']}" + (f" ({h(t['up']['cost'])} {t['up']['currency']})" if t['up'] and t['up'].get('cost') else '')
            + (f" [{CROSS[t['name']]}]" if t['name'] in CROSS else '') for t in items))
    cross = [u for u in o['upgrades'] if u['name'] in CROSS and not u['maxed'] and u['cost']]
    if cross: L.append('Feeds other systems: ' + ', '.join(f"{u['name']} Lv {u['lv']}{'/' + str(u['max']) if u['max'] else ''} -> {CROSS[u['name']]} ({h(u['cost'])} {u['currency']})" for u in cross))
    if o['best_mobs']: L.append('Most bones per drop: ' + ', '.join(f"{a} ({b}) {h(c)}" for a, b, c in o['best_mobs'][:3]) + ' (AFK spot pick vs his Death Note targets).')
    L.append("Griffy 2026-10: max AFK gains before spending bones; damage + accuracy first (AFK Info shows if accuracy hits the target). Griffy 2026-08: Yummy Peach Ring is one of the first ribbons to rank 20.")
    return L


def routed(o):
    u = next((u for u in o['upgrades'] if u['name'] == 'Pure Opals'), None)
    if not u or u['maxed']: return {}
    return {HOLE_OWNER: [f"Hole opals (Zemo's Grimoire): Pure Opals Lv {u['lv']}/{u['max']}, next {h(u['cost'])} {u['currency']}. AutoReview wants 15 for Grimoire tier 4."]}


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)
    print(routed(o))
