"""Buff Sources ledger (Zack 2026-11-17). Every stat AutoReview breaks into sources ("Sources of X",
"... multis and ...", "Account wide sources of ...", "Remaining sources of ...") -> one list per stat:
each source owned (done / value) or missing (current -> goal), routed to the owner character.
Diff vs the previous snapshot marks newly unlocked sources (stacking log).
Writes model/buffs.json + buffs.md. Usage: python3 model/buffs.py"""
import json, gzip, os, re, yaml
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAPS = sorted(p for p in os.listdir(os.path.join(R, 'snapshots')) if p[:1].isdigit())
stamp = open(os.path.join(R, 'snapshots', 'LATEST')).read().strip()
Y = yaml.safe_load(open(os.path.join(R, 'model', 'jobs.yaml')))
SRC = re.compile(r'^(Sources of|Account wide sources of|Remaining sources of)|multis and|Sources of', re.I)

# section -> owner characters (from jobs.yaml); lever routes override by label
sec_owner = {}
for n, cfg in Y['characters'].items():
    for j in cfg['jobs']:
        for e in j.get('sections', []):
            sec_owner.setdefault(e if isinstance(e, str) else e['s'], []).append(n)
routes = Y.get('lever_routes', [])
KEY = [(r'Schematic', 'Villagers'), (r'Land Rank|Exotic Market|Seed of', 'Farming'), (r'Cape Vine|Gallery|Nametag|Trophy', 'Gallery'), (r'^Owl', 'Owl'), (r'Family Bonus|Guild|Codex|Friend Bonus|Obol', '__account__'), (r'^Grimoire|Wraith|Death Bringer', 'The Grimoire'), (r'^Tesseract|Arcane', 'The Tesseract'), (r'^Compass|Wind Walker|Medallion', 'Compass'),
       (r'Sneaking|Pristine Charm|Jade', 'Sneaking'), (r'^Equinox', 'Equinox'), (r'Achievement', 'Achievements'), (r'Merit', 'Meritocracy'),
       (r'Atom|Collider', 'Atom Collider'), (r'Summoning|Winner', 'Summoning'), (r'Breeding|Shiny|Pet ', 'Breeding'), (r'Meal|Cooking|Kitchen|Ribbon', 'Cooking'),
       (r'Farming|Crop|Bean', 'Farming'), (r'Gaming|Superbit|Snail', 'Gaming'), (r'Divinity|God', 'Divinity'), (r'Prayer', 'Prayers'), (r'Statue', 'Statues'),
       (r'Artifact|Sailing|Captain', 'Sailing'), (r'Upgrade Vault|^Vault', 'Upgrade Vault'), (r'Gem Shop', 'Gem Shop'), (r'Event Shop', 'Event Shop'),
       (r'Spelunk', 'Spelunking'), (r'Research|Grid', 'Research'), (r'Sushi', 'Sushi Station'), (r'Jelly', 'Jelly Operator'), (r'Emperor', 'Emperor'),
       (r'Shrine', 'Buildings'), (r'Salt Lick', 'Salt Lick'), (r'Library|Book', 'Library'), (r'Arcade', 'Arcade'), (r'Sigil', 'Sigils'), (r'Refinery|Salt', 'Refinery'),
       (r'Trap|Critter', 'Trapping'), (r'Worship|Totem', 'Prayers'), (r'Royal|Guardian', 'Royal Armory'), (r'Kattlekruk|Set bonus', 'Armor Sets'),
       (r'Bribe', 'Bribes'), (r'Star Sign|Seraph|Silkrode', 'Star Signs'), (r'Hole|Cavern|Villager|Monument|Opal', 'Villagers'), (r'Bubble', 'Bubbles'), (r'Vial', 'Vials'),
       (r'Stamp', 'Stamps'), (r'Card', 'Cards'), (r'Legend Talent', 'Legend Talents'), (r'Coral', 'Coral Reef'), (r'Zenith', 'Zenith Market'), (r'Clam', 'Clam Work')]
