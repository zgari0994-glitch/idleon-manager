"""GOAL blocks -> pipeline (Phase B, Zack 2026-11-28). Reads every APPROVED block in brain/systems/*.md (format: docs/planners.md),
works out each system's current rung, target and next task, owner (check.who wins over jobs.yaml; ties = Zack decides),
stall (data unchanged N pulls, or ETA over the limit) and finished state (every rung done -> maintained, tasks leave scoring).
Policy (cadence, unowned, minigames, daily watches): brain/goal_policy.yaml.
Used by: model/score.py (tasks), model/cards3.py (card lines + Account systems), tools/build_brain.py (AUTO line), tools/card.py.
Usage: python3 model/goals.py            summary + problems, writes model/goals.json
       python3 model/goals.py --record   also logs this save's data fingerprints to state/goal_history.json (pipeline only)"""
import re, json, sys, hashlib, datetime as dt
from pathlib import Path
import yaml
sys.path.insert(0, str(Path(__file__).resolve().parent))
import livepath as LP

ROOT = Path(__file__).resolve().parent.parent
SYS = ROOT / 'brain' / 'systems'; OUT = ROOT / 'model' / 'goals.json'; HIST = ROOT / 'state' / 'goal_now_history.json'  # v2: live now only (old goal_history.json retired 2026-11-28)
POL = yaml.safe_load((ROOT / 'brain' / 'goal_policy.yaml').read_text()) or {}
IDX = yaml.safe_load((ROOT / 'model' / 'system_index.yaml').read_text()) or {}
JOBS = yaml.safe_load((ROOT / 'model' / 'jobs.yaml').read_text()) or {}
CHARS = list(JOBS['characters'])
SAVE = (ROOT / 'snapshots' / 'LATEST').read_text().strip()
DAY = dt.datetime.strptime(SAVE[:8], '%Y%m%d').date()
FIELDS = ('role', 'goal', 'ladder', 'objective', 'check', 'buffs', 'triggers', 'stall', 'tasks')
BLOCK = re.compile(r'<!-- GOAL:START.*?```yaml\n(.*?)```.*?<!-- GOAL:END -->', re.S)
MINI = set(POL.get('minigames') or [])
NICK = {'Autiszemo': 'Zemo', 'Autistocat': 'Cat', 'Autisticles': 'Ticles', 'Autistastic': 'Tastic', 'Autistabish': 'Bish',
        'Autistacular': 'Tacular', 'Autistotle': 'Totle', 'Autistomatic': 'Matic', 'Autistronaut': 'Naut',
        'Autistopher': 'Topher', 'Autistachio': 'Tachio'}

_D = None
def data():
    global _D
    if _D is None:
        try:
            from data import load; _D = load()
        except Exception: _D = False
    return _D


def owners(who):
    """check.who -> (kind, [names]). kind: one / multi / every / zack / unowned."""
    w = str(who or '').strip(); lw = w.lower()
    if lw.startswith('every'): return 'every', list(CHARS)
    if not w or lw.startswith(('unassigned', 'none')): return 'unowned', []
    names = sorted([c for c in CHARS if c in w], key=w.index)
    if names: return ('multi' if len(names) > 1 else 'one'), names
    if lw.startswith('zack'): return 'zack', []
    return 'unowned', []


def tier_done(t): return bool(t.get('done')) or bool(re.search(r'\(done\b', str(t.get('target', '')), re.I))


def num(x):
    try: return float(str(x).replace(',', ''))
    except Exception: return None


def short(s, n=110):
    s = re.sub(r'\s+', ' ', str(s)).strip(); return s if len(s) <= n else s[:n - 3] + '...'


def now_spec(y): return y.get('now_path') or (y.get('objective') or {}).get('now_path')


def live_now(y):
    s = now_spec(y)
    if not s: return None
    try: return LP.resolve(s)
    except Exception: return None


