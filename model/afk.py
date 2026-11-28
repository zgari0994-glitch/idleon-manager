"""AFK park lines v2 (Zack 2026-11-27). Rebuilt every pull, nothing is a fixed spot.

Order of candidates per character (first live one wins, the rest show as fallbacks):
  1. LAW    weekly override, a duty that only counts on this character (Law 2), then the account goal (Law 1: Spelunking POW)
  2. JOB    jobs.yaml afk candidates with a live finish line from this save
  3. CLASS  sourced class spot (creator / AutoReview)
  4. READ   my read, plus the gap that is still missing
Each line = world / map / mob + why + finish line + source.
- "now: X" when the save shows the character somewhere else.
- Active play: the same off-line spot on 2 pulls in a row -> "keep?" prompt on the card.
- Pins: `python3 tools/afk_pin.py <nick> active <activity>` pins until cleared or 3 pulls.
- Stale check every pull: finished targets, GAP lines, old Zack lines (>21 days) and source conflicts get flagged.
State lives in state/afk_state.json (written only by record(), i.e. on a pull).
"""
import gzip, json, re, sys
from datetime import date
from pathlib import Path

import yaml
from data import load

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / 'state' / 'afk_state.json'
# POW 900K target retired 2026-11-27: Spelunking's target = the next lore boss (goalpick.target)
PIN_PULLS = 3
ACTIVE_PULLS = 2
STALE_DAYS = 21
NICK = {'Zemo': 'Autiszemo', 'Cat': 'Autistocat', 'Ticles': 'Autisticles', 'Tastic': 'Autistastic', 'Bish': 'Autistabish',
        'Tacular': 'Autistacular', 'Totle': 'Autistotle', 'Matic': 'Autistomatic', 'Naut': 'Autistronaut', 'Topher': 'Autistopher',
        'Tachio': 'Autistachio'}
NAME2NICK = {v: k for k, v in NICK.items()}
TIER_ORDER = {'plan': -2, 'master': -1, 'law': 0, 'job': 1, 'class': 2, 'read': 3}

D = load()
CFG = yaml.safe_load((ROOT / 'model' / 'jobs.yaml').read_text())
SAVE = D.stamp


def short(n):
    n = float(n)
    for d, s in ((1e9, 'B'), (1e6, 'M'), (1e3, 'K')):
        if abs(n) >= d: return f"{n / d:.1f}{s}".replace('.0', '')
    return f"{n:,.0f}"


def _deep(obj, pred, depth=0):
    if depth > 6: return
    if isinstance(obj, dict):
        if pred(obj): yield obj
        for v in obj.values(): yield from _deep(v, pred, depth + 1)
    elif isinstance(obj, list):
        for v in obj: yield from _deep(v, pred, depth + 1)


def _soft(fn, default=None):
    try: return fn()
    except Exception: return default


# ---------- what the save shows ----------
def _raw():
    p = ROOT / 'snapshots' / SAVE / 'raw.json.gz'
    return _soft(lambda: json.load(gzip.open(p)), {}) or {}


RAW = _raw()
RAW = RAW.get('data', RAW) if isinstance(RAW, dict) else {}


def observed(name):
    """(mob, afk type, map) the save has this character on."""
    c = _soft(lambda: D.char(name), {}) or {}
    idx = c.get('playerId', c.get('character_index', c.get('index')))
    code = RAW.get(f'AFKtarget_{idx}') if idx is not None else None
    mob, kind = _soft(lambda: __import__('cardpresets').afk_type(code), (code, '?')) or (code, '?')
    mp = str(c.get('currentMap', '') or '').replace('_', ' ')
    return {'mob': str(mob or '?'), 'kind': str(kind), 'map': mp}


def matches(line, obs):
    if not line: return True
    if line.get('kind') == 'spelunk':
        have = (obs['mob'] + obs['kind'] + obs['map']).lower()
        return f"spelunking{line['cave']}" in have if line.get('cave') else 'spelunk' in have
    keys = [k.lower() for k in (line.get('mob'), line.get('map')) if k]
    have = (obs['mob'] + ' ' + obs['map']).lower()
    return any(k in have for k in keys) if keys else True


