"""Phase C step D (Zack 2026-11-28): data gaps that still matter. One module, used by tools/lookup.py and
model/syscheck2.py. Everything reads Toolbox's parser (data.py) or the raw save; anything not sourced says "my read".
Dry run: python3 model/phase_d.py"""
import csv, glob, gzip, json, math, sys
from pathlib import Path
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
ROOT = Path(__file__).resolve().parents[1]
_D = None


def D():
    global _D
    if _D is None:
        import data
        _D = data.load()
    return _D


def A():
    return D().raw['account']


def raw():
    r = json.load(gzip.open(ROOT / 'snapshots' / D().stamp / 'raw.json.gz'))
    return r.get('data', r)


def short(v):
    try: v = float(v)
    except Exception: return str(v)
    if abs(v) >= 1e21: return f"{v:.3g}"
    for n, s in ((1e18, 'QQ'), (1e15, 'Q'), (1e12, 'T'), (1e9, 'B'), (1e6, 'M'), (1e3, 'K')):
        if abs(v) >= n: return f"{v / n:.3g}{s}"
    return f"{v:.3g}" if v != int(v) else str(int(v))


def nm(s):
    return str(s or '').replace('_', ' ')


# ---------- Salt: flag only when an input is short and production stalls ----------
STALL_SOON_CYCLES = 24   # my read: a Toolbox-deficit input with under 24 cycles left counts as "about to stall"


def salt_rows():
    """Per active salt: each input's cost per cycle (Toolbox calcCost: floor(rank^(1.3 if salt and index<=salt task
    level else 1.5)) x quantity), owned, cycles left; deficit = Toolbox dashboard saltDeficit alert."""
    ref = A()['refinery']; stl = ref.get('refinerySaltTaskLevel') or 0
    salts = ref.get('salts') or []; names = {s.get('saltName') for s in salts}
    deficit = {x.get('saltName') for x in ((((A().get('_zack') or {}).get('alerts') or {}).get('account') or {}).get('World 3') or {}).get('construction', {}).get('saltDeficit') or []}
    rows = []
    for i, s in enumerate(salts):
        if not s.get('active') or not s.get('unlocked'): continue
        rank = s.get('rank') or 0
        for c in s.get('cost') or []:
            is_salt = c.get('name') in names
            per = math.floor(rank ** (1.3 if is_salt and i <= stl else 1.5)) * (c.get('quantity') or 0)
            have = c.get('totalAmount') or 0
            rows.append({'salt': s.get('saltName'), 'rank': rank, 'input': c.get('name'), 'per_cycle': per, 'have': have,
                         'cycles': have / per if per else float('inf'), 'deficit': s.get('saltName') in deficit and is_salt})
    return rows


def salt_check():
    rows = salt_rows()
    stalled = [r for r in rows if r['cycles'] < 1]
    soon = [r for r in rows if r['deficit'] and 1 <= r['cycles'] < STALL_SOON_CYCLES]
    if not stalled and not soon: return None
    subs = [f"{nm(r['salt'])} R{r['rank']}: {nm(r['input'])} {short(r['have'])} / {short(r['per_cycle'])} per cycle = STALLED" for r in stalled]
    subs += [f"{nm(r['salt'])} R{r['rank']}: {nm(r['input'])} {short(r['have'])}, {r['cycles']:.0f} cycles left (Toolbox deficit)" for r in soon]
    head = 'DO NOW Salt: production stalled, refill the input or drop the rank' if stalled else 'Salt: input about to run dry (my read: under 24 cycles)'
    return ('refinery', head, subs + ['fix: raise the input (printer / previous salt) or lower that salt\'s rank to Toolbox maxSafeRank'])


def salt_lines():
    out = [f"  {nm(r['salt'])} R{r['rank']} <- {nm(r['input'])}: {short(r['have'])} owned, {short(r['per_cycle'])}/cycle, "
           + (f"{r['cycles']:.0f} cycles" if r['cycles'] < 1e6 else 'plenty') + (' | Toolbox deficit' if r['deficit'] else '')
           + (' | STALLED' if r['cycles'] < 1 else '') for r in salt_rows()]
    return out + [f"  card flag: only when stalled (<1 cycle) or Toolbox deficit with <{STALL_SOON_CYCLES} cycles left (my read)"]


