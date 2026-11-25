"""Summoning planner (Autistocat). Unclaimed familiar EXP, daily Familiar buy, affordable essence upgrades per colour, Teal gate (Spelunking)."""
import re
from tbhelp import tb, ar_items, save

UNIT = {'': 1, 'K': 1e3, 'M': 1e6, 'B': 1e9, 'T': 1e12, 'Q': 1e15, 'QQ': 1e18}
def q(s):
    m = re.match(r'([\d.,]+)\s*(QQ|Q|T|B|M|K)?', s.strip()); return float(m.group(1).replace(',', '')) * UNIT[m.group(2) or ''] if m else None


def build():
    # Zack 2026-11-25: Toolbox parser numbers (model/data.py); next cost = cost * costExponent^level (my read of the game formula)
    from data import load
    S = load().system('summoning')
    COL = ['White', 'Green', 'Yellow', 'Blue', 'Purple', 'Red', 'Cyan', 'Teal', 'Black']
    ess = {COL[i] if i < len(COL) else str(i): (v, '') for i, v in enumerate(S['essences'])}
    ups = []
    for grp in S['upgrades'].values():
        for u in grp:
            c = u.get('colour', 0); held = S['essences'][c] if isinstance(c, int) and c < len(S['essences']) else None
            ups.append({'name': u['name'].replace('_', ' '), 'lv': u['level'], 'max': u['maxLvl'], 'cost': u['cost'] * u.get('costExponent', 1) ** u['level'] if u.get('cost') else None,
                        'held': held, 'colour': COL[c] if isinstance(c, int) and c < len(COL) else c, 'daily': 'Familiar' in u['name'] and u.get('cost') == 1})
    fe = S['familiarExp']
    unc = (f"{fe['expPerHour'] * fe['savedSeconds'] / 3600:,.0f} EXP", f"{fe['savedSeconds'] / 86400:.1f}d unclaimed") if fe.get('savedSeconds') else None
    return save('summoning', {'unclaimed': unc, 'endless': S['highestEndlessLevel'], 'essence': ess, 'upgrades': ups, 'teal': None, 'wins': S['totalWins']})

def card_lines(o):
    L = []
    if o['unclaimed']: L.append(f"TOP: claim the familiar EXP ({o['unclaimed'][0]}, {o['unclaimed'][1].split(' unclaimed')[0]} of it).")
    if [x for x in o['upgrades'] if x['daily'] and x['lv'] < x['max']]: L.append('Buy Familiar every day. It costs 1 essence and the price resets daily.')
    aff = [x for x in o['upgrades'] if x['cost'] and x['held'] and x['cost'] <= x['held'] * 0.01 and x['lv'] < x['max'] and not x['daily']]
    if aff: L.append(f"{len(aff)} upgrades are basically free right now: " + ', '.join(x['name'] for x in aff[:6]) + '.')
    if o['teal']: L.append(f"Teal battles ({o['teal'][0]} of {o['teal'][1]}) open up after Autistomatic's Spelunking cave.")
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
