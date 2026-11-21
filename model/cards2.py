"""Cards v3 (Zack 2026-11-20): Goal card, then per character Dailies / Housekeeping / Goal part / Park.
Each step: one line, short why, nested a/b/c. No info dumps. Every line comes from planner output, the save or
Toolbox; anything not sourced says "needs checking". Builds on plans/latest.json (run plan.py first).
Run from the AutoReview folder: PYTHONPATH=.:<repo>/model python3 <repo>/model/cards2.py
Writes plans/cards_<save>.md, plans/cards.json, dashboard/cards.html.
"""
import gzip, json, re, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAPN = (ROOT / 'snapshots' / 'LATEST').read_text().strip()
SNAP = ROOT / 'snapshots' / SNAPN
TB = SNAP / 'toolbox'
J = lambda v: json.loads(v) if isinstance(v, str) else v
plan = json.load(open(ROOT / 'plans' / 'latest.json'))
CARDS = plan['cards'] if 'cards' in plan else plan
raw = json.load(gzip.open(SNAP / 'raw.json.gz')); raw = raw.get('data', raw)
chars = {c['character_name']: c for c in json.load(open(SNAP / 'chars.json'))['characters']}

def tbtext(page, tab=None):
    try:
        o = json.load(open(TB / f'{page}.json'))
        tabs = o['tabs']
        return tabs[tab]['text'] if tab else '\n'.join(t['text'] for t in tabs.values())
    except Exception:
        return ''

def num(s):
    s = str(s).replace(',', '').strip()
    m = re.match(r'([\d.]+)\s*([KMBT]|QQ|Q)?', s)
    if not m: return None
    mult = {'K': 1e3, 'M': 1e6, 'B': 1e9, 'T': 1e12, 'Q': 1e15, 'QQ': 1e18}.get(m.group(2) or '', 1)
    return float(m.group(1)) * mult

def short(n):
    for v, s in ((1e12, 'T'), (1e9, 'B'), (1e6, 'M'), (1e3, 'K')):
        if n >= v: return f"{n / v:.3g}{s}"
    return f"{n:.0f}"

# ---------------- GOAL ----------------
GOAL = {'name': 'Spelunking POW 900K', 'target': 900_000,
        'why': 'Frees the Pillar Coral fish (Seaweed Street cage), a new coral type. Spelunking is the biggest blocker.',
        'src': 'idleon.wiki Coral Reef (cage POW list); Zack approved 2026-11-20'}

def goal_card():
    sp = tbtext('spelunking', 'Upgrades')
    m = re.search(r'\nPower\n([\d,.]+)', sp)
    now = num(m.group(1)) if m else None
    out = {'name': GOAL['name'], 'why': GOAL['why'], 'now': now, 'target': GOAL['target'], 'prereqs': [], 'levers': [], 'unknown': []}
    # Sushi: Live Octopus 3x POW; fuel cap vs next unlock; Research 28 gate
    su = tbtext('sushi', 'Sushi')
    cap = re.search(r'Fuel\n[\d,]+ / ([\d,]+)\n', su); nxt = re.search(r'Next unlock\n([^\n(]+)\(([\d,]+) fuel\)', su)
    uniq = re.search(r'Unique sushi\n(\d+)', su)
    best_research = max((c['skills'].get('Research') or 0) for c in chars.values())
    if cap and nxt and num(cap.group(1)) < num(nxt.group(2)):
        out['prereqs'].append({'who': 'Autisticles', 'do': f"Raise sushi fuel cap to {nxt.group(2)} so {nxt.group(1).strip()} can cook (cap is {cap.group(1)})"})
    if best_research < 28:
        out['prereqs'].append({'who': 'Autistotle', 'do': f"Research level 28 on anyone (best is {best_research}). Unlocks Fuel Capacity II for sushi"})
    out['levers'].append({'who': 'Autisticles', 'do': f"Sushi: cook up to Live Octopus (sushi 21, you have {uniq.group(1) if uniq else '?'}). Gives 3x POW", 'size': '3x'})
    # Jelly
    je = tbtext('jelly', 'Layout')
    ob = re.search(r'Obstructions removed\n(\d+)\n(\d+)', je)
    out['levers'].append({'who': 'Autistocat', 'do': "Jelly Operator: reach Jellofish Fields (1B Pirate Underling portal kills, she has 3.1M at about 1.1M an hour, so about 5 weeks; then 60M Eggroll). Speed it up with Thanatos's Teachings (legend talent, Griffy) and Kill per Kill weeks. Then clear obstructions to Morning Glory: 1.30x POW", 'size': '1.3x'})
    # Amber shop
    for k, gain in (('Learning the POW', '+8%'), ('Discovering the POW', '+9%')):
        mm = re.search(re.escape(k) + r'\nLv (\d+) / [\d,]+\n[\s\S]{0,400}?\n([\d,.]+[KMB]?)\n/\n([\d,.]+[KMB]?)\n', sp)
        if mm: out['levers'].append({'who': 'Autistomatic', 'do': f"Spelunk shop: {k} to level {int(mm.group(1)) + 1} ({mm.group(3)} amber, have {mm.group(2)})", 'size': gain})
    out['levers'].append({'who': 'everyone', 'do': 'Spelunking levels: every level on anyone adds 13 base POW (Learning the POW), about +0.4% each. This is why most characters park on Spelunking', 'size': '+0.4%/lv'})
    # Dancing coral
    rf = tbtext('reef', 'Dancing Coral')
    vc = re.search(r'Vibrant Coral[\s\S]*?Isaccian Shrine LV\n(\d+)[\s\S]*?\n([\d.,]+[KMB]?)\n/\n([\d.,]+[KMB]?)', rf)
    if vc: out['levers'].append({'who': 'Autistachio', 'do': f"Dancing Coral: buy Vibrant Coral ({vc.group(3)}, have {vc.group(2)}). Then Isaccian Shrine above 200 gives +5% POW per level (Autistastic, shrine at {vc.group(1)})", 'size': '+5%/lv'})
    out['levers'].append({'who': 'account', 'do': 'Boomy Mine companion: 20x total POW, Griffy rates it S tier. Not owned; it comes from companion rolls (my read: the W7 Shallow Waters companion pool)', 'size': '20x'})
    cl = tbtext('clam', 'Compensations'); wc = re.search(r'Worker class\nLv (\d+)', cl)
    out['levers'].append({'who': 'Autisticles', 'do': f"Clam Work: worker class 12 gives 2x POW (now {wc.group(1) if wc else '?'}). Long term", 'size': '2x'})
    out['unknown'] = ['God rank: what it gives before spending points', 'Lab jewel and chip check', 'Ballot votes', 'Park spots marked needs checking', 'Spelunk tools (+% total POW)', 'Research grid daily POW boost', 'POW elixirs (need pages)', 'Sushi fuel costs past the next one']
    return out

