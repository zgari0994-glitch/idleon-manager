#!/usr/bin/env python3
"""One-shot lookup (v2, Zack 2026-11-26): ONE call per system answers a normal question.
Usage:  tools/lookup.py <system> [terms...]           e.g. lookup.py tesseract arcanist
        tools/lookup.py --terms "super talent reset"   (free search, no system)
        tools/lookup.py <system> --path account.tesseract.upgrades   (drill into raw data)
        tools/lookup.py <system> --full                (no row caps; only if the compact view truncated)
Output (~4K tokens max, every cut is flagged TRUNCATED):
  0. header   save stamp + age, owners
  1. DATA     scalars + every upgrade-like list: Lv cur/max, next cost vs balance, LOCKED + exact unlock condition,
              creator tier grade matched to the item name
  2. AUTOREVIEW items (cur -> goal)
  3. CREATORS ranked Griffy > Pulse = Nocturne > others, newest first, tier grade [S]/[A].. parsed from tier lists
  4. FINDINGS files that mention it
  5. COVERAGE creators + data coverage + what was cut
Every call is logged to state/lookups.log.
"""
import csv, glob, gzip, json, re, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'model'))
from data import load, DataMissing, MAP  # noqa: E402
import phase_d as PD   # Phase C step D views
import yaml  # noqa: E402

IDX = yaml.safe_load(open(ROOT / 'model' / 'system_index.yaml'))
RANK = {'griffybit': 0, 'pulseidle': 1, 'nocturne': 1}
SHORT = {'griffybit': 'Griffy', 'pulseidle': 'Pulse', 'nocturne': 'Nocturne', 'will309': 'Will'}
BUDGET = 14000          # chars ~= 4K tokens
args = sys.argv[1:]
FULL = '--full' in args
if FULL:
    args.remove('--full')
path = None
if '--path' in args:
    i = args.index('--path'); path = args[i + 1]; del args[i:i + 2]
if args and args[0] == '--terms':
    system, terms = None, args[1].lower().split()
else:
    system = args[0] if args else None
    terms = [t.lower() for t in args[1:]]
if system and system not in MAP:
    near = [s for s in MAP if system.lower() in s or s in system.lower()]
    if len(near) == 1:
        system = near[0]
    else:
        print(f"unknown system '{system}'. Close: {near or sorted(MAP)[:40]}"); sys.exit(2)

D = load(); PD._D = D   # share the loaded save with phase_d
cut = []                 # what got truncated
ROWS = 999 if FULL else 14


def fmt(v):
    if isinstance(v, bool) or v is None:
        return str(v)
    if isinstance(v, (int, float)):
        a = abs(v)
        if a >= 1e15:
            return f"{v:.2e}"
        for div, s in ((1e12, 'T'), (1e9, 'B'), (1e6, 'M'), (1e3, 'K')):
            if a >= div:
                return f"{v / div:.3g}{s}"
        return f"{v:.3g}" if isinstance(v, float) else str(v)
    s = str(v).replace('_', ' ')
    return s if len(s) < 70 else s[:67] + '...'


def nm(d):  # 2026-11-27: arcade shop has no name (use effect), menagerie boosts use description
    n = d.get('name') or d.get('rawName') or d.get('effect') or d.get('description') or d.get('index', '?')
    return re.sub(r'\s+', ' ', str(n).replace('_', ' ').replace('{', '#').replace('}', '#')).strip()


PLACEHOLDER = lambda d: isinstance(d, dict) and d.get('name') == 'Name' and d.get('description') == 'desc'   # empty research grid cells


# ---------- research level (gates Jelly upgrades) ----------
def research_level():
    r = D.account.get('research') or {}
    for k in ('researchLevel', 'researchLv', 'level', 'lv', 'totalLevel'):
        if isinstance(r.get(k), (int, float)):
            return r[k]
    best = 0
    for c in D.characters:
        sk = c.get('skillsInfo') or c.get('skills') or {}
        v = sk.get('research') if isinstance(sk, dict) else None
        if isinstance(v, dict):
            v = v.get('level')
        if isinstance(v, (int, float)):
            best = max(best, v)
    return best or None


# ---------- per-system specs: balance, max field, lock condition ----------
def _tess_cond(d):
    return f"{d['x6']} total Tesseract LVs (have {D.account['tesseract'].get('totalUpgradeLevels')})" if d.get('x6') else None


