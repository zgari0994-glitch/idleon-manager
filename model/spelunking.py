"""Spelunking planner (Autistomatic). Cave bonuses gate other systems (routed to their owners), amber, optimizer buys, page reads."""
import re
from tbhelp import tb, ar_items, n, save

ROUTE = {'Superbits': ('Autistastic', 'Gaming'), 'Cards': ('Autistronaut', 'Cards'), 'Exotic Market': ('Autiszemo', 'Farming'), 'Teal Summoning': ('Autistocat', 'Summoning'),
         'Cooking Meals': ('Autiszemo', 'Cooking'), 'Sigils': ('Autistocat', 'Sigils')}


# Sourced buy order (Zack 2026-11-21: shops get a sourced order; my math never above a sourced pick)
BUY_ORDER = [
    ('Discovering the POW', 'Griffy (Apr 2026): POW upgrades first; Toolbox optimizer top POW buy'),
    ('Amber on the Brain', 'Griffy: useful early upgrade'),
    ('Stamina Resurgence', 'Pulse (Sep 7): max the stamina column fast'),
    ('Big Time Stamina', 'Pulse (Sep 7): max the stamina column fast'),
    ('Overstim Meter', 'Pulse: one of the big three'),
    ('Uncanny Ability to Find Narrow Passages', 'Pulse: big rope source, caps early'),
    ('Rope Subsidy', 'Pulse: big three, after the early caps'),
    ('Jobs All Done', 'Pulse: big three, after the early caps'),
    ('Free Refills', 'Pulse: fantastic'),
]


def shop_levels(u):
    """name -> (lv, max, next_cost or None) from the Toolbox Upgrades tab text."""
    out = {}
    for m in re.finditer(r'\n([^\n]+)\nLv (\d+) / ([\d,]+)\n', u):
        rest = u[m.end():m.end() + 900]
        nxt = re.search(r'\n[\d,.]+\n/\n([\d,.]+[KMBTQe+\d]*)\nneed', rest)
        stop = re.search(r'\nLv \d+ / ', rest)
        if nxt and stop and nxt.start() > stop.start(): nxt = None
        out[m.group(1).strip()] = (int(m.group(2)), int(m.group(3).replace(',', '')), n(nxt.group(1)) if nxt else None)
    return out


def build():
    T = tb('spelunking'); u = T['Upgrades']['text']
    g = lambda k: (re.search(k + r'\n([^\n]+)', u) or [None, None])[1]
    opt = T['Upgrade Optimizer']['text']
    seq = re.findall(r'\n([A-Z][^\n]+)\nLv (\d+) → (\d+)[^\n]*\n(?:x\d+\n)?TOTAL BENEFITS\nPower\n([^\n]+)\nTotal cost\n([\d,.]+[KMB]?)', opt)
    tier, items = ar_items('Spelunking')
    caves = [{'cave': i['label'].split(':')[0], 'bonus': i['label'].split(':', 1)[1] if ':' in i['label'] else '', 'done': i.get('goal') == '✔' or i.get('cur') == i.get('goal')}
             for i in items if i['group'] == 'Cave Bonuses']
    return save('spelunking', {'amber': n(g('Amber Found')), 'pages': g('Daily Page Reads'), 'disc': g('Discoveries'), 'power': g('Power'), 'optimizer': seq, 'caves': caves, 'shop': shop_levels(u)})


def card_lines(o):
    L = []
    nxt = [c for c in o['caves'] if not c['done']]
    if nxt: L.append(f"TOP: Spelunking is the biggest thing holding the account back. The next caves unlock: " + '; '.join(c['bonus'].split('!')[0][:60] for c in nxt[:4]) + '.')
    if o['pages']: L.append(f"Read the rest of today's pages ({o['pages']} used).")
    shop, a = o.get('shop', {}), o['amber'] or 0
    buys = []
    for name, why in BUY_ORDER:
        if name not in shop: buys.append(f"{name}: not unlocked yet ({why})"); continue
        lv, mx, c = shop[name]
        if lv >= mx: continue
        buys.append(f"{name} {lv} -> {lv + 1}: {c:,.0f} amber" + (" (can buy)" if c and c <= a else "") + f". {why}" if c else f"{name} {lv}: {why}")
    if buys: L.append(f"Amber buys in sourced order (you have {a:,.0f} amber): " + ' | '.join(buys[:4]))
    if o['optimizer']:
        a = o['amber']; s = o['optimizer'][0]; c = n(s[4])
        L.append(f"Toolbox optimizer (POW): {s[0]} {s[1]} -> {s[2]} for {s[4]} amber total, {s[3]}.")
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
