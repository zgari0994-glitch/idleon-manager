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
    if nxt: L.append(f"TOP: Spelunking is the biggest thing holding the account back. The next caves unlock: " + '; '.join(c['bonus'].split('!')[0][:60] for c in nxt[:4]) + '.')
    if o['pages']: L.append(f"Read the rest of today's pages ({o['pages']} used).")
    if o['optimizer']:
        a = o['amber']; s = o['optimizer'][0]; c = n(s[4])
        L.append(f"Next buy: {s[0]} for {s[4]} amber" + (" (you can afford it)." if c <= a else f", you have {a:,.0f}."))
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