def _jelly_cond(d):
    rl = research_level()
    if 'lvReq' not in d and 'expReq' in d:          # a cell: unlocked by its "<Name> Cell Cultivation" upgrade
        up = next((u for u in D.account['jellyOperator']['upgrades'] if u.get('name', '').startswith(f"{d.get('name')} Cell")), None)
        if up:
            return f"upgrade '{up['name']}' (" + (f"Research LV {up['lvReq']}, have {rl}" if up.get('lvReq') else 'see upgrades') + ")"
    return f"Research LV {d['lvReq']}" + (f" (have {rl})" if rl is not None else ' (your Research LV not in parser)') if d.get('lvReq') else None


SPEC = {
    'jelly_operator': {'bal': lambda: (D.account['jellyOperator'].get('bloodcells'), 'Bloodcells'), 'cond': _jelly_cond},
    'spelunk': {'bal': lambda: (D.account['spelunking'].get('currentAmber'), 'Amber')},
    'tesseract': {'max': 'x4', 'cond': _tess_cond, 'note': 'cost currency per upgrade (tachyon color) not in parser; balances in header'},
    'compass': {'max': 'x4', 'skip': {'maps', 'medallions', 'upgrades'}, 'note': 'dust balances + dust type per upgrade first (phase_d)'},
}
def _rng(xs):
    xs = [x for x in xs if isinstance(x, (int, float))]
    return f"{fmt(min(xs))}-{fmt(max(xs))}" if xs else '-'


def _sailing_extra():
    s = D.account['sailing']
    b, c, a = s.get('boats') or [], s.get('captains') or [], s.get('artifacts') or []
    out = [f"  boats {len(b)}: Lv {_rng([x.get('level') for x in b])}, loot Lv {_rng([x.get('lootLevel') for x in b])}, speed Lv {_rng([x.get('speedLevel') for x in b])}"]
    if b:
        lo = sorted(b, key=lambda x: x.get('lootLevel') or 0)[:3]
        out.append('    lowest loot Lv: ' + ', '.join(f"boat {x.get('boatIndex')} L{x.get('lootLevel')} (Lv {x.get('level')}, isl {fmt((x.get('island') or {}).get('name'))})" for x in lo))
    out.append(f"  captains {len(c)}: Lv {_rng([x.get('level') for x in c])}")
    tiers = {}
    for x in a:
        tiers[x.get('acquired', 0)] = tiers.get(x.get('acquired', 0), 0) + 1
    out.append('  artifacts by tier (Toolbox index, 0 = not found): ' + ', '.join(f"t{k}:{v}" for k, v in sorted(tiers.items())))
    miss = [nm(x) for x in a if not x.get('acquired')]
    if miss:
        out.append('    not found: ' + ', '.join(miss[:12]) + (f" +{len(miss) - 12}" if len(miss) > 12 else ''))
    return out


def _compass_extra():
    out = []
    for g in D.account['compass'].get('groupedUpgrades') or []:
        out += render_levels(f"{g.get('path')} path", g.get('list') or [], SPEC['compass'])
    return out


SPEC['compass']['extra'] = _compass_extra
SPEC['compass']['skip'] = {'maps', 'medallions', 'upgrades', 'groupedUpgrades', 'abominations'}
SPEC['sailing'] ={'extra': _sailing_extra, 'skip': {'artifacts', 'boats', 'captains'}}


