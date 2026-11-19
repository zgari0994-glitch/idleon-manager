"""Tesseract planner (Autistocat, Arcanist). Tachyon balances, next unlock, AutoReview account-wide targets, optimizer, best maps per tachyon."""
import re
from tbhelp import tb, ar_items, n, save
from compass import upgrades
from spend import h
TACH = ['Purple', 'Brown', 'Green', 'Red', 'Silver', 'Gold']


def build():
    T = tb('tesseract'); u = T['Upgrades']['text']
    bal = {d: n(v) for d, v in re.findall(r'\n(' + '|'.join(TACH) + r')\n([\d.,]+[KMBTQ]?)(?=\n)', u)}
    top = re.search(r'Total levels\n([\d,]+)', u); nx = re.search(r'Next upgrade\n([^\n]+)\nAt ([\d,]+) total levels', u)
    ups = upgrades(u[u.find('Filters'):], TACH, bal)
    opt = T['Upgrade Optimizer']['text']; i = opt.find('Recommended')
    optl = re.findall(r'\n([A-Z][^\n]+)\nLv (\d+) → (\d+)\n(?:x\d+\n)?Damage\n([^\n]+)\n(?:Total cost|Cost)\n([^\n]+)\n([^\n]+)', opt[i:])
    M = T['Maps']['text']
    maps = re.findall(r'\n([A-Z][^\n]+)\nTachyons per drop\n[^\n]+\nWith Extra tachyon\n([^\n]+)', M)
    tier, items = ar_items('The Tesseract')
    return save('tesseract', {'balance': bal, 'total': int(top.group(1).replace(',', '')) if top else None, 'next': (nx.group(1), int(nx.group(2).replace(',', ''))) if nx else None,
                              'upgrades': ups, 'optimizer': optl, 'maps': [(a, n(b)) for a, b in maps], 'ar_tier': tier, 'ar': items})


def card_lines(o):
    L, bal = [], o['balance']
    if o['next']: L.append(f"Next unlock: {o['next'][0]} at {o['next'][1]} total levels ({o['total']} now, {o['next'][1] - o['total']} to go).")
    aff = sorted([u for u in o['upgrades'] if u['cost'] and u['currency'] and not u['maxed'] and u['cost'] <= bal.get(u['currency'], 0)], key=lambda u: u['cost'])
    if aff: L.append(f"TOP: {len(aff)} upgrades affordable now, cheapest: " + ', '.join(f"{u['name']} {u['lv']}->{u['lv'] + 1} {h(u['cost'])} {u['currency']}" for u in aff[:6]) + ' (each counts toward the next unlock).')
    acc = [i for i in o['ar'] if i['group'].startswith('Level up the following')]
    first = {}
    for i in acc: first.setdefault(i['label'], i)
    if first:
        by = {u['name']: u for u in o['upgrades']}
        L.append(f"AutoReview (tier {o['ar_tier']}): " + ', '.join(f"{k} {i['cur']} -> {i['goal']}" + (f" ({h(by[k]['cost'])} {by[k]['currency'] or 'of a tachyon you hold 0 of'})" if by.get(k, {}).get('cost') else ' (locked)') for k, i in first.items()))
    L.append('Tachyons: ' + ', '.join(f"{k} {h(v)}" for k, v in bal.items()) + '.')
    zero = [k for k, v in bal.items() if not v]
    if zero: L.append(f"No {', '.join(zero)} tachyons yet: those come from later-world maps (Toolbox Maps tab shows per-map drops; colour per map not in the page text, GAP).")
    if o['optimizer']: L.append('Toolbox optimizer: ' + '; '.join(f"{a} {b}->{c} {d} for {e} ({f})" for a, b, c, d, e, f in o['optimizer'][:2]))
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
