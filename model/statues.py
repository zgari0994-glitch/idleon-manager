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
    t = list(dict.fromkeys(o['targets']))
    L = [f"Statue goals: {'; '.join(x.split(': ', 1)[-1] for x in t[:3])}."]
    if o['prereq']: L.append('Before farming Onyx: ' + '; '.join(p.split(':')[0] for p in o['prereq'][:3]) + '.')
    L.append('Griffy: golden statues only keep the highest level, so stockpile them and turn them all in on one character. Turning in every statue at once can wipe stored greenstacks.')
    return L


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)
