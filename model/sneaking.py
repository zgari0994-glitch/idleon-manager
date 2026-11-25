"""Sneaking planner (Autistacular). Charm rolls left, affordable jade upgrades, floor gaps, gemstones (AutoReview)."""
import re
from tbhelp import tb, ar_items, n, save
from spend import h


def build():
    # Zack 2026-11-25: Toolbox parser numbers (model/data.py)
    from data import load
    D = load(); S = D.system('sneaking')
    jade = float(S['jadeCoins'])
    ups = [{'name': u['name'].replace('_', ' '), 'lv': u['level'], 'cost': u.get('cost') or u.get('nextLevelCost')} for u in S['upgrades'] if u.get('isUnlocked')]
    floors = [(D.characters[i]['name'] if i < len(D.characters) else f"#{i}", '', str(p.get('floor'))) for i, p in enumerate(S['players'])]
    tier, items = ar_items('Sneaking')
    return save('sneaking', {'jade': jade, 'rolls': (S['remainingSymbolRolls'], S['remainingPristineRolls']), 'hats': (S['hatsFound'], S['hatsTotal']),
                             'floors': floors, 'upgrades': ups, 'emporium': sorted([(e['name'].replace('_', ' '), e['cost']) for e in S['jadeEmporium'] if not e.get('unlocked')], key=lambda e: e[1])[:6],
                             'ar': items})

def card_lines(o):
    L = []
    if o['rolls'] and (o['rolls'][0] or o['rolls'][1]): L.append(f"TOP: use today's charm rolls ({o['rolls'][0]} symbol, {o['rolls'][1]} pristine left). They don't carry over.")
    aff = [u for u in o['upgrades'] if u['cost'] and o['jade'] and u['cost'] <= o['jade'] and u['lv'] > 0]
    if aff: L.append('You can afford these jade upgrades: ' + ', '.join(u['name'] for u in sorted(aff, key=lambda u: u['cost'])) + '.')
    new = [u['name'] for u in o['upgrades'] if u['cost'] and o['jade'] and u['cost'] <= o['jade'] and u['lv'] == 0]
    if new: L.append(f"These are cheap but still at level 0, check they're unlocked: {', '.join(new)}.")
    em = [e for e in o.get('emporium', []) if e[1] and e[1] <= o['jade']]
    if em: L.append('Jade Emporium buys you can afford: ' + ', '.join(e[0] for e in em) + ' (ninja upgrade costs are website-only, check in game).')
    top = max(int(f) for _, _, f in o['floors']) if o['floors'] else 0
    low = [c for c, _, f in o['floors'] if int(f) < top]
    if low: L.append(f"{', '.join(low)} {'is' if len(low) == 1 else 'are'} behind on floors (everyone else is on {top}).")
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
