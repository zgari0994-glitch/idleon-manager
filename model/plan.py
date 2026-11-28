import re
try:
    from consts.consts_monster_data import script_monster_definitions as _MDS
    _RESP = {m.group(1).replace('_', ' '): float(m.group(2)) for m in re.finditer(r'Name:"([^"]+)",AFKtype:"\w+".*?RespawnTime:([\d.E]+)', _MDS)}
except Exception:
    _RESP = {}
try:
    from consts.consts_w3 import getEnemyNameFromMap as _MAPNOTE
except Exception:
    _MAPNOTE = lambda m: ''
"""Card engine v2 (Phase 1, 2026-11-17). One card per character, fixed layout:
move -> quick wins -> active -> AFK -> every sub-system (current -> goal) -> locked -> library talents -> bags.
Plus an account block: alerts, money, salts, ranked active list, unassigned jobs.
Reads jobs.yaml (layer 2), AutoReview review.json, chars.json, raw money, rinse scores.
Writes plans/<save>.md and plans/latest.json (dashboard feed). Usage: python3 model/plan.py"""
import json, gzip, os, re, yaml, datetime as dt
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
stamp = open(os.path.join(R, 'snapshots', 'LATEST')).read().strip()
snap = os.path.join(R, 'snapshots', stamp)
review = json.load(gzip.open(os.path.join(snap, 'review.json.gz')))
chars = json.load(open(os.path.join(snap, 'chars.json')))['characters']
raw = json.load(gzip.open(os.path.join(snap, 'raw.json.gz'))); raw = raw.get('data', raw)
Y = yaml.safe_load(open(os.path.join(R, 'model', 'jobs.yaml')))
RN = json.load(open(os.path.join(R, 'rinse', 'latest.json')))
SCORE = {(r['section'], r['label']): r['score'] for r in RN['rows']}
meta = review['meta']
secs = {s['name']: s for w in review['worlds'] for s in w['sections']}
by_name = {c['character_name']: c for c in chars}
NAMES = list(by_name)
SK = [k for k in chars[0]['skills'] if k != 'Combat' and 'Lol' not in k]
best = {s: max(chars, key=lambda c: c['skills'].get(s, 0)) for s in SK}

# ---------- guidance (2026-11-19): creator HOW from all tagged videos + prerequisites ----------
import sys as _sys
_sys.path.insert(0, os.path.join(R, 'model'))
import guidance as GD
from rapidfuzz import fuzz as _fz
SI_ALL = yaml.safe_load(open(os.path.join(R, 'model', 'system_index.yaml')))
SEC_OWNER = {}
for _k, _v in SI_ALL.items():
    for _sec in _v.get('autoreview', []) or []:
        if _v.get('owners'): SEC_OWNER.setdefault(_sec, _v['owners'][0])
DONE = {}
for _w in review['worlds']:
    for _s in _w['sections']:
        for _g in _s['groups']:
            for _t in [_g] + list(_g.get('tabs', [])):
                for _a in _t.get('items', []):
                    for _b in (_a.get('items') or [_a]):
                        if _b.get('completed') and _b.get('label'): DONE.setdefault(_s['name'], []).append(GD.label_name(_b['label']))

def _afk0(cfg):
    a = cfg.get('afk') or {}
    a = a[0] if isinstance(a, list) and a else a
    return {'text': a.get('text') or a.get('where') or 'GAP', 'src': a.get('src', 'GAP'), **({'park_rule': a['park_rule']} if a.get('park_rule') else {})}

def creator_take(sec, n=2):
    # skip narration ("he uses...") - not an instruction
    """Top creator claims for a whole system, minus ones about things already done."""
    pool = [x for sl in GD._sec2slug().get(sec, []) for x in GD._idx().get(sl, []) if x['type'] in ('priority', 'how_to', 'blocker', 'warning')]
    done = DONE.get(sec, [])
    keep = []
    for x in pool:
        if x['k'] and any(_fz.token_set_ratio(x['k'], d) >= 92 for d in done if len(d) > 4): continue
        if NARR.search(x['say']) or x['date'] < '2024-06': continue
        keep.append(x)
        if len(keep) >= 6: break
    return [GD.fmt(c) for c in GD._dedupe(keep)[:n]]

def how_line(sec, label):
    cs, kind = GD.how(sec, label, 2)
    return [(GD.tag(c), GD.fmt(c)) for c in cs] if kind == 'exact' else []
NARR = re.compile(r'\b(he|his|him|she|her|they|their)\b', re.I)
INFO_ONLY = re.compile(r'^(Info\b|Grand Total|Suggestion:|Note:)', re.I)

LOCK_RE = re.compile(r'(Locked[^.;]*|Needs [^.;]+|Requires [^.;]+|Unlocks? (?:at|by|with|from) [^.;]+)', re.I)
PREREQ = {}   # owner -> list of 'unblocks' lines (filled while building cards)

def prereq_of(label, sec, who):
    """(unlock text, owner of the unlocking system) when an AutoReview line says it's locked."""
    m = LOCK_RE.search(label)
    if not m: return None
    txt = m.group(1).strip()
    if re.search(r'previous', txt, re.I): return (txt, who)
    best, own = 0, None
    for sname, o in SEC_OWNER.items():
        sc = _fz.partial_ratio(sname.lower(), txt.lower())
        if sc > best and len(sname) > 4: best, own = sc, o
    return (txt, own if best >= 90 else None)

