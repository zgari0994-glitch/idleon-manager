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
    pr = [i for i in o['ar'] if i['group'].startswith('Level Priority')]
    seen = {}
    for i in pr: seen.setdefault(i['label'].split(' - ')[0], i)
    by = {a['atom']: a for a in o['atoms']}
    aff = sorted([a for a in o['atoms'] if a['cost'] and a['lv'] < a['max'] and a['cost'] <= P], key=lambda a: a['cost'])
    neon = by.get('Neon')
    if neon and neon['cost'] and neon['lv'] < neon['max']:
        L.append(f"TOP: Neon {neon['lv']} -> {neon['lv'] + 1} for {h(neon['cost'])} (of {h(P)} particles). Neon is +1% damage and -1% on every atom cost per level, so it goes before the big saves (my read from Toolbox cost-cut breakdown; Neon is 27.5% of your cut).")
    L.append(f"Particles {h(P)}, +{h(o['per_hr'])}/hr ({h(o['per_hr'] * 24)}/day). Atoms unlocked {o['unlocked'][0]}/{o['unlocked'][1]}. Cost cut {o['cost_cut']}%.")
    L.append(f"AutoReview priority (tier {o['ar_tier']}): " + ', '.join(f"{k} {i['cur']} -> {i['goal']}" + (f" ({h(by[k]['cost'])}{', ' + by[k]['eta'] if by.get(k, {}).get('eta') else ''})" if by.get(k, {}).get('cost') else ' (maxed/locked)' if by.get(k) and by[k]['lv'] >= by[k]['max'] else ' (locked)') for k, i in seen.items()))
    rest = [a for a in aff if a['atom'] != 'Neon']
    if rest: L.append('Also affordable now: ' + ', '.join(f"{a['atom']} ({a['name']}) {a['lv']}->{a['lv'] + 1} {h(a['cost'])}" for a in rest))
    L.append('Max level 40 (base 20 + event 20). More max: Compass Atomic Potential (Autistacular), Isotope Discovery superbit (Gaming), Menagerie boost 18.')
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
