"""Sweep creator tags for advice filed under the wrong game system (e.g. god links tagged outside Divinity).

Each row is scored per system from its statement + subsystem text:
  game entity names (AutoReview consts + model jsons) = 3, system keywords = 1 each.
Rule: current system has no evidence and another scores >= 3 (>= 2 for catch-all slugs) -> MOVE.
      current has evidence but another beats it by >= 3 -> ALSO (row is indexed under both).
Writes sources/findings/resection.json (applied by model/guidance.py) + resection.md (report).
"""
import csv, glob, json, os, re, collections

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EN = json.load(open(os.path.join(R, 'sources', 'findings', 'entity_names.json')))
GENERIC = {'apple', 'egg', 'pie', 'corn', 'salad', 'cheese', 'onion', 'leek', 'orange', 'pizza', 'donut', 'soda', 'kiwi fruit', 'pumpkin', 'cookies',
           'blue', 'green', 'purple', 'nullo', 'trove', 'pea pod', 'eel', 'mutton', 'sawdust', 'pretzel', 'cabbage', 'canopy', 'riceball', 'dango',
           'potion', 'big muscle', 'envelope pile', 'distilled water', 'dense water', 'talent point', 'talent points', 'bargain tag', 'carpenter',
           'level up gift', 'cheap shot', 'kattlekruk'}
CATCH_ALL = {'general', 'characters', 'talent_points', 'damage', 'drop_rate', 'money', 'account_structure', 'daily_routine', 'speedrun', 'quests',
             'w7_push', 'class_exp', 'masterclass', 'class_choice', 'dashboard', 'random_events', 'storage'}
GODS = ['Snehebatu', 'Arctis', 'Nobisect', 'Harriep', 'Goharut', 'Omniphau', 'Purrmep', 'Flutterbis', 'Kattlekruk', 'Bagur']
KW = {
    'divinity': ['divinity', 'god rank', 'coral kid', 'singularity', 'blessing', 'minor link', 'major link', 'meditat', 'altar'] + [g.lower() for g in GODS if g != 'Kattlekruk'],
    'sailing': ['sailing', 'captain', 'boat', 'loot pile', 'artifact', 'world\'s end', 'the maw'],
    'cooking': ['kitchen', 'meal', 'plate', 'spice', 'ribbon', 'cooking', 'ladle'],
    'farming': ['crop', 'beans', 'night market', 'day market', 'exotic', 'land rank', 'overgrowth', 'gmo', 'farming', 'megacrop'],
    'breeding': ['shiny', 'fence', 'egg', 'breeding', 'breed ', 'territory', 'pet arena', 'breedability', 'incubator'],
    'printer': ['3d print', 'printer', 'sample', 'printing'],
    'bubbles': ['bubble'], 'vials': ['vial'], 'sigils': ['sigil'], 'statues': ['statue', 'onyx'], 'prayers': ['prayer'],
    'atom_collider': ['atom', 'collider', 'particle'], 'stamps': ['stamp'], 'refinery': ['refinery', 'salts'],
    'construction': ['cog', 'construction', 'build rate', 'flag'], 'lab': ['lab ', 'mainframe', 'lab chip', 'jewel'],
    'worship': ['worship', 'totem', 'tower defen'], 'summoning': ['summoning', 'endless summon', 'essence'],
    'sneaking': ['sneaking', 'ninja', 'jade', 'emporium'], 'spelunking': ['spelunk', 'lore boss', 'amber', 'delve'],
    'hole': ['the hole', 'cavern', 'villager', 'opal', 'well '], 'gaming': ['gaming', 'bits', 'palette', 'superbit', 'sprout', 'log book'],
    'menagerie': ['menagerie', 'lumi'], 'research': ['research grid', 'research exp', 'grid square'], 'dungeons': ['dungeon', 'flurbo'],
    'compass': ['compass', 'nomadic', 'tempest'], 'grimoire': ['grimoire', 'bones', 'wraith'], 'death_note': ['death note', 'deathnote', 'chow', 'zow'],
    'equinox': ['equinox', 'dream'], 'tesseract': ['tesseract', 'tachyon'], 'upgrade_vault': ['upgrade vault', 'vault upgrade'],
    'salt_lick': ['salt lick'], 'legend_talents': ['legend talent'], 'killroy': ['killroy', 'kilroy'], 'sushi': ['sushi'],
    'emperor': ['emperor'], 'coral_reef': ['coral reef'], 'owl': ['owl', 'feather'], 'kangaroo': ['kangaroo'], 'tome': ['tome'],
    'arcade': ['arcade'], 'traps': ['trap', 'critter'], 'constellations': ['constellation', 'star sign'], 'library': ['library', 'talent book', 'checkout'],
    'merits': ['merit'], 'royal_armory': ['armory'], 'minehead': ['minehead'], 'jelly_operator': ['jelly operator'], 'the_button': ['the button'],
    'ballot': ['ballot', 'vote'], 'gem_shop': ['gem shop'], 'event_shop': ['event shop'], 'cards': [' card', 'card set'],
    'slab': ['slab'], 'rift': ['rift'], 'achievements': ['achievement'], 'forge': ['forge'], 'anvil': ['anvil'], 'weekly_boss': ['weekly boss'],
    'beanstalk': ['beanstalk', 'golden food'], 'greenstacks': ['greenstack'], 'clam_work': ['clam'], 'bubba': ['bubba'], 'glimbo': ['glimbo'],
    'zenith_market': ['zenith market'], 'cauldrons_liquids': ['cauldron', 'liquid'], 'armor_smithy': ['armor set', 'smithy'],
}
ENT = {'bubbles': 'bubbles', 'vials': 'vials', 'sigils': 'sigils', 'statues': 'statues', 'prayers': 'prayers', 'atom_collider': 'atom_collider',
       'cooking': 'cooking', 'sailing': 'sailing'}