# ---------- live finish lines ----------
_MS = None


def milestones():
    """Death Note kill milestones from cards2 (only if cards2 is import-safe)."""
    global _MS
    if _MS is None:
        _MS = {}
        src = (ROOT / 'model' / 'cards2.py').read_text()
        if "__name__ == '__main__'" in src or '__name__ == "__main__"' in src:
            _MS = _soft(lambda: __import__('cards2').milestones(), {}) or {}
    return _MS


def statue(name):
    st = _soft(lambda: D.system('statues'), None)
    for s in _deep(st, lambda d: name.lower() in str(d.get('name', d.get('rawName', ''))).lower()):
        lv = s.get('level', s.get('lvl'))
        if lv is not None: return float(lv)
    return None


def divinity_level(name):
    c = _soft(lambda: D.char(name), {}) or {}
    for k in ('divinityLevel',):
        if k in c: return float(c[k])
    for s in _deep(c, lambda d: any('divin' in str(k).lower() for k in d)):
        for k, v in s.items():
            if 'divin' in str(k).lower() and 'level' in str(k).lower() and isinstance(v, (int, float)): return float(v)
    sk = c.get('skillsInfo') or {}
    v = (sk.get('divinity') or {}).get('level') if isinstance(sk, dict) else None
    return float(v) if v is not None else None


def bar_total(raw):
    """Zack 2026-11-27: bars = storage + every inventory + forge slots (Automation Arm moves them between all three)."""
    n = 0
    for it in (_soft(lambda: D.get('account.storage.list'), []) or []):
        if isinstance(it, dict) and it.get('rawName') == raw: n += it.get('amount') or it.get('quantity') or 0
    for c in (_soft(lambda: D.get('characters'), []) or []):
        for it in (c.get('inventory') or []) if isinstance(c, dict) else []:
            if isinstance(it, dict) and it.get('rawName') == raw: n += it.get('amount') or 0
    for sl in (_soft(lambda: D.get('account.forge.list'), []) or []):
        b = (sl or {}).get('bar') or {}
        if b.get('rawName') == raw: n += b.get('quantity') or 0
    return n or None


