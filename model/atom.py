"""Atom Collider planner (Autistastic Construction block). Particles, rate, atom costs, AutoReview priority, Neon cost-cut math."""
import re
from tbhelp import tb, ar_items, n, save
from spend import h


def build():
    # Zack 2026-11-25: Toolbox parser numbers (model/data.py)
    from data import load, SNAPS
    D = load(); A = D.system('atom_collider')
    atoms = [{'atom': a['name'].split('_-_')[0], 'name': a['name'].split('_-_')[-1].replace('_', ' '), 'lv': a['level'], 'max': a['maxLevel'],
              'cost': a.get('cost'), 'eta': None, 'locked': a.get('locked'), 'desc': a['desc'].replace('_', ' ')[:120]} for a in A['atoms']]
    per_hr = None   # rate = particle change since the previous save (spending makes it an underestimate)
    prev = sorted(p.name for p in SNAPS.iterdir() if p.is_dir() and p.name < D.stamp and (p / 'tb_parsed.json.gz').exists())
    if prev:
        P = load(prev[-1]); dp = A['particles'] - P.get('account.atoms.particles', allow_empty=True); dh = (D.save_time - P.save_time) / 3600
        if dp > 0 and dh > 0: per_hr = dp / dh
    for a in atoms:
        if per_hr and a['cost'] and a['cost'] > A['particles']: a['eta'] = f"{(a['cost'] - A['particles']) / per_hr / 24:.1f} days"
    tier, items = ar_items('Atom Collider')
    return save('atom', {'particles': A['particles'], 'per_hr': per_hr, 'cost_cut': A['costCut'].get('sum'),
                         'unlocked': (sum(1 for a in atoms if not a['locked']), len(atoms)), 'atoms': atoms, 'ar_tier': tier, 'ar': items})

def card_lines(o):
    P = o['particles']; L = []
    by = {a['atom']: a for a in o['atoms']}
    neon = by.get('Neon')
    if neon and neon['cost'] and neon['lv'] < neon['max'] and neon['cost'] <= P:
        L.append(f"TOP: buy Neon ({h(neon['cost'])} particles, you have {h(P)}). It makes every other atom cheaper, so get it before saving for the big ones (my read).")
    he = by.get('Helium')
    if he and he['cost']: L.append(f"AutoReview's top atom is Helium: {h(he['cost'])} particles" + (f", about {he['eta']} away at your rate ({h(o['per_hr'] * 24)} a day)." if he['eta'] else '.'))
    aff = [a for a in o['atoms'] if a['cost'] and a['lv'] < a['max'] and a['cost'] <= P and a['atom'] not in ('Neon',)]
    if aff: L.append('Also affordable now: ' + ', '.join(f"{a['atom']} ({h(a['cost'])})" for a in sorted(aff, key=lambda a: a['cost'])) + '.')
    L.append(f"{o['unlocked'][0]} of {o['unlocked'][1]} atoms unlocked. Aluminium comes from Compass Nomadic 32 on Autistacular.")
    return L


if __name__ == '__main__':
    for l in card_lines(build()): print(l)
