"""Status checks, part 2 (pending_changes "Left to build", built 2026-11-28). Same format as syscheck.py:
(system, line, [subs]). Reads Toolbox's parser through data.py; account._zack holds extras the harness adds with
Toolbox's own functions (tools/tbparse/zack.test.mjs): bubbleCosts (Bubbles page math) and alerts (dashboard alerts,
default trackers). Every line is data; anything without a creator source says "my read".
Dry run: python3 model/syscheck2.py [nickname]"""
import gzip, json, re, sys
from pathlib import Path
import yaml
sys.path.insert(0, str(Path(__file__).resolve().parent))
import syscheck as S1

ROOT, D, short, nm = S1.ROOT, S1.D, S1.short, S1.nm
A = D.raw['account']; CH = D.raw['characters']
NAMES = [c.get('name') for c in CH]
Z = A.get('_zack') or {}
LIGHT = 'Autistachio'   # Zack: unowned systems anyone can do go to the lighter-load character
VIAL_COST = [0, 100, 1E3, 2500, 1E4, 5E4, 1E5, 5E5, 1000001, 5E6, 25E6, 1E8, 1E9, 5E10]  # Toolbox vialCostsArray
VIAL_MAX = 13
GS = 1e7   # greenstack


def stor(raw):
    return sum(x.get('amount') or 0 for x in A.get('storage', {}).get('list') or [] if x.get('rawName') == raw)


def stor_by_name(name):
    k = str(name).replace('_', ' ').lower()
    xs = [x.get('amount') or 0 for x in A.get('storage', {}).get('list') or [] if str(x.get('displayName', '')).replace('_', ' ').lower() == k]
    return sum(xs) if xs else None


def item_name(raw):
    x = next((x for x in A.get('storage', {}).get('list') or [] if x.get('rawName') == raw), None)
    return nm(x.get('displayName')) if x else raw


def prev_parsed():
    """newest older snapshot with a parse (for per-day rates)."""
    for d in sorted((ROOT / 'snapshots').iterdir(), reverse=True):
        if d.name >= D.stamp or not (d / 'tb_parsed.json.gz').exists(): continue
        try: return json.load(gzip.open(d / 'tb_parsed.json.gz')), d.name
        except Exception: continue
    return None, None


_P = None
def per_day(raw):
    global _P
    if _P is None:
        p, s = prev_parsed()
        _P = (p, s)
    p, s = _P
    if not p: return None
    t0, t1 = (p.get('_meta') or {}).get('parsed_at_save_time'), D.save_time
    if not t0 or not t1 or t1 - t0 < 43200: return None
    old = sum(x.get('amount') or 0 for x in p['account'].get('storage', {}).get('list') or [] if x.get('rawName') == raw)
    return (stor(raw) - old) / ((t1 - t0) / 86400)


# ---------- Toolbox missables / alerts routed to owners (pending L13) ----------
# alert section -> system key (system_index owners). Character alerts go on that character's own card.
ROUTE = {
    'General.etc.arcanistDailyDrops': 'tesseract', 'General.etc.freeCompanion': 'companions', 'General.etc.miniBosses': 'world_bosses',
    'General.etc.randomEvents': 'world_bosses', 'General.gemsFromBosses': 'world_bosses', 'General.shops': 'greenstacks',
    'General.tasks': 'tasks', 'General.guild': 'guild_bonuses', 'General.etc.familyObols': 'obols', 'General.etc.petMartGems': 'gemshop',
    'General.etc.tournamentRegister': 'tournament', 'General.etc.raidRegister': 'tournament', 'General.etc.glimmerwickCandle': 'tome',
    'General.etc.dailyCrystals': 'crystal_spawn_chance', 'General.materialTracker': 'greenstacks',
    'World 1.owl': 'owl', 'World 1.statues': 'statues', 'World 1.stamps': 'stamps', 'World 1.forge': 'forge_upgrades', 'World 1.anvil': 'anvil',
    'World 2.alchemy': 'alchemy_vials', 'World 2.arcade': 'arcade', 'World 2.islands': 'islands', 'World 2.kangaroo': 'islands',
    'World 2.postOffice': 'post_office', 'World 2.weeklyBosses': 'weekly_boss', 'World 2.killRoy': 'killroy', 'World 2.bubba': 'bubba',
    'World 3.construction.saltDeficit': 'refinery', 'World 3.construction': 'construction_buildings', 'World 3.library': 'library',
    'World 3.printer': 'printer', 'World 3.traps': 'trapping', 'World 3.worship': 'worship', 'World 3.equinox': 'equinox',
    'World 3.atoms': 'atom_collider', 'World 3.refinery': 'refinery', 'World 3.salt': 'saltlick',
    'World 4.breeding': 'breeding', 'World 4.cooking': 'cooking', 'World 4.lab': 'lab_mainframe', 'World 4.tome': 'tome',
    'World 5.gaming': 'gaming', 'World 5.hole': 'caverns', 'World 5.sailing': 'sailing', 'World 5.divinity': 'divinity',
    'World 6.farming': 'farming', 'World 6.sneaking': 'sneaking', 'World 6.summoning': 'summoning',
    'World 7.jellyOperator': 'jelly_operator', 'World 7.menagerie': 'menagerie', 'World 7.minehead': 'minehead', 'World 7.research': 'research',
    'World 7.royalGuardian': 'royal_armory', 'World 7.spelunking': 'spelunk', 'World 7.sushiStation': 'sushi_station',
    'World 7.theButton': 'the_button', 'World 7.zenithMarket': 'zenith_market', 'World 7.compass': 'compass', 'World 7.coralReef': 'coral_reef',
}
EMPTY = (False, None, [], {}, 0, -1, '', 'OFF')