# ---------------- step transform ----------------
CREATOR = re.compile(r'^(?:[\w+&\' /-]{1,40}:\s*)?(Griffy|Pulse|Nocturne|AutoReview|Next goal|older|Coming up|HOW|WHY)\b', re.I)
VERB = re.compile(r'^(TOP: )?(Buy|Spend|Collect|Use|Take|Leave|Put|Get|Level|Move|Swap|Switch|Push|Place|Hold|Unlock|Claim|Turn|Equip|Run|Set|Feed|Craft|Upgrade|Do|Make|Check|Vote|Park|Farm|Kill|Open|Replant|Send|Spin|Roll|Raise|Max|Finish|Add|Start|Cook|Breed|Deposit|Trade|Keep|Read|Clear|Fill|Go|Rotate|Plant|Harvest|Bring|Skip|Save|Stop|Don\'t|Do not|Focus|Pick|Time|Grind|Defeat|Beat|Reset|Restart|Activate|Discover|Summon|Drop|Sell|Refine|Transmute|Meditate|Link|Assign|Fix)\b', re.I)
DROPBLK = ('Levers for other jobs', 'Every character: Combat level', 'Timers ready', 'Super CHOWs', 'Traps')
WHY = {  # short plain why per system (my wording; the facts behind are on the planner pages)
    'Farming': 'crops feed discovery, cooking and shiny rate', 'Cooking': 'meals are account-wide buffs',
    'Grimoire': 'bone upgrades are account buffs', 'prints': 'prints feed resources while you sleep',
    'Emperor': 'daily attempts, bonuses stack', 'Prayers': 'wrong prayers cost gains', 'Worship': 'charge and souls keep worship moving',
    'Sailing': 'artifacts and treasure', 'Alchemy': 'bubbles and vials are account-wide', 'Breeding': 'pets and shinies',
    'Divinity': 'divinity points drive talent levels and class EXP', 'Lab': 'lab bonuses only work when connected',
    'Construction': 'build rate and atoms', 'Statue': 'statues are account buffs', 'Stamps': 'stamps are account buffs',
    'Greenstacks': 'greenstacks count for Equinox', 'Post Office': 'box points are permanent stats', 'Sneaking': 'jade and stealth',
    'Summoning': 'winner bonuses are big multipliers', 'Spelunking': 'Spelunking is the account goal', 'Trapping': 'critters for vials',
    'Gaming': 'bits and nuggets', 'Compass': 'portals and dust', 'Equinox': 'bar fills cloud bonuses', 'Kilroy': 'weekly',
    'Gallery': 'trophies and nametags for everyone', 'W7 minis': 'minis feed the goal', 'Research': 'research unlocks W7 upgrades',
}

def why_for(block):
    for k, v in WHY.items():
        if k.lower() in block.lower(): return v
    return ''