def entity_terms():
    t = {}
    for k, slug in ENT.items():
        for n in EN.get(k, []):
            n2 = n.lower().split(' - ')[0].strip()
            if len(n2) >= 5 and n2 not in GENERIC: t.setdefault(slug, set()).add(n2)
    t.setdefault('divinity', set()).update(g.lower() for g in GODS if g != 'Kattlekruk')   # Kattlekruk is also a W5 boss + gear set
    try:
        import importlib, sys
        sys.path.insert(0, '/home/claude/work/ar/mysite')
        w2 = importlib.import_module('consts.consts_w2')
        for cat in w2.alchemy_description:
            for x in cat:
                if x and x[0] != 'BUBBLE':
                    n = x[0].replace('_', ' ').lower()
                    if len(n) >= 6 and n not in GENERIC: t['bubbles'].add(n)
    except Exception:
        pass
    return t


def score(text, ents):
    s = collections.Counter(); why = collections.defaultdict(list)
    for slug, names in ents.items():
        for n in names:
            if re.search(r'\b' + re.escape(n) + r'\b', text): s[slug] += 3; why[slug].append(n)
    if 'kattlekruk' in text and re.search(r'link|blessing|god\b|divinity|bubble', text): s['divinity'] += 3; why['divinity'].append('kattlekruk (god context)')
    for slug, kws in KW.items():
        for k in kws:
            if k in text: s[slug] += 1; why[slug].append(k)
    return s, why


def main():
    ents = entity_terms()
    out, rep = {}, collections.Counter(); ex = collections.defaultdict(list)
    for f in glob.glob(os.path.join(R, 'sources', 'creators', '*', 'tags', '*.csv')):
        for r in csv.DictReader(open(f, encoding='utf-8')):
            cur = r['system']
            if cur in ('none', ''): continue
            text = ' ' + (r.get('statement', '') + ' | ' + r.get('subsystem', '')).lower() + ' '
            s, why = score(text, ents)
            if not s: continue
            best, bs = s.most_common(1)[0]
            if best == cur: continue
            cs = s.get(cur, 0)
            need = 2 if cur in CATCH_ALL else 3
            act = 'move' if cs == 0 and bs >= need else ('also' if bs >= cs + 3 else None)
            if not act: continue
            key = f"{r['video_id']}|{r['t_start']}|{r.get('subsystem', '')}"
            out[key] = {'to': best, 'act': act, 'from': cur, 'why': why[best][:4]}
            rep[(cur, best, act)] += 1
            if len(ex[(cur, best)]) < 2: ex[(cur, best)].append(r['statement'][:120])
    json.dump(out, open(os.path.join(R, 'sources', 'findings', 'resection.json'), 'w'), indent=0)
    L = [f"# Resection sweep: {len(out)} rows re-filed ({sum(v for (a, b, c), v in rep.items() if c == 'move')} moved, "
         f"{sum(v for (a, b, c), v in rep.items() if c == 'also')} also-filed)\n"]
    by_to = collections.Counter()
    for (a, b, c), v in rep.items(): by_to[b] += v
    L.append('## Gained per system\n' + '\n'.join(f"- {b}: +{v}" for b, v in by_to.most_common()))
    L.append('\n## Biggest flows (from -> to, move/also, examples)')
    for (a, b, c), v in rep.most_common(40):
        L.append(f"- {a} -> {b} ({c}) {v}: " + ' / '.join(ex[(a, b)]))
    open(os.path.join(R, 'sources', 'findings', 'resection.md'), 'w').write('\n'.join(L))
    print(L[0]); print('\n'.join(L[1].split('\n')[:25]))


if __name__ == '__main__':
    main()
