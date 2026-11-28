"""Active plan block (Zack 2026-11-19; v2 2026-11-27, model-driven).
Overnight = Zack's plan only (brain/plans.yaml slot overnight_active = Cat). Nobody else gets it; night watch flags rivals.
Tonight / morning = top Task Scores (model/score.py). Owners come from jobs.yaml (score.owner_of), never hardcoded here."""
import json
from tbhelp import ROOT


def build():
    import score as S
    T = S.tasks()
    ov = [{'who': p['who'], 'do': f"Zack's plan ({p['date']}): {p['do']}", 'src': 'zack', 'need': 0, 'section': ''}
          for p in S.P['plans'] if p.get('slot') == 'overnight_active']
    fl = S.cat_flag()
    if fl: ov.append({'who': S.P['slots']['overnight_active'], 'do': fl, 'src': 'night watch (score.py)', 'need': 0, 'section': ''})
    top3 = {x['section'] for x in S.needs()[:3]}
    row = lambda t: {'who': t['owner'], 'do': f"{t['task']} (score {t['score']})", 'src': t['src'], 'need': int(t.get('section') in top3), 'section': t.get('section', '')}
    mor = sorted([t for t in T if t.get('slot') == 'morning'], key=lambda t: -t['score'])[:6]
    ton = sorted([t for t in T if t.get('slot') != 'morning' and not str(t['id']).startswith('need:') and t.get('minutes', 30) < 240], key=lambda t: -t['score'])[:5]
    o = {'overnight': ov, 'tonight': [row(t) for t in ton], 'morning': [row(t) for t in mor], 'needs': [x['section'] for x in S.needs()[:3]]}
    json.dump(o, open(ROOT / 'model' / 'active.json', 'w'), indent=1)
    return o


def lines(o):
    f = lambda c: f"{c['who']}: {c['do']}" + (' (biggest-need system)' if c['need'] else '') + f" [{c['src']}]"
    L = ['ACTIVE PLAN']
    L.append('Overnight on the PC (pick one):'); L += [f"  {i + 1}. {f(c)}" for i, c in enumerate(o['overnight'])]
    L.append('Active play tonight (do as many as you like, best first):'); L += [f"  {i + 1}. {f(c)}" for i, c in enumerate(o['tonight'])]
    L.append('Morning, game up while at work:'); L += [f"  - {f(c)}" for c in o['morning']]
    return L


if __name__ == '__main__':
    print('\n'.join(lines(build())))
