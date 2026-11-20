"""Sneaking planner (Autistacular). Charm rolls left, affordable jade upgrades, floor gaps, gemstones (AutoReview)."""
import re
from tbhelp import tb, ar_items, n, save
from spend import h


def build():
    T = tb('sneaking'); inv = T['Inventory']['text']
    jade = re.search(r'Jade coins\n([^\n]+)', inv); rolls = re.search(r'Daily charm rolls used\n(\d+) / (\d+)', inv)
    hats = re.search(r'Hats found\n(\d+) / (\d+)', inv)
    floors = re.findall(r'\n(Autis\w+)\nLv (\d+) · Sneaking · Floor (\d+)', inv)
    up = T['Upgrades']['text']
    ups = [{'name': a, 'lv': int(b), 'cost': n(d)} for a, b, c, d in re.findall(r'\n([A-Z][^\n]+)\nLv (\d+)\n\n([^\n]+)\n\n[\d.e+]+\n/\n([\d.e+]+(?:QQ|Q|T|B|M|K)?)\n', up)]
    tier, items = ar_items('Sneaking')
    return save('sneaking', {'jade': n(jade.group(1)) if jade else None, 'rolls': rolls.groups() if rolls else None,
                             'hats': hats.groups() if hats else None, 'floors': floors, 'upgrades': ups, 'ar': items})


def card_lines(o):
    L = []
    if o['rolls'] and int(o['rolls'][0]) < int(o['rolls'][1]): L.append(f"TOP: charm rolls {o['rolls'][0]}/{o['rolls'][1]} used today: roll them (daily, lost at reset).")
    aff = [u for u in o['upgrades'] if u['cost'] and o['jade'] and u['cost'] <= o['jade']]
    if aff: L.append(f"Jade {o['jade']:.3g}. Affordable: " + ', '.join(f"{u['name']} Lv {u['lv']} ({u['cost']:.3g})" + (' [Lv 0: check it is unlocked]' if u['lv'] == 0 else '') for u in sorted(aff, key=lambda u: u['cost'])))
    top = max(int(f) for _, _, f in o['floors']) if o['floors'] else 0
    low = [(c, f) for c, _, f in o['floors'] if int(f) < top]
    if low: L.append(f"Floor gaps (others on {top}): " + ', '.join(f"{c} floor {f}" for c, f in low))
    if o['hats']: L.append(f"Hats {o['hats'][0]}/{o['hats'][1]}.")
    gem = [i for i in o['ar'] if i['group'].startswith('Percentage of Gemstone')]
    if gem: L.append('AutoReview gemstones: ' + ', '.join(f"{i['label'].split(':')[0]} {i['cur']}" for i in gem[:7]))
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