def _leaves(o, p):
    if isinstance(o, dict) and not any(k in o for k in ('name', 'rawName', 'current', 'remaining', 'percent', 'left', 'count', 'available')):
        for k, v in o.items(): yield from _leaves(v, p + [k])
    elif o not in EMPTY:
        yield '.'.join(p), o


def _pretty(key, v):
    """one plain-English line per alert. Generic fallback keeps the numbers."""
    k = key.split('.')[-1]
    if k == 'icon': return None
    if key == 'General.tasks': return f"tasks ready to claim in world {', '.join(str(x) for x in v)}"
    if k == 'dailyShipments': return f"post office: {len(v)} daily shipments to send"
    if k == 'sigils' and isinstance(v, list): return 'sigils ready to tier up: ' + ', '.join(nm(x.get('name')) for x in v)
    words = re.sub(r'([a-z])([A-Z])', r'\1 \2', k).lower()
    sysw = key.split('.')[1] if key.startswith('World') else ''
    sysw = re.sub(r'([a-z])([A-Z])', r'\1 \2', sysw).lower().strip()
    if isinstance(v, bool): return f"{sysw} {words}: ready".strip()
    if isinstance(v, (int, float)): return f"{sysw} {words}: {short(v)}".strip()
    if isinstance(v, str): return f"{sysw} {words}: {nm(v)}".strip()
    if isinstance(v, dict):
        if 'left' in v: return f"{sysw} {words}: {v['left']} / {v.get('max')} left"
        if 'remaining' in v: return f"{sysw} {words}: {v['remaining']} left"
        if 'available' in v: return f"{sysw} {words}: {v['available']} available"
        if 'current' in v: return f"{sysw} {words}: {short(v['current'])}" + (f" / {short(v['cap'])}" if 'cap' in v else '')
        if 'percent' in v: return f"{sysw} {words}: {v['percent']:.0f}%"
        if 'count' in v:
            ops = ', '.join(nm(o.get('name')) for o in v.get('outposts') or [])[:120]
            return f"{sysw} {words}: {v['count']}" + (f" ({ops})" if ops else '')
        if 'name' in v: return f"{sysw} {words}: {nm(v['name'])}"
        return f"{sysw} {words}"
    if isinstance(v, list):
        flat = [x for x in v for x in (x if isinstance(x, list) else [x])]
        names = []
        for x in flat[:8]:
            if isinstance(x, dict):
                n = nm(x.get('name') or x.get('displayName') or x.get('bagType') or x.get('monsterName') or x.get('saltName') or x.get('type') or '')
                extra = (f" x{short(x['amount'])}" if x.get('amount') and x.get('amount') != 1 else '') + (f" -> {x['to']}" if x.get('to') else '')
                extra += f" {x['remaining']} left" if x.get('remaining') is not None else ''
                names.append((n + extra).strip())
            else:
                names.append(str(x))
        return f"{sysw} {words} ({len(flat)}): " + ', '.join(n for n in names if n) + (' ...' if len(flat) > 8 else '')
    return f"{sysw} {words}"


def alert_owner(key):
    best = max((p for p in ROUTE if key.startswith(p)), key=len, default=None)
    sysk = ROUTE.get(best)
    own = S1.owners(sysk) if sysk else []
    return sysk, (own[0] if own else LIGHT)


def routed_alerts():
    al = Z.get('alerts') or {}
    out = {}
    for sec, a in (al.get('account') or {}).items():
        for key, v in _leaves(a, [sec]):
            if key.startswith('World 3.construction.saltDeficit'): continue   # Zack 2026-11-28: salt flags only on a real stall (phase_d.salt_check)
            sysk, own = alert_owner(key)
            ln = _pretty(key, v)
            if ln: out.setdefault(own, []).append((sysk or 'unrouted', ln))
    for c in al.get('characters') or []:
        for key, v in _leaves(c.get('alerts') or {}, ['char']):
            if key.startswith('char.classSpecific.betterRing.'):
                if key.endswith('.displayName'): out.setdefault(c['name'], []).append(('equipment', f"better ring in inventory: {nm(v)} (equip it)"))
                continue
            if key == 'char.talents.unmaxedTalents': continue   # used by talent books check
            ln = _pretty(key.replace('char.', 'World X.'), v)
            if not ln: continue
            ln = re.sub(r'^x (\w+) \1\b', r'\1', ln[0:]).replace('x ', '', 1) if ln.startswith('x ') else ln
            ln = re.sub(r'\b(\w+) (?:\w+ )?\1\b', r'\1', ln, count=1)   # "tools tools", "bags unmaxed bags"
            out.setdefault(c['name'], []).append(('self', ln))
    return out


_RA = None
def c_missables(name):
    global _RA
    if _RA is None: _RA = routed_alerts()
    rows = _RA.get(name) or []
    if not rows:
        if not Z.get('alerts'): return ('Toolbox alerts', 'Toolbox alerts: missing from this parse (re-run tools/tb_parse.sh)', [])
        return None
    unowned = [r for s, r in rows if name == LIGHT and s != 'self' and not [o for o in S1.owners(s)]]
    subs = [r.strip() for s, r in rows]
    return ('toolbox_alerts', f"Toolbox alerts ({len(rows)}): do these before AFK" + (f" ({len(unowned)} unowned, given to the lightest load)" if unowned else ''), subs)


