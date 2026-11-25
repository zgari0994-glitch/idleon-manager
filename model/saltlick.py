"""Salt Lick planner (Autistopher). Levels buyable now per upgrade (Toolbox 'Can buy now')."""
import re
from tbhelp import tb, ar_items, save

def build():
    # Zack 2026-11-25: Toolbox parser numbers (model/data.py); cost = floor(baseCost * increment^level) like Toolbox's page
    from data import load
    ups = []
    for u in load().system('saltlick'):
        lv, have, buy = u['level'], u.get('totalAmount') or 0, 0
        while lv + buy < u['maxLevel']:
            c = int(u['baseCost'] * u['increment'] ** (lv + buy))
            if c > have: break
            have -= c; buy += 1
        ups.append({'desc': u['desc'].replace('_', ' ').replace('{', str(round(u['baseBonus'] * lv, 2))), 'lv': lv, 'max': u['maxLevel'], 'buy': buy})
    tier, items = ar_items('Salt Lick')
    return save('saltlick', {'upgrades': ups, 'ar_tier': tier, 'ar': items})

def card_lines(o):
    buy = [u for u in o['upgrades'] if u['buy']]
    nm = lambda u: re.sub(r'^\+?[\d.]+%? ', '', re.split(r'\. ', u['desc'])[0]).split(' for ')[0][:40]
    L = ['TOP: buy Salt Lick levels: ' + ', '.join(f"{nm(u)} +{u['buy']}" for u in buy) + '.'] if buy else []
    left = [u for u in o['upgrades'] if u['lv'] < u['max']]
    if left: L.append('Still to max: ' + ', '.join(f"{nm(u)} {u['lv']}/{u['max']}" for u in left) + '.')
    return L


def refinery_line(o):
    u = next((u for u in o['upgrades'] if 'Refinery Speed' in u['desc']), None)
    return (f"Salt Lick Refinery Speed is {u['lv']}/{u['max']}" + (f", Autistopher can buy {u['buy']} more now" if u['buy'] else '')) if u else None


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)
    print(refinery_line(o))
