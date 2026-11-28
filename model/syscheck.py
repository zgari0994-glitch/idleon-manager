"""Per-system status checks from Toolbox's parser (data.py). One owner, one line per system,
format "System: current -> goal (next)". Sub-lines carry detail. Built 2026-11-27 (pending_changes cleanup).
Every line is data; anything that is my read (no creator source) says "my read".
Usage: import syscheck; syscheck.lines('Autistabish') -> [(system, line, [sub...]), ...]
Dry run: python3 model/syscheck.py [nickname]"""
import json, sys, re
from pathlib import Path
import yaml
sys.path.insert(0, str(Path(__file__).resolve().parent))
import data

ROOT = Path(__file__).resolve().parent.parent
D = data.load()
IDX = yaml.safe_load(open(ROOT / 'model' / 'system_index.yaml')) or {}
# owner overrides where jobs.yaml says "unassigned" but Zack routed it (source in comment)
OVERRIDE = {
    'worship': ['Autistacular'],          # Zack 2026-11-16: worship totems = Beast Master line (Tacular)
    'alchemy_cauldrons': ['Autistocat'],
    'worship_skulls': ['Autistacular'],   # every-character sweep (pending L265), worship owner
    'breeding': None,                     # falls through to system_index owners  # pending L23: liquids + sigils are Cat's daily alchemy check
}
G = lambda s: D.system(s, allow_empty=True)
nm = lambda s: re.sub(r'\s*[{}]x?', '', str(s or '').replace('_', ' ')).strip()


def short(n):
    try: n = float(n)
    except (TypeError, ValueError): return str(n)
    if abs(n) >= 1e18: return f"{n:.2e}"
    for u, v in (('Q', 1e15), ('T', 1e12), ('B', 1e9), ('M', 1e6), ('K', 1e3)):
        if abs(n) >= v: return f"{n / v:.3g}{u}"
    return f"{n:.0f}" if n == int(n) else f"{n:.2f}"


def eta(key, cur, goal):
    try:
        import growth
        return growth.eta(key, cur, goal)
    except Exception:
        return ''


# ---------- checkers: each returns (line, [subs]) or None ----------
def c_caverns():
    v = G('caverns'); cv = v['caverns']; s = []
    f = lambda k: cv.get(k) or {}
    ev, ml, gr, dn, gb = f('evertree'), f('motherlode'), f('grotto'), f('theDen'), f('gambit')
    s.append(f"Motherlode: layer {ml.get('layer')}, {ml.get('layerBreaksLeft')} breaks left on this layer")
    s.append(f"Den: best {short(dn.get('bestScore'))} -> next opal at {short(dn.get('nextOpalAt'))}")
    for k in ('bravery', 'justice', 'wisdom'):
        c = f(k); nb = c.get('nextHourBreakpoint') or {}
        nxt = next((x for x in nb.values() if isinstance(x, (int, float))), None) if isinstance(nb, dict) else None
        s.append(f"{k.title()} Monument: {c.get('hours')} hrs" + (f" -> next breakpoint {short(nxt)} hrs" if nxt else '') + (', fight ready' if (c.get('timeForNextFight') or 1) <= 0 else ''))
    b = f('theBell'); s.append(f"Bell: {b.get('rings')} rings, {b.get('bellMethodsOwned')} methods owned")
    h = f('theHarp'); s.append(f"Harp: next note {short(h.get('newNoteOwned'))} / {short(h.get('newNoteCost'))}" + (' (can buy)' if (h.get('newNoteOwned') or 0) >= (h.get('newNoteCost') or 1e99) else '') + f", strings {h.get('stringSlots')}")
    lp = f('theLamp'); s.append(f"Lamp: {lp.get('currentWishes')} wishes banked (+{(lp.get('wishPerDay') or 0):.1f}/day): spend them")
    s.append(f"Hive: layer {f('theHive').get('layer')}")
    s.append(f"Grotto: layer {gr.get('layer')}, {short(gr.get('mushroomKillsLeft'))} kills to the Monarch")
    j = f('theJars'); s.append(f"Jars: {j.get('totalJars')} jars, {j.get('unlockedSlots')} slots, new jar costs {short(j.get('newJarCost'))}")
    s.append(f"Evertree: layer {ev.get('layer')}")
    s.append(f"Gambit: {short(gb.get('points'))} -> next opal at {short(gb.get('nextOpalPoints'))}" + (' (attempt ready: run it)' if gb.get('attemptReady') else ''))
    s.append(f"Temple: layer {f('theTemple').get('layer')}, {short(f('theTemple').get('torches'))} torches")
    w = f('theWell'); s.append(f"Well: opal {short(w.get('opalCostOwned'))} / {short(w.get('opalCost'))}" + (' (can trade)' if (w.get('opalCostOwned') or 0) >= (w.get('opalCost') or 1e99) else ''))
    fo = f('theFountain'); s.append(f"Fountain (#16): {fo.get('spacesOwned')} spaces, {fo.get('watersOwned')} waters (just found: build it up)")
    s.append(f"Bottomless Trench: layer {f('theBottomlessTrench').get('layer')}")
    vil = v.get('villagers') or []
    if vil:
        s.append('Villagers: ' + ', '.join(f"{nm(x.get('name') or x.get('villagerName') or i)} {x.get('level', '?')}" + (f" ({x.get('opalInvested')} opals)" if x.get('opalInvested') is not None else '') + (' LEVEL READY' if x.get('readyToLevel') else '') for i, x in enumerate(vil)))
    act = [nm(x.get('name')) for x in (v.get('studies') or {}).get('studies', []) if x.get('active')]
    s.append(f"Study (Bolaia): {', '.join(act) or 'nothing active: pick one'}")
    s.append(f"Schematics: {v.get('totalSchematics')} owned, {v.get('unlockedSchematics')} unlocked")
    return (f"The Hole: {v.get('unlockedCaverns')} caverns, {v.get('totalOpalsFound')} opals found; per cavern below (what to push = gap: no creator order yet, my read = cheapest ready first)", s)