# ---------- Alchemy: affordable bubble levels + vial print-swap (pending L4) ----------
def c_bubbles():
    bc = Z.get('bubbleCosts')
    if not bc: return ('alchemy_bubbles', 'Bubbles: costs missing from this parse (re-run tools/tb_parse.sh)', [])
    ok = sorted((b for b in bc if b['affordable'] > 0), key=lambda b: -b['affordable'])
    stuck = sorted((b for b in bc if b['affordable'] == 0), key=lambda b: -b['level'])
    subs = [f"{nm(b['name']).title()} ({b['cauldron']}) lv {b['level']}: +{b['affordable']} levels affordable now (runs out of {nm(b['limitedBy'])} first)" for b in ok[:10]]
    if stuck:
        subs.append('short for even 1 level: ' + '; '.join(
            f"{nm(b['name']).title()} lv {b['level']} needs " + ', '.join(f"{short(m['cost'])} {nm(m['name'])} (have {short(m['owned']) if m['owned'] is not None else 'not tracked'})" for m in b['next'] if (m['owned'] or 0) < m['cost'])
            for b in stuck[:5]))
    return ('alchemy_bubbles', f"Bubbles: {len(ok)} / {len(bc)} can level now with what you own (Toolbox cost math; which to push = the bubble goals above, rest my read: biggest gain first)", subs)


def printed():
    """rawName -> [(character, per-day)] for every active print (Toolbox printer value)."""
    out = {}
    for i, slots in enumerate(A.get('printer') or []):
        for s in slots or []:
            if s.get('active') and s.get('item') and s.get('item') != 'Blank':
                out.setdefault(s['item'], []).append((NAMES[i] if i < len(NAMES) else i, s.get('boostedValue') or s.get('value') or 0))
    return out


def c_vials():
    vs = A.get('alchemy', {}).get('vials') or []
    pr = printed(); subs = []
    open_ = [v for v in vs if 0 < (v.get('level') or 0) < VIAL_MAX and v.get('mainItem') and not str(v.get('mainItem')).startswith('Liquid')]
    # level-now first, then closest to max (owned / cost-to-max); show 12, rest counted
    key = lambda v: (stor(v['mainItem']) < VIAL_COST[v['level']], -stor(v['mainItem']) / max(1, sum(VIAL_COST[v['level']:VIAL_MAX])))
    open_.sort(key=key)
    for v in open_[:12]:
        lv, raw = v['level'], v['mainItem']
        need = sum(VIAL_COST[lv:VIAL_MAX]); nxt = VIAL_COST[lv]; have = stor(raw)
        p = pr.get(raw); rate = sum(x for _, x in p) if p else None; gr = per_day(raw)
        if have >= nxt:
            subs.append(f"{nm(v['name']).title()} {lv} -> {lv + 1}: costs {short(nxt)} {item_name(raw)}, you have {short(have)}: level it now")
            continue
        if p:
            d = (need - have) / rate if rate else None
            subs.append(f"{nm(v['name']).title()} {lv}/13: {short(have)} / {short(need)} {item_name(raw)} to max, printing on {', '.join(str(c) for c, _ in p)} ({short(rate)}/day): ~{d:.0f} days" if d else f"{nm(v['name']).title()} {lv}/13: printing, rate unknown")
        else:
            subs.append(f"{nm(v['name']).title()} {lv}/13: {short(have)} / {short(need)} {item_name(raw)} to max, NOT printed" + (f" (gaining {short(gr)}/day)" if gr else '') + ": swap a print to it if this vial matters now (Matic prints)")
    if len(open_) > 12: subs.append(f"... {len(open_) - 12} more vials further from max")
    return ('alchemy_vials', f"Vials to max: {len(open_)} open item vials (13 = max), closest first, print-swap check per vial", subs)


# ---------- Fractal Island + Coral Kid (pending L6) ----------
def c_fractal():
    isl = A.get('islands') or {}; f = next((x for x in isl.get('list') or [] if x.get('name') == 'Fractal'), None)
    if not f: return None
    b, bpd = isl.get('bottles') or 0, isl.get('bottlesPerDay') or 0
    if f.get('unlocked'):
        import phase_d as PD
        PD._D = D
        _, t, tl, plan = PD.trash_list()
        return ('islands', f"Fractal Island: unlocked, {short(f.get('hoursAfk'))} AFK hours banked (spend on its rewards)",
                [f"DO NOW trash shop, buy in order ({plan['source']}, {short(t.get('trash'))} trash):"] + tl)
    gap = (f.get('cost') or 0) - b
    eta = f", ~{gap / bpd:.0f} days at {bpd}/day" if gap > 0 and bpd else ''
    return ('islands', f"Fractal Island: locked, {short(b)} / {short(f.get('cost'))} bottles" + (' (buy it now)' if gap <= 0 else eta),
            [f"unclaimed island days: {isl.get('numberOfDaysAfk')} (claim bottles daily so they don't cap)"])


def total_div_lv():
    return sum(((c.get('skillsInfo') or {}).get('divinity') or {}).get('level') or 0 for c in CH)


def c_coral_kid():
    cr = A.get('coralReef') or {}; ups = cr.get('coralKidUpgrades') or []
    if not ups: return None
    dp = (A.get('divinity') or {}).get('divinityPoints') or 0; tl = total_div_lv(); subs = []
    for u in ups:
        req = u.get('divinityLevelReq') or 0; d = nm(u.get('description')).split('@')[0][:70]
        if tl < req: subs.append(f"#{u['index']} locked: total Divinity LV {tl} / {req} ({d})"); continue
        can = dp >= (u.get('cost') or 1e99)
        subs.append(f"#{u['index']} lv {u.get('level')}: next {short(u.get('cost'))} Divinity PTS" + (' (can buy)' if can else f" (have {short(dp)})") + f" ({d})")
    return ('divinity_coral_kid', f"Coral Kid: {cr.get('coralKidUpgradeLevelTotal')} upgrade levels, {short(dp)} Divinity PTS banked, total Divinity LV {tl} (buy order = gap, my read: cheapest open first)", subs)


