"""Statues planner: Onyx targets with their farmer, crystal-spawn prereqs, statue value levers, turn-in rules -> Autisticles' turn-in block.
Farmers' own cards already carry their statue Push lines (jobs.yaml statue jobs)."""
import gzip, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / 'snapshots' / (ROOT / 'snapshots' / 'LATEST').read_text().strip()


def build():
    r = json.load(gzip.open(SNAP / 'review.json.gz')); out = {'snapshot': SNAP.name, 'targets': [], 'prereq': [], 'value': [], 'onyx': []}
    for w in r['worlds']:
        for s in (w.get('sections') or []):
            if s.get('name') != 'Statues': continue
            out['tier'] = s.get('tier')
            for g in s['groups']:
                for it in g['items']:
                    for x in it.get('items', []):
                        if x.get('completed'): continue
                        rec = f"{x['label'][:95]} ({x['cur']} -> {x['goal']})"
                        if g['name'].startswith('Beef'): out['targets'].append(rec)
                        elif g['name'].startswith('To-Do'): out['prereq'].append(rec)
                        elif it.get('tab', '').startswith('Effect bonuses'): out['value'].append(rec)
                        elif 'Onyx' in x['label']: out['onyx'].append(rec)
    json.dump(out, open(ROOT / 'model' / 'statues.json', 'w'), indent=1)
    return out


def card_lines(o):
    L = [f"Statues {o.get('tier')}. AutoReview targets (farmer in brackets): " + '; '.join(dict.fromkeys(o['targets']))]
    if o['prereq']: L.append('Before dedicated Onyx farming: ' + '; '.join(o['prereq']))
    if o['value']: L.append('Statue value levers: ' + '; '.join(o['value']))
    L.append('Turn-in rules (Griffy): golden statues keep only the highest level, so stockpile and dump into one character instead of splitting; '
             'depositing all statues can destroy stored greenstacks (2025-12).')
    return L


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)