def fingerprint(slug, y=None):
    """Stall fingerprint = the live now value only (Phase C A, 2026-11-28), so timers can't fake progress. No now_path = None."""
    if y is None: y = parse()[0].get(slug) or {}
    v = live_now(y)
    return None if v is None else hashlib.sha1(json.dumps(v, sort_keys=True, default=str).encode()).hexdigest()[:12]


def hist():
    try: return json.loads(HIST.read_text())
    except Exception: return {}


def parse():
    out, problems = {}, []
    for p in sorted(SYS.glob('*.md')):
        if p.name.startswith('_'): continue
        slug = p.stem; m = BLOCK.search(p.read_text())
        if not m: problems.append(f'{slug}: no GOAL block'); continue
        try: y = yaml.safe_load(m.group(1)) or {}
        except Exception as e: problems.append(f'{slug}: GOAL yaml does not parse ({str(e).splitlines()[0]})'); continue
        st = str(y.get('status', '')).split()[0] if y.get('status') else ''
        if st == 'MERGED': continue
        if st != 'APPROVED': problems.append(f'{slug}: status {st or "missing"}, not wired'); continue
        miss = [f for f in FIELDS if f not in y]
        if miss: problems.append(f"{slug}: missing {', '.join(miss)}")
        out[slug] = y
    return out, problems


def evaluate(slug, y, H):
    lad = sorted([t for t in (y.get('ladder') or []) if isinstance(t, dict)], key=lambda t: t.get('tier', 0))
    obj = y.get('objective') or {}; chk = y.get('check') or {}; stall = y.get('stall') or {}
    start = int(obj.get('rung') or 1)
    open_ = [t for t in lad if not tier_done(t) and t.get('tier', 0) >= start] or [t for t in lad if not tier_done(t)]
    cur = open_[0] if open_ else None
    on_obj = bool(cur) and cur.get('tier') == obj.get('rung')
    spec = now_spec(y); live = live_now(y) if spec else None
    written = obj.get('now') if on_obj else None
    if not cur: now, now_src = 'all rungs done', 'done'
    elif spec and live is not None: now, now_src = live, 'live'
    elif spec: now, now_src = f'not in save (path {spec})', 'missing'
    else: now, now_src = 'not in save' + (f' (last written: {short(written, 50)})' if written not in (None, '') else ''), 'written'
    target = (obj.get('target') if on_obj and obj.get('target') is not None else None) or (cur or {}).get('target')
    op = str(y.get('now_op') or '>=')
    kind, names = owners(chk.get('who'))
    flags = []
    if now_src == 'live' and num(now) is not None and num(target) is not None and LP.OPS.get(op, LP.OPS['>='])(num(now), num(target)):
        nxt = next((t for t in open_ if t.get('tier', 0) > cur.get('tier', 0)), None)
        if nxt:
            flags.append(f"TARGET HIT (live {LP.fmt(now)} {op} {LP.fmt(target)}): rung {cur.get('tier')} done, now rung {nxt.get('tier')} -> {short(nxt.get('target'), 60)}")
            cur, target = nxt, nxt.get('target')
        else: flags.append(f"TARGET HIT (live {LP.fmt(now)} {op} {LP.fmt(target)}): last rung done, confirm maintained")
    eta, over = num(obj.get('eta_days')), num(stall.get('eta_over_days'))
    if eta is not None and over is not None and eta > over: flags.append(f'STALL: ETA {eta:g}d > {over:g}d')
    n = int(stall.get('pulls_no_progress') or 0); fp = [x[1] for x in H.get(slug, [])][-(n + 1):] if n and spec else []
    if n and len(fp) == n + 1 and fp[0] is not None and len(set(fp)) == 1: flags.append(f'STALL: live now unchanged {n} pulls')
    trig = []
    for t in (y.get('triggers') or []):
        if not isinstance(t, dict): continue
        st, c, v = LP.check(t); trig.append({**t, 'state': st, 'cur': c, 'val': v})
        if st == 'fired': flags.append(f"TRIGGER fired ({short(t.get('when'), 50)}): {short(t.get('then'), 80)}")
    tasks = [t for t in (y.get('tasks') or []) if isinstance(t, dict) and t.get('do')]
    finished = cur is None
    return {'slug': slug, 'title': slug.replace('_', ' ').title(), 'role': str(y.get('role') or '?'), 'goal': y.get('goal'),
            'section': (IDX.get(slug, {}).get('autoreview') or [slug.replace('_', ' ').title()])[0],
            'rung': (cur or {}).get('tier'), 'rungs': len(lad), 'now': now, 'now_src': now_src, 'now_path': spec, 'op': op,
            'target': target, 'src': (cur or {}).get('source'),
            'finished': finished, 'flags': flags, 'cadence': str(chk.get('cadence') or 'daily'), 'look_at': chk.get('look_at'),
            'who': chk.get('who'), 'owner_kind': kind, 'owners': names, 'minigame': slug in MINI,
            'triggers': trig, 'tasks': tasks}