# ---------- Lab per character + jewel end goal (pending L10, L17) ----------
def c_lab_chars():
    L = A.get('lab') or {}
    conn = {x.get('name') for x in L.get('connectedPlayers') or []}
    subs = []
    for i, c in enumerate(L.get('playersCords') or []):
        n = c.get('playerName') or NAMES[i]
        pc = (L.get('playersChips') or [])[i] if i < len(L.get('playersChips') or []) else []
        chips = [nm(x.get('name')) for x in (pc if isinstance(pc, list) else []) if isinstance(x, dict) and x.get('name')]
        if n in conn: st = 'connected'
        elif not c.get('lineWidth'): st = 'not in the lab (no lab bonuses while away; fine if their job is elsewhere)'
        else: st = 'in the lab but NOT connected: move them inside a lit line'
        subs.append(f"{n}: {st}" + (f", range {c.get('lineWidth')}" if c.get('lineWidth') else '') + f", chips {', '.join(chips) or 'none'}")
    js = L.get('jewels') or []; miss = [j for j in js if not j.get('acquired')]
    for j in miss:
        req = '; '.join(f"{short(r.get('amount'))} {nm(r.get('name'))} (have {short(stor_by_name(r.get('name'))) if stor_by_name(r.get('name')) is not None else 'not in storage: check in game'})" for r in j.get('requirements') or [])
        subs.append(f"jewel goal: {nm(j['name'])}: {req}")
    nc = sum(1 for s in subs if 'NOT connected' in s); away = sum(1 for s in subs if 'not in the lab' in s)
    return ('lab_chars', f"Lab positions: {len(conn)} / {len(L.get('playersCords') or [])} connected; jewel end goal = all {len(js)} ({len(js) - len(miss)} owned)" + (f"; {nc} need moving" if nc else '') + (f"; {away} away from the lab" if away else ''), subs)


# ---------- Trigger map (pending L11): brain/triggers.yaml, Divinity first ----------
def metrics():
    dv = A.get('divinity') or {}; m = {'total_div_lv': total_div_lv(), 'god_rank': dv.get('godRank') or 0,
                                       'div_pts': dv.get('divinityPoints') or 0}
    for c in CH:
        m[f"div_lv:{c.get('name')}"] = ((c.get('skillsInfo') or {}).get('divinity') or {}).get('level') or 0
    m['blessings_maxed'] = sum(1 for d in dv.get('deities') or [] if (d.get('level') or 0) >= (d.get('maxLevel') or 1e9))
    m['deities'] = len(dv.get('deities') or [])
    for u in (A.get('coralReef') or {}).get('coralKidUpgrades') or []:
        m[f"coral_kid_req:{u['index']}"] = u.get('divinityLevelReq') or 0
    m['vials_maxed'] = sum(1 for v in A.get('alchemy', {}).get('vials') or [] if (v.get('level') or 0) >= VIAL_MAX)
    return m


def c_triggers(name):
    """brain/triggers.yaml (Phase C B, 2026-11-28): when_path + op + value read live every pull (model/livepath.py).
    Card = row owner, or the owner of `target:` system when set. Fired = DO NOW; armed = next; no path = check in game."""
    f = ROOT / 'brain' / 'triggers.yaml'
    if not f.exists(): return None
    import livepath as LP
    T = yaml.safe_load(open(f)) or {}; subs = []
    try:
        import goals as GL; G = GL.load()['systems']
    except Exception: G = {}
    for t in T.get('triggers') or []:
        g = G.get(t.get('target')) or {} if t.get('target') else {}
        own = g.get('owners') if g.get('owners') else [x.strip() for x in str(t.get('owner') or '').split(',')]
        if name not in own: continue
        st, cur, val = LP.check(t); src = t.get('source', 'my read'); tag = f"[{t['system']}]"
        if st == 'fired': subs.append(f"{tag} DO NOW: {t['then']} (fired: {t['when']}, {LP.fmt(cur)} / {LP.fmt(val)}) ({src})")
        elif st == 'armed': subs.append(f"{tag} next: {t['when']} ({LP.fmt(cur)} / {LP.fmt(val)}) -> {t['then']} ({src})")
        elif st == 'missing': subs.append(f"{tag} next: {t['when']}: {t.get('when_path')} not in save, check in game -> {t['then']} ({src})")
        else: subs.append(f"{tag} next: {t['when']}: no path yet, check in game -> {t['then']} ({src})")
    if not subs: return None
    fired = sum(' DO NOW:' in s for s in subs)
    return ('triggers', f"Triggers: {fired} fired (do now), {len(subs) - fired} next", sorted(subs, key=lambda s: ' DO NOW:' not in s))


# ---------- Rotation-aware weeks (pending L12) ----------
BOOST_SYS = [  # keyword in ballot / meritocracy text -> systems it boosts (my read on the mapping)
    ('damage', 'fighting pushes, kill goals, Death Note'), ('class_exp', 'leveling, Spelunking'), ('skill_exp', 'skilling catch-ups'),
    ('drop', 'drop-rate farming, bag sweep, Cat frogs'), ('cooking', 'Cooking, meals'), ('construction', 'Construction'),
    ('refinery', 'Refinery, salts'), ('sailing', 'Sailing'), ('gaming', 'Gaming'), ('divinity', 'Divinity'), ('breeding', 'Breeding'),
    ('farming', 'Farming'), ('summoning', 'Summoning'), ('sneaking', 'Sneaking/Jade'), ('alchemy', 'Alchemy'), ('lab', 'Lab'),
    ('artifact', 'Sailing artifacts'), ('crop', 'Farming'), ('shiny', 'Breeding shinies'), ('jade', 'Sneaking'), ('spelunk', 'Spelunking'),
    ('mining', 'Mining'), ('choppin', 'Choppin'), ('fishing', 'Fishing'), ('catching', 'Catching'), ('trapping', 'Trapping'),
    ('worship', 'Worship'), ('stat', 'everything a bit'), ('coin', 'money'), ('cash', 'money'), ('efficiency', 'skilling AFK'),
]


