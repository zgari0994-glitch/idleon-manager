"""Super talents (Zack 2026-11-20: sourced only, points are permanent).
Open points come from the save (Spelunk[20+i] / Spelunk[32+i] = supers per talent preset, AutoReview models/w7/spelunk.py;
points = 1 per 100 class levels from 500). Picks come ONLY from creator lists below, in their order, skipping ones
already supered. No sourced pick left = "hold the points".
Sources: Griffy 2025-11-28 fo2WwEKsty0 (per-class super talent guide), Pulse 2026-09-20 DWEVaYI4iWA (super tier talk),
Pulse 2026-09-15/2026-08-29, Griffy+Pulse 2026-08: Royal Guardian's own talents can't be supered until the Royal Armory shelf unlock.
"""
import gzip, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / 'snapshots' / (ROOT / 'snapshots' / 'LATEST').read_text().strip()

G, P = 'Griffy', 'Pulse'
# class -> role -> [(talent name as in game, source line)]
PICKS = {
    'Death Bringer': {
        'skill': [('Brute Efficiency', f'{G}+{P}: big efficiency on skilling setups'), ('Big Pick', f'{P}: must super on the skilling setup for copper prints'),
                  ('Worming Undercover', f'{G}: fishing efficiency'), ('Skill Strengthen', f'{G}: larger prints'),
                  ('Dank Ranks', f'{G}: stronger land rank bonuses'), ("Agricultural 'preciation", f'{G}: farming and land rank EXP')],
        'fight': [('Monster Decimator', f'{G}+{P}: good on active and AFK setups'), ('Charred Skulls', f'{G}: kill scaling from stats'),
                  ('Sentinel Axes', f'{G}: bigger auto attacks'), ('Graveyard Shift', f'{G}: better respawn'),
                  ('Wraith Overlord', f'{G}: multiplicative damage, when using Wraith Form')],
    },
    'Siege Breaker': {
        'skill': [('Elusive Efficiency', f'{G}: efficiency scales strongly'), ("Teleki'net'ic Logs", f'{G}: catching efficiency, bigger prints'),
                  ('Briar Patch Runner', f'{G}: agility into catching efficiency'), ('Skill Ambidexterity', f'{G}: skilling, before Agi Again')],
        'fight': [('Stacked Skulls', f'{G}: kills per kill from agility'), ('Pirate Flag', f'{G}: more EXP and drops'),
                  ('Archlord Of The Pirates', f'{G}: multiplicative drop rate and EXP. {P}: make sure it is supered'),
                  ('Homing Arrows', f'{G}: more arrows and damage'), ('Suppressing Fire', f'{G}: multiple hits')],
    },
    'Royal Guardian': {   # Divine Knight talents only; RG's own talents are locked until the Royal Armory shelf
        'skill': [('Big Pick', f'{G}+{P}: mining efficiency, copper prints'), ('Copper Collector', f'{G}+{P}: mining efficiency'),
                  ('Tool Proficiency', f'{G}+{P}: mining power, bigger prints'), ('Brute Efficiency', f'{G}+{P}: efficiency on skilling setups')],
        'fight': [('Shockwave Slash', f'{G}: carries most of the DK kit'), ('Orb Of Remembrance', f'{P}: top five, fixed now so super it'),
                  ('Charred Skulls', f'{G}: kill scaling from stats'), ('Knightly Disciple', f'{G}: longer duration, more knights'),
                  ('Mega Mongorang', f'{G}: size and more targets')],
    },
    'Elemental Sorcerer': {
        'skill': [('Smart Efficiency', f'{G}: larger log prints'), ('Log On Logs', f'{G}: big boost to chopping prints'),
                  ('Leaf Thief', f'{G}: larger prints'), ('Skill Wiz', f'{G}: skill output')],
        'fight': [('Tornado', f'{G}: strong combat ability'), ('Dimensional Wormhole', f'{G}: worth it since the orb and portal fixes'),
                  ('Meteor Shower', f'{G}: faster clears'), ('Memorial Skulls', f'{G}: kill scaling from stats'),
                  ('Shared Beliefs', f'{G}: more divinity EXP for everyone')],
    },
    'Arcane Cultist': {
        'skill': [('Log On Logs', f'{G}: same mage log talents for chopping'), ('Smart Efficiency', f'{G}: same mage efficiency talents'),
                  ('Skill Wiz', f'{G}: skilling output')],
        'fight': [('Sizzling Skull', f'{G}+{P}: drives auto attack damage, 100% super'), ('Cranium Cooking', f'{G}+{P}: drives alchemy, a mainstay'),
                  ('Memorial Skulls', f'{G}: kill scaling from stats'), ('Arcane Skulls', f'{G}: longer duration, more kills'),
                  ('Arcane Crystals', f'{G}: more arcane monsters'), ('Backup Energy', f'{G}+{P}: right after the top row')],
    },
    'Wind Walker': {
        'skill': [('Elusive Efficiency', f'{G}: skilling'), ('Sneaky Skilling', f'{G}: sneaking support is where WW supers are strongest'),
                  ('Eagle Eye', f'{G}: more critters and EXP')],
        'fight': [('Eternal Hunt', f'{G}: respawns and dust in Tempest Form'), ('Spirit Ballista', f'{G}: stronger auto attacks'),
                  ('Price Recession', f'{G}: ninja knowledge discount for sneaking')],
    },
    'Voidwalker': {
        'skill': [('Left Hand Of Learning', f'{G}+{P}: more EXP for others, global talents work with supers now'),
                  ('Right Hand Of Action', f'{G}+{P}: others get skill efficiency, bigger prints'), ('Printer Go Brrr', f'{G}: more printed hours')],
        'fight': [('One Step Ahead', f'{G}: more Voidwalker talent points'), ('Gimme Gimme', f'{G}: more double loot'),
                  ('Void Radius', f'{G}: bigger range, multikill helps prints')],
    },
    'Beginner': {'skill': [('Happy Dude', f'{P}: skill EXP, the only page one talent maybe worth a super')],
                 'fight': [('Extra Bags', f'{P}: carry capacity, maybe worth it for candy or stamps')]},
}
SKILL_HINT = ('Efficiency', 'Logs', 'Pick', 'Miner', 'Collector', 'Thief', 'Wiz', 'Skilling', 'Learning', 'Action', 'Printer', 'Happy Dude', 'Worming', 'Dank', 'Preciation', 'Briar')