def first_sentence(s):
    s = re.sub(r'^TOP: ', '', s.strip())
    p = re.split(r'(?<=[a-z0-9)])\. (?=[A-Z])', s, maxsplit=1)
    return p[0].rstrip('.'), (p[1].rstrip('.') if len(p) > 1 else '')

STATUS = re.compile(r'^(\d[\d,.]* \w+ so far|Combat Lv|Worship level \d+, charge|Prayers on:|Equipped:)', re.I)

def _goal_line(s):
    m = re.match(r'^(?:[\w+&\' /-]{1,40}: )?Next goal: (.+?) ([\d.,]+[KMBT]?%?) -> ([\d.,∞]+[KMBT]?%?)$', s.strip())
    if m and m.group(3) != '∞': return f"Push {m.group(1).strip()} to {m.group(3)} (now {m.group(2)})"
    return None

def to_step(block, owner=''):
    """Zack 2026-11-20: never hide work. Keep every planner line that isn't a creator quote; 'nothing needed' only when none."""
    name = re.sub(r'^Every character: ', '', block['block'])
    lines = []
    for s in block.get('steps', []):
        if not isinstance(s, str) or not s.strip(): continue
        if any(o in s for o in OTHERS.get(owner, ())) and VERB.match(s): continue   # someone else's action
        g = _goal_line(s)
        if g: lines.append(g); continue
        if CREATOR.match(s): continue
        lines.append(s.strip())
    if not lines:
        return {'do': f"{name}: nothing needed", 'why': '', 'sub': []}
    acts = [l for l in lines if VERB.match(l) or l.startswith('Push ')]
    mainl = acts[0] if acts else next((l for l in lines if not STATUS.match(l)), lines[0])
    main, why = first_sentence(mainl)
    sub = [first_sentence(l)[0] for l in lines if l is not mainl][:5]
    if main[:1].isupper() and not main.split()[0].isupper(): main = main[0].lower() + main[1:]
    return {'do': f"{name}: {main}", 'why': why or why_for(name), 'sub': sub}

OTHERS = {n: tuple(f'({o})' for o in chars if o != n) for n in chars}

def dancing_step():
    rf = tbtext('reef', 'Dancing Coral'); buy = []
    for m in re.finditer(r'\n(\w+ Coral)\n\+100 max LV for ([\w ]+?)\n[\s\S]*?\n([\d.,]+[KMB]?)\n/\n([\d.,]+[KMB]?)(?=\n)(\nneed)?', rf):
        if not m.group(5) and (num(m.group(3)) or 0) >= (num(m.group(4)) or 1): buy.append(f"{m.group(1)} ({m.group(4)}): +100 max level {m.group(2)}")
    if not buy: return {'do': 'Dancing Coral: nothing to buy yet', 'why': '', 'sub': []}
    return {'do': 'Dancing Coral (Barnacle Curb, right side platform): buy these', 'why': 'raises shrine caps, Vibrant Coral feeds the POW goal', 'sub': buy}

def talent_preset_line(name):
    """Right talent preset for the park: skilling preset for skilling/Spelunking parks, fighting preset for fighting parks (roles from the super talents on each preset)."""
    try:
        st = json.load(open(ROOT / 'model' / 'supertalents.json')).get(name, {})
    except Exception:
        return None
    roles = {r['preset']: r.get('role') for r in st.get('presets', []) if r.get('role')}
    if len(set(roles.values())) < 2: return None
    try:
        import cardpresets as C
        kind = C.afk_type(raw.get(f"AFKtarget_{chars[name]['character_index']}"))[1]
    except Exception:
        return None
    want = 'skill' if kind not in ('FIGHTING',) else 'fight'
    if name in GOAL_PARK and 'Spelunking' in GOAL_PARK[name]: want = 'skill'
    active = int(chars[name].get('active_talent_preset') or 0) + 1
    need = next((p for p, r in roles.items() if r == want), None)
    if need and need != active:
        return {'do': f"Talents: switch to talent preset {need} ({'skilling' if want == 'skill' else 'fighting'}) for where he is parked", 'why': 'the other preset holds the wrong talents for this job', 'sub': []}
    return None

def weeklies():
    out = []
    for tab, label in (('Bonus', 'Bonus Ballot (W2)'), ('Meritocracy', 'Meritocracy (W7)')):
        tt = tbtext('ballot', tab)
        nxt = re.search(r'Next week in\n([^\n]+)', tt); now = re.search(r'Hide off-rotation\n([^\n]+)', tt)
        if now: out.append(f"{label}: {now.group(1).strip()} (next vote in {nxt.group(1) if nxt else '?'})" + (' DIVINITY WEEK: put everyone on the Divinity platform (Pulse)' if 'ivinit' in now.group(1) else ''))
    return out

def here(name):
    try:
        import cardpresets as C
        return C.afk_type(raw.get(f"AFKtarget_{chars[name]['character_index']}"))[0]
    except Exception:
        return '?'

