"""Stamps planner: exalt pick, AutoReview priority stamps (coin level-ups + max-level raises), shared-resource check -> Topher's Stamps block.

Costs: tools/stamp_cost.py (Toolbox stamp formulas). Priority = AutoReview 'high-priority' tiers, raised when a priority section needs it
(Zack 2026-11-19: focus stamp levels when they push a priority section forward). Materials shared with other systems are flagged.
"""
import gzip, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
SNAP = ROOT / 'snapshots' / (ROOT / 'snapshots' / 'LATEST').read_text().strip()


def _ar(sec):
    r = json.load(gzip.open(SNAP / 'review.json.gz'))
    for w in r['worlds']:
        for s in (w.get('sections') or []):
            if s.get('name') == sec: return s


def build():
    import stamp_cost as SC
    s = _ar('Stamps')
    pri, exalt_rec, exalt_avail, total = [], [], None, None
    for g in s['groups']:
        for it in g['items']:
            for x in it.get('items', []):
                if x.get('completed'): continue
                lab = x['label']
                if g['name'].startswith('Improve high-priority'):
                    m = re.match(r'(?:\w+): (.+)', lab); nm = m.group(1) if m else lab
                    pri.append({'stamp': nm, 'cur': x['cur'], 'goal': x['goal'], 'tier': it.get('tab', '')})
                elif 'Recommended Exalts' in (it.get('tab') or ''):
                    exalt_rec.append(re.sub(r'^\w+: ', '', lab))
                elif lab.startswith('Total Exalted Stamps spent'):
                    exalt_avail = (x['cur'], x['goal'])
                elif lab.startswith('Total Stamp Levels') and total is None:
                    total = (x['cur'], x['goal'])
    seen, rows = set(), []
    for p in pri:
        if p['stamp'] in seen: continue
        seen.add(p['stamp'])
        nm = p['stamp'] if p['stamp'].endswith('Stamp') else p['stamp'] + ' Stamp'
        try:
            goal = max(int(q['goal']) for q in pri if q['stamp'] == p['stamp'])
            c = SC.cost(nm, goal); n1 = SC.cost(nm, c['level'] + 1) if c['level'] < c['max'] else None
        except Exception as e:
            rows.append({'stamp': nm, 'err': str(e)[:60]}); continue
        rows.append({'stamp': nm, 'level': c['level'], 'max': c['max'], 'goal': goal, 'coins_to_goal': c['coins'], 'next_coin': n1['coins'] if n1 else None,
                     'capped': c['level'] >= c['max'], 'material': c['material'], 'owned': c['owned'], 'next_raise': c['next_raise'], 'raises_left': len(c['raises']),
                     'tier': p['tier']})
    out = {'snapshot': SNAP.name, 'money': SC.MONEY, 'rows': rows, 'exalt_rec': exalt_rec, 'exalt_avail': exalt_avail, 'total_levels': total}
    json.dump(out, open(ROOT / 'model' / 'stamps.json', 'w'), indent=1)
    return out


SHARED = {'Soul': 'also prayers, vials, bubbles, salts', 'Butterfly': 'also printer prints (Bug prints)', 'Fly': 'printer sample target',
          'Copper': 'printer sample target / refinery', 'Oak': 'printer sample target'}


def card_lines(o):
    import spend
    L = []
    if o['exalt_avail']:
        a, b = o['exalt_avail']
        if str(a) != str(b): L.append(f"TOP: you have an unused stamp exalt. AutoReview's order: {', '.join(o['exalt_rec'][:3])}.")
    lv, cap = [], []
    for r in o['rows']:
        if r.get('err') or 'material' not in r: continue
        if r['capped']:
            ok = r['owned'] >= r['next_raise']
            cap.append((ok, r['stamp'].replace(' Stamp', ''), r['material'], spend.h(r['next_raise'] - r['owned'])))
        elif r['next_coin']: lv.append(r['stamp'])
    if lv: L.append('Level these with coins: ' + ', '.join(lv[:6]) + '.')
    rdy = [c[1] for c in cap if c[0]]; short = [f"{c[1]} ({c[3]} more {c[2]})" for c in cap if not c[0]]
    if rdy: L.append(f"Raise the max level on {', '.join(rdy[:6])}, you have the materials.")
    if short: L.append('Max-level raises still short: ' + ', '.join(short[:4]) + '.')
    L.append('If a stamp material is also used by another system, the card flags it. The Envelope Pile sigil makes max-level raises a lot cheaper.')
    return L


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)
