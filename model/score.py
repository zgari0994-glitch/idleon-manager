"""Task Score + card job picker (Zack 2026-11-27). Formula: docs/scoring.md. Weights: model/score_weights.yaml.
Card job order (never overrides the Laws):
  1. Zack's plan (brain/plans.yaml, labeled "Zack's plan")
  2. Law 2 duties (every owned system, every day)
  3. masterclass duty (jobs.yaml masterclass:). Top-10 need -> NOW alongside Spelunking. A Death Bringer drops to
     Spelunking only when Grimoire is in a good spot (not a top-10 need).
  4. top-scored task in that character's systems (Reach doubles on the goal chain). No personal goal -> main goal (Law 3).
Night watch: an active-only task beating Cat's overnight frogs 2 pulls in a row -> Cat's card lists the top 3, "reconsider?". Flag only.
  python3 score.py          dry run, one line per character, writes nothing
  python3 score.py --top    account top 10s (quick < 10 min, long 10+ min) with inputs
build() -> model/score.json; record(save) -> state/nightwatch.json (pull only)."""
import json, sys
from pathlib import Path
import yaml
from data import load

ROOT = Path(__file__).resolve().parent.parent
D = load(); SAVE = D.stamp
W = yaml.safe_load((ROOT / 'model' / 'score_weights.yaml').read_text())
Y = yaml.safe_load((ROOT / 'model' / 'jobs.yaml').read_text())
P = yaml.safe_load((ROOT / 'brain' / 'plans.yaml').read_text())
NW = ROOT / 'state' / 'nightwatch.json'
NICK = {'Autiszemo': 'Zemo', 'Autistocat': 'Cat', 'Autisticles': 'Ticles', 'Autistastic': 'Tastic', 'Autistabish': 'Bish',
        'Autistacular': 'Tacular', 'Autistotle': 'Totle', 'Autistomatic': 'Matic', 'Autistronaut': 'Naut', 'Autistopher': 'Topher',
        'Autistachio': 'Tachio'}


def J(n):
    try: return json.load(open(ROOT / 'model' / f'{n}.json'))
    except Exception: return {}


def age_h():
    try: return float(D.age_hours)
    except Exception: return 0.0


_NEEDS = None
def needs():
    global _NEEDS
    if _NEEDS is None:
        import priority as PR
        _NEEDS = PR.build().get('needs', [])
    return _NEEDS


def need_rank(section):
    return next((i for i, x in enumerate(needs(), 1) if x['section'] == section), None)


def goal():
    try:
        import goalpick as G; return G._state().get('goal', 'Spelunking')
    except Exception: return 'Spelunking'


def goal_target():
    try:
        import goalpick as G; return G.target(goal())[0]
    except Exception: return goal()


def _secs(j): return [s if isinstance(s, str) else s.get('s') for s in j.get('sections', [])]


def owner_of(section):
    """First character whose job lists the section (or names it). jobs.yaml is the only owner source."""
    if not section: return None
    for n, cfg in Y['characters'].items():
        for j in cfg.get('jobs', []):
            if section in _secs(j) or section.lower() in j['job'].lower(): return n
    return None


def conf(src):
    s = str(src).lower(); v = [c for k, c in W['confidence'].items() if k in s]
    c = max(v) if v else W['default_confidence']
    a = age_h()
    return c * max(0.5, 1 - (a - 24) / 96) if a > 24 else c


def score(t):
    g, sec = goal(), t.get('section', '')
    if 'impact' in t: imp = t['impact']
    elif sec == g: imp = W['goal_impact']
    else:
        n = next((x for x in needs() if x['section'] == sec), None)
        top = max([x['score'] for x in needs()] or [1])
        imp = n['score'] / top if n else W['default_impact']
    reach = 1 + 0.5 * (W.get('unblocks') or {}).get(sec, 0)
    if sec == g or sec in (W.get('goal_chain') or []): reach *= 2
    c = conf(t.get('src', '')); urg = 1.5 if t.get('urgent') else 1.0
    eff = max(1.0, t.get('minutes', 30)) / 30 + 0.1 * t.get('wait_h', 0) + t.get('cost_share', 0)
    raw = imp * reach * c * urg / eff
    t['inputs'] = {'impact': round(imp, 2), 'reach': round(reach, 2), 'conf': round(c, 2), 'urgency': urg, 'effort': round(eff, 2)}
    t['value'] = imp * reach * c * urg   # effort-free: night watch compares a full night either way
    t['score'] = round(100 * raw / (raw + W['K']), 1)
    return t


def plan_task_ids():
    s = set()
    for p in P['plans']:
        t = p.get('task'); s |= set(t if isinstance(t, list) else [t] if t else [])
    return s


def plans_for(name):
    return [p for p in P['plans'] if name in (p['who'] if isinstance(p['who'], list) else [p['who']])]


