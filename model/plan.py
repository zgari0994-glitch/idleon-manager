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
        if not is_open(a) or any(re.search(x, a['label'], re.I) for x in Y.get('exclude', [])): continue
        tab_owner = owner_of_tab(path)
        if tab_owner and tab_owner != who: continue
        pre = a['label'].split(':', 1)[0].strip()
        if pre in by_name and pre != who: continue
        k = key(e['s'], path, a)
        if e.get('m') and not re.search(e['m'], path + ' :: ' + a['label'], re.I): continue
        if e.get('rest') and k in claimed: continue
        out.append({'section': e['s'], 'group': g.get('name', '')[:70], 'label': re.sub(r'\s+', ' ', a['label'])[:150],
                    'cur': a.get('cur', ''), 'goal': a.get('goal', ''), 'score': SCORE.get((e['s'], a['label']), 0),
                    'ready': ready(a), 'infinite': '∞' in str(a.get('goal')) or a.get('cur') == 'Linear'})
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
ATASKS = Y.get('active_tasks', [])
# Toolbox dashboard timers (newest timers.json across snapshots; age shown)
tfiles = sorted(os.path.join(R, 'snapshots', d, 'timers.json') for d in os.listdir(os.path.join(R, 'snapshots'))
                if os.path.exists(os.path.join(R, 'snapshots', d, 'timers.json')))
TM = json.load(open(tfiles[-1])) if tfiles else None
ready_now = []
if TM:
    for x in TM['timers'].get('READY NOW', []):
        rt = next((r for r in Y.get('timer_routes', []) if re.search(r['m'], x['name'], re.I)), {'owner': 'unrouted'})
        ready_now.append({'name': x['name'], 'value': x.get('value', ''), 'owner': rt['owner'], 'note': rt.get('note', '')})
cards = []
for name, cfg in Y['characters'].items():
    c = by_name[name]
    card = {'slot': c['character_index'] + 1, 'name': name, 'class': c['class_name'], 'level': c['combat_level'],
            'afk': cfg.get('afk', {'text': 'GAP', 'src': 'GAP'}), 'save_map': f"W{c['world']} map {c['current_map_index']}",
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
    cards.append(card)

# ---------- account block ----------
alerts = []
for al in Y.get('alerts', []):
    hits = [a['label'] for g, path, a in leaves(al['section']) if is_open(a) and re.search(al['m'], path + ' :: ' + a['label'], re.I)
            and (al.get('when') == 'match' or ready(a))]
    if hits: alerts.append({'name': al['name'], 'owner': al['owner'], 'hits': hits[:4]})
salts = [f"{a['label']} {a.get('cur','')}".strip() for g, path, a in leaves('Refinery') if g.get('name', '').startswith('Salt Excess')]
lp = os.path.join(R, 'model', 'ledger.json')
ledger = json.load(open(lp)) if os.path.exists(lp) else None
ranked = sorted(ATASKS, key=lambda t: (t['importance'], t['minutes']))
account = {'money': {'total': sum(money.values()) + bank, 'bank': bank, 'per_char': money,
                     'holder': max(money, key=money.get)},
           'alerts': alerts + [{'name': f"{r['name']} ({r['value']})", 'owner': r['owner'], 'hits': [r['note']] if r['note'] else []} for r in ready_now if r['owner'] in ('anyone', 'unrouted')],
           'timers_captured': TM['captured_utc'] if TM else None, 'salts': salts, 'ledger': ledger, 'active_ranked': ranked,
           'quick_mode': [t for t in ranked if t['minutes'] <= 15],
           'unassigned': Y.get('unassigned', []),
           'loop': ['7am PC: refresh, full/maxed/timers checklist, dailies due now',
                    'Workday: active task(s) running (top of the ranked list)',
                    '3pm: cloud save, refresh, then cards one character at a time on the tablet']}
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
    L.append(f"- MOVE: {cd['move']['text']} [{cd['move']['src']}]")
    for q in cd['quick']: L.append(f"- QUICK: {q}")
    for t in cd['active']: L.append(f"- ACTIVE: {t['task']}" + (' · ' + '; '.join(t.get('notes', [])) if t.get('notes') else ''))
    L.append(f"- AFK: {cd['afk']['text']} [{cd['afk']['src']}] (save shows {cd['save_map']})")
    for f in cd['flags']: L.append(f"- FLAG {f}")
    for j in cd['jobs']:
        t = ', '.join(f"{k} {v}" for k, v in j['tiers'].items())
        L.append(f"- **{j['job']}**" + (f" ({t})" if t else '') + (f" · {j['note']}" if j.get('note') else '') + (f" · {j['state']}" if j.get('state') else ''))
        for f in j.get('findings', []): L.append(f"  - findings: {f}")
        for w in j.get('where', []): L.append(f"  - data: {w['system']} · Toolbox {', '.join(w['toolbox'])} · sources {w['sources']}")
        if j.get('maestro_behind'): L.append(f"  - behind: {', '.join(j['maestro_behind'])}")
        for s in j['subs']:
            L.append(f"  - {s['name']}: " + '; '.join(f"{i['label'][:80]} {i['cur']} -> {i['goal']}" + (' READY' if i['ready'] else '') for i in s['items']) + (f" (+{s['more']} more)" if s.get('more', 0) > 0 else ''))
    for l in cd['locked']: L.append(f"- LOCKED: {l['feature']} <- {l['unlock']}")
    for k, v in cd['talents'].items(): L.append(f"- Talents {k}: " + ', '.join(v))
    if cd['bags']: L.append('- Bags missing: ' + '; '.join(b[:50] for b in cd['bags']))
    L.append('')
open(os.path.join(R, 'plans', f'{stamp}.md'), 'w').write('\n'.join(L))
print(f"{len(cards)} cards, {sum(len(j['subs']) for c in cards for j in c['jobs'])} sub-systems, {len(alerts)} alerts -> plans/{stamp}.md")