def c_slab():
    v = G('slab'); n, t = v['lootedItems'], v['totalItems']
    return (f"Slab: {n} / {t} items looted ({v['missingItems']} missing){eta('slab', n, t)}", [])


def c_achievements():
    a = G('achievements'); done = sum(1 for x in a if x.get('completed'))
    left = [x for x in a if not x.get('completed') and not x.get('secretAchievement')]
    return (f"Achievements: {done} / {len(a)} done{eta('achievements', done, len(a))}",
            [f"open: {nm(x['name'])}: {nm(x.get('desc'))}" for x in left[:5]] + ([f"+{len(left) - 5} more open"] if len(left) > 5 else []))


def c_lab():
    v = G('lab_mainframe'); js = v.get('jewels') or []
    miss = [x for x in js if not x.get('acquired')]
    subs = []
    for x in miss:
        req = ', '.join(f"{short(r.get('amount'))} {nm(r.get('name'))}" for r in x.get('requirements') or [])
        subs.append(f"missing jewel {nm(x['name'])} ({nm(x.get('description'))}): needs {req}")
    pc = v.get('playersChips') or []
    empty = sum(1 for p in pc if isinstance(p, list) and len([c for c in p if c]) < 2)
    subs.append(f"chips: {v.get('totalRawChips')} raw chips; {empty} characters with an open chip slot" + (': fill them (Lab Chips shop rotation is website-only, check in game)' if empty else ''))
    return (f"Lab: jewels {len(js) - len(miss)} / {len(js)}", subs)


def c_cape():
    v = G('cape_vine'); miss = [x for x in v['allCapes'] if not x.get('isAcquired')]
    return (f"Cape Vine: {v['totalCapes']} / {v['totalEligibleCapes']} capes, golden vines {v.get('goldenVines')} (next at class level {v.get('nextGoldenVineClassLevel')})",
            [f"get {nm(x.get('displayName'))} (craft lv {x.get('lvReqToCraft')})" for x in miss[:8]])


def c_gallery():
    v = G('gallery'); subs = []
    for k, lab in (('allTrophies', 'trophy'), ('allNametags', 'nametag')):
        miss = [nm(x.get('displayName')) for x in v.get(k) or [] if not x.get('isAcquired')]
        if miss: subs.append(f"missing {lab}s ({len(miss)}): " + ', '.join(miss[:8]))
    return (f"Gallery: {v['podiumsOwned']} podiums (lv2 {v['lv2PodiumsOwned']}, lv3 {v['lv3PodiumsOwned']}, lv4 {v['lv4PodiumsOwned']}); push podium levels", subs)


