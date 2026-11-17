"""Free, code-only transcript index (no AI). Splits every transcript into ~60s chunks and tags each chunk
with the systems it mentions (same slugs as handoff/tagging_spec.md). Query with:
  python3 tools/transcript_index.py build
  python3 tools/transcript_index.py find cooking [--creator griffybit] [--since 2025-10] [--words "speed|ribbon"] [--top 15]
Output of find: creator, date, video, timestamp, matched systems, the chunk text (short)."""
import csv, glob, gzip, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, 'sources', 'creators', 'transcript_index.json.gz')
KW = {
 'stamps': r'stamp', 'bubbles': r'bubble|cauldron|nblb|no bubble left', 'vials': r'\bvials?\b', 'sigils': r'sigil',
 'cauldrons_liquids': r'liquid|water droplet|nitrogen|cranium cooking', 'arcade': r'arcade|gold balls?', 'killroy': r'kill ?roy',
 'printer': r'printer|\bprints?\b|sampl', 'refinery': r'refinery|\bsalts?\b', 'atom_collider': r'atom collider|\batoms?\b|particles',
 'equinox': r'equinox', 'buildings': r'construction|building|trimmed slot|\bcogs?\b', 'death_note': r'death ?note|\bzows?\b|\bchows?\b|super chow|\bwows?\b',
 'worship': r'worship|totem|\bsouls?\b|tower defen[cs]e', 'prayers': r'prayer', 'traps': r'\btraps?\b|trapping|critter', 'salt_lick': r'salt lick',
 'library': r'library|talent book|checkout', 'cooking': r'cooking|\bmeals?\b|kitchen|ribbon|cooking speed', 'breeding': r'breeding|shiny|\bpets?\b|spice|territory|fence',
 'lab': r'\blab\b|laboratory|\bchips?\b|jewels?', 'rift': r'\brift\b', 'tome': r'\btome\b', 'cape_vine': r'cape vine|\bcapes?\b',
 'sailing': r'sailing|artifact|captain|\bboats?\b', 'divinity': r'divinity|\bgods?\b|blessing|minor link', 'gaming': r'gaming|superbit|mutation|palette|snail|fertili[sz]er|imports?\b',
 'hole': r'\bhole\b|cavern|villager|opals?|\bwell\b|motherlode|\bden\b|bravery|\bbell\b|\bharp\b|\blamp\b|\bhive\b|grotto|justice|\bjars?\b|evertree|wisdom monument|gambit|temple|polonai|kaipu|cosmos|minau|bolaia|schematic',
 'slab': r'\bslab\b', 'farming': r'farming|crops?\b|land rank|exotic market|night market|beans?\b', 'sneaking': r'sneaking|ninja|jade|gemstone|pristine|charms?\b',
 'summoning': r'summoning|familiar|essence|endless', 'beanstalk': r'beanstalk|golden food', 'emperor': r'emperor|showdown',
 'spelunking': r'spelunk|lunarheim|amber|\bdepth', 'research': r'research|observation|magnifier|monocle|grid', 'gallery': r'gallery|trophy|trophies|nametag',
 'legend_talents': r'legend talent', 'coral_reef': r'coral', 'zenith_market': r'zenith', 'clam_work': r'clam ?works?|pearls?', 'advice_fish': r'advice fish|doodlefish',
 'minehead': r'minehead|mine ?sweeper', 'glimbo': r'glimbo', 'sushi': r'sushi', 'jelly_operator': r'jelly operator|jellofish|obstruction', 'menagerie': r'menagerie|\blumi\b|shells?',
 'the_button': r'the button', 'upgrade_vault': r'upgrade vault|\bvault\b', 'grimoire': r'grimoire|\bbones?\b|wraith|femur|ribcage', 'compass': r'compass|tempest|medallion|abomination|\bdust\b',
 'tesseract': r'tesseract|arcanist|tachyon', 'royal_armory': r'royal guardian|\brg\b|outpost|armory|orblet|barracks', 'achievements': r'achievement', 'merits': r'merit',
 'gem_shop': r'gem shop|\bgems?\b', 'statues': r'statue|onyx', 'cards': r'\bcards?\b|card set|card preset', 'drop_rate': r'drop ?rate|\bdr\b',
 'money': r'\bmoney\b|\bcoins?\b|cash', 'class_exp': r'class exp|exp gain', 'damage': r'\bdamage\b|\bdmg\b', 'talent_points': r'talent point',
 'greenstacks': r'green ?stack', 'storage': r'storage|\bbags?\b|inventory|carry cap', 'masterclass': r'master ?class', 'w7_push': r'world 7|\bw7\b|shimmerfin',
}
KWC = {k: re.compile(v, re.I) for k, v in KW.items()}
LINE = re.compile(r'^\[(\d\d):(\d\d):(\d\d)\] (.*)$')

def build():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'sources', 'creators', '*', 'transcripts', '*.txt'))):
        creator = f.split(os.sep)[-3]; stem = os.path.basename(f)[:-4]; date, vid = stem.split('_', 1)
        head, chunk, start = {}, [], None
        with open(f, encoding='utf-8', errors='ignore') as fh:
            body = False
            for ln in fh:
                ln = ln.rstrip('\n')
                if not body:
                    if ln == '---': body = True
                    elif ':' in ln: k, v = ln.split(':', 1); head[k.strip()] = v.strip()
                    continue
                m = LINE.match(ln)
                if not m: continue
                sec = int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3])
                if start is None: start = sec
                chunk.append(m[4])
                if sec - start >= 60:
                    out.append(_mk(creator, date, vid, head.get('title', ''), start, chunk)); chunk, start = [], None
            if chunk: out.append(_mk(creator, date, vid, head.get('title', ''), start or 0, chunk))
    with gzip.open(IDX, 'wt', encoding='utf-8') as g: json.dump(out, g)
    print(f'indexed {len(out)} chunks from {len(set(c["v"] for c in out))} videos -> {IDX}')

def _mk(creator, date, vid, title, start, lines):
    text = ' '.join(lines)
    return {'c': creator, 'd': date, 'v': vid, 'ti': title, 't': start, 'x': text, 's': [k for k, r in KWC.items() if r.search(text)]}

def find(system, creator=None, since=None, words=None, top=15):
    data = json.load(gzip.open(IDX, 'rt', encoding='utf-8'))
    w = re.compile(words, re.I) if words else None
    hits = [c for c in data if system in c['s'] and (not creator or c['c'] == creator)
            and (not since or (c['d'] != 'nodate' and c['d'] >= since)) and (not w or w.search(c['x']))]
    pr = {'griffybit': 0, 'pulseidle': 1, 'nocturne': 2}
    hits.sort(key=lambda c: (pr[c['c']], '\uffff' if c['d'] == 'nodate' else ''.join(chr(255 - ord(ch)) for ch in c['d']), c['t']))
    print(f'{len(hits)} chunks for {system}' + (f' ({creator})' if creator else ''))
    for c in hits[:top]:
        s = int(c['t']); print(f"\n[{c['c']} {c['d']} {c['v']} {s//3600:02d}:{s%3600//60:02d}:{s%60:02d}] {c['ti'][:60]}\n  {c['x'][:600]}")

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] == 'build': build()
    elif a[0] == 'find':
        opt = {a[i][2:]: a[i + 1] for i in range(2, len(a) - 1, 2) if a[i].startswith('--')}
        find(a[1], opt.get('creator'), opt.get('since'), opt.get('words'), int(opt.get('top', 15)))
