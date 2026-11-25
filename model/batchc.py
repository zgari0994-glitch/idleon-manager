"""Batch C planners (Zack 2026-11-19). Each system: build_<x>() + lines_<x>(o). Thin wrapper modules (emperor.py, islands.py ...) register in plan.py."""
import re
from tbhelp import tb, ar_items, n, save
G = lambda t, k: (re.search(re.escape(k) + r'\n([^\n]+)', t) or [None, None])[1]
_DC = None


def _fmt(t, v):
    # game text: { = the value, } = 1 + value/100 as a multiplier
    try: v = float(v)
    except (TypeError, ValueError): return t.replace('{', '').replace('}', '')
    return t.replace('{', f"{v:g}").replace('}', f"{1 + v / 100:.2f}")


def _D():
    global _DC
    if _DC is None:
        from data import load
        _DC = load()
    return _DC


def build_emperor():
    # Zack 2026-11-25: Toolbox parser numbers; owner Autistocat (Arcane Cultist: Griffy 2026-08 + Pulse 2026-10-31)
    E = _D().system('emperor')
    nx = [(b['bonus'].replace('_', ' '), '', f"{b['level']}") for b in E['upcomingBonuses']]
    return save('emperor', {'best': E['highestEmperorShowdown'], 'attempts': f"{E['attempts']} / {E['maxAttempts']}", 'next_bonus': None, 'bonuses': nx, 'daily': E.get('dailyAttempts')})


def lines_emperor(o):
    best = int(o['best']); L = []
    a = o['attempts'].split(' / ')
    if int(a[0]) > 0: L.append(f"TOP: use your {a[0]} Emperor attempts on Autistocat and push past showdown {best}. Pulse: stand on the small platform next to the boss and auto attack so the skulls bounce; Skull + Aura only, 2nd-page damage talents, boost foods. Big pushes are best saved for statue week.")
    nxt = sorted([(int(x), b) for b, tot, x in o['bonuses'] if str(x).isdigit()])[:4]
    if nxt: L.append('Coming up: ' + ', '.join(f"showdown {lv}: {b}" for lv, b in nxt) + '.')
    return L


def build_islands():
    I = _D().system('islands')
    return save('islands', {'Bottles': f"{I['bottles']:,.0f}", 'Unclaimed trash days': I.get('numberOfDaysAfk'), 'Garbage to collect': str(I.get('trashPerDaysAfk') or 0),
                            'Garbage': None, 'Mobs waiting': '0', 'Shimmer': I.get('allShimmerBonus'), 'crystal_days': None})


def lines_islands(o):
    d = []
    if o['Garbage to collect'] and o['Garbage to collect'] != '0': d.append(f"collect {o['Garbage to collect']} garbage")
    if o['Mobs waiting'] and o['Mobs waiting'] != '0': d.append(f"fight the {o['Mobs waiting']} crystal mobs (they drop candy)")
    return [f"TOP: Islands: {' and '.join(d)}."] if d else []


def build_arcade():
    A = _D().system('arcade')
    rot = [x for x in A['shop'] if x.get('active')]
    return save('arcade', {'balls': A['balls'], 'full': False, 'gold': A['goldBalls'], 'ups': [(_fmt(x['bonusName'].replace('_', ' '), x['bonus']), x['level'], None) for x in rot],
                           'rotation': ', '.join(x['bonusName'].replace('_', ' ') for x in rot)})


def lines_arcade(o):
    L = []
    if o['full']: L.append("TOP: the Arcade is full, claim your balls.")
    rot = [u for u in o['ups'] if u[0] in o['rotation']]
    nm = lambda a: re.sub(r'^\+?[\d.]+[x%]? ', '', a)
    if o['gold']: L.append(f"{o['gold']:,.0f} gold balls. On rotation now: {', '.join(nm(a) for a, lv, c in o['ups'])} (check costs in game).")
    return L


def build_owl():
    O = _D().system('owl')
    ups = [(u['name'].replace('_', ' '), u['level'], u['cost']) for u in O['upgrades'] if u.get('unlocked')]
    return save('owl', {'feathers': O['feathers'], 'mega': len([m for m in O['megaFeathers'] if m]) if isinstance(O['megaFeathers'], list) else O['megaFeathers'], 'ups': ups})


def lines_owl(o):
    aff = [u for u in o['ups'] if u[2] and u[2] <= o['feathers']]
    return [f"Owl: buy all {len(aff)} upgrades, you have way more feathers than they cost."] if aff else []


def build_killroy():
    K = _D().system('killroy')
    return save('killroy', {'skulls': K['skulls'], 'weeks': [], 'perm': [(u['description'].replace('_', ' '), u['cost']) for u in K['permanentUpgrades'] if u.get('cost') is not None],
                            'rooms': K.get('rooms'), 'kills': K.get('totalKills')})


def lines_killroy(o):
    L = []
    if o.get('rooms'): L.append(f"Killroy: {o['rooms']} rooms this week.")
    aff = [x for x in o['perm'] if x[1] <= o['skulls']]
    if aff: L.append(f"With {o['skulls']} skulls you can buy: " + ', '.join(a.split(',')[0].split('!')[0][:40] for a, c in aff[:4]) + '.')
    L.append('Get 2,000 kills in one room to finish an Equinox challenge (best so far 1,296).')
    return L


