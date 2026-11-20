"""Gallery planner (Autistachio). Podium counts, empty podiums, nametags owned vs missing (acquire.py has sources)."""
import re
from tbhelp import tb, ar_items, save


def build():
    T = tb('gallery'); t = T['Trophies']['text']; nt = T['Nametags']['text']
    f = lambda k: (re.search(re.escape(k) + r'\n([^\n]+)', t) or [None, None])[1]
    tags = [(a, b) for a, b in re.findall(r'([^\n|]+Nametag)\n(Lv \d+|[ \t]*)(?=\n)', nt)]
    tier, items = ar_items('Gallery')
    return save('gallery', {'podiums': f('Podiums'), 'multi': f('Bonus multi'), 'empty': len(re.findall(r'(?<=\n)Empty(?=\n)', t)), 'tags_owned': [a for a, b in tags if b.startswith('Lv')],
                            'tags_missing': [a for a, b in tags if not b.startswith('Lv')], 'ar': items, 'tier': tier})


def card_lines(o):
    L = []
    if o['empty']: L.append(f"TOP: {o['empty']} empty podium slots: put trophies in them.")
    L.append(f"Gallery {o['podiums']} podiums, bonus {o['multi']}. Nametags owned {len(o['tags_owned'])} (missing ones + sources in acquire.md).")
    ar = [i for i in o['ar'] if i.get('cur') != i.get('goal')][:4]
    if ar: L.append(f"AutoReview (tier {o['tier']}): " + '; '.join(f"{i['label'][:60]} {i['cur']}->{i['goal']}" for i in ar))
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