def finish(spec, name):
    """-> (text, done, measured). measured False = no number in the data (say so)."""
    if not spec: return ('finish line = GAP (no measurable target yet)', False, False)
    k = spec.get('kind')
    if k == 'pow':   # Zack 2026-11-27: Spelunking target = next lore boss
        t, hit = _soft(lambda: __import__('goalpick').target('Spelunking'), ('Spelunking target not in this save', False))
        return (t, hit, True)
    if k == 'plan': return (spec.get('text', "Zack's plan: runs until he changes it"), False, True)
    if k == 'compass':
        t = _soft(lambda: __import__('compass').tier_line())
        return (t or 'Compass tier not in this save', False, bool(t))
    if k == 'statue':
        lv = statue(spec['name'])
        if lv is None: return (f"{spec['name']} Statue level not in the parser: check in game", False, False)
        return (f"{spec['name']} Statue {lv:g} / {spec['to']}", lv >= spec['to'], True)
    if k == 'deathnote':
        m = milestones().get(name, {}).get(spec['set'], {})
        nx = m.get('next') or []
        if not m: return (f"{spec['set']} kills: not loaded in this run (cards2 milestones)", False, False)
        if not nx: return (f"all {spec['set']}s done", True, True)
        (mob, mp), (rem, _cur) = nx[0]
        h = m.get('have')
        return (f"{mob} at {mp}: {short(rem)} kills left" + (f" ({h[0]} of {h[1]} {spec['set']}s)" if h else ''), False, True)
    if k == 'divinity_level':
        lv = divinity_level(name)
        if lv is None: return (f"Divinity level not found in the parser: check in game (target {spec['to']})", False, False)
        return (f"Divinity {lv:g} / {spec['to']}", lv >= spec['to'], True)
    if k == 'divpoints':
        import needs as N
        kid, pts = _soft(N._div_points_needed, (None, None))
        if kid is None and pts is None: return ('divinity points not in this save', False, False)
        if kid is None: return (f"divinity points {short(pts)}: next Coral Kid upgrade affordable", True, True)
        return (f"divinity points {short(pts)} / {short(kid['cost'])} for the next Coral Kid upgrade", False, True)
    if k == 'map_past':   # Zack 2026-11-27: Arcanist Form = crystal mobs before the map timer unlocks the next map
        code = observed(name)['mob']
        moved = code != spec['code'] and re.match(r'w(\d)', code or '') and code > spec['code']
        return (f"unlock the map after {spec['label']} (save shows him on {code})", bool(moved), True)
    if k == 'bars':   # Zack 2026-11-27: storage + inventories + forge
        n = bar_total(spec['item'])
        lbl = spec.get('label', spec['item'])
        if n is None: return (f"{lbl}: not found in storage/inventory/forge (check in game, target {short(spec['to'])})", False, False)
        return (f"{lbl} {short(n)} / {short(spec['to'])} ({n / spec['to']:.0%})", n >= spec['to'], True)
    if k == 'maestro':
        r = skill_ranks(name)
        if not r: return ('skill ranks not in the parser', False, False)
        bad = [x for x in r if x[1] > 1]
        if not bad: return ('#1 in every skill', True, True)
        w = max(bad, key=lambda x: x[1])
        return (f"worst: {w[0]} rank {w[1]} (L{w[2]}); not #1 in {len(bad)} skill(s): " + ', '.join(f"{a} #{b}" for a, b, _ in bad[:6]), False, True)
    return ('finish line = GAP', False, False)


def skill_ranks(name):
    sk = (_soft(lambda: D.char(name), {}) or {}).get('skillsInfo') or {}
    return [(k, int(v['rank']), v.get('level')) for k, v in sk.items() if isinstance(v, dict) and v.get('rank') is not None]


# ---------- candidates ----------
def law_lines(name):
    out = []
    import needs as N
    import goalpick as G
    for who, do, why in _soft(lambda: N.weekly()['notes'], []) or []:
        if who == name and 'parked' in do:
            out.append({'tier': 'law', 'where': 'Monument (Hole)', 'why': f"weekly override: {why}", 'src': 'save votes', 'fin': ('until the week rolls', False, True)})
    for c in afk_cfg(name):
        if c.get('exclusive'):
            out.append(dict(c, tier='law', why=f"Law 2, only he does this: {c['why']}"))
    gs = _soft(G.status, {}) or {}
    goal = gs.get('goal', 'Spelunking')
    if any(c.get('exclusive') and not finish(c.get('finish'), name)[1] for c in afk_cfg(name)): return out
    if goal == 'Spelunking':
        spot = spelunk_spots().get(name)
        if spot:
            cave, why, fin = spot
            out.append({'tier': 'law', 'kind': 'spelunk', 'where': f"W7 Spelunking cave {cave} ({CAVE_NAMES[cave - 1]})", 'cave': cave,
                        'why': f"Law 1 goal Spelunking ({gs.get('target', '?')}). Why this cave: {why}", 'fin': (fin, False, True),
                        'src': 'goal review + spot rules (Zack 2026-11-27)', 'goal': True})
    elif name in gs.get('owners', []):
        out.append({'tier': 'law', 'where': f"{goal}: hard-focus (goal owner)", 'why': f"Law 1 goal {goal}: {gs.get('why')}",
                    'fin': (gs.get('target', 'GAP'), gs.get('hit', False), True), 'src': 'goal review (model/goalpick.py)'})
    return out