def sushi_step():
    su = tbtext('sushi', 'Sushi'); bo = tbtext('sushi', 'Bonuses')
    cap = re.search(r'Fuel\n[\d,]+ / ([\d,]+)\n', su); nxt = re.search(r'Next unlock\n([^\n(]+)\(([\d,]+) fuel\)', su)
    sub = []
    if cap and nxt and num(cap.group(1)) < num(nxt.group(2)):
        sub.append(f"Fuel Capacity I until max fuel reaches {nxt.group(2)} (now {cap.group(1)}), so {nxt.group(1).strip()} can cook")
    sub += ['Then Fastburn Fuel I and II (fuel per hour)', 'Then Hourly Wage Meter and Customer Surcharge I (more bucks)']
    return {'do': 'Sushi: spend bucks in this order', 'why': 'new sushi types give bonuses, Live Octopus is 3x POW for the goal', 'sub': sub}

def greens_step():
    try:
        import tbhelp as T
        tier, items = T.ar_items('Greenstacks')
    except Exception:
        return None
    def p(x):
        try: return float(str(x['cur']).rstrip('%'))
        except Exception: return -1
    # Zack 2026-11-20: only items Totle can work toward himself. Out: crystal drops, shop buys (time gated),
    # souls (need the worship runner), rare/boss/colosseum/quest drops.
    OK = {'Base Monster Materials': 'farm the monster', 'Printable Skilling Resources': 'skill it (or print it)', 'Other Skilling Resources': 'skill it'}
    rows = [i for i in items if i['tab'] in OK and 'Collect' not in i['label'] and 'Timegated' not in i['group']
            and 'Endangered' not in i['group'] and 'Soul' not in i['label']]
    HOW = {'Void Bar': 'smelt in the Forge', 'Godshard Bar': 'smelt in the Forge'}
    sub = [f"{i['label']} ({p(i):.0f}%): {HOW.get(i['label'], OK[i['tab']])}" for i in sorted(rows, key=p, reverse=True)[:5]]
    return {'do': 'Greenstacks: your closest five you can farm yourself', 'why': 'each one counts for Equinox', 'sub': sub}

LEGEND_ORDER = [  # every line sourced: Griffy first, Pulse 2026-09-25 tier list (newest wins on conflict)
    ('Daily Shopping Spree', 'Pulse: S tier, Royal Guardian is only pushable with it. Griffy: finish RG upgrades first'),
    ("Thanatos's Teachings", 'Griffy: get the extra-kill talent for portals and Death Note while multikill is limited (helps the W7 push)'),
    ('Skillium Fancyson', 'Pulse: high A, maybe low S'),
    ('Furry Friends Forever', 'Pulse: high A since the Orion and Poppy buffs'),
    ('Picasso Gaming', 'Pulse: A+'),
    ('Democracy FTW', 'Griffy: the ballot multiplier talent is a good choice'),
    ('Extended Database', 'Pulse: A. Griffy: only once Land Ranks are unlocked (they are)'),
    ('Blue Ribbon Certification', 'Pulse: A'),
    ('Best Story Ever Told', 'Pulse: mid A'),
    ('Buy One Get One Free', 'Pulse: high A, needs the Exotic Market unlocked'),
    ('Two Time Jelly Operation', 'Pulse: big progression but 12 points and needs Jelly unlocked'),
    ('Minehead My Beloved', 'Pulse: big progression but 12 points and needs the Lumi mechanic'),
    ('Midusian Appetite', 'Pulse: B+'), ('Whats in your Jar?', 'Pulse: B+'), ('+1 Slab', 'Pulse: high B'),
    ('Purebred Eggs', 'Griffy: useful when pushing breeding. Pulse: B'),
    ("Kruk be Bubblin'", 'Pulse: B'),
]

def mastery_step():
    """Corrected 2026-11-20: mastery points go onto MEALS (mastery nodes), not held for the EXP categories."""
    tt = tbtext('cooking', 'Mastery'); kt = tbtext('cooking', 'Kitchens')
    lv = re.search(r'Mastery level\n(\d+)', tt); pu = re.search(r'Purple points\n(\d+) / (\d+)', tt); ye = re.search(r'Yellow points\n(\d+) / (\d+)', tt)
    node = re.search(r'Mastery node\nLv (\d+) \(([\d.]+x)\)\n([^\n]+)', kt)
    if not lv: return None
    sub = [f"Points: purple {pu.group(1)} of {pu.group(2)}, yellow {ye.group(1)} of {ye.group(2)} (check in game which are free)" if pu and ye else 'Points: check in game',
           (f"Your node now: {node.group(3)} level {node.group(1)} ({node.group(2)}), Tempura Shrimp is Spelunking EXP, so it helps the goal" if node else 'No node found'),
           'Pulse (Aug): for money, 10-15 points on Yummy Peach Ring and 5 on Bundt Cake',
           'Pulse: push mastery to 15, it scales hard after 10']
    return {'do': f"Cooking mastery (level {lv.group(1)}): points go onto meals", 'why': 'correction: I had said hold them; they are placed on meals', 'sub': sub}

