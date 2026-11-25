"""Extra card steps (Zack 2026-11-20 sweep). Every line is from the save/Toolbox/AutoReview plus a named source,
or says "my read". Used by cards2.py. Each function returns {name: [step, ...]} (house) or a talent ranking.
"""
import gzip, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAPN = (ROOT / 'snapshots' / 'LATEST').read_text().strip()
SNAP = ROOT / 'snapshots' / SNAPN
TB = SNAP / 'toolbox'

def tb(page, tab=None):
    raise RuntimeError('extras.tb is retired: use model/data.py')

def _old_tb(page, tab=None):
    try:
        o = json.load(open(TB / f'{page}.json'))
        return o['tabs'][tab]['text'] if tab else '\n'.join(t['text'] for t in o['tabs'].values())
    except Exception:
        return ''

REVIEW = gzip.open(SNAP / 'review.json.gz').read().decode()

def step(do, why='', sub=None):
    return {'do': do, 'why': why, 'sub': sub or []}

# ---- Royal Guardian super talents: hold until the Royal Armory shelf unlocks (Griffy + Pulse 2026-08) ----
RG_SUPERS = [  # Pulse 2026-09-20 super talk, RG section (newest)
    ('Pit of Pages', 'Pulse: a 5-6x true multi, 100% worth a super on the scaling setup (feeds the POW goal)'),
    ('Marble talent', 'Pulse: 100% worth a super'), ('Orb talent', 'Pulse: 100% worth a super, probably top five'),
    ('Regal Intervention', 'Pulse: one point gives most of it'), ('Warbound Politics', 'Pulse: worth it on the main or second RG'),
    ('Built Different', 'Pulse: one point for a lot of base strength'), ('Grand Vein', 'Pulse: worth it if Grand Discoveries are slow'),
    ('Castle Convine + Royal Armory talent', 'Pulse: worth it on your second RG'),
]

def rg_supers():
    m = re.search(r"Super Talent Unban[^\"]*?Requires (\d+) more Upgrade Levels", REVIEW)
    left = int(m.group(1)) if m else None
    if left is None:
        return {}
    near = left <= 50
    s = step(f"Royal Guardian super talents: locked, {left} more Royal Armory upgrade levels" + (' (close, line up the points)' if near else ''),
             'Griffy + Pulse: RG talents can only be supered after that shelf. Hold these picks for it',
             [f"{n}: {w}" for n, w in RG_SUPERS[:5]])
    return {'Autistastic': [s], 'Autistomatic': [s]}

# ---- cooking mastery conditions (Zemo owns cooking) ----
LADLES = '4,183'   # Zemo inventory, save 20261120T0452 (checked 2026-11-20)

def mastery_plan():
    from data import load
    D = load(); M = D.get('account.cooking.cookingMastery', True)
    if not M: return {}
    lad = D.item_count('Ladle') if hasattr(D, 'item_count') else None
    return {'Autiszemo': [step(f"Cooking mastery level {M.get('level')} (rank {M.get('rank')}): use your ladles" + (f" ({lad:,.0f} owned)" if lad else ''),
        'mastery ranks unlock with ladles used and Divorce Cake levels',
        ['Use your ladles on Divorce Cake, one at a time, claiming each kitchen between (Griffy 2026-11). That counts as ladles used and levels the cake (my read: both conditions at once)',
         'Pulse: the daily ladle system dumps all ladles on your lowest-timer meal, so do this before it runs',
         'Pulse: push mastery to 15'])]}

# ---- research grid points + research level gate ----
def research_plan():
    from data import load
    R = load().system('research')
    sub = []
    if R['gridPTSavailable']:
        sub.append(f"Grid points: {R['gridPTSavailable']} unspent. Hold them: Pulse 2026-10-31 keeps about 12 on hand (Jelly needs 12, Menagerie 8)")
    if R.get('nextUnlockResearchLv'): sub.append(f"Next research unlock at level {R['nextUnlockResearchLv']}")
    return {'Autistotle': [step('Research: points and next level', 'research gates W7 upgrades', sub)]} if sub else {}

