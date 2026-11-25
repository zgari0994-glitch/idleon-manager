"""Luminous Menagerie planner (Autisticles). Lumi, affordable boosts, mission progress, claimable missions, unlocks owned."""
import re
from tbhelp import tb, n, save


def build():
    # Zack 2026-11-25: Toolbox parser numbers (model/data.py)
    from data import load
    M = load().system('menagerie')
    d = lambda x: str(x).replace('_', ' ')
    boosts = [(d(b['description']), b['level'], b['cost']) for b in M['boosts'] if b.get('visible', True) and b['rankRequired'] <= M['rank']]
    locked = [(d(b['description']), f"rank {b['rankRequired']} required") for b in M['boosts'] if b['rankRequired'] > M['rank']]
    miss = [(m['name'], m['claims'], m['description'], f"{m['progress']:,.0f} / {m['requirement']:,.0f}") for m in M['missions'] if m.get('visible', True)]
    return save('menagerie', {'rank': M['rank'], 'lumi': M['lumi'], 'per_hr': M['lumiRate'], 'claimable': str(sum(m.get('claimable') or 0 for m in M['missions'])),
                              'unlocks': f"{sum(1 for u in M['unlocks'] if u.get('owned'))} / {len(M['unlocks'])}", 'boosts': boosts, 'locked': locked, 'missions': miss,
                              'shells': (M.get('shells'), M.get('shellReq'))})

def card_lines(o):
    L = []
    if o['claimable'] and o['claimable'] != '0': L.append(f"TOP: claim {o['claimable']} missions.")
    aff = [b for b in o['boosts'] if b[2] and b[2] <= o['lumi']]
    if aff: L.append(f"Buy {', '.join(re.sub(r'^\+?[\d.]+x? ', '', a).split(' to ')[0][:30] for a, lv, c in aff)} with Lumi (you have {o['lumi']:,.0f}).")
    if o['locked']: L.append(f"Next rank unlocks: {o['locked'][0][0][:50]} ({o['locked'][0][1]}). You're rank {o['rank']}.")
    close = [(a, p) for a, c, req, p in o['missions'] if '/' in p]
    if close: L.append('Missions in progress: ' + ', '.join(f"{a} {p}" for a, p in close[:4]) + '.')
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