def _lab_extra(kind):  # Zack 2026-11-27: each lab system gets its own view, not the same generic dump
    def f():
        L, out = D.account['lab'], []
        cl = lambda s: str(s).replace('_', ' ')
        req = lambda r: ', '.join(f"{fmt(x['amount'])} {cl(x['name'])}" for x in r)
        if kind == 'chips':
            ch = L['chips']
            miss = [c for c in ch if not c['amount']]
            out.append(f"chips: {len(ch) - len(miss)}/{len(ch)} types owned; raw chips {L.get('totalRawChips')}")
            for c in ch:
                out.append(f"  {cl(c['name'])}: own {c['amount']}" + (f" / {c['totalAmount']}" if (c.get('totalAmount') or 0) > 0 else '') + (f" | MISSING, cost: {req(c['requirements'])}" if not c['amount'] else ''))
            rot = [cl(ch[int(i)]['name']) if int(i) < len(ch) else i for i in L.get('currentRotation') or []]
            out.append(f"repo rotation now (index -> name is my read, verify in game): {rot}")
        elif kind == 'jewels':
            js = L['jewels']
            out.append(f"jewels: {sum(1 for j in js if j['acquired'])}/{len(js)} acquired")
            for j in js:
                if not j['acquired']:
                    out.append(f"  MISSING {cl(j['name'])}: {cl(j.get('description', ''))[:70]} | cost: {req(j['requirements'])}")
        elif kind == 'bonuses':
            bs = L['labBonuses']
            out.append(f"lab bonuses: {sum(1 for b in bs if b.get('active'))}/{len(bs)} on")
            out.append('  ON: ' + ', '.join(cl(b['name']) for b in bs if b.get('active')))
            out.append('  OFF: ' + ', '.join(cl(b['name']) for b in bs if not b.get('active')) + '  (parser does not say range vs locked)')
        else:
            con = {p['name'] for p in L['connectedPlayers']}
            out.append(f"mainframe: {len(con)}/{len(L['playersCords'])} players connected")
            for p in L['playersCords']:
                out.append(f"  {p['playerName']} ({cl(p.get('class'))}): {'CONNECTED' if p['playerName'] in con else 'not connected'}, line width {fmt(p.get('lineWidth'))}")
        return out
    return f


_LAB_KEYS = {'chips', 'jewels', 'labBonuses', 'playersChips', 'playersCords', 'connectedPlayers', 'currentRotation'}
for _k, _kind in [('lab_chips', 'chips'), ('lab_jewels', 'jewels'), ('lab_bonuses', 'bonuses'), ('lab_mainframe', 'mainframe')]:
    SPEC[_k] = {'extra': _lab_extra(_kind), 'skip': _LAB_KEYS}
def _ach_extra():
    A = D.account['achievements']
    real = [a for a in A if a.get('name') and not str(a.get('name')).startswith('FILLERZZZ')]
    done = [a for a in real if a.get('completed')]
    out = [f"achievements: {len(done)}/{len(real)} done ({len(real) - len(done)} left, {sum(a.get('gems') or 0 for a in real if not a.get('completed'))} gems left)"]
    return out


def _rg_bal(d):
    i = d.get('costResourceIndex')
    st = D.account['royalGuardian'].get('resourceStorage') or []
    return (st[i], f"resource #{i}") if isinstance(i, int) and 0 <= i < len(st) else (None, None)


def _rg_cond(d):
    A = D.account['royalGuardian']['armory']
    need = d.get('shelfUnlockTotalLevels') or d.get('unlockTotalLevels')
    return f"{fmt(need)} total armory levels (have {A['totalLevels']})" if need else None


def _legend_extra():
    L = D.account['legendTalents']
    own, sp = L['pointsOwned']['value'] if isinstance(L['pointsOwned'], dict) else L['pointsOwned'], L['pointsSpent']
    if sp > own:
        return [f"LEGEND POINTS DON'T ADD UP: spent {sp} > owned {own} (Toolbox misses at least {sp - own} owned points from a source it doesn't read). Unspent = check in game."]
    return []


SPEC['legend_talents'] = {'extra': _legend_extra}
SPEC['achievements'] = {'extra': _ach_extra, 'skip': {'achievements'}}
SPEC['royal_armory'] = {'rowbal': _rg_bal, 'cond': _rg_cond}


# ---------- Phase C step C (Zack 2026-11-28): 8 systems + trophies + shrines fix ----------
def _names():
    return [c.get('name') for c in D.characters]


def _anvil_extra():
    import anvil as AV
    out = [f"  {n}: {AV.line(n, D).replace('Anvil (daily): ', '')}" for n in _names()]
    return out + ['  ' + AV.bars_line(D)]


def _shrines_extra():
    import json as _j
    mn = _j.load(open(ROOT / 'brain' / 'tb_static.json'))['map_names']
    out = []
    for s in sorted(D.account['shrines'], key=lambda x: -(x.get('shrineLevel') or 0)):
        m = s.get('mapId'); mp = mn[m] if isinstance(m, int) and 0 <= m < len(mn) and mn[m] else f'map {m}'
        out.append(f"  {nm(s)} Lv {s.get('shrineLevel')} | bonus {fmt(s.get('bonus'))}% | {'placed on ' + mp if s.get('placed') else 'NOT PLACED'}"
                   + (' | world tour' if s.get('worldTour') else '') + f" | {fmt(s.get('desc'))}")
    eb = D.account.get('shrinesExpBonus')
    if eb not in (None, {}, []):
        out.append(f"  shrine exp bonus: {fmt(eb.get('total') if isinstance(eb, dict) else eb)}")
    return out


