"""Build the brother's jobs.yaml from Zack's model/jobs.yaml (Zack 2026-11-19: "follow the setup of my account").
Same jobs, same owners by class role. Zack-account specifics (notes, numbers, AFK spots, active tasks, locked
targets, his priorities) are dropped, since they describe Zack's account. Every job gets basis 'auto'.
Duplicate classes: higher combat level keeps the class jobs (auto pick, change ROLE below to override).
Usage: python3 accounts/brother/make_jobs.py   (run from repo root)
"""
import yaml, os, json
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Z = yaml.safe_load(open(os.path.join(R, 'model', 'jobs.yaml')))

# Zack's character -> brother's character (by class role)
ROLE = {
    'Autistacular': 'IdleOnLech',      # Wind Walker
    'Autistastic':  'IdleOnLechII',    # Royal Guardian #1 (509 > 493)
    'Autistomatic': 'IdleOnLechVIII',  # Royal Guardian #2
    'Autistocat':   'IdleOnLechIII',   # Arcane Cultist
    'Autiszemo':    'IdleOnLechIV',    # Death Bringer (only one)
    'Autistabish':  'IdleOnLechV',     # Elemental Sorcerer #1 (515 > 499)
    'Autistronaut': 'IdleOnLechIX',    # Elemental Sorcerer #2
    'Autisticles':  'IdleOnLechX',     # Siege Breaker #1 (518 > 506)
    'Autistotle':   'IdleOnLechVII',   # Voidwalker
    'Autistopher':  'IdleOnLechVI',    # 2nd Siege Breaker takes the account/light jobs (Zack rule)
    'Autistachio':  'IdleOnLechIX',    # no Beginner: light jobs go to ES #2 (lightest load)
}
ORDER = ['IdleOnLech'] + ['IdleOnLech' + r for r in 'II III IV V VI VII VIII IX X'.split()]
# jobs that only make sense for Zack's specific character
MOVE = {'Super CHOWs': 'IdleOnLechIV'}   # Death Note rest: only DB does CHOWs
DROP = ('Divinity to 40',)               # Beginner-only leveling job

KEEP = ('job', 'sections', 'weekly', 'timers', 'miniboss_max', 'rule', 'daily', 'feeds')
chars = {}
for zc, z in Z['characters'].items():
    bc = ROLE[zc]
    c = chars.setdefault(bc, {'afk': {'text': 'AFK spot: not set (auto setup)', 'src': 'GAP'}, 'jobs': []})
    for j in z.get('jobs', []):
        if any(j['job'].startswith(d) for d in DROP):
            continue
        nj = {k: v for k, v in j.items() if k in KEEP}
        nj['basis'] = 'auto'
        tgt = next((v for k, v in MOVE.items() if j['job'].startswith(k)), bc)
        chars.setdefault(tgt, {'afk': {'text': 'AFK spot: not set (auto setup)', 'src': 'GAP'}, 'jobs': []})['jobs'].append(nj)
    if z.get('first'):
        c['first'] = z['first']

remap = lambda o: ', '.join(ROLE.get(x.strip(), x.strip()) for x in str(o).split(','))
out = {
    'exclude': Z.get('exclude', []),
    'account_priority': {'text': 'Not set (auto setup)', 'set_by': 'auto'},
    'priorities': [],
    'characters': {k: chars[k] for k in ORDER if k in chars},
    'lever_routes': [{**r, 'owner': remap(r['owner'])} for r in Z.get('lever_routes', [])],
    'account_wide': Z.get('account_wide', []),
    'reference_only': Z.get('reference_only', []),
    'every_character': [{k: v for k, v in e.items() if k != 'note'} for e in Z.get('every_character', [])],
    'unassigned': None,
    'active_tasks': [],
    'locked': [],
    'alerts': [{**a, 'owner': remap(a['owner'])} for a in Z.get('alerts', [])],
    'timer_routes': [{**t, 'owner': remap(t['owner'])} for t in Z.get('timer_routes', [])],
}
hdr = ('# Brother (IdleOnLech) jobs: AUTO-GENERATED from Zack\'s model/jobs.yaml by make_jobs.py (2026-11-19).\n'
       '# Same jobs by class role; Zack-account notes/numbers dropped. Edit ROLE/MOVE in make_jobs.py, then rerun.\n')
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'jobs.yaml'), 'w').write(hdr + yaml.safe_dump(out, sort_keys=False, allow_unicode=True, width=200))
json.dump(ROLE, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'roles.json'), 'w'), indent=1)
print({k: len(v['jobs']) for k, v in out['characters'].items()})