def _boost_targets(txt):
    t = str(txt).lower()
    return sorted({v for k, v in BOOST_SYS if k in t}) or ['needs mapping']


def c_rotation():
    V = A.get('voteBallot') or {}; subs = []
    rows = [('Ballot', nm(b.get('0')).replace('{', str(b.get('1'))).replace('}', str(b.get('1'))), b.get('active')) for b in V.get('bonuses') or []]
    rows += [('Meritocracy', nm(b.get('description')).replace('{', str(b.get('bonus'))).replace('}', str(b.get('bonus'))), b.get('active')) for b in V.get('meritocracyBonuses') or []]
    if not rows: return None
    on = [r for r in rows if r[2]]
    for src, txt, _ in on:
        subs.append(f"HARD-FOCUS ({src} boost up now): {txt[:70]} -> {', '.join(_boost_targets(txt))}")
    off = {t for _, txt, a in rows if not a for t in _boost_targets(txt)} - {t for _, txt, _ in on for t in _boost_targets(txt)} - {'needs mapping'}
    if off: subs.append('HOLD slow, non-urgent tasks in: ' + ', '.join(sorted(off)) + ' (their boost is on the ballot list but not up this week; quick tasks still go now)')
    subs.append('OPPORTUNISTIC: any quick task in a boosted system jumps the queue this week')
    vf = (A.get('serverVars') or {}).get('_carried') or ''
    return ('rotation', "This week's rotation (Ballot + Meritocracy): hard-focus / opportunistic / hold (mapping is my read)" + (f" [votes from save {vf}]" if vf else ''), subs)


# ---------- Quest-only greenstacks on Tachio (pending L13 in old numbering L302) ----------
def c_quest_gs():
    seen = {}
    for w, npcs in (A.get('quests') or {}).items():
        for npc in npcs:
            for q in npc.get('npcQuests') or []:
                for raw in q.get('missableDrops') or []:
                    open_ = [NAMES[p['charIndex']] for p in q.get('progress') or [] if p.get('status') == 0 and p['charIndex'] < len(NAMES)]
                    notyet = [NAMES[p['charIndex']] for p in q.get('progress') or [] if p.get('status') == -1 and p['charIndex'] < len(NAMES)]
                    s = seen.setdefault(raw, {'quests': [], 'open': set(), 'notyet': set()})
                    s['quests'].append(f"{nm(npc.get('name'))}: {nm(q.get('Name'))}"); s['open'] |= set(open_); s['notyet'] |= set(notyet)
    subs, closed = [], []
    for raw, s in seen.items():
        have = stor(raw)
        if have >= GS: continue
        if not s['open'] and not s['notyet']:
            closed.append(f"{item_name(raw)} {short(have)}"); continue
        r = per_day(raw)
        where = ('open on ' + ', '.join(sorted(s['open']))) if s['open'] else (('not started on ' + ', '.join(sorted(s['notyet'])[:3])) if s['notyet'] else 'CLOSED on every character (gone)')
        d = f", ~{(GS - have) / r:.0f} days to 10M at {short(r)}/day" if r and r > 0 else ', no farm rate yet (needs 2 pulls 12+ h apart)'
        tach = ' (Tachio holds it)' if LIGHT in s['open'] else (' (start it on Tachio)' if LIGHT in s['notyet'] else '')
        subs.append(f"{item_name(raw)} {short(have)} / 10M: {s['quests'][0]}, {where}{tach}{d}")
    if closed: subs.append(f"quest closed on every character, can't farm these any more: {', '.join(closed)}")
    if not subs: return None
    return ('quest_greenstacks', f"Quest-only drops not greenstacked: {len(subs) - (1 if closed else 0)} still farmable (only drop while the quest is open; my read: keep each open on Tachio until 10M)", subs)


# ---------- Inventory + storage + carry capacity sweep (pending L14) ----------
def c_inventory():
    st = A.get('storage') or {}; slots = (st.get('slots') or {}).get('value') or 0; used = len(st.get('list') or [])
    subs = [f"storage: {used} / {slots} slots used" + (' (nearly full: clear junk)' if slots and used / slots > .9 else '')]
    bagsets = [{nm(b.get('displayName')) for b in c.get('invBagsUsed') or [] if not b.get('acquired')} for c in CH]
    carsets = [{k for k, v in (c.get('maxCarryCap') or {}).items() if k not in ('fillerz', 'Quests') and v < 35000} for c in CH]
    cb, cc = set.intersection(*bagsets) if bagsets else set(), set.intersection(*carsets) if carsets else set()
    if cb: subs.append('missing on every character (event/shop bags, skip unless offered): ' + ', '.join(sorted(cb)))
    if cc: subs.append(f"carry caps under max on every character ({len(cc)}): " + ', '.join(sorted(cc)) + ' (Toolbox: max is 35K; craft the next carry bag tier when the mats are cheap)')
    for c in CH:
        inv = len([x for x in c.get('inventory') or [] if x.get('rawName') not in (None, 'Blank')]); sl = c.get('inventorySlots') or 0
        bags = [nm(b.get('displayName')) for b in c.get('invBagsUsed') or [] if not b.get('acquired') and nm(b.get('displayName')) not in cb]
        car = [k for k, v in (c.get('maxCarryCap') or {}).items() if k not in ('fillerz', 'Quests') and v < 35000 and k not in cc]
        bits = [f"inventory {inv}/{sl}" + (' FULL-ish' if sl and inv / sl > .85 else '')]
        if bags: bits.append('missing bags: ' + ', '.join(bags[:4]))
        if car: bits.append(f"carry caps under max: {', '.join(car)}")
        if len(bits) > 1 or 'FULL' in bits[0]: subs.append(f"{c.get('name')}: " + '; '.join(bits))
    return ('inventory', 'Inventory + storage + carry cap sweep: one active session on Tachio (craft/buy the missing carry bags, empty full inventories; my read)', subs)


