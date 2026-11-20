"""Batch C planners (Zack 2026-11-19). Each system: build_<x>() + lines_<x>(o). Thin wrapper modules (emperor.py, islands.py ...) register in plan.py."""
import re
from tbhelp import tb, ar_items, n, save
G = lambda t, k: (re.search(re.escape(k) + r'\n([^\n]+)', t) or [None, None])[1]


def build_emperor():
    t = tb('emperor')['_page']['text']
    bon = [(a, tot, nxt) for a, tot, nxt in re.findall(r'\n([A-Z][^\n]+)\nTotal\n([^\n]+)\nPer level\n[^\n]+\nReached at\n[^\n]+\nNext at\n([^\n]+)', t)]
    return save('emperor', {'best': G(t, 'Highest showdown'), 'attempts': G(t, 'Attempts'), 'next_bonus': G(t, 'Next level bonus'), 'bonuses': bon})


def lines_emperor(o):
    best = int(o['best']); L = []
    a = o['attempts'].split(' / ')
    if int(a[0]) > 0: L.append(f"TOP: use your {a[0]} Emperor attempts and push past showdown {best}. Autiszemo goes, he hits hardest. Only reset and climb again if you really need a drop.")
    nxt = sorted([(int(x.split(',')[0]), b) for b, tot, x in o['bonuses'] if x[0].isdigit()])[:4]
    L.append('Coming up: ' + ', '.join(f"{lv} gives more {b.lower()}" for lv, b in nxt) + '.')
    return L


def build_islands():
    t = tb('islands')['_page']['text']
    return save('islands', {k: G(t, k) for k in ('Bottles', 'Unclaimed trash days', 'Garbage to collect', 'Garbage', 'Mobs waiting', 'Shimmer')} | {'crystal_days': (re.search(r'Unclaimed days \n([^\n]+)', t) or [0, None])[1]})


def lines_islands(o):
    d = []
    if o['Garbage to collect'] and o['Garbage to collect'] != '0': d.append(f"collect {o['Garbage to collect']} garbage")
    if o['Mobs waiting'] and o['Mobs waiting'] != '0': d.append(f"fight the {o['Mobs waiting']} crystal mobs (they drop candy)")
    return [f"TOP: Islands: {' and '.join(d)}."] if d else []


def build_arcade():
    t = tb('arcade')['_page']['text']
    ups = [(a, int(lv), n(c)) for a, lv, c in re.findall(r'\n([^\n]+)\nLv (\d+) / 100\n[\d,]+\n/\n([\d,]+)', t)]
    return save('arcade', {'balls': G(t, 'Balls'), 'full': 'Full: claim now' in t, 'gold': n(G(t, 'Gold balls')), 'ups': ups, 'rotation': t[t.find('Current rotation'):t.find('Off rotation')]})


def lines_arcade(o):
    L = []
    if o['full']: L.append("TOP: the Arcade is full, claim your balls.")
    rot = [u for u in o['ups'] if u[0] in o['rotation']]
    nm = lambda a: re.sub(r'^\+?[\d.]+[x%]? ', '', a)
    aff = sorted([u for u in rot if u[2] <= o['gold'] and u[1] > 0], key=lambda u: u[2])
    if aff: L.append(f"Spend gold balls on {', '.join(nm(a) for a, lv, c in aff)} ({o['gold']:,.0f} gold balls).")
    big = [u for u in rot if u[2] > o['gold']]
    if big: L.append(f"Saving for {' and '.join(nm(a) for a, lv, c in big)} (they cost {big[0][2]:,.0f}+).")
    return L


def build_owl():
    t = tb('owl')['_page']['text']
    f = n(G(t, 'Feathers'))
    ups = [(a, lv, n(c)) for a, lv, c in re.findall(r'\n([A-Z][^\n]+)\nLv (\d+)\n\n[^\n]+\n\n[\d.e+KMBTQ]+\n/\n([\d.e+KMBTQ]+)', t)]
    return save('owl', {'feathers': f, 'mega': G(t, 'MEGAFEATHERS'), 'ups': ups})


def lines_owl(o):
    aff = [u for u in o['ups'] if u[2] and u[2] <= o['feathers']]
    return ([f"Owl: buy all {len(aff)} upgrades, you have way more feathers than they cost."] if aff else []) + [f"{o['mega']} megafeathers so far."]


def build_killroy():
    T = tb('killroy'); s = T['Schedule']['text']; p = T['Permanent Upgrades']['text']
    weeks = re.findall(r'(\d\d/\d\d/\d{4}) 19:00\n(Room 1 ·\n\w+\n[\d,]+\nRoom 2 ·\n\w+\n[\d,]+)', s)
    perm = re.findall(r'\n([^\n]{10,90})\n(?:\n[^\n]+\n\n(?:Toward its cap\n[^\n]+\n)?)?Cost\n(\d+)', p)
    return save('killroy', {'skulls': int(G(s, 'Skulls') or 0), 'weeks': [(d, r.replace('\n', ' ')) for d, r in weeks], 'perm': [(a, int(c)) for a, c in perm if not a[0].isdigit() or 'Chance' in a]})


def lines_killroy(o):
    L = []
    if o['weeks']: L.append(f"This week's Killroy rooms: {o['weeks'][0][1].replace(' ·', ':')}.")
    aff = [x for x in o['perm'] if x[1] <= o['skulls']]
    if aff: L.append(f"With {o['skulls']} skulls you can buy: " + ', '.join(a.split(',')[0].split('!')[0][:40] for a, c in aff[:4]) + '.')
    L.append('Get 2,000 kills in one room to finish an Equinox challenge (best so far 1,296).')
    return L