def owner(sec, label):
    for r in routes:
        if re.search(r['m'], label, re.I): return r['owner']
    for rx, s2 in KEY:
        if re.search(rx, label, re.I):
            if s2 == '__account__': return 'account'
            if sec_owner.get(s2): return sec_owner[s2][0]
    o = sec_owner.get(sec)
    return o[0] if o else 'account'

def leaves(node, path=''):
    for a in node.get('items', []):
        if 'items' in a: yield from leaves(a, path + '/' + a.get('tab', ''))
        else: yield path, a
    for t in node.get('tabs', []): yield from leaves(t, path + '/' + str(t.get('tab', '')))

def build(st):
    rv = json.load(gzip.open(os.path.join(R, 'snapshots', st, 'review.json.gz')))
    stats = []
    for w in rv['worlds']:
        for s in w['sections']:
            for g in s['groups']:
                gn = g.get('name', '')
                if not SRC.search(gn): continue
                rows = []
                for path, a in leaves(g):
                    lab = re.sub(r'\s+', ' ', a.get('label', ''))
                    if not lab: continue
                    cur, goal = str(a.get('cur', '')), str(a.get('goal', ''))
                    done = bool(a.get('completed')) or goal in ('✔',) or (cur and cur == goal)
                    info = not done and not cur and not goal
                    rows.append({'source': lab[:160], 'tab': path.strip('/')[:60], 'cur': cur, 'goal': goal,
                                 'state': 'owned' if done else ('info' if info else 'missing'),
                                 'owner': owner(s['name'], lab)})
                stats.append({'stat': gn[:120], 'section': s['name'], 'owned': sum(r['state'] == 'owned' for r in rows),
                              'missing': sum(r['state'] == 'missing' for r in rows), 'rows': rows})
    return stats

cur = build(stamp)
prev = [s for s in SNAPS if s < stamp]
newly = []
if prev:
    try:
        old = {(s['section'], s['stat'].split('(')[0], r['source'][:60]): r['state'] for s in build(prev[-1]) for r in s['rows']}
        for s in cur:
            for r in s['rows']:
                k = (s['section'], s['stat'].split('(')[0], r['source'][:60])
                if r['state'] == 'owned' and old.get(k) == 'missing': newly.append(f"{s['stat'][:50]}: {r['source'][:80]}")
    except Exception as e:
        newly = [f'diff failed: {e}']
by_owner = {}
for s in cur:
    for r in s['rows']:
        if r['state'] == 'missing': by_owner.setdefault(r['owner'], []).append(f"{s['stat'][:45]} · {r['source'][:90]} {r['cur']} -> {r['goal']}")
out = {'stamp': stamp, 'vs': prev[-1] if prev else None, 'stats': cur, 'newly_owned': newly, 'missing_by_owner': by_owner}
json.dump(out, open(os.path.join(R, 'model', 'buffs.json'), 'w'), indent=1)
L = [f"# Buff sources · save {stamp} vs {out['vs']}", f"{len(cur)} stats, {sum(s['owned'] for s in cur)} sources owned, {sum(s['missing'] for s in cur)} missing", '']
if newly: L += ['## Newly unlocked since last save'] + [f"- {x}" for x in newly] + ['']
for s in cur:
    L.append(f"## {s['section']}: {s['stat']}  ({s['owned']} owned / {s['missing']} missing)")
    for r in s['rows']:
        mark = {'owned': '[x]', 'missing': '[ ]', 'info': ' - '}[r['state']]
        L.append(f"- {mark} {r['source'][:110]}" + (f" {r['cur']} -> {r['goal']}" if r['state'] == 'missing' else '') + (f" · {r['owner']}" if r['state'] == 'missing' else ''))
    L.append('')
open(os.path.join(R, 'model', 'buffs.md'), 'w').write('\n'.join(L))
print(L[1], '| newly owned:', len(newly), '| owners with missing:', {k: len(v) for k, v in by_owner.items()})
