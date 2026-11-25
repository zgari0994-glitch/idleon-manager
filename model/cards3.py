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
        if c.get('item'):
            n = item_count(c['item'])
            if n >= c.get('target', 0): continue
            extra = f" ({n} of {c['target']})"
        out.append(f"{c['text']}{extra}. Why: {c['why']}")
    return out
def owned(name): return sorted(s for s, v in IDX.items() if name in (v.get('owners') or []))
def sys_words(s): return [w for w in s.replace('_', ' ').split() if len(w) > 3] or [s]

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
holes = D.get('holes', [])
for ch in C['chars']:
    name = ch['name']; b = D['by_char'].get(name, {})
    card = {'name': name, 'systems': [], 'spend': [], 'do': [], 'toward': [], 'locked': [], 'dont': [], 'notes': [], 'bags': [], 'park': ch.get('park') or ''}
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
    for s in owned(name):
        if not any(w.lower() in seen for w in sys_words(s)):
            card['systems'].append(f"{s.replace('_', ' ').title()}: no check yet, plan being built (owned by {name})")
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
    md.append('Do:'); md.append('1. Grab anvil production if it is cranking')
    for i, s in enumerate(card['do'], 2):
        md.append(f"{i}. {s['do']}"); md += [f"   {chr(97 + j)}. {x}" for j, x in enumerate(s['sub'])]
    if card['systems']: md.append('Systems (every day):'); md += [f'- {x}' for x in card['systems']]
    if card['bags']: md.append('Bags to pick up: ' + '; '.join(card['bags']))
    if card['dont']: md.append("Don't:"); md += [f'- {x}' for x in card['dont']]
    if card['toward']: md.append('Working toward (no step today):'); md += [f'- {x}' for x in card['toward']]
    if card['locked']: md.append('Locked targets:'); md += [f'- {x}' for x in card['locked']]
    if card['notes']: md.append('Notes:'); md += [f'- {x}' for x in card['notes']]
    md.append(f"Park: {card['park'] or 'no park line (hole)'}"); md.append('')

acct = D['by_char'].get('account', {})
md.append('## Not checked by anything yet (being built)')
md += [f'- {h}' for h in holes if 'nothing checks it' in h]
if acct.get('notes'): md.append('## Account notes'); md += [f'- {x}' for x in acct['notes']]
json.dump({'save': SAVE, 'goal': C.get('goal'), 'cards': cards, 'holes': holes}, open(ROOT / 'plans' / 'cards4.json', 'w'), indent=1)
(ROOT / 'plans' / f'cards4_{SAVE}.md').write_text('\n'.join(md) + '\n')
print('wrote', f'plans/cards4_{SAVE}.md', len(md), 'lines')
