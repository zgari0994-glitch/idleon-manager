"""Prayers planner: fluid per-character loadouts (task-driven, creator rules), soul-safe upgrade buys, Royal Sampler print-day plan.

Inputs: snapshots/<LATEST>/toolbox/prayers.txt (Toolbox prayers page), chars.json (equipped), jobs.yaml (afk/active tasks), model/printer.json.
Every rule cites its creator source; mapping a rule onto a character uses that character's own task text (jobs.yaml).
"""
import json, re
from pathlib import Path
import yaml
import spend

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / 'snapshots' / (ROOT / 'snapshots' / 'LATEST').read_text().strip()
SOULS = ['Forest Soul', 'Dune Soul', 'Rooted Soul', 'Frigid Soul', 'Squishy Soul']
# other uses of souls (sweep of parsed systems): stamps (materials), vials (Sippy Soul uses Forest Soul), bubbles, refinery salt chain (Zack)
SOUL_RESERVE_SHARE = 0.05   # my read: a prayer buy may use at most 5% of that soul type until the salt/stamp/vial soul needs are modeled
RULES = [  # (when the task text matches, prayer, action, source)
    (r'trap', 'Skilled Dimwit + Unending Energy', 'equip while PLACING traps, unequip after (snapshotted)', 'Griffy (traps clip)'),
    (r'trap|critter', 'Shiny Snitch', 'only while trapping (bundles of shiny critters; curse lowers shiny chance)', 'prayer text'),
    (r'giant|weekly', 'giant-monster prayers', 'remove before the weekly reset so giant-kill quests still count', 'Griffy 2026-11'),
    (r'kill|death note|zow|chow|crystal|push|combat|fight', 'Midas Minded / Big Brain Time', 'drop rate / class EXP when you overkill the map (curse raises mob HP)', 'Griffy (drop rate/EXP prayers until 200 crit)'),
    (r'active', 'Unending Energy', '+Class & Skill EXP, but AFK caps at 10h: only when you claim within 10h', 'prayer text'),
]


def _n(s):
    s = s.replace(',', '').strip()
    m = re.match(r'([\d.]+)\s*([KMBT])?$', s)
    return float(m.group(1)) * {None: 1, 'K': 1e3, 'M': 1e6, 'B': 1e9, 'T': 1e12}[m.group(2)] if m else None


def build():
    t = (SNAP / 'toolbox' / 'prayers.txt').read_text()
    bal = {k: _n(v) for k, v in re.findall(r'\n(' + '|'.join(SOULS) + r')\n([^\n]+)', t)}
    pr = []
    for m in re.finditer(r'\n([A-Z][A-Za-z ]+)\nLv (\d+) / (\d+)\n(Maxed\n)?Bonus\n([^\n]+)\nCurse\n([^\n]+)\n(.*?)(?=\n[A-Z][A-Za-z ]+\nLv \d+ / |\Z)', t, re.S):
        body = m.group(7)
        cost = re.search(r'Cost to max\n([^\n]+)\n([^\n]+)\n/\n([^\n]+)', body)
        have = _n(cost.group(2)) if cost else None
        cur = next((k for k, v in bal.items() if have and v and abs(v - have) / v < 0.01), None)
        pr.append({'name': m.group(1).strip(), 'lv': int(m.group(2)), 'max': int(m.group(3)), 'maxed': bool(m.group(4)), 'bonus': m.group(5), 'curse': m.group(6),
                   'equipped_by': re.findall(r'Autis\w+', body), 'to_max': _n(cost.group(1)) if cost else None, 'next': _n(cost.group(3)) if cost else None,
                   'soul': cur, 'unlock': (re.search(r'Unlocks at\n([^\n]+)', body) or [0, ''])[1]})
    waves = {}
    try:
        wt = (SNAP / 'toolbox' / 'worship.txt').read_text()
        waves = {a.strip(): int(b) for a, b in re.findall(r'\n([A-Z][A-Za-z ]+)\n\t(\d+)\t', wt)}
    except Exception:
        pass
    for p in pr:
        m = re.match(r'Wave (\d+) in (.+)', p['unlock'] or '')
        if m and m.group(2).strip() in waves:
            p['wave_need'], p['totem'], p['wave_now'] = int(m.group(1)), m.group(2).strip(), waves[m.group(2).strip()]
            p['locked'] = p['wave_now'] < p['wave_need']
    Y = yaml.safe_load(open(ROOT / 'model' / 'jobs.yaml'))
    tasks = {}
    for cn, c in Y['characters'].items():
        txt = ' '.join([str((c.get('afk') or {}).get('text', ''))] + [j['job'] for j in c.get('jobs', [])] + [str(a) for a in c.get('active', [])])
        tasks[cn] = txt
    ch = {c['character_name']: c for c in json.load(open(SNAP / 'chars.json'))['characters']}
    # AutoReview tier targets
    import gzip
    r = json.load(gzip.open(SNAP / 'review.json.gz')); targets = {}
    for w in r['worlds']:
        for s in (w.get('sections') or []):
            if s.get('name') == 'Prayers':
                for g in s['groups']:
                    for it in g['items']:
                        for x in it.get('items', []):
                            targets[x['label']] = (x['cur'], x['goal'], g['name'])
    opts = []
    for p in pr:
        if p['maxed'] or not p['next'] or not p['soul'] or p.get('locked'): continue
        tg = targets.get(p['name'])
        opts.append({'item': f"{p['name']} {p['lv']}/{p['max']}", 'currency': p['soul'], 'balance': bal.get(p['soul']), 'cost': p['next'],
                     'gain_pct': None, 'stat': p['bonus'][:40], 'weight': 2 if tg and 'Recommended' in tg[2] else 1,
                     'note': (f"AutoReview {tg[0]} -> {tg[1]}" if tg else '')})
    ranked = spend.rank(opts)
    printer = {}
    try: printer = json.load(open(ROOT / 'model' / 'printer.json'))
    except Exception: pass
    out = {'snapshot': SNAP.name, 'souls': bal, 'prayers': pr, 'tasks': tasks, 'equipped': {k: v.get('equipped_prayers') for k, v in ch.items()},
           'ranked': ranked, 'targets': targets, 'gold_relic': printer.get('gold_relic')}
    json.dump(out, open(ROOT / 'model' / 'prayers.json', 'w'), indent=1)
    return out


