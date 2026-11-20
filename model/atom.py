"""Atom Collider planner (Autistastic Construction block). Particles, rate, atom costs, AutoReview priority, Neon cost-cut math."""
import re
from tbhelp import tb, ar_items, n, save
from spend import h


def build():
    t = tb('atom')['_page']['text']
    p = re.search(r'Particles\n([\d.,]+[KMB]?)\nParticles per hour\n([\d,.]+)', t)
    cut = re.search(r'Atom cost cut\n([\d.]+)%', t); unl = re.search(r'Atoms unlocked\n(\d+) / (\d+)', t)
    atoms = []
    for m in re.finditer(r'\n([A-Z][a-z]+) - ([^\n]+)\nLv (\d+) / (\d+)\n(.*?)(?=\n[A-Z][a-z]+ - |\nDiscord|\Z)', t, re.S):
        b = m.group(5); c = re.search(r'\n([\d.,]+[KMB]?)\n/\n([\d.,]+[KMB]?)(?:\n|$)', b); nl = re.search(r'Next level in\n([^\n]+)', b)
        atoms.append({'atom': m.group(1), 'name': m.group(2), 'lv': int(m.group(3)), 'max': int(m.group(4)), 'cost': n(c.group(2)) if c else None, 'eta': nl.group(1) if nl else None,
                      'desc': next((l for l in b.split('\n') if len(l) > 30), '')[:120]})
    tier, items = ar_items('Atom Collider')
    return save('atom', {'particles': n(p.group(1)), 'per_hr': n(p.group(2)), 'cost_cut': float(cut.group(1)) if cut else None,
                         'unlocked': unl.groups() if unl else None, 'atoms': atoms, 'ar_tier': tier, 'ar': items})


def card_lines(o):
    P = o['particles']; L = []
    by = {a['atom']: a for a in o['atoms']}
    neon = by.get('Neon')
    if neon and neon['cost'] and neon['lv'] < neon['max'] and neon['cost'] <= P:
        L.append(f"TOP: buy Neon ({h(neon['cost'])} particles, you have {h(P)}). It makes every other atom cheaper, so get it before saving for the big ones (my read).")
    he = by.get('Helium')
    if he and he['cost']: L.append(f"AutoReview's top atom is Helium: {h(he['cost'])} particles, about {he['eta'] or '?'} away at your rate ({h(o['per_hr'] * 24)} a day).")
    aff = [a for a in o['atoms'] if a['cost'] and a['lv'] < a['max'] and a['cost'] <= P and a['atom'] not in ('Neon',)]
    if aff: L.append('Also affordable now: ' + ', '.join(f"{a['atom']} ({h(a['cost'])})" for a in sorted(aff, key=lambda a: a['cost'])) + '.')
    L.append(f"{o['unlocked'][0]} of {o['unlocked'][1]} atoms unlocked. Aluminium comes from Compass Nomadic 32 on Autistacular.")
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
