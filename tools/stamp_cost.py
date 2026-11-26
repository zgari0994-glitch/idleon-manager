"""Stamp cost (formulas copied from Idleon Toolbox source, parsers/world-1/stamps.ts, 2026-11-17).
Usage: python3 tools/stamp_cost.py "Blackheart Stamp" 246
Params come from the item def: effect,func,x1,x2,reqMulti,material,baseMat,powMat,baseCoin,powCoin.
Coin discounts: Insider Trading bribe (assumed 5%) + stamp-cost vials (Blue Flav + Venison Malt, cap 90%).
Material cost shown raw and with the 90% vial cap; stamp reducer (atoms), Envelope Pile sigil, merit NOT applied."""
import sys, gzip, json, os
sys.path.insert(0, '/home/claude/ar/mysite'); sys.path.insert(0, '/home/claude/work/ar/mysite')
from consts.generated.raw_item_data import raw_item_data as RD
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_snap = open(os.path.join(R, 'snapshots', 'LATEST')).read().strip()
d = json.load(gzip.open(os.path.join(R, 'snapshots', _snap, 'raw.json.gz'))); d = d.get('data', d)
g = lambda k: json.loads(d[k]) if isinstance(d.get(k), str) else d.get(k)
S = json.load(gzip.open(os.path.join(R, 'snapshots', _snap, 'systems.json.gz'))); S = S.get('systems', S)
VIAL = sum(v['value'] for v in S['alchemy_vials'].values() if v['short_name'] in ('Blue Flav', 'Venison Malt'))
MONEY = sum(v for k, v in d.items() if k.startswith('Money_'))

def owned(code):
    return sum(q for c, q in zip(g('ChestOrder'), g('ChestQuantity')) if c == code) + sum(
        q for i in range(12) for c, q in zip(g(f'InventoryOrder_{i}') or [], g(f'ItemQTY_{i}') or []) if c == code)

def cost(name, target):
    code, it = next((k, v) for k, v in RD.items() if isinstance(v, dict) and v.get('Name', '').lower() == name.lower())
    p = it['Description'].split(',')
    req, mat, bmat, pmat, bcoin, pcoin = int(p[4]), p[5], float(p[6]), float(p[7]), float(p[8]), float(p[9])
    tree = {'A': 0, 'B': 1, 'C': 2}[code[5]]; idx = int(code[6:]) - 1
    lv, mx = int(g('StampLv')[tree][str(idx)]), int(g('StampLvM')[tree][str(idx)])
    gold = lambda L: int(bcoin * 0.95 * max(1.05, pcoin - L / (L + 5 * req) * 0.25) ** (L * 10 / req) * max(0.1, 1 - VIAL / 100))
    matc = lambda L: bmat * pmat ** (max(0, round(L / req) - 1) ** 0.8) * 0.1  # vial cap applied
    raises = list(range(mx, target, req))
    return {'stamp': name, 'level': lv, 'max': mx, 'target': target, 'coins': sum(gold(i) for i in range(lv, target)),
            'material': RD[mat]['Name'], 'owned': owned(mat), 'raises': [(L, matc(L)) for L in raises],
            'next_raise': matc(raises[0]) if raises else 0, 'total_mat': sum(matc(L) for L in raises)}

if __name__ == '__main__':
    c = cost(sys.argv[1], int(sys.argv[2]))
    print(f"{c['stamp']}: lv {c['level']}, max {c['max']} -> {c['target']} | coins {c['coins']:.3e} (account {MONEY:.3e}) | {c['material']} owned {c['owned']:,}")
    for L, m in c['raises']: print(f"  max raise at {L}: {m:,.0f} (vial cap applied)")
    print(f"  total {len(c['raises'])} raises: {c['total_mat']:,.0f}")