def _st_extra():
    out = []
    for c in D.characters:
        i = c.get('superTalentsInfo') or {}
        out.append(f"  {c['name']}: {len(i.get('talents') or [])} super talents set, bonus {fmt(i.get('bonus'))}%, {c.get('superTalentLeftToSpend')} left to spend"
                   + (f" | {', '.join(PD.talent_name(t.get('talentIndex')) for t in i.get('talents') or [])}" if i.get('talents') else ''))
    return out + ['  names: brain/talent_names.json (Toolbox talents.json skillIndex), presetIndex shown in --path']


def _poppy_extra():
    k = D.account['kangaroo']
    out = [f"  fish {fmt(k.get('fish'))}, total {fmt(k.get('totalFish'))}, tar fish {fmt(k.get('tarFishOwned'))}, unspent reset points {fmt(k.get('unspentResetPoints'))}, next reset at {fmt(k.get('nextResetPoints'))}"]
    out += ['  bonuses: ' + ', '.join(f"{nm(b)} {fmt(b.get('bonus'))}" for b in (k.get('bonuses') or [])[:8])]
    for key in ('upgrades', 'tarUpgrades', 'resetBonuses'):
        if isinstance(k.get(key), list) and is_levelled(k[key]):
            out += render_levels(key, k[key], {})
    return out + ['  note: Poppy = Toolbox key "kangaroo" (my read of the mapping)']


def _snail_extra():
    g = D.account['gaming']; s = g.get('snail') or {}
    return [f"  snail Lv {g.get('snailLevel')}/{s.get('maxLevel')}, encouragement {g.get('snailEncouragement')}, success {fmt((s.get('successChance') or 0) * 100)}%, reset {fmt((s.get('resetChance') or 0) * 100)}%, hole bonus {fmt(s.get('holeBonus'))}",
            '  note: snail_mail = Gaming snail (no mail key in the save; my read)']


def _wb_extra():
    out = []
    try:
        W = yaml.safe_load(open(ROOT / 'brain' / 'weekly_boss.yaml'))
        for wk, x in sorted((W.get('weeks') or {}).items()):
            out.append(f"  week {wk}: {x.get('boss')} ({x.get('start')} -> {x.get('end')}) | 5 skulls {x.get('skulls5')} | trophy {x.get('trophy')}")
        out.append(f"  source: {W.get('source')} fetched {W.get('fetched')} (fan src)")
    except Exception as e:
        out.append(f"  brain/weekly_boss.yaml not read: {e}")
    return out + PD.weekly_raw_lines()


def _worldboss_raw():
    r = json.load(gzip.open(ROOT / 'snapshots' / D.stamp / 'raw.json.gz')); d = r.get('data', r)
    bi = d.get('BossInfo')
    if not bi:
        return ['  BossInfo not in raw save']
    rows = [[x.get(str(i)) for i in range(x.get('length', 3))] if isinstance(x, dict) else x for x in bi]
    return [f"  BossInfo: {len(rows)} rows [flag, hp, ?] raw, NOT decoded (step D):"] + [f"    {i}: {r_}" for i, r_ in enumerate(rows[:12])]


def _trophy_extra():
    import trophies as TR
    return ['  ' + x for x in TR.gallery_lines(D)] + ['  have: ' + ', '.join(t['name'] for t in TR.status(D) if t['have'])]


SPEC['anvil'] = {'extra': _anvil_extra, 'norender': True}
SPEC['shrines'] = {'extra': _shrines_extra, 'norender': True}
SPEC['super_talents'] = {'extra': _st_extra, 'norender': True}
SPEC['poppy'] = {'extra': _poppy_extra, 'norender': True}
SPEC['snail_mail'] = {'extra': _snail_extra, 'norender': True}
SPEC['weekly_boss'] = {'extra': _wb_extra, 'norender': True}
SPEC['world_bosses'] = {'raw': PD.world_bosses}


