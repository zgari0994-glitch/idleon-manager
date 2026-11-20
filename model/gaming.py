"""Gaming planner (Autistastic). Garden full / visit gaps, acorn shop buys, snail (AutoReview mail plan), superbits."""
import re
from tbhelp import tb, ar_items, n, save


def build():
    T = tb('gaming'); t = T['Imports']['text']
    spr = re.search(r'Sprouts\n(\d+) / (\d+)', t); bits = re.search(r'Bits\n([^\n]+)', t)
    since = [(k, re.search(k + r'.*?Since last (?:dig|visit)\n([^\n]+)', t, re.S).group(1)) for k in ('Dirty Shovel', 'Autumn Squirrel') if re.search(k + r'.*?Since last', t, re.S)]
    acorns = re.search(r'\nAcorns\n(\d+)', t)
    shop = [(a, int(b), int(c)) for a, b, c in re.findall(r'\n([A-Z][^\n]+)\nLv (\d+)\n\t(\d+)', t)]
    snail = re.search(r'SNAIL\nLevel\n(\d+)\nMax level\n(\d+)\nEncouragement\n(\d+)\nSuccess chance\n([^\n]+)\nReset chance\n([^\n]+)', t)
    sb = T['Superbits']['text']
    owned = sb.count('\nOwned\n')
    tier, items = ar_items('Gaming')
    return save('gaming', {'sprouts': spr.groups() if spr else None, 'bits': bits.group(1) if bits else None, 'since': since, 'acorns': int(acorns.group(1)) if acorns else 0,
                           'shop': shop, 'snail': snail.groups() if snail else None, 'superbits_owned': owned, 'ar': items})


def card_lines(o):
    L = []
    if o['sprouts'] and o['sprouts'][0] == o['sprouts'][1]: L.append("TOP: the garden is full, harvest it. Nothing new grows until you do.")
    if o['since']: L.append(f"Dig with the shovel and collect the squirrel's acorns, neither has been touched in {o['since'][0][1]}.")
    buy = [s for s in o['shop'] if s[2] <= o['acorns']]
    if buy: L.append(f"Acorn shop: buy {', '.join(re.sub(r'^(Boosts |All plants )', '', re.sub(r' by \+?[\d.]+%$', '', a)).strip() for a, b, c in buy)} ({o['acorns']} acorns).")
    if o['snail']: L.append(f"Snail is level {o['snail'][0]} of {o['snail'][1]}. AutoReview's mail plan is on this card.")
    L.append('Spelunking cave Sedimeadow (Autistomatic) adds a second page of superbits.')
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