# ---------- Trash shop: buy list when Fractal opens ----------
def trash_list():
    isl = A().get('islands') or {}
    t = next((x for x in isl.get('list') or [] if x.get('name') == 'Trash'), {}) or {}
    f = next((x for x in isl.get('list') or [] if x.get('name') == 'Fractal'), {}) or {}
    plan = yaml.safe_load(open(ROOT / 'brain' / 'trash_shop.yaml'))
    shop = {x.get('name'): x for x in t.get('shop') or []}
    lines = []
    for i, it in enumerate(plan['order'], 1):
        s = shop.get(it['name'], {})
        cost = s.get('cost'); have = t.get('trash') or 0
        st = '' if cost is None else (' OK' if have >= cost else f" SHORT {short(cost - have)}")
        lines.append(f"{i}. {it['name']} ({short(cost)} trash{st}): {it['why']}")
    return f, t, lines, plan


def trash_check():
    f, t, lines, plan = trash_list()
    if not f.get('unlocked'): return None
    return ('islands', f"DO NOW Trash shop (Fractal is open): buy in this order, {short(t.get('trash'))} trash on hand ({plan['source']})", lines)


# ---------- Obols: meta watch only ----------
TOP = {'griffybit', 'griffy', 'pulseidle', 'pulse', 'nocturne'}


def obol_watch():
    m = yaml.safe_load(open(ROOT / 'brain' / 'obol_meta.yaml'))
    since = str(m['checked'])
    hits = []
    for fn in glob.glob(str(ROOT / 'sources/creators/*/tags/*.csv')):
        for r in csv.DictReader(open(fn)):
            if r.get('creator', '').lower() not in TOP: continue
            dt = str(r.get('date') or '')
            if not dt[:1].isdigit() or dt <= since: continue   # undated claims can't count as newer
            st = r.get('statement', '').lower()
            if 'obol' in st and r.get('claim_type') in ('setup', 'priority', 'opinion', 'how_to', 'target'):
                hits.append(r)
    return m, sorted(hits, key=lambda r: r['date'], reverse=True)


def obol_check():
    m, hits = obol_watch()
    if not hits: return None
    return ('obols', f"Obols: {len(hits)} new top-creator obol claim(s) since {m['checked']}, compare vs your setup (meta watch)",
            [f"{r['creator']} {r['date']}: {r['statement'][:140]} [{r['video_id']} {r['t_start']}]" for r in hits[:5]]
            + ['if it changes the setup: update brain/obol_meta.yaml (setup + checked date)'])


def obol_lines():
    m, hits = obol_watch()
    s = m['setup']
    out = [f"  Zack's setup (every character + family): silver {s['silver']}, gold {s['gold']}, platinum {s['platinum']}, molten {s['molten']}",
           f"  meta watch: baseline checked {m['checked']} ({m['basis']}); new Griffy/Pulse/Nocturne obol claims since: {len(hits)}"]
    out += [f"    {r['creator']} {r['date']}: {r['statement'][:120]}" for r in hits[:5]]
    return out + ['  card: silent unless a new top-creator obol claim lands (then Tachio\'s card says compare)']


# ---------- World bosses (BossInfo) ----------
BOSSES = ['Amarok', 'Efaunt', 'Chizoar', 'Troll', 'Kattlekruk', 'Emperor']   # Toolbox parsers/class-specific/speedrun.ts
DIFF = ['Normal', 'Chaotic', 'Nightmare']


def world_bosses():
    bi = raw().get('BossInfo') or []
    rows = [[x.get(str(i)) for i in range(x.get('length', 3))] if isinstance(x, dict) else x for x in bi]
    out = []
    for i, r_ in enumerate(rows[:6]):
        d = int(round(float(r_[0] or 0)))
        pay = f", pays out on Kattlekruk's difficulty ({DIFF[int(round(float(rows[4][0] or 0)))]})" if i == 5 else ''
        out.append(f"  {BOSSES[i]}: difficulty {DIFF[d] if d < 3 else d}, HP {short(r_[1])}, defence {short(r_[2])}{pay}")
    return out + ['  source: Toolbox speedrun.ts (BossInfo[n] = [difficulty, hp, defence]); kill/done state is not in BossInfo']


# ---------- Weekly boss raw ----------
def weekly_raw_lines():
    w = A().get('weeklyBossesRaw') or {}
    c, g = w.get('c') or 0, w.get('g') or 0
    skins = sorted(k[3:] for k, v in w.items() if k.startswith('UI_') and str(v) == '1')
    return [f"  week buffs (Toolbox getWeeklyBossBuffs): tea break +{min(150, float(c)):.0f}% Class EXP, chilly hotdogs +{min(150, float(g)):.0f}% damage (cap 150)",
            f"  UI skins owned: {', '.join(skins) or 'none'}",
            f"  done-state: not decodable ({sum(1 for k in w if k.startswith('d_'))} d_* keys, Toolbox doesn't read them), so the daily line stays until the boss changes"]


# ---------- Super talent names ----------
_TN = None