# ---------- Phase C step D (2026-11-28): extra views from model/phase_d.py ----------
def _add_extra(key, fn, first=False):
    sp = SPEC.setdefault(key, {}); old = sp.get('extra')
    sp['extra'] = (lambda: fn() + (old() if old else [])) if first else (lambda: (old() if old else []) + fn())


def _trash_view():
    f, t, lines, plan = PD.trash_list()
    return [f"  Trash shop buy list ({plan['source']}), fires when Fractal opens (now {'OPEN' if f.get('unlocked') else 'locked'}), trash {PD.short(t.get('trash'))}:"] + ['    ' + x for x in lines]


_add_extra('refinery', PD.salt_lines, first=True)
_add_extra('obols', PD.obol_lines)
_add_extra('guild_bonuses', PD.guild_lines)
_add_extra('compass', PD.compass_dust_lines, first=True)
_add_extra('spelunk', PD.lore_lines, first=True)
_add_extra('advice_fish', lambda: PD.FISH_NOTE)
_add_extra('islands', _trash_view)
SPEC['trophies'] = {'extra': _trophy_extra, 'norender': True}
SPEC['bubba'] = {'skip': set()}
def _palette_extra():
    P = [x for x in D.account['gaming'].get('palette') or [] if isinstance(x, dict)]
    on = [x for x in P if (x.get('level') or 0) > 0]
    out = [f"  palette: {len(on)}/{len(P)} colours levelled, final bonus {fmt(D.account['gaming'].get('paletteFinalBonus'))}, luck {fmt(D.account['gaming'].get('paletteLuck'))}"]
    for x in sorted(on, key=lambda x: -(x.get('level') or 0))[:ROWS]:
        out.append(f"    {nm(x)} Lv {x.get('level')} | bonus {fmt(x.get('bonus'))} | {fmt(x.get('description'))}" + (f" | black stars {x.get('blackStars')}" if x.get('blackStars') else ''))
    if len(on) > ROWS:
        cut.append(f"palette: {len(on) - ROWS} levelled colours"); out.append(f"    ... TRUNCATED {len(on) - ROWS} more")
    out.append('  not levelled: ' + ', '.join(nm(x) for x in P if not x.get('level'))[:240])
    return out


SPEC['palette'] = {'extra': _palette_extra, 'norender': True}
GORD = {g: i for i, g in enumerate(['S+', 'S', 'S-', 'A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F'])}
SKIP_KEYS = re.compile(r'^(x\d+|description|.*Description|sprite.*|Monster.*|imageName|xyPointer|save|layout|raw.*|rawDancingCoral|mapBonusRaw|expression|tree)$')

# ---------- creator claims (needed early: tier grades annotate data rows) ----------
GRADE = re.compile(r'\b([SABCDF][+-]?)[ -]tier\b|\btier[ -]([SABCDF][+-]?)\b|\b([SABCDF][+-]?)[ -]rank(?:ed)?\b')


def grade(st):
    m = GRADE.search(st)
    return next((g for g in m.groups() if g), None) if m else None


_tr = IDX.get(system, {}).get('transcripts') if system else None
slug = (_tr.get('slug') if isinstance(_tr, dict) else None) or system
tg = (MAP.get(system, {}).get('tags') or [slug]) if system else []
kw = (MAP.get(system, {}).get('kw') or []) if system else []
claims = []
for f in glob.glob(str(ROOT / 'sources/creators/*/tags/*.csv')):
    for r in csv.DictReader(open(f)):
        st = r.get('statement', '').lower()
        hit_sys = system and ((r.get('system') in tg) or (kw and any(k in st for k in kw)))
        hit_terms = terms and all(t in st for t in terms)
        if (hit_sys and (not terms or any(t in st for t in terms))) or hit_terms:
            claims.append(r)
seen, uniq = set(), []
for r in sorted(claims, key=lambda r: (RANK.get(r['creator'], 2), r.get('date') == 'nodate', [-ord(c) for c in r.get('date', '')])):
    k = (r['creator'], r['statement'])
    if k not in seen:
        seen.add(k); r['grade'] = grade(r['statement']); uniq.append(r)
USEFUL_T = ('priority', 'how_to', 'setup', 'skip', 'warning', 'target', 'comparison', 'meta_change', 'opinion', 'mechanic', 'blocker', 'threshold')
useful = [r for r in uniq if r.get('claim_type') in USEFUL_T or r['grade']]
graded = [r for r in useful if r['grade']]