def build_hole():
    T = tb('hole'); st = T['Study']['text']; en = T['Engineer']['text']; ex = T['Explore']['text']
    ready = re.findall(r'\n([A-Z][^\n]+)\nLv (\d+) · ([^\n]+)\n(?:●\nActive\n)?\n[^\n]+\n\nProgress\n[^\n]+\nNext level\n●\nReady', st)
    soon = re.findall(r'\n([A-Z][^\n]+)\nLv (\d+) · ([^\n]+)\n(?:●\nActive\n)?\n[^\n]+\n\nProgress\n[^\n]+\nNext level\n(\d+m \d+s|\d+h \d+m)', st)
    schem = [(a, c) for a, b, c in re.findall(r'\n([A-Z][^\n]+)\n\n[^\n]+\n\n(?:Total Bonus: [^\n]+\n\n)?([\d.,]+[KMBT]?)\n/\n([\d.,]+[KMBT]?)\n(?!need)', en)]
    return save('hole', {'caverns': G(ex, 'Unlocked caverns'), 'ready': ready, 'soon': soon[:4], 'schematics': G(en, 'Unlocked schematics'), 'schem_aff': schem[:6]})


def lines_hole(o):
    L = []
    if o['ready']: L.append(f"TOP: Hole study level ready on {', '.join(a for a, b, c in o['ready'])}, bump it.")
    if o['soon']: L.append('Next ones ready: ' + ', '.join(f"{a} in {t}" for a, b, c, t in o['soon'][:3]) + '.')
    if o['schem_aff']: L.append('Engineer schematics you can afford: ' + ', '.join(a for a, c in o['schem_aff'][:4]) + '.')
    return L


def build_slab():
    t = tb('slab')['_page']['text']
    return save('slab', {k: G(t, k) for k in ('Looted items', 'Missing items', 'Greenstacks', 'Slab bonus multi')})


def lines_slab(o):
    return [f"Slab: {o['Missing items']} items you've never picked up. Each new one raises the slab bonus."]


def build_beanstalk():
    t = tb('beanstalk')['_page']['text']
    foods = []
    for blk in re.split(r'\n(?=(?:Golden [^\n]+|Butter Bar)\nRank \d / 3)', t):
        m = re.match(r'(Golden [^\n]+|Butter Bar)\nRank (\d) / 3\n.*?Owned\n([\d.,]+[KM]?)\n / ([\d.,]+[KM]?)', blk, re.S)
        if m: foods.append((m.group(1), int(m.group(2)), n(m.group(3)), n(m.group(4))))
    return save('beanstalk', {'foods': foods})


def lines_beanstalk(o):
    f = sorted([x for x in o['foods'] if x[2] < x[3]], key=lambda x: -(x[2] / x[3]))
    return ['Beanstalk, closest to the next rank: ' + ', '.join(f"{a} ({ow / nd:.0%})" for a, r, ow, nd in f[:4]) + '.']


def build_capevine():
    t = tb('capevine')['_page']['text']
    return save('capevine', {k: G(t, k) for k in ('Capes collected', 'Bonus multi', 'Golden Vines', 'Next Golden Vine')})


def lines_capevine(o):
    return [f"{o['Capes collected']} capes on the vine. The next golden vine comes at {o['Next Golden Vine'].lower()}."]


def build_shops():
    e = tb('eventshop')['_page']['text'].replace('\xa0', ' '); b = tb('ballot')
    items = re.findall(r'\n([A-Z][^\n]+)\n\n([^\n]+)\n\n(\d+)\n/\n(\d+)\nneed', e)
    return save('shops', {'points': G(e, 'Event Points'), 'rotation': (re.search(r'Current rotation: ([^\n]+)', e) or [0, None])[1], 'items': items[:8],
                          'ballot_next': G(b['Bonus']['text'], 'Next week in'), 'merit_next': G(b['Meritocracy']['text'], 'Next week in')})


def lines_shops(o):
    it = sorted(o['items'], key=lambda x: int(x[3]))[:2]
    return [f"Event Shop: {o['points']} points. Cheapest wanted: " + ', '.join(f"{a} ({c})" for a, d, h_, c in it) + '.',
            f"Vote on the Ballot before it resets ({o['ballot_next']})."]


def build_tome():
    t = tb('tome')['Overview']['text']
    return save('tome', {'points': G(t, 'Total points'), 'rank': G(t, 'Rank'), 'gap': (re.search(r'([\d,]+) to Top', t) or [0, None])[1]})


def lines_tome(o):
    return [f"Tome is at {o['points']} points, {o['gap']} short of the next bracket. Every other card raises it."]


def build_maint():
    T = tb('rift'); t = T['Tasks']['text']
    cur = re.search(r'\n([A-Z][^\n]+)\nRift (\d+)\n●\nCurrent\n\n([^\n]+)\n\nProgress\n([^\n]+)', t)
    nxt = re.findall(r'\n([A-Z][^\n]+)\nRift (\d+)\n\n([^\n]+)', t)
    return save('maint', {'rift': (re.search(r'Rift\n(\d+ / \d+)', t) or [0, None])[1], 'cur': cur.groups() if cur else None, 'next': [x for x in nxt if 'cannot progress' not in x[2]][:3]})


def lines_maint(o):
    L = []
    if o['cur']: L.append(f"Rift {o['rift'].split(' / ')[0]}: {o['cur'][2].split('.')[0]} ({o['cur'][3]}).")
    if o['next']: L.append('After that: ' + '; '.join(c.split('.')[0] for a, b, c in o['next'][:2]) + '.')
    return L