def legend_step():
    tt = tbtext('legend')
    m = re.search(r'(\d+) unspent', tt)
    if not m or int(m.group(1)) == 0: return {'do': 'Legend talents: nothing needed', 'why': '', 'sub': []}
    open_ = {mm.group(1): (int(mm.group(2)), int(mm.group(3))) for mm in re.finditer(r'\n([^\n]{3,45})\nLv (\d+) / (\d+)', tt)}
    sub = [f"{n} ({open_[n][0]}/{open_[n][1]}): {why}" for n, why in LEGEND_ORDER if n in open_ and open_[n][0] < open_[n][1]][:6]
    return {'do': f"Legend talents (Whallamus): {m.group(1)} points unspent, spend in this order", 'why': 'sourced order, best first', 'sub': sub}

# ---------------- every-character checks ----------------
TRAP_PLAN = {}
for row in (ROOT / 'plans' / 'trapping.md').read_text().splitlines():
    m = re.match(r'\| (Autis\w+) \| (\w+)[^|]*\| ([^|]+) \| ([^|]+) \|', row)
    if m: TRAP_PLAN[m.group(1)] = (m.group(2), m.group(3).strip(), m.group(4).strip())
CRIT = {'Critter1': 'Froge', 'Critter2': 'Crabbo', 'Critter3': 'Scorpie', 'Critter4': 'Mousey', 'Critter5': 'Owlio', 'Critter6': 'Pingy',
        'Critter7': 'Bunny', 'Critter8': 'Dung Beat', 'Critter9': 'Honker', 'Critter10': 'Blobfish', 'Critter11': 'Tuttle'}

def trap_line(name):
    i = chars[name]['character_index']
    traps = [t for t in (J(raw.get(f'PldTraps_{i}')) or []) if isinstance(t, list) and len(t) > 6 and t[0] != -1]
    plan_c = TRAP_PLAN.get(name)
    if not plan_c: return {'do': 'Traps: nothing needed', 'why': '', 'sub': []}
    want, where, why = plan_c
    on = sorted({CRIT.get(t[3], t[3]) for t in traps})
    short_t = sum(1 for t in traps if (t[6] or 0) < 144000)
    if on == [want] and not short_t:
        return {'do': 'Traps: nothing needed', 'why': '', 'sub': []}
    sub = [f"Now on {', '.join(on) or 'nothing'}"] + ([f"{short_t} traps on a short timer, use 40 hours"] if short_t else [])
    return {'do': f"Traps: move all to {want} at {where}, Royal traps, 40 hours", 'why': why, 'sub': sub}

DIV = json.load(open(ROOT / 'model' / 'divinity.json')) if (ROOT / 'model' / 'divinity.json').exists() else {}

DIV_RUNNER = 'Autistronaut'   # my read: already on Mindful (Pulse 2026-11-09: best style for points); his park had no plan

def divinity_line(name):
    """Doot is owned: every god + every minor link counts for everyone (Griffy 2026-01/02), so links don't move."""
    pts = (DIV.get('head') or {}).get('Divinity PTS/hr', '')
    if name == DIV_RUNNER:
        return {'do': 'Divinity: sit him at the W5 Divinity altar on Mindful style', 'why': 'nobody is earning divinity points right now (0 an hour)' if pts.startswith('0') else 'keeps points coming in', 'sub': []}
    if name == 'Autistabish':   # divinity owner: spend side
        sub = []
        for cur, lst in (DIV.get('coral') or {}).items() if isinstance(DIV.get('coral'), dict) else []:
            pass
        bl = DIV.get('blessing_rank') or {}
        for cur, items in bl.items():
            for it in items:
                if it.get('afford'): sub.append(f"Blessing: {it['item'].split(' blessing')[0]} ({it['stat']})")
        ck = [c for c in (DIV.get('coral') or []) if isinstance(c, dict) and c.get('lv') == 0 and c.get('needs_lv', 0) <= 1815]
        nxt = next((c for c in ck if 'ALL players' not in c['desc']), None)
        if nxt: sub.insert(0, f"Coral Kid next: {nxt['desc'][:60].rstrip()}... at {short(nxt['cost'])} points (have {short(DIV.get('points') or 0)})")
        sub = sub[:5] + ['God rank (you are 1): Pulse targets 20 (Menagerie challenge, next-patch content) then 25-30. Push it in Divinity week. No-RNG way (Pulse): roll offerings until one shows 100%, then take it. Griffy: use cheap offerings until a guaranteed one shows']
        return {'do': 'Divinity: buy these blessings, then god rank', 'why': 'blessings raise divinity points; god ranks add divinity EXP, class EXP and talent points (Pulse, Griffy)', 'sub': sub}
    return {'do': 'Divinity: nothing needed (Doot gives every god to everyone)', 'why': '', 'sub': []}