# ---------- Construction trimmed-slot priority (pending L15), shared by Tastic + Matic ----------
# Uses Toolbox's Buildings page math (account._zack.web.buildings): real max level incl. extra levels, build cost, hours left.
GRIFFY_BUILD = [('Death_Note', 'Griffy 2026-11-07/10-28: upgrade while cheap, more multikill'),
                ('Talent_Book_Library', 'Griffy 2026-10-28: faster checkouts'),
                ('Automation_Arm', 'Griffy 2026-10-04: build toward it (unlocks the MSA)'),
                ('Trapper_Drone', 'Griffy 2026-10-04: build toward it')]
WEB = Z.get('web') or {}


def _hrs(h):
    if h is None: return '?'
    if h <= 0: return 'READY: claim it'
    if h < 0.1: return 'under 6 min'
    return f"{h:.1f} h" if h < 48 else f"{h / 24:.0f} d"


def c_construction_slots():
    B = WEB.get('buildings') or {}
    bs = B.get('list') or []
    if not bs or isinstance(B, dict) and B.get('error'): return ('construction_slots', 'Construction: building data missing from this parse (re-run tools/tb_parse.sh)', [])
    open_ = [b for b in bs if (b.get('level') or 0) < (b.get('maxLevel') or 0)]
    gated = [b for b in open_ if not (b.get('buildCost') or 0) > 0]   # cost 0 = level-gated (Toolbox gives no cost)
    open_ = [b for b in open_ if b not in gated]
    import phase_d as PD; PD._D = D   # Zack 2026-11-28: only salts that stall (or are about to) count as short
    salt = ', '.join(sorted({nm(r['salt']) for r in PD.salt_rows() if r['cycles'] < 1 or (r['deficit'] and r['cycles'] < PD.STALL_SOON_CYCLES)}))
    fmt = lambda b, why: (f"{nm(b['name'])} {b['level']}/{b['maxLevel']}" + (' [in trimmed slot]' if b.get('isSlotTrimmed') else ' [in a slot]' if b.get('slot', -1) != -1 else '')
                          + f", next level {_hrs(b.get('trimmedHoursLeft') if b.get('isSlotTrimmed') else b.get('hoursLeft'))}" + f" ({why})")
    order, subs = [], []
    for raw, why in GRIFFY_BUILD:
        b = next((x for x in open_ if x.get('name') == raw), None)
        if b: order.append(b); subs.append(f"{len(order)}. " + fmt(b, why))
    # my read for the rest: shortest trimmed build first, since a trimmed slot is ~{boost}x faster
    rest = sorted((b for b in open_ if b not in order), key=lambda b: (b.get('trimmedHoursLeft') if b.get('trimmedHoursLeft') is not None else 1e9))
    for b in rest[:6]:
        order.append(b); subs.append(f"{len(order)}. " + fmt(b, 'my read: quickest in a trimmed slot'))
    ready = [nm(b['name']) for b in bs if b.get('slot', -1) != -1 and ((b.get('trimmedHoursLeft') if b.get('isSlotTrimmed') else b.get('hoursLeft')) or 1) <= 0]
    if ready: subs.insert(0, 'READY to level now: ' + ', '.join(ready))
    if gated: subs.append('no build cost yet (level-gated, check what unlocks the next level in game): ' + ', '.join(f"{nm(b['name'])} {b['level']}/{b['maxLevel']}" for b in gated))
    if salt: subs.append(f"salt-short (Griffy: build Boulder Rollers instead of Poisonic when salts run out): {salt}")
    return ('construction_slots', f"Construction: {B.get('trimmedSlots')} trimmed slots at {B.get('trimmedBoost', 0):.1f}x speed; {len(open_) + len(gated)} buildings not maxed (Tastic + Matic share this list)", subs)


# ---------- website-only numbers, now from Toolbox's own functions (pending gaps, 2026-11-28) ----------
def c_drop_rate():
    dr = [d for d in WEB.get('dropRate') or [] if isinstance(d.get('dropRate'), (int, float))]
    if not dr: return None
    dr.sort(key=lambda d: -d['dropRate'])
    rg = [d for d in dr if any(c.get('name') == d['name'] and 'Royal' in str(c.get('class')) for c in CH)]
    best = rg[0] if rg else dr[0]
    return ('drop_rate', f"Drop rate (Toolbox formula): best Royal Guardian = {best['name']} {best['dropRate']:.0f}% -> they do the bag sweep (Zack's plan)",
            ['all: ' + ', '.join(f"{d['name']} {d['dropRate']:.0f}" for d in dr)])