def summary(g):
    if g['finished']: return f"{g['title']}: maintained (every rung done)"
    nxt = g['tasks'][0] if g['tasks'] else None
    nowtxt = LP.fmt(g['now']) + (' (live)' if g.get('now_src') == 'live' else '')
    s = f"{g['title']} [{g['role']}] rung {g['rung']}/{g['rungs']}: now {short(nowtxt, 90)} -> {short(g['target'], 90)}"
    if nxt: s += f". Next: {short(nxt['do'])} [{nxt.get('source') or '?'}]" + (f" (+{len(g['tasks']) - 1} more scored)" if len(g['tasks']) > 1 else '')
    arm = [t for t in g.get('triggers') or [] if t.get('state') == 'armed']
    if arm: s += f" | next: {short(arm[0].get('when'), 60)} ({LP.fmt(arm[0]['cur'])} / {LP.fmt(arm[0]['val'])})"
    if g['flags']: s += ' | ' + ' | '.join(g['flags'])
    return s


def today(g):
    """Full line today? daily = every day; weekly = Thu (weekly reset day); monthly = the 1st. Flags always show."""
    if g['flags']: return True
    c = g['cadence'].lower()
    if c.startswith('week'): return DAY.weekday() == 3
    if c.startswith('month'): return DAY.day == 1
    return True


def build():
    Y, problems = parse(); H = hist()
    G = {s: evaluate(s, y, H) for s, y in Y.items()}
    for s, g in G.items():   # Zack 2026-11-28: helpers = work the system without owning it; split = owners Zack already decided
        c = Y[s].get('check') or {}; g['helpers'] = c.get('helpers') or []; g['split'] = c.get('split')
    for g in G.values(): g['summary'] = summary(g)
    mism, multi = [], []
    for s, g in G.items():
        jo = IDX.get(s, {}).get('owners') or []
        if g['owner_kind'] in ('one', 'multi') and jo and set(jo) - set(g['helpers']) != set(g['owners']):
            mism.append(f"{s}: GOAL check.who {', '.join(NICK.get(n, n) for n in g['owners'])} vs system_index {', '.join(NICK.get(n, n) for n in jo)} (check.who wins)")
        if g['owner_kind'] == 'multi' and not g['split']: multi.append(f"{s}: {g['who']}")
    o = {'v': 2, 'save': SAVE, 'day': str(DAY), 'systems': G, 'problems': problems, 'owner_mismatch': mism, 'multi_owner': multi}
    OUT.write_text(json.dumps(o, indent=1, default=str)); return o


_G = None
def load():
    global _G
    if _G is None:
        try:
            o = json.loads(OUT.read_text()); _G = o if o.get('save') == SAVE and o.get('v') == 2 else build()
        except Exception: _G = build()
    return _G


