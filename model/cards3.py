"""Cards v4 (Zack 2026-11-21): only the in-game steps per character, mainly where to spend points and why.
Input: plans/cards.json (every step the engine makes, parent + sub structure kept) + reports/<save>/decisions.json
(reserve holds, lean-checked systems, holes). Output: plans/cards4_<save>.md and plans/cards4.json.
Per character: Spend (with where-to-put subs) / Do / Working toward (one line each) / Locked targets / Don't / Notes / Park.
Status lines ("nothing needed", worship level, what's printing) never reach a card; they live in the Report.
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SAVE = (ROOT / 'snapshots' / 'LATEST').read_text().strip()
C = json.load(open(ROOT / 'plans' / 'cards.json'))
D = json.load(open(ROOT / 'reports' / SAVE / 'decisions.json'))
import yaml
RES = yaml.safe_load(open(ROOT / 'brain' / 'reserves.yaml')) or {}
# Zack 2026-11-21: every system a character owns shows every day, even with nothing to do (agreed spec: dailies stay full)
IDX = yaml.safe_load(open(ROOT / 'model' / 'system_index.yaml')) or {}
CM = yaml.safe_load(open(ROOT / 'brain' / 'cant_miss.yaml')) or []
def item_count(code):
    import gzip
    d = json.load(gzip.open(ROOT / 'snapshots' / SAVE / 'raw.json.gz')); d = d.get('data', d)
    L = lambda k: json.loads(d[k]) if isinstance(d.get(k), str) else (d.get(k) or [])
    tot = sum(q for x, q in zip(L('ChestOrder'), L('ChestQuantity')) if x == code)
    for c in range(11): tot += sum(q for x, q in zip(L(f'InventoryOrder_{c}'), L(f'ItemQTY_{c}')) if x == code)
    return int(tot)
def cant_miss(name):
    out = []
    for c in CM:
        if c['owner'] != name: continue
        extra = ''
        if c.get('super_left'):
            import gzip
            ch = [x for x in json.load(gzip.open(ROOT / 'snapshots' / SAVE / 'tb_parsed.json.gz'))['characters'] if x.get('name') == name]
            n = (ch[0].get('superTalentLeftToSpend') or 0) if ch else 0
            if n <= 0: continue
            extra = f" ({n} unspent)"
        if c.get('weekly_boss'):
            import subprocess
            out.append(subprocess.run(['python3', str(ROOT / 'tools' / 'weekly_boss.py'), '--today'], capture_output=True, text=True).stdout.strip() + f". Why: {c['why']}"); continue
        if c.get('item'):
            n = item_count(c['item'])
            if n >= c.get('target', 0): continue
            extra = f" ({n} of {c['target']})"
        out.append(f"{c['text']}{extra}. Why: {c['why']}")
    return out
def owned(name): return sorted(s for s, v in IDX.items() if name in (v.get('owners') or []))
STEMS = {'statues': ['statue'], 'printer': ['print', 'printer'], 'zenith_market': ['zenith'], 'arcade': ['arcade']}
def sys_words(s): return STEMS.get(s.lower()) or [w for w in s.replace('_', ' ').split() if len(w) > 3] or [s]

STATUS = re.compile(r"nothing needed|nothing to buy|: worship level \d+, charge full|printing: .*samples held|lab is fine|no samples and no prints|"
                    r"tome is at|charges much faster|If he ever becomes", re.I)
NOPLAN = re.compile(r'no plan for this one yet', re.I)
TARGET = re.compile(r'\bpush\b.*\bto\b.*\(now ', re.I)
UNLOCK = re.compile(r'^Unlock: ')
SPEND = re.compile(r'\b(Library checkouts|points?|DNA|bucks|super talents|mastery|ladles|blessings|Equinox bar|charm rolls|Land Rank|Legend Talent|buy|claim the familiar)\b', re.I)
VERB = re.compile(r'^\W*(push|buy|spend|move|take|use|level|swap|put|collect|claim|read|cook|unlock|turn in|equip|switch|set|send|fight|do|grab|craft|'
                  r'vote|plant|trade|start|run|reset|feed|upgrade|max|get|go|keep|hold|lock|sit|farm|kill|harvest|check|talent preset)\b', re.I)
BAG = re.compile(r'^Missing bag: (.+)$')

def reserve(line):
    if re.search(r"\b(don't|do not|never) (spend|use)\b", line, re.I): return None
    for res, holds in RES.items():
        for h in holds:
            if re.search(h['match'], line, re.I): return f"{res} are held for {h['for'].replace('_', ' ')}: {h['why']}"
    return None

def subs_for(st, keep_all):
    out = []
    for s in st.get('sub') or []:
        if STATUS.search(s) or TARGET.search(s): continue
        if keep_all or VERB.match(s): out.append(s)
    return out

cards, md = [], [f'# Cards {SAVE}', '']
_g = C.get('goal') or {}
md += [f"## Account goal: {_g.get('name', '')}", f"- Now: {_g.get('now', '')}", f"- {_g.get('why', '')}"] + [f"- Need {x}" for x in _g.get('needs', [])] + ([f"- FLAG: {_g['flag']}"] if _g.get('flag') else []) + [f"- This week: {w}" for w in _g.get('weekly', [])] + ['']
try:   # Zack 2026-11-27: two account top 10s, quick (< 10 min) and long (10+ min), same score
    import score as _S0; _T0 = _S0.tasks()
    for _q, _lbl in ((True, f'quick, under {_S0.QUICK_MIN} min'), (False, f'long, {_S0.QUICK_MIN}+ min')):
        md += [f'### Top 10 ({_lbl})'] + [f"{_n}. {_S0.NICK.get(t['owner'], t['owner'])}: {t['task']} ({t.get('minutes', 30)} min, score {t['score']}, {t['src']})" for _n, t in enumerate(_S0.top10(_T0, _q), 1)] + ['']
except Exception as _e:
    md += [f'- FLAG: top 10 lists failed ({_e})', '']
holes = D.get('holes', [])
NICKS = {'Autiszemo': 'Zemo', 'Autistocat': 'Cat', 'Autisticles': 'Ticles', 'Autistastic': 'Tastic', 'Autistabish': 'Bish', 'Autistacular': 'Tacular', 'Autistotle': 'Totle', 'Autistomatic': 'Matic', 'Autistronaut': 'Naut', 'Autistopher': 'Topher', 'Autistachio': 'Tachio'}
# Baba Yaga -> next character still missing Inventory Bag D (its quest needs a Baba kill), in card order (Zack 2026-11-25)
def _baba_route(chars):
    need = [c['name'] for c in chars if any('Inventory Bag D' in (st.get('do') or '') for st in c.get('house') or [])]
    if not need: return
    for c in chars:
        for blk in ('daily', 'house'):
            for st in list(c.get(blk) or []):
                txt = (st.get('do') or '') + ' ' + ' '.join(st.get('sub') or [])
                if re.search(r'baba yaga[^.;]*up now', txt, re.I):
                    st['sub'] = [x for x in st.get('sub') or [] if 'baba yaga' not in x.lower()]
                    do = re.sub(r'\s*baba yaga[^,;]*up now[^,;]*(, go kill it)?', '', st.get('do') or '', flags=re.I).rstrip(': ,')
                    if do.endswith(')') and st['sub']: do += ': check the minibosses below'
                    st['do'] = do
                    if not st['sub'] and do.lower().startswith('world bosses'): c[blk].remove(st)
                    first = next(x for x in chars if x['name'] == need[0])
                    rest = ', '.join(NICKS.get(n, n) for n in need[1:])
                    first.setdefault('daily', []).insert(0, {'do': f"Baba Yaga is up: kill it on this character for the Inventory Bag D quest", 'why': f"then the next one: {rest}" if rest else 'last one who needs it', 'sub': []})
                    return
_baba_route(C['chars'])
for ch in C['chars']:
    name = ch['name']; b = D['by_char'].get(name, {})
    card = {'name': name, 'systems': [], 'spend': [], 'do': [], 'toward': [], 'locked': [], 'dont': [], 'notes': [], 'bags': [], 'park': ch.get('park') or ''}
    try:
        import score as _S; card['jobs'] = _S.card_lines(name)
    except Exception as _e:
        card['jobs'] = [f'job picker failed: {_e}']
    card['goal'] = [{'do': p['do'], 'why': p.get('why', '')} for p in ch.get('part') or []]
    for blk in ('daily', 'house'):
        for st in ch.get(blk) or []:
            do = st['do']
            if STATUS.search(do) and not st.get('sub'): card['systems'].append(do); continue
            if NOPLAN.search(do): card['notes'].append(f"{do.split(':')[0]}: no plan yet (hole, being built)"); continue
            m = BAG.match(do)
            if m: card['bags'].append(m.group(1)); continue
            r = reserve(do + ' ' + ' '.join(st.get('sub') or []))
            if r: card['dont'].append(f"{do} ({r})"); continue
            if UNLOCK.match(do): card['locked'].append(do[8:]); continue
            if re.search(r': locked, ', do): card['locked'].append(do + (' (then: ' + '; '.join(s.split(':')[0] for s in st.get('sub') or []) + ')' if st.get('sub') else '')); continue
            if re.match(r'(Super CHOW|WOW|ZOW|CHOW)s', do):
                card['do'].append({'do': do, 'sub': list(st.get('sub') or [])}); continue
            if TARGET.search(do):
                acts = subs_for(st, False)
                if not acts: card['toward'].append(do); continue
                card['do'].append({'do': do, 'sub': acts}); continue
            if SPEND.search(do): card['spend'].append({'do': do, 'why': st.get('why', ''), 'sub': subs_for(st, True)}); continue
            card['do'].append({'do': do, 'sub': subs_for(st, False)})
    card['notes'] += b.get('notes', [])
    seen = ' '.join([x if isinstance(x, str) else x.get('do', '') + ' ' + ' '.join(x.get('sub') or []) for k in ('systems', 'spend', 'do', 'toward', 'locked', 'dont', 'notes') for x in card[k]]).lower()
    try:
        import syscheck as _SC; _chk = _SC.lines(name)
    except Exception as _e:
        _chk = [('syscheck', f'syscheck failed: {_e}', [])]
    for _s, _l, _subs in _chk:
        card['systems'].append(_l + ''.join(f'\n   {chr(97 + j)}. {x}' for j, x in enumerate(_subs)))
    seen += ' ' + ' '.join(k + ' ' + k.replace('_', ' ') for k, _, _ in _chk) + (' lab chips lab jewels lab bonuses meritocracy' if _chk else '')
    try:   # Phase B 2026-11-28: every owned system from its approved GOAL block (model/goals.py), replaces the 'no check yet' filler
        import goals as _GL; card['goals'] = _GL.card_lines(name); card['anvil'] = _GL.anvil_line(name)
        if name in (_GL.load()['systems'].get('cog_board') or {}).get('owners', []):   # Phase C E: Toolbox optimizer plan
            import cogs as _CG; card['goals'] += _CG.lines()
    except Exception as _e:
        card['goals'] = [f'goals failed: {_e}']; card['anvil'] = 'Grab anvil production if it is cranking'
    cards.append(card)

    md.append(f'## {name}')
    cm = cant_miss(name); card['cant_miss'] = cm
    if cm: md.append("Can't miss today:"); md += [f'- {x}' for x in cm]
    if card['goal']:
        md.append('Goal:'); md += [f"- {x['do']}" + (f" ({x['why']})" if x['why'] else '') for x in card['goal']]
    md.append('Spend:')
    if card['spend']:
        for i, s in enumerate(card['spend'], 1):
            md.append(f"{i}. {s['do']}"); md += [f"   {chr(97 + j)}. {x}" for j, x in enumerate(s['sub'])]
    else: md.append('- nothing open')
    md.append('Do:'); md.append('1. ' + card['anvil'])
    for i, s in enumerate(card['do'], 2):
        md.append(f"{i}. {s['do']}"); md += [f"   {chr(97 + j)}. {x}" for j, x in enumerate(s['sub'])]
    if card['systems']: md.append('Systems (every day):'); md += [f'- {x}' for x in card['systems']]
    if card.get('goals'): md.append('Goals (every owned system, from its GOAL block):'); md += [f'- {x}' for x in card['goals']]
    if card['bags']: md.append('Bags to pick up: ' + '; '.join(card['bags']))
    if card['dont']: md.append("Don't:"); md += [f'- {x}' for x in card['dont']]
    if card['toward']: md.append('Working toward (no step today):'); md += [f'- {x}' for x in card['toward']]
    if card['locked']: md.append('Locked targets:'); md += [f'- {x}' for x in card['locked']]
    if card['notes']: md.append('Notes:'); md += [f'- {x}' for x in card['notes']]
    md.append('Jobs (in order):'); md += [f'- {l}' for l in card.get('jobs', [])]
    md.append(f"Park: {card['park'] or 'no park line (hole)'}"); md.append('')

acct = D['by_char'].get('account', {})
try:
    import goals as _GL; md.append('## Account systems (unowned + Zack, on their cadence)'); md += [f'- {x}' for x in _GL.account_lines()]; md.append('')
except Exception as _e: md.append(f'## Account systems\n- goals failed: {_e}')
md.append('## Not checked by anything yet (being built)')
md += [f'- {h}' for h in holes if 'nothing checks it' in h]
if acct.get('notes'): md.append('## Account notes'); md += [f'- {x}' for x in acct['notes']]
json.dump({'save': SAVE, 'goal': C.get('goal'), 'cards': cards, 'holes': holes}, open(ROOT / 'plans' / 'cards4.json', 'w'), indent=1)
(ROOT / 'plans' / f'cards4_{SAVE}.md').write_text('\n'.join(md) + '\n')
print('wrote', f'plans/cards4_{SAVE}.md', len(md), 'lines')