def talent_name(i):
    global _TN
    if _TN is None:
        _TN = json.load(open(ROOT / 'brain' / 'talent_names.json'))['names']
    return _TN.get(str(i), f"talent {i}")


# ---------- Guild (Toolbox needs the guild doc, the paste doesn't carry it) ----------
def guild_lines():
    g = raw().get('Guild')
    g = json.loads(g) if isinstance(g, str) else g
    if not g: return ['  Guild: not in the raw save (not in a guild)']
    names = [b.get('name') for b in (A().get('guild') or {}).get('guildBonuses') or []]
    lv = g[0] if g and isinstance(g[0], list) else []
    out = ['  in a guild: YES. Toolbox shows "unlocked=False / Lv 0" only because its guild doc (Firestore) is not in a Copy raw data paste',
           '  bonus levels from the save\'s own copy (Guild[0], same field Toolbox sums for GP):']
    out += ['    ' + ', '.join(f"{nm(names[i]) if i < len(names) else i} {v}" for i, v in enumerate(lv) if v)]
    out.append(f"  task rows: {len(g) - 1} (Guild[1:], [task id, done flag, progress])")
    return out


# ---------- Compass dust per upgrade ----------
def compass_dust_lines():
    c = A()['compass']; dusts = [d.get('name') for d in c.get('dusts') or []]; bal = {d.get('name'): d.get('value') or 0 for d in c.get('dusts') or []}
    out = ['  dust balances: ' + ', '.join(f"{n} {short(v)}" for n, v in bal.items())]
    opn = []
    for u in c.get('upgrades') or []:
        try: dn = dusts[int(u.get('x3') or 0)]
        except Exception: dn = f"dust {u.get('x3')}"
        cost = u.get('cost')
        if cost is None or u.get('unlocked') is False: continue
        if (u.get('x4') or 0) > 0 and (u.get('level') or 0) >= u['x4']: continue   # x4 = max level (shapeIcon ...Max)
        opn.append((cost / max(bal.get(dn) or 1e-9, 1e-9), u, dn))
    opn.sort(key=lambda x: x[0])
    for _, u, dn in opn[:10]:
        ok = 'OK' if (bal.get(dn) or 0) >= u['cost'] else f"SHORT {short(u['cost'] - (bal.get(dn) or 0))}"
        out.append(f"    {nm(u.get('name'))} Lv {u.get('level')} | next {short(u['cost'])} {dn} {ok}")
    return out + ['  dust type = Toolbox dustNames[upgrade.x3] (compass.ts); cheapest vs own dust first']


# ---------- Lunarheim (next lore boss) POW requirement ----------
def lore_lines():
    sp = A()['spelunking']; pw = (sp.get('power') or {}).get('value') or 0
    zones = ['Pebble Cove', 'Sedimeadow', 'Rustbelt', 'Blushpit', 'Chucklemire', 'Lunarheim', 'Bizarrio', 'Glitter End', 'Scoutpost', 'Exiled Throne']
    out = [f"  POW now {short(pw)}"]
    for b in sp.get('loreBosses') or []:
        i = b.get('index'); ds = b.get('discoveries') or []
        if b.get('defeated'): continue
        first = ds[0]['powerReq'] if ds else None
        out.append(f"  NEXT lore boss: {zones[i] if i < len(zones) else i} (#{i + 1}): first discovery needs {short(first)} POW "
                   f"({'OK' if pw >= (first or 0) else 'SHORT x' + format((first or 0) / max(pw, 1), '.2f')}), boss found at cave level {b.get('foundAt')} (my read of foundAt), best cave {b.get('bestCaveLevel')}")
        out.append(f"    reward: {nm(b.get('description'))[:110]}")
        break
    return out


def lore_check():
    ls = lore_lines()
    return ('spelunk', 'Spelunking target: ' + ls[1].strip() if len(ls) > 1 else None, ls[2:]) if len(ls) > 1 else None


FISH_NOTE = ['  currency: not in Toolbox\'s read of the save (getAdviceFish has levels + costs only, no balance); check the Advice Fish balance in game (my read)']


if __name__ == '__main__':
    print(f"save {D().stamp}, {D().age_hours:.1f} h old")
    for title, fn in (('salt', salt_lines), ('obols', obol_lines), ('world bosses', world_bosses), ('weekly raw', weekly_raw_lines),
                      ('compass dust', compass_dust_lines), ('lore', lore_lines)):
        print('##', title); [print(x) for x in fn()]
    f, t, lines, plan = trash_list()
    print(f"## trash shop (Fractal unlocked={f.get('unlocked')}, trash {t.get('trash')})"); [print('  ' + x) for x in lines]
    print('## card checks:', salt_check(), trash_check(), obol_check(), lore_check(), sep='\n')