def c_menagerie():
    v = G('menagerie')
    ms = [x for x in v.get('missions') or [] if x.get('visible', True)]
    claim = [x for x in ms if x.get('canClaim')]
    near = sorted((x for x in ms if not x.get('canClaim') and x.get('requirement')), key=lambda x: -(x.get('progress') or 0) / x['requirement'])[:4]
    subs = [f"CLAIM NOW: {nm(x['name'])} ({x.get('claimable')} ready)" for x in claim]
    subs += [f"closest: {nm(x['name'])} {short(x.get('progress'))} / {short(x['requirement'])} ({nm(x.get('description'))})" for x in near]
    aff = [x for x in v.get('boosts') or [] if x.get('affordable') and x.get('visible')]
    if aff: subs.append('affordable boosts: ' + '; '.join(f"{x['description']} lv {x['level']} ({short(x['cost'])} Lumi)" for x in aff[:4]) + ' (buy order = gap, my read: cheapest first)')
    nu = next((x for x in v.get('unlocks') or [] if not x.get('owned')), None)
    if nu: subs.append(f"next unlock: {nm(nu['name'])} for {short(nu['cost'])} Lumi" + (' (can buy)' if v['lumi'] >= nu['cost'] else ''))
    return (f"Menagerie: rank {v['rank']}, Shells {v['shells']} / {v['shellReq']} to rank up (+1 per claimed mission), Lumi {short(v['lumi'])} (+{short(v['lumiRate'])}/hr)", subs)


def c_alchemy():
    a = G('alchemy_cauldrons'); subs = []
    names = ['Water Droplets', 'Liquid Nitrogen', 'Trench Seawater', 'Toxic Mercury']
    for i, (amt, lc) in enumerate(zip(a.get('liquids') or [], a.get('liquidCauldrons') or [])):
        subs.append(f"{names[i] if i < 4 else 'Liquid ' + str(i + 1)}: decant cap lv {lc.get('decantCap', {}).get('level')}, rate lv {lc.get('decantRate', {}).get('level')}" + (' (Dragonic)' if lc.get('isDragonic') else ''))
    vs = a.get('vials') or []
    mx = sum(1 for x in vs if (x.get('level') or 0) >= 13); un = sum(1 for x in vs if (x.get('level') or 0) > 0)
    subs.append(f"Vials: {un} / {len(vs)} unlocked, {mx} maxed (13){eta('vials_maxed', mx, len(vs))}")
    sg = (a.get('p2w') or {}).get('sigils') or []
    on = [x for x in sg if x.get('characters')]
    nx = lambda x: x.get('nextCost') or 0
    on.sort(key=lambda x: (x.get('progress') or 0) / nx(x) if nx(x) else 9, reverse=True)
    if on: subs.append('Sigils charging: ' + '; '.join(f"{nm(x['name'])} {short(x.get('progress'))} / {short(nx(x))}" + (' (next tier ready)' if nx(x) and (x.get('progress') or 0) >= nx(x) else '') for x in on))
    idle = [nm(x['name']) for x in sg if not x.get('characters') and x.get('unlocked') and nx(x)]
    lockd = [x for x in sg if not x.get('unlocked')]
    subs.append(f"Sigils: {len(on)} charging, {len(idle)} unlocked but idle" + (f" ({', '.join(idle[:6])})" if idle else '') + (f", {len(lockd)} locked (next: {nm(lockd[0]['name'])} at {short(lockd[0].get('unlockCost'))})" if lockd else '') + ' (which to charge = gap, my read: the one feeding the goal)')
    subs.append(f"Prisma bubbles: {len([x for x in (a.get('prismaBubbles') or '').split(',') if x])}, fragments {a.get('prismaFragments')}")
    return ("Alchemy (liquids, vials, sigils): daily check", subs)