def dynamic():
    """Data-driven tasks (text from this save, owner from jobs.yaml)."""
    T = []
    try:
        import compass as CP; c = CP.plan()
        T.append({'id': 'compass_active', 'section': 'Compass', 'active': True, 'minutes': 30, 'task': c['active_line'], 'src': 'save + idleon.wiki Wind Walker (fan, flagged)'})
    except Exception as e: print('compass plan failed:', e, file=sys.stderr)
    T.append({'id': 'tesseract_active', 'section': 'The Tesseract', 'active': True, 'minutes': 30,
              'task': "Short daytime Tesseract session + Arcanist Form map push: kill the map's crystal mobs before the timer to open the next map",
              'src': 'zack rule + Griffy N5yJ4-tZLbY 00:52 (active-only)'})
    gr = J('grimoire')
    if gr.get('next_unlock'):
        T.append({'id': 'grimoire_bones', 'section': 'The Grimoire', 'minutes': 60,
                  'task': f"Wraith Form bones at {gr['best_mobs'][0][0] if gr.get('best_mobs') else 'the best bones mob'}: {gr['next_unlock'][1] - gr['total']} upgrade levels to {gr['next_unlock'][0]}",
                  'src': 'Griffy: max AFK gains before spending bones'})
    em = J('emperor')
    if em and str(em.get('attempts', '0')).split(' / ')[0] != '0':
        T.append({'id': 'emperor', 'section': 'Emperor', 'active': True, 'minutes': 20, 'task': f"Emperor showdowns: {em['attempts']} attempts, push past {em.get('best')}", 'src': 'Griffy ypb7kpQov30 05:36 + Pulse 6JgdYbiEKus'})
    sp = J('spelunking')
    if sp:
        T.append({'id': 'spelunk_goal', 'section': 'Spelunking', 'minutes': 60, 'task': f"Spelunking: {goal_target()}", 'src': 'save (goalpick.py)'})
    for t in T: t['owner'] = owner_of(t['section'])
    return T


def tasks():
    skip, T = plan_task_ids(), []
    for t in Y.get('active_tasks', []):
        if t['id'] in skip: continue
        t = dict(t)
        if t.get('owner') in (None, 'auto'): t['owner'] = owner_of(t.get('section')) or 'every character'
        T.append(t)
    T += dynamic()
    have = {(t['owner'], t.get('section')) for t in T}
    for i, n in enumerate(needs(), 1):
        for o in n['owners']:
            if o.startswith('Autis') and (o, n['section']) not in have:
                T.append({'id': f"need:{n['section']}", 'owner': o, 'section': n['section'], 'minutes': 60, 'src': 'AutoReview tiers (priority.py)',
                          'task': f"Push {n['section']} {n['cur'].replace('T ', 'tier ')} -> {n['goal'].replace('T ', 'tier ')}" if n.get('cur') else f"Push {n['section']}",
                          'why': f"#{i} need: {n['why']}"})
    return [score(t) for t in T]


def duties(name):
    mc = {m['section'] for m in Y.get('masterclass', []) if m['who'] == name}
    return [j['job'] for j in Y['characters'][name].get('jobs', []) if not (set(_secs(j)) & mc)]


def masterclass(name):
    out = []
    for m in Y.get('masterclass', []):
        if m['who'] != name: continue
        r = need_rank(m['section']); now = bool(r and r <= 10)
        tag = f"NOW, alongside {goal()} (#{r} need)" if now else (f"daily check (#{r} need)" if r else "daily check (not a ranked need)")
        out.append({'step': 'masterclass', 'text': f"Masterclass: {m['do']}. {tag}", 'why': m['why'], 'src': m['src'], 'now': now})
    return out


def grimoire_ok():
    r = need_rank('The Grimoire'); return r is None or r > 10


def is_db(name): return any(m['who'] == name and m['section'] == 'The Grimoire' for m in Y.get('masterclass', []))


def night_watch(T=None):
    T = T if T is not None else tasks()
    frog = score({'id': 'cat_frogs', **W['night_watch']})['value']
    act = [t for t in T if t.get('active') or t.get('section') in W['active_only_sections']]
    return frog, sorted([t for t in act if t['value'] > frog], key=lambda t: -t['value'])[:3]


def _nw_state():
    try: return json.loads(NW.read_text())
    except Exception: return {'last_save': None, 'streak': 0, 'top3': []}


def record(save=SAVE):
    st = _nw_state()
    if st.get('last_save') == save: return st
    frog, beat = night_watch()
    st.update(last_save=save, streak=(st.get('streak', 0) + 1) if beat else 0, frog=round(frog, 3),
              top3=[f"{NICK.get(t['owner'], t['owner'])}: {t['task']} ({t['value']:.2f} vs frogs {frog:.2f})" for t in beat])
    NW.write_text(json.dumps(st, indent=1)); return st