# ---------- helpers ----------
MULT = {'K': 1e3, 'M': 1e6, 'B': 1e9, 'T': 1e12, 'Q': 1e15}
def num(x):
    if x is None: return None
    m = re.search(r'(-?[\d,]*\.?\d+(?:e[+-]?\d+)?)\s*([KMBTQ])?', str(x))
    if not m: return None
    v = float(m.group(1).replace(',', ''))
    return v * MULT.get(m.group(2) or '', 1)

def owner_of_tab(path):
    for n in NAMES:
        if re.search(r'(^|/)' + re.escape(n) + r'(\b|$)', path): return n
    return None

def leaves(sec):
    """yield (group_name, path, leaf) for every leaf in a section."""
    s = secs.get(sec)
    if not s: return
    def walk(node, gname, path):
        if 'tabs' in node:
            for t in node['tabs']:
                yield from walk(t, gname, path + '/' + str(t.get('tab', '')))
            return
        for a in node.get('items', []):
            if 'items' in a:
                for b in a['items']:
                    yield gname, path + '/' + a.get('tab', ''), b
            else:
                yield gname, path, a
    for g in s['groups']:
        for gname, path, a in walk(g, g.get('name', ''), g.get('name', '')):
            yield g, path, a

def is_open(a):
    if a.get('completed') or not (a.get('cur') or a.get('goal')) or a.get('goal') in ('✔',): return False
    c, g = num(a.get('cur')), num(a.get('goal'))
    if c is not None and c == g and '%' not in str(a.get('cur')) and 'unspent' not in a['label'].lower(): return False  # at target (keep-as-is rows)
    return True

def ready(a):
    c, g = num(a.get('cur')), num(a.get('goal'))
    if 'unspent' in a['label'].lower() and c: return True
    if c is None or g is None or g <= 0 or '∞' in str(a.get('goal')): return False
    return c > g or (c >= g and '%' in str(a.get('cur')))

def key(sec, path, a): return f"{sec}::{path}::{a['label']}"

def spec(e): return e if isinstance(e, dict) else {'s': e}

# claimed leaves by m-filters (for rest:)
claimed = set()
for cfg in Y['characters'].values():
    for j in cfg['jobs']:
        for e in map(spec, j.get('sections', [])):
            if e.get('m'):
                for g, path, a in leaves(e['s']):
                    if re.search(e['m'], path + ' :: ' + a['label'], re.I): claimed.add(key(e['s'], path, a))

def pick(e, who):
    """open leaves of one section entry for one character."""
    out = []
    for g, path, a in leaves(e['s']):
        if not is_open(a) or any(re.search(x, a['label'], re.I) for x in Y.get('exclude', [])) or any(x in path for x in Y.get('exclude_paths', [])): continue
        tab_owner = owner_of_tab(path)
        if tab_owner and tab_owner != who: continue
        mw = re.search(r'with (Autis\w+)', g.get('name', '') + ' ' + path)
        if mw and mw.group(1) in by_name and mw.group(1) != who: continue
        pre = a['label'].split(':', 1)[0].strip()
        if pre in by_name and pre != who: continue
        k = key(e['s'], path, a)
        if e.get('m') and not re.search(e['m'], path + ' :: ' + a['label'], re.I): continue
        if e.get('rest') and k in claimed: continue
        if e.get('itype'):
            t = ITYPE.get(a['label'].split(':')[0].strip().lower())
            if t is None and not e.get('levers'): continue          # non-item rows (levers) only on the job marked levers
            if t is not None and t != e['itype']: continue
        lk = next((l for l in Y.get('locked', []) if l.get('match') and l['match'] in path), None)
        out.append({'locked': f"LOCKED -> {lk['unlock']}" if lk else '', 'section': e['s'], 'group': g.get('name', '')[:70], 'label': re.sub(r'\s+', ' ', a['label'])[:150],
                    'cur': a.get('cur', ''), 'goal': a.get('goal', ''), 'score': SCORE.get((e['s'], a['label']), 0),
                    'ready': ready(a), 'infinite': '∞' in str(a.get('goal')) or a.get('cur') == 'Linear' or bool(re.fullmatch(r'9{4,}', str(a.get('goal', '')).replace(',', '')))})
    return out

def tier(n):
    s = secs.get(n)
    if not s: return 'n/a'
    if s.get('completed'): return 'done'
    t = s.get('tier') or ''
    return 'untiered' if t in ('0/0', '') else t

def subsystems(items, sec_list):
    """every group of the job's sections: done, or next 2 (finite goals first, rinse score)."""
    subs = []
    for sec in sec_list:
        s = secs.get(sec)
        if not s: subs.append({'name': sec, 'state': 'no AutoReview section', 'items': []}); continue
        for g in s['groups']:
            its = [i for i in items if i['section'] == sec and i['group'] == g.get('name', '')[:70]]
            its.sort(key=lambda i: (not i['ready'], i['infinite'], -i['score']))
            nm = f"{sec}: {g.get('name','')}"[:90]
            if its and any(x['name'] == nm for x in subs): continue
            if its: subs.append({'name': f"{sec}: {g.get('name','')}"[:90], 'state': 'open', 'items': its[:2], 'more': len(its) - 2})
    return subs

