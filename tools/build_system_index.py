"""Phase 1b: system index. Every system -> Toolbox page(s) (+ guide line) -> raw/parsed key -> AutoReview section(s)
-> transcript slug (+ tagged rows, index chunks) -> owner(s) from jobs.yaml -> findings file.
Code-built from the sources; ALIAS holds the hand mappings. Writes model/system_index.yaml + .md."""
import json, gzip, os, re, glob, csv, collections, yaml
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
stamp = open(os.path.join(R, 'snapshots', 'LATEST')).read().strip()
systems = json.load(gzip.open(os.path.join(R, 'snapshots', stamp, 'systems.json.gz')))
systems = sorted(systems.get('systems', systems).keys())
review = json.load(gzip.open(os.path.join(R, 'snapshots', stamp, 'review.json.gz')))
AR = [s['name'] for w in review['worlds'] for s in w['sections']]
guide = open(os.path.join(R, 'sources', 'creators', 'idleon-toolbox-guide.md')).read().splitlines()
pages = {}
for i, line in enumerate(guide, 1):
    for p in re.findall(r'(?:account/)?(world-\d/[a-z-]+|class-specific/[a-z-]+|misc/[a-z-]+|task-board/[a-z-]+|prem-currency/[a-z-]+|clickers/[a-z-]+|tools/[a-z-]+)', line):
        pages.setdefault(p, i)
idx = json.load(gzip.open(os.path.join(R, 'sources', 'creators', 'transcript_index.json.gz')))
chunks = collections.Counter(s for c in idx for s in c['s'])
tagged = collections.Counter()
for p in glob.glob(os.path.join(R, 'sources', 'creators', '*', 'tags', '*.csv')):
    for r in csv.DictReader(open(p)): tagged[r['system']] += 1
J = yaml.safe_load(open(os.path.join(R, 'model', 'jobs.yaml')))
owners = collections.defaultdict(set)
for n, cfg in J['characters'].items():
    for j in cfg['jobs']:
        for e in j.get('sections', []):
            owners[e if isinstance(e, str) else e['s']].add(n)
findings = {os.path.basename(f)[:-3] for f in glob.glob(os.path.join(R, 'sources', 'findings', '*.md'))}
norm = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
# hand mappings: system key -> (AR sections, transcript slug, toolbox page tails)
ALIAS = {
 'alchemy_bubbles': (['Bubbles'], 'bubbles', ['bubbles']), 'alchemy_vials': (['Vials'], 'vials', ['vials']),
 'alchemy_cauldrons': ([], 'cauldrons_liquids', ['cauldrons']), 'alchemy_p2w': (['Pay2Win'], 'cauldrons_liquids', ['cauldrons']),
 'arcade': (['Arcade'], 'arcade', ['arcade-shop']), 'ballot': (['Bonus Ballot'], None, ['vote-ballot']),
 'construction_buildings': (['Buildings'], 'buildings', ['buildings', 'construction']), 'caverns': (['Villagers', 'Shallow Caverns', 'Glowshroom Tunnels', 'Underground Overgrowth'], 'hole', ['hole']),
 'gemshop': (['Gem Shop'], 'gem_shop', ['gem-shop']), 'event_points_shop': (['Event Shop'], None, ['event-shop']),
 'lab_bonuses': ([], 'lab', ['laboratory']), 'lab_chips': ([], 'lab', ['laboratory']), 'lab_jewels': ([], 'lab', ['laboratory']), 'lab_mainframe': ([], 'lab', ['laboratory']),
 'saltlick': (['Salt Lick'], 'salt_lick', ['salt-lick']), 'spelunk': (['Spelunking'], 'spelunking', ['spelunking']),
 'sushi_station': (['Sushi Station'], 'sushi', ['sushi-station']), 'trapping': (['Trapping'], 'traps', ['traps']),
 'vault': (['Upgrade Vault'], 'upgrade_vault', ['upgrade-vault']), 'menagerie': (['Luminous Menagerie'], 'menagerie', ['menagerie']),
 'killroy': (['Killroy'], 'killroy', ['killroy']), 'royal_armory': (['Royal Armory'], 'royal_armory', ['royal-armory']),
 'tesseract': (['The Tesseract'], 'tesseract', ['tesseract']), 'grimoire': (['The Grimoire'], 'grimoire', ['grimoire']),
 'library': (['Library'], 'library', ['library']), 'storage': (['Storage'], 'storage', ['storage']),
 'meritocracy': (['Meritocracy'], 'merits', []), 'merits': ([], 'merits', ['merits']), 'star_signs': (['Star Signs'], None, ['constellations']),
 'forge_upgrades': (['Smithing'], None, ['forge', 'anvil']), 'armor_sets': (['Armor Sets'], None, ['armor-smithy']),
 'drop_rate': (['Drop Rate'], 'drop_rate', []), 'greenstacks': (['Greenstacks', 'Endangered Greenstacks'], 'greenstacks', ['storage']),
 'world_progress': (['Pinchy high', 'Pinchy low', 'Pinchy all'], 'w7_push', []), 'tome': ([], 'tome', ['tome']),
 'statues': (['Statues'], 'statues', ['statues']), 'cards': (['Cards'], 'cards', ['card-search']),
 'death_note': (['Death Note'], 'death_note', ['death-note']), 'prayers': (['Prayers'], 'prayers', ['prayers']),
 'worship': ([], 'worship', ['worship']), 'refinery': (['Refinery'], 'refinery', ['refinery']), 'printer': (['Sampling'], 'printer', ['printer', 'sampling-companion']),
 'meals': (['Cooking'], 'cooking', ['cooking']), 'cooking': (['Cooking'], 'cooking', ['cooking']),
}
def default(k):
    ar = [s for s in AR if norm(s) == norm(k) or norm(s) == norm(k.replace('_', ' '))]
    slug = k if k in chunks or k in tagged else None
    return ar, slug, [k.replace('_', '-')]
