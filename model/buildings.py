"""Construction buildings planner (Autistastic). Finished-but-slotted buildings, trimmed slot moves, blocked materials, AutoReview tiers."""
import re
from tbhelp import tb, ar_items, n, save


def build():
    # Zack 2026-11-25: Toolbox parser numbers (model/data.py). Build times/ready state are website-only; the dashboard timers say when a building is ready.
    from data import load
    T = load().get('account.towers')
    bs = []
    for t in T['data']:
        if t['level'] >= t['maxLevel'] and not t.get('inProgress'): continue
        bs.append({'name': t['name'].replace('_', ' '), 'lv': t['level'], 'max': t['maxLevel'], 'slot': 'building' if t.get('inProgress') or t.get('slot', -1) >= 0 else None,
                   'ready': False, 'left': None, 'have': None, 'need': None})
    tier, items = ar_items('Buildings')
    return save('buildings', {'speed': (T.get('buildMultiplier'), None), 'buildings': bs, 'ar': items})

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