# ---------- account data ----------
money = {n: raw.get(f"Money_{c['character_index']}", 0) for n, c in by_name.items()}
bank = raw.get('MoneyBANK', 0)
tp = os.path.join(snap, 'timers.json'); week_start = None
if os.path.exists(tp):
    T = json.load(open(tp)); w = T['resets'].get('Weekly', '')
    secsleft = sum(int(n) * {'d': 86400, 'h': 3600, 'm': 60}[u] for n, u in re.findall(r'(\d+)([dhm])', w))
    cap = dt.datetime.fromisoformat(T['captured_utc'].replace('Z', '+00:00'))
    week_start = (cap + dt.timedelta(seconds=secsleft) - dt.timedelta(days=7)).strftime('%Y-%m-%d')
CONF = json.load(open(os.path.join(R, 'state', 'confirmed.json')))

def library(who):
    out = {}
    for g, path, a in leaves('Library'):
        m = re.match(r'(Skilling|Combat) - (High|Medium|Low) Priority', g.get('name', ''))
        if not m or owner_of_tab(path) != who or not is_open(a): continue
        out.setdefault(f"{m.group(1)} {m.group(2)}", []).append(f"{a['label'].split(':',1)[-1].strip()} {a['cur']}/{a['goal']}")
    return {k: v[:4] for k, v in out.items()}

def bags(who):
    return [f"{a['label']}" for g, path, a in leaves('Storage')
            if g.get('name', '').startswith('Collect more inventory') and owner_of_tab(path) == who and is_open(a)]

SI = yaml.safe_load(open(os.path.join(R, 'model', 'system_index.yaml'))) if os.path.exists(os.path.join(R, 'model', 'system_index.yaml')) else {}
SEC2SYS = {}
for k, v in SI.items():
    for a in v['autoreview']: SEC2SYS.setdefault(a, []).append(k)
