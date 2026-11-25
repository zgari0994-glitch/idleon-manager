"""Coral Reef + Dancing Coral planner (Autistachio). Affordable reef upgrades, coral bonuses gated by shrine levels (routed to Autistastic)."""
import re
from tbhelp import tb, n, save


def build():
    # Zack 2026-11-25: Toolbox parser numbers (model/data.py)
    from data import load
    C = load().system('coral_reef')
    d = lambda x: str(x).replace('_', ' ')
    ups = [(d(u['description']), u['level'], u.get('maxLevel') or 10**9, u['cost']) for u in C['reefUpgrades']]
    dance = [(d(x['coralName']), d(x['description']), d(x['tower']['name']), str(x['tower']['level']), d(x['dropResource']), '201') for x in C['dancingCoral']]
    kid = [(d(k['description'])[:70], k['level'], k['cost'], k.get('divinityLevelReq')) for k in C.get('coralKidUpgrades', [])]
    return save('reef', {'coral': C['ownedCorals'], 'ups': ups, 'dance': dance, 'daily': (C.get('reefDayGains') or {}).get('value'), 'coral_kid': kid})

def card_lines(o):
    aff = sorted([u for u in o['ups'] if u[3] and u[3] <= o['coral'] and u[1] < u[2]], key=lambda u: u[3])
    L = []
    if aff:
        run = sum(u[3] for u in aff if u[3] <= o['coral'])
        L.append(f"TOP: spend coral on all {len(aff)} Reef upgrades ({run:,.0f} of your {o['coral']:,.0f})." + (" One of them gives a Menagerie shell." if any('Shell' in u[0] for u in aff) else ''))
    if o['dance']: L.append('Dancing Coral bonuses start when ' + ' and '.join(f"{s} reaches 201 (now {lv})" for c, b, s, lv, src, st in o['dance']) + '. Autistastic levels the shrines.')
    return L


def routed(o):
    return {'Autistastic': [f"Level {s} from {lv} to 201 to start Autistachio's {c} bonus." for c, b, s, lv, src, st in o['dance'] if int(lv) < 201][:3]} if o['dance'] else {}


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)
    print(routed(o))
