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

SKILL_WORDS = SKILL_HINT + ('Proficiency', 'Ambidexterity', 'Strengthen', 'Smart', 'Eagle', 'Sneaky', 'Fish', 'Catch', 'Mining', 'Chop',
                            'Bug', 'Trap', 'Worship', 'Cook', 'Ranks', 'Skill', 'Ore', 'Log', 'Farm', 'Crop', 'Sample', 'Print')

def preset_roles(T, sl_active, sl_other, active_idx):
    """Role per preset from where its regular talent points sit (Zack 2026-11-21): the preset with the larger
    share of points in skilling talents is the skilling preset, the other is fighting. Never from existing supers."""
    def share(sl):
        s = f = 0
        for k, lv in sl.items():
            if not isinstance(lv, (int, float)) or lv <= 0: continue
            n = T.get(int(k), {}).get('name', '') if str(k).isdigit() else ''
            if any(w.lower() in n.lower() for w in SKILL_WORDS): s += lv
            else: f += lv
        return s / max(1, s + f)
    by_preset = {active_idx + 1: sl_active, 2 - active_idx: sl_other}   # presets are 1 and 2
    sh = {p: share(sl) for p, sl in by_preset.items()}
    skill_p = max(sh, key=sh.get)
    return {p: ('skill' if p == skill_p else 'fight') for p in by_preset}, by_preset, sh

def build():
    from utils.all_talentsDict import all_talentsDict as T
    raw = json.load(gzip.open(SNAP / 'raw.json.gz')); raw = raw.get('data', raw)
    J = lambda v: json.loads(v) if isinstance(v, str) else v
    sp = J(raw['Spelunk'])
    name_of = lambda x: T.get(int(x), {}).get('name', str(x)) if str(x).lstrip('-').isdigit() else str(x)
    out = {}
    for c in json.load(open(SNAP / 'chars.json'))['characters']:
        i = c['character_index']; lv = int(J(raw[f'Lv0_{i}'])[0]); pts = max(0, lv // 100 - 4)
        cls = c['class_name']; picks = None if cls == 'Beginner' else PICKS.get(cls)   # Pulse only says 'maybe' for Beginner: hold
        act = int(c.get('active_talent_preset') or 0)
        roles, by_preset, sh = preset_roles(T, J(raw[f'SL_{i}']), J(raw[f'SLpre_{i}']), act)
        tree = {name_of(k) for k in by_preset[1]}          # talents this character actually has
        own = {n for r in (picks or {}).values() for n, _ in r}
        other = {n for k, v in PICKS.items() if k != cls for r in v.values() for n, _ in r} - own   # another class's picks = left from an old class
        rows, taken = [], set()
        for pi, off in enumerate((20, 32)):
            p = pi + 1; role = roles[p]
            have = [name_of(x) for x in sp[off + i] if x != -1]
            open_ = pts - len(have)
            row = {'preset': p, 'role': role, 'skill_share': round(sh[p], 2), 'have': have, 'open': max(open_, 0), 'picks': []}
            wrong = [h for h in have if h in other]
            if wrong: row['odd'] = wrong
            if open_ > 0 and picks:
                pts_on = {name_of(k): v for k, v in by_preset[p].items()}
                cand = [(n, s) for n, s in picks[role] if n not in have and n in tree and (pts_on.get(n) or 0) > 0]
                row['picks'] = cand[:open_]
                row['skipped'] = [n for n, _ in picks[role] if n not in have and n not in [x for x, _ in cand]]
            rows.append(row)
        # same pick on both presets only if a source puts it on both role lists
        both = set(n for n, _ in rows[0]['picks']) & set(n for n, _ in rows[1]['picks'])
        for n in both:
            if not all(any(n == x for x, _ in picks[r]) for r in ('skill', 'fight')):
                rows[1]['picks'] = [x for x in rows[1]['picks'] if x[0] != n]
        out[c['character_name']] = {'class': cls, 'points': pts, 'presets': rows}
    json.dump(out, open(ROOT / 'model' / 'supertalents.json', 'w'), indent=1)
    return out

def char_step(o, name):
    ch = o.get(name)
    if not ch: return None
    sub = []
    for r in ch['presets']:
        lab = f"Talent preset {r['preset']} ({'skilling' if r['role'] == 'skill' else 'fighting'})"
        if r.get('odd'):
            sub.append(f"{lab}: {', '.join(r['odd'])} is supered but isn't in his tree (left from an old class?). Reset it before spending")
        if r['open'] <= 0: continue
        if r['picks']:
            sub += [f"{lab}: super {n} ({s})" for n, s in r['picks']]
            if r['open'] > len(r['picks']): sub.append(f"{lab}: hold the other {r['open'] - len(r['picks'])} (no more sourced picks)")
        else:
            sub.append(f"{lab}: {r['open']} open, hold them (no sourced pick)")
    if not sub: return {'do': 'Super talents: nothing needed', 'why': '', 'sub': []}
    return {'do': 'Super talents: spend the open points', 'why': 'points are permanent, every pick is from Griffy or Pulse', 'sub': sub}

if __name__ == '__main__':
    o = build()
    for n, c in o.items():
        print(n, c['class'], c['points'], [(r['preset'], r['open'], [p[0] for p in r['picks']]) for r in c['presets']])
