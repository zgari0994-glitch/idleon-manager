"""Construction buildings planner (Autistastic). Finished-but-slotted buildings, trimmed slot moves, blocked materials, AutoReview tiers."""
import re
from tbhelp import tb, ar_items, n, save


def build():
    t = tb('buildings')['_page']['text']
    sp = re.search(r'Build speed\n([^\n]+)\nTrimmed build speed\n([^\n]+)', t)
    bs = []
    for m in re.finditer(r'\n([A-Z][^\n]+)\nLv (\d+) / (\d+)\n(.*?)(?=\n[A-Z][^\n]+\nLv \d+ / |\nDiscord)', t, re.S):
        b = m.group(4)
        if b.startswith('Maxed'): continue
        st = re.findall(r'●\n([^\n]+)', b); tl = re.search(r'Time left\n(?:●\n)?([^\n]+)', b); nx = re.search(r'Next level\n([^\n]+)\n/\n([^\n]+)', b)
        bs.append({'name': m.group(1), 'lv': int(m.group(2)), 'max': int(m.group(3)), 'slot': 'trimmed' if 'Trimmed slot' in st else 'building' if 'Building' in st else None,
                   'ready': (tl.group(1) == 'Ready') if tl else False, 'left': tl.group(1) if tl else None,
                   'have': n(nx.group(1)) if nx else None, 'need': n(nx.group(2)) if nx else None})
    tier, items = ar_items('Buildings')
    return save('buildings', {'speed': sp.groups() if sp else None, 'buildings': bs, 'ar': items})


def _secs(s):
    tot = 0
    for v, u in re.findall(r'([\d.]+)\s*([dhms])', s or ''): tot += float(v) * {'d': 86400, 'h': 3600, 'm': 60, 's': 1}[u]
    return tot


def card_lines(o):
    B = o['buildings']; L = []
    waste = [b for b in B if b['slot'] and b['ready']]
    tr = [b['name'] for b in waste if b['slot'] == 'trimmed']
    if waste: L.append(f"TOP: {len(waste)} buildings in slots show as finished" + (f", including all your trimmed slots ({', '.join(tr)})" if tr else '') + '. Check in game, then move the slots to unfinished buildings.')
    blocked = [b for b in B if b['have'] is not None and b['need'] and b['have'] < b['need']]
    open_ = sorted([b for b in B if not b['ready'] and b not in blocked and b['left']], key=lambda b: -_secs(b['left']))
    if open_: L.append('Best slot targets (longest builds first): ' + ', '.join(f"{b['name']} ({b['left']})" for b in open_[:3]) + '.')
    if blocked: L.append(f"{', '.join(b['name'] for b in blocked)} are stuck on one material you only have {blocked[0]['have']:,.0f} of. Check which one in game.")
    tiers = {}
    for i in o['ar']: tiers.setdefault(i['group'], []).append(f"{i['label']} {i['cur']} -> {i['goal']}")
    if 'S Tier' in tiers: L.append('AutoReview top buildings: ' + ', '.join(tiers['S Tier'][:4]) + '.')
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
