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
    if o['throttle_ready']: L.append(f"TOP: Refinery Throttle READY on {', '.join(o['throttle_ready'])} (Squire cycles, use them).")
    for s in o['salts']:
        head = f"{s['salt']} rank {s['rank']}" + (f" (max safe {s['safe']:,}, capped by {s['limit']})" if s.get('safe') else '') + f", {s['balance_hr']}/hr, auto refine {s['auto']}"
        mats = ', '.join(f"{a} {b:,.0f}" for a, b in s['mats'])
        room = s.get('safe') and s['safe'] > s['rank']
        L.append(f"{head}. Per cycle: {mats}." + (" Room to rank up." if room else ' At its safe rank: inputs cap it.'))
    if o['soul_use_hr']: L.append('Souls the salt chain eats: ' + ', '.join(f"{k} {v:,.0f}/hr ({v * 24:,.0f}/day)" for k, v in o['soul_use_hr'].items()) + '. Worship has to cover this before any prayer/stamp soul spend.')
    L.append("Griffy: red salts first, keep explosive/blue/green levels limited, aim for perpetual motion; refinery cycles are S tier in the skull shop. "
             "Prints feed the salts (Spore Cap + Copper -> Redox, Goldfish + Fly + Pocket Sand -> Spontaneity), so those prints stay locked.")
    if o['locked']: L.append('Locked salts: ' + ', '.join(o['locked']))
    return L


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)