out = {}
for k in systems:
    ar, slug, tails = ALIAS.get(k, default(k))
    tb = [p for p in pages if any(p.endswith('/' + t) for t in tails)]
    own = sorted(set().union(*[owners.get(s, set()) for s in ar])) if ar else []
    out[k] = {'toolbox': [f"{p} (guide L{pages[p]})" for p in tb] or ['GAP: no Toolbox page mapped'],
              'autoreview': ar or ['none (AutoReview does not rate it)'], 'raw_key': k,
              'transcripts': {'slug': slug, 'tagged_rows': tagged.get(slug, 0), 'index_chunks': chunks.get(slug, 0)} if slug else 'GAP: no slug',
              'owners': own or ['unassigned in jobs.yaml'],
              'findings': [f for f in findings if slug and f.startswith(slug)] or []}
yaml.safe_dump(out, open(os.path.join(R, 'model', 'system_index.yaml'), 'w'), sort_keys=True, allow_unicode=True, width=200)
gaps = {'no_toolbox': [k for k, v in out.items() if v['toolbox'][0].startswith('GAP')],
        'no_owner': [k for k, v in out.items() if v['owners'] == ['unassigned in jobs.yaml'] and v['autoreview'][0] != 'none (AutoReview does not rate it)'],
        'thin_sources': [k for k, v in out.items() if isinstance(v['transcripts'], dict) and v['transcripts']['tagged_rows'] < 10]}
L = [f"# System index · {len(out)} systems · save {stamp}", '', '| system | Toolbox | AutoReview | tagged/chunks | owners |', '|---|---|---|---|---|']
for k, v in out.items():
    t = v['transcripts']; ts = f"{t['tagged_rows']}/{t['index_chunks']}" if isinstance(t, dict) else 'gap'
    L.append(f"| {k} | {', '.join(x.split(' (')[0] for x in v['toolbox'])} | {', '.join(v['autoreview'])} | {ts} | {', '.join(v['owners'])} |")
L += ['', '## Gaps'] + [f"- {g}: {', '.join(v)}" for g, v in gaps.items()]
open(os.path.join(R, 'model', 'system_index.md'), 'w').write('\n'.join(L) + '\n')
print(len(out), 'systems;', {g: len(v) for g, v in gaps.items()})
print('\n'.join(L[-3:])[:2500])
