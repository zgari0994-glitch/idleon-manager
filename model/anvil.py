"""Anvil setup per character (Zack 2026-11-28, Phase C step C). No quantity tracking, just the setup:
hammers -> item names (Toolbox anvilProducts, brain/tb_static.json), point split speed/cap/exp, unspent.
Watched bars (Zack: 'Gas Shard + Historium' = Godshard Bar + Prehistrium Bar, my read of the names): forge slots + storage."""
import json
from collections import Counter
from pathlib import Path
from data import load

ROOT = Path(__file__).resolve().parent.parent
ST = json.load(open(ROOT / 'brain' / 'tb_static.json'))
PROD = {p['index']: p['name'] for p in ST['anvil_products']}
WATCH_BARS = ['Godshard_Bar', 'Prehistrium_Bar']


def setup(name, D=None):
    D = D or load()
    a = D.char(name)['anvil']
    st, sel = a['anvilStats'], a['anvilSelected']
    sel = sel if isinstance(sel, list) else [sel]
    ham = Counter(PROD.get(i, f'item #{i}') for i in sel)
    earned = sum(st.get(k) or 0 for k in ('pointsFromCoins', 'pointsFromMats', 'pointsFromAcme'))
    spent = sum(st.get(k) or 0 for k in ('speedPoints', 'capPoints', 'xpPoints'))
    return {'producing': dict(ham), 'speed': st.get('speedPoints'), 'cap': st.get('capPoints'), 'exp': st.get('xpPoints'),
            'unspent': int(st.get('availablePoints') or 0), 'earned_read': earned, 'spent': spent}


def line(name, D=None):
    try:
        s = setup(name, D)
    except Exception as e:
        return f'Anvil (daily): grab production, spend points (anvil not read from this save: {e.__class__.__name__})'
    prod = ', '.join(f"{n} x{c}" if c > 1 else n for n, c in s['producing'].items())
    out = f"Anvil (daily): producing {prod}; points speed {s['speed']} / cap {s['cap']} / exp {s['exp']}; unspent {s['unspent']}"
    if s['unspent'] > 0:
        out += ' -> spend them'
    if s['unspent'] < 0:
        out += f" (Toolbox reads {s['unspent']}: spent {s['spent']} vs points it can see {s['earned_read']}+; a points source Toolbox doesn't read, check unspent in game)"
    if s['cap'] == 0:
        out += ' (cap 0 = every point on speed, base capacity only: fine if you grab production daily, my read)'
    return out


def bars(D=None):
    D = D or load()
    have = {b: [0, 0] for b in WATCH_BARS}
    for x in (D.account.get('forge') or {}).get('list') or []:
        b = (x.get('bar') or {})
        if b.get('displayName') in have:
            have[b['displayName']][0] += b.get('quantity') or 0
    stg = D.account.get('storage') or {}
    for it in (stg.get('list') if isinstance(stg, dict) else stg) or []:
        if not isinstance(it, dict): continue
        n = it.get('name') or it.get('displayName') or it.get('rawName')
        if n in have:
            have[n][1] += it.get('amount') or 0
    return have


def bars_line(D=None):
    try:
        h = bars(D)
    except Exception as e:
        return f'Watch daily (anvil/forge) [{e.__class__.__name__}]: Godshard + Prehistrium bars (not read from this save)'
    return 'Watch daily (forge): ' + ', '.join(f"{n.replace('_', ' ')} {f} in forge slots + {s} in storage" for n, (f, s) in h.items()) + ': months of grinding ahead, keep stockpiling (Zack 2026-11-28)'


if __name__ == '__main__':
    D = load()
    for c in D.characters:
        print(c['name'], '|', line(c['name'], D))
    print(bars_line(D))