def item_grade(name):
    n = name.lower()
    if len(n) < 5:
        return ''
    for r in graded:                       # already ranked creator > newest
        if n in r['statement'].lower():
            return f" [{SHORT.get(r['creator'], r['creator'][:6])} {r['grade']} {r['date'][:7]}]"
    return ''


# ---------- DATA renderer ----------
def is_levelled(lst):
    return lst and isinstance(lst[0], dict) and 'level' in lst[0] and ('cost' in lst[0] or 'maxLevel' in lst[0] or 'unlocked' in lst[0] or 'bonus' in lst[0])


def flat(lst):
    if lst and isinstance(lst[0], list) and lst[0] and isinstance(lst[0][0], dict):
        return [x for sub in lst for x in sub]
    return lst


def render_levels(key, lst, spec):
    bal, cur = (spec['bal']() if spec.get('bal') else (None, None))
    mxk = spec.get('max')
    rows, maxed, locked = [], 0, []
    if not all(isinstance(d, dict) for d in lst):
        return [f'{key}: {len(lst)} items (non-dict list)']
    empty = sum(1 for d in lst if PLACEHOLDER(d))
    lst = [d for d in lst if not PLACEHOLDER(d)]
    for d in lst:
        mx = d.get('maxLevel') if d.get('maxLevel') is not None else (d.get(mxk) if mxk else None)
        if isinstance(mx, str):  # parser uses 'Infinity' for uncapped rows (sushi, gaming)
            try: mx = float(mx)
            except ValueError: mx = None
        if isinstance(mx, (int, float)) and (mx >= 99999 or mx != mx):
            mx = None
        lv = d.get('level') or 0
        is_locked = d.get('unlocked') is False
        cond = (spec.get('cond') or (lambda _: None))(d) or d.get('requirement') or d.get('unlockReq')
        if spec.get('rowbal'):
            bal, cur = spec['rowbal'](d)
        if is_locked:
            locked.append(f"    LOCKED {nm(d)} -> needs {cond or 'unlock condition not in parser'}" + (f", cost {fmt(d['cost'])}" if d.get('cost') else '') + item_grade(nm(d)))
            continue
        if mx is not None and lv >= mx:
            maxed += 1; continue
        cost = d.get('cost')
        c = ''
        if isinstance(cost, (int, float)) and cost > 0:
            c = f" | next {fmt(cost)}"
            if isinstance(bal, (int, float)):
                c += ' OK' if bal >= cost else f" SHORT {fmt(cost - bal)}"
        b = d.get('bonus')
        ig = item_grade(nm(d))
        g = GORD.get(ig.split()[1], 50) if ig else 50
        rows.append(((g, cost if isinstance(cost, (int, float)) else 9e99),
                     f"    {nm(d)} Lv {fmt(lv)}/{fmt(mx) if mx is not None else '-'}" + (f" (bonus {fmt(b)})" if b not in (None, '', 0) else '') + c + ig))
    rows.sort(key=lambda x: x[0])          # creator tier grade first, then cheapest
    head = f"  {key}: {len(lst)} total, {maxed} maxed, {len(rows)} open, {len(locked)} locked" + (f" | balance {fmt(bal)} {cur}" if bal is not None and not spec.get('rowbal') else '') + (f" ({empty} empty grid cells hidden)" if empty else '')
    out = [head] + [r for _, r in rows[:ROWS]]
    if len(rows) > ROWS:
        cut.append(f"{key}: {len(rows) - ROWS} open rows (cheapest shown; --full for all)"); out.append(f"    ... TRUNCATED {len(rows) - ROWS} more open (cheapest first)")
    out += locked[:ROWS]
    if len(locked) > ROWS:
        cut.append(f"{key}: {len(locked) - ROWS} locked rows"); out.append(f"    ... TRUNCATED {len(locked) - ROWS} more locked")
    return out