# ---------- Spelunking spots (Zack 2026-11-27): a cave per character, with a reason ----------
MAX_CAVE = 4   # Zack 2026-11-27: cave 4 is the deepest he runs now; 5 not yet
CAVE_NAMES = ['Fearful Tunnel', 'Decaying Crevasse', 'Buried Church', 'One Way Opening', 'Plunder Cranny']   # idleon.wiki: Plunder Cranny (Pirate Upper Deck) drops Chapter Five; order per wiki tunnel list
CAVE_CHAPTER = {c: c - 1 for c in range(1, 6)}   # Zack 2026-11-27: cave N drops Chapter N pages
EFF_LEVELS = [(50, 4), (30, 3), (10, 2), (0, 1)]   # my read: Spelunking level -> deepest cave he runs well. XP per cave is not in the parser
_SPOTS = None


def chapter_need(i):
    ch = D.system('spelunk')['chapters'][i]
    capped = [b for b in ch if b.get('maxBonus')]
    worst = min(capped, key=lambda b: b['bonus'] / b['maxBonus'])
    need = 1 - sum(b['bonus'] / b['maxBonus'] for b in capped) / len(capped)
    nm = re.sub(r'[{}|]', ' ', worst['name'].replace('_', ' ')).replace('+', '').strip()
    return need, f"{re.sub(' +', ' ', nm)} {worst['bonus']:.3g}/{worst['maxBonus']:g}"


def spelunkers():
    """Characters whose park falls to the Spelunking goal (no weekly override, no live exclusive duty)."""
    import needs as N
    wk = [w for w, d, _ in (_soft(lambda: N.weekly()['notes'], []) or []) if 'parked' in d]
    out = []
    for name in NICK.values():
        if name in wk: continue
        if any(c.get('exclusive') and not finish(c.get('finish'), name)[1] for c in afk_cfg(name)): continue
        out.append(name)
    return out


def spelunk_spots():
    """Re-checked every pull (Zack 2026-11-27): 1) every cave 1-MAX covered, strongest + Royal Guardians on the deepest,
    2) everyone else on their most efficient cave (deepest they run well), 3) spread by page need, cave 1 gets the fewest.
    Close calls are flagged for Zack to decide in the moment."""
    global _SPOTS
    if _SPOTS is not None: return _SPOTS
    S = D.system('spelunk'); names = spelunkers()
    lv = {n: D.char(n)['skillsInfo']['spelunking']['level'] for n in names}
    rg = {n for n in names if 'Royal_Guardian' in str(D.char(n).get('class'))}
    eff = {n: min(MAX_CAVE, next(c for t, c in EFF_LEVELS if lv[n] >= t)) for n in names}
    at = {c: [] for c in range(1, MAX_CAVE + 1)}; why = {}
    order = sorted(names, key=lambda n: (-(n in rg), -lv[n]))
    for n in order:
        at[eff[n]].append(n)
        why[n] = (f"Royal Guardian, level {lv[n]}: RG talents suit the deepest cave" if n in rg and eff[n] == MAX_CAVE else
                  f"level {lv[n]}: cave {eff[n]} is the deepest he runs well (my read)")
    # coverage: fill empty caves from the deepest crowded cave, weakest non-RG first
    for c in range(MAX_CAVE - 1, 0, -1):
        if at[c]: continue
        src = next((d for d in range(MAX_CAVE, c, -1) if len([x for x in at[d] if x not in rg]) and len(at[d]) > 1), None)
        if src is None: continue
        n = min([x for x in at[src] if x not in rg], key=lambda x: lv[x])
        at[src].remove(n); at[c].append(n)
        why[n] = f"level {lv[n]}: moved down to cover cave {c} so Chapter {c} pages keep coming (every cave needs someone)"
    # spread: a crowded cave gives its weakest non-RG to a shallower cave with a bigger page need (not cave 1)
    for c in range(MAX_CAVE, 2, -1):
        while len(at[c]) > 2:
            cand = [x for x in at[c] if x not in rg]
            if not cand: break
            tgt = max(range(2, c), key=lambda d: chapter_need(CAVE_CHAPTER[d])[0] / (1 + len(at[d])))
            n = min(cand, key=lambda x: lv[x]); at[c].remove(n); at[tgt].append(n)
            need, worst = chapter_need(CAVE_CHAPTER[tgt])
            why[n] = f"level {lv[n]}: cave {tgt} has the bigger open page need, Chapter {tgt} {need:.0%} short (weakest {worst}). Close call vs cave {c}: your call in the moment"
    out = {}
    for c, ns in at.items():
        for n in ns:
            out[n] = (c, why[n], f"Chapter {c}: {chapter_need(CAVE_CHAPTER[c])[1]}; cave {c} best depth {S['bestCaveLevels'][c - 1]}")
    if 'Autistotle' in out:   # Zack 2026-11-27: XP only matters for Totle (stays highest level)
        c, w, f = out['Autistotle']
        out['Autistotle'] = (c, w + f". CHECK IN GAME: open the AFK window on caves {max(1, c - 1)}-{MAX_CAVE} and keep him on the highest Spelunking EXP/hr (idleon.wiki: EXP comes from Spelunking Efficiency)", f)
    if not at[MAX_CAVE]:
        out['_gap'] = f"nobody runs cave {MAX_CAVE} well: raise Spelunking levels / POW (see goal card)"
    _SPOTS = out
    return out