def c_research():
    r = G('research'); ob = r.get('observations') or []
    found = sum(1 for o in ob if o.get('found')); up = [nm(o['name']) for o in ob if o.get('canLevelUp')]
    subs = [f"observations found {found} / {len(ob)}; daily rolls left {r.get('dailyRollsLeft')}",
            f"magnifiers {r.get('magnifiersOwned')} ({r.get('magnifiersPerSlot')}/slot), monocles {r.get('opticalMonocleOwned')}, kaleidoscopes {r.get('kaleidoscopeOwned')}",
            f"grid points {r.get('gridPTSavailable')} open ({r.get('gridPTSpent')} / {r.get('gridPTSearned')} spent), next unlock at Research lv {r.get('nextUnlockResearchLv')}"]
    if up: subs.insert(0, 'level up now: ' + ', '.join(up))
    return (f"Research: {r.get('dailyRollsLeft')} observation rolls left today" + (' (use them)' if r.get('dailyRollsLeft') else ''), subs)


def c_worship():
    w = G('worship'); tot = sum(t.get('maxWave') or 0 for t in w)
    req = next((m['requirement'] for m in G('menagerie').get('missions') or [] if 'Worship' in str(m.get('description'))), None)
    subs = [f"{nm(t.get('name') or t.get('monsterName'))} ({nm(t.get('map'))}): best wave {t.get('maxWave')}" for t in sorted(w, key=lambda t: t.get('maxWave') or 0)[:3]]
    return (f"Worship totems: {tot} total best waves" + (f" -> {req:,} (Menagerie mission)" if req else '') + ", push the lowest first", subs)


def c_killroy():
    k = G('killroy'); up = [u for u in k.get('permanentUpgrades') or [] if u.get('cost') is not None]
    buy = [u for u in up if (u.get('cost') or 1e9) <= (k.get('skulls') or 0)]
    return (f"Killroy: {k.get('skulls')} skulls, {k.get('totalKills')} kills total, {k.get('rooms')} rooms" + (f"; can buy: {', '.join(nm(u['description'])[:50] + ' (' + str(u['cost']) + ')' for u in buy[:2])}" if buy else ''), [])


def c_refinery():
    r = G('refinery'); s = r.get('salts') or []
    low = sorted((x for x in s if x.get('unlocked')), key=lambda x: x.get('rank') or 0)
    subs = [f"{nm(x['saltName'])} rank {x['rank']}, auto-refine {x.get('autoRefinePercentage')}%" for x in low]
    return (f"Refinery: {r.get('totalLevels')} total ranks; lowest is {nm(low[0]['saltName'])} {low[0]['rank']} (my read: raise the lowest that a print or salt lick needs)" if low else 'Refinery: none unlocked', subs)


def c_saltlick():
    s = G('saltlick'); op = [x for x in s if x.get('unlocked') and (x.get('level') or 0) < (x.get('maxLevel') or 0)]
    return (f"Salt Lick: {len(s) - len(op)} / {len(s)} maxed" + ('' if op else ' (done)'), [f"{nm(x['desc'])[:60]}: {x['level']} -> {x['maxLevel']} ({nm(x['name'])} owned {short(x.get('totalAmount'))})" for x in op])


def c_death_note():
    dn = G('death_note'); subs = []
    for w, v in sorted(dn.items()):
        mobs = v.get('mobs') if isinstance(v, dict) else None
        if not mobs: continue
        lo = min(mobs, key=lambda m: m.get('kills') or 0)
        subs.append(f"{'World ' + str(int(w) + 1) if w.isdigit() else nm(w)}: lowest {nm(lo['displayName'])} {short(lo.get('kills'))} kills")
    return ("Death Note: lowest mob per world (Law 3: Zemo bursts small kills, Topher grinds the big ones)", subs)


def c_ballot():
    b = G('ballot'); a, m = b.get('selectedBonus') or {}, b.get('selectedMeritocracyBonus') or {}
    t = lambda x: nm(x.get('description') or x.get('0') or x.get('name'))
    return (f"Ballot: {t(a)} (x{b.get('voteMulti', 0):.2f}); Meritocracy: {t(m)} (x{b.get('meritocracyMult', 0):.2f}). Vote on reset day", [])


