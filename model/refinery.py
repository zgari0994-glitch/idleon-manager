"""Refinery planner: salt balances, rank headroom (Toolbox max safe rank), throttle-ready Squires, inputs tied to prints, soul use/hr.
-> Autistastic's Construction block (Refinery section). Griffy: red salts first, limit explosive/blue/green, aim for perpetual motion."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / 'snapshots' / (ROOT / 'snapshots' / 'LATEST').read_text().strip()
CYCLE = {'Redox Salts': 'Combustion', 'Explosive Salts': 'Combustion', 'Spontaneity Salts': 'Combustion',
         'Dioxide Synthesis': 'Synthesis', 'Purple Salt': 'Synthesis', 'Nullo Salt': 'Synthesis'}


def _n(s):
    s = s.replace(',', '').replace('+', '').strip()
    m = re.match(r'(-?[\d.]+)\s*([KMBT])?$', s)
    return float(m.group(1)) * {None: 1, 'K': 1e3, 'M': 1e6, 'B': 1e9, 'T': 1e12}[m.group(2)] if m else None


def build():
    # Zack 2026-11-25: Toolbox parser numbers (model/data.py). Safe rank, cycles/hr and throttle state are website-only.
    from data import load
    R = load().system('refinery')
    salts = [{'salt': x['saltName'].replace('_', ' '), 'rank': x['rank'], 'auto': x.get('autoRefinePercentage'), 'cycle': CYCLE.get(x['saltName'].replace('_', ' ')),
              'mats': [(c['name'].replace('_', ' '), c['quantity']) for c in x['cost']], 'have': {c['name'].replace('_', ' '): c.get('totalAmount') for c in x['cost']},
              'safe': None, 'limit': None, 'balance_hr': None, 'refined': x.get('refined'), 'cap': x.get('powerCap')} for x in R['salts'] if x.get('unlocked')]
    soul_per_cycle = {}
    for s_ in salts:
        for mname, q in s_['mats']:
            if 'Soul' in mname: soul_per_cycle[mname] = soul_per_cycle.get(mname, 0) + q
    out = {'snapshot': SNAP.name, 'cycles_per_hr': {}, 'salts': salts, 'throttle_ready': [], 'soul_use_hr': {}, 'soul_per_cycle': soul_per_cycle, 'locked': [],
           'total_levels': R.get('totalLevels')}
    json.dump(out, open(ROOT / 'model' / 'refinery.json', 'w'), indent=1)
    return out


def card_lines(o):
    L = []
    if o['throttle_ready']: L.append(f"TOP: Refinery Throttle is ready on {' and '.join(o['throttle_ready'])}, use it.")
    room = [s for s in o['salts'] if s.get('safe') and s['safe'] > s['rank']]
    if room:
        r0 = room[0]
        L.append(f"Rank up {r0['salt']} first (rank {r0['rank']}, lots of room). Each salt above it is held back by the one below, so raising the first one frees the rest. Griffy: red salts first.")
    tight = [s['salt'] for s in o['salts'] if s.get('safe') and s['safe'] - s['rank'] <= 1]
    if tight: L.append(f"{', '.join(tight)} {'is' if len(tight) == 1 else 'are'} one rank from {'its' if len(tight) == 1 else 'their'} cap.")
    if o['soul_use_hr']: L.append('The salts eat ' + ' and '.join(f"{v * 24 / 1000:,.0f}K {k} a day" for k, v in o['soul_use_hr'].items()) + '. Keep that covered before spending souls elsewhere.')
    elif o.get('soul_per_cycle'): L.append('The salts use ' + ' and '.join(f"{v} {k} per cycle" for k, v in o['soul_per_cycle'].items()) + '. Keep souls covered before spending them elsewhere.')
    short = [(s['salt'], m) for s in o['salts'] for m, q in s['mats'] if s.get('have', {}).get(m) is not None and s['have'][m] < q * 1000]
    if short: L.append('Running low for the salts: ' + ', '.join(f"{m} ({sa})" for sa, m in short[:3]) + '.')
    L.append('Keep the Spore Cap, Copper, Goldfish, Fly and Pocket Sand prints, they feed the salts.')
    try:
        import saltlick; sl = saltlick.refinery_line(saltlick.build())
        if sl: L.append(sl + '.')
    except Exception: pass
    return L


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)