try:
    import cardpresets as _CP
    _CPO = json.load(open(ROOT / 'model' / 'cardpresets.json'))
except Exception:
    _CP = None

def cards_line(name):
    if not _CP: return None
    l = _CP.char_lines(_CPO, name)
    return {'do': l[0] if l else 'Cards: nothing needed', 'why': '', 'sub': []}

# ---------------- kill milestones (Topher / Zemo) ----------------
def milestones():
    r = json.loads(gzip.open(SNAP / 'review.json.gz').read())
    out = {}
    def walk(o, g=''):
        if isinstance(o, dict):
            nm = o.get('name') if isinstance(o.get('name'), str) else g
            if 'label' in o and 'remaining)' in str(o['label']): out.setdefault(nm, []).append(o)
            for v in o.values(): walk(v, nm)
        elif isinstance(o, list):
            for v in o: walk(v, g)
    walk(r)
    try:
        from consts.consts_w3 import getEnemyNameFromMap as N
    except Exception:
        N = lambda m: ''
    res = {}
    for g, items in out.items():
        kind = next((k for k in ('Super CHOW', 'WOW', 'CHOW', 'ZOW') if k + 's with' in g or k + ' ' in g), None)
        who = re.search(r'with (Autis\w+)', g)
        if not kind or not who: continue
        rows = {}
        for a in items:
            m = re.match(r'(.+?) in (.+?) \(([\d.,]+[KMB]?) remaining\)', a['label'])
            if m and str(N(m.group(2))).startswith('Special') and 'AFK only' not in str(N(m.group(2))): continue
            if m: rows[(m.group(1), m.group(2))] = (num(m.group(3)), a.get('cur'))
        cnt = re.search(r'\((\d+)/(\d+)\)', g)
        res.setdefault(who.group(1), {})[kind] = {'have': cnt.groups() if cnt else None,
                                                  'next': sorted(rows.items(), key=lambda x: x[1][0])[:5]}
    return res

# ---------------- goal-based parking (Zack 2026-11-20: the way to the goal can't be wrong) ----------------
SPELUNK_CAVE = 'Fearful Tunnel (Zack: deeper caves give way less here)'
GOAL_PARK = {   # every line: where, card preset, and why with its source
    'Autistomatic': f"Spelunking: {SPELUNK_CAVE}, card preset 5. Why: Pulse (Oct 31) puts both Royal Guardians on Spelunking (Pit of Pages, fixed Nov 10); every Spelunking level adds base POW",
    'Autistastic': f"Spelunking: {SPELUNK_CAVE}, card preset 5. Why: Pulse (Oct 31): both Royal Guardians on Spelunking. His statue push waits (money mode when coins are short)",
    'Autistocat': "W7 Pirate Upper Deck (Pirate Underling), card preset 1. Why: she is the furthest toward Jellofish Fields (3.1M of 1B portal kills, about 1.1M an hour; then 60M at Sushi Perimeter). Jelly is 1.3x POW. Pulse: Arcane Cultist is the top damage class",
    'Autisticles': f"Spelunking: {SPELUNK_CAVE}, card preset 2. Why: Pulse (Nov 1): most characters on Spelunking; adds base POW",
    'Autistabish': f"Spelunking: {SPELUNK_CAVE}, card preset 2. Why: Pulse (Nov 1): most characters on Spelunking; adds base POW. His statue push waits",
    'Autistacular': f"Spelunking: {SPELUNK_CAVE}, card preset 2. Why: Pulse (Nov 1): most characters on Spelunking; adds base POW",
    'Autistotle': f"Spelunking: {SPELUNK_CAVE}, skill card preset. Why: Lab catch-up done (top Lab level, Zack 2026-11-21); his Spelunking is the lowest, so every level adds base POW and works him toward the best",
}
SIDE_PARK_WHY = {   # characters kept off Spelunking, and why that beats helping POW
    'Autiszemo': 'Side reason: his ZOWs and CHOWs only count on him and each W7 ZOW is only 100K kills, so he rotates through them',
    'Autistopher': 'Side reason: Super CHOW and WOW only count on him (account buffs); after the Ram he farms Green Mushrooms for coins + a WOW',
    'Autistronaut': 'Side reason: nobody earns divinity points right now; Pulse: skipping divinity costs 1-2 years in super week',
    'Autistachio': 'Side reason: monument week (4x rewards) this week; Spelunking level 1, so little POW from him',
}