def c_gemshop():
    return ("Gem Shop: paid only, flag only: Dragonic Liquid Cauldron 1 -> 4 (Limited Specials), More Coral 5 -> 10. Nothing to do for free.", [])


def c_beanstalk():
    b = G('beanstalk'); n1 = sum(1 for x in b if (x or 0) >= 1); n2 = sum(1 for x in b if (x or 0) >= 2)
    return (f"Beanstalk: {n1} / {len(b)} golden foods deposited, {n2} upgraded" + (f": next deposit any of the {len(b) - n1} missing" if n1 < len(b) else ''), [])


def c_equinox():
    e = G('equinox'); act = [x for x in e.get('challenges') or [] if x.get('active')]
    return (f"Equinox: bar {short(e.get('currentCharge'))} / {short(e.get('chargeRequired'))} ({e.get('chargeRate')}/hr), {e.get('totalUpgradeLevels')} upgrade levels",
            [f"challenge: {nm(x['label'])} {x.get('current')} / {x.get('goal')}" for x in act])


def c_dungeons():
    v = G('dungeons')
    return (f"Dungeons: rank {v.get('rank')}, progress {short(v.get('progress'))} / {short(v.get('rankReq'))}, {short(v.get('credits'))} credits, {short(v.get('flurbos'))} flurbos (no planner: gap)", [])


def c_meals():
    m = G('meals'); cap = m['mealMaxLevel']; ms = m['meals']
    low = sorted((x for x in ms if (x.get('level') or 0) < cap), key=lambda x: x.get('level') or 0)
    return (f"Cooking: {len(ms) - len(low)} / {len(ms)} meals at cap {cap} (Lunarheim lore boss: +30 cap)",
            ['lowest: ' + ', '.join(f"{nm(x['name'])} {x.get('level')}" for x in low[:6])] if low else [])


def c_artifacts():
    a = G('sailing').get('artifacts') or []
    TIER = ['none', 'Base', 'Ancient', 'Eldritch', 'Sovereign', 'Omnipotent', 'Transcendent']
    cnt = {}
    for x in a: cnt[x.get('acquired') or 0] = cnt.get(x.get('acquired') or 0, 0) + 1
    zero = [nm(x['name']) for x in a if not x.get('acquired')]
    subs = ['tiers: ' + ', '.join(f"{TIER[k] if k < len(TIER) else k} {v}" for k, v in sorted(cnt.items()))]
    if zero: subs.append(f"not found ({len(zero)}): " + ', '.join(zero[:10]) + ' (find levers: Maw = Research grid node, Vault Artifact Find, Arcade, Teal Summoning, Glowing Veil, Noble Sluggo)')
    return (f"Artifacts: {len(a) - len(zero)} / {len(a)} found", subs)


def c_breeding():
    b = G('breeding'); pets = [p for w in b.get('pets') or [] for p in (w if isinstance(w, list) else [])]
    if not pets: return None
    lv = lambda p: p.get('breedingLevel') or 0
    h7 = sum(1 for p in pets if lv(p) >= 7)
    near = sorted((p for p in pets if lv(p) < 7), key=lambda p: -lv(p))[:3]
    return (f"Breedability: {h7} / {len(pets)} pets at heart 7 (side goal: one shiny slot breeds one pet at a time)",
            ['focus next: ' + ', '.join(f"{nm(p.get('name') or p.get('monsterName') or '?')} heart {lv(p)}" for p in near)] if near else [])


def c_skulls():
    miss = []
    for n in sorted({o for v in IDX.values() for o in (v.get('owners') or []) if str(o).startswith('Autis')}):
        try: tl = D.char(n).get('tools') or []
        except Exception: continue
        if not any('SKULL' in str(t.get('Type', '')).upper() or 'skull' in str(t.get('displayName', '')).lower() for t in tl if isinstance(t, dict)):
            miss.append(n)
    return (f"Worship skulls: {'every character has one' if not miss else 'missing on ' + ', '.join(miss)}", [])


def c_stamps():
    st = G('stamps'); subs = []
    for grp in ('combat', 'skills', 'misc'):
        xs = st.get(grp) or []
        lo = sorted((x for x in xs if (x.get('level') or 0) > 0), key=lambda x: x.get('level') or 0)[:3]
        locked = sum(1 for x in xs if not x.get('level'))
        subs.append(f"{grp.title()}: {len(xs) - locked} / {len(xs)} owned; lowest " + ', '.join(f"{nm(x.get('name') or x.get('displayName'))} {x.get('level')}" for x in lo))
    return ("Stamps by group (Combat / Skills / Misc)", subs)


