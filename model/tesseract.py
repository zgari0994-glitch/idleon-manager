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
    aff = sorted([u for u in o['upgrades'] if u['cost'] and u['currency'] and not u['maxed'] and u['cost'] <= bal.get(u['currency'], 0)], key=lambda u: u['cost'])
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
