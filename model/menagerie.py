"""Luminous Menagerie planner (Autisticles). Lumi, affordable boosts, mission progress, claimable missions, unlocks owned."""
import re
from tbhelp import tb, n, save


def build():
    T = tb('menagerie'); m = T['Missions']['text']; b = T['Boosts']['text']
    g = lambda t, k: (re.search(re.escape(k) + r'\n([^\n]+)', t) or [None, None])[1]
    lumi = n(g(m, 'Lumi'))
    boosts = [(a, int(lv), n(c)) for a, lv, c in re.findall(r'\n([^\n]{8,80})\nLv (\d+)\nPer LV\n[^\n]+\n[\d.,]+\n/\n([\d.,]+[KMB]?)', b)]
    locked = re.findall(r'\n([^\n]{8,80})\nLv 0\nLocked\nPer LV\n[^\n]+\n\n([^\n]+required)', b)
    miss = re.findall(r'\n([A-Z][^\n]+)\nClaimed (\d+) times\n([^\n]+)\nProgress\n([^\n]+)', m)
    return save('menagerie', {'rank': g(m, 'Menagerie rank'), 'lumi': lumi, 'per_hr': g(m, 'Lumi per hour'), 'claimable': g(m, 'Claimable missions'),
                              'unlocks': g(m, 'Unlocks owned'), 'boosts': boosts, 'locked': locked, 'missions': miss})


def card_lines(o):
    L = []
    if o['claimable'] and o['claimable'] != '0': L.append(f"TOP: {o['claimable']} missions claimable.")
    aff = [b for b in o['boosts'] if b[2] and b[2] <= o['lumi']]
    if aff: L.append(f"Lumi {o['lumi']:,.0f} (+{o['per_hr']}/hr). Affordable boosts: " + ', '.join(f"{a[:50]} Lv {lv} ({c:,.0f})" for a, lv, c in sorted(aff, key=lambda x: x[2])))
    if o['locked']: L.append('Locked boosts (target): ' + ', '.join(f"{a[:40]} ({r})" for a, r in o['locked'][:4]))
    L.append(f"Rank {o['rank']}, unlocks {o['unlocks']}. Missions: " + '; '.join(f"{a} {p}" for a, c, req, p in o['missions'][:5]))
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
