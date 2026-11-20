"""Spelunking planner (Autistomatic). Cave bonuses gate other systems (routed to their owners), amber, optimizer buys, page reads."""
import re
from tbhelp import tb, ar_items, n, save

ROUTE = {'Superbits': ('Autistastic', 'Gaming'), 'Cards': ('Autistronaut', 'Cards'), 'Exotic Market': ('Autiszemo', 'Farming'), 'Teal Summoning': ('Autistocat', 'Summoning'),
         'Cooking Meals': ('Autiszemo', 'Cooking'), 'Sigils': ('Autistocat', 'Sigils')}


def build():
    T = tb('spelunking'); u = T['Upgrades']['text']
    g = lambda k: (re.search(k + r'\n([^\n]+)', u) or [None, None])[1]
    opt = T['Upgrade Optimizer']['text']
    seq = re.findall(r'\n([A-Z][^\n]+)\nLv (\d+) → (\d+)[^\n]*\nPower\n([^\n]+)\nCost\n([\d,.]+[KMB]?)', opt)
    tier, items = ar_items('Spelunking')
    caves = [{'cave': i['label'].split(':')[0], 'bonus': i['label'].split(':', 1)[1] if ':' in i['label'] else '', 'done': i.get('goal') == '✔' or i.get('cur') == i.get('goal')}
             for i in items if i['group'] == 'Cave Bonuses']
    return save('spelunking', {'amber': n(g('Amber Found')), 'pages': g('Daily Page Reads'), 'disc': g('Discoveries'), 'power': g('Power'), 'optimizer': seq, 'caves': caves})


def card_lines(o):
    L = []
    nxt = [c for c in o['caves'] if not c['done']]
    if nxt: L.append(f"TOP (need outweighs math: gates 6 systems): next caves " + '; '.join(f"{c['cave']}: {c['bonus'][:70]}" for c in nxt[:6]))
    if o['pages']: L.append(f"Daily page reads {o['pages']}: read the rest today.")
    if o['optimizer']:
        a = o['amber']; aff = [s for s in o['optimizer'] if n(s[4]) <= a]
        L.append(f"Amber {a:,.0f}. Optimizer next: {o['optimizer'][0][0]} {o['optimizer'][0][1]}->{o['optimizer'][0][2]} for {o['optimizer'][0][4]} ({o['optimizer'][0][3]} POW)" + (' , affordable' if aff else f", short {n(o['optimizer'][0][4]) - a:,.0f}"))
    L.append(f"Power {o['power']}, discoveries {o['disc']}.")
    return L


def routed(o):
    out = {}
    for c in o['caves']:
        if c['done']: continue
        for k, (who, sysname) in ROUTE.items():
            if k.lower() in c['bonus'].lower(): out.setdefault(who, []).append(f"{sysname} gated by Spelunking cave {c['cave']} (Autistomatic): {c['bonus'][:80]}")
    return out


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)
    print(routed(o))
