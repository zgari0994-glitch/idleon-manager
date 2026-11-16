"""Daily plan: one card per character in slot order.
For each job: its AutoReview tier + the next open targets (AutoReview order for now; Griffy-weighted rinse
replaces the ordering later). Writes plans/<save>.md and plans/latest.json (dashboard feed).
Usage: python model/plan.py [N targets per job, default 3]"""
import json, gzip, os, sys, yaml, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
stamp = open(os.path.join(R, 'snapshots', 'LATEST')).read().strip()
snap = os.path.join(R, 'snapshots', stamp)
review = json.load(gzip.open(os.path.join(snap, 'review.json.gz')))
chars = json.load(open(os.path.join(snap, 'chars.json')))['characters']
Y = yaml.safe_load(open(os.path.join(R, 'model', 'jobs.yaml')))
N = int(sys.argv[1]) if len(sys.argv) > 1 else 3
meta = review['meta']
RN = json.load(open(os.path.join(R, 'rinse', 'latest.json')))
SCORE = {(r['section'], r['label']): r['score'] for r in RN['rows']}
secs = {s['name']: s for w in review['worlds'] for s in w['sections']}
by_name = {c['character_name']: c for c in chars}
SK = [k for k in chars[0]['skills'] if k != 'Combat' and 'Lol' not in k]
best = {s: max(chars, key=lambda c: c['skills'].get(s, 0)) for s in SK}

def leaves(g, gname):
    if 'tabs' in g:
        for t in g['tabs']:
            yield from leaves(t, t.get('tab') or gname)
        return
    for a in g.get('items', []):
        if 'items' in a:
            for b in a['items']:
                yield gname, b
        else:
            yield gname, a

def targets(sec_name, who):
    s = secs.get(sec_name)
    if not s or s.get('completed'):
        return []
    out = []
    for g in s['groups']:
        if g.get('completed') or g.get('informational'):
            continue
        for gname, a in leaves(g, g.get('name', '')):
            if a.get('completed') or a.get('informational') or not (a['cur'] or a['goal']):
                continue
            # tabbed (per-character) groups: keep only this character's tab when tabs are names
            if gname in by_name and gname != who:
                continue
            pre = a['label'].split(':', 1)[0].strip()
            if pre in by_name and pre != who:  # per-character rows (e.g. Post Office boxes) stay on their own card
                continue
            out.append({'section': sec_name, 'group': gname[:80], 'label': a['label'][:140],
                        'cur': a['cur'], 'goal': a['goal'], 'optional': bool(a.get('optional') or g.get('optional'))})
    seen, ded = set(), []
    for t in out:  # next step only
        if t['label'] not in seen:
            seen.add(t['label']); t['score'] = SCORE.get((sec_name, t['label']), 0); ded.append(t)
    return sorted(ded, key=lambda t: -t['score'])

def tier(n):
    s = secs.get(n)
    if not s: return 'n/a'
    if s.get('completed'): return 'done'
    t = s['tier'] or '-'
    return 'untiered' if t == '0/0' else t

# weekly jobs: show from weekly reset until confirmed in state/confirmed.json
import datetime as _dt
tp = os.path.join(snap, 'timers.json')
week_start = None
if os.path.exists(tp):
    T = json.load(open(tp)); w = T['resets'].get('Weekly', '')
    m = re.findall(r'(\d+)([dhm])', w); wsecs = sum(int(n) * {'d': 86400, 'h': 3600, 'm': 60}[u] for n, u in m)
    cap = _dt.datetime.fromisoformat(T['captured_utc'].replace('Z', '+00:00'))
    week_start = (cap + _dt.timedelta(seconds=wsecs) - _dt.timedelta(days=7)).strftime('%Y-%m-%d')
CONF = json.load(open(os.path.join(R, 'state', 'confirmed.json')))
cards = []
for name, cfg in Y['characters'].items():
    c = by_name[name]
    card = {'slot': c['character_index'] + 1, 'name': name, 'class': c['class_name'], 'level': c['combat_level'],
            'afk': f"W{c['world']} map {c['current_map_index']}", 'jobs': [], 'flags': []}
    for j in cfg['jobs']:
        jd = {'job': j['job'], 'basis': j.get('basis'), 'tiers': {s: tier(s) for s in j.get('sections', [])}, 'next': []}
        for s in j.get('sections', []):
            jd['next'] += targets(s, name)[:N]
        jd['next'] = sorted(jd['next'], key=lambda t: -t['score'])[:N]
        if j.get('rule') == 'maestro':
            behind = [f"{s} {c['skills'].get(s,0)}/{best[s]['skills'][s]} ({best[s]['character_name']})"
                      for s in SK if best[s]['skills'][s] > c['skills'].get(s, 0)]
            jd['maestro_behind'] = behind
            card['flags'].append(f"Maestro: behind in {len(behind)}/{len(SK)} skills")
        if j.get('note'):
            jd['note'] = j['note']
        if j.get('weekly'):
            done = name in CONF.get(week_start or '', {}).get(j['weekly'], [])
            jd['weekly'] = {'week_start': week_start, 'done': done}
            if not done:
                card['flags'].append(f"Weekly {j['weekly']}: not confirmed for week of {week_start or '?'}")
        card['jobs'].append(jd)
    for s in (Y.get('extra_light') or {}).get(name, []):
        card['jobs'].append({'job': s, 'basis': 'light', 'tiers': {s: tier(s)}, 'next': targets(s, name)[:1]})
    if cfg.get('plan'):
        card['flags'].append('PLAN: ' + cfg['plan'])
    cards.append(card)

os.makedirs(os.path.join(R, 'plans'), exist_ok=True)
json.dump({'meta': meta, 'cards': cards}, open(os.path.join(R, 'plans', 'latest.json'), 'w'), indent=1)
L = [f"# Daily plan · game save {meta['game_save_et']} · ordering: Griffy rinse (Thigh Gap v2)", '']
for cd in sorted(cards, key=lambda x: x['slot']):
    L.append(f"## {cd['slot']}. {cd['name']} · {cd['class']} {cd['level']} · AFK {cd['afk']}")
    for f in cd['flags']:
        L.append(f"- ⚑ {f}")
    for j in cd['jobs']:
        t = ', '.join(f"{k} {v}" for k, v in j['tiers'].items())
        L.append(f"- **{j['job']}**" + (f" ({t})" if t else '') + (f" · {j['note']}" if j.get('note') else ''))
        for x in j['next']:
            L.append(f"  - [{x['score']}] {x['label']}: {x['cur']} → {x['goal']}")
    L.append('')
open(os.path.join(R, 'plans', f'{stamp}.md'), 'w').write('\n'.join(L))
print('\n'.join(L)[:6000])