CHECKS = {'caverns': c_caverns, 'slab': c_slab, 'achievements': c_achievements, 'lab_mainframe': c_lab,
          'cape_vine': c_cape, 'gallery': c_gallery, 'menagerie': c_menagerie, 'alchemy_cauldrons': c_alchemy,
          'research': c_research, 'worship': c_worship, 'killroy': c_killroy, 'refinery': c_refinery,
          'saltlick': c_saltlick, 'death_note': c_death_note, 'ballot': c_ballot,
          'gemshop': c_gemshop, 'beanstalk': c_beanstalk, 'equinox': c_equinox, 'dungeons': c_dungeons,
          'meals': c_meals, 'sailing': c_artifacts, 'breeding': c_breeding, 'worship_skulls': c_skulls, 'stamps': c_stamps}
ALIAS = {'meritocracy': 'ballot', 'lab_chips': 'lab_mainframe', 'lab_jewels': 'lab_mainframe', 'lab_bonuses': 'lab_mainframe'}


def owners(sysname):
    return (OVERRIDE.get(sysname) or []) or [o for o in (IDX.get(sysname) or {}).get('owners') or [] if o.startswith('Autis')]


def ledger_lines(name):
    try: L = json.load(open(ROOT / 'model' / 'ledger.json'))
    except Exception: return []
    out = []
    for w in L.get('watch') or []:
        if w.get('owner') != name: continue
        bits = [f"{w['item']}: {short(w.get('owned'))}"]
        if w.get('target'): bits.append(f"/ {short(w['target'])}, short {short(w.get('shortage'))}")
        if w.get('runout_days'): bits.append(f"RUNS OUT in {w['runout_days']:.1f} d")
        elif w.get('eta_days'): bits.append(f"ETA {w['eta_days']:.1f} d")
        out.append(' '.join(bits) + f" ({w.get('why')})")
    return out


def lines(name, only=None):
    """[(system, line, subs)] for every checked system this character owns (dedup by checker)."""
    out, done = [], set()
    for s in list(CHECKS) + list(ALIAS):
        fn_key = ALIAS.get(s, s)
        if fn_key in done or name not in owners(s): continue
        if only and s not in only and fn_key not in only: continue
        done.add(fn_key)
        try:
            r = CHECKS[fn_key]()
            if r: out.append((fn_key, r[0], r[1]))
        except Exception as e:
            out.append((fn_key, f"{fn_key.replace('_', ' ').title()}: check failed ({type(e).__name__}: {str(e)[:60]}), fix in model/syscheck.py", []))
    try:
        import syscheck2 as _S2   # part 2 checks (pending_changes Left to build, 2026-11-28)
        for k, l, subs in _S2.lines(name):
            if only and k not in only: continue
            out.append((k, l, subs))
    except Exception as e:
        out.append(('syscheck2', f"syscheck2 failed ({type(e).__name__}: {str(e)[:60]}), fix in model/syscheck2.py", []))
    lg = ledger_lines(name)
    if lg: out.append(('materials', 'Materials to watch (ledger): ' + lg[0], lg[1:]))
    return out


if __name__ == '__main__':
    NICK = {'zemo': 'Autiszemo', 'cat': 'Autistocat', 'ticles': 'Autisticles', 'tastic': 'Autistastic', 'bish': 'Autistabish', 'tacular': 'Autistacular',
            'totle': 'Autistotle', 'matic': 'Autistomatic', 'naut': 'Autistronaut', 'topher': 'Autistopher', 'tachio': 'Autistachio'}
    who = [NICK.get(a.lower(), a) for a in sys.argv[1:]] or list(NICK.values())
    print(f"save {D.stamp if hasattr(D, 'stamp') else ''}, {D.age_hours:.1f} h old")
    for n in who:
        print(f"## {n}")
        for s, l, subs in lines(n):
            print('- ' + l); [print('   ' + x) for x in subs]
