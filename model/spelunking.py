"""Spelunking planner (Autistomatic). Cave bonuses gate other systems (routed to their owners), amber, optimizer buys, page reads."""
import re
from tbhelp import tb, ar_items, n, save
from spend import h

ROUTE = {'Superbits': ('Autistastic', 'Gaming'), 'Cards': ('Autistronaut', 'Cards'), 'Exotic Market': ('Autiszemo', 'Farming'), 'Teal Summoning': ('Autistocat', 'Summoning'),
         'Cooking Meals': ('Autiszemo', 'Cooking'), 'Sigils': ('Autistocat', 'Sigils')}


# Sourced buy order (Zack 2026-11-21: shops get a sourced order; my math never above a sourced pick)
BUY_ORDER = [
    # Zack 2026-11-27: POW upgrades first, cheapest first
    ('Overpow Technique', 'Griffy (Apr 2026): POW upgrades first'),
    ('Depthing the POW', 'Griffy (Apr 2026): POW upgrades first'),
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
    # Zack 2026-11-25: Toolbox parser numbers (model/data.py). Upgrade max = x3, level -1 = locked. Optimizer is website-only.
    from data import load
    S = load().system('spelunk')
    # costs are in base amber; currentAmber is in the account's amber tier (game AmberDenominator: upgrade 66/51/41/20 -> 1e36/1e21/1e9/1e3)
    lv = {u.get('originalIndex'): u['level'] for u in S['upgrades']}
    den = 1e36 if lv.get(66, 0) >= 1 else 1e21 if lv.get(51, 0) >= 1 else 1e9 if lv.get(41, 0) >= 1 else 1e3 if lv.get(20, 0) >= 1 else 1
    # Zack 2026-11-27: cost and currentAmber are both raw amber (bank 57.8T, Discovering 1.03T); the old /den showed 1.03T as 1,032
    shop = {u['name'].replace('_', ' '): (u['level'], u.get('x3') or 99999, (u.get('cost') or 0)) for u in S['upgrades'] if u['level'] >= 0}
    tier, items = ar_items('Spelunking')
    caves = [{'cave': i['label'].split(':')[0], 'bonus': i['label'].split(':', 1)[1] if ':' in i['label'] else '', 'done': i.get('goal') == '✔' or i.get('cur') == i.get('goal')}
             for i in items if i['group'] == 'Cave Bonuses']
    return save('spelunking', {'amber': S['currentAmber'], 'pages': None, 'disc': f"{S['discoveriesCount']} / {S['maxDiscoveries']}", 'power': S['power']['value'],
                               'optimizer': [], 'caves': caves, 'shop': shop, 'overstim': S.get('overstimLevel'), 'upgrade_levels': S['totalUpgradeLevels']})


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
        if lv >= mx and not (c and name == 'Overpow Technique'): continue  # parser says Overpow 1/1 but still prices a level: show it, check in game
        buys.append(f"{name} {lv} -> {lv + 1}: {h(c)} amber" + (" (can buy)" if c and c <= a else "") + f". {why}" if c else f"{name} {lv}: {why}")
    if buys: L.append(f"Amber buys in sourced order (you have {h(a)} amber): " + ' | '.join(buys[:4]))
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
