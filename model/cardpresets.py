"""Card presets per character (Zack 2026-11-19).
One preset per task the character needs. Passive cards never go in a preset:
  - cards AutoReview tags "(Passive)" (Griffy 2023-03-18 / 2026-11-07, wiki: passive bonuses need no equipping)
  - every card of a skill whose account total is 300+ (Rift Skill Mastery 300, wiki; Griffy 2026-10-28:
    once skill cards are passive, separate skill sets are not needed)
Fixed numbering: 1 Fighting AFK, 2 Skilling, 3 Drop rate, 4 Active EXP, 5 Spelunking, 6 Crystal hunt, 7 niche.
Doubled slots: top-left needs Omega Nanochip, bottom-right needs Omega Motherboard (AutoReview cards.py).
Run from the AutoReview folder: PYTHONPATH=. python3 .../model/cardpresets.py
"""
import gzip, json, sys
from pathlib import Path
from consts.consts_general import card_raw_data, cardset_names, CardSets
from consts.consts_monster_data import decode_monster_name
from models.general.cards import Card

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / 'snapshots' / (ROOT / 'snapshots' / 'LATEST').read_text().strip()
J = lambda v: json.loads(v) if isinstance(v, str) else v
raw = json.load(gzip.open(SNAP / 'raw.json.gz')); raw = raw.get('data', raw)
chars = json.load(open(SNAP / 'chars.json'))['characters']

# Rift Skill Mastery 300 -> all that skill's cards passive (wiki: Mining, Chopping, Fishing, Catching, Trapping, Worship)
MASTERY = {'Mining': 'Mining', 'Chopping': 'Choppin', 'Fishing': 'Fishing', 'Catching': 'Catching',
           'Trapping': 'Trapping', 'Worship': 'Worship'}
tot = {}
for c in chars:
    for k, v in c['skills'].items(): tot[k] = tot.get(k, 0) + (v if isinstance(v, (int, float)) else 0)
rift_on = (J(raw.get('Rift')) or [0])[0] >= 16
mastered = [w for s, w in MASTERY.items() if rift_on and tot.get(s, 0) >= 300]

counts = J(raw.get('Cards0')) or {}
cards = []
for si, setd in enumerate(card_raw_data):
    for ci in setd:
        if ci[0] == 'Blank': continue
        try: cpv = float(ci[4])
        except ValueError: cpv = 0.0
        c = Card(ci[0], decode_monster_name(ci[0], card=True), cardset_names[si] if si < len(cardset_names) else f'set{si}',
                 counts.get(ci[0], 0), float(ci[2]), cpv, ci[3].replace('_', ' '))
        c.eff = ci[3].replace('+{', '').replace('%', '').replace('_', ' ').strip()
        c.passive = '(Passive)' in c.eff or any(w in c.eff for w in mastered)
        cards.append(c)
owned = [c for c in cards if c.level > 0 and not c.passive]