MAPS = {v.replace('_', ' '): int(k) for k, v in json.load(open(os.path.join(R, 'sources', 'toolbox', 'map_names.json'))).items()}
def world_of(map_name):
    i = MAPS.get(map_name)
    return None if i is None else min(7, i // 50 + 1)
import sys as _sys
_sys.path.insert(0, '/home/claude/ar/mysite'); _sys.path.insert(0, '/home/claude/work/ar/mysite')
from consts.generated.raw_item_data import raw_item_data as _RD
ITYPE = {}
for _v in _RD.values():
    if isinstance(_v, dict) and _v.get('Name'): ITYPE.setdefault(_v['Name'].lower(), _v.get('Type', ''))
ROUTES = Y.get('lever_routes', [])
def route_of(label):
    for r in ROUTES:
        if re.search(r['m'], label, re.I): return r['owner']
    return None
ROUTED = {}
ATASKS = Y.get('active_tasks', [])
try:
    import priority as _PRIM
    _PRI = _PRIM.build(); PRI_TOP = _PRI['top']['section'] if _PRI['top'] else ''
    PRI_SECS = {x['section'] for x in _PRI['needs'][:3]}
except Exception as _e:
    _PRI, PRI_TOP, PRI_SECS = None, '', set()
# Toolbox dashboard timers (newest timers.json across snapshots; age shown)
tfiles = sorted(os.path.join(R, 'snapshots', d, 'timers.json') for d in os.listdir(os.path.join(R, 'snapshots'))
                if os.path.exists(os.path.join(R, 'snapshots', d, 'timers.json')))
TM = json.load(open(tfiles[-1])) if tfiles else None
TM_AGE = "" if (tfiles and stamp in str(tfiles[-1])) else (f" (timers read {TM.get('captured_utc','?')[:16]}Z, older than this save: check in game)" if TM else '')
ready_now = []
if TM:
    for x in TM['timers'].get('READY NOW', []):
        rt = next((r for r in Y.get('timer_routes', []) if re.search(r['m'], x['name'], re.I)), {'owner': 'unrouted'})
        ready_now.append({'name': x['name'], 'value': x.get('value', ''), 'owner': rt['owner'], 'note': rt.get('note', '')})
cards = []
for name, cfg in Y['characters'].items():
    c = by_name[name]
    card = {'slot': c['character_index'] + 1, 'name': name, 'class': c['class_name'], 'level': c['combat_level'],
            'afk': _afk0(cfg), 'save_map': f"W{c['world']} map {c['current_map_index']}",
            'money': money.get(name, 0), 'jobs': [], 'flags': []}
    allitems = []
    for j in cfg['jobs']:
        ents = list(map(spec, j.get('sections', [])))
        items = [i for e in ents for i in pick(e, name)]
        allitems += [dict(i, job=j['job']) for i in items]
        jd = {'job': j['job'], 'basis': j.get('basis'), 'tiers': {e['s']: tier(e['s']) for e in ents},
              'subs': subsystems(items, list(dict.fromkeys(e['s'] for e in ents))),
              'next': sorted(items, key=lambda i: (not i['ready'], i['infinite'], -i['score']))[:3]}
        if j.get('note'): jd['note'] = j['note']
        sysk = list(dict.fromkeys(k for e in ents for k in SEC2SYS.get(e['s'], [])))
        jd['where'] = [{'system': k, 'toolbox': [t.split(' (')[0] for t in SI[k]['toolbox']],
                        'sources': (f"{SI[k]['transcripts']['tagged_rows']} tagged / {SI[k]['transcripts']['index_chunks']} chunks" if isinstance(SI[k]['transcripts'], dict) else 'no slug')} for k in sysk]
        if j.get('findings'): jd['findings'] = [f"sources/findings/{f}.md" for f in j['findings']]
        if not ents: jd['state'] = 'no AutoReview section: plan from sources/Toolbox map (gap pipeline)'
        if j.get('rule') == 'maestro':
            jd['maestro_behind'] = [f"{s} {c['skills'].get(s,0)}/{best[s]['skills'][s]} ({best[s]['character_name']})"
                                    for s in SK if best[s]['skills'][s] > c['skills'].get(s, 0) and s != 'Construction']
        if j.get('weekly'):
            done = name in CONF.get(week_start or '', {}).get(j['weekly'], []) or j['weekly'] in CONF.get(week_start or '', {})
            jd['weekly'] = {'week_start': week_start, 'done': done}
            if not done: card['flags'].append(f"Weekly {j['weekly']}: not confirmed for week of {week_start or '?'}")
        card['jobs'].append(jd)
    finite = [i for i in allitems if not i['infinite']]
    top = max(finite or allitems or [{}], key=lambda i: (i.get('ready', False), i.get('score', 0)))
    card['move'] = cfg.get('move') or ({'text': f"{top['job']}: {top['label']} {top['cur']} -> {top['goal']}", 'src': 'rinse (Griffy-weighted AutoReview)'} if top else {'text': 'GAP', 'src': 'GAP'})
    qg = {}
    for i in allitems:
        if i['ready']: qg.setdefault((i['job'], i['group']), []).append(i)
    card['quick'] = [f"{g[0][:30]} / {g[1][:40]}: {v[0]['label'][:90]} ({v[0]['cur']} / {v[0]['goal']})" + (f" +{len(v)-1} more ready" if len(v) > 1 else '')
                     for g, v in qg.items()][:8]
    card['quick'] = [f"READY (Toolbox): {r['name']} {r['value']}" + (f" · {r['note']}" if r['note'] else '') for r in ready_now if r['owner'] == name] + card['quick']
    card['active'] = [t for t in ATASKS if name in str(t['owner'])]
    card['locked'] = [l for l in Y.get('locked', []) if name in str(l['owner'])]
    card['talents'] = library(name)
    card['bags'] = bags(name)
    if cfg.get('plan'): card['flags'].append('PLAN: ' + cfg['plan'])
    # PARK: data rule (Zack-approved): DBs park on the open target with the fewest kills left
    rule = _afk0(cfg).get('park_rule')
    card['park'] = {'text': _afk0(cfg).get('text', 'GAP'), 'src': _afk0(cfg).get('src', 'GAP')}
    if rule:
        cand = []
        for g, path, a in leaves('Death Note'):
            if rule in g.get('name', '') + path and is_open(a):
                mm = re.search(r'\(([\d.,]+[KMB]?) remaining\)', a['label'])
                mob = a['label'].split(' in ')[0]; rs = _RESP.get(mob)
                note = _MAPNOTE(a['label'].split(' in ', 1)[-1].split(' (')[0])
                special = str(note).startswith('Special') and 'AFK only' not in str(note)   # e.g. hidden mushroom in King Doot's map
                if mm and rs is not None and rs <= 120 and not special:   # Zack 2026-11-20: skip once-a-day / boss / special spawns
                    cand.append((num(mm.group(1)) * (1 if True else 0), -(num(a.get('cur')) or 0) * 0, rs, a['label'].split(' (')[0], g.get('name', ''), -(num(a.get('cur')) or 0)))
        cand = [c for c in cand if (world_of(c[3].split(' in ', 1)[-1]) or 0) <= 6]   # his rule: W1-W6
        if cand:
            r0 = min(cand, key=lambda c: (c[0], c[2]))   # fewest kills left, then fastest respawn
            mp = r0[3].split(' in ', 1)[-1]; wd = world_of(mp)
            card['park'] = {'text': f"W{wd if wd else '?'} {mp} ({r0[3].split(' in ')[0]}) · {r0[0]:,.0f} kills left, {-r0[5]:.0f}% done · fewest kills left, fastest respawn ({r0[2]}s)", 'src': 'data rule (Zack-approved) on AutoReview Death Note'}
    # WORKING TOWARD: rinse #1 for this character; flag when it is not on the account priority
    pri = PRI_TOP   # Zack 2026-11-19: priority = biggest current need (model/priority.py), never pinned
    pjobs = [j['job'] for j in cfg['jobs'] if any((s if isinstance(s, str) else s.get('s')) in PRI_SECS for s in j.get('sections', []))]
    first = cfg.get('first')  # Zack override: this job goes above the priority on this card
    rin = max(finite or [{}], key=lambda i: i.get('score', 0)) if finite else None
    card['toward'] = {'first': first, 'priority': pri, 'priority_jobs': pjobs,
                      'rinse1': f"{rin['job']}: {rin['label'][:90]} {rin['cur']} -> {rin['goal']} (score {rin['score']})" if rin else 'none',
                      'flag': (f"Rinse ranks {rin['job']} first; the account's biggest need right now is {pri}" if rin and rin['job'] not in pjobs and rin['job'] != first and pjobs else '')}
    # TODAY: ordered steps
    steps = []
    for r in ready_now:
        if r['owner'] == name: steps.append({'do': f"{r['name']}: {r['value']}", 'done': 'claimed / restarted', 'src': 'Toolbox timer' + (' · ' + r['note'] if r['note'] else '')})
    pitems = [i for i in finite if i['job'] in pjobs]
    if first:
        fi = [i for i in finite if i['job'] == first]
        if fi:
            f0 = max(fi, key=lambda i: (i['ready'], i['score']))
            steps.append({'do': f"FIRST ({first}, Zack's order): {f0['label'][:90]} {f0['cur']} -> {f0['goal']}", 'done': f"{f0['goal']}", 'src': 'rinse within that job'})
    if pitems:
        pi = max(pitems, key=lambda i: (i['ready'], i['score']))
        if pi['section'] == 'Death Note' and rule:
            steps.append({'do': f"BIGGEST NEED ({pi['section']}): {pi['job']} at PARK: {card['park']['text'].split(' · ')[0]}", 'done': 'target cleared, then next fewest-left', 'src': card['park']['src']})
        else:
            steps.append({'do': f"BIGGEST NEED ({pi['section']}): {pi['job']}: {pi['label'][:90]} {pi['cur']} -> {pi['goal']}", 'done': f"{pi['goal']}", 'src': 'priority.py (biggest current need)'})
    if card['move']['src'] != 'GAP' and not (first and card['move']['text'].startswith(first)): steps.append({'do': card['move']['text'], 'done': 'goal reached or next step', 'src': card['move']['src']})
    for v in qg.values():
        i = v[0]; steps.append({'do': f"{i['job']}: {i['label'][:90]}", 'done': f"{i['goal']}", 'src': 'AutoReview (ready now)' + (f", +{len(v)-1} more" if len(v) > 1 else '')})
    for t in card['active']:
        steps.append({'do': f"ACTIVE {t['task']}" + (' · ' + '; '.join(t.get('notes', [])) if t.get('notes') else ''), 'done': f"{t['minutes']} min session", 'src': t['src']})
    card['today'] = steps[:10]
    # DAILY RUN (Zack 2026-11-17): every job listed every day. Playbook steps when a playbook exists,
    # else rinse steps (ready items first, then the job's top rinse target). Then park.
    PB = {}  # job -> playbook steps (filled as playbooks get built)
    daily = []
    if cfg.get('move'): daily.append({'block': 'Top move (sourced)', 'kind': 'move', 'steps': [f"{cfg['move']['text']} [{cfg['move']['src']}]"]})
    tim = [f"{r['name']}: {r['value']}" for r in ready_now if r['owner'] == name]
    if tim: daily.append({'block': 'Timers ready (Toolbox)', 'kind': 'timer', 'steps': tim})
    for j, jcfg in zip(card['jobs'], cfg['jobs']):
        its = [dict(i, job=j['job']) for sb in j['subs'] for i in sb['items']]
        st = list(jcfg.get('daily_fixed', []))
        if jcfg.get('timers') and TM:   # job driven by Toolbox dashboard timers (all buckets)
            mx = jcfg.get('miniboss_max', {})
            for bucket, xs in TM['timers'].items():
                for x in xs:
                    if not re.search(jcfg['timers'], x['name'], re.I): continue
                    if x['name'] in mx:
                        mc = re.search(r'Current (\d+)', x.get('value', ''))
                        cur = int(mc.group(1)) if mc else 0
                        st.append(f"{x['name']}: {cur}/{mx[x['name']]} stored" + (" · RUN NOW (max)" if cur >= mx[x['name']] else f" · wait, run at {mx[x['name']]} ({x.get('value','')})"))
                    else:
                        v = x.get('value', '')
                        # Zack 2026-11-21: 'Up · Killed' on Toolbox does not mean you killed it; Up = go kill it
                        up = v.startswith('Up') or bucket == 'READY NOW'
                        st.append(f"{x['name']}: " + ("up now, go kill it" if up else v) + TM_AGE)
        if j['job'] in PB: st += PB[j['job']]; kind = 'playbook'
        else:
            kind = 'rinse'
            secs_in_job = list(dict.fromkeys(i['section'] for i in its))
            multi = len(secs_in_job) > 1
            seen_ct = set()
            for sec in secs_in_job:   # every sub-system of the job gets its own line(s)
                si = [i for i in its if i['section'] == sec]
                pre = f"{sec}: " if multi else ''
                for ct in creator_take(sec):
                    if ct[:60] in seen_ct: continue
                    seen_ct.add(ct[:60]); st.append(f"{pre}CREATORS: {ct}")
                rd = [i for i in si if i['ready']]
                st += [f"{pre}{i['label'][:80]} ({i['cur']} / {i['goal']}) READY" for i in rd[:2] if not INFO_ONLY.search(i['label'])]
                fin = [] if jcfg.get('daily') == 'ready_only' else sorted([i for i in si if not i['ready'] and not i['infinite']], key=lambda i: -i['score'])
                seen_g = []
                seen_l = set()
                for f0 in fin:   # best push per group, up to 3 per sub-system
                    if f0['group'] in seen_g or INFO_ONLY.search(f0['label']): continue
                    ln = re.sub(r'^Autis\w+:\s*', '', f0['label'])[:60]
                    if ln in seen_l: continue
                    seen_l.add(ln)
                    seen_g.append(f0['group'])
                    ro = route_of(f0['label'])
                    if ro and ro != name:
                        if not any(f0['label'][:60] in x for x in ROUTED.get(ro, [])): ROUTED.setdefault(ro, []).append(f"{f0['label'][:80]} {f0['cur']} -> {f0['goal']} (toward {name} {j['job']})")
                        st.append(f"{pre}Lever on {ro}: {f0['label'][:60]}"); continue
                    pq = prereq_of(f0['label'], sec, name)
                    if pq and pq[1] and pq[1] != name:
                        PREREQ.setdefault(pq[1], []).append(f"{name} is waiting on you: {pq[0].split('. Now:')[0].split(' Now:')[0][:90]}.")
                    st.append(f"{pre}Push: {re.sub(r'^Autis[a-z]+:\s*', '', f0['label'])[:80]} {f0['cur']} -> {f0['goal']}" + (f" · {f0['locked']}" if f0.get('locked') else '')
                              + (f" · BLOCKED: {pq[0][:80]}" + (f" ({pq[1]}'s job)" if pq[1] and pq[1] != name else '') if pq else ''))
                    for tg, h in how_line(sec, f0['label']):
                        st.append(f"{pre}  {tg}: {h}")
                    if len(seen_g) == 3: break
            if not st: st.append('Nothing to do today.' if jcfg.get('daily') == 'ready_only' else ('No plan for this one yet.' if not j.get('note') or 'AutoReview section' in (j.get('note') or j.get('state') or '') else j['note']))
        daily.append({'block': j['job'], 'kind': kind, 'steps': st})
    for l in card['locked']:
        daily.append({'block': f"Unlock: {l['feature']}", 'kind': 'unlock', 'steps': [l['unlock']]})
    card['daily'] = daily
    cards.append(card)

for l in Y.get('locked', []):
    o_unlock = None; best = 0
    for sname, o in SEC_OWNER.items():
        sc = _fz.partial_ratio(sname.lower(), l['unlock'].lower())
        if sc > best and len(sname) > 4: best, o_unlock = sc, o
    for feat_owner in [x.strip() for x in str(l['owner']).split(',')]:
        if best >= 90 and o_unlock and o_unlock != feat_owner and feat_owner in by_name:
            PREREQ.setdefault(o_unlock, []).append(f"{feat_owner} is waiting on you: {l['unlock'].split('. Now:')[0].split(' Now:')[0][:90]} (unlocks {re.split(r' [(]', l['feature'])[0]}).")
            for cd in cards:
                if cd['name'] == feat_owner:
                    for b in cd['daily']:
                        if b['kind'] == 'unlock' and l['feature'] in b['block']: b['steps'].append(f"BLOCKED on {o_unlock}'s job")
# ---------- system planners (model/<system>.py: build() + card_lines(); optional routed()) ----------
import importlib
PLANNERS = [('sailing', 'Sailing'), ('farming', 'Farming'), ('cooking', 'Cooking'), ('divinity', 'Divinity'), ('breeding', 'Breeding'), ('printer', 'prints'), ('alchemy', 'Alchemy'), ('stamps', 'Stamps'), ('greenstacks', 'Greenstacks'), ('statues', 'Statue turn-ins'), ('refinery', 'Construction'), ('worship', 'Worship totems'), ('compass', 'Compass'), ('grimoire', 'Grimoire'), ('deathnote', 'CHOW'), ('equinox', 'Equinox'), ('atom', 'Construction'), ('saltlick', 'Salt Lick'), ('armor', 'Godshard'), ('vault', 'Upgrade Vault'), ('tesseract', 'Tesseract'), ('royal_armory', 'Royal Guardian #1'), ('lab', 'Lab'), ('buildings', 'Construction'), ('gaming', 'Gaming'), ('sneaking', 'Sneaking'), ('summoning', 'Summoning'), ('spelunking', 'Spelunking'), ('w7minis', 'W7 minis'), ('menagerie', 'Luminous Menagerie'), ('research', 'Research'), ('reef', 'W7 reef'), ('gallery', 'Gallery'), ('emperor', 'Emperor'), ('islands', 'Islands'), ('arcade', 'W7 minis'), ('owl', 'Clickers'), ('killroy', 'Kilroy'), ('hole', 'The Hole'), ('slab', 'Slab'), ('beanstalk', 'Farming'), ('capevine', 'Gallery + capes'), ('shops', 'Gem / Event'), ('tome', 'Tome'), ('maint', 'Maintenance')]   # (module, daily block name contains)
for _mod, _blk in PLANNERS:
    try:
        _m = importlib.import_module(_mod)
        _o = _m.build(); _sl = _m.card_lines(_o)
        if hasattr(_m, 'routed'):
            for _w, _ls in _m.routed(_o).items(): ROUTED.setdefault(_w, []).extend(_ls)
        _first = True
        for cd in cards:
            for b in cd['daily']:
                if _blk in b['block']:
                    head = _m.char_lines(_o, cd['name']) + (_sl if _first else []) if hasattr(_m, 'char_lines') else (_sl if _first else [])   # no char_lines: first matching block only
                    _first = False
                    if b.get('kind') == 'playbook': b['steps'] = b['steps'] + head   # second planner on the same block appends
                    else: b['steps'] = head + [x for x in b['steps'] if any(k in x for k in ('Push:', 'HOW:', 'WHY:', 'CREATORS:', 'READY', 'Collect'))]
                    b['kind'] = 'playbook'
    except Exception as e:
        print(f'{_mod} planner failed:', e)
for cd in cards:
    if PREREQ.get(cd['name']):
        cd['daily'].insert(1 if cd['daily'] and cd['daily'][0]['kind'] == 'move' else 0,
                           {'block': 'Unblocks other characters (do these first)', 'kind': 'prereq', 'steps': list(dict.fromkeys(PREREQ[cd['name']]))[:6]})
    if ROUTED.get(cd['name']):
        cd['daily'].insert(len(cd['daily']), {'block': 'Levers for other jobs', 'kind': 'lever', 'steps': ROUTED[cd['name']][:6]})
# ---------- every_character jobs (Zack 2026-11-19): each card gets its own slice ----------
try:
    import printer as _P; _PO = json.load(open(os.path.join(R, 'model', 'printer.json')))
except Exception:
    pass
EVERY = []
_chars_facts = {c['character_name']: c for c in chars}
for ej in Y.get('every_character', []):
    shared = []
    per = {cd['name']: [] for cd in cards}
    for sec in ej['sections']:
        for g, path, a in leaves(sec):
            if not is_open(a): continue
            line = f"{a['label'][:110]} ({a.get('cur')} -> {a.get('goal')})"
            hit = [n for n in per if n.lower() in (path + ' ' + a['label']).lower()]
            if hit:
                for n in hit: per[n].append(line)
            else: shared.append(f"{sec}: {line}")
    for cd in cards:
        steps = list(dict.fromkeys(per.get(cd['name'], [])))[:4]
        f = _chars_facts.get(cd['name'], {})
        if ej.get('facts') == 'prayers':
            try:
                import prayers as _PR
                if '_PRO' not in globals(): _PRO = _PR.build(); EVERY_SHARED_EXTRA = _PR.card_lines(_PRO)
                steps = _PR.char_lines(_PRO, cd['name']) + steps
            except Exception as e:
                steps.insert(0, f"Equipped: {', '.join(f.get('equipped_prayers') or []) or 'none'} (prayers planner failed: {e})")
        if ej.get('facts') == 'worship':
            try:
                import worship as _W
                if '_WO' not in globals(): _WO = _W.build()
                steps = _W.char_lines(_WO, cd['name']) + steps
            except Exception as e: steps.insert(0, f"(worship planner failed: {e})")
        if ej.get('facts') == 'postoffice':
            try:
                import postoffice as _PO2
                if '_POO' not in globals(): _POO = _PO2.build()
                steps = _PO2.char_lines(_POO, cd['name']) + steps
            except Exception as e: steps.insert(0, f"(post office planner failed: {e})")
        if ej.get('facts') == 'setup':
            try:
                import cardpresets as _CP
                if '_CPO' not in globals(): _CPO = _CP.build(); json.dump(_CPO, open(os.path.join(R, 'model', 'cardpresets.json'), 'w'), indent=1)
                steps = _CP.char_lines(_CPO, cd['name']) + steps
            except Exception as e: steps.insert(0, f"(setup check failed: {e})")
            if steps: cd['daily'].insert(0, {'block': 'Setup check', 'kind': 'every', 'steps': steps})
            continue
        if ej.get('facts') == 'combat': steps.insert(0, f"Combat Lv {f.get('combat_level')}")
        if ej.get('facts') == 'printer':
            if any('prints' in b['block'] for b in cd['daily']): continue
            try:
                import printer as _P; steps = _P.char_lines(_PO, cd['name']) if '_PO' in globals() else []
            except Exception: steps = []
        if steps: cd['daily'].append({'block': f"Every character: {ej['job']}", 'kind': 'every', 'steps': steps + ([f"({ej['note']})"] if ej.get('note') else [])})
    if ej.get('facts') == 'prayers' and 'EVERY_SHARED_EXTRA' in globals(): shared = EVERY_SHARED_EXTRA + shared
    EVERY.append({'job': ej['job'], 'shared': shared[:14], 'note': ej.get('note', '')})

# ---------- account block ----------
alerts = []
for al in Y.get('alerts', []):
    hits = [a['label'] for g, path, a in leaves(al['section']) if is_open(a) and re.search(al['m'], path + ' :: ' + a['label'], re.I)
            and (al.get('when') == 'match' or ready(a))]
    if hits: alerts.append({'name': al['name'], 'owner': al['owner'], 'hits': hits[:4]})
salts = [f"{a['label']} {a.get('cur','')}".strip() for g, path, a in leaves('Refinery') if g.get('name', '').startswith('Salt Excess')]
lp = os.path.join(R, 'model', 'ledger.json')
ledger = json.load(open(lp)) if os.path.exists(lp) else None
bp = os.path.join(R, 'model', 'buffs.json')
buffs = json.load(open(bp)) if os.path.exists(bp) else None
for cd in cards: cd['buffs_missing'] = (buffs or {}).get('missing_by_owner', {}).get(cd['name'], [])
cp = os.path.join(R, 'model', 'coins.json')
coins = json.load(open(cp)) if os.path.exists(cp) else None
ranked = sorted(ATASKS, key=lambda t: (t['importance'], t['minutes']))
account = {'money': {'total': sum(money.values()) + bank, 'bank': bank, 'per_char': money,
                     'holder': max(money, key=money.get)},
           'alerts': alerts + [{'name': f"{r['name']} ({r['value']})", 'owner': r['owner'], 'hits': [r['note']] if r['note'] else []} for r in ready_now if r['owner'] in ('anyone', 'unrouted')],
           'timers_captured': TM['captured_utc'] if TM else None, 'salts': salts, 'ledger': ledger, 'buffs': {'newly_owned': buffs['newly_owned'], 'account_missing': buffs['missing_by_owner'].get('account', []), 'stats': [{'stat': x['stat'], 'section': x['section'], 'owned': x['owned'], 'missing': x['missing']} for x in buffs['stats']]} if buffs else None, 'coins': {k: coins[k] for k in ('richest', 'vault', 'advice_fish', 'vendor', 'caveats')} if coins else None, 'active_ranked': ranked,
           'quick_mode': [t for t in ranked if t['minutes'] <= 15],
           'unassigned': Y.get('unassigned') or [], 'account_wide': Y.get('account_wide', []), 'every_character': EVERY,
           'loop': ['7am PC: refresh, full/maxed/timers checklist, dailies due now',
                    'Workday: active task(s) running (top of the ranked list)',
                    '3pm: cloud save, refresh, then cards one character at a time on the tablet']}
try:
    import active as _ACT
    account['active_plan'] = _ACT.build()
except Exception as _e:
    account['active_plan'] = None; print('active plan failed:', _e)
import plain as _PL
cards = _PL.clean(cards); account = _PL.clean(account)
print("wording spots: %d" % _PL.write_log())
json.dump({'meta': meta, 'cards': cards, 'account': account}, open(os.path.join(R, 'plans', 'latest.json'), 'w'), indent=1)

# ---------- markdown ----------
def m(x): return f"{x:.2e}"
L = [f"# Cards · game save {meta['game_save_et']}", '', '## Account']
L += [f"- ALERT {a['name']} -> {a['owner']}: " + '; '.join(h[:70] for h in a['hits']) for a in alerts]
L.append(f"- Money: total {m(account['money']['total'])}, bank {m(bank)}, {account['money']['holder']} holds {100*money[account['money']['holder']]/max(1,sum(money.values())):.0f}%")
L += [f"- Salt: {s}" for s in salts]
L.append('- Active (ranked): ' + ' | '.join(f"{t['owner']}: {t['task']} ({t['minutes']}m)" for t in ranked))
L += [f"- Unassigned: {u['job']} ({u['note']})" for u in account['unassigned']]
L.append('')
for cd in sorted(cards, key=lambda x: x['slot']):
    L.append(f"## {cd['slot']}. {cd['name']} · {cd['class']} {cd['level']} · coins {m(cd['money'])}")
    tw = cd['toward']
    L.append(f"FOCUS: the account's biggest need is {tw['priority']}." + (f" His part: {', '.join(tw['priority_jobs'])}." if tw['priority_jobs'] else '') + (f" {tw['first']} comes first on this card (your call)." if tw.get('first') else ''))

    L.append(f"PARK: {re.sub(r' *[(\[][^)\]]*(?:[0-9]{2}:[0-9]{2}|Pulse|zack)[^)\]]*[)\]]', '', cd['park']['text'])}")
    L.append('DAILY RUN:')
    n = 0
    for b in cd['daily']:
        L.append(f"  {b['block'].upper()}" + ('' if b['kind'] == 'playbook' else f"  [{b['kind']}]"))
        for st in b['steps']:
            n += 1; L.append(f"   {n}. {st}")
    L.append(f"  PARK: {cd['park']['text']}")
    for f in cd['flags']: L.append(f"- FLAG {f}")
    L.append('DETAILS:')
    for j in cd['jobs']:
        t = ', '.join(f"{k} {v}" for k, v in j['tiers'].items())
        L.append(f"- **{j['job']}**" + (f" ({t})" if t else '') + (f" · {j['note']}" if j.get('note') else '') + (f" · {j['state']}" if j.get('state') else ''))
        for f in j.get('findings', []): L.append(f"  - findings: {f}")
        if j.get('maestro_behind'): L.append(f"  - behind: {', '.join(j['maestro_behind'])}")
        for sb in j['subs']:
            L.append(f"  - {sb['name']}: " + '; '.join(f"{i['label'][:80]} {i['cur']} -> {i['goal']}" + (' READY' if i['ready'] else '') for i in sb['items']) + (f" (+{sb['more']} more)" if sb.get('more', 0) > 0 else ''))
    for l in cd['locked']: L.append(f"- LOCKED: {l['feature']} <- {l['unlock']}")
    for k, v in cd['talents'].items(): L.append(f"- Talents {k}: " + ', '.join(v))
    if cd['bags']: L.append('- Bags missing: ' + '; '.join(b[:50] for b in cd['bags']))
    if cd.get('buffs_missing'): L.append(f"- BUFF SOURCES MISSING ({len(cd['buffs_missing'])}, model/buffs.md): " + ' | '.join(cd['buffs_missing'][:8]))
    L.append('')
if account.get('active_plan'): L += ['', '## Active plan', ''] + _ACT.lines(account['active_plan'])[1:]
open(os.path.join(R, 'plans', f'{stamp}.md'), 'w').write('\n'.join(L))
print(f"{len(cards)} cards, {sum(len(j['subs']) for c in cards for j in c['jobs'])} sub-systems, {len(alerts)} alerts -> plans/{stamp}.md")
