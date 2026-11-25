"""Equinox planner (Autistopher). Bar fill/cap, claimable challenges, locked upgrades + unlock progress, AutoReview targets."""
import re
from tbhelp import tb, ar_items, n, save


def build():
    # Zack 2026-11-25: Toolbox parser numbers (model/data.py)
    from data import load
    E = load().system('equinox')
    cl = lambda x: str(x).replace('_', ' ')
    ups = [{'name': cl(u['name']), 'lv': u['lvl'], 'max': u['maxLvl'], 'locked': not u.get('unlocked'), 'unlock': None, 'progress': None} for u in E['upgrades']]
    ch = []
    for c in E['challenges']:
        if c.get('locked') or not c.get('active'): continue
        done = (c.get('current') or 0) >= (c.get('goal') or 1)
        ch.append({'task': cl(c['label']), 'state': 'Requirement met' if done else None, 'reward': cl(c['reward']), 'progress': f"{c.get('current')} / {c.get('goal')}"})
    tier, items = ar_items('Equinox')
    return save('equinox', {'fill_hr': E['chargeRate'], 'bar': (E['currentCharge'], E['chargeRequired']), 'upgrades': ups, 'challenges': ch, 'ar_tier': tier, 'ar': items})

def card_lines(o):
    L = []
    if o['bar'] and o['fill_hr']:
        cur, cap = o['bar']; mins = cap / o['fill_hr'] * 60
        L.append(f"TOP: spend the Equinox bar{' (it is full)' if cur >= cap else ''}. It refills in about {mins:.0f} minutes, so spend it every time you're on.")
    claim = [x for x in o['challenges'] if x['state'] and 'met' in x['state'].lower()]
    if claim: L.append(f"Claim {len(claim)} finished challenges: " + '; '.join(x['reward'] for x in claim) + '.')
    fillc = [x for x in o['challenges'] if 'fill rate' in x['reward'].lower() and x not in claim and 'Requires' not in x['task']]
    if fillc: L.append('Faster bar: ' + '; '.join(f"{x['task'].split('.')[0].split(' in a party')[0][:45]} ({x['progress']}) gives {x['reward'].replace(' Equinox Bar fill rate', ' fill')}" for x in fillc[:3]) + '.')
    lk = [u for u in o['upgrades'] if u['locked']]
    lka = [i for i in o['ar'] if 'unlock' in str(i.get('group', '')).lower() or 'locked' in str(i.get('label', '')).lower()]
    if lk: L.append('Locked: ' + ', '.join(u['name'] for u in lk[:6]) + (' (unlocks: ' + '; '.join(i['label'][:60] for i in lka[:3]) + ')' if lka else '') + '.')
    up = [i for i in o['ar'] if i['group'].startswith('Upgrade more')]
    if up: L.append('AutoReview wants: ' + ', '.join(f"{i['label'].split(' (')[0]} {i['cur']} -> {i['goal']}" for i in up) + '.')
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