# task -> (stat weights by effect text, creator pins, card set candidates, source line)
TASKS = {
    1: ('Fighting AFK', {'Fighting AFK gain rate': 6, 'Multikill per tier': 5, 'Total Damage Multi': 4, 'Total Damage': 3,
                         'Critical Damage': 1, 'Total Drop Rate': 1},
        [], ['Spirited Valley', "Smolderin' Plateau", 'Bosses n Nightmares'],
        'Griffy: every character runs the AFK card; his kill setups are mostly multikill cards'),
    2: ('Skilling', {'All Skill Efficiency': 6, 'Skill AFK gain rate': 6, 'Skill EXP': 3, 'Double AFK claim chance': 2,
                     'Boost Food Effect': 1},
        ['Chaotic Troll'], ['Easy Resources', 'Hard Resources', 'Medium Resources'],
        'Griffy: Chaotic Troll is one of the strongest skill efficiency cards, double it; Amarok card for skill AFK'),
    3: ('Drop rate', {'Drop Rate Multi': 8, 'Total Drop Rate': 4, 'Fighting AFK gain rate': 1},
        ['Demon Genie'], ['Events', 'Bosses n Nightmares'],
        'Pulse 2026-09: doubled Demon Genie plus a drop rate multi card in the other doubled slot; multi beats any additive card'),
    4: ('Active EXP', {'Monster EXP While Active': 6, 'EXP from monsters': 5, 'Class EXP Multi': 5, 'EXP Conversion from Talent': 1},
        [], ['Shimmerfin Deep', 'Bosses n Nightmares'],
        'Griffy: active monster EXP cards are underrated when farming EXP'),
    5: ('Spelunking', {'Spelunking Efficiency': 6, 'Spelunking AFK Gain': 6, 'Spelunking EXP': 4, 'All Skill Efficiency': 2,
                       'Skill AFK gain rate': 2, 'Skill EXP': 1},
        ['Chaotic Troll'], ['Easy Resources', 'Hard Resources'], '(my read) Spelunking cards are not passive yet'),
    6: ('Crystal hunt', {'Crystal Mob Spawn Chance': 7, 'Drop Rate Multi': 5, 'Total Drop Rate': 3},
        ['Demon Genie', 'Poop'], ['Events', 'Bosses n Nightmares'],
        'Pulse: Royal Guardian needs a drop rate + crystal page; Griffy: Poop + Demon Genie for crystal spawn'),
    7: ('Cooking', {'Cooking EXP gain': 6, 'All Skill Efficiency': 3, 'Skill EXP': 3, 'Skill AFK gain rate': 2},
        ['Chaotic Troll'], ['Medium Resources', 'Easy Resources'], '(my read) only one non-passive cooking card exists'),
    8: ('Lab', {'Lab EXP gain': 6, 'Skill EXP': 3, 'Skill AFK gain rate': 2},
        [], ['Medium Resources'], '(my read) one Lab EXP card'),
}

def cset_star(name):
    s = [c for c in cards if c.cardset == name]
    if not s: return 0
    return min(sum(min(c.star, 5) + 1 for c in s) // len(s), 5)

SET_BONUS = {cardset_names[i]: (a.replace('{%_', '').replace('_', ' '), float(b)) for i, (a, b, _) in enumerate(CardSets) if i < len(cardset_names)}

def best_set(cands):
    sc = [(SET_BONUS[n][1] * cset_star(n), n) for n in cands if n in SET_BONUS]
    v, n = max(sc)
    return {'set': n, 'bonus': f"+{v:g}% {SET_BONUS[n][0]}"}

def score(c, w):
    return max((wt for k, wt in w.items() if c.eff.startswith(k) or c.eff == k), default=0)

def build_preset(tid, chips):
    name, w, pins, sets, src = TASKS[tid]
    pool = [c for c in owned if score(c, w) > 0 or c.name in pins]
    pool.sort(key=lambda c: (c.name in pins, score(c, w), c.level * c.value_per_level), reverse=True)
    pick = pool[:8]
    if not pick: return None
    dbl = [i for i, chip in ((0, 'Omega Nanochip'), (7, 'Omega Motherboard')) if chip in chips]
    slots = [None] * 8; rest = list(pick)
    for i in dbl:                     # strongest (pins first) into the doubled slots
        if rest: slots[i] = rest.pop(0)
    for i in range(8):
        if slots[i] is None and rest: slots[i] = rest.pop(0)
    tgt = None
    if tid in (3, 6):
        miss = [c.name for c in cards if c.eff.startswith('Drop Rate Multi') and c.level == 0]
        if len(miss) == sum(1 for c in cards if c.eff.startswith('Drop Rate Multi')):
            tgt = (f"No drop rate multi card owned yet ({', '.join(miss)}). Pulse: push one fast, then double it. "
                   "It goes in the doubled slot over the weakest drop card.")
    return {'n': tid, 'task': name, 'cards': [s.name if s else 'free (nothing else helps)' for s in slots], 'target': tgt,
            'detail': [f"{s.name} ({s.eff}, {s.star + 1} star)" if s else 'empty' for s in slots],
            'doubled': [i + 1 for i in dbl], **best_set(sets), 'src': src}

def tasks_for(c):
    sk = [s for s in (c['specialized_skills'] or []) if s]
    t = [1, 2, 3, 4]
    if 'Spelunking' in sk: t.append(5)
    if c['class_name'] == 'Royal Guardian': t.append(6)          # Pulse: RG drop rate + crystal page
    if 'Cooking' in sk: t.append(7)
    if 'Laboratory' in sk: t.append(8)
    return t

import re as _re
from consts.consts_monster_data import script_monster_definitions as _MD
def afk_type(code):
    m = _re.search(r'addNewMonster\("' + _re.escape(code or '') + r'",\{Name:"([^"]+)",AFKtype:"(\w+)"', _MD)
    return (m.group(1).replace('_', ' '), m.group(2)) if m else (code, '?')

GAME_SLOT = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 7}   # Lab shares game preset 7 (Cat has no Cooking)