def render(v, key, spec, depth, out):
    if depth > 3:
        return
    pad = '  ' * depth
    if isinstance(v, dict):
        if 'statName' in v and 'totalValue' in v:
            out.append(f"{pad}{key}: {v['statName']} = {v['totalValue']}"); return
        if set(v) >= {'value', 'breakdown'} and not isinstance(v['value'], (dict, list)):
            out.append(f"{pad}{key}: {fmt(v['value'])}"); return
        if len(v) > 8 and all(isinstance(x, bool) for x in v.values()):
            out.append(f"{pad}{key}: {len(v)} flags, {sum(v.values())} True"); return
        sc = [(k, x) for k, x in v.items() if not isinstance(x, (dict, list)) and not SKIP_KEYS.match(str(k))]
        nest = [(k, x) for k, x in v.items() if isinstance(x, (dict, list)) and not SKIP_KEYS.match(str(k))]
        if key:
            out.append(f"{pad}{key}:")
        if sc:
            line = ', '.join(f"{k}={fmt(x)}" for k, x in sc[:24])
            out.append(f"{pad}  {line}" + (f" ... +{len(sc) - 24}" if len(sc) > 24 else ''))
        for k, x in nest:
            if k in spec.get('skip', set()) and depth == 0:
                if isinstance(x, list):
                    out.append(f"{pad}  {k}: {summ(x)}")
                continue
            render(x, k, spec, depth + 1, out)
        return
    if isinstance(v, list):
        lst = flat(v)
        if is_levelled(lst):
            out += [pad + ln for ln in render_levels(key, lst, spec)]
        elif lst and isinstance(lst[0], dict):
            if all(set(d) <= {'name', 'value'} for d in lst[:5]):
                out.append(f"{pad}{key}: " + ', '.join(f"{fmt(d.get('name'))} {fmt(d.get('value'))}" for d in lst[:12]))
            else:
                out.append(f"{pad}{key}: {summ(lst)}")
        elif lst:
            out.append(f"{pad}{key}: {[fmt(x) for x in lst[:15]]}" + (f" ...({len(lst)})" if len(lst) > 15 else ''))


def summ(lst):
    lst = flat(lst)
    s = f"{len(lst)} items"
    if lst and isinstance(lst[0], dict):
        for b in ('unlocked', 'acquired', 'defeated', 'owned', 'isInUse'):
            n = sum(1 for d in lst if isinstance(d, dict) and d.get(b) not in (None, False, 0))
            if any(b in d for d in lst[:3] if isinstance(d, dict)):
                s += f", {b} {n}"
    return s


out = []
age = f"{D.age_hours:.1f}h old" if D.age_hours else 'age unknown'
own = ', '.join(MAP.get(system, {}).get('owners') or []) if system else ''
out.append(f"# lookup {system or ''} {' '.join(terms)} | save {D.stamp} ({age}) | owner {own or '-'}")
data_lines = ['\n## 1. DATA (Toolbox parser)']
spec = SPEC.get(system, {})
try:
    if path:
        # Accept full paths (account.alchemy.x), system-relative (cauldrons.x) or bare (alchemy.x).
        base = (MAP.get(system, {}).get('path') or '') if system else ''
        cands = [path, f'account.{path}']
        if base and not base.startswith('@'):
            cands += [f'{base}.{path}', f'account.{base}.{path}']
        hit = None
        for c in dict.fromkeys(cands):
            try:
                hit = (c, D.get(c, allow_empty=True)); break
            except DataMissing:
                continue
        if hit is None:
            raise DataMissing(f"{path}: not found (tried {', '.join(dict.fromkeys(cands))}) ({D.stamp})")
        if hit[0] != path:
            data_lines.append(f"path resolved: {hit[0]}")
        render(hit[1], hit[0], spec, 0, data_lines)
    elif system:
        v = D.system(system, allow_empty=True)
        data_lines.append(f"path: {MAP[system].get('path')}" + (f" | note: {spec['note']}" if spec.get('note') else ''))
        if spec.get('extra'):
            data_lines += spec['extra']()
        if not spec.get('norender'):
            render(v, '', spec, 0, data_lines)
except DataMissing as e:
    if spec.get('raw') and not path:      # not in Toolbox's parser: read the raw save and say so
        data_lines.append(f"not in Toolbox's parser, raw save read: {e}")
        data_lines += spec['raw']()
    else:
        data_lines.append(f"DATA MISSING: {e}")
DATA_CAP = 8000 if not FULL else 10 ** 9
txt, kept = 0, []
for ln in data_lines:
    if len(ln) > 260:
        ln = ln[:257] + '...'
    if txt + len(ln) > DATA_CAP:
        cut.append(f"DATA section: {len(data_lines) - len(kept)} lines past {DATA_CAP} chars (use --path to drill in)")
        kept.append('  ... TRUNCATED (data cap) - drill in with --path'); break
    kept.append(ln); txt += len(ln) + 1