# ---- lab chips (rotate weekly in the lab shop) + jewels ----
CHIP_GOAL = {  # end-goal chips, sourced
    'Chocolatey Chip': ('Autistastic', 'Autistomatic'),       # Pulse 2026-09-23/11-11, Griffy 2026-11-07: meta, crystal + money farming
    'Omega Nanochip': ('Autistocat', 'Autistastic', 'Autisticles', 'Autistabish'),   # Pulse 2026-09: double the drop multi card (top-left)
    'Omega Motherboard': ('Autistocat', 'Autistastic', 'Autisticles', 'Autistabish'),  # bottom-right doubler
    'Silkrode Processor': ('Autistastic',),                    # pendant doubler for the money pendant (AutoReview chip text, Griffy 2026-01)
}
CHIP_SRC = {'Chocolatey Chip': 'Pulse: meta-defining, the most important if you lack it; rarely in rotation, farm its materials ahead',
            'Omega Nanochip': 'Pulse: doubled slot for the drop rate multi card', 'Omega Motherboard': 'Pulse: doubled slot for the drop rate multi card',
            'Silkrode Processor': 'Griffy: the money pendant doubled by the pendant doubler'}

def chips_plan(chars):
    out = {}
    for c in chars:
        n = c['character_name']; have = set(c.get('equipped_lab_chips') or [])
        miss = [ch for ch, who in CHIP_GOAL.items() if n in who and ch not in have]
        if miss:
            out.setdefault(n, []).append(step('Lab chips: end-goal chips missing, buy when they rotate in', 'chips rotate weekly; missed means wait',
                                              [f"{ch}: {CHIP_SRC[ch]}" for ch in miss]))
    jl = sorted(set(re.findall(r'"label": "Jewel of ([^:"]+): Permanently unlocks a new Jewel in the LabRequires (\d+) more Upgrades', REVIEW)), key=lambda x: int(x[1]))
    if jl:
        out.setdefault('Autistocat', []).append(step('Lab jewels: missing ones unlock from Royal Armory upgrades', 'not on the weekly rotation',
                                                     [f"Jewel of {a}: {b} more upgrades" for a, b in jl]))
    return out

# ---- Autistronaut and Arcane Cultist roster rules (AutoReview code) ----
def naut_note():
    return {'Autistronaut': [step('If he ever becomes an Arcane Cultist: nothing moves by roster position',
        'AutoReview: tachyons use the BEST Arcane Cultist Tesseract and Backup Energy levels; the AC family bonus uses the highest-level AC (Autistocat now)',
        ['So he only takes over once his Tesseract/Backup Energy talent levels or class level pass Autistocat', 'Not like Super CHOW/WOW, which track the last Death Bringer in the roster'])]}

# ---- Autistopher super talents odd data ----
def topher_note():
    return {'Autistopher': [step('Super talents: the save still shows Siege Breaker talents in his super slots (from before his class switch)',
        'check in game whether they can be cleared; until then nothing is spent there', [])]}