def cat_flag():
    st = _nw_state()
    if st.get('streak', 0) >= 2:
        return f"Night watch: {len(st['top3'])} active task(s) beat the frogs {st['streak']} pulls in a row. Reconsider? " + ' | '.join(st['top3'])
    return None


def pick(name, T=None):
    T = T if T is not None else tasks()
    steps = []
    for p in plans_for(name):
        txt = p['do'] + (f"; then {p['then']}" if p.get('then') else '')
        if p.get('rule') == 'best_dr_rg': txt += " (whichever of Tastic / Matic has the higher drop rate: per-character DR isn't in the parser, check in game)"
        steps.append({'step': 'plan', 'text': f"Zack's plan ({p['date']}): {txt}", 'why': p.get('finish') or p.get('gap') or 'Zack set it', 'src': 'zack'})
    if name == P['slots'].get('overnight_active') and cat_flag():
        steps.append({'step': 'flag', 'text': cat_flag(), 'why': 'flag only, never switched', 'src': 'night watch'})
    d = duties(name)
    if d: steps.append({'step': 'duties', 'text': 'Law 2 duties, every day: ' + ', '.join(d), 'why': 'focus never means neglect', 'src': 'jobs.yaml'})
    steps += masterclass(name)
    mine = [t for t in T if t['owner'] == name and not str(t.get('slot')) == 'morning']
    hold = is_db(name) and not grimoire_ok()
    if hold: mine = [t for t in mine if t.get('section') != 'Spelunking']
    mine.sort(key=lambda t: -t['score'])
    rank = sorted(T, key=lambda t: -t['score'])
    if mine:
        t = mine[0]; r = rank.index(t) + 1
        steps.append({'step': 'scored', 'text': t['task'], 'why': t.get('why') or f"top task in his systems, score {t['score']} (#{r} of {len(T)})", 'src': t['src'], 'score': t['score']})
    if not plans_for(name) and not hold:
        steps.append({'step': 'goal', 'text': f"Main goal (Law 3, no personal goal): {goal()}", 'why': goal_target(), 'src': 'goalpick.py'})
    if hold: steps.append({'step': 'hold', 'text': f"No Spelunking until Grimoire is in a good spot (Grimoire is the #{need_rank('The Grimoire')} need)", 'why': 'masterclass rule', 'src': 'zack'})
    return steps


def card_lines(name, T=None):
    return [f"{i}. {s['text']} ({s['why']}) [{s['src']}]" for i, s in enumerate(pick(name, T), 1)]


QUICK_MIN = 10   # Zack 2026-11-27: two top 10s, quick (< 10 min) and long (10+ min); same score, no floor


def top10(T, quick):
    return sorted([t for t in T if (t.get('minutes', 30) < QUICK_MIN) == quick], key=lambda t: -t['score'])[:10]


def build():
    T = tasks()
    frog, beat = night_watch(T)
    o = {'save': SAVE, 'age_h': round(age_h(), 1), 'goal': goal(), 'picks': {n: pick(n, T) for n in Y['characters']},
         'top10_quick': [{k: t.get(k) for k in ('owner', 'task', 'section', 'score', 'minutes', 'inputs', 'src')} for t in top10(T, quick=True)],
         'top10_long': [{k: t.get(k) for k in ('owner', 'task', 'section', 'score', 'minutes', 'inputs', 'src')} for t in top10(T, quick=False)],
         'night_watch': {'frog_value': round(frog, 3), 'beats_now': [t['task'] for t in beat], 'state': _nw_state()}}
    json.dump(o, open(ROOT / 'model' / 'score.json', 'w'), indent=1)
    return o


if __name__ == '__main__':
    T = tasks()
    print(f"save {SAVE} ({age_h():.1f}h old) | goal {goal()}: {goal_target()}")
    if '--top' in sys.argv:
        for q, lbl in ((True, f'quick (under {QUICK_MIN} min)'), (False, f'long ({QUICK_MIN}+ min)')):
            print(f'-- top 10 {lbl}')
            for t in top10(T, q): print(f"{t['score']:5} {t.get('minutes', 30):>3}m {NICK.get(t['owner'], t['owner'])}: {t['task']} {t['inputs']} [{t['src']}]")
    else:
        for n in Y['characters']:
            st = pick(n, T); h = st[0]
            rest = ' || '.join(s['text'][:110] for s in st[1:] if s['step'] not in ('duties',))
            print(f"{NICK[n]}: {h['text']} | why: {h['why']} | src: {h['src']}" + (f"\n    then: {rest}" if rest else ''))
        frog, beat = night_watch(T)
        print(f"night watch: frogs {frog:.2f}; beating now: {[(NICK.get(t['owner']), t['task'][:50], round(t['value'], 2)) for t in beat]}")
