"""Cards v4 (Zack 2026-11-21): built only from reports/<save>/decisions.json. Per character in rotation order:
Spend (open points: where + why) / Goal part / Do / Don't (reserve holds) / Notes (lean-checked systems) / Park.
Every card gets the standing anvil line. Info lines never reach cards (they stay in the Report).
"""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
SAVE = (ROOT / 'snapshots' / 'LATEST').read_text().strip()
D = json.load(open(ROOT / 'reports' / SAVE / 'decisions.json'))
chars = [c['character_name'] for c in json.load(open(ROOT / 'snapshots' / SAVE / 'chars.json'))['characters']]
SPEND = re.compile(r'\b(points?|super|talent preset|mastery|land rank|PO|Post Office|ladles?|star sign|DNA|Kilroy|amber|particles?)\b', re.I)
PARK = re.compile(r'^card_engine: PARK: ')
clean = lambda x: re.sub(r'^[a-z_0-9]+: ', '', x)

out = [f'# Cards {SAVE}', '', f"Holes the system still has (from the decision layer): {len(D['holes'])}. Top: " + '; '.join(D['holes'][:5]), '']
unowned = D['by_char'].get('account', {})
for name in chars:
    b = D['by_char'].get(name, {'goal': [], 'do': [], 'hold': [], 'notes': [], 'park': []})
    park = b.get('park') or []
    acts = [x for x in b['goal'] + b['do'] if not PARK.match(x)]
    spend = [clean(x) for x in acts if SPEND.search(x)]
    goal = [clean(x) for x in b['goal'] if x not in [y for y in acts if SPEND.search(y)] and not PARK.match(x)]
    do = [clean(x) for x in b['do'] if not SPEND.search(x) and not PARK.match(x)]
    out.append(f'## {name}')
    out.append('Spend:'); out += [f'{i}. {x}' for i, x in enumerate(spend, 1)] or ['- nothing open']
    if goal: out.append('Goal part:'); out += [f'{i}. {x}' for i, x in enumerate(goal, 1)]
    out.append('Do:'); out += [f'{i}. {x}' for i, x in enumerate(['Grab anvil production if it is cranking'] + do, 1)]
    if b['hold']: out.append("Don't:"); out += [f'- {clean(x)}' for x in b['hold']]
    if b['notes']: out.append('Notes (lean checks, no planner yet):'); out += [f'- {x}' for x in b['notes']]
    out.append('Park: ' + (park[0] if park else 'no park line (hole)')); out.append('')
if unowned:
    out.append('## Account (no owner yet)'); out += [f'- {x}' for k in unowned for x in unowned[k]]
P = ROOT / 'plans' / f'cards4_{SAVE}.md'; P.write_text('\n'.join(out) + '\n'); print('wrote', P.relative_to(ROOT), len(out), 'lines')