def afk_cfg(name):
    a = (CFG.get('characters') or CFG).get(name, {}).get('afk') if isinstance(CFG.get('characters') or CFG, dict) else None
    if a is None:
        for v in CFG.values():
            if isinstance(v, dict) and name in v: a = v[name].get('afk'); break
    if isinstance(a, dict): a = [a]
    return a or []


def stale(c):
    flags = []
    if 'GAP' in (c.get('where', '') + ' ' + c.get('text', '')): flags.append('has a GAP')
    d = c.get('date')
    if d and c.get('src', '').startswith('zack'):
        age = (date.today() - date.fromisoformat(str(d))).days
        if age > STALE_DAYS: flags.append(f"Zack line is {age} days old: still true?")
    if c.get('conflict'): flags.append(c['conflict'])
    return flags


def candidates(name):
    """-> (live rows ranked, retired rows). A hit target never stays on the card (Zack 2026-11-27)."""
    rows, retired = [], []
    for c in law_lines(name) + [dict(x) for x in afk_cfg(name) if not x.get('exclusive')]:
        c.setdefault('tier', 'read')
        if str(c.get('when', '')).startswith('top_need:'):   # only while that system is a top-10 need (score.need_rank)
            r = _soft(lambda: __import__('score').need_rank(c['when'].split(':', 1)[1]))
            if not r or r > 10: continue
        if c.get('dyn') == 'compass': c.update(_soft(lambda: __import__('compass').park_fields(), {}) or {})
        c['fin'] = c.get('fin') or finish(c.get('finish'), name)
        if c['fin'][1]: retired.append(c); continue
        c['stale'] = stale(c) + ([] if c.get('finish') or c.get('fin', (0, 0, False))[2] or c['tier'] == 'law' else ['no finish line'])
        rows.append(c)
    rows.sort(key=lambda c: TIER_ORDER.get(c['tier'], 9))
    return rows, retired


def fmt(c):
    loc = c.get('where') or ' / '.join(x for x in (c.get('world'), c.get('map'), c.get('mob')) if x) or 'spot = GAP'
    tag = {'plan': "ZACK'S PLAN", 'master': 'MASTERCLASS', 'law': 'LAW', 'job': 'JOB', 'class': 'CLASS', 'read': 'MY READ'}[c['tier']]
    s = f"[{tag}] {loc}. Why: {c.get('why', '?')}. Finish: {c['fin'][0]}. Source: {c.get('src', 'GAP')}"
    if c.get('gap'): s += f". Gap: {c['gap']}"
    if c.get('stale'): s += f"  [STALE CHECK: {'; '.join(c['stale'])}]"
    return s


