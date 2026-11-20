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
    if int(a[0]) > 0: L.append(f"TOP: {o['attempts']} Emperor attempts unused (+1/day, cap {a[1]}): push past {best}. Zack 2026-11-19: best fighter (Autiszemo, highest damage on Toolbox) pushes for the bonuses; reset + re-climb only if a drop is really needed.")
    nxt = sorted([(int(x.split(',')[0]), b) for b, tot, x in o['bonuses'] if x[0].isdigit()])[:5]
    L.append(f"Next showdown breakpoints after {best}: " + ', '.join(f"{lv} {b}" for lv, b in nxt) + f". Next level gives {o['next_bonus']}.")
    return L


def build_islands():
    t = tb('islands')['_page']['text']
    return save('islands', {k: G(t, k) for k in ('Bottles', 'Unclaimed trash days', 'Garbage to collect', 'Garbage', 'Mobs waiting', 'Shimmer')} | {'crystal_days': (re.search(r'Unclaimed days \n([^\n]+)', t) or [0, None])[1]})


def lines_islands(o):
    d = []
    if o['Garbage to collect'] and o['Garbage to collect'] != '0': d.append(f"collect {o['Garbage to collect']} garbage (holding {o['Garbage']})")
    if o['Mobs waiting'] and o['Mobs waiting'] != '0': d.append(f"fight {o['Mobs waiting']} crystal mobs (candy)")
    return ([f"TOP: Islands: {', '.join(d)}."] if d else []) + [f"Bottles {o['Bottles']}, shimmer {o['Shimmer']} (weekly trial)."]


def build_arcade():
    t = tb('arcade')['_page']['text']
    ups = [(a, int(lv), n(c)) for a, lv, c in re.findall(r'\n([^\n]+)\nLv (\d+) / 100\n[\d,]+\n/\n([\d,]+)', t)]
    return save('arcade', {'balls': G(t, 'Balls'), 'full': 'Full: claim now' in t, 'gold': n(G(t, 'Gold balls')), 'ups': ups, 'rotation': t[t.find('Current rotation'):t.find('Off rotation')]})


def lines_arcade(o):
    L = []
    if o['full']: L.append(f"TOP: Arcade full ({o['balls']} balls): claim now.")
    rot = [u for u in o['ups'] if u[0] in o['rotation']]
    aff = sorted([u for u in rot if u[2] <= o['gold'] and u[1] > 0], key=lambda u: u[2])
    if aff: L.append(f"Arcade gold balls {o['gold']:,.0f}, in rotation and affordable: " + ', '.join(f"{a} Lv {lv} ({c:,.0f})" for a, lv, c in aff))
    big = [u for u in rot if u[2] > o['gold']]
    if big: L.append('Arcade saving for: ' + ', '.join(f"{a} Lv {lv} ({c:,.0f})" for a, lv, c in big))
    return L


def build_owl():
    t = tb('owl')['_page']['text']
    f = n(G(t, 'Feathers'))
    ups = [(a, lv, n(c)) for a, lv, c in re.findall(r'\n([A-Z][^\n]+)\nLv (\d+)\n\n[^\n]+\n\n[\d.e+KMBTQ]+\n/\n([\d.e+KMBTQ]+)', t)]
    return save('owl', {'feathers': f, 'mega': G(t, 'MEGAFEATHERS'), 'ups': ups})


def lines_owl(o):
    aff = [u for u in o['ups'] if u[2] and u[2] <= o['feathers']]
    L = [f"Owl: {len(aff)} upgrades affordable ({o['feathers']:.3g} feathers): " + ', '.join(f"{a} Lv {lv}" for a, lv, c in aff) + '.'] if aff else []
    L.append(f"Megafeathers {o['mega']} (Equinox Voter Rights needs all 10 megafeathers + 12 megafish).")
    return L


def build_killroy():
    T = tb('killroy'); s = T['Schedule']['text']; p = T['Permanent Upgrades']['text']
    weeks = re.findall(r'(\d\d/\d\d/\d{4}) 19:00\n(Room 1 ·\n\w+\n[\d,]+\nRoom 2 ·\n\w+\n[\d,]+)', s)
    perm = re.findall(r'\n([^\n]{10,90})\n(?:\n[^\n]+\n\n(?:Toward its cap\n[^\n]+\n)?)?Cost\n(\d+)', p)
    return save('killroy', {'skulls': int(G(s, 'Skulls') or 0), 'weeks': [(d, r.replace('\n', ' ')) for d, r in weeks], 'perm': [(a, int(c)) for a, c in perm if not a[0].isdigit() or 'Chance' in a]})


def lines_killroy(o):
    L = []
    if o['weeks']: L.append(f"Killroy this week ({o['weeks'][0][0]}): {o['weeks'][0][1]}. Next: " + '; '.join(f"{d} {r}" for d, r in o['weeks'][1:3]))
    aff = [x for x in o['perm'] if x[1] <= o['skulls']]
    if aff: L.append(f"Killroy skulls {o['skulls']}: permanent upgrades affordable: " + ', '.join(f"{a[:50]} ({c})" for a, c in aff))
    L.append('Equinox challenge: 2,000 kills in one Killroy run = +35% bar fill (best single room so far 1,296).')
    return L


