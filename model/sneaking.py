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
    if o['rolls'] and int(o['rolls'][0]) < int(o['rolls'][1]): L.append(f"TOP: use today's charm rolls ({o['rolls'][1]} left). They don't carry over.")
    aff = [u for u in o['upgrades'] if u['cost'] and o['jade'] and u['cost'] <= o['jade'] and u['lv'] > 0]
    if aff: L.append('You can afford these jade upgrades: ' + ', '.join(u['name'] for u in sorted(aff, key=lambda u: u['cost'])) + '.')
    new = [u['name'] for u in o['upgrades'] if u['cost'] and o['jade'] and u['cost'] <= o['jade'] and u['lv'] == 0]
    if new: L.append(f"These are cheap but still at level 0, check they're unlocked: {', '.join(new)}.")
    top = max(int(f) for _, _, f in o['floors']) if o['floors'] else 0
    low = [c for c, _, f in o['floors'] if int(f) < top]
    if low: L.append(f"{', '.join(low)} {'is' if len(low) == 1 else 'are'} behind on floors (everyone else is on {top}).")
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
