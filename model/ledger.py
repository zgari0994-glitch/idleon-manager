"""Material ledger (Phase 1 item 7, material foresight). Code only.
Owned = storage chest + every character inventory, from the raw save. Rate = change vs the previous snapshot.
Flags: any item falling with a run-out ETA under RUNOUT_DAYS, watchlist items (ledger.yaml) with targets:
net shortage = max(0, target - owned); ETA = shortage / net rate (no ETA when rate <= 0: change the producer).
Writes model/ledger.json + ledger.md. Usage: python3 model/ledger.py"""
import json, gzip, os, sys, re, yaml, datetime as dt
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '/home/claude/ar/mysite'); sys.path.insert(0, '/home/claude/work/ar/mysite')
try:
    from consts.generated.raw_item_data import raw_item_data
    NAME = {k: v.get('Name', k).replace('_', ' ') for k, v in raw_item_data.items() if isinstance(v, dict)}
    TYPE = {k: v.get('Type', '') for k, v in raw_item_data.items() if isinstance(v, dict)}
except Exception:
    NAME, TYPE = {}, {}
STACK = ('BAR', 'MATERIAL', 'ORE', 'LOG', 'FISH', 'BUG', 'CRITTER', 'SOUL', 'MONSTER_DROP', 'CARD', 'STATUE', 'FOOD', 'SPICE')
RUNOUT_DAYS = 7
SNAPS = sorted(p for p in os.listdir(os.path.join(R, 'snapshots')) if p[:1].isdigit())
cur_stamp = open(os.path.join(R, 'snapshots', 'LATEST')).read().strip()

def load(stamp):
    d = json.load(gzip.open(os.path.join(R, 'snapshots', stamp, 'raw.json.gz'))); d = d.get('data', d)
    g = lambda k: json.loads(d[k]) if isinstance(d.get(k), str) else d.get(k)
    own = {}
    for code, q in zip(g('ChestOrder') or [], g('ChestQuantity') or []):
        if code != 'Blank': own[code] = own.get(code, 0) + (q or 0)
    for i in range(20):
        for code, q in zip(g(f'InventoryOrder_{i}') or [], g(f'ItemQTY_{i}') or []):
            if code != 'Blank': own[code] = own.get(code, 0) + (q or 0)
    t = d.get('TimeAway'); t = json.loads(t) if isinstance(t, str) else t
    return own, float(t['GlobalTime'])

own, t1 = load(cur_stamp)
prev = [s for s in SNAPS if s < cur_stamp]
rate, hours = {}, None
if prev:
    own0, t0 = load(prev[-1]); hours = (t1 - t0) / 3600
    if hours > 0.5:
        for k in set(own) | set(own0):
            rate[k] = (own.get(k, 0) - own0.get(k, 0)) / hours
W = yaml.safe_load(open(os.path.join(R, 'model', 'ledger.yaml')))
by_name = {v: k for k, v in NAME.items()}
watch = []
for w in W.get('watch', []):
    code = by_name.get(w['item'], w['item'])
    o, r = own.get(code, 0), rate.get(code)
    row = {'item': w['item'], 'owned': o, 'rate_hr': r, 'owner': w.get('owner'), 'why': w.get('why')}
    if w.get('target'):
        short = max(0, w['target'] - o); row.update(target=w['target'], shortage=short)
        row['eta_days'] = (short / r / 24) if (short and r and r > 0) else (0 if not short else None)
        if short and not (r and r > 0): row['flag'] = 'no net income: change producer'
    if r and r < 0:
        row['runout_days'] = o / -r / 24
    watch.append(row)
runout = []
for k, r in rate.items():
    if not TYPE.get(k, '').startswith(STACK) or 'EQUIP' in TYPE.get(k, ''): continue
    if r < 0 and own.get(k, 0) > 0:
        days = own[k] / -r / 24
        if days < RUNOUT_DAYS: runout.append({'item': NAME.get(k, k), 'owned': own[k], 'rate_hr': r, 'runout_days': days})
    elif r < 0 and own.get(k, 0) == 0:
        runout.append({'item': NAME.get(k, k), 'owned': 0, 'rate_hr': r, 'runout_days': 0})
runout.sort(key=lambda x: x['runout_days'])
# stamp material needs: only stamps AutoReview targets (data-driven, never picked by hand)
sys.path.insert(0, os.path.join(R, 'tools'))
from stamp_cost import cost as stamp_cost
review = json.load(gzip.open(os.path.join(R, 'snapshots', cur_stamp, 'review.json.gz')))
st = next(s for w in review['worlds'] for s in w['sections'] if s['name'] == 'Stamps')
targets = {}
def walk(n):
    for a in n.get('items', []):
        if 'items' in a: walk(a); continue
        m = re.match(r"(?:\w+: )?(.+? Stamp)\b", a.get('label', ''))
        if m and not a.get('completed') and str(a.get('goal', '')).isdigit() and 'Exalt' not in n.get('name', '') + n.get('tab', ''):
            targets[m.group(1)] = max(targets.get(m.group(1), 0), int(a['goal']))
    for t in n.get('tabs', []): walk(t)
for gr in st['groups']:
    if 'Exalt' not in gr.get('name', ''): walk(gr)
stamps = []
for nm, tg in targets.items():
    try: c = stamp_cost(nm, tg)
    except StopIteration: continue
    if c['level'] >= tg: continue
    stamps.append({k: c[k] for k in ('stamp', 'level', 'max', 'target', 'coins', 'material', 'owned', 'next_raise', 'total_mat')})
stamps.sort(key=lambda x: x['next_raise'] / max(1, x['owned']))
out = {'stamps': stamps, 'stamp': cur_stamp, 'vs': prev[-1] if prev else None, 'hours': hours, 'watch': watch, 'runout': runout[:25]}
json.dump(out, open(os.path.join(R, 'model', 'ledger.json'), 'w'), indent=1)
f = lambda x: f"{x:,.0f}" if x is not None else '?'
L = [f"# Material ledger · save {cur_stamp} vs {out['vs']} ({hours or 0:.1f} h)", '', '## Watchlist']
for w in watch:
    L.append(f"- {w['item']}: {f(w['owned'])}" + (f" / target {f(w['target'])}, short {f(w['shortage'])}" if w.get('target') else '')
             + (f", {w['rate_hr']:+,.0f}/hr" if w['rate_hr'] is not None else ', rate n/a')
             + (f", ETA {w['eta_days']:.1f} d" if w.get('eta_days') else '') + (f", RUNS OUT {w['runout_days']:.1f} d" if w.get('runout_days') else '')
             + (f" · {w['flag']}" if w.get('flag') else '') + f" · {w['owner']}: {w['why']}")
L += ['', f'## Falling, out within {RUNOUT_DAYS} days']
L += [f"- {x['item']}: {f(x['owned'])} at {x['rate_hr']:+,.0f}/hr -> {x['runout_days']:.1f} d" for x in runout[:25]] or ['- none']
L += ['', '## Stamp material needs (AutoReview targets; vial cap applied, sigil/atom reducers not)']
L += [f"- {x['stamp']} {x['level']} (max {x['max']}) -> {x['target']}: next raise {x['next_raise']:,.0f} {x['material']} (own {x['owned']:,})" + (' READY' if x['next_raise'] <= x['owned'] else '') + f" · to target {x['total_mat']:,.0f}" for x in stamps]
open(os.path.join(R, 'model', 'ledger.md'), 'w').write('\n'.join(L) + '\n')
print('\n'.join(L))