def current(i):
    return [[x for x in p if x != 'B'] for p in (J(raw.get(f'CardPreset_{i}')) or [])]

def build():
    out = {'mastered_passive': mastered, 'passive_tagged': sum(1 for c in cards if '(Passive)' in c.eff),
           'skill_totals': {s: tot.get(s, 0) for s in MASTERY}, 'chars': {}}
    for c in chars:
        i, chips = c['character_index'], c.get('equipped_lab_chips') or []
        ps = [p for p in (build_preset(t, chips) for t in tasks_for(c)) if p]
        # niche 7/8 share game slot 7; game has 7 presets
        cur = current(i)
        for pr in ps: pr['slot'] = GAME_SLOT[pr['n']]
        afk = afk_type(raw.get(f'AFKtarget_{i}'))
        out['chars'][c['character_name']] = {'class': c['class_name'], 'presets': ps, 'now': cur, 'afk': afk,
                                             'equipped_now': [x for x in (J(raw.get(f'CardEquip_{i}')) or []) if x != 'B']}
    return out

NAME = {c.codename: c.name for c in cards}

def char_lines(o, name):
    """Setup check, cards part: only says something when a change is needed."""
    ch = o['chars'].get(name)
    if not ch: return []
    out = []
    now = [{NAME.get(x, x) for x in p} for p in ch['now']]
    off = [p['slot'] for p in ch['presets'] if p['slot'] - 1 >= len(now) or now[p['slot'] - 1] != {x for x in p['cards'] if not x.startswith('free')}]
    if off:
        out.append(f"Cards: presets {', '.join(map(str, off))} not built to plan yet (card build session).")
        return out
    eq = {NAME.get(x, x) for x in ch['equipped_now']}
    where, kind = ch['afk']
    want = {'FIGHTING': [1, 3, 4, 6], 'SPELUNKING': [5, 2]}.get(kind)
    if want:
        match = [p for p in ch['presets'] if eq == {x for x in p['cards'] if not x.startswith('free')}]
        if not any(p['n'] in want for p in match):
            best = next(p for p in ch['presets'] if p['n'] in want)
            out.append(f"Cards: switch to preset {best['slot']} ({best['task']}) for {where}.")
    return out

def card_lines(o):
    return []

if __name__ == '__main__':
    o = build()
    json.dump(o, open(ROOT / 'model' / 'cardpresets.json', 'w'), indent=1)
    print('mastered passive:', o['mastered_passive'], '| tagged passive:', o['passive_tagged'])
    for n, ch in o['chars'].items():
        print(f"\n{n} ({ch['class']})")
        for p in ch['presets']:
            print(f"  {p['n']} {p['task']}: {', '.join(p['cards'])} | set {p['set']} {p['bonus']} | doubled {p['doubled']}" + (f" | TARGET {p['target'][:40]}" if p['target'] else ''))