out += kept

# ---------- 2. AUTOREVIEW ----------
labels = []
if system:
    names = [n.lower() for n in IDX.get(system, {}).get('autoreview', [])]
    rv = json.load(gzip.open(ROOT / 'snapshots' / D.stamp / 'review.json.gz'))

    def walk(o, sec=''):
        if isinstance(o, dict):
            n = str(o.get('name') or '')
            sec2 = n if n.lower() in names else sec
            done = str(o.get('goal')) in ('✔', 'True') or (o.get('goal') not in (None, '') and str(o.get('cur')) == str(o.get('goal')))
            if sec2 and o.get('label') and not done:
                labels.append(f"  [{sec2}] {o['label'][:100]}" + (f" ({o.get('cur')} -> {o.get('goal')})" if o.get('goal') not in (None, '') else ''))
            for x in o.values():
                walk(x, sec2)
        elif isinstance(o, list):
            for x in o:
                walk(x, sec)
    walk(rv)
AR_N = 999 if FULL else 12
out.append(f"\n## 2. AUTOREVIEW ({len(labels)} items)")
out += labels[:AR_N]
if len(labels) > AR_N:
    cut.append(f"AutoReview: {len(labels) - AR_N} items"); out.append(f"  ... TRUNCATED {len(labels) - AR_N} more")

# ---------- 3. CREATORS ----------
CR_N = 999 if FULL else 16
G_N = 999 if FULL else 10
out.append(f"\n## 3. CREATORS ({len(useful)} claims, {len(graded)} tier-graded; Griffy > Pulse = Nocturne > others, newest first)")


def cl(r):
    old = ' OLD' if r.get('date', '') < '2024-06' else ''
    g = f"[{r['grade']}] " if r['grade'] else ''
    fan = '' if r['creator'] in RANK else ' (fan src)'
    return f"  {SHORT.get(r['creator'], r['creator'][:7])}{fan} {r.get('date')}{old} {r.get('claim_type')}: {g}{r['statement'][:150]} [{r['video_id']} {r.get('t_start')}]"


if graded:
    out.append('  TIER GRADES:')
    out += [cl(r) for r in graded[:G_N]]
    if len(graded) > G_N:
        cut.append(f"tier grades: {len(graded) - G_N}"); out.append(f"  ... TRUNCATED {len(graded) - G_N} more graded")
rest = [r for r in useful if not r['grade']]
out.append('  CLAIMS:')
out += [cl(r) for r in rest[:CR_N]]
if len(rest) > CR_N:
    cut.append(f"claims: {len(rest) - CR_N} (add terms to narrow)"); out.append(f"  ... TRUNCATED {len(rest) - CR_N} more (add terms to narrow)")

# ---------- 4. FINDINGS ----------
keys = [k for k in [system, slug] + terms if k]
fnd = [p.name for p in (ROOT / 'sources/findings').glob('*.md') if any(k.replace('_', ' ') in p.read_text().lower() or k in p.name for k in keys)]
out.append(f"\n## 4. FINDINGS: {', '.join(fnd[:12]) or 'none'}" + (f" +{len(fnd) - 12}" if len(fnd) > 12 else ''))

# ---------- 5. COVERAGE ----------
by = {}
for r in useful:
    by[SHORT.get(r['creator'], r['creator'])] = by.get(SHORT.get(r['creator'], r['creator']), 0) + 1
out.append('\n## 5. COVERAGE: creators ' + (', '.join(f"{k} {v}" for k, v in by.items()) if by else
           'NONE: answer from data/wiki, label it "my read", report the gap'))
txt = '\n'.join(out)
if len(txt) > BUDGET and not FULL:
    txt = txt[:BUDGET - 200] + '\n... TRUNCATED (hard budget)'
    cut.append('hard budget hit')
txt += '\nTRUNCATED: ' + ('; '.join(cut) if cut else 'nothing')
print(txt)

(ROOT / 'state').mkdir(exist_ok=True)
with open(ROOT / 'state' / 'lookups.log', 'a') as lg:
    lg.write(json.dumps({'t': time.strftime('%Y-%m-%dT%H:%M:%S'), 'system': system, 'terms': terms, 'path': path,
                         'save': D.stamp, 'ar_items': len(labels), 'claims': len(useful), 'by': by, 'chars': len(txt), 'cut': cut}) + '\n')