def build_hole():
    H = _D().system('caverns')
    st = H['studies']['studies'] if isinstance(H.get('studies'), dict) else []
    return save('hole', {'caverns': None, 'ready': [], 'soon': [], 'schematics': H.get('cosmoSchematics'), 'schem_aff': [],
                         'studies': [(x['name'].replace('_', ' '), x['level'], x.get('active')) for x in st], 'opals': H.get('totalOpalsFound')})


def lines_hole(o):
    L = []
    if o['ready']: L.append(f"TOP: Hole study level ready on {', '.join(a for a, b, c in o['ready'])}, bump it.")
    if o['soon']: L.append('Next ones ready: ' + ', '.join(f"{a} in {t}" for a, b, c, t in o['soon'][:3]) + '.')
    if o['schem_aff']: L.append('Engineer schematics you can afford: ' + ', '.join(a for a, c in o['schem_aff'][:4]) + '.')
    return L


def build_slab():
    L = _D().system('slab')
    return save('slab', {'Looted items': L['lootedItems'], 'Missing items': L['missingItems'], 'Greenstacks': L['greenStackedCount'], 'Slab bonus multi': None})


def lines_slab(o):
    return [f"Slab: {o['Missing items']} items you've never picked up. Each new one raises the slab bonus."]


def build_beanstalk():
    # beanstalk food ranks/owned are not broken out by Toolbox's parser yet: AutoReview lines carry it
    tier, items = ar_items('Beanstalk')
    foods = [(i['label'][:40], 0, float(str(i.get('cur') or 0).replace(',', '') or 0) if str(i.get('cur', '')).replace(',', '').replace('.', '').isdigit() else 0,
              float(str(i.get('goal')).replace(',', '')) if str(i.get('goal', '')).replace(',', '').replace('.', '').isdigit() else 0) for i in items]
    return save('beanstalk', {'foods': [f for f in foods if f[3]]})


def lines_beanstalk(o):
    f = sorted([x for x in o['foods'] if x[2] < x[3]], key=lambda x: -(x[2] / x[3]))
    return ['Beanstalk, closest to the next rank: ' + ', '.join(f"{a} ({ow / nd:.0%})" for a, r, ow, nd in f[:4]) + '.'] if f else []


def build_capevine():
    C = _D().system('cape_vine')
    return save('capevine', {'Capes collected': f"{C['totalCapes']} / {C['totalEligibleCapes']}", 'Bonus multi': C['bonusMulti'], 'Golden Vines': C['goldenVines'],
                             'Next Golden Vine': f"class level {C['nextGoldenVineClassLevel']}"})


def lines_capevine(o):
    return [f"{o['Capes collected']} capes on the vine. The next golden vine comes at {o['Next Golden Vine'].lower()}."]


def build_shops():
    # event shop is not in Toolbox's parser (AutoReview has it); ballot + Meritocracy from the parser
    V = _D().system('ballot')
    cl = lambda x: str(x).replace('_', ' ')
    sb, sm = V.get('selectedBonus') or {}, V.get('selectedMeritocracyBonus') or {}
    tier, items = ar_items('Event Points Shop')
    return save('shops', {'points': None, 'rotation': None, 'items': [], 'ar_event': [i['label'][:60] for i in items if i.get('cur') != i.get('goal')][:4],
                          'ballot_next': None, 'merit_next': None,
                          'ballot_now': _fmt(cl(sb.get('0', '')), sb.get('1')), 'merit_now': _fmt(cl(sm.get('description', '')), sm.get('bonus')),
                          'vote_multi': V.get('voteMulti'), 'merit_multi': V.get('meritocracyMult')})


def lines_shops(o):
    L = [f"This week's Ballot bonus: {o['ballot_now']} (x{o['vote_multi']}). Meritocracy: {o['merit_now']} (x{o['merit_multi']})."]
    if o.get('ar_event'): L.append('Event Shop (AutoReview): ' + '; '.join(o['ar_event'][:3]) + '.')
    return L


def build_tome():
    T = _D().system('tome')
    pts = T['totalPoints']; up = sorted([t for t in T['tops'] if t and t > pts])
    return save('tome', {'points': f"{pts:,.0f}", 'rank': T.get('top'), 'gap': f"{up[0] - pts:,.0f}" if up else None})


def lines_tome(o):
    return [f"Tome is at {o['points']} points, {o['gap']} short of the next bracket. Every other card raises it."]


def build_maint():
    R = _D().system('rift')
    cur = R['list'][R['currentRift']] if R['currentRift'] < len(R['list']) else None
    task = str(cur['task']).replace('_', ' ') if cur else ''
    nxt = [(x['monsterName'], i + 1, str(x['task']).replace('_', ' ')) for i, x in enumerate(R['list'][R['currentRift'] + 1:R['currentRift'] + 3], start=R['currentRift'])]
    return save('maint', {'rift': f"{R['currentRift']} / {len(R['list'])}", 'cur': (cur['monsterName'], R['currentRift'], task, f"{R.get('currentProgress')}") if cur and 'CANNOT PROGRESS' not in task else None,
                          'next': [x for x in nxt if 'CANNOT PROGRESS' not in x[2]]})


def lines_maint(o):
    L = []
    if o['cur']: L.append(f"Rift {o['rift'].split(' / ')[0]}: {o['cur'][2].split('.')[0]} ({o['cur'][3]}).")
    if o['next']: L.append('After that: ' + '; '.join(c.split('.')[0] for a, b, c in o['next'][:2]) + '.')
    return L