# ---------------- build ----------------
def build():
    goal = goal_card()
    goal['weekly'] = weeklies()
    import extras as _EX
    global EXTRA
    EXTRA = _EX.all_house(CARDS, list(chars.values()))
    ms = milestones()
    goal['weekly'] = weeklies()
    out = {'save': SNAPN, 'goal': goal, 'chars': []}
    for cd in sorted(CARDS, key=lambda c: c['slot']):
        n = cd['name']
        daily, house, part = [], [], []
        for b in cd.get('daily', []):
            if (any(b['block'].startswith(x) for x in DROPBLK) and b['block'] != 'Trapping (collect + set)') or b['block'] == 'Setup check': continue
            if b['block'].startswith('W7 reef'):
                daily.append(dancing_step()); continue
            if 'Post Office' in b['block']:
                for s in b.get('steps', []):
                    if VERB.match(s): house.append({'do': first_sentence(s)[0], 'why': 'box points are permanent stats', 'sub': []})
                continue
            if 'ZOWs + CHOWs' in b['block']: continue   # replaced by the milestone step below
            daily.append(to_step(b, n))
        if n == 'Autisticles': daily.append(sushi_step()); daily.append(legend_step())
        if n == 'Autiszemo':
            ms_ = mastery_step()
            if ms_: house.insert(0, ms_)
        if n == 'Autistotle':
            gs = greens_step()
            if gs: daily.append(gs)
        if n == 'Autistachio' and any('Monument' in w for w in goal.get('weekly', [])):
            daily.insert(0, {'do': 'Monument week: claim and restart Bravery and Wisdom monuments, keep him parked there', 'why': 'Meritocracy is 4x monument rewards this week', 'sub': []})
        tp = talent_preset_line(n)
        if tp: daily.append(tp)
        if n == 'Autistacular':
            house.append({'do': 'Card set: farm 1 Verminous card', 'why': 'Bosses n Nightmares set goes 24% to 30% damage, drop and EXP for everyone', 'sub': ['Pulse: Verminous farms on the Insta castle map with Wind Walker + candy (mixed reports, test it)']})
        # every-character checks, always shown
        for f in (cards_line, trap_line, divinity_line):
            x = f(n)
            if x: daily.append(x)
        # kill milestones
        m = ms.get(n, {})
        for kind in ('Super CHOW', 'WOW', 'ZOW', 'CHOW'):
            if kind in m and m[kind]['next']:
                h = m[kind]['have']
                sub = [f"{mob} at {mp}: {short(rem)} kills left" for (mob, mp), (rem, cur) in m[kind]['next']]
                daily.append({'do': f"{kind}s: {h[0]} of {h[1]} done. Closest:" if h else f"{kind}s closest:", 'why': {'Super CHOW': 'only his own kills count, account buff tier', 'WOW': 'his WOW count feeds the golden food bonus', 'ZOW': 'counted on your best Barbarian (him)', 'CHOW': 'counted on your best Barbarian (him)'}[kind], 'sub': sub})
        # housekeeping
        try:
            import supertalents as _ST
            if '_STO' not in globals(): globals()['_STO'] = _ST.build()
            st = _ST.char_step(_STO, n)
            if st and not st['do'].endswith('nothing needed'): house.append(st)
        except Exception as ex:
            house.append({'do': f'Super talents: check failed ({ex})', 'why': '', 'sub': []})
        for bag in cd.get('bags') or []:
            house.append({'do': f"Missing bag: {bag}", 'why': '', 'sub': []})
        house += EXTRA.get(n, [])
        # goal part
        for lv in goal['levers'] + goal['prereqs']:
            if lv['who'] == n: part.append({'do': lv['do'], 'why': 'account goal', 'sub': []})
        park = cd.get('park', {}).get('text', '')
        if n == 'Autiszemo' and 'ZOW' in m and m['ZOW']['next']:
            pick = m['ZOW']['next'][3][0] if len(m['ZOW']['next']) > 3 else m['ZOW']['next'][0][0]
            park = (f"W7 {pick[1]} ({pick[0]}) for his ZOW, card preset 1, then the next W7 ZOW map he can reach. "
                    "Autistopher keeps the Dedotated Ram kills")
        if n == DIV_RUNNER:
            park = 'W5 Divinity altar, Mindful style (my read: nobody is earning divinity points; Pulse: Mindful is the best style)'
        if n in GOAL_PARK:
            park = GOAL_PARK[n]
        elif n == 'Autistachio' and any('Monument' in w for w in goal.get('weekly', [])):
            park = 'Bravery Monument this week (Meritocracy 4x monument rewards), then back to Divinity. Spelunking level 1, so little POW from him'
        elif n in SIDE_PARK_WHY:
            park = f"{park}. {SIDE_PARK_WHY[n]}"
        if 'GAP' in park:
            park = f"Stay at {here(n)} for now (no park plan yet, needs checking)"
        money = []
        if n == 'Autistastic':
            mp = (ROOT / 'plans' / 'money_plan.md').read_text()
            money = [ln[3:] for ln in mp.splitlines() if re.match(r'^\d\. ', ln)][:6]
        out['chars'].append({'name': n, 'money': money, 'class': cd.get('class'), 'daily': daily, 'house': house, 'part': part, 'park': park})
    return out

