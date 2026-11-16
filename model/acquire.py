"""Acquisition map: missing trophies, capes, nametags, hats + open achievements, with bonus and source.
Facts: save (via AutoReview parser) + idleon.wiki snapshots in sources/ (refresh rarely: they're static).
Source kinds: in-game vs paid (gem shop / bundle) vs event (limited time). -> model/acquire.md + acquire.json"""
import json, gzip, os, re, html
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AR = '/home/claude/work/ar/mysite'
snap = os.path.join(R, 'snapshots', open(os.path.join(R, 'snapshots', 'LATEST')).read().strip())
S = json.load(gzip.open(os.path.join(snap, 'systems.json.gz')))['systems']
mech = json.load(open(os.path.join(R, 'model', 'mechanics.json')))
hats_w = json.load(gzip.open(os.path.join(R, 'sources', 'wiki_hats.json.gz')))
ach_w = json.load(gzip.open(os.path.join(R, 'sources', 'wiki_achievements.json.gz')))

def kind(src):
    s = src.lower()
    paid = any(k in s for k in ('gem shop', 'bundle', 'pack'))
    event = any(k in s for k in ('event', 'anniversary', 'choco box', 'summer', 'spring', 'golden gift', 'potluck', 'giftmas', 'halloween', 'twitch', 'edible coin', 'luckulyte', 'royal egg', 'cropfall', 'valen', 'easter', 'santa', 'christmas'))
    if paid and event: return 'paid/event'
    if paid: return 'paid'
    if event: return 'event'
    if src.strip() in ('', '—'): return 'unknown'
    return 'in-game'

def cell(row, prefix):
    for c in row:
        if c.startswith(prefix): return c[len(prefix):].strip()
    return ''

# Wiki trophy/cape/nametag rows captured 2026-11-16 (Trophies, Capes, Nametags pages)
WIKI = json.load(open(os.path.join(R, 'sources', 'wiki_cosmetics.json')))

out = {'trophies': [], 'capes': [], 'nametags': [], 'hats': [], 'achievements': []}
for name in mech['gallery_missing'].get('trophy', []):
    w = WIKI['trophies'].get(name, {}); out['trophies'].append({'name': name, **w, 'kind': kind(w.get('source', ''))})
for name in mech['capes_missing']:
    w = WIKI['capes'].get(name, {}); out['capes'].append({'name': name, **w, 'kind': kind(w.get('source', ''))})
for name in mech['gallery_missing'].get('nametag', []):
    w = WIKI['nametags'].get(name, {})
    src = w.get('source', '')
    if name.startswith('Tome ') and src in ('', '—'): src = 'Tome rank reward (Tome score tiers)'
    out['nametags'].append({'name': name, **w, 'source': src, 'kind': kind(src) if not name.startswith('Tome ') else 'in-game'})

# Hats: owned codes -> names via AutoReview's item data
txt = open(os.path.join(AR, 'consts', 'consts_item_data.py')).read()
code2name = {}
for m in re.finditer(r'displayName="([^"]+)".{0,1500}?addNewEquip\("(EquipmentHats[^"]+)"', txt):
    code2name[m.group(2)] = m.group(1).replace('_', ' ')
owned = {code2name.get(c, c).lower() for c in S['hat_rack']['codes']}
prem = {r[0]: r for r in hats_w.get('Premium_Helmets', []) if r}
for r in hats_w['Hat_Rack'][1:]:
    name = r[0]
    if name.lower() in owned: continue
    bonus = ', '.join(x for x in (cell(r, 'Bonus'), cell(r, 'Second Bonus')) if x and x != '—')
    pr = prem.get(name, [])
    src = next((c[6:] for c in pr if c.startswith('Source')), '') if pr else ''
    out['hats'].append({'name': name, 'bonus': bonus, 'source': src or 'see wiki', 'kind': kind(src)})

# Achievements: open ones with wiki description/reward
def clean(s):
    s = html.unescape(html.unescape(s or ''))
    s = re.sub(r'\d+px\|link=.*?">', '', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)\]\]', r'\1', s)
    s = re.sub(r'\bGe\b', 'gems', s)
    return re.sub(r'\s+', ' ', s).strip()
wk = {html.unescape(a['Name']).lower(): a for a in ach_w}
for n in mech['achievements_open']:
    a = wk.get(n.lower(), {})
    out['achievements'].append({'name': n, 'how': clean(a.get('Description'))[:220], 'reward': clean(a.get('Reward'))[:120],
                                'notes': clean(a.get('Notes'))[:160]})

json.dump(out, open(os.path.join(R, 'model', 'acquire.json'), 'w'), indent=1)
L = ['# Acquisition map (wiki sources, captured 2026-11-16)', '',
     'kind: in-game = obtainable by playing; paid = gem shop/bundle; event = limited-time; trophies/nametags count only in a Gallery showcase slot.', '']
for key, title in (('trophies', 'Trophies'), ('capes', 'Capes'), ('nametags', 'Nametags'), ('hats', 'Hats (rack)')):
    L.append(f"## {title} missing ({len(out[key])})")
    for x in sorted(out[key], key=lambda x: (x['kind'] != 'in-game', x['name'])):
        L.append(f"- **{x['name']}** [{x['kind']}] {x.get('bonus','')} · {x.get('source','')}")
    L.append('')
L.append(f"## Achievements open ({len(out['achievements'])})")
for a in out['achievements']:
    L.append(f"- **{a['name']}**: {a['how']} → {a['reward'] or 'reward n/a'}" + (f" ({a['notes']})" if a['notes'] else ''))
open(os.path.join(R, 'model', 'acquire.md'), 'w').write('\n'.join(L) + '\n')
print({k: len(v) for k, v in out.items()}, 'hat names mapped', len(code2name))
