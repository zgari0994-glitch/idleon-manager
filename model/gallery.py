"""Gallery planner (Autistachio). Podium counts, empty podiums, nametags owned vs missing (acquire.py has sources)."""
import re
from tbhelp import tb, ar_items, save


def build():
    # Zack 2026-11-25: Toolbox parser numbers (model/data.py)
    from data import load
    G = load().system('gallery')
    nm = lambda x: str(x.get('displayName') or x.get('name') or x.get('ID')).replace('_', ' ')
    used = {nm(t) for t in G['nametagsUsed']}
    tier, items = ar_items('Gallery')
    return save('gallery', {'podiums': G['podiumsOwned'], 'multi': f"{G['bonusMulti']:.2f}x", 'empty': max(0, G['podiumsOwned'] - len(G['trophiesUsed'])),
                            'spare_trophies': [nm(t) for t in G['inventoryTrophies']], 'tags_owned': sorted(used),
                            'tags_missing': [nm(t) for t in G['allNametags'] if nm(t) not in used], 'ar': items, 'tier': tier})

def card_lines(o):
    L = []
    if o['empty']: L.append(f"TOP: {o['empty']} empty podium slots: put trophies in them" + (f" (in your bags: {', '.join(o['spare_trophies'][:4])})." if o.get('spare_trophies') else '.'))
    L.append(f"Gallery {o['podiums']} podiums, bonus {o['multi']}. Nametags owned {len(o['tags_owned'])} (missing ones + sources in acquire.md).")
    ar = [i for i in o['ar'] if i.get('cur') != i.get('goal')][:4]
    if ar: L.append(f"AutoReview (tier {o['tier']}): " + '; '.join(f"{i['label'][:60]} {i['cur']}->{i['goal']}" for i in ar))
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