# ---------- state: active play + pins ----------
def _state():
    return _soft(lambda: json.loads(STATE.read_text()), None) or {'last_save': None, 'chars': {}}


def pick(name, st=None):
    st = st or _state()
    rows, retired = candidates(name)
    chosen = (rows or [None])[0]
    cs = st['chars'].get(name, {})
    return rows, chosen, cs, retired


def park_text(name, st=None):
    """Card Park line(s): chosen line, now:, pin / keep? prompt, next fallbacks."""
    rows, chosen, cs, retired = pick(name, st)
    nick = NAME2NICK.get(name, name)
    obs = observed(name)
    L = []
    pin = cs.get('pin')
    if pin:
        L.append(f"PINNED: {nick} active {pin['activity']} ({pin['left']} pull(s) left, clear: `afk_pin.py {nick} clear`)")
    L.append(fmt(chosen) if chosen else 'no park line (hole)')
    if chosen and not matches(chosen, obs) and not pin:
        L.append(f"now: {obs['mob']} on {obs['map'] or '?'} ({obs['kind']})")
    if cs.get('prompt') and not pin:
        L.append(f"keep? {nick} has been on {cs['prompt']} for {ACTIVE_PULLS} pulls. Say \"{nick} active <activity>\" to pin it, or move him back")
    for c in [r for r in rows if r is not chosen][:2]:
        L.append('then: ' + fmt(c))
    for c in retired:
        L.append(f"retired: {c.get('where') or c.get('map')} ({c['fin'][0]}): target hit, removed")
    return L


def record():
    """Call once per pull (new save). Updates history, active-play prompts, pin countdown."""
    st = _state()
    if st.get('last_save') == SAVE: return st
    for nick, name in NICK.items():
        cs = st['chars'].setdefault(name, {'hist': []})
        _rows, chosen, _, retired = pick(name, st)
        if retired:
            R = ROOT / 'state' / 'retired.json'
            rr = _soft(lambda: json.loads(R.read_text()), []) or []
            rr += [{'save': SAVE, 'who': name, 'line': c.get('where') or c.get('map'), 'finish': c['fin'][0]} for c in retired if not any(x['who'] == name and x['line'] == (c.get('where') or c.get('map')) for x in rr)]
            R.write_text(json.dumps(rr, indent=1))
        obs = observed(name)
        off = None if matches(chosen, obs) else f"{obs['mob']} ({obs['map'] or '?'})"
        cs['hist'] = (cs.get('hist', []) + [{'save': SAVE, 'off': off}])[-5:]
        last = [h['off'] for h in cs['hist'][-ACTIVE_PULLS:]]
        cs['prompt'] = last[0] if len(last) == ACTIVE_PULLS and last[0] and len(set(last)) == 1 else None
        if cs.get('pin'):
            cs['pin']['left'] -= 1
            if cs['pin']['left'] <= 0: cs.pop('pin')
    st['last_save'] = SAVE
    STATE.write_text(json.dumps(st, indent=1))
    return st


def preview():
    age = _soft(lambda: f"{D.age_hours:.1f}h", '?')
    import goalpick as G
    g = G.status()
    print(f"save {SAVE} ({age} old)\nGOAL: {g['goal']} (score {g['score']}): {g['target']}\n  why: {g['why']}\n  runners-up: {g['runners_up']}  prompt: {g['prompt']}")
    for nick, name in NICK.items():
        obs = observed(name)
        print(f"\n## {nick} ({name})  save shows: {obs['mob']} / {obs['map'] or '?'} / {obs['kind']}")
        _rows, chosen, _, retired = pick(name)
        for i, c in enumerate(_rows, 1):
            print(f"{i}. {'>> ' if c is chosen else ''}{fmt(c)}")
        for c in retired: print(f"   retired: {c.get('where') or c.get('map')} ({c['fin'][0]})")


if __name__ == '__main__':
    preview() if '--record' not in sys.argv else print(json.dumps(record(), indent=1)[:2000])