def build():
    from utils.all_talentsDict import all_talentsDict as T
    raw = json.load(gzip.open(SNAP / 'raw.json.gz')); raw = raw.get('data', raw)
    J = lambda v: json.loads(v) if isinstance(v, str) else v
    sp = J(raw['Spelunk'])
    out = {}
    for c in json.load(open(SNAP / 'chars.json'))['characters']:
        i = c['character_index']; lv = int(J(raw[f'Lv0_{i}'])[0]); pts = max(0, lv // 100 - 4)
        cls = c['class_name']; picks = None if cls == 'Beginner' else PICKS.get(cls)   # Pulse only says 'maybe' for Beginner: hold
        rows = []
        own = {n for r in (picks or {}).values() for n, _ in r} | ({n for r in PICKS['Beginner'].values() for n, _ in r} if cls == 'Voidwalker' else set())
        other = {n for k, v in PICKS.items() if k != cls for r in v.values() for n, _ in r} - own
        for pi, off in enumerate((20, 32)):
            have = [T.get(x, {}).get('name', str(x)) for x in sp[off + i] if x != -1]
            open_ = pts - len(have)
            if any(h in other for h in have):
                rows.append({'preset': pi + 1, 'have': have, 'open': 0, 'picks': [], 'odd': True}); continue
            if open_ <= 0 or not picks:
                rows.append({'preset': pi + 1, 'have': have, 'open': max(open_, 0), 'picks': []}); continue
            role = 'skill' if sum(any(h in n for h in SKILL_HINT) for n in have) >= max(1, len(have) / 2) else ('fight' if have else 'skill')
            cand = [(n, s) for n, s in picks[role] if n not in have][:open_]
            rows.append({'preset': pi + 1, 'have': have, 'open': open_, 'role': role, 'picks': cand})
        out[c['character_name']] = {'class': cls, 'points': pts, 'presets': rows}
    json.dump(out, open(ROOT / 'model' / 'supertalents.json', 'w'), indent=1)
    return out

def char_step(o, name):
    ch = o.get(name)
    if not ch: return None
    sub = []
    for r in ch['presets']:
        if r.get('odd'):
            sub.append(f"Talent preset {r['preset']}: the save shows another class's talents supered ({', '.join(r['have'])}). Check in game before spending"); continue
        if r['open'] <= 0: continue
        if r['picks']:
            sub += [f"Talent preset {r['preset']}: super {n} ({s})" for n, s in r['picks']]
            if r['open'] > len(r['picks']): sub.append(f"Talent preset {r['preset']}: hold the other {r['open'] - len(r['picks'])} (no more sourced picks)")
        else:
            sub.append(f"Talent preset {r['preset']}: {r['open']} open, hold them (no sourced pick)")
    if not sub: return {'do': 'Super talents: nothing needed', 'why': '', 'sub': []}
    return {'do': 'Super talents: spend the open points', 'why': 'points are permanent, every pick is from Griffy or Pulse', 'sub': sub}

if __name__ == '__main__':
    o = build()
    for n, c in o.items():
        print(n, c['class'], c['points'], [(r['preset'], r['open'], [p[0] for p in r['picks']]) for r in c['presets']])
