"""Build/refresh the brain: one linked note per system (Obsidian-compatible markdown).
Only the AUTO block (between the markers) is rewritten; everything else in a note is curated and kept.
Usage: python3 tools/build_brain.py
"""
import re, yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRAIN = ROOT / 'brain'; SYS = BRAIN / 'systems'; SYS.mkdir(parents=True, exist_ok=True)
A0, A1 = '<!-- AUTO:START (tools/build_brain.py rewrites this block) -->', '<!-- AUTO:END -->'

idx = yaml.safe_load(open(ROOT / 'model' / 'system_index.yaml'))
# systems the index never had (Zack 2026-11-21: nothing was checking these)
EXTRA = {
    'weekly_boss': 'W2 weekly boss', 'world_bosses': 'World bosses (daily/weekly)', 'anvil': 'Anvil production',
    'poppy': 'Poppy (W1 clicker)', 'bubba': 'Bubba (W1 clicker)', 'snail_mail': 'Snail mail', 'palette': 'Palette / Black Star',
    'talents': 'Talent points (both presets)', 'super_talents': 'Super talents (both presets)',
}
# planner module -> system slug(s) it covers
PLANNER = {
    'sailing': ['sailing'], 'farming': ['farming'], 'cooking': ['cooking', 'meals'], 'divinity': ['divinity'], 'breeding': ['breeding'],
    'printer': ['printer'], 'alchemy': ['alchemy_bubbles', 'alchemy_cauldrons', 'alchemy_vials', 'alchemy_p2w'], 'stamps': ['stamps'],
    'greenstacks': ['greenstacks'], 'statues': ['statues'], 'refinery': ['refinery'], 'worship': ['worship'], 'compass': ['compass'],
    'grimoire': ['grimoire'], 'deathnote': ['death_note'], 'equinox': ['equinox'], 'atom': ['atom_collider'], 'saltlick': ['saltlick'],
    'armor': ['armor_sets'], 'vault': ['vault'], 'tesseract': ['tesseract'], 'royal_armory': ['royal_armory'],
    'lab': ['lab_bonuses', 'lab_chips', 'lab_jewels', 'lab_mainframe'], 'buildings': ['construction_buildings'], 'gaming': ['gaming'],
    'sneaking': ['sneaking'], 'summoning': ['summoning'], 'spelunking': ['spelunk', 'caverns'],
    'w7minis': ['legend_talents', 'jelly_operator', 'clam_work', 'sushi_station', 'minehead', 'glimbo', 'zenith_market', 'the_button'],
    'menagerie': ['menagerie'], 'research': ['research'], 'reef': ['coral_reef', 'dancing_coral', 'divinity_coral_kid'], 'gallery': ['gallery'],
    'emperor': ['emperor'], 'islands': ['islands'], 'arcade': ['arcade'], 'owl': ['owl'], 'killroy': ['killroy'], 'hole': ['caverns'],
    'slab': ['slab'], 'beanstalk': ['beanstalk'], 'capevine': ['cape_vine'], 'shops': ['gemshop', 'ballot', 'meritocracy'], 'tome': ['tome'],
    'maint': ['rift', 'star_signs'], 'postoffice': ['post_office'], 'supertalents': ['super_talents'], 'prayers': ['prayers'],
}
# AutoReview bookkeeping entries, not game systems: never counted as holes
NOT_SYSTEM = {'data_source', 'version', 'tabbed_advice_groups', 'max_subgroups', 'manual_tome_score', 'reset_counters', 'library_group_characters', 'item_filter', 'highest_dmg'}
cover = {}
for mod, slugs in PLANNER.items():
    for s in slugs: cover.setdefault(s, []).append(f'model/{mod}.py')

TEMPLATE = """---
name: {slug}
description: {title}: state, how it works, links, plan, today
---
# {title}

{auto}

## How it works (mechanics, multipliers, formulas; cite source)

## Links
- Feeds ->
- Fed by <-
- Uses (reserve-checked) :
- Unlocks / is gated by :

## Creator rule of thumb (Griffy > Pulse = Nocturne; newest wins)

## Plan
- Now:
- Next:
- Stop point (bottleneck / slow burn):
- Waiting on:

## Today (written by the decision layer each pull)
"""

def main():
    import json
    try: GJ = json.load(open(ROOT / 'model' / 'goals.json'))['systems']
    except Exception: GJ = {}
    gaps = [l for l in (ROOT / 'sources' / 'findings' / 'gaps.md').read_text().splitlines() if l.startswith('|') and '| open |' in l]
    check = (BRAIN / 'checklist_2026-11-21.md').read_text().splitlines() if (BRAIN / 'checklist_2026-11-21.md').exists() else []

    def words(slug): return {w for w in slug.split('_') if len(w) > 3} | {slug.replace('_', ' ')}


    rows = []
    for slug in [s for s in list(idx) + list(EXTRA) if s not in NOT_SYSTEM]:
        e = idx.get(slug, {}) if slug in idx else {}
        title = EXTRA.get(slug) or slug.replace('_', ' ').title()
        w = words(slug)
        g = [x.split('|')[1].strip() + ': ' + x.split('|')[4].strip() for x in gaps if any(t in x.lower() for t in w)]
        ch = [x.strip()[6:] for x in check if f'[[{slug}]]' in x]
        tr = e.get('transcripts'); tr = tr if isinstance(tr, dict) else {}
        auto = '\n'.join([A0,
            f"- GOAL: {GJ[slug]['summary'] if slug in GJ else 'no wired GOAL block'}",
            f"- Owners: {', '.join(e.get('owners') or []) or 'UNASSIGNED'}",
            f"- Toolbox: {'; '.join(e.get('toolbox') or []) or 'none mapped'}",
            f"- AutoReview: {', '.join(e.get('autoreview') or []) or 'not rated'}",
            f"- Planner: {', '.join(cover.get(slug, [])) or 'NONE (nothing checks this yet)'}",
            f"- Creator rows: {tr.get('tagged_rows', 0)}",
            f"- Findings: {', '.join(e.get('findings') or []) or 'none'}",
            *( [f"- Open gaps: " + ' | '.join(g)] if g else [] ),
            *( [f"- Checklist: " + ' | '.join(ch)] if ch else [] ),
            A1])
        p = SYS / f'{slug}.md'
        if p.exists():
            t = p.read_text(); t = re.sub(re.escape(A0) + r'.*?' + re.escape(A1), lambda m: auto, t, flags=re.S)
        else:
            t = TEMPLATE.format(slug=slug, title=title, auto=auto)
        p.write_text(t)
        curated = bool(re.search(r'## Plan\n- Now: \S', t))
        rows.append((slug, title, bool(cover.get(slug)), curated, len(g), bool(e.get('owners'))))

    out = ['---', 'name: brain-index', 'description: Every system, whether anything checks it, whether it has a plan', '---',
           '# Brain index', '', '| system | owner | planner | plan written | open gaps |', '|---|---|---|---|---|']
    for slug, title, pl, cur, ng, own in sorted(rows, key=lambda r: (r[2], r[3], r[0])):
        out.append(f"| [[{slug}]] | {'yes' if own else 'NO'} | {'yes' if pl else 'NO'} | {'yes' if cur else 'no'} | {ng or ''} |")
    n = len(rows)
    out += ['', f"{n} systems: {sum(r[2] for r in rows)} with a planner, {sum(r[3] for r in rows)} with a written plan, {sum(not r[5] for r in rows)} unowned."]
    (BRAIN / 'index.md').write_text('\n'.join(out) + '\n')
    print(out[-1])

if __name__ == '__main__':
    main()
