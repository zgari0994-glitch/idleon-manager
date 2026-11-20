"""Greenstacks planner (10M of an item = a greenstack): near-done stacks, daily vendor buys, endangered items, protect list + replace math.
-> Autistotle's Greenstacks block; writes model/protect.json that spenders (prayers, printer swaps, stamps) read.
Zack 2026-11-19: spending a near-stack is fine, but the card must say it's gone and how it gets replaced.
"""
import gzip, json, re
from pathlib import Path
import rates

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / 'snapshots' / (ROOT / 'snapshots' / 'LATEST').read_text().strip()
STACK = 1e7
REPLACE = {'Soul': 'Worship (souls from tower defense / worship waves)', 'Salt': 'Refinery (salt output vs what the chain consumes)',
           'Potion': 'W4 town vendor, time-gated daily buys', 'Snow Ball': 'W3 monster drops'}


def build():
    r = json.load(gzip.open(SNAP / 'review.json.gz'))
    near, vendor, endangered, tier = [], [], [], None
    for w in r['worlds']:
        for s in (w.get('sections') or []):
            if s.get('name') == 'Greenstacks':
                tier = s.get('tier')
                for g in s['groups']:
                    for it in g['items']:
                        for x in it.get('items', []):
                            if x.get('completed'): continue
                            m = re.match(r'([\d.]+)%', str(x['cur']))
                            if not m: continue
                            pct = float(m.group(1)); name = re.sub(r'\s*\(W\d Town\)', '', x['label'])
                            rec = {'item': name, 'pct': pct, 'group': g['name'], 'tab': it.get('tab', '')}
                            if 'Vendor' in rec['tab'] and g['name'].startswith('Timegated'): vendor.append(rec)
                            if pct >= 75: near.append(rec)
            if s.get('name') == 'Endangered Greenstacks':
                for g in s['groups']:
                    if g['name'].startswith('Still'):
                        for it in g['items']:
                            for x in it.get('items', []): endangered.append(x['label'])
    seen = set(); near = [x for x in sorted(near, key=lambda x: -x['pct']) if not (x['item'] in seen or seen.add(x['item']))]
    for x in near:
        i = rates.info(x['item'])
        x['owned'] = i['owned'] if i else STACK * x['pct'] / 100
        x['need'] = max(0, STACK - x['owned'])
        x['rate_hr'] = i and i['rate_hr']
        x['window'] = i and i['window']
        x['replace'] = next((v for k, v in REPLACE.items() if k in x['item']), 'its normal source')
    protect = {x['item']: {'owned': x['owned'], 'need_for_stack': x['need'], 'rate_hr': x['rate_hr'], 'replace': x['replace']} for x in near}
    json.dump(protect, open(ROOT / 'model' / 'protect.json', 'w'), indent=1)
    out = {'snapshot': SNAP.name, 'tier': tier, 'near': near, 'vendor': sorted({v['item']: v for v in vendor}.values(), key=lambda v: -v['pct']), 'endangered': endangered}
    json.dump(out, open(ROOT / 'model' / 'greenstacks.json', 'w'), indent=1)
    return out


def card_lines(o):
    L = []
    if o['near']: L.append('Close to a greenstack, don\'t spend these: ' + ', '.join(f"{x['item']} ({x['pct']:.0f}%)" for x in o['near']) + '. Other cards will warn you before using them.')
    if o['vendor']: L.append('Buy the daily vendor items that are closest to a greenstack: ' + ', '.join(v['item'] for v in o['vendor'][:5]) + '.')
    if o['endangered']: L.append(f"{len(o['endangered'])} quest items still need greenstacks while you can still get them.")
    L.append("Your call on the free exalt: Pulse says the vendor shop stamp, AutoReview says Summoner Stone.")
    return L


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)
