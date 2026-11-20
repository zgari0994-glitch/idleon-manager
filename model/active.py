"""Active plan (Zack 2026-11-19): one block at the end of all cards.
Overnight (top 2): one long push for a character left active on the PC.  Tonight (top 5): pick as many as you want.
Morning: things to keep ticking with the game up while at work.
Ranking = need first (model/priority.py), then the job's own importance. Plain-English lines, each names its character."""
import json
import yaml
from tbhelp import ROOT


def J(name):
    try: return json.load(open(ROOT / 'model' / f'{name}.json'))
    except Exception: return {}


def candidates():
    C = []
    cp, gr, sp, em, kr, eq, dn = J('compass'), J('grimoire'), J('spelunking'), J('emperor'), J('killroy'), J('equinox'), J('deathnote')
    # overnight: long single-task pushes
    if cp: C.append({'kind': 'overnight', 'who': 'Autistacular', 'section': 'Compass', 'base': 3,
                     'do': f"Tempest Form farming for stardust and medallions ({cp.get('total_levels')} compass levels now). Elemental Path for tier 4 needs about 9.5M more stardust, and medallions go 27 -> 39.",
                     'src': 'Griffy: farm all medallions'})
    if gr: C.append({'kind': 'overnight', 'who': 'Autiszemo', 'section': 'The Grimoire', 'base': 3,
                     'do': f"Wraith Form bone farming at {gr['best_mobs'][0][0] if gr.get('best_mobs') else 'the best bones mob'}. {gr['next_unlock'][1] - gr['total']} upgrade levels to the next unlock ({gr['next_unlock'][0]})." if gr.get('next_unlock') else 'Wraith Form bone farming.',
                     'src': 'Griffy: max AFK gains before spending bones'})
    for t in yaml.safe_load(open(ROOT / 'model' / 'jobs.yaml')).get('active_tasks', []):
        kind = 'overnight' if t['minutes'] >= 240 else 'tonight' if t['minutes'] >= 20 else 'morning'
        C.append({'kind': kind, 'who': t['owner'], 'section': t.get('section', ''), 'base': 4 - t['importance'], 'do': t['task'], 'src': t['src']})
    # tonight: active sessions
    if sp: C.append({'kind': 'tonight', 'who': 'Autistomatic', 'section': 'Spelunking', 'base': 3,
                     'do': f"Delve for amber and depth ({sp.get('amber', 0):,.0f} amber now) and read the rest of today's pages ({sp.get('pages')}). Every cave gets other systems moving.", 'src': 'my read'})
    if em and em.get('attempts', '0').split(' / ')[0] != '0':
        C.append({'kind': 'tonight', 'who': 'Autiszemo', 'section': 'Emperor', 'base': 2,
                  'do': f"Emperor showdowns: {em['attempts']} attempts, push past {em['best']}.", 'src': 'Zack: best fighter pushes for bonuses'})
    if kr: C.append({'kind': 'tonight', 'who': 'Killroy owner this week', 'section': 'Killroy', 'base': 1,
                     'do': "One big Killroy run aiming for 2,000 kills in a room (best so far 1,296). That finishes an Equinox challenge (+35% bar fill).", 'src': 'Equinox challenge'})
    if dn and dn.get('cur'):
        k = sorted([(m, w, v) for m, (w, v) in dn['cur']['kills'].items() if 0 < v < 1e9 and w != 'Minibosses'], key=lambda x: -x[2])[:1]
        if k: C.append({'kind': 'tonight', 'who': 'Autiszemo', 'section': 'Death Note', 'base': 1,
                        'do': f"Finish the {k[0][0]} Eclipse skull ({(1e9 - k[0][2]) / 1e6:,.0f}M kills left).", 'src': 'Death Note'})
    # morning: game up while at work
    if eq and eq.get('fill_hr'): C.append({'kind': 'morning', 'who': 'Autistopher', 'section': 'Equinox', 'base': 3,
                                           'do': f"Spend the Equinox bar whenever you pass the PC. It fills in about {eq['bar'][1] / eq['fill_hr'] * 60:.0f} minutes.", 'src': 'Toolbox Equinox'})
    C.append({'kind': 'morning', 'who': 'Autisticles', 'section': 'Arcade', 'base': 2, 'do': 'Claim Arcade balls a couple of times (one every 39 min, the bank caps).', 'src': 'Toolbox Arcade'})
    C.append({'kind': 'morning', 'who': 'Autistastic', 'section': 'Gaming', 'base': 2, 'do': 'Harvest the gaming garden every few hours (sprouts regrow every 2.5 hours and stop at 20).', 'src': 'Toolbox Gaming'})
    C.append({'kind': 'morning', 'who': 'Autistabish', 'section': 'The Hole', 'base': 2, 'do': 'Check the Hole study timers and bump each level as it comes ready.', 'src': 'Toolbox Hole'})
    C.append({'kind': 'morning', 'who': 'every character', 'section': 'Prayers', 'base': 1, 'do': 'Set prayers to what each character is doing today (AFK vs active).', 'src': 'Zack: prayers stay fluid per task'})
    C.append({'kind': 'morning', 'who': 'Autistopher', 'section': 'Owl', 'base': 1, 'do': 'Clickers: buy Owl, Bubba and Poppy upgrades as feathers stack up.', 'src': 'Toolbox Owl'})
    return C


def build():
    pr = J('priority'); needs = [x['section'] for x in pr.get('needs', [])]
    for c in candidates():
        pass
    C = candidates()
    for c in C:
        c['need'] = (len(needs) - needs.index(c['section'])) if c['section'] in needs else 0
        c['score'] = c['need'] * 10 + c['base']
    pick = lambda k, n: sorted([c for c in C if c['kind'] == k], key=lambda c: -c['score'])[:n]
    o = {'overnight': pick('overnight', 2), 'tonight': pick('tonight', 5), 'morning': pick('morning', 6), 'needs': needs[:3]}
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
