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
    if o['sprouts'] and o['sprouts'][0] == o['sprouts'][1]: L.append(f"TOP: garden full ({o['sprouts'][0]}/{o['sprouts'][1]} sprouts): harvest, nothing grows while full.")
    if o['since']: L.append('Not visited: ' + ', '.join(f"{a} {b}" for a, b in o['since']) + ' (dig with the shovel, collect squirrel acorns).')
    buy = [s for s in o['shop'] if s[2] <= o['acorns']]
    L.append(f"Acorn shop ({o['acorns']} acorns): " + ', '.join(f"{a} Lv {b} next {c}" + (' BUY' if (a, b, c) in buy else '') for a, b, c in o['shop']))
    if o['snail']:
        lv, mx, enc, ok, rs = o['snail']
        plan = [i for i in o['ar'] if i['group'] == 'Snail Ranks' and 'Step' in i['label']]
        L.append(f"Snail Lv {lv}/{mx}, encouragement {enc}, success {ok}, reset {rs}. AutoReview steps: " + ' | '.join(i['label'][:80] for i in plan[:4]))
    L.append(f"Superbits owned {o['superbits_owned']}. Isotope Discovery superbit (+10 atom max) is a target on this card. Spelunking Sedimeadow cave adds superbits page 2.")
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
