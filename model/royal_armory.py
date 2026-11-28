"""Royal Armory planner (Autistastic, Royal Guardian #1). AutoReview only until the Toolbox page reads (it didn't load 2026-11-19)."""
from tbhelp import ar_items, save, tb


def build():
    # Zack 2026-11-25: Toolbox parser numbers (model/data.py) + AutoReview
    from data import load
    R = load().system('royal_armory')
    tier, items = ar_items('Royal Armory')
    ups = [{'name': u['name'].replace('_', ' '), 'lv': u['level'], 'max': u['maxLevel'], 'cost': u['cost'], 'res': u.get('costResourceIndex'), 'open': bool(u.get('unlocked'))} for u in R['armory']['upgrades']]
    stor = R.get('resourceStorage') or []
    for u in ups:
        u['have'] = stor[u['res']] if isinstance(u['res'], int) and u['res'] < len(stor) else None
    # Zack 2026-11-28 Phase C finish: the gate is shelfUnlockTotalLevels (same field lookup.py shows). Kingdom Expansion 5-8 have no cost/resource = not in game yet (my read), skipped.
    tot = R['armory']['totalLevels']
    lk = sorted((u for u in R['armory']['upgrades'] if not u.get('unlocked') and u.get('cost') and u.get('costResourceRawName') and (u.get('shelfUnlockTotalLevels') or 0) > tot), key=lambda u: u['shelfUnlockTotalLevels'])
    nxt = None
    nxt = [{'name': u['name'].replace('_', ' '), 'at': u['shelfUnlockTotalLevels'], 'cost': u['cost'], 'res': u['costResourceRawName'],
            'have': stor[u['costResourceIndex']] if isinstance(u.get('costResourceIndex'), int) and u['costResourceIndex'] < len(stor) else 0}
           for u in lk if u['shelfUnlockTotalLevels'] == lk[0]['shelfUnlockTotalLevels']] if lk else None
    return save('royal_armory', {'next_unlock': nxt, 'ar_tier': tier, 'ar': items, 'toolbox': True, 'tabs': [], 'armory_levels': R['armory']['totalLevels'],
                                 'next_shelf': R['armory']['nextShelfAt'], 'upgrades': ups, 'orblets': R.get('orblets'),
                                 'deployments': [(d.get('jobName'), str(d.get('mapName')).replace('_', ' '), d.get('idle')) for d in R.get('deployments', [])]})

def card_lines(o):
    L = []
    it = [i for i in o['ar'] if i['group'] == 'Royal Statues' and i.get('cur') == '0']
    if it: L.append(f"Next Royal statue to build: {it[0]['label'].split(':')[0]}.")
    up = [i for i in o['ar'] if i['group'] == 'Armory Upgrades' and i.get('goal') not in (None, '', '✔') and i.get('cur') != i.get('goal')]
    if up: L.append('Armory upgrades to push: ' + ', '.join(i['label'].split(':')[0] for i in up[:3]) + '.')
    aff = [u for u in o.get('upgrades', []) if u.get('open', True) and u['lv'] < u['max'] and u['have'] is not None and u['cost'] and u['cost'] <= u['have']]
    if aff: L.append('Affordable Armory upgrades: ' + ', '.join(u['name'] for u in sorted(aff, key=lambda u: u['cost'])[:5]) + '.')
    if o.get('next_shelf'): L.append(f"Armory levels {o['armory_levels']} / {o['next_shelf']} for the next shelf.")
    nx = o.get('next_unlock')
    if nx: L.append(f"Next unlock at {nx[0]['at']} armory levels (have {o['armory_levels']}): " + '; '.join(f"{n['name']} costs {n['cost']:,.0f} {n['res']} (have {n['have']:,.0f})" for n in nx) + '.')
    idle = [d for d in o.get('deployments', []) if d[2]]
    if idle: L.append('Idle Royal Guardian deployment: ' + ', '.join(f"{d[0]} on {d[1]}" for d in idle) + '.')
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
