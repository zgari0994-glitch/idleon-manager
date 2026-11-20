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
    T = json.load(open(SNAP / 'toolbox' / 'refinery.json'))['tabs']['refinery:_page']
    t = T['text'].replace('\xa0', ' ')
    cph = {k: float(v) for k, v in re.findall(r'(Combustion|Synthesis|Polymerize) cycle time\n[^\n]+\n([\d.]+) cycles per hour', t)}
    bal = {a.strip(): b for a, b in re.findall(r'\n([A-Z][A-Za-z ]+)\n\t([^\t\n]+)\t', t.replace('\\t', '\t'))}
    salts = []
    for m in re.finditer(r'\n([A-Z][A-Za-z ]+)\nRank (\d+) · Auto refine (\w+)\nMATERIAL\tCYCLE\t\n(.*?)(?=\n[A-Z][A-Za-z ]+\nRank \d+ ·|\nDiscord|\Z)', t.replace('\\t', '\t'), re.S):
        name = m.group(1).strip()
        mats = [(a.strip(), _n(b)) for a, b in re.findall(r'\n([A-Z][A-Za-z ]+)\n\t\n([\d,]+)\n', m.group(4))]
        salts.append({'salt': name, 'rank': int(m.group(2)), 'auto': m.group(3), 'mats': mats, 'cycle': CYCLE.get(name), 'balance_hr': bal.get(name)})
    # max safe rank per salt (Toolbox breakdown order follows the salt order)
    safes = [b for b in T['breakdowns'] if b['label'].startswith('Max safe rank')]
    for s_, b in zip(salts, safes):
        mm = re.search(r'Max safe rank\n([\d,]+)', b['text']); s_['safe'] = int(mm.group(1).replace(',', '')) if mm else None
        lim = [l for l in b['text'].split('\n')[1:] if re.match(r'[A-Z][A-Za-z ]+$', l)]
        s_['limit'] = lim[0] if lim else None
    ready = re.findall(r'\n(Autis\w+)\n●\nReady\nRefinery Throttle', t)
    soul_use = {}
    for s_ in salts:
        for mname, q in s_['mats']:
            if 'Soul' in mname and s_['cycle'] in cph: soul_use[mname] = soul_use.get(mname, 0) + q * cph[s_['cycle']]
    out = {'snapshot': SNAP.name, 'cycles_per_hr': cph, 'salts': salts, 'throttle_ready': ready, 'soul_use_hr': soul_use,
           'locked': re.findall(r'\n([A-Z][A-Za-z ]+)\n\tLocked', t.replace('\\t', '\t'))}
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
    L.append('Keep the Spore Cap, Copper, Goldfish, Fly and Pocket Sand prints, they feed the salts.')
    try:
        import saltlick; sl = saltlick.refinery_line(saltlick.build())
        if sl: L.append(sl + '.')
    except Exception: pass
    return L


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)
