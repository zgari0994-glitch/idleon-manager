"""Prayers planner: fluid per-character loadouts (task-driven, creator rules), soul-safe upgrade buys, Royal Sampler print-day plan.

Inputs: data.py (Toolbox parser), chars.json (equipped), jobs.yaml (afk/active tasks), model/printer.json.
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
    # Zack 2026-11-25: Toolbox parser numbers (model/data.py); next cost = Toolbox's calcPrayerCost (added by the parse harness)
    from data import load
    D = load()
    SOULN = {'Soul1': 'Forest Soul', 'Soul2': 'Dune Soul', 'Soul3': 'Rooted Soul', 'Soul4': 'Frigid Soul', 'Soul5': 'Squishy Soul', 'Soul6': 'Oozie Soul', 'Soul7': 'Breezy Soul'}
    bal, pr = {}, []
    eq = {c['name']: [p.replace('_', ' ') for p in (c.get('activePrayers') or []) if isinstance(p, str)] for c in D.characters}
    waves = {t['name'].replace('_', ' '): t.get('maxWave', 0) for t in D.system('worship') if t.get('name')}
    for p in D.system('prayers'):
        nm = p['name'].replace('_', ' '); soul = SOULN.get(p.get('soul'), p.get('soul'))
        bal[soul] = p.get('totalAmount')
        pr.append({'name': nm, 'lv': p['level'], 'max': p['maxLevel'], 'maxed': p['level'] >= p['maxLevel'], 'bonus': p['effect'].replace('_', ' '), 'curse': p['curse'].replace('_', ' '),
                   'equipped_by': [c for c, ps in eq.items() if nm in ps], 'to_max': None, 'next': p.get('nextCost'), 'soul': soul,
                   'unlock': f"Wave {p.get('unlockWave')} in {p.get('unlockZone')}"})
    for p in pr:
        m = re.match(r'Wave (\d+) in (.+)', p['unlock'] or '')
        if m and m.group(2).strip() in waves:
            p['wave_need'], p['totem'], p['wave_now'] = int(m.group(1)), m.group(2).strip(), waves[m.group(2).strip()]
            p['locked'] = p['wave_now'] < p['wave_need']
    Y = yaml.safe_load(open(ROOT / 'model' / 'jobs.yaml'))
    tasks = {}
    for cn, c in Y['characters'].items():
        txt = ' '.join([' '.join(str(a.get('text', a) if isinstance(a, dict) else a) for a in (c.get('afk') if isinstance(c.get('afk'), list) else [c.get('afk') or {}]))] + [j['job'] for j in c.get('jobs', [])] + [str(a) for a in c.get('active', [])])
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
    L = [f"Prayers on: {', '.join(eq) or 'none'}."]
    for pat, pray, act, src in RULES:
        if re.search(pat, task, re.I): L.append(f"{pray}: {act}.")
    if 'Shiny Snitch' in eq and not re.search(r'trap|critter', task, re.I):
        L.append("Take off Shiny Snitch, it only helps while trapping and it lowers shiny chance otherwise.")
    if 'Skilled Dimwit' in eq and re.search(r'kill|death note|zow|chow|push|fight', task, re.I) and not re.search(r'skill|lab|cook|farm|spelunk|divinity', task, re.I):
        L.append("Skilled Dimwit doesn't fit a fighting job, swap it.")
    if 'The Royal Sampler' in eq: L.append('Leave Royal Sampler on until print day.')
    return L


def card_lines(o):
    L = []
    gd = o.get('gold_relic') or [None, None, None]
    L.append(f"Print day: Royal Sampler only comes off by clearing samples, so it waits for print day. Pulse uses statue week; Gold Relic is at {gd[0]} of {gd[1]} days.")
    L.append('Griffy before print day: book talents first, and the Royal Sampler EXP hit is smaller than it looks.')
    buys = []
    for cur, ops in o['ranked'].items():
        for x in ops:
            if x['afford'] and x['share'] is not None and x['share'] <= SOUL_RESERVE_SHARE: buys.append(x)
    buys.sort(key=lambda x: (-x.get('weight', 1), x['share']))
    if buys: L.append('Prayer upgrades you can buy without eating into your soul reserve: ' + ', '.join(x['item'].split(' ')[0] + ' ' + x['item'].split(' ')[1] for x in buys[:5]) + '.')
    try:
        prot = json.load(open(ROOT / 'model' / 'protect.json'))
        for x in buys:
            if x['currency'] in prot: L.append(f"Careful: {x['currency']} is close to a greenstack, buying {x['item'].split(' ')[0]} spends some of it.")
    except Exception:
        pass
    lk = [p for p in o['prayers'] if p.get('locked')][:3]
    if lk: L.append('Locked prayers: ' + '; '.join(f"{p['name']} needs {p['totem']} wave {p['wave_need']} (best {p['wave_now']})" for p in lk) + '.')
    L.append("Set each character's prayers to what they're doing today, the cards show each one.")
    return L


if __name__ == '__main__':
    o = build()
    for l in card_lines(o): print(l)
    for c in o['equipped']: print(c, char_lines(o, c))
