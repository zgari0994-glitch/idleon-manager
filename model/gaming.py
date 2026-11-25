"""Gaming planner (Autistastic). Garden full / visit gaps, acorn shop buys, snail (AutoReview mail plan), superbits."""
import re
from tbhelp import tb, ar_items, n, save


def build():
    # Zack 2026-11-25: Toolbox parser numbers (model/data.py)
    from data import load
    G = load().system('gaming')
    hrs = lambda s: f"{s / 3600:.0f}h" if s < 172800 else f"{s / 86400:.0f}d"
    since = [('Dirty Shovel', hrs(G['lastShovelClicked'])), ('Autumn Squirrel', hrs(G['lastAcornClicked']))]
    sb = G['superbitsUpgrades']
    owned = [s for s in sb if s.get('unlocked')]
    nxt = sorted([s for s in sb if not s.get('unlocked')], key=lambda s: s['cost'])
    tier, items = ar_items('Gaming')
    return save('gaming', {'sprouts': (G['availableSprouts'], int(G['sproutsCapacity'])), 'bits': G['bits'], 'since': since, 'acorns': G['acorns'],
                           'shop': [], 'snail': (G['snailLevel'], G['snail']['maxLevel'], G.get('snailEncouragement'), G['snail']['successChance'], G['snail']['resetChance']),
                           'superbits_owned': len(owned), 'superbits_next': [(s['name'].replace('_', ' '), s['cost'], s['description'].replace('_', ' ')[:80]) for s in nxt[:4]],
                           'ar': items})

def card_lines(o):
    L = []
    if o['sprouts'] and o['sprouts'][0] == o['sprouts'][1]: L.append("TOP: the garden is full, harvest it. Nothing new grows until you do.")
    if o['since']: L.append(f"Dig with the shovel and collect the squirrel's acorns, neither has been touched in {o['since'][0][1]}.")
    buy = [s for s in o['shop'] if s[2] <= o['acorns']]
    if buy: L.append(f"Acorn shop: buy {', '.join(re.sub(r'^(Boosts |All plants )', '', re.sub(r' by \+?[\d.]+%$', '', a)).strip() for a, b, c in buy)} ({o['acorns']} acorns).")
    if o['snail']: L.append(f"Snail is level {o['snail'][0]} of {o['snail'][1]} ({o['snail'][3] * 100:.0f}% success, {o['snail'][4] * 100:.0f}% reset chance).")
    nx = o.get('superbits_next') or []
    if nx:
        s0 = nx[0]; L.append(f"Next superbit: {s0[0]} at {s0[1]:.1e} bits (you have {o['bits']:.1e})" + (' - buy it.' if s0[1] <= o['bits'] else '.'))
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