# ---- voting: every option on the ballot, its vote share, why / why not (Zack decides) ----
VOTE_WHY = {   # keyed by a phrase in the option text
    'Artifact Find': 'for: Ticles is hunting missing artifacts; Pointagon makes Chapter Lore 1.3x, and Chapters are in your POW (goal). against: only matters while boats hunt',
    'Refinery Cycle': 'for: faster salts (Griffy: invest in refinery cycles while salts are locked). against: no tie to the goal',
    'cash earned': 'for: money mode on Autistastic gets doubled coins that week. against: only if you farm coins that week',
    'Shiny Critters': 'for: a shiny week; the shiny Tottoise greenstack is the hardest, so this is when to farm it (switch traps to shiny). against: no vial needs a shiny now',
    'Vials': 'for: every vial 1.75x for the week, account-wide. against: nothing specific to the goal',
    'Starsigns': 'for: all star signs 1.9x. against: low impact for your setup (my read)',
}
def voting():
    from data import load
    V = load().system('ballot'); out = []
    def fmt(t, v):
        t = t.replace('_', ' ')
        try: v = float(v)
        except (TypeError, ValueError): return t.replace('{', '').replace('}', '')
        return t.replace('{', f"{v:g}").replace('}', f"{1 + v / 100:.2f}")
    for label, rows in (('Bonus Ballot', [(fmt(b['0'], b.get('1')), b['percent']) for b in V['bonuses'] if b.get('active') or b.get('percent')]),
                        ('Meritocracy', [(fmt(b['description'], b.get('bonus')), b['percent']) for b in V['meritocracyBonuses'] if b.get('active') or b.get('percent')])):
        if not rows: continue
        out.append(f"{label}, on the ballot now:")
        for o, pct in rows:
            w = next((v for k, v in VOTE_WHY.items() if k.lower() in o.lower()), 'needs checking')
            out.append(f"  {o[:80]} ({pct}% now). {w}")
    return {'Autistotle': [step('Voting: your pick (reset day)', 'every option on the ballot, with why for and against', out)]} if out else {}

# ---- talent ranking: top 5 per character + overall 1-55 ----
TIER = {'High': 3, 'Medium': 2, 'Low': 1}
def talent_rank(cards):
    try:
        g = json.load(open(ROOT / 'model' / 'guidance.json'))
        claims = [x for v in g.values() if isinstance(v, list) for x in v if x.get('date', '') >= '2025-06']
    except Exception:
        claims = []
    def why(name):
        k = name.lower().split(' ')[0]
        hits = sorted((x for x in claims if name.lower() in x['say'].lower()), key=lambda x: x['date'], reverse=True)
        return f"{ {'griffybit': 'Griffy', 'pulseidle': 'Pulse', 'nocturne': 'Nocturne'}.get(hits[0]['who'], hits[0]['who'])}: {hits[0]['say'][:90]}" if hits else 'AutoReview library priority'
    allrows = []
    per = {}
    for cd in cards:
        rows = []
        for grp, lst in (cd.get('talents') or {}).items():
            kind, tier = grp.split(' ')
            for s in lst:
                m = re.match(r'(.+) (\d+)/(\d+)$', s)
                if not m: continue
                name, lv, mx = m.group(1), int(m.group(2)), int(m.group(3))
                if lv >= mx: continue
                rows.append({'char': cd['name'], 'talent': name, 'lv': lv, 'max': mx, 'kind': kind, 'tier': TIER[tier]})
        rows.sort(key=lambda r: (-r['tier'], -(r['max'] - r['lv'])))
        per[cd['name']] = rows[:5]
        allrows += rows[:5]
    allrows.sort(key=lambda r: (-r['tier'], -(r['max'] - r['lv'])))
    for i, r in enumerate(allrows, 1):
        r['rank'] = i; r['why'] = why(r['talent'])
    json.dump({'save': SNAPN, 'ranked': allrows}, open(ROOT / 'plans' / f'talents_{SNAPN}.json', 'w'), indent=1)
    out = {}
    for n, rows in per.items():
        if rows:
            out[n] = [step('Talents to level next (Library checkouts)', 'ranked across all 11 characters',
                           [f"#{r['rank']} {r['talent']} {r['lv']} -> {r['max']} ({r['why']})" for r in rows])]
    return out

def all_house(cards, chars):
    parts = [rg_supers(), mastery_plan(), research_plan(), chips_plan(chars), naut_note(), topher_note(), voting(), talent_rank(cards)]
    out = {}
    for p in parts:
        for n, steps in p.items(): out.setdefault(n, []).extend(steps)
    return out