def c_atoms():
    a = A.get('atoms') or {}; ph = WEB.get('atomParticlesPerHour')
    if not a: return None
    p = a.get('particles') or 0; subs = []
    up = sorted((x for x in a.get('atoms') or [] if not x.get('locked') and (x.get('level') or 0) < (x.get('maxLevel') or 0)), key=lambda x: x.get('cost') or 1e99)
    for x in up[:6]:
        c = x.get('cost') or 0
        when = 'can buy now' if p >= c else (f"in {(c - p) / ph:.0f} h" if isinstance(ph, (int, float)) and ph > 0 else 'rate unknown')
        subs.append(f"{nm(x['name'])} {x['level']}/{x['maxLevel']}: next {short(c)} particles ({when})")
    rate = f", +{short(ph)}/hr ({short(ph * 24)}/day)" if isinstance(ph, (int, float)) else ''
    return ('atom_collider', f"Atoms: {short(p)} particles{rate}; cheapest next levels below (buy order = gap, my read: cheapest first)", subs)


TACH = {0: 'Purple', 1: 'Brown', 2: 'Green', 3: 'Red', 4: 'Silver', 5: 'Gold'}


def c_tesseract_maps():
    mp = WEB.get('tesseractMaps')
    if not isinstance(mp, list) or not mp: return None
    try:
        sys.path.insert(0, str(ROOT / 'model'))
    except Exception: pass
    best = {}
    for m in mp:
        if not m.get('unlocked'): continue
        t_ = m.get('tachyonType'); q = m.get('tachyonQuantity') or 0
        if t_ is None: continue
        if q > best.get(t_, (0, ''))[0]: best[t_] = (q, nm(m.get('mapName')))
    subs = [f"{TACH.get(k, k)} tachyon: best unlocked map {v[1]} ({v[0]:.2f} per drop)" for k, v in sorted(best.items())]
    opt = WEB.get('tesseractOptimizer') or {}
    for cat in ('damage', 'tachyons'):
        st = opt.get(cat)
        if isinstance(st, list) and st:
            seen = []
            for s in st:
                n = nm(s.get('name'))
                if n not in seen: seen.append(n)
            subs.append(f"Toolbox optimizer ({cat}): " + ' > '.join(seen[:4]))
    locked = sum(1 for m in mp if not m.get('unlocked'))
    return ('tesseract', f"Tesseract: tachyon per map + Toolbox upgrade optimizer ({len(mp) - locked} maps open, {locked} locked)", subs)


def c_spelunk_opt():
    so = WEB.get('spelunkingOptimizer') or {}
    subs = []
    for k, lab in (('power', 'POW'), ('amber', 'amber gain')):
        st = so.get(k)
        if isinstance(st, list) and st:
            seen = []
            for s in st:
                n = nm(s.get('name'))
                if n not in seen: seen.append(n)
            subs.append(f"{lab} buy order (Toolbox optimizer): " + ' > '.join(seen[:4]) + f" (next {short(st[0].get('cost'))} amber)")
    if not subs: return None
    return ('spelunk', f"Spelunking upgrades: Toolbox optimizer on {so.get('character')} (highest Spelunking)", subs)


def c_lab_shop():
    L = A.get('lab') or {}; rot = L.get('currentRotation') or []; chips = L.get('chips') or []
    if not rot: return None
    names = []
    for i in rot:
        c = next((x for x in chips if x.get('index') == i), None)
        if c:
            req = ', '.join(f"{short(r.get('amount'))} {nm(r.get('name'))}" for r in c.get('requirements') or [])
            names.append(f"{nm(c.get('name'))} ({req})")
    return ('lab_chips', f"Lab chip shop this rotation: {len(names)} chips", names)


def c_ninja():
    u = WEB.get('ninjaUpgradeCosts')
    if not isinstance(u, list): return None
    jade = (A.get('sneaking') or {}).get('jadeCoins') or 0
    try: jade = float(jade)
    except (TypeError, ValueError): jade = 0
    ok = sorted((x for x in u if x.get('unlocked') and isinstance(x.get('cost'), (int, float))), key=lambda x: x['cost'])
    aff = [x for x in ok if x['cost'] <= jade]
    subs = [f"{nm(x['name'])} lv {x['level']}: {short(x['cost'])} jade" + (' (can buy)' if x['cost'] <= jade else '') for x in ok[:6]]
    return ('sneaking', f"Ninja knowledge: {short(jade)} jade, {len(aff)} upgrades affordable (buy order = gap, my read: cheapest first)", subs)


def c_minehead():
    m = A.get('minehead') or {}
    if not m: return None
    aff = [x for x in m.get('upgrades') or [] if x.get('canAfford')]
    subs = [f"affordable: {nm(x.get('description'))[:60]} ({short(x.get('cost'))})" for x in aff[:5]]
    return ('minehead', f"Minehead: {m.get('dailyTriesLeft')} / {m.get('dailyTriesMax')} tries left today, {m.get('opponentsBeat')} / {len(m.get('opponents') or [])} opponents beaten, {short(m.get('mineCurrency'))} currency", subs)


def c_minigames():
    hs = {x.get('name'): x for x in (A.get('highscores') or {}).get('minigameHighscores') or []}
    subs = []
    for key, lab in (('hoops', 'Basketball (hoops)'), ('darts', 'Darts')):
        x = hs.get(key)
        if not x: continue
        lock = [u for u in x.get('upgrades') or [] if not u.get('unlocked')]
        nxt = min((u.get('cost') or 1e99 for u in x.get('upgrades') or [] if u.get('unlocked')), default=None)
        subs.append(f"{lab}: best {x.get('score')}, {x.get('totalPoints')} points; cheapest next upgrade {short(nxt)}" + (f"; {len(lock)} locked (next at {lock[0].get('pointsToUnlock')} points)" if lock else ''))
        try:
            import trophies as _TR; tl = _TR.minigame_line(key)
            if tl: subs.append(f"  trophy: {tl}")
        except Exception: pass
    try:
        import trophies as _TR; tl = _TR.minigame_line('fishing')
        if tl: subs.append(f"Fishing minigame trophy: {tl}")
    except Exception: pass
    if not subs: return None
    return ('minigames', 'Minigames: points and upgrades (check spend in game)', subs)