def tasks():
    """Scorable tasks for model/score.py. Finished systems drop out. Owner: first named (multi = Zack decides, flagged)."""
    T = []
    for s, g in load()['systems'].items():
        if g['finished']: continue
        own = {'one': None, 'multi': None, 'every': 'every character', 'zack': 'Zack', 'unowned': 'unowned'}[g['owner_kind']] or g['owners'][0]
        for i, t in enumerate(g['tasks']):
            T.append({'id': f'goal:{s}:{i}', 'owner': own, 'section': g['section'], 'system': s, 'task': f"{g['title']}: {t['do']}",
                      'minutes': num(t.get('active_min')) or 30, 'wait_h': num(t.get('wait_hr')) or 0, 'src': t.get('source') or 'GOAL block',
                      'urgent': bool(t.get('urgent')) or g['role'].startswith('blocker'), 'unblocks': t.get('unblocks') or [],
                      'active': g['minigame'] or None, 'no_night': g['minigame'],
                      'why': f"GOAL {g['title']} rung {g['rung']}/{g['rungs']} -> {short(g['target'], 60)}"})
    return T


def anvil_line(name):
    """Phase C step C (2026-11-28): full anvil setup from model/anvil.py (hammers, S/C/E split, unspent)."""
    import anvil as _AV
    return _AV.line(name)


def anvil_watch():
    import anvil as _AV
    return _AV.bars_line()


def card_lines(name):
    """Every system this character owns (one/multi/every), full line on its cadence, the rest as one compact line."""
    full, later = [], []
    for s, g in sorted(load()['systems'].items()):
        if name not in g['owners'] or s == 'anvil': continue
        tag = f" (split: {g['split']})" if g.get('split') else ' (shared: Zack decides)' if g['owner_kind'] == 'multi' else (' (every character, own)' if g['owner_kind'] == 'every' else '')
        if g['minigame'] and not g['flags']: later.append(f"{g['title']} (minigame, suggested active)"); continue
        (full if today(g) else later).append(g['summary'] + tag if today(g) else f"{g['title']} ({g['cadence']})")
    if later: full.append('Not due today (full line on its day, weekly = Thu): ' + ', '.join(later))
    return full


def account_lines():
    """Unowned + Zack systems on their cadence; minigames as suggested active tasks; daily watches."""
    L, later, mini = [], [], []
    for k, v in (POL.get('daily_watch') or {}).items(): L.append(anvil_watch() if k == 'anvil' else f"Watch daily ({k}): {v}")
    for s, g in sorted(load()['systems'].items()):
        if g['owner_kind'] not in ('unowned', 'zack'): continue
        who = 'Zack' if g['owner_kind'] == 'zack' else 'unowned'
        if g['minigame']: mini.append(f"{g['title']}: {short(g['tasks'][0]['do'], 90) if g['tasks'] else 'no task'}"); continue
        if today(g): L.append(f"[{who}] {g['summary']}")
        else: later.append(g['title'])
    if mini: L.append('Minigames (suggested active task, trophies; no daily nag): ' + ' | '.join(mini))
    if later: L.append('Unowned, not due today (weekly = Thu): ' + ', '.join(later))
    return L


def record(save=SAVE):
    H = hist(); changed = False
    for s, y in parse()[0].items():
        h = H.setdefault(s, [])
        if h and h[-1][0] == save: continue
        h.append([save, fingerprint(s, y)]); H[s] = h[-8:]; changed = True
    if changed: HIST.parent.mkdir(exist_ok=True); HIST.write_text(json.dumps(H, indent=0))
    return H


if __name__ == '__main__':
    if '--record' in sys.argv: record()
    o = build(); G = o['systems']
    print(f"save {SAVE} ({DAY:%a}): {len(G)} systems wired, {sum(g['finished'] for g in G.values())} maintained, "
          f"{sum(g['now_src'] == 'live' for g in G.values())} live now, {sum(bool(g['flags']) for g in G.values())} flagged, {sum(len(g['tasks']) for g in G.values() if not g['finished'])} tasks to score")
    for k in ('problems', 'owner_mismatch', 'multi_owner'):
        if o[k]: print(f"{k} ({len(o[k])}):"); print('\n'.join('  ' + x for x in o[k]))
    for g in G.values():
        if g['flags']: print('FLAG', g['summary'])