def build_hole():
    T = tb('hole'); st = T['Study']['text']; en = T['Engineer']['text']; ex = T['Explore']['text']
    ready = re.findall(r'\n([A-Z][^\n]+)\nLv (\d+) · ([^\n]+)\n(?:●\nActive\n)?\n[^\n]+\n\nProgress\n[^\n]+\nNext level\n●\nReady', st)
    soon = re.findall(r'\n([A-Z][^\n]+)\nLv (\d+) · ([^\n]+)\n(?:●\nActive\n)?\n[^\n]+\n\nProgress\n[^\n]+\nNext level\n(\d+m \d+s|\d+h \d+m)', st)
    schem = [(a, c) for a, b, c in re.findall(r'\n([A-Z][^\n]+)\n\n[^\n]+\n\n(?:Total Bonus: [^\n]+\n\n)?([\d.,]+[KMBT]?)\n/\n([\d.,]+[KMBT]?)\n(?!need)', en)]
    return save('hole', {'caverns': G(ex, 'Unlocked caverns'), 'ready': ready, 'soon': soon[:4], 'schematics': G(en, 'Unlocked schematics'), 'schem_aff': schem[:6]})


def lines_hole(o):
    L = []
    if o['ready']: L.append('TOP: Hole study levels Ready: ' + ', '.join(f"{a} Lv {b} ({c})" for a, b, c in o['ready']) + '.')
    if o['soon']: L.append('Next study levels: ' + ', '.join(f"{a} in {t}" for a, b, c, t in o['soon']))
    if o['schem_aff']: L.append('Engineer schematics affordable: ' + ', '.join(f"{a} ({c})" for a, c in o['schem_aff']))
    L.append(f"Caverns {o['caverns']}, schematics {o['schematics']}.")
    return L


def build_slab():
    t = tb('slab')['_page']['text']
    return save('slab', {k: G(t, k) for k in ('Looted items', 'Missing items', 'Greenstacks', 'Slab bonus multi')})


def lines_slab(o):
    return [f"Slab {o['Looted items']} looted, {o['Missing items']} missing (each new item raises the slab multi {o['Slab bonus multi']}). Greenstacks {o['Greenstacks']}."]


def build_beanstalk():
    t = tb('beanstalk')['_page']['text']
    foods = []
    for blk in re.split(r'\n(?=(?:Golden [^\n]+|Butter Bar)\nRank \d / 3)', t):
        m = re.match(r'(Golden [^\n]+|Butter Bar)\nRank (\d) / 3\n.*?Owned\n([\d.,]+[KM]?)\n / ([\d.,]+[KM]?)', blk, re.S)
        if m: foods.append((m.group(1), int(m.group(2)), n(m.group(3)), n(m.group(4))))
    return save('beanstalk', {'foods': foods})


def lines_beanstalk(o):
    f = sorted(o['foods'], key=lambda x: -(x[2] / x[3]))
    return ['Beanstalk next ranks (closest first): ' + ', '.join(f"{a} R{r} {ow:,.0f}/{nd:,.0f}" for a, r, ow, nd in f[:5])]


def build_capevine():
    t = tb('capevine')['_page']['text']
    return save('capevine', {k: G(t, k) for k in ('Capes collected', 'Bonus multi', 'Golden Vines', 'Next Golden Vine')})


def lines_capevine(o):
    return [f"Cape Vine {o['Capes collected']} capes, multi {o['Bonus multi']}. Next Golden Vine at {o['Next Golden Vine']} (missing capes + sources in acquire.md)."]


def build_shops():
    e = tb('eventshop')['_page']['text'].replace('\xa0', ' '); b = tb('ballot')
    items = re.findall(r'\n([A-Z][^\n]+)\n\n([^\n]+)\n\n(\d+)\n/\n(\d+)\nneed', e)
    return save('shops', {'points': G(e, 'Event Points'), 'rotation': (re.search(r'Current rotation: ([^\n]+)', e) or [0, None])[1], 'items': items[:8],
                          'ballot_next': G(b['Bonus']['text'], 'Next week in'), 'merit_next': G(b['Meritocracy']['text'], 'Next week in')})


def lines_shops(o):
    return [f"Event Shop ({o['rotation']}): {o['points']} points. Cheapest targets: " + ', '.join(f"{a} {c}" for a, d, h, c in sorted(o['items'], key=lambda x: int(x[3]))[:4]) + '.',
            f"Ballot vote resets in {o['ballot_next']}, Meritocracy in {o['merit_next']}: vote before reset."]


def build_tome():
    t = tb('tome')['Overview']['text']
    return save('tome', {'points': G(t, 'Total points'), 'rank': G(t, 'Rank'), 'gap': (re.search(r'([\d,]+) to Top', t) or [0, None])[1]})


def lines_tome(o):
    return [f"Tome {o['points']} points ({o['rank']}), {o['gap']} to the next bracket. Tome score comes from every system: the other planners raise it."]


def build_maint():
    T = tb('rift'); t = T['Tasks']['text']
    cur = re.search(r'\n([A-Z][^\n]+)\nRift (\d+)\n●\nCurrent\n\n([^\n]+)\n\nProgress\n([^\n]+)', t)
    nxt = re.findall(r'\n([A-Z][^\n]+)\nRift (\d+)\n\n([^\n]+)', t)
    return save('maint', {'rift': (re.search(r'Rift\n(\d+ / \d+)', t) or [0, None])[1], 'cur': cur.groups() if cur else None, 'next': [x for x in nxt if 'cannot progress' not in x[2]][:3]})


def lines_maint(o):
    L = []
    if o['cur']: L.append(f"Rift {o['rift']}: current task ({o['cur'][0]}): {o['cur'][2][:90]} ({o['cur'][3]}).")
    if o['next']: L.append('Next rifts: ' + '; '.join(f"Rift {b} {c[:70]}" for a, b, c in o['next']))
    L.append('Constellations 229/229 done.')
    return L