def c_event_shop():
    ev = WEB.get('eventShop') or {}
    if not ev or ev.get('error'): return None
    stars = (A.get('accountOptions') or [None] * 999)
    want = [b for t_ in ev.get('tiers') or [] for b in t_.get('bonuses') or [] if not b.get('owned')]
    subs = [f"not owned this event: {nm(b.get('name'))} {b.get('price')} pts ({nm(b.get('description'))[:50]})" for b in want[:8]]
    off = [b for b in ev.get('offRotation') or [] if not b.get('owned')]
    if off: subs.append(f"off rotation (wait for it): " + ', '.join(nm(b.get('name')) for b in off[:6]))
    return ('event_points_shop', f"Event shop: {ev.get('currentEvent')}, {len(want)} unowned in rotation" + (f", {ev.get('starsToFinish')} points to finish" if ev.get('starsToFinish') is not None else ''), subs)


# ---------- Talent books: 2 checkouts / day / character + sub-200 bumps (pending L16) ----------
_TR = None
def c_talent_books(name):
    global _TR
    if _TR is None:
        f = ROOT / 'plans' / f'talents_{D.stamp}.json'
        if not f.exists():
            fs = sorted((ROOT / 'plans').glob('talents_*.json')); f = fs[-1] if fs else None
        _TR = json.load(open(f))['ranked'] if f else []
    mine = sorted((r for r in _TR if r['char'] == name), key=lambda r: r['rank'])[:2]
    ch = next((c for c in (Z.get('alerts') or {}).get('characters') or [] if c.get('name') == name), {})
    um = ((ch.get('alerts') or {}).get('talents') or {}).get('unmaxedTalents') or []
    low = sorted((t for t in um if (t.get('level') or 0) < 200), key=lambda t: (t.get('level') or 0))
    if not mine and not low: return None
    subs = []
    if mine: subs.append('checkouts today (2): ' + '; '.join(f"#{r['rank']} {r['talent']} {r['lv']} -> {r['max']}" for r in mine))
    if low: subs.append('sub-200 bumps (book lifts these the most): ' + ', '.join(f"{nm(t['name']).title()} {t['level']} -> {t.get('target')}" for t in low[:6]))
    books = (A.get('libraryTimes') or {}).get('bookCount')
    return ('talent_books', f"Talent books: perfect checkout = 2 a day on this character" + (f" ({books} books in the library now)" if books else ''), subs)


def _pd(fn_name):
    def f():
        import phase_d as PD
        PD._D = D   # reuse the save syscheck already loaded
        return getattr(PD, fn_name)()
    return f


CHECKS2 = {'refinery_salt': _pd('salt_check'), 'obol_meta': _pd('obol_check'), 'spelunk_lore': _pd('lore_check'),'alchemy_bubbles': c_bubbles, 'alchemy_vials': c_vials, 'islands': c_fractal, 'divinity_coral_kid': c_coral_kid,
           'lab_chars': c_lab_chars, 'rotation': c_rotation, 'quest_greenstacks': c_quest_gs, 'inventory': c_inventory,
           'construction_slots': c_construction_slots, 'drop_rate': c_drop_rate, 'atom_collider': c_atoms,
           'tesseract': c_tesseract_maps, 'spelunk': c_spelunk_opt, 'lab_chips': c_lab_shop, 'sneaking': c_ninja,
           'minehead': c_minehead, 'minigames': c_minigames, 'event_points_shop': c_event_shop}
OWN2 = {'refinery_salt': S1.owners('refinery'), 'obol_meta': [LIGHT], 'spelunk_lore': S1.owners('spelunk'),'lab_chars': ['Autistocat'], 'rotation': ['Autistotle'], 'quest_greenstacks': [LIGHT], 'inventory': [LIGHT],
        'construction_slots': ['Autistastic', 'Autistomatic'], 'alchemy_vials': ['Autistocat', 'Autistomatic'],
        'drop_rate': ['Autistastic', 'Autistomatic'], 'minehead': [LIGHT], 'minigames': [LIGHT]}
PER_CHAR = {'toolbox_alerts': c_missables, 'triggers': c_triggers, 'talent_books': c_talent_books}


def owners2(k):
    return OWN2.get(k) or S1.owners(k)


def lines(name):
    out = []
    for k, fn in CHECKS2.items():
        if name not in owners2(k): continue
        try:
            r = fn()
            if r: out.append(r)
        except Exception as e:
            out.append((k, f"{k.replace('_', ' ').title()}: check failed ({type(e).__name__}: {str(e)[:60]}), fix in model/syscheck2.py", []))
    for k, fn in PER_CHAR.items():
        try:
            r = fn(name)
            if r: out.append(r)
        except Exception as e:
            out.append((k, f"{k.replace('_', ' ').title()}: check failed ({type(e).__name__}: {str(e)[:60]}), fix in model/syscheck2.py", []))
    return out


if __name__ == '__main__':
    NICK = {'zemo': 'Autiszemo', 'cat': 'Autistocat', 'ticles': 'Autisticles', 'tastic': 'Autistastic', 'bish': 'Autistabish', 'tacular': 'Autistacular',
            'totle': 'Autistotle', 'matic': 'Autistomatic', 'naut': 'Autistronaut', 'topher': 'Autistopher', 'tachio': 'Autistachio'}
    who = [NICK.get(a.lower(), a) for a in sys.argv[1:]] or list(NICK.values())
    print(f"save {D.stamp}, {D.age_hours:.1f} h old")
    for n in who:
        print(f"## {n}")
        for s, l, subs in lines(n):
            print('- ' + l); [print('   ' + x) for x in subs]
