"""Tesseract planner (Autistocat, Arcanist). Tachyon balances, next unlock, AutoReview account-wide targets, optimizer, best maps per tachyon."""
import re
from tbhelp import tb, ar_items, n, save
from compass import upgrades
from spend import h
TACH = ['Purple', 'Brown', 'Green', 'Red', 'Silver', 'Gold']


def build():
    # Zack 2026-11-25: numbers from Toolbox's own parser on the save (model/data.py), not page text
    from data import load
    t = load().system('tesseract')
    bal = {x['name']: x['value'] for x in t['tachyons']}
    total = t['totalUpgradeLevels']
    ups, nxt = [], None
    for u in t['upgrades']:
        name = u['name'].replace('_', ' ')
        cur = TACH[int(u.get('x3') or 0)] if str(u.get('x3', '')).isdigit() and int(u['x3']) < len(TACH) else None
        maxed = u['level'] >= (u.get('x4') or 999999)
        ups.append({'name': name, 'level': u['level'], 'cost': u.get('cost'), 'currency': cur, 'maxed': maxed, 'unlocked': u.get('unlocked'), 'unlock_at': u.get('x6')})
        if not u.get('unlocked') and (nxt is None or (u.get('x6') or 0) < nxt[1]):
            nxt = (name, u.get('x6') or 0)
    tier, items = ar_items('The Tesseract')
    return save('tesseract', {'balance': bal, 'total': total, 'next': nxt, 'upgrades': ups, 'optimizer': [], 'maps': [],
                              'crystal_charge': t.get('crystalChargeReq'), 'ar_tier': tier, 'ar': items})


def card_lines(o):
    L, bal = [], o['balance']
    aff = sorted([u for u in o['upgrades'] if u['cost'] and u['currency'] and u.get('unlocked', True) and not u['maxed'] and u['cost'] <= bal.get(u['currency'], 0)], key=lambda u: u['cost'])
    if aff: L.append(f"TOP: {len(aff)} Tesseract upgrades are affordable, cheapest first: " + ', '.join(u['name'] for u in aff[:5]) + '. Every level counts toward the next unlock.')
    if o['next']: L.append(f"{o['next'][1] - o['total']} more levels unlock {o['next'][0]}.")
    zero = [k for k, v in bal.items() if not v]
    acc = {}
    for i in o['ar']:
        if i['group'].startswith('Level up the following'): acc.setdefault(i['label'], i)
    if acc: L.append('AutoReview wants ' + ', '.join(acc) + (f", but they cost {'/'.join(zero)} tachyons you don't have yet." if zero else '.'))
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