def to_md(o):
    g = o['goal']; L = [f"# Cards (save {o['save']})", '', f"## ACCOUNT GOAL: {g['name']}" + (f" (now {short(g['now'])})" if g['now'] else ''), g['why'], '']
    if g['prereqs']:
        L.append('Prereqs:'); L += [f"{i}. {p['do']} ({p['who']})" for i, p in enumerate(g['prereqs'], 1)]; L.append('')
    L.append('Buffs that push it:'); L += [f"{i}. {p['do']} ({p['who']})" for i, p in enumerate(g['levers'], 1)]
    if g.get('weekly'): L += ['', 'This week:'] + [f'- {w}' for w in g['weekly']]
    L += ['', 'Needs checking: ' + ', '.join(g['unknown']), '']
    for c in o['chars']:
        L += [f"## {c['name']}", '', 'Dailies:']
        for i, s in enumerate(c['daily'], 1):
            L.append(f"{i}. {s['do']}" + (f" *({s['why']})*" if s['why'] else ''))
            L += [f"   {chr(97 + j)}. {x}" for j, x in enumerate(s['sub'])]
        if c['house']:
            L.append('Housekeeping:')
            for i, s in enumerate(c['house'], 1):
                L.append(f"{i}. {s['do']}"); L += [f"   {chr(97 + j)}. {x}" for j, x in enumerate(s['sub'])]
        if c['part']:
            L.append('Goal part:'); L += [f"{i}. {s['do']}" for i, s in enumerate(c['part'], 1)]
        if c.get('money'):
            L.append('Money mode (when coins are short):'); L += [f"{i}. {s}" for i, s in enumerate(c['money'], 1)]
        L += [f"Park: {c['park']}", '']
    return '\n'.join(L)

def to_html(o):
    e = html.escape
    def steps(lst):
        h = '<ol>'
        for s in lst:
            h += f"<li>{e(s['do'])}" + (f" <i>({e(s['why'])})</i>" if s.get('why') else '')
            if s.get('sub'): h += '<ol type="a">' + ''.join(f'<li>{e(x)}</li>' for x in s['sub']) + '</ol>'
            h += '</li>'
        return h + '</ol>'
    g = o['goal']
    body = f"<section class=goal><h2>Account goal: {e(g['name'])}" + (f" <span>now {short(g['now'])}</span>" if g['now'] else '') + f"</h2><p>{e(g['why'])}</p>"
    if g['prereqs']: body += '<h3>Prereqs</h3>' + steps([{'do': f"{p['do']} ({p['who']})"} for p in g['prereqs']])
    body += '<h3>Buffs that push it</h3>' + steps([{'do': f"{p['do']} ({p['who']})"} for p in g['levers']])
    if g.get('weekly'): body += '<h3>This week</h3>' + steps([{'do': w} for w in g['weekly']])
    body += f"<p class=unk>Needs checking: {e(', '.join(g['unknown']))}</p></section>"
    for c in o['chars']:
        body += f"<details class=card><summary>{e(c['name'])} <small>{e(c['class'] or '')}</small></summary><h3>Dailies</h3>{steps(c['daily'])}"
        if c['house']: body += '<h3>Housekeeping</h3>' + steps(c['house'])
        if c['part']: body += '<h3>Goal part</h3>' + steps(c['part'])
        if c.get('money'): body += '<h3>Money mode (when coins are short)</h3>' + steps([{'do': s} for s in c['money']])
        body += f"<h3>Park</h3><p>{e(c['park'])}</p></details>"
    css = ('body{font:15px/1.45 system-ui,sans-serif;margin:0;padding:12px;background:#111;color:#eee}h1{font-size:18px}'
           'section,details{background:#1c1c1c;border-radius:10px;padding:10px 14px;margin:10px 0}summary{font-size:17px;font-weight:600;cursor:pointer}'
           'h2{font-size:17px;margin:4px 0}h2 span{font-weight:400;color:#9cf}h3{font-size:14px;color:#9cf;margin:12px 0 4px}'
           'ol{padding-left:22px;margin:4px 0}li{margin:3px 0}i{color:#aaa}small{color:#888;font-weight:400}.unk{color:#c96;font-size:13px}.goal{border:1px solid #357}')
    return f"<!DOCTYPE html><html><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>IdleOn Manager</title><style>{css}</style></head><body><h1>IdleOn cards · save {e(o['save'])}</h1>{body}</body></html>"

if __name__ == '__main__':
    import plain as _PL
    o = build()
    o = _PL.clean(o) if hasattr(_PL, 'clean') else o
    json.dump(o, open(ROOT / 'plans' / 'cards.json', 'w'), indent=1)
    (ROOT / 'plans' / f'cards_{SNAPN}.md').write_text(to_md(o))
    (ROOT / 'dashboard' / 'cards.html').write_text(to_html(o))
    print('cards v3:', len(o['chars']), 'characters; goal now', o['goal']['now'])