def char_lines(o, c):
    eq = o['equipped'].get(c) or []
    task = o['tasks'].get(c, '')
    L = [f"Equipped now: {', '.join(eq) or 'none'}. Task: {task[:90]}"]
    for pat, pray, act, src in RULES:
        if re.search(pat, task, re.I): L.append(f"{pray}: {act} ({src})")
    if 'The Royal Sampler' in eq: L.append("Royal Sampler: keep until print day (it only unequips by clearing samples).")
    if 'Shiny Snitch' in eq and not re.search(r'trap|critter', task, re.I):
        L.append("CHECK: Shiny Snitch is on, but this character's task isn't trapping. It only pays while trapping and its curse lowers shiny chance (prayer text).")
    if 'Skilled Dimwit' in eq and re.search(r'kill|death note|zow|chow|push|fight', task, re.I) and not re.search(r'skill|lab|cook|farm|spelunk|divinity', task, re.I):
        L.append("CHECK: Skilled Dimwit (+skill efficiency, -skill EXP) on a fighting task.")
    return L


def card_lines(o):
    L = []
    rs = next((p for p in o['prayers'] if p['name'] == 'The Royal Sampler'), None)
    gd = o.get('gold_relic') or [None, None, None]
    if rs:
        L.append(f"PRINT DAY plan (Royal Sampler, worn by {len(rs['equipped_by'])}): it unequips only by clearing samples, so dropping it = full resample day. "
                 f"Pulse 2026-10: statue week is the yearly resample time (copper prints first). Gold Relic is {gd[0]}/{gd[1]} days and resets on a sample, so print day = statue week or day 100.")
        L.append("Before print day (Griffy): book talents first (2026-10), Voidwalker in speedrun form while sampling (2026-08), keep Maestro's skills above the others (Right Hand, 2026-09), "
                 "multi-resource bubbles (Sploosh Sploosh, Bug Squared, Molto Loggo, 2026-07), Island stamp toward 90% sample size (2026-10), extra sample slots (gems, 2026-10). "
                 "Griffy 2026-10: the Royal Sampler EXP curse is additive (10x EXP becomes ~9.4x, not 4x), so waiting costs less than the -87% reads.")
    L.append('Souls: ' + ', '.join(f"{k.split()[0]} {spend.h(v)}" for k, v in o['souls'].items()) +
             f". Reserve rule (my read until salt/stamp/vial soul needs are modeled): a prayer buy may use at most {int(SOUL_RESERVE_SHARE * 100)}% of that soul type. Souls also feed stamps, vials (Sippy Soul), bubbles and your salt chain.")
    buys = []
    for cur, ops in o['ranked'].items():
        for x in ops:
            if x['afford'] and x['share'] is not None and x['share'] <= SOUL_RESERVE_SHARE: buys.append(x)
    buys.sort(key=lambda x: (-x.get('weight', 1), x['share']))
    if buys: L.append('Safe prayer buys now (inside the reserve, AutoReview-recommended first): ' + ' > '.join(spend.fmt(x) for x in buys[:8]))
    held = [x for ops in o['ranked'].values() for x in ops if x['afford'] and x['share'] and x['share'] > SOUL_RESERVE_SHARE]
    if held: L.append('Held (over the reserve): ' + ', '.join(spend.fmt(x) for x in held[:4]))
    try:
        prot = json.load(open(ROOT / 'model' / 'protect.json'))
        import rates
        for x in buys + held:
            if x['currency'] in prot:
                pr_ = prot[x['currency']]
                L.append(f"  {x['currency']} is on the greenstack protect list ({pr_['owned']:,.0f}, {pr_['need_for_stack']:,.0f} short of 10M). "
                         f"Buying {x['item'].split(' ')[0]} spends {x['cost']:,.0f}; {rates.replace_line(x['currency'], x['cost'])}. Replace via {pr_['replace']}.")
    except Exception:
        pass
    lk = [p for p in o['prayers'] if p.get('locked')]
    if lk: L.append('Locked prayers (worship wave needed, so not buyable yet): ' + '; '.join(f"{p['name']} needs wave {p['wave_need']} in {p['totem']} (best {p['wave_now']})" for p in lk))
    L.append('Loadouts are fluid: each card shows its own prayers vs that character\'s task (AFK or active). Change prayers when the task changes.')
    return L


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)
    for c in o['equipped']: print(c, char_lines(o, c))
